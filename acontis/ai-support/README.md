# support-rag (Option B: LlamaIndex + Qdrant + LiteLLM)

Implements the **Knowledge Retrieval (RAG)** service from [`_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md`](_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md) using LlamaIndex, Qdrant hybrid search, a local cross-encoder reranker, and an OpenAI-compatible **LLM Gateway** (e.g. LiteLLM) for all embeddings and retrieval LLM calls.

## Quick start (Docker)

```bash
cp config.example.yaml config.yaml
# Set RAG_SERVICE_TOKEN, RAG_ADMIN_TOKEN, Qdrant URL, LiteLLM base URL in config or env
docker compose up --build
```

Ensure `config.yaml` exists next to `docker-compose.yaml` (the compose file mounts it read-only).

- REST: `http://localhost:8080` — `GET /rag/health`, `POST /rag/retrieve`, `POST /rag/index/{namespace}`, `DELETE /rag/index/{namespace}`
- Qdrant: `6333`, LiteLLM: expected at `llm_gateway.base_url` in `config.yaml`

## Local development

Requires **Python 3.11 or 3.12** (3.14 is not yet supported by several ML stack wheels).

```bash
cp config.example.yaml config.yaml
# Optional: cp .env.example .env  and set RAG_SERVICE_TOKEN, RAG_ADMIN_TOKEN there (auto-loaded; see .env.example)
export RAG_SERVICE_TOKEN=dev
export RAG_ADMIN_TOKEN=admin
export RAG_LLM_GATEWAY__BASE_URL=http://127.0.0.1:4000
py -3.12 -m pip install -e ".[dev]"
py -3.12 -m uvicorn support_rag.app:app --host 0.0.0.0 --port 8080
```

### Ingest a folder (CLI)

With the API up, index every `*.md`, `*.txt`, and `*.rst` file under a directory (UTF-8; symlinks skipped):

```bash
export RAG_MCP_BASE_URL=http://127.0.0.1:8080
export RAG_ADMIN_TOKEN=your-admin
py -3.12 scripts/ingest_folder.py --root /path/to/docs --namespace kb
```

Dry-run (list planned parent `id` values, no `POST`):

```bash
py -3.12 scripts/ingest_folder.py --root /path/to/docs --namespace kb --dry-run
```

### Export retrieve results (CLI)

Run a test query and write the `POST /rag/retrieve` JSON body to a file (for diffs or golden fixtures):

```bash
export RAG_MCP_BASE_URL=http://127.0.0.1:8080
export RAG_SERVICE_TOKEN=your-service
py -3.12 scripts/retrieve_to_file.py --query "your question" --out /tmp/retrieve_out.json
```

Omit `--query` to read the query from stdin. Optional: `--top-k`, `--namespaces kb,tickets`, `--filters '{"namespace":"kb"}'`, `--no-rewrite` / `--no-rerank`, `--no-hybrid` / `--hybrid`.

### Web UI (browser)

With the API running, open **`/ui/`** (or `/`, which redirects there) in a browser. Unless you set **`RAG_ENABLE_WEB_UI=0`**, the service exposes:

- **Chat** — enter the **service** bearer used for `POST /rag/retrieve`; each send is a **single** user message to the LLM gateway (no prior turns). Use the checkbox to run retrieval first and append chunk text to the prompt before the LLM call.
- **Index folder** — enter the **admin** bearer and an **absolute path to a directory on the host where the API runs** (same file rules as `scripts/ingest_folder.py`: `*.md` / `*.txt` / `*.rst`, UTF-8). Ingest uses the in-process indexer (no extra HTTP hop to yourself).

## Tests

```bash
py -3.12 -m pytest tests/ -q
```

### Contract tests (offline)

`tests/contract/` holds API-shape and R-10 chunk-id contracts. The default `pytest` run stays **offline** (Qdrant and the LLM gateway are mocked or bypassed). Markers `integration` and `requires_services` are reserved for tests that need a live stack; those are **skipped** unless you set `RUN_INTEGRATION=1` (or `true` / `yes`). Residual PRD test gaps: R-8 (`test_index_request_validation.py`), R-9 (kb vs tickets chunk counts), NFR-5 (chunker + `embedding_model`). **NFR-6 (unit):** `tests/unit/test_service_lifecycle_nfr6.py` (two offline lifecycles). **NFR-6 (process):** `tests/integration/test_nfr6_compose_restart.py` restarts the `support-rag` service via `docker compose` — requires a live stack, `RUN_INTEGRATION=1`, and `RUN_NFR6_COMPOSE=1`. **NFR-7 (401 matrix):** `tests/contract/test_protected_routes_401.py` (single table + OpenAPI guard; replaces scattered 401-only assertions in other contract modules). **R-18:** `tests/unit/test_cross_encoder_r18_smoke.py` — the **default GitLab** `mvp1_script_help_golden` job runs `-m "not slow"` (frozen reranker model id, no Hub); the optional `slow` CrossEncoder load is for local/extended runs. **R-14 (live capabilities / Qdrant “stores”)** and **R-11 (live delete/erasure touchpoint)** are covered partially by `tests/integration/test_qdrant_optional_r11_r14.py` when `RUN_INTEGRATION=1`; default CI stays offline. **R-5, R-11, R-12, and §2.8#4 (live filters + delete + replace + erasure)** use `tests/integration/test_qdrant_filters_erasure_live.py` with the same `RUN_INTEGRATION=1` gate (requires reachable Qdrant and a working embedding gateway per `config` / env). Run only contracts:

```bash
py -3.12 -m pytest tests/contract/ -q
```

**NFR-4 and MCP (offline):** `tests/contract/test_otel_routes.py` checks that index/delete routes use span names `rag.index` and `rag.delete` (mocked tracer, no OTLP). `tests/contract/test_admin_index_delete.py` uses mocked `RAGService` for `POST`/`DELETE` success/400 paths (NFR-7 unauthorized paths: `test_protected_routes_401.py`). R-5 filter mapping: `tests/unit/test_qfilter.py`. `tests/test_gateway_trace_ctx.py` asserts W3C `traceparent` is forwarded on `LLMGatewayClient` request headers. `tests/unit/test_gateway_slot_headers.py` asserts R-15/R-16 `X-Slot` headers on `embed` / `chat_completion` (mock transport, no network). `tests/test_mcp_tools.py` verifies FastMCP exposes the R-19 tool names `rag.health`, `rag.retrieve`, and `rag.index` (the `mcp` package is a normal install dependency; see `pyproject.toml`).

**MCP in-process HTTP binding (R-19, R-20, no stdio / no live RAG in CI):** `tests/contract/test_mcp_http_binding.py` patches `httpx.AsyncClient` in `support_rag.mcp_server` with `httpx.MockTransport`, sets `RAG_MCP_BASE_URL` to a dummy host, and asserts `GET /rag/health` and `POST /rag/retrieve` use the **service** bearer, while `POST /rag/index/{namespace}` uses the **admin** bearer. A negative test ensures `RAG_ADMIN_TOKEN` unset (service token only) makes `rag.index` raise before any request—mirroring REST admin gating. Stdio or a subprocess MCP server is not required for these checks.

**Retrieve path (R-1..R-7, offline):** `tests/contract/test_retrieve_http.py` uses a mocked `RAGService` for `POST /rag/retrieve` (401/200 + JSON fields). R-2/R-5: `test_retrieve_vector_query_params.py` and `test_retrieve_filters_aquery.py` capture `VectorStoreQuery` and `qdrant_filters` via mocked vector stores. R-3/R-4: `test_retrieve_rerank_path.py`, `test_retrieve_rewrite.py`. R-6: `test_retrieve_chunk_shape.py`. R-7: `tests/unit/test_retrieve_min_score.py`. No extra env vars beyond the usual `RAG_SERVICE_TOKEN` / `RAG_ADMIN_TOKEN` in those modules.

See `mcp/` for the `support-rag` MCP stdio entrypoint and `config.example.yaml` for all settings.

### E2E / Ollama profile (optional)

For live stack tests with **small local models only** (no cloud LLM APIs in this profile) via **LiteLLM → Ollama**, use the dedicated file. **Default ports on `127.0.0.1`:** LiteLLM **4000**, RAG **8080**, Qdrant **6333** (align with `config.e2e.example.yaml` and your compose).

- **Runbook (step-by-step):** [docs/runbook-allow-remote-false-e2e.md](docs/runbook-allow-remote-false-e2e.md) — all-**local** (no Docker): Ollama + **pip** LiteLLM (latest) + Qdrant binary + uvicorn; simple `model` routing, optional auth check.
- **LiteLLM example config:** [docs/litellm-ollama-e2e.example.yaml](docs/litellm-ollama-e2e.example.yaml) — Ollama-only `model_list` for `embedding` and `retrieval` model names.
- **Template:** `config.e2e.example.yaml` — **embedding** `all-minilm`, **chat / rewrite** `llama3.2:1b`, `qdrant.vector_size: 384`, `collection_prefix: support_rag_e2e_`.
- **Usage:** `cp config.e2e.example.yaml config.e2e.yaml`, set `RAG_CONFIG=config.e2e.yaml`, point `llm_gateway.base_url` at **LiteLLM**, `ollama pull` the models, and align **LiteLLM** with the example YAML. If embed dimension differs, adjust `vector_size` to match the gateway output.

## Golden-set eval (hybrid vs dense)

Requires a **running** stack: Qdrant (with hybrid collections), LLM gateway for embeddings, and this API. The script calls `POST /rag/retrieve` twice per question (`hybrid: true` vs `hybrid: false`) with `rerank: true` so the comparison isolates the sparse+dense fusion leg.

1. **Seed the smoke parent document** so `gold_doc_id` in `eval/golden/questions.jsonl` exists (default `doc-smoke-1` in namespace `kb`). Example:

   ```bash
   curl -sS -X POST "http://127.0.0.1:8080/rag/index/kb" \
     -H "Authorization: Bearer $RAG_ADMIN_TOKEN" -H "Content-Type: application/json" \
     -d '{"docs":[{"id":"doc-smoke-1","text":"EtherCAT master redundancy, ENI, cycle time, EC-Master API, distributed clocks, Windows/Linux RT, firmware, CoE, ring topology, licensing, Wireshark, NIC models, VLAN, SOEM comparison, OP timeout, EoE/FoE/SoE, junction redundancy, frame size, bug reporting, source build, log rotation, security, error 0x0811, hot-plug, memory and CPU tuning.","metadata":{}}]}'
   ```

   Replace the `text` with your real KB excerpt if needed; chunk `parent_id` must match the ingest `id`.

2. **Run the eval** (service token, not admin):

   ```bash
   export RAG_SERVICE_TOKEN=dev
   py -3.12 eval/eval_hybrid_vs_dense.py --base-url http://127.0.0.1:8080
   ```

   Optional: `RAG_EVAL_BASE_URL`, `--jsonl`, `--top-k`, `--rewrite` / `--no-rewrite`. Set `ENFORCE_THRESHOLDS=1` to exit non-zero when hybrid does not beat dense by at least **10% relative** hit-rate lift (or dense hit rate is 0 while hybrid is also 0).

**CI:** this job needs Qdrant, gateway, embeddings, and reranker CPU; keep it on a **self-hosted** or GPU/CPU runner with those services, or run manually — not enabled in default unit-test CI.

## MVP1 eval + perf CI (GitLab)

Automated **hybrid vs dense** eval and **NFR retrieve** smoke are wired for [`.gitlab-ci.yml`](.gitlab-ci.yml) (GitLab, not GitHub Actions). The default `pytest` developer loop stays offline; these jobs use a **tagged self-hosted GitLab runner** (default tag: `rag-mvp1-eval`).

| Job | When it runs | Exit code / blocking | Notes |
|-----|----------------|----------------------|--------|
| `mvp1_script_help_golden` | **Merge requests**, branch pipelines, and other default `test`-stage events on **shared** runners (no `rag-mvp1-eval` tag) | Non-zero if deliverable CLI, golden line-count, or R-18 non-slow test fails. | **Offline / no Hub:** `pytest tests/unit/test_mvp1_deliverable_cli.py` and `pytest tests/unit/test_cross_encoder_r18_smoke.py -m "not slow"` (§2.11 deliverables, `eval/golden/questions.jsonl` ≥ 30 lines, frozen CrossEncoder model id for R-18). Caches under `.cache/huggingface/` and `.cache/sentence-transformers/`. The optional `slow` Hub smoke is not part of this gate. |
| `hybrid_golden_eval` | Schedule, **Run pipeline** (web), API, parent pipeline, or **manual** on branch push (not on merge requests) | With `ENFORCE_THRESHOLDS=1`, exit non-zero if hybrid does not meet the ≥10% relative lift rule (see `eval/eval_hybrid_vs_dense.py`). Unset: metrics only, exit 0. | **Not** a default MR gate. To require it on MRs, add an explicit `merge_request` rule and document that in this table. |
| `nfr_retrieve_smoke` | Same `rules` as above | `NFR_ENFORCE=0` (default): always exit 0 (report p95 and concurrent errors). `NFR_ENFORCE=1`: non-zero if p95 exceeds the budget or any concurrent call fails. | **Report-only** at first: job has `allow_failure: true`. Set `allow_failure: false` when the SLO is trusted. |
| `e2e_privacy_allow_remote` | Same `rules` as `hybrid_golden_eval` (self-hosted `rag-mvp1-eval` only) | Non-zero if `e2e_gateway_preflight` or `RUN_E2E_PRIVACY=1 pytest -m e2e_privacy` fails. | **§2.8(5):** full LiteLLM + Ollama + Qdrant + RAG stack must be up on the runner (or reachable). Set `RAG_CONFIG` (default `config.e2e.example.yaml`), `RAG_SERVICE_TOKEN`, `RAG_ADMIN_TOKEN` in GitLab; see [docs/runbook-allow-remote-false-e2e.md](docs/runbook-allow-remote-false-e2e.md). |

**Runner:** In GitLab, register a runner on the host that can reach the RAG app (e.g. `RAG_EVAL_BASE_URL=http://127.0.0.1:8080` or the Docker bridge address). **Another machine:** register a second runner with the **same** tag, then disable the old one — the tag is the only coupling (see [spec-golden-set-hybrid-vs-dense-eval.md](_bmad-output/implementation-artifacts/spec-golden-set-hybrid-vs-dense-eval.md) for eval semantics).

**CI/CD variables (GitLab):** `RAG_SERVICE_TOKEN` (required; mask), `RAG_EVAL_BASE_URL` (base URL the runner uses to call `POST /rag/retrieve`), optional `ENFORCE_THRESHOLDS=1` for the eval job, optional `NFR_ENFORCE=1` and `NFR_P95_BUDGET_SEC=2.0` for the NFR script. See [scripts/nfr_retrieve_smoke.py](scripts/nfr_retrieve_smoke.py) for the full NFR env surface.

**PRD touchpoints:** §2.8(1)(2) (golden eval + 10% lift) and NFR-1 / NFR-2 (p95 and concurrency) are **covered (scheduled/self-hosted)** once this pipeline and a seeded Qdrant are in place; labeling quality remains a human step for the golden set.
