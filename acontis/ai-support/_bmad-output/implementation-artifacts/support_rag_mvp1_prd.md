# Support RAG Service — PRD MVP 1

Scope: this document covers **only the Knowledge Retrieval (RAG) component (C)** from `support_prd.md` §12.5. It is the basis for the first implementation plan.

---

## 1. Intro — Fastest path to a Claude Projects-quality RAG service

Looking at `support_prd.md` (specifically component **C – Knowledge Retrieval** in §12.5 and the recommended stack in §8), here is the minimum-effort recipe.

### 1.1 TL;DR

Use **R2R** or **RAGFlow** as a turn-key "RAG-as-a-service" container — both expose exactly the `POST /rag/retrieve` + `POST /rag/index` REST surface the PRD requires (§12.5), and ship hybrid search + reranking + structured chunking out of the box. You wrap them behind your `KnowledgeRetrieval` Protocol and you're done.

If you must DIY (more control, still small): **LlamaIndex + Qdrant + bge-reranker-v2-m3 + LiteLLM** — this is the PRD's explicit recommendation in §8 (`support_prd.md` line 215-231).

### 1.2 Quality vs. Claude Projects

Claude Projects basically does: chunking → embedding → dense retrieval → stuffing into Claude's huge context. To **match or beat** it you only need three things, all available off-the-shelf:

1. **Strong embedder** — `bge-m3` (local via Ollama) or `voyage-3-large` (web). Both outperform Anthropic's internal embedder on MTEB.
2. **Hybrid + rerank** — Claude Projects does *not* do this. Adding `bge-reranker-v2-m3` already puts you ahead on context precision (§16 acceptance criterion: ≥10% over dense-only).
3. **Claude Opus as `answer_llm`** — same generator quality as Projects.

So "comparable to Claude Projects" is actually a *low* bar; the PRD's default stack exceeds it.

### 1.3 Recommended fastest setup (1–2 days)

#### Option A — Drop-in service (easiest)

```bash
docker run -p 7272:7272 sciphiai/r2r:latest
```

R2R gives you:

- Hybrid (dense + BM25) retrieval
- Reranking
- Ingestion API (`POST /documents`)
- Auth, multi-tenancy
- OpenAI-compatible LLM config → point at LiteLLM or Anthropic directly

Then write a ~50-line adapter implementing the `KnowledgeRetrieval` Protocol from `support_prd.md` §12.5 that calls R2R's REST API. Swap-out path (FR contract requirement) is preserved.

**RAGFlow** is the alternative if your KB is PDF-heavy with tables/layouts — its DeepDoc parser is the best open-source layout-aware chunker available (covers FR-13).

#### Option B — LlamaIndex assembly (PRD's official pick, §8)

```bash
pip install llama-index qdrant-client litellm sentence-transformers
docker run -p 6333:6333 qdrant/qdrant
ollama pull bge-m3
```

Then ~150 lines of Python:

- `QdrantVectorStore` with hybrid mode (`enable_hybrid=True`)
- `SentenceTransformerRerank(model="BAAI/bge-reranker-v2-m3", top_n=6)`
- `HyDEQueryTransform` for FR-14
- All LLM/embedding calls routed through LiteLLM proxy (FR-22, FR-23, and the §12.5 hard rule that *all internal LLM calls go through the LLM Gateway*)

LlamaIndex's `RetrieverQueryEngine` composes these in ~20 lines.

### 1.4 Critical things not to skip

From `support_prd.md`, the things that distinguish "production-grade" from "demo":

1. **Stable chunk IDs** (§12.5 contract guarantee) — every chunk needs a deterministic `id` resolvable to a source URL/ticket so citations (FR-17) work and `delete()` cascades work (§13 right-to-erasure).
2. **All internal LLM calls through the LLM Gateway** (§12.5 last bullet, §12.6) — query rewriting, HyDE, LLM-as-reranker must call LiteLLM, not provider SDKs directly. Otherwise `allow_remote: false` (FR-23) is unenforceable.
3. **Two namespaces** (`kb`, `tickets`) — FR-10 requires them indexed separately but retrievable jointly. Both R2R and LlamaIndex support this trivially via metadata filters.
4. **Capabilities advertised in `/health`** — so the orchestrator knows whether to expect hybrid/graph (§12.5 contract test).

### 1.5 What to defer

- **GraphRAG / LightRAG** — explicitly Phase 3 (§10). Skip for MVP.
- **Ragas eval harness** — Phase 2. Add once you have a golden set.
- **Curation pipeline** — Phase 2. For MVP, manually mark tickets indexable.

### 1.6 Recommendation

The PRD's §8 picks LlamaIndex; R2R is strictly faster to stand up and meets the same contract. Both meet "comparable to Claude Projects". This MVP 1 PRD goes with **Option B (LlamaIndex)** because it gives the team direct control over hybrid/rerank/HyDE wiring, fits the PRD §8 default stack, and keeps the `KnowledgeRetrieval` boundary owned in our codebase rather than behind a third-party service.

---

## 2. PRD — RAG Service MVP 1 (Option B: LlamaIndex stack)

### 2.1 Purpose & non-goals

**Purpose.** Deliver a self-contained `KnowledgeRetrieval` service implementing `support_prd.md` §12.5 with the LlamaIndex + Qdrant + bge-reranker + LiteLLM stack. Quality target: at least matches Claude Projects on a small internal eval set; hybrid + reranker beats dense-only by ≥10% context precision (§16).

**Non-goals (MVP 1).**

- No GraphRAG / LightRAG (Phase 3).
- No Ragas-automated CI eval (Phase 2; manual eval set only).
- No curation pipeline / closed-ticket auto-ingestion (Phase 2; ingestion is admin-driven).
- No web UI (admin uses REST/CLI).
- No multi-tenant auth beyond a single shared service token.
- No incremental re-embedding on model change (full reindex acceptable).

### 2.2 Position in the system

This service implements component **C** only. It depends on component **D (LLM Gateway / LiteLLM)** for every embedding and chat-completion call (FR-22, FR-23, §12.5 last bullet). It is consumed by the **Orchestrator (E)** via REST and optionally by other workflows via MCP.

```text
Orchestrator ──► [ RAG Service (this PRD) ] ──► LLM Gateway (LiteLLM) ──► Ollama / Anthropic / …
                       │
                       ├── Qdrant (vectors + sparse)
                       └── local cross-encoder (bge-reranker-v2-m3)
```

### 2.3 Functional requirements

Mapped to `support_prd.md` FR-IDs where applicable.

#### 2.3.1 Retrieval API (FR-11, FR-12, FR-14, FR-15, FR-17)

- **R-1** Implement `POST /rag/retrieve` exactly per `support_prd.md` §12.5 (`RetrievalRequest` → `RetrievalResponse`).
- **R-2** Hybrid retrieval (dense + sparse) is **on by default**. Fusion via Reciprocal Rank Fusion (RRF). Top-k upper bounds: `top_k_dense=30`, `top_k_sparse=30`, `top_k_final=6` (config-driven, defaults match `support_prd.md` §9).
- **R-3** Cross-encoder reranking via `BAAI/bge-reranker-v2-m3` is **on by default**, applied after fusion, before truncation to `top_k_final`.
- **R-4** Query rewriting: when `rewrite=true`, generate up to 3 alternative queries via the `retrieval_llm` slot of the LLM Gateway. HyDE optional (config flag, default off in MVP 1).
- **R-5** Metadata filtering: `filters` field accepts equality and `$in` predicates over `product`, `lang`, `created_at` (range), `status`, `namespace`. Translated to Qdrant filter expressions.
- **R-6** Every returned `Chunk` carries: stable `id`, `parent_id`, `text`, `score` (post-rerank), `metadata` including `source_uri` (or `ticket_id`), `namespace`, `created_at`, `chunker_version`.
- **R-7** `min_score` truncates after reranking; empty result is a valid response (caller decides degrade behavior per `support_prd.md` §14).

#### 2.3.2 Ingestion API (FR-10, FR-13, FR-18 partial)

- **R-8** `POST /rag/index/{namespace}` accepts a list of `Document` (`id`, `text`, `metadata`). Two namespaces supported: `kb` and `tickets` (FR-10).
- **R-9** Chunking strategy:
  - `kb` namespace: layout-aware sentence-window splitter (LlamaIndex `SentenceWindowNodeParser`) with `window_size=3`, `chunk_size≈512` tokens.
  - `tickets` namespace: Q&A-pair chunking — one chunk per `(question, resolution)` pair from a closed ticket, plus one summary chunk per ticket (FR-13).
- **R-10** Chunk IDs are **deterministic**: `sha256(namespace + parent_id + chunk_index + chunker_version)[:16]`. Re-ingesting the same document with the same chunker produces identical IDs (idempotent upsert).
- **R-11** `DELETE /rag/index/{namespace}` accepts a list of `parent_id`s and removes all chunks (vectors + sparse entries) belonging to those parents. Required for `support_prd.md` §13 right-to-erasure cascade.
- **R-12** Incremental indexing supported at the document level: re-ingesting with a new `parent_id` adds; re-ingesting an existing `parent_id` replaces its chunks atomically (delete-then-insert in one Qdrant operation). Full reindex is *not* automated in MVP 1 but a `scripts/reindex.py` is shipped.

#### 2.3.3 Health & capabilities (§12.5 contract)

- **R-13** `GET /rag/health` returns:

  ```json
  {
    "status": "ok",
    "version": "<semver>",
    "contract_version": "1.0",
    "capabilities": {
      "hybrid": true,
      "rerank": true,
      "graph": false,
      "namespaces": ["kb", "tickets"]
    },
    "models": {
      "embedding": "<from LLM Gateway describe()>",
      "retrieval_llm": "<from LLM Gateway describe()>",
      "reranker": "BAAI/bge-reranker-v2-m3"
    },
    "stores": { "qdrant": "ok" }
  }
  ```

- **R-14** Capabilities advertised in `health()` MUST match runtime behavior (`support_prd.md` §12.10 contract test).

#### 2.3.4 LLM Gateway integration (FR-22, FR-23, §12.5 last bullet)

- **R-15** All embedding calls (indexing + query) go through the LLM Gateway's `/v1/embeddings` endpoint with `X-Slot: embedding`.
- **R-16** All retrieval-side chat completions (query rewriting, HyDE) go through `/v1/chat/completions` with `X-Slot: retrieval_llm`.
- **R-17** No direct provider SDK imports (`anthropic`, `openai`, `ollama` clients) anywhere in the RAG service code. Enforced by import-lint rule in CI.
- **R-18** Cross-encoder reranking runs **locally in-process** via `sentence-transformers` (exempt per §12.5 — not a chat completion).

#### 2.3.5 MCP surface (`support-rag` server, §12.8)

- **R-19** Expose the three tools: `rag.retrieve`, `rag.index` (admin-scoped), `rag.health`. Tool schemas generated from the same Pydantic models used by REST.
- **R-20** `rag.index` requires an elevated bearer token; `rag.retrieve` accepts the standard service token.

### 2.4 Non-functional requirements

- **NFR-1 Latency.** `retrieve` p95 ≤ 2.0 s for `top_k_final=6` on a 100k-chunk corpus, with rewriting + reranking enabled, against local Ollama embedder. (Contributes to the orchestrator's overall §NFR-2 budget.)
- **NFR-2 Throughput.** ≥ 5 concurrent `retrieve` calls without queueing on a single node (uvicorn workers ≥ 4).
- **NFR-3 Privacy.** Service runs on-prem; only outbound calls are to the LLM Gateway. No direct internet access required.
- **NFR-4 Observability.** Every `retrieve` and `index` call emits an OpenTelemetry span; all LLM Gateway calls are correlated to the parent span via traceparent header. Langfuse trace ID, when provided in headers, is propagated.
- **NFR-5 Reproducibility.** `chunker_version` and embedding-model identifier are stamped on every chunk's metadata. A change in either bumps the version and triggers (manual) reindex.
- **NFR-6 Reliability.** Service is stateless except for Qdrant. Restart safe. Ingestion is idempotent (R-10).
- **NFR-7 Security.** Bearer token on every endpoint; admin endpoints (`index`, `delete`) require elevated token. mTLS optional (deployment concern).

### 2.5 Architecture (MVP 1)

```text
                   HTTP / MCP
                       │
                       ▼
        ┌─────────────────────────────────┐
        │  FastAPI app (this service)     │
        │  ┌───────────────────────────┐  │
        │  │ Routers: retrieve, index, │  │
        │  │          delete, health   │  │
        │  └───────────┬───────────────┘  │
        │              ▼                  │
        │  ┌───────────────────────────┐  │
        │  │ RetrievalPipeline         │  │
        │  │  - QueryRewriter (LLM GW) │  │
        │  │  - HybridRetriever        │  │
        │  │     dense + BM25 (Qdrant) │  │
        │  │  - RRF Fusion             │  │
        │  │  - CrossEncoderReranker   │  │
        │  └───────────┬───────────────┘  │
        │              │                  │
        │  ┌───────────▼───────────────┐  │
        │  │ IngestionPipeline         │  │
        │  │  - Chunker (per namespace)│  │
        │  │  - Embedder (LLM GW)      │  │
        │  │  - Qdrant upsert (vec+bm25)│ │
        │  └───────────────────────────┘  │
        └────────┬───────────────┬────────┘
                 │               │
                 ▼               ▼
         ┌──────────────┐  ┌──────────────┐
         │  Qdrant      │  │ LLM Gateway  │
         │  (hybrid)    │  │  (LiteLLM)   │
         └──────────────┘  └──────────────┘
```

Key library choices:

- **FastAPI** — REST surface.
- **LlamaIndex** — `QdrantVectorStore(enable_hybrid=True)`, `SentenceWindowNodeParser`, `HyDEQueryTransform` (Phase 2-ready), retrievers, RRF.
- **Qdrant** — vector + native sparse (BM25/SPLADE) in one store; metadata filters.
- **sentence-transformers** — local cross-encoder reranker.
- **httpx** — calls to LLM Gateway (no provider SDKs).
- **Pydantic v2** — schemas shared between REST and MCP.
- **OpenTelemetry SDK** + Langfuse compatibility (header propagation only in MVP 1).

### 2.6 Configuration

A single `config.yaml` (overridable via env vars, prefix `RAG_`). Example:

```yaml
service:
  bind: 0.0.0.0:8080
  service_token_env: RAG_SERVICE_TOKEN
  admin_token_env: RAG_ADMIN_TOKEN

llm_gateway:
  base_url: http://litellm:4000
  timeout_s: 30
  embedding_slot: embedding
  retrieval_slot: retrieval_llm

qdrant:
  url: http://qdrant:6333
  collection_prefix: support_rag_
  vector_size: 1024
  distance: cosine

retrieval:
  hybrid: true
  top_k_dense: 30
  top_k_sparse: 30
  top_k_final: 6
  fusion: rrf
  rrf_k: 60
  query_rewrite:
    enabled: true
    n_alternatives: 3
  hyde:
    enabled: false
  reranker:
    model: BAAI/bge-reranker-v2-m3
    device: cpu

chunking:
  kb:
    strategy: sentence_window
    chunk_size: 512
    window_size: 3
  tickets:
    strategy: qa_pair

observability:
  otel_endpoint: http://otel-collector:4317
  service_name: support-rag
```

The collection naming convention is `<prefix><namespace>` (e.g. `support_rag_kb`, `support_rag_tickets`). One Qdrant collection per namespace; cross-namespace retrieval issues parallel queries and merges via RRF.

### 2.7 Data model

#### 2.7.1 Chunk metadata (stored alongside vectors in Qdrant)

| Field             | Type    | Notes                                   |
|-------------------|---------|-----------------------------------------|
| `parent_id`       | string  | Source document or ticket ID            |
| `namespace`       | string  | `kb` or `tickets`                       |
| `source_uri`      | string  | URL or ticket reference                 |
| `product`         | string? | Filterable                              |
| `lang`            | string? | Filterable                              |
| `created_at`      | int     | Unix epoch; range filterable            |
| `status`          | string? | (`tickets` only)                        |
| `chunk_index`     | int     | Position within parent                  |
| `chunker_version` | string  | e.g. `kb-v1`, `tickets-v1`              |
| `embedding_model` | string  | Stamped from gateway response           |

#### 2.7.2 Wire schemas

Match `support_prd.md` §12.5 exactly. JSON shape derived from the Python `@dataclass` definitions; Pydantic models in code carry the same field names.

### 2.8 Acceptance criteria (MVP 1)

1. **Contract test pass.** All `KnowledgeRetrieval` contract tests from `support_prd.md` §12.10 pass:
   - hybrid beats dense-only on the golden set,
   - chunk IDs stable across two ingest runs of the same document,
   - capabilities advertised in `health()` match runtime behavior.
2. **Quality.** On a small (≥ 30 question) internal eval set, hybrid + reranker beats dense-only by ≥ 10% context precision (matches `support_prd.md` §16). Manual labeling acceptable in MVP 1.
3. **Latency.** `retrieve` p95 ≤ 2.0 s under NFR-1 conditions.
4. **Right-to-erasure.** `DELETE /rag/index/tickets` with a `parent_id` removes all corresponding chunks; subsequent `retrieve` for content from that ticket returns nothing.
5. **Privacy switch.** With `allow_remote: false` configured on the LLM Gateway, indexing and retrieval still work end-to-end with local embedder + local retrieval LLM only.
6. **No provider SDKs.** CI import-lint passes (R-17).
7. **MCP server.** `rag.retrieve` and `rag.health` are callable from Claude Desktop / Cursor with the standard service token.

### 2.9 Out-of-scope (explicit deferrals)

- HyDE on by default (config exists, off in MVP 1).
- LLM-as-reranker (cross-encoder only).
- GraphRAG / entity extraction.
- Automated curation of closed tickets.
- Ragas eval harness in CI.
- Multi-tenant ACL beyond the two-token model.
- Cost/budget guardrails on retrieval LLM (handled by LLM Gateway).
- Web admin UI.

### 2.10 Risks (MVP-1 specific)

| Risk | Mitigation |
|---|---|
| Qdrant hybrid sparse mode immature for some payloads | Pin Qdrant version known-good; fallback to LlamaIndex `BM25Retriever` over an in-memory store if needed (still hybrid, only ops change). |
| Reranker latency on CPU dominates p95 | Make `top_k` after fusion tunable; allow GPU device in config; document CPU baseline. |
| LLM Gateway becomes a bottleneck for query rewriting | Cache rewrites by query hash for N minutes (small in-memory LRU). |
| Chunker version churn forces reindex | Stamp `chunker_version` per chunk; ship a `scripts/reindex.py`; document reindex as an accepted operational cost in MVP 1. |
| Provider-SDK creep (devs importing `openai` directly) | Import-lint rule + code review checklist. |

### 2.11 Deliverables

- `support_rag/` Python package (FastAPI app + LlamaIndex pipelines).
- `Dockerfile` and `docker-compose.yaml` (service + Qdrant; LLM Gateway expected as an external dependency).
- `config.example.yaml`.
- `mcp/support-rag/` MCP server descriptor + entrypoint.
- `tests/` — unit + the shared contract test suite from `support_prd.md` §12.10.
- `scripts/reindex.py`, `scripts/seed_kb.py`.
- `README.md` covering local bring-up (Qdrant + LiteLLM + Ollama + this service).
- A small labeled eval set (≥ 30 Q/A pairs) under `eval/golden/`.

### 2.12 Implementation phasing inside MVP 1

This is intentionally fine-grained so the implementation plan can map 1:1 onto it.

1. **Skeleton.** FastAPI app, config loader, health endpoint advertising capabilities, auth middleware, OTel wiring.
2. **LLM Gateway client.** Thin `httpx` wrapper for `/v1/embeddings` and `/v1/chat/completions` with slot header; no provider SDKs.
3. **Qdrant integration.** Collection bootstrap per namespace; LlamaIndex `QdrantVectorStore(enable_hybrid=True)` plumbed in.
4. **Ingestion pipeline.** Chunkers per namespace, deterministic IDs, idempotent upsert, `index` + `delete` endpoints.
5. **Retrieval pipeline.** Dense + sparse retrievers, RRF fusion, metadata filters, `min_score`.
6. **Query rewriting.** Retrieval-LLM-driven rewrite (n=3), merge results pre-rerank.
7. **Cross-encoder reranker.** Local model load, batched scoring, top_k_final truncation.
8. **MCP server.** Tools generated from Pydantic schemas; admin scope on `rag.index`.
9. **Contract tests + eval set.** Wire §12.10 tests; produce hybrid-vs-dense delta report.
10. **Hardening.** Idempotency tests, restart safety, error paths, README and compose file.

