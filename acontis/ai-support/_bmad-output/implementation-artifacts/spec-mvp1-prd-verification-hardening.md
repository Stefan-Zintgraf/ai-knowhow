---
title: 'MVP1 PRD — contract tests & test harness'
type: 'feature'
created: '2026-04-25T12:00:00Z'
status: 'done'
baseline_commit: '307f7c8d72fd6fc945eb37a5c9711d3d2bb14315'
context:
  - 'support_rag_mvp1_prd.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `support_rag` implements the MVP1 stack, but `support_rag_mvp1_prd.md` §2.8 / §2.12 require demonstrable **API-level** compliance. Today only `tests/test_chunk_id.py` and `tests/test_no_provider_sdk.py` cover small slices; there is no structured contract test bundle for health, auth, and R-10 idempotent chunk identity.

**Approach:** Add **pytest contract modules** (health JSON shape and semantics, 401 on bad/missing service token for `GET /rag/health`, stable chunk IDs across duplicate ingest) plus **shared test wiring** (`conftest`, markers, `pyproject.toml`, short `README` subsection). Use mocks for gateway/Qdrant in the default path so `pytest` stays offline. Defer golden hybrid-vs-dense eval to a follow-up (see `deferred-work.md`).

## Boundaries & Constraints

**Always:** No new provider SDKs; `tests/test_no_provider_sdk.py` must keep passing. Reuse `support_rag/schemas.py` where helpful. Mark any test that needs real Qdrant or gateway with `integration` or `requires_services` so default runs skip them. Chunk IDs: PRD R-10 (stable across identical re-ingest).

**Ask First:** If `support_prd.md` appears in-tree, align health wording; else mirror `support_rag_mvp1_prd.md` §2.8 item 1 in docstrings. CI policy (unit-only vs integration runner) remains a separate decision.

**Never:** No retrieval pipeline rewrites, GraphRAG, Ragas, or web UI. Security model unchanged except **asserting** 401/403 behavior. No eval script or hybrid-vs-dense report in this spec (deferred).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|---------------|-----------------------------|----------------|
| Health contract | `RAGService.health()` or `GET /rag/health` with service token | `status`, `contract_version`, `capabilities` (hybrid, rerank, graph, namespaces), `models`, `stores`; `capabilities` match `AppConfig.retrieval` / MVP1 (`graph` false, `namespaces` lists `kb` and `tickets`, `hybrid` matches `config.retrieval.hybrid`, `rerank` true); response may include `version` (service semver from config) | Qdrant down → `status` / `stores.qdrant` degraded as implemented today |
| Auth | Missing/wrong bearer on `/rag/health` | HTTP 401 | Valid token: 200 + JSON |
| Idempotent chunk id | Same parent document chunked twice (same namespace, text, metadata, chunker version) | Identical `TextNode.id_` values per R-10 | N/A in happy path |
| SDK guard | Import lint test | No forbidden provider SDKs | Regression fails |

</frozen-after-approval>

## Code Map

- `support_rag/app.py` — `GET /rag/health` uses `Depends(require_service)`; `_require_bearer` returns 401 for missing/wrong bearer when `RAG_SERVICE_TOKEN` (or `config.service.service_token_env`) is set.
- `support_rag/service.py` — `RAGService.health()` calls `_qdrant.get_collections()` and `await self._gateway.describe_models()`; builds `capabilities` from `self._config.retrieval` and `NAMESPACES`; `index()` uses `chunk_kb` / `chunk_tickets` then `idx.ainsert_nodes`.
- `support_rag/chunking.py` — `chunk_kb` / `chunk_tickets` assign `stable_chunk_id` to each `TextNode.id_` (R-10 surface for contract tests without Qdrant).
- `support_rag/chunk_id.py` — `stable_chunk_id` implementation.
- `support_rag/gateway.py` — `LLMGatewayClient.describe_models()` (mock in health tests).
- `support_rag/config.py` — `ServiceConfig.service_token_env` (default `RAG_SERVICE_TOKEN`), `RetrievalConfig.hybrid`, defaults for chunker versions.
- `tests/test_chunk_id.py`, `tests/test_no_provider_sdk.py` — existing guards; must remain green.
- `pyproject.toml` — extend `[tool.pytest.ini_options]` with `markers` for `integration` and `requires_services`.

## Tasks & Acceptance

**Execution:**

- [x] `pyproject.toml` — Register pytest markers `integration` and `requires_services` (and any aliases you use) under `[tool.pytest.ini_options]` so pytest 8+ does not warn on unknown marks.
- [x] `tests/conftest.py` — Define shared fixtures: optional env-based skip for `integration` / `requires_services`; helpers to build `AppConfig` or `FastAPI` app with test tokens and mocked `RAGService` dependencies where useful. Keep default suite offline.
- [x] `tests/contract/test_health_capabilities.py` — Assert `RAGService.health()` dict shape: `status`, `contract_version`, `capabilities` (`hybrid` matches config, `rerank` True, `graph` False, `namespaces` equals `["kb", "tickets"]`), `models`, `stores`. Mock `_gateway.describe_models` to return stable embedding/LLM strings; mock `_qdrant.get_collections` (or inject a client) so the test does not require a live Qdrant. Cover degraded path if Qdrant raises (optional second test with mock raising).
- [x] `tests/contract/test_auth_health.py` — Using `httpx.AsyncClient` + `ASGITransport` (or `TestClient`) against `support_rag.app.app`, set `RAG_SERVICE_TOKEN` to a known value in the environment for the test process, call `GET /rag/health` with no `Authorization`, wrong bearer, and correct bearer; expect 401 then 200 with JSON body.
- [x] `tests/contract/test_chunk_id_ingest_idempotent.py` — Load real `AppConfig` (or minimal constructed config). Run `chunk_kb` (and at least one `chunk_tickets` path) twice on the same `IngestDocument`; assert ordered lists of `id_` are identical. No Qdrant or gateway calls required.
- [x] `README.md` — Short subsection: default `pytest` is offline; how to run `tests/contract/`; when to use `-m integration` / service env vars.

**Acceptance Criteria:**

- Given dev dependencies installed, when `pytest` runs with default options, then all tests pass without live Qdrant or LLM gateway and no tests marked `integration` / `requires_services` run unless explicitly selected.
- Given a configured `AppConfig` with `retrieval.hybrid` True or False, when `RAGService.health()` is invoked with gateway and Qdrant behavior mocked, then `capabilities.hybrid` matches that config and `capabilities.namespaces` lists both `kb` and `tickets`.
- Given `RAG_SERVICE_TOKEN` set, when `GET /rag/health` is called without a valid bearer token, then the response status code is 401; when called with the correct bearer token, then the response status code is 200 and the body parses as JSON with `contract_version` and `capabilities`.
- Given the same KB ingest document and config, when `chunk_kb` is invoked twice, then the sequence of chunk node ids is identical.

## Spec Change Log

- 2026-04-25 — Split: hybrid vs dense eval script and golden integration evidence deferred to `deferred-work.md`.
- 2026-04-25 — Planning refresh: aligned code map with `chunking.py` / `health()` implementation; clarified health includes optional `version` key; chunked idempotent AC via double `chunk_kb` (offline); task order wiring-first.

## Design Notes

Prefer mocks/stubs for `get_collections` and `describe_models` in default `pytest`. Reserve `@pytest.mark.integration` or `requires_services` for any future test that opens real TCP to Qdrant or the gateway. For ASGI tests, lifespan must run so `app.state.rag` exists — use libraries already in `dev` (e.g. `httpx` + `ASGITransport`, `pytest-asyncio`, or `starlette.testclient`).

## Verification

**Commands:**

- `py -3.12 -m pytest tests/ -q` — all pass; integration-marked tests skipped unless `-m integration` (or document chosen skip behavior).
- `py -3.12 -m pytest tests/contract/ -q` — contract tests pass offline.

**Manual checks (if no CLI):** None required for this spec.

## Suggested Review Order

**Offline contract harness**

- Mock Qdrant, async client, and indices so `RAGService` exercises real `health()` without TCP.
  [`conftest.py:32`](../../tests/conftest.py#L32)

- Assert MVP1 capability flags, models, and degraded Qdrant path on the service dict.
  [`test_health_capabilities.py:12`](../../tests/contract/test_health_capabilities.py#L12)

**Production fixes uncovered by contracts**

- Pass `gateway` into `BaseEmbedding` so Pydantic validates `GatewayEmbeddings` under current LlamaIndex.
  [`embeddings.py:22`](../../support_rag/embeddings.py#L22)

- Align KB chunking with `SentenceWindowNodeParser` API; rebuild `TextNode` when `ref_doc_id` is immutable.
  [`chunking.py:38`](../../support_rag/chunking.py#L38)

**HTTP auth surface**

- Exercise `require_service` on `/rag/health` with lifespan, patched startup `RAGService`, and typed `Request` override.
  [`test_auth_health.py:34`](../../tests/contract/test_auth_health.py#L34)

**R-10 idempotency**

- Double-run `chunk_kb` / `chunk_tickets` on the same ingest doc and compare ordered `id_` lists.
  [`test_chunk_id_ingest_idempotent.py:10`](../../tests/contract/test_chunk_id_ingest_idempotent.py#L10)

**Tooling and docs**

- Register `integration` / `requires_services` markers for pytest 8+.
  [`pyproject.toml:52`](../../pyproject.toml#L52)

- Document offline contract runs and `RUN_INTEGRATION` gate for future live tests.
  [`README.md:37`](../../README.md#L37)
