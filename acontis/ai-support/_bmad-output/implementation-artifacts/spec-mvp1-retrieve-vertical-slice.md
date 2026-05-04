---
title: 'MVP1 PRD — retrieve vertical slice (R-1..R-7) contract tests'
type: 'feature'
created: '2026-04-25T20:00:00Z'
status: 'done'
baseline_commit: 'e038368ed2ab29815411e96b94e30862fc93701d'
context:
  - 'support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The gap table marks R-1, R-2, R-3, R-4, R-5, R-6, and R-7 as Partial or Missing. Offline tests exercise `RAGService.retrieve` and `to_qdrant_filter`, but not the full retrieve stack: HTTP wire (or strict request/response invariants), filters into `aquery`, `min_score` after rerank, query rewrite (gateway `chat`) when enabled, `rerank=True` path, RRF/top_k propagation, and serialized chunk fields.

**Approach:** Add **pytest** modules under `tests/contract/` and `tests/unit/` using `TestClient` / ASGI, `AsyncMock` / dependency overrides for `RAGService`, and captured calls to a mocked `Qdrant` client’s `aquery` (and gateway for rewrite). No live Qdrant in default CI; use `RUN_INTEGRATION=1` only if an optional follow task adds it.

## Boundaries & Constraints

**Always:** No provider SDKs. Default `pytest` remains offline. Reuse `tests/conftest.py` and patterns from `test_auth_health.py` / `test_retrieval_hybrid_flag.py` / `test_admin_index_delete.py`.

**Ask First:** Whether `POST /rag/retrieve` should be the single HTTP entry for R-1 or a thinner service-level contract is enough for CI policy.

**Never:** Change public JSON schemas or retrieval algorithms beyond test seams; no GraphRAG or new endpoints except tests.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected | Error handling |
|----------|---------------|----------|----------------|
| R-1 HTTP | Valid service token, JSON body | 200 + `RetrievalResponse` shape; 401 if token wrong | Pydantic 422 on bad body (if applicable) |
| R-5 filters | `RetrievalRequest.filters` set | Mock `aquery` receives Qdrant filter matching `to_qdrant_filter` output | N/A |
| R-7 `min_score` | Scores below threshold after rerank | Chunks with score `< min_score` excluded; empty list valid | N/A |
| R-4 rewrite | `rewrite=True`, query_rewrite enabled in config | `chat_completion` (or rewrite seam) called with `retrieval_llm` slot; n≤3 alts | HyDE off unless config says otherwise |
| R-3 rerank | `rerank=True` | Reranker invoked (mock `CrossEncoderRerank` or service branch) | `rerank=False` skips (existing pattern) |
| R-2 RRF / top_k | Config sets hybrid, RRF, caps | `VectorStoreQuery` (or capture) includes expected top_k / fusion params | N/A |
| R-6 chunk JSON | One scored node from mock | Response includes `id`, `parent_id`, `score`, expected metadata keys | N/A |

</frozen-after-approval>

## Code Map

- `support_rag/app.py` — `POST /rag/retrieve`, `require_service`, request/response models.
- `support_rag/service.py` — `retrieve`, `_rewrite_queries`, `_query_one` / `aquery`, `min_score`, `rerank` branch.
- `support_rag/gateway.py` — `embed`, `chat_completion` with `X-Slot` (R-4/R-16 tested here indirectly; dedicated header tests in `spec-mvp1-gateway-slot-headers.md`).
- `support_rag/schemas.py` — `RetrievalRequest`, `RetrievalResponse`, chunk types.
- `support_rag/qfilter.py` — `to_qdrant_filter` (already unit-tested; R-5 is **path** to `aquery`).
- `tests/contract/test_retrieval_hybrid_flag.py` — extend or mirror for R-2; new modules for HTTP and filters.

## Tasks & Acceptance

**Execution:**

- [x] `tests/contract/test_retrieve_http.py` (or name aligned with repo) — ASGI + mocked `get_service` / `RAGService`: 401 without bearer, 200 with service token, JSON body parses to expected top-level keys for retrieve response (R-1).
- [x] Same or `tests/contract/test_retrieve_filters_aquery.py` — Assert `filters` in request lead to `aquery` (or `AsyncQdrantClient` mock) with filter payload consistent with R-5 (R-5).
- [x] `tests/unit/test_retrieve_min_score.py` (or extend service tests) — Inject ranked scores; assert post-filter list respects `min_score`; allow empty (R-7).
- [x] `tests/contract/test_retrieve_rewrite.py` or unit — Mock gateway `chat_completion`; with rewrite enabled, assert alt queries used and count ≤3; HyDE default off (R-4).
- [x] `tests/contract/test_retrieve_rerank_path.py` — With `rerank=True`, assert rerank seam invoked (mock); with `False`, not invoked (R-3).
- [x] `tests/contract/test_retrieve_vector_query_params.py` — Capture `VectorStoreQuery` or equivalent; assert `top_k` / RRF-related fields per config (R-2).
- [x] `tests/contract/test_retrieve_chunk_shape.py` — Mock retrieve returns one node; assert serialized chunk fields per PRD (R-6).
- [x] `README.md` — One paragraph: env vars for new contract tests if any.

**Acceptance Criteria:**

- Given `pytest` default (no live Qdrant), when `pytest tests/ -q` runs, then all new tests pass.
- Given a retrieve request with `filters`, when the service runs against mocked Qdrant, then the filter passed to `aquery` matches the PRD R-5 expectation.
- Given `min_score` set and synthetic scores, when `retrieve` completes, then no chunk in the response has `score` below `min_score`.
- Given rewrite enabled in config and mocked gateway, when `retrieve` runs with `rewrite=True`, then the rewrite path is exercised with at most three query variants.
- Given `RAG_SERVICE_TOKEN` and valid body, when `POST /rag/retrieve` is called, then the response is 200 and JSON includes the contract fields needed for R-1/R-6.

## Spec Change Log

- 2026-04-25 — Authored from gap table “Suggested next steps” item 1 and rows R-1..R-7.
- 2026-04-25 — Implemented contract/unit tests; marked done; R-1–R-7 row updates in `mvp1-prd-to-automated-tests-gap-table.md`.

## Design Notes

Prefer patching at `get_service` / `RAGService` the same way as `test_admin_index_delete.py` to avoid `isinstance` on mock classes. For `aquery` capture, assign `AsyncMock` to the vector store client used inside `RAGService` if a small refactor is required for injectability, keep it test-only or behind a `Protocol`.

## Verification

**Commands:** `python -m pytest tests/ -q --tb=short` · `python -m ruff check support_rag tests`

**Manual checks:** None if CI green.

## Suggested Review Order

**HTTP and auth (R-1)**

- `TestClient` + `RAGService` override mirrors `test_admin_index_delete` for retrieve.
  [`test_retrieve_http.py:1`](../../tests/contract/test_retrieve_http.py#L1)

- Live stack still needs `RAG_SERVICE_TOKEN` at runtime; contract tests set it via `monkeypatch`.
  [`test_retrieve_http.py:23`](../../tests/contract/test_retrieve_http.py#L23)

**Filters and vector params (R-2, R-5)**

- `qdrant_filters` on mocked `aquery` must match `to_qdrant_filter` for the same payload.
  [`test_retrieve_filters_aquery.py:1`](../../tests/contract/test_retrieve_filters_aquery.py#L1)

- Dense and hybrid `VectorStoreQuery` fields compared to `AppConfig.retrieval` defaults.
  [`test_retrieve_vector_query_params.py:1`](../../tests/contract/test_retrieve_vector_query_params.py#L1)

**Rerank, rewrite, response shape (R-3, R-4, R-6, R-7)**

- Mocks `embed` so retrieve never calls real httpx, then checks `_ce` use vs skip.
  [`test_retrieve_rerank_path.py:1`](../../tests/contract/test_retrieve_rerank_path.py#L1)

- Stubs `chat_completion_sync` for alternatives; asserts HyDE stays off in default config.
  [`test_retrieve_rewrite.py:1`](../../tests/contract/test_retrieve_rewrite.py#L1)

- `ChunkResult` / JSON keys from a single `TextNode` in the no-rerank path.
  [`test_retrieve_chunk_shape.py:1`](../../tests/contract/test_retrieve_chunk_shape.py#L1)

- Rerank path + `min_score` with NumPy `predict` return values; empty `chunks` is valid.
  [`test_retrieve_min_score.py:1`](../../tests/unit/test_retrieve_min_score.py#L1)

**Peripherals**

- README call-out for the new retrieve contract modules; no new env requirements.
  [`README.md:37`](../../README.md#L37)

- Gap table R-1..R-7 rows and backlog ordering updated in lockstep.
  [`mvp1-prd-to-automated-tests-gap-table.md:16`](./mvp1-prd-to-automated-tests-gap-table.md#L16)
