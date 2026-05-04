---
title: 'MVP1 automation backlog — R-5 Qdrant filters, R-11/R-12/§2.8#4 live erasure'
type: 'feature'
created: '2026-04-25T12:00:00Z'
status: 'done'
baseline_commit: '69d3b453c4fa6fca26a011f69a384e499303e036'
context:
  - '_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-automation-first-gap-table.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
  - 'tests/integration/test_qdrant_optional_r11_r14.py'
  - 'README.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** MVP1 marks **R-5** (metadata filters on retrieve), **R-11** (delete removes all chunks for `parent_id`), **R-12** (re-index / replace by `parent_id`), and **§2.8#4** (erasure: after delete, retrieve has no hits) as **Must automate**, but live Qdrant coverage is only a shallow health/list check—no proof that filters, delete, and re-ingest behave correctly against real storage.

**Approach:** Add **opt-in integration tests** (`RUN_INTEGRATION=1`) that use a reachable Qdrant (and the configured LLM gateway for embeddings) to index documents with PRD metadata, run filtered retrieve, verify Qdrant-side counts/scroll where needed, exercise double-index replace semantics, and assert post-delete retrieve is empty for the erased ticket/id. Fix any implementation gaps in the same change set; update both gap tables when rows close.

## Boundaries & Constraints

**Always:**
- Skip cleanly when Qdrant URL is missing or unreachable (same pattern as `tests/integration/test_qdrant_optional_r11_r14.py` and `conftest.py`: `RUN_INTEGRATION=1` unblocks `integration` / `requires_services` markers).
- Document required env vars next to the integration module docstring (e.g. `RAG_QDRANT__URL` / `QDRANT_URL`, gateway URL for live embeds, tokens if tests call HTTP—mirror README).
- Default `pytest tests/ -q` remains green offline (skipped integration, not failing).
- Any production code fix ships **in the same PR** as the tests that prove it; refresh **`mvp1-prd-automation-first-gap-table.md`** and **`mvp1-prd-to-automated-tests-gap-table.md`** when automation state changes.

**Ask First:**
- Introducing a **new** integration marker file layout (e.g. splitting out of `test_qdrant_optional_r11_r14.py`) if the team prefers one module per PRD slice.
- Dropping or renaming collections on the shared dev Qdrant—prefer **unique `collection_prefix`** / isolated test prefix in config for integration runs if collision risk exists.

**Never:**
- Require live Qdrant or gateway in default CI without documented opt-in (no breaking offline developers).
- Fake “integration” by asserting only mocks; this spec is for **live** Qdrant round-trips.
- Leave automatable PRD rows in **Must automate** / **Partial** without updating the gap tables in the same merge.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| R-5 filter hit | Indexed `kb` doc with `metadata` carrying e.g. `product`, `lang`, `status`, `namespace`, numeric `created_at`; retrieve with matching `filters` | Returned chunks all satisfy filter; query without filter can still retrieve the doc | Skip if no Qdrant/embed gateway |
| R-5 filter miss | Same index; retrieve with contradictory `filters` (e.g. different `product`) | No chunks for that doc (empty or only other docs) | Same |
| R-11 post-delete storage | After `delete` for `parent_id`, scroll/count in Qdrant for payload `ref_doc_id` / filter on parent | Zero points for that parent in the namespace collection | Treat 404 collection as empty (aligned with `RAGService._delete_one`) |
| R-12 double index | Two `index` calls with same ingest `id` / `parent_id`, different text | Only one logical generation of chunks (count stable after second ingest; no duplicate chunk rows for old content) | Document actual semantics: `index` already pre-deletes by `id` before insert |
| §2.8#4 erasure | Delete ticket id then `retrieve` targeting that content (query + optional `filters.parent_id`) | Response has **no** chunks tied to erased parent | Same skip rules |

</frozen-after-approval>

## Code Map

- `support_rag/service.py` — `index` (pre-delete by doc id, `ainsert_nodes`), `retrieve` (`to_qdrant_filter`), `_delete_one` / `delete` (Qdrant `FilterSelector` on `ref_doc_id`).
- `support_rag/qfilter.py` — `to_qdrant_filter`; allowed keys include PRD metadata fields.
- `support_rag/chunking.py` — `_base_metadata` merges ingest `metadata` (`product`, `lang`, `created_at`, `status`, …) onto chunk payloads; `ref_doc_id` set to doc id.
- `tests/conftest.py` — `RUN_INTEGRATION` gates `integration` and `requires_services`.
- `tests/integration/test_qdrant_optional_r11_r14.py` — baseline live Qdrant smoke; extend here or add a focused sibling module.
- `tests/unit/test_qfilter.py` / `tests/unit/test_service_delete_erasure.py` — offline reference behavior (not substitutes for this spec).

## Tasks & Acceptance

**Execution:**

- [x] `tests/integration/test_qdrant_filters_erasure_live.py` — R-5: index with rich `metadata`, retrieve with filters, assert hit vs miss (`test_r5_filters_hit_and_miss_live`).
- [x] Same module — R-11: after `delete` for `parent_id`, Qdrant `count` with `ref_doc_id` filter is zero (`test_r11_delete_removes_points_live`).
- [x] Same — R-12: double `index` same doc `id`; old marker absent from retrieve, new marker present (`test_r12_reindex_replaces_content_live`).
- [x] Same — §2.8#4: delete then `retrieve` with `filters.parent_id`; empty chunks (`test_erasure_retrieve_empty_after_delete_live`).
- [x] `_bmad-output/implementation-artifacts/mvp1-prd-automation-first-gap-table.md` — R-5 / R-11 / R-12 / §2.8#4 → **Done** with test pointers.
- [x] `_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md` — **Covered (integration)** rows + change log + key artifacts.
- [x] `README.md` — Integration paragraph extended for `test_qdrant_filters_erasure_live.py`.

**Acceptance Criteria:**

- **Given** `RUN_INTEGRATION=1` and reachable Qdrant (+ working embed path as required by `index`/`retrieve`), **when** documents are indexed with PRD metadata and retrieve runs with matching and non-matching filters, **then** results respect metadata filters (R-5).
- **Given** chunks exist for a `parent_id`, **when** delete runs for that id, **then** Qdrant has no remaining points for that parent (R-11).
- **Given** two ingest operations with the same parent/document id, **when** inspection runs after the second, **then** stored chunks match replace semantics with no orphaned prior generation (R-12).
- **Given** erasure delete for a ticket/document id, **when** retrieve runs for content tied to that id, **then** the response contains no hits (§2.8#4).

## Spec Change Log

- **2026-04-25** — Draft from automation-first backlog (R-5, R-11, R-12, §2.8#4).
- **2026-04-25** — Step 2: expanded to full quick-dev spec template (frozen intent, I/O matrix, task paths).
- **2026-04-25** — Step 3: implemented `tests/integration/test_qdrant_filters_erasure_live.py`, gap tables, README; `baseline_commit` = HEAD at start of implementation.

## Design Notes

`RAGService.index` already collects unique ingest ids and calls `_delete_one` before insert, so R-12 is expected to be **replace-by-id** (second ingest wins). Integration tests should encode that contract explicitly so regressions surface if ordering or delete scope changes.

## Verification

**Commands:**

- `py -3.12 -m pytest tests/ -q` — expected: all pass offline; integration tests skipped without `RUN_INTEGRATION=1`.
- `set RUN_INTEGRATION=1` (PowerShell) then `py -3.12 -m pytest tests/integration/ -q -m "integration or requires_services"` — expected: new tests pass against live Qdrant when env is configured; documented skips when URL missing.

**Manual checks (if no CLI):**

- Once per environment: confirm Qdrant URL and gateway embedding match `config` vector size; seed/collection_prefix does not clobber shared data you care about.

## Suggested Review Order

**Live Qdrant integration**

- Isolated `collection_prefix` plus `load_config()` keeps vector size aligned with YAML/env.
  [`test_qdrant_filters_erasure_live.py:27`](../../tests/integration/test_qdrant_filters_erasure_live.py#L27)

- R-11 proof uses Qdrant `count` on payload `ref_doc_id`, 404 → zero like production delete.
  [`test_qdrant_filters_erasure_live.py:44`](../../tests/integration/test_qdrant_filters_erasure_live.py#L44)

- Fixture deletes `kb`/`tickets` collections after `aclose` to limit test pollution.
  [`test_qdrant_filters_erasure_live.py:66`](../../tests/integration/test_qdrant_filters_erasure_live.py#L66)

- R-5 hit/miss, R-12 replace markers, §2.8#4 `parent_id` filter erasure scenarios.
  [`test_qdrant_filters_erasure_live.py:86`](../../tests/integration/test_qdrant_filters_erasure_live.py#L86)

**PRD / docs**

- Automation-first table: R-5, R-11, R-12, §2.8#4 marked **Done** with test pointers.
  [`mvp1-prd-automation-first-gap-table.md:43`](./mvp1-prd-automation-first-gap-table.md#L43)

- Coverage gap table: **Covered (integration)** rows and key-artifacts item 6.
  [`mvp1-prd-to-automated-tests-gap-table.md:44`](./mvp1-prd-to-automated-tests-gap-table.md#L44)

- README integration blurb; residual-gaps sentence no longer lists R-12 as missing.
  [`README.md:39`](../../README.md#L39)
