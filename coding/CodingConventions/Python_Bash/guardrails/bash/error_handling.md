# Error Handling

## Scope
Applies to `SH-MUST-08`.

## Requirements
- Handle command failures intentionally.
- For expected failures, branch explicitly (`if ! cmd; then ... fi`).
- Emit actionable failure messages to stderr.
- Return meaningful exit codes from functions and script entrypoint.
- Avoid masking errors with unconditional `|| true` unless documented.

## Anti-patterns

```bash
# WRONG: unconditional || true masks real failures
curl -sSfL "$url" | sh -s -- -b /usr/local/bin || true

# RIGHT: handle the failure explicitly
if ! curl -sSfL "$url" | sh -s -- -b /usr/local/bin; then
    echo "generate_sbom.sh: error: failed to install syft" >&2
    return 1
fi
```

```bash
# WRONG: no error message -- caller cannot diagnose the failure
syft dir:/ -o cyclonedx-json="$out"

# RIGHT: check status and emit actionable message
if ! syft dir:/ -o cyclonedx-json="$out" --quiet; then
    echo "generate_sbom.sh: error: syft scan failed" >&2
    return 1
fi
```

**Caution**: do **not** reference `$?` inside `if ! cmd; then ...` -- the `if`
statement resets `$?` to `0` when the negated condition is true. If the original
exit code is needed, capture it before the conditional:

```bash
local rc=0
syft dir:/ -o cyclonedx-json="$out" --quiet || rc=$?
if (( rc != 0 )); then
    echo "generate_sbom.sh: error: syft scan failed (exit ${rc})" >&2
    return 1
fi
```

## Review checklist
- Changed command calls have clear failure behavior.
- Error paths provide context for troubleshooting.
- Exit codes are propagated or transformed intentionally.

## Typical evidence
- `path/to/script.sh:line` for guarded command execution and error messages.
- Tests for negative paths when available.

## Source basis
- `../sources/defensive_bash_programming_repost.html`
- `../sources/shellcheck_wiki.html`

