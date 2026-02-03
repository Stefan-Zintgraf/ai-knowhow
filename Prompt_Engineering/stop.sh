#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.jupyter.pid"

if [[ ! -f "$PID_FILE" ]]; then
    echo "JupyterLab is not running (no PID file found)."
    exit 1
fi

PID=$(cat "$PID_FILE")

if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "JupyterLab stopped (PID: $PID)."
else
    echo "JupyterLab is not running (stale PID: $PID)."
fi

rm -f "$PID_FILE"
