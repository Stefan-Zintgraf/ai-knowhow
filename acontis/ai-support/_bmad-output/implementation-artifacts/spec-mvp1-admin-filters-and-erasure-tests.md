---
title: 'MVP1 PRD — admin route contracts, R-5 filters, and delete/erasure tests'
type: 'feature'
created: '2026-04-25T18:00:00Z'
status: 'done'
baseline_commit: 'ddfda6524bb3a9a6112a6be516dafad77b9627e2'
context:
  - 'support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/spec-mvp1-prd-verification-hardening.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `support_rag_mvp1_prd.md` requires R-5 (metadata filters), R-11 and §2.8 item 4 (right-to-erasure), and NFR-7 (admin on index/delete). The offline suite covers health and service token, but not **admin** `POST`/`DELETE /rag/index/{namespace}`; `qfilter.to_qdrant_filter` is **untested**; there is no automated check that **delete** clears indexed content (even via mocks).

**Approach:** Add `pytest` tests: **HTTP** 401/200 for admin routes (mirror `test_auth_health.py` with `RAG_ADMIN_TOKEN`); **unit** tests for `to_qdrant_filter` (equality, `$in`, `created_at` range, unknown keys); **erasure** — mock `RAGService` or `QdrantClient.delete` / empty `aquery` so that **Given** a `parent_id` removed, **when** retrieve runs against mocks, **then** no chunk carries that `parent_id`. Defer real docker/Qdrant e2e to `requires_services` with `RUN_INTEGRATION=1` only if a follow task adds it.

## Boundaries & Constraints

**Always:** No provider SDKs. Offline by default. Reuse conftest patterns.

**Ask First:** Whether erasure should stay **100% mocked** in default CI, or add one optional live integration (time vs fidelity).

**Never:** Change wire schemas or RAG algorithms beyond test seams.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected | Error Handling |
|----------|---------------|----------|----------------|
| Admin index | No/wrong `Authorization` | 401 | Admin token + mocked `index` → 200 |
| Admin delete | Same | 401 / 200 | Bad namespace → 400 (optional assert) |
| `to_qdrant_filter` | `product`, `lang` `$in`, `created_at` | `Filter` `must` matches | None if empty/invalid only |

</frozen-after-approval>

## Code Map

- `support_rag/app.py` — `post_index`, `del_index` + `require_admin`.
- `support_rag/qfilter.py` — `to_qdrant_filter`.
- `support_rag/service.py` — `delete`, `_delete_one`, `retrieve` / `_query_one`.
- `tests/contract/test_auth_health.py` — ASGI + token pattern.

## Tasks & Acceptance

**Execution:**

- [x] `tests/unit/test_qfilter.py` — Cover `to_qdrant_filter` for None/empty, scalar equality, list/`$in`, `created_at` with `$gte`/`$lte` or `gte`/`lte`, unknown keys dropped, all-invalid → `None`.
- [x] `tests/contract/test_admin_index_delete.py` — `TestClient` + `dependency_overrides` for `get_service` (patched `RAGService` at startup; avoids `isinstance` on mock class) with `AsyncMock` for `index`/`delete`: 401 without admin bearer, 401 with service token only, 200 with `RAG_ADMIN_TOKEN`.
- [x] `tests/unit/test_service_delete_erasure.py` — Stubs `_query_one` / `_delete_one` on `rag_service_offline` to show post-`delete` retrieve has no chunk for that `parent_id` per PRD §2.8 #4.
- [x] `README.md` — Document `RAG_SERVICE_TOKEN` / `RAG_ADMIN_TOKEN` for admin contract tests.

**Acceptance Criteria:**

- Given default `pytest` (no `RUN_INTEGRATION`), when `pytest tests/ -q` runs, then all tests pass.
- Given `RAG_ADMIN_TOKEN` set, when `POST /rag/index/kb` lacks valid admin bearer, then status is 401; when the correct admin bearer and mocked `index` are used, then status is 200.
- Given `filters` examples from R-5, when `to_qdrant_filter` runs, then Qdrant `Filter` encodes the predicates.
- Given delete executed for a `parent_id` under test doubles, when retrieve is executed against the same doubles, then results exclude that `parent_id`.

## Spec Change Log

- 2026-04-25 — Added **Risks / pre-mortem** (elicitation) for test gaps and `app.py` coordination.
- 2026-04-25 — Implemented qfilter, admin index/delete, and service erasure tests; `TestClient` + `get_service` override (httpx 0.28 `ASGITransport` is async-only; see contract module docstring).

## Design Notes

Share fixtures with `test_auth_health` (lifespan, env monkeypatch) to avoid duplicate FastAPI app wiring.

## Risks / pre-mortem

*Failure imagined:* CI is green, but PRD R-5 / §2.8 #4 / NFR-7 are still doubted in review or manual smoke.

- **Erasure only proves stubs** — If retrieve is mocked empty without tying it to a **completed `delete`**, the test can pass while production wiring is wrong. Prefer asserting `delete` was awaited (or `RAGService.delete` called with expected args) *and* subsequent retrieve has no chunk for that `parent_id` on the same doubles. Optional `RUN_INTEGRATION` remains the only high-fidelity check if chosen under **Ask First**.
- **`to_qdrant_filter` vs runtime** — Unit matrix can pass while ingest/API use different key names or date shapes. Keep tests aligned with the same schema or constants the API uses for R-5.
- **Admin contract vs deployment** — ASGI 401/200 with patched `RAGService` covers wiring; still verify `RAG_ADMIN_TOKEN` / `require_admin` behavior matches how CI and containers set env, and add asserts for “optional” cases (e.g. bad `namespace` → 400) if the product wants them locked.
- **`app.py` with `spec-mvp1-otel-and-mcp-smoke.md`** — Both specs touch `app.py` (admin routes vs spans). Use one branch or a documented merge order to avoid half-wrapped routes (e.g. retrieve/delete inconsistent).

## Verification

**Commands:** `python -m pytest tests/ -q --tb=short` · `python -m ruff check support_rag tests`

**Manual checks:** None if CI green.

## Suggested Review Order

**Admin (NFR-7) / FastAPI**

- `get_service` override avoids `isinstance` on patched `RAGService`; mirrors `test_auth_health` override pattern
  [`test_admin_index_delete.py:33`](../../tests/contract/test_admin_index_delete.py#L33)

- 401/200 matrix for `POST/DELETE` with mocked `index` / `delete`
  [`test_admin_index_delete.py:50`](../../tests/contract/test_admin_index_delete.py#L50)

**R-5 `to_qdrant_filter`**

- None/empty, scalar, `$in`, `created_at` range, unknown keys, all-invalid → `None`
  [`test_qfilter.py:12`](../../tests/unit/test_qfilter.py#L12)

**§2.8 #4 erasure (offline doubles)**

- State flips in stubbed `_delete_one`; retrieve drops chunk for same `parent_id`
  [`test_service_delete_erasure.py:32`](../../tests/unit/test_service_delete_erasure.py#L32)

**Docs & backlog**

- Contract suite notes + R-5 pointer in README
  [`README.md:45`](../../README.md#L45)

- PRD gap table rows moved to Partial where this work landed
  [`mvp1-prd-to-automated-tests-gap-table.md:27`](mvp1-prd-to-automated-tests-gap-table.md#L27)
