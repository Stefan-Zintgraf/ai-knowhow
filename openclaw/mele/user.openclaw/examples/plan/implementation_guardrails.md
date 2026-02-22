# Implementation Guardrails (Agent Instructions)

## Mandatory Applicability
These instructions are mandatory for any coding or testing activity in this repository.
Every implementation and test step must follow this file.

Primary references:
- `plan/sbom_implementation_guidelines.md` (cross-cutting rules, test isolation, output conventions)
- `sbom_implementation_run_config.json` (effective execution controls for profiles, limits, stop points, and progress tracking)
- `sbom_implementation_run_config.schema.json` (strict validation schema for run configuration)
- `plan/sbom_implementation_config.md` (configuration parameter contract)
- `plan/implementation_guardrails.md` (this file)
- `plan/code_review.md` (mandatory pre-test review gate)
- `plan/guardrails/python_guardrails.md` (Python rule IDs and module mapping)
- `plan/guardrails/bash_guardrails.md` (Bash rule IDs and module mapping)
- `plan/guardrails/compliance_matrix_template.md` (mandatory evidence format)

If a change touches both Python and Bash, both language guardrails apply.

## Execution Contract for Agents
For each implementation step:
1. Read `plan/sbom_implementation_guidelines.md`, `sbom_implementation_run_config.json`, `sbom_implementation_run_config.schema.json`, the relevant step file in `plan/`, and this guardrail file.
2. Identify changed language(s) and load the applicable rule set(s):
   - Python: all `PY-MUST-*` rules in `plan/guardrails/python_guardrails.md`
   - Bash: all `SH-MUST-*` rules in `plan/guardrails/bash_guardrails.md`
3. Load mapped detail modules from the language guardrail files under `plan/guardrails/python/` and/or `plan/guardrails/bash/`.
4. Resolve the effective step configuration from `sbom_implementation_run_config.json` (`resolved_profile` from `step_overrides.<N>.profile` or active `workflow.profile_rollout` phase, plus optional `component_limits` and `stop_after_substep`).
5. If no explicit step is requested by the user, select the first incomplete enabled step in the active profile.
6. If an explicit step is requested by the user, execute only that step (`workflow.explicit_step_request_behavior`).
7. Implement only the scoped requirements of the current step and honor configured sampling limits.
8. At every sub-step boundary, update progress state under `plan/progress/steps/` and append configured events under `plan/progress/events/`.
9. If a configured stop point is reached, stop execution and mark progress accordingly.
10. Run required static checks for changed files.
11. Execute the code review workflow in `plan/code_review.md`.
12. Fix all blocking review findings.
13. Only then run the step test(s).
14. Record a completed guardrail compliance matrix with evidence.

For each test run:
1. Execute `plan/code_review.md` first.
2. Do not run tests if blocking findings remain.
3. Run test script(s) defined in the step/test specification.

## Non-Negotiable Rules
- MUST satisfy all `MUST` rules in the language guardrails.
- MUST read mapped detail modules for all applicable `MUST` IDs.
- MUST not skip code review before testing.
- MUST not suppress lint/type/static issues without a short justification.
- MUST preserve existing behavior unless the current step requires a change.
- MUST keep changes scoped, traceable, and testable.
- MUST validate `sbom_implementation_run_config.json` against `sbom_implementation_run_config.schema.json` before execution.
- MUST honor active profile limits and step overrides from `sbom_implementation_run_config.json`.
- MUST honor configured stop points and persist progress state to `plan/progress/`.
- MUST follow the test isolation rules in `sbom_implementation_guidelines.md` for all test code.
- MUST provide evidence (`file:line` or command result) for each applicable `MUST` ID.

## Required Checks Baseline

All tools below are **mandatory prerequisites** (see "Development Host Prerequisites" in
`sbom_implementation_guidelines.md`). They must be installed before implementation begins.
It is not acceptable to skip checks because of missing packages.

Run the checks relevant to modified files. The commands listed here are the canonical
baseline -- language-specific guardrail files and `code_review.md` repeat them for
self-containment. If a command needs to change, update it here first and then align the
other files.

Python baseline:
```bash
ruff check .
ruff format --check .
mypy .
pytest -q
```

Bash baseline:
```bash
shfmt -d .
find . -type f -name '*.sh' -print0 | xargs -0 shellcheck
```

Note: the `find | xargs` command above omits the GNU-specific `-r` flag for portability
across development hosts. On GNU systems, `xargs` without `-r` still works correctly
when `find` returns results; it may invoke `shellcheck` with no arguments if no `.sh`
files exist, which shellcheck handles gracefully.

Use repository-specific equivalents (e.g., via `pyproject.toml` or `.editorconfig`)
when configured. If a repository-specific equivalent differs from the baseline commands,
document it in the completion report.

## Guardrail Compliance Matrix
Use `plan/guardrails/compliance_matrix_template.md`.

Rules:
- Each applicable rule ID must have `PASS`, `N/A`, or `FAIL`.
- `N/A` requires a brief rationale.
- `FAIL` is blocking until fixed or explicitly accepted in writing.

## Completion Report Template
Every implementation completion report must include:
1. Guardrails referenced
2. Files changed
3. Checks run and results
4. Code review status (from `plan/code_review.md`)
5. Guardrail compliance matrix (or link to it)
6. Test execution status
7. Remaining risks/deviations

---

## Revision History
<!-- Latest entries first. Add new rows directly below the header row. -->
<!-- Same-day revisions: append .2, .3, ... to the date (e.g. 2026-02-14.2). -->

| Date | Change |
|------|--------|
| 2026-02-14.4 | Added default step-selection rule: if no explicit step is requested, select first incomplete enabled step in active profile. Shifted execution contract numbering accordingly. |
| 2026-02-14.3 | Added mandatory use of `sbom_implementation_run_config.json` and `sbom_implementation_config.md`. Extended execution contract for profile resolution, stop-point handling, and progress/event persistence under `plan/progress/`. Added non-negotiable configuration-compliance rules. |
| 2026-02-14.2 | Added `sbom_implementation_guidelines.md` to primary references and execution contract step 1. Replaced hardcoded rule ID ranges with authoritative source references. Added test isolation rule to non-negotiable rules. Designated this file as canonical source for quality gate commands. Removed GNU-specific `xargs -r` for portability. |
| 2026-02-14 | Initial version. |


