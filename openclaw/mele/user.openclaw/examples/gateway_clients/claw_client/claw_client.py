#!/usr/bin/env python3
"""
OpenClaw gateway client — CLI tool and importable library.

Sends a prompt to the OpenClaw gateway and returns (or streams) the agent's
response.  Works both as a standalone command-line tool and as a Python library
that test scripts or AI agents can import.

CLI usage (unchanged):
    python claw_client.py "your prompt here"
    python claw_client.py --session myproject "what did we discuss?"
    echo "some text" | python claw_client.py
    echo "some text" | python claw_client.py "optional prefix prompt"
    cat file.txt    | python claw_client.py "summarise this"
    git diff HEAD~1 | python claw_client.py --session codereview "review this diff"
    cat file.txt    | python claw_client.py - --session notes

Library usage (synchronous):
    from claw_client import prompt_sync, ClawResponse

    response = prompt_sync("/bmad help", session_key="test")
    print(response.text)
    assert "brainstorm" in response.text.lower()

Library usage (async):
    from claw_client import prompt_async, GatewayConfig

    config = GatewayConfig(token="secret")
    response = await prompt_async("/bmad help", config=config)

Library usage with streaming:
    from claw_client import prompt_sync

    response = prompt_sync("hello", on_token=lambda t: print(t, end="", flush=True))

Stdin is read only when no CLI argument is given (or when the sole argument
is "-"). This avoids hanging when the script is run from a non-interactive
terminal where isatty() returns False even though nothing is piped in.

Configuration (via .env next to this script or the environment):
    OPENCLAW_GATEWAY_TOKEN  — required; must match the gateway's token
    OPENCLAW_GATEWAY_HOST   — default: localhost
    OPENCLAW_GATEWAY_PORT   — default: 18789

Identity:
    On first run an Ed25519 key pair is generated and saved to identity.json
    next to this script (mode 0600). The public key is used to prove identity
    to the gateway during the connect handshake, which is required to obtain
    operator.admin scope. On subsequent runs the same key pair is reused so
    the gateway recognises this client.

Protocol sequence diagram:

    CLIENT                              GATEWAY                        AGENT
      |                                    |                              |
      |──── TCP/WebSocket open ───────────>|                              |
      |                                    |                              |
      |   ── INIT ─────────────────────────────────────────────────────  |
      |<─── event: connect.challenge ──────|                              |
      |     { nonce }                      |                              |
      |                                    |                              |
      |──── req: connect ─────────────────>|                              |
      |     { clientId, role,              |                              |
      |       scopes: [operator.admin],    |                              |
      |       auth: { token },             |                              |
      |       device: { publicKey,         |                              |
      |                 signature(nonce),  |                              |
      |                 signedAt } }       |                              |
      |<─── res: ok ───────────────────────|                              |
      |     (operator.admin granted)       |                              |
      |                                    |                              |
      |   ── SEND PROMPT ───────────────────────────────────────────────  |
      |──── req: chat.send ───────────────>|                              |
      |     { sessionKey, message,         |                              |
      |       idempotencyKey }             |──── invoke agent ───────────>|
      |<─── res: ok ───────────────────────|                              |
      |                                    |                              |
      |   ── STREAM RESPONSE ───────────────────────────────────────────  |
      |<─── event: agent ──────────────────|<── token delta ──────────────|
      |     { stream: "lifecycle",         |                              |
      |       data: { phase: "start" } }   |                              |
      |<─── event: agent ──────────────────|<── token delta ──────────────|
      |     { stream: "assistant",         |                              |
      |       data: { delta: "Hello" } }   |  (repeats per token)         |
      |         ...                        |                              |
      |<─── event: agent ──────────────────|<── run complete ─────────────|
      |     { stream: "lifecycle",         |                              |
      |       data: { phase: "end" } }     |                              |
      |                                    |                              |
      |   ── DEINIT ────────────────────────────────────────────────────  |
      |──── WebSocket close ──────────────>|                              |
      |                                    |                              |

    Notes:
      • The gateway pushes events to all connected operator.admin clients
        automatically — no chat.subscribe call is needed on this connection.
      • The signature binds to the nonce so it cannot be replayed on a
        different session.
      • chat.send returns ok immediately; the agent run starts asynchronously.

See also:
    https://docs.openclaw.ai/gateway/protocol
    https://docs.openclaw.ai/concepts/architecture
"""

import argparse
import asyncio
import base64
import hashlib
import json
import os
import sys
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import websockets
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
    load_pem_public_key,
)
from dotenv import load_dotenv

_HERE = Path(__file__).parent
load_dotenv(_HERE / ".env")

GATEWAY_HOST = os.getenv("OPENCLAW_GATEWAY_HOST", "localhost")
GATEWAY_PORT = os.getenv("OPENCLAW_GATEWAY_PORT", "18789")
GATEWAY_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN", "")
GATEWAY_URL = f"ws://{GATEWAY_HOST}:{GATEWAY_PORT}"

# CLIENT_ID must be the literal string "gateway-client" — the gateway validates
# this against a fixed allowlist and rejects any other value.
CLIENT_ID = "gateway-client"
CLIENT_MODE = "ui"
ROLE = "operator"
SCOPES = ["operator.admin"]

# Default session key used when --session is not provided. The gateway stores
# message history per session key persistently, so the agent remembers context
# across multiple invocations that use the same key.
DEFAULT_SESSION_KEY = "claw_client"

IDENTITY_FILE = _HERE / "identity.json"

__all__ = [
    "ClawResponse",
    "GatewayConfig",
    "GatewayClient",
    "prompt_async",
    "prompt_sync",
    "DEFAULT_SESSION_KEY",
]


# ── public data types ─────────────────────────────────────────────────────────

@dataclass
class GatewayConfig:
    """
    Connection parameters for the OpenClaw gateway.

    Construct manually to override defaults, or use ``GatewayConfig.from_env()``
    to load from environment variables / .env file (the same vars the CLI reads).
    """
    host: str = "localhost"
    port: int = 18789
    token: str = ""
    identity_file: Path | None = None

    @property
    def url(self) -> str:
        return f"ws://{self.host}:{self.port}"

    @classmethod
    def from_env(cls) -> "GatewayConfig":
        """Create a config from environment variables (reads .env automatically on import)."""
        return cls(
            host=os.getenv("OPENCLAW_GATEWAY_HOST", "localhost"),
            port=int(os.getenv("OPENCLAW_GATEWAY_PORT", "18789")),
            token=os.getenv("OPENCLAW_GATEWAY_TOKEN", ""),
        )


@dataclass
class ClawResponse:
    """
    Structured response from an agent prompt.

    Attributes:
        text:            Full response text (all token deltas concatenated).
        run_id:          Gateway-assigned run identifier (useful for log correlation).
        elapsed_seconds: Wall-clock time from connection open to lifecycle:end.
        events:          Raw event payloads received during the run (for debugging /
                         advanced assertions). Only populated when ``capture_events``
                         is True in prompt_async().
    """
    text: str = ""
    run_id: str | None = None
    elapsed_seconds: float = 0.0
    events: list[dict] = field(default_factory=list)


# ── identity / signing ────────────────────────────────────────────────────────
# The gateway requires a device identity (Ed25519 key pair) to grant
# operator.admin scope. The public key is sent with the connect request;
# the private key signs a challenge-response payload so the gateway can
# verify that this client actually holds the private key.

def _b64url(data: bytes) -> str:
    """URL-safe base64 encoding without padding (as used throughout the gateway protocol)."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _generate_identity() -> dict:
    """
    Generate a new Ed25519 key pair and derive a stable device ID from the
    public key (SHA-256 of the raw 32-byte public key, hex-encoded).

    The returned dict matches the identity.json schema used by other OpenClaw
    clients (e.g. the testnode example).
    """
    key = Ed25519PrivateKey.generate()
    priv_pem = key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode()
    pub_pem = key.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode()
    raw_pub = key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    device_id = hashlib.sha256(raw_pub).hexdigest()
    return {
        "version": 1,
        "deviceId": device_id,
        "publicKeyPem": pub_pem,
        "privateKeyPem": priv_pem,
        "createdAtMs": int(time.time() * 1000),
    }


def _load_or_create_identity(identity_file: Path | None = None) -> dict:
    """
    Load the identity from disk if it exists and is valid, otherwise generate a
    new one and persist it. File permissions are set to 0600 to protect the
    private key.
    """
    path = identity_file or IDENTITY_FILE
    if path.exists():
        data = json.loads(path.read_text())
        if data.get("version") == 1 and data.get("deviceId") and data.get("privateKeyPem"):
            return data
    identity = _generate_identity()
    path.write_text(json.dumps(identity, indent=2))
    path.chmod(0o600)
    return identity


def _sign(private_pem: str, payload: str) -> str:
    """Ed25519-sign a UTF-8 string and return the signature as URL-safe base64."""
    key = load_pem_private_key(private_pem.encode(), password=None)
    return _b64url(key.sign(payload.encode()))


def _pub_b64url(public_pem: str) -> str:
    """Extract the raw 32-byte Ed25519 public key and encode it as URL-safe base64."""
    pub = load_pem_public_key(public_pem.encode())
    return _b64url(pub.public_bytes(Encoding.Raw, PublicFormat.Raw))


def _build_device_payload(
    device_id: str,
    client_id: str,
    client_mode: str,
    role: str,
    scopes: list[str],
    signed_at_ms: int,
    token: str,
    nonce: str | None,
) -> str:
    """
    Build the pipe-delimited string that is Ed25519-signed to prove device identity.

    Format v1 (no nonce, legacy):
        v1|<deviceId>|<clientId>|<mode>|<role>|<scopes,>|<signedAt>|<token>

    Format v2 (with nonce, current):
        v2|<deviceId>|<clientId>|<mode>|<role>|<scopes,>|<signedAt>|<token>|<nonce>

    The gateway verifies this signature using the public key sent in the same
    connect request, binding the signature to the specific challenge nonce so
    it cannot be replayed.
    """
    version = "v2" if nonce else "v1"
    parts = [version, device_id, client_id, client_mode, role, ",".join(scopes), str(signed_at_ms), token]
    if version == "v2":
        parts.append(nonce)
    return "|".join(parts)


# ── gateway client ────────────────────────────────────────────────────────────

class GatewayClient:
    """
    Thin async wrapper around an OpenClaw gateway WebSocket connection.

    Why a background reader task?
    ─────────────────────────────
    The gateway multiplexes two kinds of frames on the same WebSocket:

      • res  — responses to RPC requests, matched by id
      • event — unsolicited push events (challenges, agent tokens, health, tick…)

    A naive "send then await recv()" loop breaks immediately because the gateway
    sends a "connect.challenge" event *before* responding to the connect request.
    Consuming that event as the connect response causes the code to deadlock
    waiting for the next frame.

    The background _reader() task solves this by continuously reading every
    incoming frame and routing it to the right destination:
      • res frames  → futures stored in self._pending, keyed by request id
      • event frames → self._events queue, consumed by next_event()

    This means callers can await an RPC response and iterate over events
    independently, without either blocking the other.
    """

    def __init__(self, ws, identity: dict, *, token: str = ""):
        self._ws = ws
        self._identity = identity
        self._token = token
        # Maps request id → Future that resolves when the matching res arrives.
        self._pending: dict[str, asyncio.Future] = {}
        # All event frames land here in arrival order.
        self._events: asyncio.Queue = asyncio.Queue()
        self._reader_task: asyncio.Task | None = None

    async def start(self) -> None:
        """Start the background frame-routing task. Must be called before connect()."""
        self._reader_task = asyncio.create_task(self._reader())

    async def stop(self) -> None:
        """Cancel the background reader task. Safe to call even if already stopped."""
        if self._reader_task:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except asyncio.CancelledError:
                pass

    async def _reader(self) -> None:
        """Background task: read every frame and route it to the right consumer."""
        async for raw in self._ws:
            msg = json.loads(raw)
            if msg.get("type") == "res":
                fut = self._pending.pop(msg.get("id", ""), None)
                if fut and not fut.done():
                    fut.set_result(msg)
            elif msg.get("type") == "event":
                await self._events.put(msg)

    async def _rpc(self, method: str, params: dict) -> dict:
        """
        Send an RPC request and wait for the matching response.

        Registers a Future in self._pending before sending so the background
        reader can resolve it as soon as the res frame arrives, even if other
        frames (events) arrive in between.
        """
        req_id = str(uuid.uuid4())
        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        self._pending[req_id] = fut
        await self._ws.send(json.dumps({"type": "req", "id": req_id, "method": method, "params": params}))
        return await fut

    async def next_event(self) -> dict:
        """Return the next event frame from the queue (blocks until one arrives)."""
        return await self._events.get()

    async def connect(self) -> None:
        """
        Perform the gateway authentication handshake.

        Sequence:
          1. Wait for the "connect.challenge" event (gateway sends it immediately
             on connection, before any request is made).
          2. Build a v2 device-auth payload string and Ed25519-sign it using
             the challenge nonce, binding the signature to this specific session.
          3. Send the "connect" RPC with the signed device proof.
          4. Raise RuntimeError if the gateway rejects the request.

        After this method returns, operator.admin scope is active and chat
        methods can be called.
        """
        nonce = None
        while True:
            msg = await asyncio.wait_for(self._events.get(), timeout=10)
            if msg.get("event") == "connect.challenge":
                nonce = msg.get("payload", {}).get("nonce")
                break

        identity = self._identity
        device_id = identity["deviceId"]
        signed_at_ms = int(time.time() * 1000)
        token = self._token

        auth_payload = _build_device_payload(
            device_id=device_id,
            client_id=CLIENT_ID,
            client_mode=CLIENT_MODE,
            role=ROLE,
            scopes=SCOPES,
            signed_at_ms=signed_at_ms,
            token=token,
            nonce=nonce,
        )
        signature = _sign(identity["privateKeyPem"], auth_payload)

        resp = await self._rpc("connect", {
            "minProtocol": 3,
            "maxProtocol": 3,
            "client": {
                "id": CLIENT_ID,
                "displayName": "claw-client-py",
                "version": "1.0",
                "platform": sys.platform,
                "mode": CLIENT_MODE,
                "instanceId": device_id,
            },
            "role": ROLE,
            "scopes": SCOPES,
            "auth": {"token": token} if token else None,
            "device": {
                "id": device_id,
                "publicKey": _pub_b64url(identity["publicKeyPem"]),
                "signature": signature,
                "signedAt": signed_at_ms,
                "nonce": nonce,
            },
        })
        if not resp.get("ok"):
            raise RuntimeError(f"connect failed: {resp.get('error')}")

    async def send(self, session_key: str, message: str) -> None:
        """
        Send a user message to the agent in the given session.

        The idempotencyKey makes this call safe to retry — if the network drops
        after the gateway processes the request but before we receive the ack,
        resending with the same key is a no-op rather than a duplicate message.
        """
        resp = await self._rpc("chat.send", {
            "sessionKey": session_key,
            "message": message,
            "idempotencyKey": str(uuid.uuid4()),
            "deliver": True,
        })
        if not resp.get("ok"):
            raise RuntimeError(f"chat.send failed: {resp.get('error')}")


# ── public API ────────────────────────────────────────────────────────────────

async def prompt_async(
    message: str,
    *,
    session_key: str = DEFAULT_SESSION_KEY,
    config: GatewayConfig | None = None,
    on_token: Callable[[str], None] | None = None,
    timeout: float | None = None,
    capture_events: bool = False,
) -> ClawResponse:
    """
    Send a message to the agent and return the complete response.

    This is the primary library entry point.  It opens a WebSocket connection,
    authenticates, sends the message, collects every token delta until the agent
    run completes, and returns a ``ClawResponse`` with the full text.

    Args:
        message:        The prompt to send to the agent.
        session_key:    Gateway session key — the agent retains conversation
                        context across calls that share the same key.
        config:         Gateway connection parameters.  If *None*, loads from
                        environment variables / ``.env`` (same as the CLI).
        on_token:       Optional callback invoked with each token delta string
                        as it arrives.  Useful for live-streaming output (e.g.
                        ``lambda t: print(t, end="", flush=True)``).  The
                        callback is called synchronously inside the event loop;
                        keep it lightweight.
        timeout:        Maximum seconds to wait for the complete response.
                        *None* means no limit.  Raises ``asyncio.TimeoutError``
                        if exceeded.
        capture_events: When *True*, every raw event dict received during the
                        run is appended to ``ClawResponse.events``.  Useful for
                        debugging or protocol-level assertions in test scripts.

    Returns:
        A ``ClawResponse`` containing the full text, run ID, elapsed time,
        and (optionally) the raw event log.

    Raises:
        ValueError:           If ``OPENCLAW_GATEWAY_TOKEN`` is not configured.
        RuntimeError:         If the gateway rejects the connection or message,
                              or if the agent reports an error.
        asyncio.TimeoutError: If *timeout* is exceeded before the run finishes.
    """
    cfg = config or GatewayConfig.from_env()
    if not cfg.token:
        raise ValueError(
            "OPENCLAW_GATEWAY_TOKEN is not set — "
            "pass a GatewayConfig(token=...) or set the environment variable"
        )

    identity = _load_or_create_identity(cfg.identity_file)
    t0 = time.monotonic()

    async def _execute() -> ClawResponse:
        async with websockets.connect(cfg.url) as ws:
            client = GatewayClient(ws, identity, token=cfg.token)
            await client.start()
            try:
                await client.connect()
                await client.send(session_key, message)

                run_id = None
                chunks: list[str] = []
                raw_events: list[dict] = []

                while True:
                    msg = await client.next_event()
                    event = msg.get("event", "")
                    payload = msg.get("payload", {})

                    if capture_events:
                        raw_events.append(msg)

                    if event == "agent" and payload.get("stream") == "lifecycle":
                        phase = payload.get("data", {}).get("phase")
                        if phase == "start":
                            run_id = payload.get("runId")
                        elif phase == "end":
                            if run_id is None or payload.get("runId") == run_id:
                                break

                    elif event == "agent" and payload.get("stream") == "assistant":
                        delta = payload.get("data", {}).get("delta", "")
                        if delta:
                            chunks.append(delta)
                            if on_token is not None:
                                on_token(delta)

                    elif event == "chat.error":
                        raise RuntimeError(f"Agent error: {payload}")
            finally:
                await client.stop()

        return ClawResponse(
            text="".join(chunks),
            run_id=run_id,
            elapsed_seconds=time.monotonic() - t0,
            events=raw_events if capture_events else [],
        )

    if timeout is not None:
        return await asyncio.wait_for(_execute(), timeout=timeout)
    return await _execute()


def prompt_sync(
    message: str,
    *,
    session_key: str = DEFAULT_SESSION_KEY,
    config: GatewayConfig | None = None,
    on_token: Callable[[str], None] | None = None,
    timeout: float | None = None,
    capture_events: bool = False,
) -> ClawResponse:
    """
    Synchronous wrapper around :func:`prompt_async`.

    Convenience for scripts and test runners that don't use ``async/await``.
    All parameters are forwarded directly — see :func:`prompt_async` for full
    documentation.
    """
    return asyncio.run(
        prompt_async(
            message,
            session_key=session_key,
            config=config,
            on_token=on_token,
            timeout=timeout,
            capture_events=capture_events,
        )
    )


# ── CLI streaming (backward-compatible) ──────────────────────────────────────

async def run(prompt: str, session_key: str) -> None:
    """
    Open a gateway connection, send the prompt, and stream the response to
    stdout token by token.  This is the original CLI entry point.

    For programmatic use prefer :func:`prompt_async` or :func:`prompt_sync`.

    Event handling:
    ───────────────
    The gateway does not use a separate chat.token/chat.complete event schema
    on operator.admin connections. Instead it broadcasts generic "agent" events:

      agent { stream: "lifecycle", data: { phase: "start" } }
        → agent run has begun; capture runId for matching the end event

      agent { stream: "assistant", data: { delta: "..." } }
        → incremental token; print immediately to stdout without newline

      agent { stream: "lifecycle", data: { phase: "end" } }
        → run complete; print trailing newline and exit the loop

    Other event types (health, tick, chat, …) are silently ignored — they are
    broadcast to all operator clients and are not relevant to this use case.

    No explicit chat.subscribe call is needed: the gateway pushes events to all
    connected operator.admin clients automatically. (chat.subscribe is only
    valid on dedicated streaming connections opened by the web UI layer.)
    """
    if not GATEWAY_TOKEN:
        print("Error: OPENCLAW_GATEWAY_TOKEN is not set.", file=sys.stderr)
        sys.exit(1)

    def _print_token(delta: str) -> None:
        print(delta, end="", flush=True)

    try:
        await prompt_async(prompt, session_key=session_key, on_token=_print_token)
        print()
    except RuntimeError as exc:
        print(f"\n{exc}", file=sys.stderr)
        sys.exit(1)


# ── CLI parsing ───────────────────────────────────────────────────────────────

def parse_args() -> tuple[str, str]:
    """
    Parse CLI arguments and return (prompt, session_key).

    Prompt assembly rules:
      - The positional PROMPT argument forms the first part of the message.
      - Pass "-" as PROMPT to read the prompt entirely from stdin.
      - Stdin is also read automatically when no PROMPT is given and stdin is
        not a tty (i.e. something is actually piped in).
      - If both a PROMPT argument and piped stdin are present they are joined
        with a blank line so the agent sees them as one message.

    The stdin-only-when-no-arg rule prevents hanging in non-interactive
    terminals (e.g. Cursor's shell tool) where isatty() returns False even
    when nothing is actually piped in.
    """
    parser = argparse.ArgumentParser(
        prog="claw_client.py",
        description="Send a prompt to the OpenClaw gateway and stream the response.",
        epilog=(
            "Examples:\n"
            "  python claw_client.py \"hello\"\n"
            "  python claw_client.py --session myproject \"what did we discuss?\"\n"
            "  echo \"some text\" | python claw_client.py\n"
            "  git diff HEAD~1 | python claw_client.py \"review this diff\"\n"
            "  cat file.txt | python claw_client.py - --session notes"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        metavar="PROMPT",
        help='prompt text, or "-" to read from stdin (default: read stdin if piped)',
    )
    parser.add_argument(
        "--session",
        default=DEFAULT_SESSION_KEY,
        metavar="KEY",
        help=f"gateway session key (default: {DEFAULT_SESSION_KEY!r}); the gateway "
             "stores message history per key so the agent remembers context across runs",
    )

    args = parser.parse_args()
    session_key = args.session

    parts = []
    if args.prompt and args.prompt != "-":
        parts.append(args.prompt)

    read_stdin = (args.prompt == "-") or (not parts and not sys.stdin.isatty())
    if read_stdin:
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            parts.append(stdin_text)

    if not parts:
        parser.print_usage(sys.stderr)
        sys.exit(1)

    return "\n\n".join(parts), session_key


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    prompt, session_key = parse_args()
    asyncio.run(run(prompt, session_key))


if __name__ == "__main__":
    main()
