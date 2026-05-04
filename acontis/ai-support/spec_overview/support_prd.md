# Support Use Case — Product Requirements Document (PRD)

AI-assisted first-response drafting for Zammad tickets, grounded in a sophisticated local RAG system, with mandatory human review before any customer-facing reply.

This PRD complements `support_usecase.md` and is focused on **minimal-effort implementation**: maximize reuse of existing open-source building blocks; build only the glue.

---

## 1. Goals

- Speed up support by drafting answers from internal knowledge and historical tickets.
- Keep customer PII out of retrieval and prompts wherever feasible.
- Ensure every customer-facing message is reviewed and sent by a human engineer.
- Keep the RAG component **as sophisticated as possible** (hybrid search, reranking, structured chunking, optional GraphRAG) while staying configurable and replaceable.
- Make **embedding model**, **retrieval-side LLM** (e.g., for query rewriting / routing / reranking) and **answer-generation LLM** independently configurable: each can be **local** (Ollama / vLLM) or a **web** model (Anthropic Claude Opus, OpenAI, etc.).

## 2. Scope

In-scope:

- Zammad integration (ticket events, internal note creation, reassignment).
- PII anonymization pipeline.
- RAG indexing of historical tickets and company knowledge (docs, FAQs, internal articles).
- Draft generation and storage as internal note.
- Configuration layer for swapping LLMs and embedding models.

Out-of-scope (initially):

- Auto-sending answers to customers.
- Multi-language answer generation beyond what the chosen LLM supports natively.
- Voice / phone channels.

## 3. Actors

- **Zammad** — ticketing system (source of truth).
- **AI agent (Zammad user)** — owns tickets during automated processing.
- **Anonymization service** — masks PII before RAG / LLM use.
- **RAG service** — indexes and retrieves grounded passages.
- **LLM(s)** — configurable; one for retrieval-side reasoning, one for final draft.
- **Human support engineer** — reviews and sends.

## 4. Functional Requirements

### 4.1 Ticket Lifecycle

- **FR-1** New ticket → automatically assigned to AI agent user in Zammad.
- **FR-2** System reads ticket body and metadata via Zammad REST API.
- **FR-3** After draft generation, the draft is posted as an **internal note** (never as a customer-facing article).
- **FR-4** Ticket is reassigned to the configured human group/queue.
- **FR-5** Full audit trail: anonymized query, retrieved chunk IDs, model identifiers, timestamps, and prompt hash are stored on the ticket (internal note or linked record).

### 4.2 Anonymization

- **FR-6** Detect and mask: names, emails, phone numbers, postal addresses, account/customer IDs, IBANs, IPs, and configurable custom patterns (e.g., internal serial numbers).
- **FR-7** Anonymization is **deterministic per ticket** (same entity → same placeholder, e.g., `<PERSON_1>`) so the LLM can refer back consistently.
- **FR-8** Mapping table (placeholder ↔ original) is kept **in-memory / encrypted at rest** and used only to re-personalize the final draft for the human reviewer. It is **never** sent to remote LLMs.
- **FR-9** Allowlist for technical terms that look like PII (e.g., product SKUs) must be supported.

### 4.3 RAG (sophisticated)

- **FR-10** **Two corpora**, indexed separately and retrievable jointly:
  1. Historical tickets (curated, anonymized, tagged with resolution outcome).
  2. Company knowledge (docs, FAQs, internal articles, runbooks).
- **FR-11** **Hybrid retrieval**: dense (vector) + sparse (BM25), fused via Reciprocal Rank Fusion or weighted score.
- **FR-12** **Reranker** (cross-encoder or LLM-as-reranker) on top-k candidates.
- **FR-13** **Structured chunking**: layout-aware for docs (RAGFlow / Unstructured / Docling), Q&A-pair chunking for tickets.
- **FR-14** **Query transformation** before retrieval: query rewriting, HyDE, and/or multi-query expansion (uses the *retrieval-side LLM*).
- **FR-15** **Metadata filtering**: by product, language, date, ticket status.
- **FR-16** Optional **GraphRAG / knowledge-graph** layer for entity-rich domains (deferrable to phase 2).
- **FR-17** **Citations**: every retrieved chunk carries a stable source ID surfaced in the draft.
- **FR-18** **Incremental indexing**: new closed tickets are automatically added (after curation step) without full re-index.
- **FR-19** **Evaluation harness** (Ragas / TruLens) for context precision/recall and answer faithfulness.

### 4.4 LLM & Embedding Configuration

- **FR-20** Three independently configurable model slots:
  - `embedding_model` — for indexing and query embedding.
  - `retrieval_llm` — for query rewriting, reranking, routing (cheap/fast OK).
  - `answer_llm` — for the final draft (quality-first, e.g., Claude Opus).
- **FR-21** Each slot must support at minimum:
  - Local backends: **Ollama** and **vLLM** (OpenAI-compatible).
  - Web backends: **Anthropic** (Claude Opus / Sonnet), **OpenAI**, **Azure OpenAI**, **Google Gemini**, **Mistral**.
- **FR-22** Configuration via a single YAML/`.env` file; switching providers must require **no code changes**.
- **FR-23** A **privacy switch** per slot: `allow_remote: true|false`. If `false`, only local providers are accepted; system fails closed.
- **FR-24** Token/cost budget guardrails per slot (max tokens, monthly spend cap) with alerting.

### 4.5 Draft Generation

- **FR-25** Augmented prompt = anonymized question + top-k reranked chunks + style guide + few-shot examples.
- **FR-26** Draft must include: proposed answer, **citations**, and a short **confidence note** (uncertainty, missing info).
- **FR-27** Re-personalization (placeholder → real names) happens **after** the LLM call and **before** posting the internal note, so the engineer reads natural text.
- **FR-28** If retrieval confidence is below threshold, the note is marked “Low-confidence draft — knowledge gap suspected.”

## 5. Non-Functional Requirements

- **NFR-1 Privacy**: Default deployment runs fully on-prem; remote LLM calls only when explicitly enabled per slot.
- **NFR-2 Latency**: Draft posted within 60 s of ticket creation (p95) using local stack; ≤ 30 s with Claude Opus.
- **NFR-3 Reliability**: If any AI step fails, the ticket is reassigned to humans with an error note; no ticket is ever “stuck” on the AI agent.
- **NFR-4 Observability**: Structured logs + traces (OpenTelemetry / Langfuse). Every prompt/response captured with model, token count, cost, latency.
- **NFR-5 Reproducibility**: Pinned model versions and chunker versions in audit log.
- **NFR-6 Security**: Secrets via env/secret manager; mapping table encrypted; remote-LLM payloads logged only in anonymized form.
- **NFR-7 No auto-send**: Hard architectural guarantee — service has no permission to create customer-facing articles in Zammad.

## 6. Architecture (target)

```text
                ┌────────────────────────────────────────────────────────┐
                │                       Zammad                            │
Ticket events ──┤  Webhook / Trigger  ─────────────►   REST API           │
                └───────────┬─────────────────────────────────────────────┘
                            │ (assign to AI agent)
                            ▼
                ┌──────────────────────────────────┐
                │   Orchestrator (Python service)  │
                │   - listens to Zammad events     │
                │   - runs the pipeline            │
                └───┬──────────────────────────────┘
                    │
                    ▼
        ┌──────────────────────┐    ┌────────────────────────────┐
        │  Anonymizer          │    │  Config layer (LiteLLM)     │
        │  Microsoft Presidio  │    │  embedding / retrieval /    │
        │  + custom recognizers│    │  answer  →  Ollama|Claude|… │
        └─────────┬────────────┘    └────────────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────────────────────────────────┐
        │  RAG service (LlamaIndex or RAGFlow or Haystack)         │
        │  - hybrid search (Qdrant/Weaviate + BM25)                │
        │  - cross-encoder reranker (bge-reranker / Cohere)        │
        │  - query rewriting / HyDE  (retrieval_llm)               │
        │  - optional GraphRAG (LightRAG)                          │
        └─────────┬────────────────────────────────────────────────┘
                  │  top-k chunks + citations
                  ▼
        ┌──────────────────────────────────┐
        │  Answer generator (answer_llm)   │
        │  Claude Opus (web) | Ollama       │
        │  Llama 3.x / Qwen (local)         │
        └─────────┬────────────────────────┘
                  │  draft + citations
                  ▼
        ┌──────────────────────────────────┐
        │  Re-personalize (mapping table)  │
        └─────────┬────────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────────┐
        │  Zammad: post internal note,     │
        │  reassign to human group         │
        └──────────────────────────────────┘
```

## 7. Implementation Options (open source / starters)

### 7.1 Zammad integration

| Option | What it gives you | Notes |
|---|---|---|
| **`it-at-m/zammad-ai`** ([github.com/it-at-m/zammad-ai](https://github.com/it-at-m/zammad-ai)) | Python micro-service skeleton: Zammad event ingest (FastStream/Kafka), triage, response drafting, Qdrant RAG, Langfuse observability. | **Best starter** — closest match to our use case; fork and extend. |
| **Zammad 7.0+ native AI** ([zammad.com/en/artificial-intelligence](https://zammad.com/en/artificial-intelligence)) | Built-in summarization, writing assistant, “Bring Your Own AI” (OpenAI/Anthropic/Gemini/Mistral/Ollama). | Lowest effort if requirements fit; **does not give us a sophisticated custom RAG**. Use as a complement, not a replacement. |
| **Custom REST integration** | Full control via Zammad REST API + webhooks. | Use only if `zammad-ai` proves too constraining. |

### 7.2 PII anonymization

| Option | Notes |
|---|---|
| **Microsoft Presidio** ([github.com/microsoft/presidio](https://github.com/microsoft/presidio)) | Recommended. Analyzer + Anonymizer, custom `PatternRecognizer`, supports `mask`/`replace`/`encrypt`. Reversible via encryption for our re-personalization step. |
| **spaCy + custom regex** | Lightweight fallback if Presidio is overkill. |

### 7.3 RAG framework (sophisticated)

| Option | Strengths | Best for |
|---|---|---|
| **LlamaIndex** ([github.com/run-llama/llama_index](https://github.com/run-llama/llama_index)) | Best-in-class retrieval primitives: hybrid, reranking, query routing, multi-vector, knowledge graphs. Model-agnostic. | **Recommended core** for sophistication + flexibility. |
| **RAGFlow** ([github.com/infiniflow/ragflow](https://github.com/infiniflow/ragflow)) | Deep document understanding (tables, layout, images), built-in GraphRAG, ES/Infinity backends, web UI. | Use if document quality (PDFs, tables) is critical. Can be the engine; orchestrator calls its API. |
| **Haystack 2.x** ([github.com/deepset-ai/haystack](https://github.com/deepset-ai/haystack)) | Modular pipelines, strong eval, enterprise-grade. | Good fit for regulated environments. |
| **LightRAG** ([github.com/HKUDS/LightRAG](https://github.com/HKUDS/LightRAG)) | GraphRAG focus, entity-relationship retrieval. | Add-on for phase 2 if entity reasoning matters. |
| **R2R** ([github.com/SciPhi-AI/R2R](https://github.com/SciPhi-AI/R2R)) | Production RAG-as-a-service (auth, ingestion API, hybrid+graph). | Drop-in “RAG backend” option. |
| **Verba** (Weaviate) | Turn-key RAG UI on Weaviate. | Useful for the curation/admin UI. |

**Recommendation:** Start with **LlamaIndex + Qdrant + bge-reranker**. Keep the RAG service behind a thin internal API so it can later be swapped to RAGFlow or R2R without changing the orchestrator.

### 7.4 Vector store

| Option | Why |
|---|---|
| **Qdrant** | Native hybrid search, easy self-host, used by `zammad-ai`. **Recommended.** |
| **Weaviate** | Hybrid search + modules; good if Verba UI desired. |
| **pgvector / Postgres** | Simplest ops if you already run Postgres; hybrid via `tsvector`. |
| **Elasticsearch / OpenSearch** | If RAGFlow path is chosen. |

### 7.5 Embedding models (configurable)

- **Local (Ollama/HF)**: `nomic-embed-text`, `bge-m3`, `bge-large-en-v1.5`, `mxbai-embed-large`, `Qwen3-Embedding`.
- **Web**: `voyage-3-large`, `text-embedding-3-large` (OpenAI), Cohere `embed-v3`.
- Reranker: `bge-reranker-v2-m3` (local) or Cohere Rerank 3.5 (web).

### 7.6 LLMs (configurable)

- **Local**: Ollama (Llama 3.x, Qwen2.5, Mistral, Phi-4) or vLLM for higher throughput.
- **Web**: Anthropic **Claude Opus / Sonnet**, OpenAI GPT-4.x / o-series, Gemini, Mistral La Plateforme.

### 7.7 Provider abstraction layer

- **LiteLLM** ([github.com/BerriAI/litellm](https://github.com/BerriAI/litellm)) — unified OpenAI-compatible interface to 100+ providers. **Strongly recommended** to satisfy FR-20…FR-23 with minimal effort.
- Alternative: LlamaIndex / LangChain provider classes directly (less central control of cost/routing).

### 7.8 Observability & evaluation

- **Langfuse** ([github.com/langfuse/langfuse](https://github.com/langfuse/langfuse)) — self-hosted prompt/trace/cost tracking (already used by `zammad-ai`).
- **Ragas** / **TruLens** — RAG quality metrics.
- **OpenTelemetry** — service-level tracing.

## 8. Recommended minimal-effort stack

| Concern | Pick |
|---|---|
| Zammad glue | Fork **`it-at-m/zammad-ai`** |
| Anonymization | **Microsoft Presidio** + custom recognizers |
| RAG framework | **LlamaIndex** (hybrid + reranker + query rewrite) |
| Vector DB | **Qdrant** |
| Embeddings (default) | `bge-m3` via **Ollama** (configurable) |
| Reranker | `bge-reranker-v2-m3` (configurable to Cohere) |
| Retrieval LLM | Local Llama 3.1 8B via **Ollama** (configurable) |
| Answer LLM | **Claude Opus** via Anthropic API (configurable to local) |
| Provider router | **LiteLLM** |
| Observability | **Langfuse** + OpenTelemetry |
| Eval | **Ragas** |

This combination delivers FR-10…FR-24 with mostly configuration and ~glue code, not a from-scratch build.

## 9. Configuration sketch

```yaml
models:
  embedding:
    provider: ollama
    model: bge-m3
    allow_remote: false
  retrieval_llm:
    provider: ollama
    model: llama3.1:8b-instruct
    allow_remote: false
  answer_llm:
    provider: anthropic
    model: claude-opus-4
    allow_remote: true
    max_tokens: 1500
    monthly_budget_usd: 200

rag:
  vector_store: qdrant
  hybrid: true
  reranker:
    provider: huggingface
    model: BAAI/bge-reranker-v2-m3
  query_rewrite: true
  top_k_dense: 30
  top_k_sparse: 30
  top_k_final: 6

privacy:
  anonymizer: presidio
  custom_patterns:
    - name: ACCOUNT_ID
      regex: "ACC-\\d{6}"
  reversible: true

zammad:
  base_url: https://support.example.com
  ai_user: ai-agent
  human_group: L1-Support
```

## 10. Phasing

1. **Phase 1 (MVP, ~2–3 weeks):** Fork `zammad-ai`, plug in Presidio, swap default RAG to LlamaIndex+Qdrant with hybrid + reranker, wire LiteLLM, add config layer, post internal note + reassign. Default to fully-local; allow Claude Opus for `answer_llm`.
2. **Phase 2:** Query rewriting/HyDE, evaluation harness (Ragas), curation pipeline for closed tickets, Langfuse dashboards.
3. **Phase 3:** GraphRAG layer (LightRAG or RAGFlow GraphRAG), multi-tenant/product routing, cost-aware model routing in LiteLLM.

## 11. Risks & mitigations

- **Anonymization gaps** → human review is mandatory; Presidio + custom recognizers; periodic audits.
- **Hallucinated citations** → enforce that drafts cite only retrieved chunk IDs; reject drafts with unknown citations.
- **Vendor lock-in (Claude Opus)** → LiteLLM abstraction + per-slot `allow_remote` switch; keep a tested local fallback.
- **Stale knowledge** → incremental indexing + scheduled re-curation of closed tickets.
- **Privacy leakage to remote LLM** → anonymized text only; remote payload logging restricted to anonymized form; `allow_remote: false` enforces local-only.

## 12. Component Interface Contracts (pluggability)

The system is split into a small number of **major components** with clear, stable contracts at the boundary. Internals (sub-components) are deliberately hidden so a phased implementation can stand up the boundaries first and evolve internals later — including swapping a whole subsystem (e.g., LlamaIndex → RAGFlow) without touching anything else.

Each major contract is exposed through three equivalent surfaces:

1. **Python Protocol** (in-process; the source of truth).
2. **REST/JSON** (out-of-process; language-agnostic). **Implementation: FastAPI** (Pydantic v2 models are the single source of truth for request/response schemas, OpenAPI generation, and MCP tool descriptors).
3. **MCP server** (so an agent or Cursor/Claude Desktop can call it as a tool). The MCP server is a thin layer on top of the FastAPI app — either co-hosted in the same process or as a separate wrapper that calls the REST API — reusing the same Pydantic schemas.

Rule: **only major-component contracts cross process boundaries.** Sub-component interfaces exist inside a major component and may change freely as long as the major contract holds.

### 12.1 Major components (boundary-level)

Five major components only. Everything else is an internal detail.

| # | Major component | Responsibility (black-box) | Hidden sub-components | Default impl | Drop-in alternatives |
|---|---|---|---|---|---|
| A | **Ticket Gateway** | Source and sink of tickets: receive events, read ticket content, post internal notes, reassign. | Webhook listener, REST client, event normalizer, auth | Zammad REST adapter | Freshdesk, Jira SM, OTRS |
| B | **Privacy Service** | Turn raw text into anonymized text (and back, for the human-facing draft). Owns the placeholder mapping. | NER analyzer, custom recognizers, anonymizer engine, encrypted mapping store | Microsoft Presidio | spaCy+regex, AWS Comprehend, Cloud DLP |
| C | **Knowledge Retrieval (RAG)** | Given a query, return ranked, cited chunks. Owns the corpus and indexing lifecycle. | Chunker, **embedder**, **vector store**, sparse/BM25 index, query rewriter / HyDE, **reranker**, fusion, optional GraphRAG | LlamaIndex + Qdrant + bge-reranker | RAGFlow, R2R, Haystack, LightRAG |
| D | **LLM Gateway** | Single entry point for all chat completions. Enforces routing, privacy switch, budgets. | Provider adapters (Ollama, vLLM, Anthropic, OpenAI…), `retrieval_llm` slot, `answer_llm` slot, cost/quota guard, retry/cache | LiteLLM proxy | Native provider SDKs, Portkey, OpenRouter |
| E | **Orchestrator** | Drives the workflow: subscribe → anonymize → retrieve → draft → re-personalize → post note → reassign. Also exposes observability/eval. | Event loop, pipeline steps, tracer (Langfuse/OTel), evaluator (Ragas) | Python service (forked from `zammad-ai`) | Temporal/Prefect, n8n |

Why only five: each one can be **deployed as its own service** behind a stable API. A team can build/replace one without coordinating with the others. Sub-components (embedder, vector store, reranker, etc.) are intentionally **not** in this list — they live *inside* the Knowledge Retrieval boundary and are reachable only through it.

### 12.2 Phasing aligned to the boundaries

- **Phase 1 — define & stub the five contracts.** Implement the simplest viable backend per major component (e.g., dense-only retrieval, Presidio default rules, single LLM provider). Ship the end-to-end pipeline.
- **Phase 2 — deepen internals behind unchanged contracts.** Add hybrid + reranker + query rewriting inside Knowledge Retrieval. Add custom recognizers and reversible mapping inside Privacy. Add cost/quota and caching inside LLM Gateway. No orchestrator change.
- **Phase 3 — swap implementations.** Replace LlamaIndex with RAGFlow, or local LLM with Claude Opus, by changing config only.

### 12.2 Common types

```python
from typing import Protocol, Sequence, Mapping, Any, Literal
from dataclasses import dataclass

@dataclass(frozen=True)
class Document:
    id: str
    text: str
    metadata: Mapping[str, Any]      # source, product, lang, created_at, ticket_id, ...

@dataclass(frozen=True)
class Chunk(Document):
    parent_id: str
    score: float | None = None

@dataclass(frozen=True)
class AnonymizationResult:
    text: str                         # text with placeholders, e.g. "<PERSON_1>"
    mapping_token: str                # opaque handle to encrypted placeholder→original map
    entities: Sequence[Mapping[str, Any]]
```

### 12.3 (A) `TicketGateway` — Ticket Gateway contract

```python
class TicketGateway(Protocol):
    def fetch_new_tickets(self, since: str | None) -> Sequence["Ticket"]: ...
    def get_ticket(self, ticket_id: str) -> "Ticket": ...
    def add_internal_note(self, ticket_id: str, body: str, meta: Mapping[str, Any]) -> str: ...
    def assign(self, ticket_id: str, user_or_group: str) -> None: ...
    def subscribe(self, callback) -> None: ...   # webhook/event stream
```

REST surface (served by the gateway adapter):

- `POST /tickets/{id}/notes` `{body, meta}` → `{note_id}`
- `POST /tickets/{id}/assign` `{target}`
- `GET  /tickets/{id}` → ticket JSON
- `GET  /events` (SSE) → ticket events

MCP tools (so an agent or Cursor can drive the workflow):

- `ticket.get(id)` → ticket
- `ticket.add_internal_note(id, body, meta)` → note_id
- `ticket.assign(id, target)` → ok

### 12.4 (B) `PrivacyService` — Privacy Service contract

The whole anonymize/deanonymize pipeline behind one boundary. The orchestrator never sees recognizers, NER models, or the mapping store.

```python
class PrivacyService(Protocol):
    def anonymize(self, text: str, *, allowlist: Sequence[str] = ()) -> AnonymizationResult: ...
    def deanonymize(self, text: str, mapping_token: str) -> str: ...
    def health(self) -> Mapping[str, Any]: ...
```

REST:

- `POST /privacy/anonymize` `{text, allowlist?}` → `{text, mapping_token, entities}`
- `POST /privacy/deanonymize` `{text, mapping_token}` → `{text}`
- `GET  /privacy/health`

MCP tools:

- `privacy.anonymize(text, allowlist?)`
- `privacy.deanonymize(text, mapping_token)` *(local-only callers)*

Hidden sub-components (free to evolve): NER analyzer, custom `PatternRecognizer`s, anonymizer operators, encrypted mapping store, allow/deny lists.

### 12.5 (C) `KnowledgeRetrieval` — RAG contract (the most important boundary)

This single contract hides the embedder, vector store, sparse index, query rewriter, reranker, fusion, and any GraphRAG layer. **Swapping LlamaIndex → RAGFlow → R2R is invisible to callers.**

```python
@dataclass(frozen=True)
class RetrievalRequest:
    query: str
    top_k: int = 6
    namespaces: Sequence[str] = ("kb", "tickets")
    filters: Mapping[str, Any] | None = None
    rewrite: bool = True
    rerank: bool = True
    min_score: float | None = None

@dataclass(frozen=True)
class RetrievalResponse:
    chunks: Sequence[Chunk]            # carries source IDs for citations
    rewritten_queries: Sequence[str]
    debug: Mapping[str, Any]           # timings, scores, fusion weights

class KnowledgeRetrieval(Protocol):
    def retrieve(self, req: RetrievalRequest) -> RetrievalResponse: ...
    def index(self, namespace: str, docs: Sequence[Document]) -> None: ...
    def delete(self, namespace: str, ids: Sequence[str]) -> None: ...
    def health(self) -> Mapping[str, Any]: ...   # advertises capabilities (hybrid, graph, …)
```

REST surface (the canonical “RAG-as-a-service” API):

- `POST /rag/retrieve` (RetrievalRequest) → RetrievalResponse
- `POST /rag/index/{namespace}` `{docs[]}`
- `DELETE /rag/index/{namespace}` `{ids[]}`
- `GET  /rag/health`

MCP tools (the answer LLM and external agents call retrieval as a tool):

- `rag.retrieve(query, top_k?, namespaces?, filters?, rewrite?, rerank?)` → chunks + citations
- `rag.index(namespace, docs)` *(admin-scoped)*
- `rag.health()`

Contract guarantees:

- Every returned `Chunk` has a stable `id` resolvable to a source URL/ticket.
- Hybrid retrieval is on by default; backends without BM25 must emulate it or declare `capabilities.hybrid=false` in `health()`.
- `top_k` is an upper bound; fewer results allowed when `min_score` filters apply.
- Embedder, vector store, reranker, query-rewrite LLM, and chunker are **internal**. They are configured *inside* this component and are never reachable from outside.
- **All LLM and embedding calls made internally (query rewriting, HyDE, LLM-as-reranker, GraphRAG entity extraction, LightRAG `llm_func`, etc.) MUST go through the LLM Gateway (D).** Knowledge Retrieval MUST NOT open direct provider connections. Pure cross-encoder reranking models (e.g., `bge-reranker-v2-m3`) are not chat completions and are exempt.

### 12.6 (D) `LLMGateway` — LLM Gateway contract

A single boundary for all chat completions, independent of provider. Hides slot routing, privacy enforcement, retries, caching, and budget guards. Wire format mirrors the **OpenAI Chat Completions schema** for maximum compatibility (LiteLLM, Ollama, vLLM, Anthropic, OpenAI all speak it).

```python
class LLMGateway(Protocol):
    def complete(
        self, slot: Literal["retrieval_llm", "answer_llm"],
        messages: Sequence[Mapping[str, str]], *,
        tools: Sequence[Mapping[str, Any]] | None = None,
        max_tokens: int | None = None,
        temperature: float = 0.2,
    ) -> "ChatResponse": ...
    def embed(self, texts: Sequence[str], *, kind: Literal["doc", "query"]) -> list[list[float]]: ...
    def describe(self) -> Mapping[str, Any]:   # active models per slot, allow_remote flags, budget state
        ...
```

REST: `POST /v1/chat/completions` and `POST /v1/embeddings` (OpenAI-compatible), with an `X-Slot` header to select `retrieval_llm` vs `answer_llm`.

MCP tools (optional; useful for agentic workflows):

- `llm.complete(slot, messages, …)`
- `llm.describe()`

Hidden sub-components: provider adapters, the retrieval/answer slot routing, `allow_remote` enforcement, monthly budget guards, prompt cache, retry/backoff.

Contract guarantees:

- **The LLM Gateway is the single chokepoint for every chat completion and embedding call in the system**, including those made *inside* Knowledge Retrieval (query rewriting, HyDE, LLM-as-reranker, GraphRAG extraction, LightRAG/LlamaIndex/RAGFlow internal LLM hooks). No other component may call provider SDKs directly.
- This is what makes `allow_remote: false`, monthly budgets, and centralized tracing actually enforceable.

### 12.7 (E) `Orchestrator` — Workflow contract

The orchestrator is mostly an internal driver, but exposes a small control surface so it can be operated, observed, and replayed.

```python
class Orchestrator(Protocol):
    def process_ticket(self, ticket_id: str) -> "PipelineResult": ...   # idempotent
    def replay(self, ticket_id: str, *, from_step: str | None = None) -> "PipelineResult": ...
    def health(self) -> Mapping[str, Any]: ...
```

REST:

- `POST /workflow/process` `{ticket_id}` → result summary
- `POST /workflow/replay` `{ticket_id, from_step?}`
- `GET  /workflow/health`

Hidden sub-components: event subscription, pipeline steps, tracer (Langfuse/OTel), evaluator (Ragas), error routing back to humans.

### 12.8 MCP server topology

Three MCP servers, one per externally useful major component, so other AI workflows in the company can reuse them as tools:

- **`support-rag`** (component C) — `rag.retrieve`, `rag.index`, `rag.health`.
- **`support-privacy`** (component B) — `privacy.anonymize`, `privacy.deanonymize` (local-only).
- **`support-zammad`** (component A) — `ticket.get`, `ticket.add_internal_note`, `ticket.assign`.

The LLM Gateway (D) is normally consumed via its OpenAI-compatible REST endpoint rather than MCP, since most clients already speak that schema. The Orchestrator (E) is internal and not exposed via MCP.

### 12.9 Versioning & compatibility

- Each contract has a SemVer (`X-Contract-Version` HTTP header / MCP server `version`).
- Backwards-incompatible changes require a major bump and a parallel deployment window.
- A shared **`contracts/`** package holds the Python Protocols, JSON Schemas, and MCP tool descriptors so REST and MCP surfaces are generated, not hand-written.

### 12.10 Contract test suite

One shared pytest suite per **major** component (not per sub-component). Every implementation of a major contract MUST pass it:

- **Privacy Service** — round-trip: `deanonymize(anonymize(x).text, token) == x`; entity recall on a labeled set.
- **Knowledge Retrieval** — hybrid beats dense-only on a golden set; stable chunk IDs across calls; capabilities advertised in `health()` match runtime behavior.
- **LLM Gateway** — OpenAI schema conformance; `allow_remote=false` blocks remote providers; budget guard rejects over-quota calls; slot routing returns the configured model.
- **Ticket Gateway** — round-trip: a posted internal note appears in `get_ticket()`; reassignment is observable; webhook delivers events at-least-once.
- **Orchestrator** — `process_ticket` is idempotent; `replay(from_step=…)` resumes deterministically; failures reassign to humans.

This is what makes “swap LlamaIndex for RAGFlow” or “switch answer LLM from local Llama to Claude Opus” a one-line config change rather than a refactor.

## 13. Data lifecycle & retention

| Data | Where | Retention | Erasure path |
|---|---|---|---|
| Raw ticket body | Zammad (source of truth) | per Zammad policy | handled in Zammad |
| Anonymization mapping (placeholder ↔ original) | Privacy Service, encrypted at rest | **lifetime of the open ticket only**; purged when ticket is closed or after N hours, whichever first | automatic on close; manual purge via `privacy` admin endpoint |
| Anonymized ticket text used for retrieval | RAG corpus (`tickets` namespace), only after curation step | per legal/data-retention policy (e.g., 24 months) | `KnowledgeRetrieval.delete(namespace, ids)` cascades on Zammad ticket deletion |
| Company knowledge corpus | RAG corpus (`kb` namespace) | aligned with source-of-truth docs | re-index on doc deletion |
| Prompts / completions / traces | Langfuse + audit log | 90 days default; remote-LLM payloads logged **anonymized only** | bulk delete by ticket_id |
| Vectors / sparse index | Vector store + BM25 index | tied to corpus lifetime | rebuilt or pruned on `delete()` |
| Mapping store backups | encrypted, separate from main DB | ≤ 7 days | rotated automatically |

Right-to-erasure: deleting a ticket in Zammad triggers a cascade — Orchestrator calls `KnowledgeRetrieval.delete(...)` for any chunks tagged `ticket_id=X` and purges related Langfuse traces. The cascade is part of the Orchestrator contract test suite.

Curation gate: a closed ticket only enters the index after passing the curation pipeline (resolution status, quality signal, anonymization check). No ticket is auto-indexed.

## 14. Failure modes & fallback matrix

Every failure mode resolves to one of three outcomes: **halt and reassign with error note** (safest), **degrade and continue with low-confidence flag**, or **switch to fallback provider**. The customer is never reached without human review either way.

| Failing component | Detection | Fallback | Customer impact |
|---|---|---|---|
| **Privacy Service down** | health probe / call exception | **HALT.** Reassign to humans with error note `"Anonymization unavailable — please draft manually."` Never bypass. | none (human handles) |
| **Privacy Service: anonymization low-confidence** (entities < threshold) | analyzer score | **HALT** for safety; same error note. | none |
| **Knowledge Retrieval down** | health/timeout | **DEGRADE.** Generate draft from anonymized question only via answer LLM; mark note "Low-confidence — RAG unavailable, no citations." | none (note flagged) |
| **Knowledge Retrieval: empty results / below `min_score`** | response | DEGRADE same as above; note flagged "Knowledge gap suspected." | none |
| **LLM Gateway: remote provider down** (e.g., Anthropic) | error / timeout / rate limit | **SWITCH** `answer_llm` to configured local fallback; tag note "Drafted with local fallback model." | none |
| **LLM Gateway: budget exceeded** | budget guard | SWITCH to local fallback; alert ops. | none |
| **LLM Gateway: `allow_remote=false` violated** | gateway guard | **HALT.** Hard fail closed; alert security. | none |
| **Ticket Gateway: post-note fails** | API error | retry with backoff; on persistent failure, reassign with admin alert. | none |
| **Ticket Gateway: webhook missed** | reconciliation poll | catch up on next poll; processing remains at-least-once (Orchestrator is idempotent). | none |
| **Orchestrator crash mid-pipeline** | restart | resume via `replay(ticket_id, from_step=last_completed)`. | none |
| **Any unhandled exception** | catch-all | reassign to humans with the exception class (no payload) in the error note; full trace stays in Langfuse. | none |

Invariant: a ticket is **never** left assigned to the AI agent in a non-terminal state. Either the pipeline completes (note posted, reassigned to humans) or it fails closed (reassigned with error note).

## 15. Security model

### 15.1 Authentication between components

- mTLS or signed service tokens (JWT) on all inter-component REST/MCP calls. No anonymous access.
- Each component has its own service identity; no shared secrets.
- Secrets via OS keyring / Vault / cloud secret manager; never in config files committed to source control.

### 15.2 Authorization (per-tool ACL)

| Tool / endpoint | Allowed callers |
|---|---|
| `rag.retrieve` | Orchestrator, internal AI workflows, support engineers (read-only UI) |
| `rag.index`, `rag.delete` | Curation service / admins only |
| `privacy.anonymize` | Orchestrator and other on-prem services |
| `privacy.deanonymize` | **Orchestrator only**, **local network only**, never exposed via MCP to remote clients |
| `ticket.add_internal_note` | Orchestrator (scoped to AI agent user in Zammad) |
| `ticket.assign` | Orchestrator |
| Customer-facing article creation in Zammad | **denied by Zammad permissions for the AI agent user** — architectural guarantee of NFR-7 |
| `llm.complete` / `/v1/chat/completions` | Orchestrator, Knowledge Retrieval, Curation; rate-limited per caller |

### 15.3 Threat model (top items)

- **Prompt injection from ticket content.** Treat ticket body as untrusted. Pass it only inside a clearly-fenced user message; system prompt instructs the model to ignore instructions inside ticket text and retrieved chunks. Tool-use is disabled for the answer LLM call. Post-generation check rejects drafts that attempt to alter assignment, contact the customer directly, or contain non-allowed citation IDs.
- **Poisoned / malicious documents in the KB.** Curation gate signs sources; only allowlisted source roots can be indexed. Periodic diff review of newly-indexed content.
- **Exfiltration via citations or links.** Drafts are scrubbed for outbound links/IDs not in the citation set; remote LLM payloads contain only anonymized text.
- **PII leakage to remote providers.** Enforced by the LLM Gateway: `allow_remote: true` slots only receive anonymized text; remote-payload logging is anonymized; the `deanonymize` tool is not callable from remote contexts.
- **Mapping-store compromise.** Encrypted at rest with a key managed outside the service; short retention (ticket lifetime); access audited; backups encrypted and rotated.
- **Tool-call abuse via MCP.** MCP tool descriptors carry per-caller scopes; admin tools (`rag.index`, `rag.delete`) require an elevated token; deanonymize is hard-disabled in MCP servers reachable from outside the orchestrator.
- **Replay / duplicate processing.** Orchestrator is idempotent on `ticket_id`; webhook deliveries are deduplicated by event ID.

### 15.4 Audit

- Every pipeline run logs: ticket_id, anonymized query hash, retrieved chunk IDs, model identifiers per slot, token counts, cost, latency, outcome (note posted / fallback / halted).
- Audit log is append-only and separate from operational logs.
- Retention aligned with §13.

## 16. Acceptance criteria (MVP)

- New ticket triggers pipeline within 10 s; internal note posted within 60 s (local) / 30 s (Opus) p95.
- 100% of customer-facing replies still authored/sent by humans.
- Switching `answer_llm` from local Llama to Claude Opus requires only a config change and a service restart.
- Presidio masks names, emails, phones, addresses, IBANs, and at least one custom pattern in test set with ≥ 95% recall.
- Hybrid retrieval + reranker beats dense-only baseline by ≥ 10% context precision on a labeled eval set (Ragas).
