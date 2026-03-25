# claw_client.py — OpenClaw gateway client & library

A Python client that connects to the OpenClaw gateway, sends a prompt, and
returns (or streams) the agent's response. Works as a **CLI tool** and as an
**importable library** for test scripts and AI agents.

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

## CLI Usage

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
Use `--session KEY` to isolate conversation context between runs.

## Library Usage

Import the module in your own Python scripts to send prompts and inspect
responses programmatically — ideal for automated testing and AI-agent-driven
validation.

### Quick start (synchronous)

```python
from claw_client import prompt_sync

response = prompt_sync("/bmad help", session_key="test-bmad")
print(response.text)
print(f"Run ID: {response.run_id}, took {response.elapsed_seconds:.1f}s")
```

### Async

```python
from claw_client import prompt_async

response = await prompt_async("/bmad brainstorm AI robotics", session_key="test-bmad")
assert "brainstorm" in response.text.lower()
```

### Custom config (override env vars)

```python
from claw_client import prompt_sync, GatewayConfig

config = GatewayConfig(host="192.168.1.50", port=18789, token="my-token")
response = prompt_sync("hello", config=config)
```

### Streaming + collecting

```python
from claw_client import prompt_sync

response = prompt_sync(
    "explain quantum computing",
    on_token=lambda t: print(t, end="", flush=True),
)
print()  # trailing newline
# response.text still contains the full accumulated text
```

### Timeout & event capture (for debugging)

```python
from claw_client import prompt_sync

response = prompt_sync(
    "/bmad validate my idea",
    session_key="test-bmad",
    timeout=120,
    capture_events=True,
)
# response.events contains every raw gateway event dict
```

## API Reference

| Symbol | Description |
|---|---|
| `prompt_sync(message, ...)` | Send a prompt, block until done, return `ClawResponse` |
| `prompt_async(message, ...)` | Async version of `prompt_sync` |
| `ClawResponse` | Dataclass: `.text`, `.run_id`, `.elapsed_seconds`, `.events` |
| `GatewayConfig` | Dataclass: `.host`, `.port`, `.token`, `.identity_file`, `.url`, `.from_env()` |
| `GatewayClient` | Low-level async WebSocket wrapper (for advanced use) |
| `DEFAULT_SESSION_KEY` | `"claw_client"` — the default session key |
