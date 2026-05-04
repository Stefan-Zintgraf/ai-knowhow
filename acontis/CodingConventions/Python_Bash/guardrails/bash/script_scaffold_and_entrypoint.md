# Script Scaffold and Entrypoint

## Scope
Applies to `SH-MUST-01`, `SH-MUST-02`, `SH-MUST-06`, and `SH-MUST-07`.

## Requirements
- Use `#!/usr/bin/env bash` when Bash-specific features are used.
- Enable strict mode by default: `set -euo pipefail`.
- Any strict-mode exception must be local and documented.
- Organize logic into functions rather than long top-level script flow.
- Provide a `main` function and call it at script end (`main "$@"`).

## Anti-patterns

```bash
# WRONG: missing strict mode -- silent failures, undefined variables ignored
#!/usr/bin/env bash
echo "Starting..."
curl -sSfL "$url" | sh

# RIGHT: strict mode catches errors early
#!/usr/bin/env bash
set -euo pipefail
echo "Starting..." >&2
curl -sSfL "$url" | sh
```

```bash
# WRONG: all logic at top level -- hard to test, hard to read
#!/usr/bin/env bash
set -euo pipefail
format="${1:-both}"
# ... 200 lines of inline logic ...

# RIGHT: functions with a main entrypoint
#!/usr/bin/env bash
set -euo pipefail

parse_args() { ... }
install_syft() { ... }
run_scan() { ... }

main() {
    parse_args "$@"
    install_syft
    run_scan
}

main "$@"
```

## Review checklist
- Shebang and strict mode are present or explicitly justified.
- Top-level script is mostly declarations and `main` call.
- Primary behavior lives in named functions.

## Typical evidence
- `path/to/script.sh:line` for shebang, strict mode, and `main` call.

## Source basis
- `../sources/google_shell_style_guide.html`
- `../sources/defensive_bash_programming_repost.html`

