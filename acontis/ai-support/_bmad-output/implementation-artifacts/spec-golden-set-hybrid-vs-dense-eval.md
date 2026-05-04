---
title: 'Golden-set hybrid vs dense retrieval eval'
type: 'feature'
created: '2026-04-25T12:00:00Z'
status: 'done'
baseline_commit: '29ba20abfeac5130f79a7ccc6e6ec4b856ff8bc6'
context:
  - 'support_rag_mvp1_prd.md'
  - 'eval/golden/questions.jsonl'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** MVP1 PRD requires hybrid + rerank to beat dense-only by ~≥10% on a small set (`support_rag_mvp1_prd.md` §16). `RAGService._query_one` always uses hybrid Qdrant mode; `RetrievalConfig.hybrid` affects `/rag/health` only, so no dense baseline exists.

**Approach:** Implement a real **dense-only** path (vector leg only). Add optional **per-request hybrid override** so one process can run both modes. Ship `eval/eval_hybrid_vs_dense.py` reading `eval/golden/questions.jsonl`, calling `POST /rag/retrieve` per mode, printing hit@k and lift; optional `ENFORCE_THRESHOLDS=1`. Document stack + seeding in `README.md`.

## Boundaries & Constraints

**Always:** No new provider SDKs. Gateway for all LLM/embeddings. Golden schema: `q`, `gold_doc_id`, `namespace` (`gold_doc_id` == ingest id / chunk `parent_id`). Keep **rerank on** for both modes unless you document an exception — isolate hybrid fusion impact.

**Ask First:** CI/self-hosted runner policy for this job (default: doc-only).

**Never:** Ragas, GraphRAG, broad retrieval rewrites, UI, or changing golden semantics without updating script + README.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|---------------|---------------------------|----------------|
| Eval row | Indexed `gold_doc_id`, live API | Two retrieves (hybrid on/off); record if `parent_id` matches in top-`k` | HTTP errors → non-zero exit, clear message |
| Threshold | `ENFORCE_THRESHOLDS=1`, lift &lt; 10% | Non-zero exit; print rates | Explicit fail allowed on smoke set |
| No service | Bad base URL | No silent success | Non-zero exit |

</frozen-after-approval>

## Code Map

- `support_rag/schemas.py` — extend `RetrievalRequest` (e.g. `hybrid: bool | None = None` → default from config).
- `support_rag/service.py` — `_query_one`: branch `VectorStoreQueryMode` / sparse leg per effective hybrid flag.
- `support_rag/config.py` — `RetrievalConfig.hybrid` as default when request field is `None`.
- `eval/golden/questions.jsonl` — smoke corpus.
- `tests/contract/test_health_capabilities.py` — adjust if capability semantics change.

## Tasks & Acceptance

**Execution:**

- [x] `support_rag/schemas.py` — Optional per-request hybrid override.
- [x] `support_rag/service.py` — Dense-only vs hybrid query construction; align behavior with `config.retrieval.hybrid` when override absent.
- [x] `eval/eval_hybrid_vs_dense.py` — JSONL loop, two modes, table + lift; `ENFORCE_THRESHOLDS=1`.
- [x] `README.md` — Qdrant + gateway + seed smoke parent doc; example eval command; CI note.
- [x] `tests/` — Cover mode selection without live Qdrant (mock or narrow unit around query build).

**Acceptance Criteria:**

- Given smoke KB indexed with id `doc-smoke-1`, when the eval script runs, then it prints hybrid and dense-only hit@k and relative lift %.
- Given `hybrid: false` (or equivalent) on `POST /rag/retrieve`, when the service handles the request, then retrieval uses dense-only (no sparse leg); with `true`, behavior matches prior hybrid path.
- Given `ENFORCE_THRESHOLDS=1`, when lift is below 10%, then exit non-zero with printed rates; otherwise zero.
- Given default `pytest`, when the suite runs offline, then all tests pass including new coverage.

## Spec Change Log

## Design Notes

Hit@k = fraction of rows where `gold_doc_id` ∈ returned chunks’ `parent_id` (top-`k`, e.g. 6). Lift = \((h-d)/d\); if \(d=0\), document in output (N/A or explicit error). Script: `httpx` OK if already a project dep.

## Verification

**Commands:**

- `py -3.12 -m pytest tests/ -q` — all pass.
- `py -3.12 eval/eval_hybrid_vs_dense.py --help` — CLI OK; full run per README with services.

**Manual checks (if no CLI):**

- Run eval with/without `ENFORCE_THRESHOLDS=1`; confirm exit codes vs measured lift.

## Suggested Review Order

**Retrieval mode**

- Effective hybrid merges request override with config before any namespace query.
  [`service.py:220`](../../support_rag/service.py#L220)

- Dense baseline uses `DEFAULT` Qdrant mode; hybrid keeps prior RRF fusion parameters.
  [`service.py:171`](../../support_rag/service.py#L171)

**API surface**

- Optional `hybrid` on `RetrievalRequest` for eval and clients.
  [`schemas.py:34`](../../support_rag/schemas.py#L34)

**Eval harness**

- Dual `POST /rag/retrieve` per row; hit@k, relative lift, optional threshold exit.
  [`eval_hybrid_vs_dense.py:104`](../../eval/eval_hybrid_vs_dense.py#L104)

**Operator docs**

- Seed curl, env vars, CI/self-hosted note for the live stack.
  [`README.md:47`](../../README.md#L47)

**Tests**

- Offline fixture asserts `VectorStoreQueryMode` for forced true/false/config default.
  [`test_retrieval_hybrid_flag.py:15`](../../tests/contract/test_retrieval_hybrid_flag.py#L15)
