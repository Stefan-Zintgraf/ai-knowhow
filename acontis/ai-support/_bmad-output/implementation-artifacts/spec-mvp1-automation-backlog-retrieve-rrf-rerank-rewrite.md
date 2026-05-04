---
title: 'MVP1 automation backlog — R-2 RRF merge, R-3 rerank contract, R-4 rewrite/HyDE'
type: 'feature'
created: '2026-04-25T12:00:00Z'
status: 'done'
baseline_commit: '5bb3cbc3cf587b6d1be2afa7a810fb3e1b4d474e'
context:
  - '_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-automation-first-gap-table.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** MVP1 rows R-2, R-3, and R-4 in [`mvp1-prd-automation-first-gap-table.md`](mvp1-prd-automation-first-gap-table.md) are **Must automate**, but current tests only partially cover RRF **merge** behavior, rerank **ordering** beyond “`predict` was called”, and rewrite/HyDE **gateway slot** semantics on the offline fixture path.

**Approach:** Add focused unit and contract tests that call the same helpers as production—`_rrf_k_lists` in [`support_rag/service.py`](../../support_rag/service.py) for multi-list RRF, the existing rerank path in `retrieve` for score→order, and the gateway/rewrite/HyDE paths for `chat_completion_sync` and `X-Slot`. Update both gap tables in the same change when automation state advances.

## Boundaries & Constraints

**Always:** No provider SDKs (R-17); all LLM traffic via `LLMGatewayClient`. Default CI (no `slow`/`integration`) must stay fast—model loads stay behind `pytest.mark.slow` or `pytest.mark.integration` when using a real `CrossEncoder`. When a row becomes **Covered** / **Done**, update [`mvp1-prd-to-automated-tests-gap-table.md`](mvp1-prd-to-automated-tests-gap-table.md) and [`mvp1-prd-automation-first-gap-table.md`](mvp1-prd-automation-first-gap-table.md) in the same commit.

**Ask First:** Whether to add an optional **slow** job for a tiny real CE on CPU (if stub-only ordering tests are chosen for the merge gate).

**Never:** Change RRF or rerank product behavior solely to make tests pass; do not add provider SDKs; do not mark R-2/R-3/R-4 **Done** in the automation-first table without the mandated tests and table updates.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error handling |
|----------|---------------|----------------------------|----------------|
| R-2 RRF | Two or more fixed rank lists of `TextNode` with known ids; fixed `rrf_k` and `cap` | Merged order matches `_rrf_k_lists` scoring: per list, rank `r` contributes `1/(rrf_k + r + 1)`; global sort by sum descending | N/A |
| R-3 rerank order | `rerank=True`; CE `predict` returns a fixed vector of raw scores for merged nodes | Final chunk order matches sort by `sigmoid(raw)` descending; respects `min_score` if set | Malformed `predict` output already handled in service |
| R-4 rewrite slot | `rewrite=True`, query rewrite enabled; `MockTransport` or assertable client | `POST /v1/chat/completions` includes `X-Slot` = configured `retrieval_slot` (see existing R-16 pattern) | N/A |
| R-4 HyDE gate | `hyde.enabled` false vs true | When false, no HyDE completion; when true, an extra `chat_completion_sync` (or equivalent path) for hypothetical text | Covered by service logic—extend tests to pin behavior |

</frozen-after-approval>

## Code Map

- [`support_rag/service.py`](../../support_rag/service.py) -- `_rrf_k_lists` (multi-query / multi-namespace RRF merge used after `_query_one` loops); `retrieve` orchestrates HyDE, rewrite, embed, merge, `CrossEncoder.predict`, and `min_score`.
- [`support_rag/rrf.py`](../../support_rag/rrf.py) -- `reciprocal_rank_fusion` / `make_rrf_fusion_fn` (Qdrant hybrid dense+sparse fusion; same RRF weight formula as `_rrf_k_lists`).
- [`support_rag/gateway.py`](../../support_rag/gateway.py) -- `chat_completion_sync(..., slot=None)` → `X-Slot` via `_slot_headers`; default slot `config.retrieval_slot` when `slot` omitted.
- [`tests/contract/test_retrieve_rerank_path.py`](../../tests/contract/test_retrieve_rerank_path.py) -- R-3: today asserts `predict` call vs skip; extend for ordering.
- [`tests/contract/test_retrieve_rewrite.py`](../../tests/contract/test_retrieve_rewrite.py) -- R-4: rewrite alts and HyDE off; extend for HyDE on and/or slot.
- [`tests/contract/test_service_gateway_roundtrip.py`](../../tests/contract/test_service_gateway_roundtrip.py) -- R-16 reference: `X-Slot` on rewrite chat; reuse pattern for R-4 slot assertions.
- [`tests/unit/`](../../tests/unit/) -- new or extended unit tests for `_rrf_k_lists` (R-2).

## Tasks & Acceptance

**Execution:**

- [x] [`tests/unit/test_rrf_k_lists_r2.py`](../../tests/unit/test_rrf_k_lists_r2.py) (new) -- Import `_rrf_k_lists` from `support_rag.service` and build two (or more) synthetic ranked lists of `TextNode` with **distinct** `id_` so ranks interact non-trivially. Assert the merged id order and/or scores match the RRF rule for a fixed `rrf_k` (same recurrence as in [`support_rag/rrf.py`](../../support_rag/rrf.py)). Rationale: closes R-2 without touching Qdrant.
- [x] [`tests/contract/test_retrieve_rerank_path.py`](../../tests/contract/test_retrieve_rerank_path.py) (extend) or adjacent new test module -- With mocked `aquery` returning ≥2 `TextNode`s, stub `ce.predict` to return **known** monotonic scores, run `retrieve` with `rerank=True` and `min_score=None` (or set `min_score` in one case). Assert result chunk order matches the documented **score contract** (sigmoid then sort descending) in the test module docstring. Rationale: R-3 beyond mock presence.
- [x] [`tests/contract/test_retrieve_rewrite.py`](../../tests/contract/test_retrieve_rewrite.py) and/or [`tests/contract/test_service_gateway_roundtrip.py`](../../tests/contract/test_service_gateway_roundtrip.py) (extend) -- (1) Prove rewrite path issues a chat to the gateway with **`X-Slot` = `retrieval_slot`** using the same `httpx`/transport pattern as `test_retrieve_rewrite_chat_uses_retrieval_slot_and_trace_r16` if not already fully duplicated on the offline path. (2) Add **HyDE on**: `hyde.enabled` True, assert `_hyde` (or the HyDE `chat_completion_sync` path) is invoked once and a non-HyDE-only retrieve does not call it. Rationale: R-4 slot + HyDE gating.

**Acceptance Criteria:**

- **Given** two controlled ranked lists, **when** `_rrf_k_lists` merges them, **then** the output node order matches the implementation’s RRF score aggregation (R-2).
- **Given** rerank is on and `predict` returns fixed scores, **when** `retrieve` completes, **then** returned chunks are ordered per the sigmoid-based contract (R-3).
- **Given** query rewrite is enabled, **when** a rewrite runs, **then** the rewrite chat request uses the configured retrieval slot on `X-Slot`; **given** HyDE is off, **when** retrieve runs, **then** the HyDE completion path is not used; **given** HyDE is on, **when** retrieve runs, **then** the HyDE completion path runs (R-4).

## Spec Change Log

- **2026-04-25** — Step-05: implementation complete; status **done**; Suggested Review Order appended; R-2/R-3/R-4 tests + gap tables.
- **2026-04-25** — Draft from automation-first backlog; Step-02 filled `spec-template` (intent frozen, I/O matrix, code map, tasks, verification). Prior draft content merged into frozen block and Design Notes.

## Design Notes

- **RRF formula in scope:** `score(id) += 1.0 / (rrf_k + rank + 1)` for each list where the id appears, then sort by `score` descending. `_rrf_k_lists` in `service.py` is the function used after collecting per-query, per-namespace lists in `retrieve`.
- **R-3 stub docstring:** State explicitly: normalized scores = `1/(1+exp(-raw))`, sort descending; tie-break is Python sort stability—tests should use scores that avoid ambiguous ties.
- **R-4 vs R-16:** R-16 already proves rewrite + `X-Slot` in roundtrip tests; this spec adds **offline/contract** coverage or explicit HyDE on so the gap table can move R-4 without duplicate meaningless tests—prefer **one** clear test per concern.

## Verification

**Commands:**

- `pytest tests/ -q` -- expected: all green; new tests run in default selection.
- `pytest tests/unit/test_rrf_k_lists_r2.py tests/contract/test_retrieve_rerank_path.py tests/contract/test_retrieve_rewrite.py -q` -- expected: targeted files green.
- `ruff check .` -- expected: no new violations.

**Manual checks:** None for MVP1 if CI markers and mocks are correct.

## Suggested Review Order

**RRF merge (R-2)**

- Two-list hand-checked RRF scores vs `_rrf_k_lists` output id order.
  [`test_rrf_k_lists_r2.py:14`](../../tests/unit/test_rrf_k_lists_r2.py#L14)

**Rerank sigmoid (R-3)**

- Module docstring states sigmoid; three-node `predict` stub fixes chunk order.
  [`test_retrieve_rerank_path.py:91`](../../tests/contract/test_retrieve_rerank_path.py#L91)

- `min_score` after sigmoid uses midpoint threshold to keep one chunk.
  [`test_retrieve_rerank_path.py:136`](../../tests/contract/test_retrieve_rerank_path.py#L136)

**Rewrite / HyDE HTTP (R-4)**

- Tcp-free `RAGService` + recorded `httpx` (same idea as service roundtrip tests).
  [`test_retrieve_rewrite.py:31`](../../tests/contract/test_retrieve_rewrite.py#L31)

- Rewrites assert first chat `X-Slot` matches `retrieval_slot`.
  [`test_retrieve_rewrite.py:189`](../../tests/contract/test_retrieve_rewrite.py#L189)

- HyDE-only path: exactly one chat completion, same slot on header.
  [`test_retrieve_rewrite.py:233`](../../tests/contract/test_retrieve_rewrite.py#L233)

**PRD / automation tables**

- R-2–R-4 row updates + change log in automation-first and detailed gap tables.
  [`mvp1-prd-automation-first-gap-table.md:39`](./mvp1-prd-automation-first-gap-table.md#L39)
