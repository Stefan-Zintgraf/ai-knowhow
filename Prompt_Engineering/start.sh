#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Activate the virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

PID_FILE="$SCRIPT_DIR/.jupyter.pid"

# 2. Check if JupyterLab is already running
if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "JupyterLab is already running (PID: $(cat "$PID_FILE"))"
    exit 1
fi

# 3. Start JupyterLab server in the background and save PID
jupyter lab --no-browser &
echo $! > "$PID_FILE"

# 4. Wait for the server to be ready, then open the browser
sleep 3
xdg-open http://localhost:8888
echo Password is "dev"

echo "JupyterLab started (PID: $(cat "$PID_FILE")). Run ./stop.sh to stop it."
