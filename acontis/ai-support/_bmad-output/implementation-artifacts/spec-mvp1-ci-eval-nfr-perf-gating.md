---
title: 'MVP1 PRD — CI eval job + NFR-1/2 performance gating'
type: 'feature'
created: '2026-04-25T20:00:00Z'
status: 'done'
baseline_commit: 'd9ae12ec696d1945d177db9f54fbc6a7167b1e55'
context:
  - 'support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
  - '_bmad-output/implementation-artifacts/deferred-work.md'
  - '_bmad-output/implementation-artifacts/spec-golden-set-hybrid-vs-dense-eval.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The gap table lists §2.8(1)(2) (hybrid eval, ≥10% lift) as partial, NFR-1 (p95 retrieve ≤2s) and NFR-2 (≥5 concurrent) as **Planned (deferred)** in `deferred-work.md`. The eval script `eval/eval_hybrid_vs_dense.py` exists but is not the default PR gate; performance evidence needs a self-hosted or scheduled runner and a seeded corpus.

**Approach:** **Document and wire** (not necessarily in default GHA `ubuntu` minutes): a **scheduled** or **self-hosted** workflow and/or k6/locust job that (1) runs `eval_hybrid_vs_dense` with optional `ENFORCE_THRESHOLDS=1`, (2) runs retrieve latency / concurrency checks against a seeded Qdrant + app, and (3) states clearly whether failure is **blocking** or **report-only**. Update `deferred-work.md` and `README.md` with how to go “green” and what remains human (e.g. golden labeling).

## Boundaries & Constraints

**Always:** Reuse `eval/eval_hybrid_vs_dense.py` and existing compose/README patterns. Do not delete offline default `pytest` as the main developer loop.

**Ask First:** Which CI system gets the job (GHA self-hosted, Azure DevOps, internal Jenkins); p95 and concurrency SLO values for **your** corpus; whether threshold enforcement is on for PRs or only `main`.

**Never:** Block default developer PRs on jobs that need GPUs or 10GB indexes unless the org explicitly wants that.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected | Error handling |
|----------|---------------|----------|----------------|
| Eval job | Seeded Qdrant + env | Script exits 0 with thresholds met, or non-zero with `ENFORCE_THRESHOLDS=1` | Document fail as dataset/SLO issue |
| NFR-1 | k6 or pytest-benchmark | p95 under budget on runner | Flake retry policy documented |
| NFR-2 | 5+ parallel retrieve | No queueing / errors per PRD | Tune uvicorn workers in compose doc |

</frozen-after-approval>

## Code Map

- `eval/eval_hybrid_vs_dense.py` — hybrid vs dense retrieve, `ENFORCE_THRESHOLDS=1` exit rules (see script).
- `eval/golden/questions.jsonl` — `gold_doc_id` / namespace; must match seeded Qdrant parent.
- `README.md` — extend with **MVP1 eval + perf CI** (pipeline link, blocking vs report-only).
- `deferred-work.md` (under `_bmad-output/implementation-artifacts/`) — dedupe NFR/eval bullets after merge.
- [`../../.gitlab-ci.yml`](../../.gitlab-ci.yml) — heavy jobs on tag `rag-mvp1-eval`; schedule, web, API, parent, or **manual** push (not MR); token/URL via **CI/CD variables**.
- [`../../scripts/nfr_retrieve_smoke.py`](../../scripts/nfr_retrieve_smoke.py) — p95 + concurrent smoke; `NFR_ENFORCE` for blocking vs report-only.

## Tasks & Acceptance

**Execution:**

- [x] `README.md` — **MVP1 eval + perf CI**: prereqs, eval + `ENFORCE_THRESHOLDS`, links to `spec-golden-set-hybrid-vs-dense-eval.md` and **`.gitlab-ci.yml`**, blocking vs report-only matrix, runner **tag** name and how to move to another machine.
- [x] `.gitlab-ci.yml` — Job(s) with `tags: [rag-mvp1-eval]` (or the chosen tag), Python, CI variables, `python eval/eval_hybrid_vs_dense.py`; optional NFR step; `rules` for schedule and/or manual; document skip vs fail; `resource_group` or `concurrency` if needed.
- [x] `_bmad-output/implementation-artifacts/deferred-work.md` — Cross-link; mark superseded NFR/eval items this spec covers.
- [x] Optional `scripts/*nfr*` — Document env, exit codes, and report-only skip behavior if used.

**Acceptance Criteria:**

- Given a documented self-hosted or scheduled path, when an operator follows `README` steps, then they can run eval + one perf check with a known exit code contract.
- Given `ENFORCE_THRESHOLDS=1` and thresholds unmet, when the eval job runs, then it fails explicitly (for jobs where enforcement is enabled).
- Given the gap table, when this work merges, then rows for §2.8(1)(2) and NFR-1/2 are updated to **Covered** (scheduled) or **Partial** with an honest note—not left **Missing** if automation exists.

## Spec Change Log

- 2026-04-25 — **in-review:** Implemented [`.gitlab-ci.yml`](../../.gitlab-ci.yml) (`hybrid_golden_eval`, `nfr_retrieve_smoke`), [README](../../README.md#mvp1-eval--perf-ci-gitlab) matrix, [`scripts/nfr_retrieve_smoke.py`](../../scripts/nfr_retrieve_smoke.py), `deferred-work.md` + gap table updates; baseline `d9ae12ec696d1945d177db9f54fbc6a7167b1e55`.
- 2026-04-25 — **ready-for-dev:** GitLab + tagged local runner, portability via shared tag, initial gating = not MR (see **Resolved decisions**). Code map/tasks pointed at `.gitlab-ci.yml` (not GHA).
- 2026-04-25 — Step 02 plan refresh: code map, tasks, AC; checkpoint.
- 2026-04-25 — From gap table item 3; draft had pending `Ask First`.

## Resolved decisions (pre-implementation)

Decisions below implement the **Ask First** list without editing the **frozen** block. Renegotiate the frozen block only if this contradicts product intent.

| Topic | Decision |
|--------|----------|
| **CI** | **GitLab CI** (not GitHub Actions). |
| **Runner** | **GitLab Runner** on the **local machine** for now; use a **single tag** (default name `rag-mvp1-eval` — change in one place in `.gitlab-ci.yml` if you prefer). Another machine = register a runner with the **same tag**, disable the old one. |
| **NFR p95 / concurrency** | **PRD targets** (2.0s p95, ≥5 concurrent) stay the **stated goal**; first pipeline iteration may be **report-only** or **skip** NFR job until SLO numbers are fixed for your corpus. |
| **Enforcement** | **Eval with `ENFORCE_THRESHOLDS=1`:** wire for **manual / scheduled** jobs on the tagged runner first; **do not** make it a **merge request** required check until you **explicitly** add `rules: merge_request` + README. |

## Design Notes

**Process + wiring** (GitLab YAML + docs). Do not block the default **offline `pytest`** job; RAG eval stays on a **tagged** runner, not shared SaaS runners without your stack.

## Verification

**Commands:** Validate `.gitlab-ci.yml` (IDE/GitLab pipeline editor, `yamllint`, or `glab` if available). `py -3.12 eval/eval_hybrid_vs_dense.py --help`.

**Manual:** Run a **manual** pipeline or **schedule** on a branch; README matrix matches job outcomes (red/green, report-only, skip).

## Suggested Review Order

**GitLab pipeline**

- Tagged runner, MR exclusion, schedule/web vs push-manual; shared template for both jobs.
  [`.gitlab-ci.yml:16`](../../.gitlab-ci.yml#L16)

- Eval job wires `eval_hybrid_vs_dense` and required `RAG_SERVICE_TOKEN` / base URL.
  [`.gitlab-ci.yml:44`](../../.gitlab-ci.yml#L44)

- NFR job stays `allow_failure` until SLO sign-off; calls the smoke script.
  [`.gitlab-ci.yml:51`](../../.gitlab-ci.yml#L51)

**NFR smoke**

- `main()`: load smoke query, sequential samples for p95, thread pool of independent clients.
  [`nfr_retrieve_smoke.py:62`](../../scripts/nfr_retrieve_smoke.py#L62)

- `NFR_ENFORCE` maps p95, concurrency errors, and budget to a non-zero exit.
  [`nfr_retrieve_smoke.py:144`](../../scripts/nfr_retrieve_smoke.py#L144)

**Docs & traceability**

- Operator matrix for blocking vs report-only and variable list.
  [`README.md:85`](../../README.md#L85)

- `deferred-work` cross-links; NFR items superseded with ops remainder.
  [`deferred-work.md:7`](deferred-work.md#L7)

- Gap table: NFR-1/2 rows now point at GitLab + script.
  [`mvp1-prd-to-automated-tests-gap-table.md:65`](mvp1-prd-to-automated-tests-gap-table.md#L65)
