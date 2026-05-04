---
title: 'MVP1 — §2.8#5 scheduled E2E, script/golden CI, deferred-work traceability'
type: 'feature'
created: '2026-04-25T12:00:00Z'
status: 'done'
baseline_commit: '479cafef8e8396317c953d7fa60dffd37817c5ed'
context:
  - '_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-automation-first-gap-table.md'
  - '_bmad-output/implementation-artifacts/deferred-work.md'
  - 'docs/runbook-allow-remote-false-e2e.md'
  - '.gitlab-ci.yml'
  - 'README.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** PRD §2.8#5 and §2.11 need **automated** proof: scheduled **self-hosted** run of `e2e_privacy` after gateway preflight; **no-network** CI smoke for `reindex`/`seed_kb` and a **≥30** line gate on `eval/golden/questions.jsonl`; `deferred-work.md` follow-ups (**NFR ops**, LiteLLM `allow_remote`) stay **traceable** without duplicating existing NFR/eval specs.

**Approach:** Add a **`.gitlab-ci.yml`** `eval` job (same **`rag-mvp1-eval`** tag + **rules** as `hybrid_golden_eval`): `scripts/e2e_gateway_preflight.py` then `RUN_E2E_PRIVACY=1 pytest -m e2e_privacy`. Add **default CI** for script `--help` (implement **argparse** on `reindex.py` / `seed_kb.py` — they lack `--help` today) and golden line count. Document vars in **README**; touch **example YAML** / runbook / gap tables **only** in the same commit that closes a row.

## Boundaries & Constraints

**Always:** Self-hosted **tags** + `resource_group: rag_mvp1_eval` pattern; preflight/pytest **non-zero fails** the job; script smokes **no network**; gap table updates **same PR** as behavior.

**Ask First:** Optional `docker compose config` — **no** Compose in repo today; add only if/when a file exists.

**Never:** NFR-3, §2.8#2 / §2.8#7 out of scope. Do not re-document NFR-1/2 **wiring** (see `deferred-work` + `spec-mvp1-ci-eval-nfr-perf-gating`). No Ollama from default pytest.

## I/O & Edge Case Matrix

| Scenario | Input / state | Expected | On failure |
|----------|---------------|----------|------------|
| Scheduled E2E | Stack + env per runbook | Preflight **0**, then `e2e_privacy` **0** | Job **red** |
| MR pipeline | `merge_request_event` | Job **not** run (match eval template) | N/A |
| Script/golden CI | `reindex --help`, `seed_kb --help`, golden **≥30** lines | Exit **0**; count OK | Fix scripts or data |

</frozen-after-approval>

## Code Map

- `.gitlab-ci.yml` — new job beside `hybrid_golden_eval` / `nfr_retrieve_smoke` (`&eval_mvp1_template`).
- `scripts/e2e_gateway_preflight.py`, `tests/e2e/test_allow_remote_privacy.py`, `tests/e2e/conftest.py` — preflight + `e2e_privacy`. `tests/e2e/scripts/*.ps1` — local reference; Linux job uses **python** CLI.
- `docs/runbook-allow-remote-false-e2e.md`, `docs/litellm-ollama-e2e.example.yaml` — ports + Ollama-only; add **`allow_remote`** if schema supports.
- `scripts/reindex.py`, `scripts/seed_kb.py`, `eval/golden/questions.jsonl` — smoke + line gate (repo has **32** lines).

## Tasks & Acceptance

**Execution:**

- [x] `.gitlab-ci.yml` — Job: preflight then `RUN_E2E_PRIVACY=1 python -m pytest -m e2e_privacy` (install deps in `before_script`); **fail** on non-zero; README documents tokens/URLs.
- [x] `scripts/reindex.py`, `scripts/seed_kb.py` — **`--help`** (argparse) with **exit 0** before any HTTP.
- [x] **CI (test stage or small job)** — run both `--help` steps; assert `eval/golden/questions.jsonl` line count **≥ 30**.
- [x] `README.md` — §2.8#5: tag `rag-mvp1-eval`, schedule/vars, runbook link.
- [x] `docs/litellm-ollama-e2e.example.yaml` + runbook + `deferred-work.md` — `allow_remote` (or equivalent) if supported; **single** cross-link, no NFR doc duplication.
- [x] `mvp1-prd-*.md` gap tables when §2.8#5 → **Done** (same commit).

**Acceptance criteria:**

- **Given** tagged self-hosted runner + stack, **when** schedule/web/API job runs, **then** preflight and `e2e_privacy` are **green** or job **fails**.
- **Given** MR pipeline, **when** it runs, **then** this E2E job is **excluded** (like other eval MVP1 jobs).
- **Given** default CI, **when** script + golden steps run, **then** both `--help` **0** and golden **≥ 30** lines.
- **Given** maintainer reads README + example YAML, **then** vars and `deferred-work` **cross-refs** match (no duplicate NFR merge-gate narrative).

## Spec Change Log

- **2026-04-25** — Plan step: template fill; repo facts: no Compose; golden 32 lines; scripts need `--help`.
- **2026-04-25** — **Implementation:** `mvp1_script_help_golden` + `e2e_privacy_allow_remote`, `argparse` on scripts, `test_mvp1_deliverable_cli.py`, docs + gap tables (step-03/04/05: review triage: no `bad_spec` loopback; duplicate preflight in CI+fixture is acceptable).

## Verification

**Commands:** `python scripts/e2e_gateway_preflight.py` · `RUN_E2E_PRIVACY=1 python -m pytest tests/e2e -m e2e_privacy -q` · `python scripts/reindex.py --help` · `python scripts/seed_kb.py --help` · line count on `eval/golden/questions.jsonl` **≥ 30**.

**Manual:** First runner: Ollama models per runbook; RAG URL reachable from runner (align naming with `RAG_EVAL_BASE_URL` / README).

## Suggested Review Order

**CI (MR gate + self-hosted E2E)**

- Offline MR check bundles §2.11 pytest so shared runners need no RAG.
  [`test_mvp1_deliverable_cli.py:1`](../../tests/unit/test_mvp1_deliverable_cli.py#L1)

- `test` then `eval` stages: new jobs sit beside existing `rag-mvp1-eval` eval jobs.
  [`.gitlab-ci.yml:10`](../../.gitlab-ci.yml#L10)

- §2.8(5) job mirrors eval rules, installs dev stack, preflight, then `e2e_privacy`.
  [`.gitlab-ci.yml:75`](../../.gitlab-ci.yml#L75)

**Script CLI (§2.11 deliverables)**

- `reindex` uses argparse positional `export_path`; `--help` never opens HTTP.
  [`reindex.py:18`](../../scripts/reindex.py#L18)

**Docs & traceability**

- README job table is the index for when each pipeline class runs.
  [`README.md:91`](../../README.md#L91)

- Runbook links GitLab job name to CI variables and README anchor.
  [`runbook-allow-remote-false-e2e.md:178`](../../docs/runbook-allow-remote-false-e2e.md#L178)

- Gap table row §2.8#5 updated to “Covered (scheduled)”.
  [`mvp1-prd-to-automated-tests-gap-table.md:84`](mvp1-prd-to-automated-tests-gap-table.md#L84)
