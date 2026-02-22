#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.testnode.pid"

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Testnode is already running (PID: $(cat "$PID_FILE"))"
    exit 1
fi

nohup "$SCRIPT_DIR/.venv/bin/python" -u "$SCRIPT_DIR/testnode.py" > "$SCRIPT_DIR/testnode.log" 2>&1 &
echo $! > "$PID_FILE"

echo "Testnode started (PID: $(cat "$PID_FILE")). Log: $SCRIPT_DIR/testnode.log"
echo "Run ./stop.sh to stop it."
