#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

python3 -m venv "$VENV"
"$VENV/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"

echo "Virtual environment created and dependencies installed."
echo "Activate with: source $VENV/bin/activate"
