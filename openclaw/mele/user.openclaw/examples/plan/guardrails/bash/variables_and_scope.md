# Variables and Scope

## Scope
Applies to `SH-MUST-04` and `SH-MUST-05`.

## Requirements
- Declare function-local variables with `local`.
- Keep globals minimal; only constants/config should be global.
- Prefer uppercase names for readonly globals.
- Mark constants readonly when possible (`readonly NAME=value`).

## Anti-patterns

```bash
# WRONG: function leaks variables into global scope
install_syft() {
    version="$(syft version 2>/dev/null || echo "")"
    url="https://example.invalid/syft/v1.18.1/install.sh"
    # version and url now pollute the global namespace
}

# RIGHT: local declarations
install_syft() {
    local version
    local url="https://example.invalid/syft/v1.18.1/install.sh"
    version="$(syft version 2>/dev/null || echo "")"
}
```

```bash
# WRONG: magic string repeated in multiple places
if [[ "${format}" == "cyclonedx-json" ]]; then ...
# ... elsewhere ...
syft dir:/ -o cyclonedx-json="$out"

# RIGHT: readonly constant declared once
readonly FMT_CDX="cyclonedx-json"
if [[ "${format}" == "${FMT_CDX}" ]]; then ...
syft dir:/ -o "${FMT_CDX}=${out}"
```

## Review checklist
- New function variables are declared `local`.
- New globals are justified and minimal.
- Constants are uppercase and readonly where practical.

## Typical evidence
- `path/to/script.sh:line` for `local` and readonly constant declarations.

## Source basis
- `plan/guardrails/sources/google_shell_style_guide.html`

