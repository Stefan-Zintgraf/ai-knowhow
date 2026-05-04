---
title: 'MVP1 PRD — residual test gaps (R-8, R-9, R-11, R-12, R-14, R-18, NFR-4, NFR-5, NFR-6, §2.8#4 opt)'
type: 'feature'
created: '2026-04-25T20:00:00Z'
status: 'done'
baseline_commit: 'e812a0362eabecbc9b8ce64375619cf0fcbe21aa'
context:
  - 'support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The five “Suggested next steps” in the gap table do not cover every **Partial** / **Missing** row. This spec tracks **residual** automation: R-8 (index body Pydantic edge cases), R-9 (KB vs tickets chunking depth), R-11 (optional real Qdrant delete), R-12 (incremental ingest / replace by `parent_id`), R-14 (live capabilities), R-18 (local cross-encoder smoke), NFR-4 (OTel/Langfuse extras beyond current routes), NFR-5 (`chunker_version` + embedding id in metadata), NFR-6 (stateless / restart), §2.8#4 (optional live erasure after delete).

**Approach:** Implement **in priority order** (adjust as product demands): (1) fast offline tests — Pydantic validation for index request, NFR-5 metadata keys on chunk objects after index path with mocks, NFR-6 light lifecycle test; (2) optional `requires_services` / `integration` tests for R-11, R-12, R-14, §2.8#4; (3) R-9 as golden chunk-count fixture or larger follow PR; (4) R-18 as slow/marked test.

## Boundaries & Constraints

**Always:** Default CI stays fast; mark heavy tests. Update `mvp1-prd-to-automated-tests-gap-table.md` in the same commit as each batch lands.

**Ask First:** Whether R-12/R-11 live tests justify a Qdrant testcontainer vs manual integration.

**Never:** Block PRs on R-18 if cross-encoder download is slow without cache.

## I/O & Edge-Case Matrix

| ID | Scenario | Expected |
|----|-----------|----------|
| R-8 | Invalid `IndexRequest` body | 422 or validation error as implemented |
| R-9 | Same parent in kb vs tickets namespace | Documented chunk count diff per PRD chunking |
| R-12 | Re-ingest same `parent_id` | Replaces; new `parent_id` adds (under mocks or live) |
| NFR-5 | After chunk+stamp | Metadata includes `chunker_version` and embedding id fields |
| NFR-6 | Two `RAGService` / app lifecycles | No shared mutable corruption (or doc-only if non-measurable) |

</frozen-after-approval>

## Code Map

- `support_rag/app.py` — index route, Pydantic models.
- `support_rag/chunking.py` — `chunk_kb`, `chunk_tickets`.
- `support_rag/service.py` — `index`, `delete`, metadata stamping.
- `support_rag/reranker.py` or cross-encoder import path — R-18.
- `tests/contract/test_otel_routes.py` — extend for NFR-4 if new spans.
- `tests/contract/test_admin_index_delete.py`, `test_service_delete_erasure.py` — patterns for R-11, §2.8#4.

## Tasks & Acceptance

**Execution:**

- [x] R-8 — `tests/contract/test_index_request_validation.py` (or extend admin tests) for invalid/malformed `docs` payloads without Qdrant.
- [x] NFR-5 — `tests/unit/test_chunk_metadata_nfr5.py` assert keys on `TextNode.metadata` (or post-index stub) per PRD.
- [x] R-12 — unit or `requires_services` test: two ingests same `parent_id` → one logical set; new id adds (clarify against PRD wording).
- [x] R-9 — deferred subfolder or one test: fixture doc producing expected chunk counts for kb vs tickets (size kept small).
- [x] R-11 / §2.8#4 — optional `RUN_INTEGRATION=1` test file calling real Qdrant per README.
- [x] R-14 — document offline mock vs optional live job; one assertion if live job exists.
- [x] R-18 — `pytest.mark.slow` import/dry-run or skip if `TRANSFORMERS_OFFLINE=1`.
- [x] NFR-6 — test or design note in README if not automatable in-repo.

**Acceptance Criteria:**

- Given each implemented row, when the relevant test runs, then the gap table can move that row from Missing/Partial to Covered or an honest **Partial** with reason.
- Given default `pytest`, when no integration env, then new integration tests are skipped.

## Spec Change Log

- 2026-04-25 — Created to cover PRD rows not included in the five primary “Suggested next steps” specs.
- 2026-04-25 — Implemented residual test rows (R-8, R-9, R-12, R-11/§2.8#4 opt, R-14, R-18, NFR-5, NFR-6); gap table and README updated.

## Design Notes

Split into follow-up PRs by row if this spec feels large during implementation; keep this file as the **index** and update its tasks when child specs are added.

## Verification

**Commands:** `pytest tests/ -q` · `ruff check .`

**Manual checks:** Live Qdrant path once per release if R-11/R-12 integration enabled.

## Suggested Review Order

**R-8 and HTTP validation**

- Malformed `IndexRequest` contract via `TestClient` without touching Qdrant.
  [`test_index_request_validation.py:40`](../../tests/contract/test_index_request_validation.py#L40)

**NFR-5 / R-12 (index metadata and replace-by-parent)**

- Stamps `embedding_model` on all nodes after `embed_sync` probe; chunkers carry `chunker_version`.
  [`test_chunk_metadata_nfr5.py:16`](../../tests/unit/test_chunk_metadata_nfr5.py#L16)
- Re-index same `parent_id` deletes twice; batch of two parents yields one `ainsert` with both.
  [`test_index_replace_by_parent_id_r12.py:15`](../../tests/unit/test_index_replace_by_parent_id_r12.py#L15)

**R-9 chunking diff**

- Same paragraph: kb windowing vs tickets body-only and qa+summary counts.
  [`test_chunking_kb_vs_tickets_r9.py:22`](../../tests/unit/test_chunking_kb_vs_tickets_r9.py#L22)

**Optional live Qdrant (R-11, R-14 touchpoints)**

- `RUN_INTEGRATION=1` lists collections; documents partial R-14 proxy.
  [`test_qdrant_optional_r11_r14.py:23`](../../tests/integration/test_qdrant_optional_r11_r14.py#L23)

**R-18 and NFR-6**

- Configured reranker id + slow CrossEncoder load (skips on Hub errors); two offline service lifecycles.
  [`test_cross_encoder_r18_smoke.py:14`](../../tests/unit/test_cross_encoder_r18_smoke.py#L14)
- [`test_service_lifecycle_nfr6.py:32`](../../tests/unit/test_service_lifecycle_nfr6.py#L32)

**Docs and config**

- Pytest `slow` marker; README explains residual/optional integration; gap table status refresh.
  [`README.md:37`](../../README.md#L37) · [`pyproject.toml:55`](../../pyproject.toml#L55)
