# SBOM Implementation Guidelines

## Purpose

Define cross-cutting rules that apply to all SBOM implementation steps and all SBOM test
specifications in this repository.

## Scope and Precedence

- This file is normative for:
  - `../sbom_implementation_run_config.json`
  - `../sbom_implementation_run_config.schema.json`
  - `sbom_implementation_config.md`
  - `sbom_impl_step1.md` through `sbom_impl_step8.md`
  - `sbom_test_main.md`
  - `sbom_test_step1.md` through `sbom_test_step8.md`
  - `implementation_guardrails.md`
  - `code_review.md`
- Step files define step-specific behavior. This file defines shared rules.
- If a step file conflicts with this file on a cross-cutting rule, update this file first
  and then align step files. If the conflict concerns step-specific domain behavior
  (e.g., CycloneDX field names, SPDX relationship types), the step file is authoritative
  for that domain detail.

## Execution Configuration Contract

Implementation and test execution settings are controlled by:

- Effective values: `../sbom_implementation_run_config.json`
- Validation schema: `../sbom_implementation_run_config.schema.json`
- Parameter documentation: `sbom_implementation_config.md`

Precedence rules:

- Step-specific values in `step_overrides` take precedence over profile defaults.
- Profile defaults (`profiles`) take precedence over hardcoded assumptions in
  step or test files.
- If no explicit step is requested, select the first incomplete enabled step in the active profile.
- Active profiles are processed in rollout order (`bootstrap` -> `expansion` -> `full`).
- If a configured stop point exists, execution must stop at that sub-step boundary.
- Progress state and event logs must be persisted under `plan/progress/` as configured.

Change-control rule:

- Any change to configuration keys or semantics must update both
  `../sbom_implementation_run_config.json`, `../sbom_implementation_run_config.schema.json`, and `sbom_implementation_config.md` in the same change set.

## Language Strategy

| Area | Language | Responsibility |
|------|----------|----------------|
| Pipeline entrypoint and orchestration | Bash | Process orchestration, CLI handling, tool invocation, artifact lifecycle |
| SBOM data transformation | Python 3 (stdlib only) | JSON parsing/augmentation, kernel module modeling, scope classification |
| Test suite orchestration | Bash | Run order, aggregation, exit status summary |
| Individual test assertions | Python 3 (stdlib only) | Validation logic per step and per requirement |

Global rules:

- Bash owns orchestration and OS command execution boundaries.
- Python owns structured-data logic and format-specific transformations.
- Python runtime and test code remain stdlib-only on the target system.
- Adding another mandatory runtime language requires explicit plan update first.

## Development Host Prerequisites

Static analysis, linting, and test tooling listed in the quality gates are **mandatory
prerequisites** and must be installed on the development host before implementation begins.
It is not acceptable to skip guardrail checks or tests because of missing packages.

| Tool | Purpose | Install |
|------|---------|---------|
| `ruff` | Python linter and formatter | `pip install ruff` |
| `mypy` | Python static type checker | `pip install mypy` |
| `pytest` | Python test runner (used alongside stdlib test scripts) | `pip install pytest` |
| `shellcheck` | Bash static analysis | OS package manager |
| `shfmt` | Bash formatter | OS package manager or `go install` |
| `cosign` | SBOM signing (Step 8) | [sigstore/cosign releases](https://github.com/sigstore/cosign/releases) |

Runtime constraint: the **target Debian system** runs stdlib-only Python 3.11 and has no
pip. The deliverables (`generate_sbom.sh`, `augment_kmod.py`) must not import any
third-party Python package. The tools above run exclusively on the development host for
quality assurance.

### Tool Configuration

Project-level configuration for QA tools should be maintained in `pyproject.toml` at the
SBOM project root. At a minimum, configure:

- `ruff`: target Python version (`target-version = "py311"`), line length, selected rules.
- `mypy`: Python version (`python_version = "3.11"`), strict mode or selected checks.
- `shfmt`: formatting style via `.editorconfig` or command-line flags documented in
  `implementation_guardrails.md`.

When configuration files are present, all quality gate commands use them automatically.

### Test Runner Clarification

Test scripts (`tests/test_step*.py`) are standalone stdlib-only scripts designed to run
via `tests/run_all_tests.sh`. The `pytest` tool listed above is used for quality-gate
static analysis and for running any supplementary developer-side unit tests -- it is not
the primary test runner for the step test suite. Both execution paths must produce
consistent results.

## Canonical Repository Structure

The tree below is the canonical baseline structure for runtime and planning artifacts.

```text
sbom/
  sbom_implementation_run_config.json
  sbom_implementation_run_config.schema.json
  generate_sbom.sh
  augment_kmod.py
  plan/
    cve_management.md
    cve_sbom_requirements.md
    sbom_specification.md
    sbom_implementation_plan.md
    sbom_implementation_guidelines.md
    sbom_plan_review.md
    implementation_guardrails.md
    code_review.md
    guardrails/
      README.md
      python_guardrails.md
      bash_guardrails.md
      compliance_matrix_template.md
      python/
      bash/
      sources/
    progress/
      README.md
      events/
      steps/
    reviews/
    sbom_impl_step1.md ... sbom_impl_step8.md
    sbom_test_main.md
    sbom_test_step1.md ... sbom_test_step8.md
  tests/
    run_all_tests.sh
    test_step1.py ... test_step8.py
```

Folder and artifact rules:

- Runtime scripts are maintained at the SBOM project root (`sbom/`).
- Effective implementation run settings are maintained in `sbom_implementation_run_config.json`. 
- Configuration schema is maintained in `sbom_implementation_run_config.schema.json`.
- Planning files are maintained in `plan/`.
- Guardrail policy and detail modules are maintained under `plan/guardrails/`.
- `plan/implementation_guardrails.md` and `plan/code_review.md` are mandatory workflow controls.
- Progress logs/state are maintained under `plan/progress/`.
- Automated test scripts are maintained in `tests/`.
- Review execution results are stored under `plan/reviews/` (see `sbom_plan_review.md`).
- Generated SBOM/test artifacts are runtime outputs, not planning sources.
- Test executions should use a temp directory or explicit `--output-dir`.

## Stable Interface Contracts

| Interface | Owner | Contract |
|-----------|-------|----------|
| `generate_sbom.sh` CLI | Bash entrypoint | Stable user-facing command for format selection, output naming, scope selection, optional signing |
| `augment_kmod.py` CLI | Python helper | Stable machine-facing contract for SBOM augmentation and step-level standalone modes used by tests |
| `tests/run_all_tests.sh` CLI | Test orchestration layer | Stable test-suite command that invokes all `tests/test_step*.py` scripts and reports aggregate status |

Contract rules:

- Breaking CLI changes require synchronized updates to implementation and all affected test specs.
- Step-level standalone modes used by tests are part of the contract while test specs depend on them.

## Version Pinning and Artifact Verification

To keep builds reproducible and auditable:

- Do not use floating installer references such as `main` branches or `releases/latest`.
- Pin exact tool versions in implementation scripts for `syft`, `cosign`, and QA tools.
- Verify downloaded binaries or installer scripts using SHA-256 values recorded in planning
  or release notes before execution.
- Record effective tool versions in generated SBOM metadata and in run logs.

## Output Conventions

These rules apply to all runtime scripts (`generate_sbom.sh`, `augment_kmod.py`) and must
be followed consistently across all implementation steps.

- Diagnostic and progress messages go to **stderr** (`>&2`).
- Machine-readable output (SBOM JSON, system-context text) goes to a **named file** or
  **stdout** when piping is intended.
- Error messages must include the originating script or function name for context
  (e.g., `"generate_sbom.sh: error: syft not found"`).
- Exit codes:
  - `0` -- success
  - `1` -- general runtime failure
  - `2` -- usage/argument error
- Python helpers called by Bash must use the same exit code convention (`0` success,
  `1` runtime failure, `2` usage error) so the orchestrator can detect and report
  failures without translation.

## Maintainability Decomposition Policy

- Keep two stable public entry files: `generate_sbom.sh` and `augment_kmod.py`.
- Keep `generate_sbom.sh` as a thin orchestrator; avoid format-specific data logic there.
- As complexity grows, Python internals may be decomposed into helper modules while preserving
  the `augment_kmod.py` CLI contract.
- Any new mandatory runtime file must be added to planning docs before implementation.

## Testing Architecture Baseline

- `tests/run_all_tests.sh` owns test orchestration and aggregate result reporting.
- `tests/test_step*.py` own assertion logic and requirement-level validation.
- Coverage layering:
  - Steps 1-3: component-level and contract-level checks
  - Steps 4-6: integration-level artifact checks
  - Steps 7-8: end-to-end and operational behavior checks

### Test Isolation Rules

- **Idempotency**: every test script must produce the same result regardless of how many
  times it runs in sequence. Tests must not depend on side effects from a previous run.
- **Temp directory usage**: tests that produce output artifacts must write to a temporary
  directory (created per run) or to an explicit `--output-dir` / `--sbom-dir` argument.
  Tests must not write to the repository working tree.
- **Cleanup**: tests must remove their temporary directories and files on both success and
  failure paths (`trap` in Bash, `try/finally` or `atexit` in Python).
- **Fixture dependencies**: if a later step's tests require input artifacts (e.g., Step 4
  tests need a raw CycloneDX file from Step 1), the test script must either generate the
  required fixture itself or accept its path via a CLI argument. Tests must never assume
  that a previous step's test has already run.
- **No shared mutable state**: tests must not modify global configuration, environment
  variables, or files outside their temporary directory.

## Implementation Readiness Gate

Implementation work may start only when all conditions hold:

1. Language boundaries are accepted.
2. Repository structure is accepted.
3. Interface contracts are accepted.
4. Guardrail workflow controls are accepted (`implementation_guardrails.md`, `code_review.md`, `plan/guardrails/*`).
5. Development host prerequisites are installed (see table above).
6. Step and test specs explicitly reference this guideline baseline.
7. Effective runtime configuration (`sbom_implementation_run_config.json`) and its documentation
   (`sbom_implementation_config.md`) are present and aligned.

---

## Revision History
<!-- Latest entries first. Add new rows directly below the header row. -->
<!-- Same-day revisions: append .2, .3, ... to the date (e.g. 2026-02-14.2). -->

| Date | Change |
|------|--------|
| 2026-02-14.6 | Added default execution-order semantics to execution contract: first incomplete enabled step in active profile, with sequential profile rollout (`bootstrap` -> `expansion` -> `full`). |
| 2026-02-14.5 | Added execution configuration contract with precedence rules for `sbom_implementation_run_config.json`. Added `sbom_implementation_run_config.json` and `plan/progress/` to canonical tree and folder rules. Added readiness-gate requirement for configuration/documentation alignment. |
| 2026-02-14.4 | Added `plan/reviews/` to canonical tree. Clarified "project root" vs "repository root". Added tool configuration section and test runner clarification. Aligned Python exit code convention with Bash. |
| 2026-02-14.3 | Expanded canonical tree coverage, added explicit version-pinning and artifact-verification policy. |
| 2026-02-14.2 | Added development host prerequisites, output conventions, test isolation rules. Refined conflict resolution rule. Added guardrails/README.md to canonical tree. |
| 2026-02-14 | Initial version: language strategy, repository structure, interface contracts, maintainability decomposition, testing architecture, implementation readiness gate. |


