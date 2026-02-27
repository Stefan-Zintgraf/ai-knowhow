# claw_client.py — minimal OpenClaw gateway client

A minimal Python client that connects to the OpenClaw gateway, sends a prompt,
and streams the agent's response to stdout.

## Setup

```bash
bash venv_install.sh
source venv_activate.sh
```

## Configuration

Copy or edit `.env` with your gateway credentials:

```
OPENCLAW_GATEWAY_TOKEN=<your token>
OPENCLAW_GATEWAY_HOST=localhost
OPENCLAW_GATEWAY_PORT=18789
```

The token must match `OPENCLAW_GATEWAY_TOKEN` in the gateway's `.env`.

## Usage

```bash
# prompt as argument
python claw_client.py "what is the capital of France?"

# pipe stdin
echo "summarise this" | python claw_client.py

# combine: prefix prompt + piped content
git diff HEAD~1 | python claw_client.py "review this diff"
journalctl -n 50 | python claw_client.py "any errors worth investigating?"
cat error.log    | python claw_client.py "what went wrong?"
```

Responses stream token-by-token to stdout. All errors go to stderr.
The client always uses the session key `cli`, so the agent retains context
across calls within the same session.
