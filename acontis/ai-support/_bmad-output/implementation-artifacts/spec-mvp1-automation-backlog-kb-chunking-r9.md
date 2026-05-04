---
title: 'MVP1 automation backlog — R-9 KB vs tickets + KB chunk_size bound'
type: 'feature'
created: '2026-04-25T12:00:00Z'
status: 'done'
baseline_commit: '9746c874a715a5ee115988c083744e64373c23f6'
context:
  - '_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-automation-first-gap-table.md'
  - '_bmad-output/implementation-artifacts/deferred-work.md'
  - 'support_rag/chunking.py'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** R-9 / PRD §2.6 require KB chunking to honor `config.chunking.kb.chunk_size` (default 512). `chunk_kb` only uses `window_size` on `SentenceWindowNodeParser`; `chunk_size` is unused (gap table **deviation** row + `deferred-work.md`).

**Approach:** Make `chunk_size` **observed** in `chunk_kb` (e.g. `SentenceSplitter` or equivalent + sentence-window flow per `deferred-work.md`—types are implementation). Add small goldens: kb vs tickets counts, max chunk length (policy in test docstring + `config.example.yaml`). Update **both** gap tables; resolve `deferred-work` entry. Bump `chunker_version.kb` + ID tests only if same-input outputs change materially.

## Boundaries & Constraints

**Always:** Do not change tickets chunking semantics (`chunk_tickets`: `qa_pairs`, body, summary). Keep fixtures small and CI-fast. Any material change to KB chunk outputs for the same `parent_id` must include a deliberate `chunker_version.kb` bump and coordinated ID/golden updates.

**Ask First:** If LlamaIndex only offers a character-based splitter but PRD text reads “tokens,” whether to document the effective policy in PRD/config comments vs. add a tokenizer dependency—**halt** and get a one-line product choice before merging a behavior that contradicts the PRD’s token wording.

**Never:** Leave `chunk_size` unused after this work; drop R-9 kb-vs-tickets coverage; update only one of the two gap tables.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected | Errors |
|----------|----------------|----------|--------|
| Default kb vs tickets | Long multi-sentence text; tickets body-only | `len(chunk_kb) > len(chunk_tickets)`; chunks respect length policy | N/A |
| Tight N | Same fixture; `chunking.kb.chunk_size` very small (e.g. 80) | More KB chunks than default; no chunk over bound | N/A |

</frozen-after-approval>

## Code Map

- `support_rag/chunking.py` — `chunk_kb` reads and applies `chunking.kb.chunk_size`.
- `support_rag/config.py`, `config.example.yaml` (if any) — align comments with length policy.
- `tests/unit/test_chunking_kb_vs_tickets_r9.py` — counts + max length + small-`chunk_size` case.
- `tests/unit/test_chunk_id*.py` — only if `chunker_version.kb` bumps.
- `mvp1-prd-*.md` gap tables (both) + `deferred-work.md` — close R-9 / deviation; supersede deferred entry.

## Tasks & Acceptance

**Execution:**

- [x] `support_rag/chunking.py` — Implement KB chunking so `config.chunking.kb.chunk_size` affects emitted `TextNode` texts (not ignored); keep `window_size` behavior where still applicable.
- [x] `tests/unit/test_chunking_kb_vs_tickets_r9.py` — Assert kb vs tickets count relationship; add **max length** check with policy stated in docstring; add case with reduced `chunk_size` proving the config is observed.
- [x] `_bmad-output/implementation-artifacts/mvp1-prd-automation-first-gap-table.md` + `mvp1-prd-to-automated-tests-gap-table.md` — Move R-9 / deviation to closed/covered; one line each on where tested.
- [x] `_bmad-output/implementation-artifacts/deferred-work.md` — Resolve or supersede the KB chunk_size entry.
- [x] `chunker_version.kb` → `kb-v2` — hash-based `test_chunk_id.py` unchanged; idempotency contract tests still pass.

**Acceptance Criteria:**

- **Given** a fixed KB fixture and `chunking.kb.chunk_size` = **N**, **when** `chunk_kb` runs, **then** every emitted chunk respects the documented length policy and tests’ golden expectations (R-9, deviation).
- **Given** the same parent text in kb vs tickets (body-only), **when** both chunkers run, **then** strategy difference matches PRD §2.3.2 / §2.6 (multi-chunk sentence-window style vs single body chunk).
- **Given** wiring is complete, **when** unit tests run, **then** changing `chunking.kb.chunk_size` changes KB output (not a no-op).

## Spec Change Log

- **2026-04-25** — Template replan (frozen block, I/O, tasks, gaps/deferred-work).
- **2026-04-25** — Implemented: `SentenceSplitter` + `SentenceWindowNodeParser`, `kb-v2`, gap tables + deferred-work, R-9 tests.

## Verification

**Commands:** `pytest tests/unit/test_chunking_kb_vs_tickets_r9.py -q` · `pytest tests/unit/test_chunk_id.py tests/unit/test_chunk_id_ingest_idempotent.py -q` (if versions touched) · `pytest tests/ -q` · `ruff check .`

**Manual checks:** None if unit goldens pass.

## Suggested Review Order

**KB token bound + windows**

- Wire `chunk_size` via `SentenceSplitter.split_text` as custom `sentence_splitter` for sentence windows.
  [`chunking.py:39`](../../support_rag/chunking.py#L39)

- Bump default chunker version when KB segment boundaries change for the same text.
  [`config.py:82`](../../support_rag/config.py#L82)

**Proof in tests**

- Count, max token length, and sensitivity to smaller `chunk_size` for the shared long fixture.
  [`test_chunking_kb_vs_tickets_r9.py:22`](../../tests/unit/test_chunking_kb_vs_tickets_r9.py#L22)

**Ops / docs**

- Example config + comment for token budget and `kb-v2`.
  [`config.example.yaml:45`](../../config.example.yaml#L45)

**Traceability**

- Automation-first table: R-9 + deviation row closed.
  [`mvp1-prd-automation-first-gap-table.md:27`](./mvp1-prd-automation-first-gap-table.md#L27)

- Detailed gap table: R-9 covered.
  [`mvp1-prd-to-automated-tests-gap-table.md:47`](./mvp1-prd-to-automated-tests-gap-table.md#L47)

- Deferred entry superseded.
  [`deferred-work.md:21`](./deferred-work.md#L21)
