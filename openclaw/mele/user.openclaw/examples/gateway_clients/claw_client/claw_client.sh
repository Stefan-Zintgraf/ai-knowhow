#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

if [[ ! -f "$VENV/bin/activate" ]]; then
    echo "Error: virtual environment not found at $VENV" >&2
    echo "Run: $SCRIPT_DIR/venv_install.sh" >&2
    exit 1
fi

if [[ "${VIRTUAL_ENV:-}" != "$VENV" ]]; then
    # shellcheck source=/dev/null
    source "$VENV/bin/activate"
fi

exec python "$SCRIPT_DIR/claw_client.py" "$@"
