# Bash Guardrails

## Priority model
- MUST: required for merge/completion
- SHOULD: expected unless clear reason

## Enforcement model
- Every `MUST` rule has a stable ID (`SH-MUST-*`) and a mapped detail module.
- For Bash changes, review the mapped detail files under `bash/` before coding and during code review.
- A `MUST` rule can be marked `N/A` only with a short rationale in the compliance matrix.

## MUST rules and detail modules
| Rule ID | Requirement | Detail module |
| --- | --- | --- |
| `SH-MUST-01` | Use bash explicitly (`#!/usr/bin/env bash`) when Bash features are required. | `bash/script_scaffold_and_entrypoint.md` |
| `SH-MUST-02` | Start scripts with strict mode unless there is a documented exception (`set -euo pipefail`). | `bash/script_scaffold_and_entrypoint.md` |
| `SH-MUST-03` | Quote variable expansions by default (`"${var}"`). | `bash/quoting_and_expansion.md` |
| `SH-MUST-04` | Use `local` for function-scoped variables. | `bash/variables_and_scope.md` |
| `SH-MUST-05` | Keep global variables minimal and uppercase readonly constants where possible. | `bash/variables_and_scope.md` |
| `SH-MUST-06` | Prefer functions over long top-level procedural blocks. | `bash/script_scaffold_and_entrypoint.md` |
| `SH-MUST-07` | Provide `main` entrypoint and call it at end. | `bash/script_scaffold_and_entrypoint.md` |
| `SH-MUST-08` | Check command exit statuses and handle errors intentionally. | `bash/error_handling.md` |
| `SH-MUST-09` | Prefer `$(...)` over backticks. | `bash/quoting_and_expansion.md` |
| `SH-MUST-10` | Use `[[ ... ]]` for tests in Bash scripts. | `bash/quoting_and_expansion.md` |
| `SH-MUST-11` | Code must pass `shellcheck` and `shfmt`. | `bash/quality_gates.md` |

## SHOULD rules
- Keep one logical action per line where practical.
- Send error messages to stderr.
- Keep script headers and function comments concise but useful.
- Avoid `eval` unless no safer alternative exists.
- Prefer builtins and simple tools over complex process chains.

## Lint and quality gates
Use (or wire) these commands (canonical source: `../implementation_guardrails.md`):

```bash
shfmt -d .
find . -type f -name '*.sh' -print0 | xargs -0 shellcheck
```

The `find` pipeline avoids shell globstar portability issues.

## Agent completion checklist
1. Fill the guardrail compliance matrix from `compliance_matrix_template.md`.
2. Confirm every `SH-MUST-*` rule is `PASS` or justified `N/A`.
3. List commands run and outcomes.
4. List deliberate deviations and rationale.

## Source basis
- Google Shell Style Guide
- ShellCheck Wiki
- Defensive Bash Programming


