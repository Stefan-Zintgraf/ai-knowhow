---
name: testnode-skill
description: |
  Controls the Testnode (Python example node).
  Activates when the message starts with "testnode" (case-insensitive), with or without slash.
---

## Activation

Trigger on prefixes `testnode` or `test node` (case-insensitive).
If the message starts with `/`, do not activate this skill. Slash commands are handled elsewhere.

- `testnode on|start` -> start node
- `testnode off|stop` -> stop node
- `testnode restart` -> restart node
- `testnode` -> ensure started
- `testnode <text>` -> invoke `testnode.echo` with `<text>`

## Runtime commands (use `exec`)

Use gateway-side `exec` with `["bash","-c","..."]`.

Node paths:
- `$OPENCLAW_STATE_DIR/examples/nodes/testnode/testnode.py`
- `$OPENCLAW_STATE_DIR/examples/nodes/testnode/.testnode.pid`
- `$OPENCLAW_STATE_DIR/examples/nodes/testnode/identity.json`

Start/ensure script:

```bash
NODE_DIR="$OPENCLAW_STATE_DIR/examples/nodes/testnode"
PID_FILE="$NODE_DIR/.testnode.pid"
if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "already-running"
else
  nohup "$NODE_DIR/.venv/bin/python" -u "$NODE_DIR/testnode.py" > "$NODE_DIR/testnode.log" 2>&1 &
  echo $! > "$PID_FILE"
  echo "started:$(cat "$PID_FILE")"
  sleep 3
fi
```

Restart script:

```bash
NODE_DIR="OPENCLAW_STATE_DIR/examples/nodes/testnode"
PID_FILE="$NODE_DIR/.testnode.pid"
if [[ -f "$PID_FILE" ]]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then kill "$PID"; fi
  rm -f "$PID_FILE"
fi
nohup "$NODE_DIR/.venv/bin/python" -u "$NODE_DIR/testnode.py" > "$NODE_DIR/testnode.log" 2>&1 &
echo $! > "$PID_FILE"
echo "restarted:$(cat "$PID_FILE")"
sleep 3
```

Stop script:

```bash
NODE_DIR="OPENCLAW_STATE_DIR/examples/nodes/testnode"
PID_FILE="$NODE_DIR/.testnode.pid"
if [[ ! -f "$PID_FILE" ]]; then
  echo "not-running"
else
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then kill "$PID"; fi
  rm -f "$PID_FILE"
  echo "stopped:$PID"
fi
```

## Echo invoke (mandatory)

For `testnode <text>`:
1. Ensure started with the script above.
2. Read `OPENCLAW_STATE_DIR/examples/nodes/testnode/identity.json` and extract `deviceId`.
3. Invoke nodes tool with explicit node id:
   - action: invoke
   - node: `<deviceId>`  (REQUIRED, never omit)
   - command: `testnode.echo`
   - params: `{"text":"<text>"}`
4. If invoke fails with timeout/not connected: restart once, wait 2 seconds, retry once.

Never call `nodes.invoke` without `node`.
