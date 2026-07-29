# Bash Quality Gates

## Scope
Applies to `SH-MUST-11`.

## Required commands
```bash
shfmt -d .
find . -type f -name '*.sh' -print0 | xargs -0 shellcheck
```

The `find` pipeline avoids shell globstar portability issues. The canonical command
list is maintained in `../../implementation_guardrails.md` "Required Checks Baseline".

## Requirements
- Run applicable formatting and static checks for changed shell scripts.
- Any failing required check blocks test readiness.
- If tooling is unavailable, record it explicitly as an open risk.

## Review checklist
- Command list is recorded.
- Exit status/outcome is recorded for each command.
- Failures are fixed or explicitly accepted in writing.

## Typical evidence
- Command transcript summary with pass/fail outcome.

## Source basis
- `../sources/google_shell_style_guide.html`
- `../sources/shellcheck_wiki.html`


