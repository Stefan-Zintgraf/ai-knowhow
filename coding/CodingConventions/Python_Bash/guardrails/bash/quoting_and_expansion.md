# Quoting and Expansion Safety

## Scope
Applies to `SH-MUST-03`, `SH-MUST-09`, and `SH-MUST-10`.

## Requirements
- Quote variable expansions by default: `"${var}"`.
- Use `"$@"` when forwarding argument vectors.
- Use `$(...)` for command substitution; avoid legacy backticks.
- Use `[[ ... ]]` for Bash conditionals.
- Use arithmetic context `(( ... ))` where appropriate for numeric tests.

## Anti-patterns

```bash
# WRONG: unquoted variable -- breaks on spaces and glob characters
output_dir=$1
rm -rf $output_dir/*.json

# RIGHT: quoted expansion
output_dir="$1"
rm -rf "${output_dir}"/*.json
```

```bash
# WRONG: backtick substitution -- hard to nest, easy to misread
version=`syft version`

# RIGHT: $(...) substitution
version="$(syft version)"
```

```bash
# WRONG: single-bracket test -- inconsistent quoting behavior
if [ $status = "ok" ]; then ...

# RIGHT: double-bracket test
if [[ "${status}" == "ok" ]]; then ...
```

## Review checklist
- No unquoted expansions in changed lines unless intentionally word-splitting.
- No backtick command substitutions.
- Conditionals use `[[ ... ]]` in Bash scripts.

## Typical evidence
- `path/to/script.sh:line` around expansions and conditional blocks.
- `shellcheck` output for quoting-related checks.

## Source basis
- `../sources/google_shell_style_guide.html`
- `../sources/shellcheck_wiki.html`

