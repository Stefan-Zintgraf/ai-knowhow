#!/usr/bin/env python3
"""
Minimal OpenClaw gateway client.

Sends a prompt to the OpenClaw gateway and streams the agent's response to
stdout, token by token. Exits cleanly when the agent finishes.

Usage:
    python claw_client.py "your prompt here"
    python claw_client.py --session myproject "what did we discuss?"
    echo "some text" | python claw_client.py
    echo "some text" | python claw_client.py "optional prefix prompt"
    cat file.txt    | python claw_client.py "summarise this"
    git diff HEAD~1 | python claw_client.py --session codereview "review this diff"
    cat file.txt    | python claw_client.py - --session notes

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
    # Device ID is deterministic from the public key so it survives restarts.
    device_id = hashlib.sha256(raw_pub).hexdigest()
    return {
        "version": 1,
        "deviceId": device_id,
        "publicKeyPem": pub_pem,
        "privateKeyPem": priv_pem,
        "createdAtMs": int(time.time() * 1000),
    }


def _load_or_create_identity() -> dict:
    """
    Load the identity from identity.json if it exists and is valid, otherwise
    generate a new one and persist it. File permissions are set to 0600 to
    protect the private key.
    """
    if IDENTITY_FILE.exists():
        data = json.loads(IDENTITY_FILE.read_text())
        if data.get("version") == 1 and data.get("deviceId") and data.get("privateKeyPem"):
            return data
    identity = _generate_identity()
    IDENTITY_FILE.write_text(json.dumps(identity, indent=2))
    IDENTITY_FILE.chmod(0o600)
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

    def __init__(self, ws, identity: dict):
        self._ws = ws
        self._identity = identity
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
                # Wake up the coroutine waiting for this specific request id.
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
        # The gateway sends connect.challenge as the very first event; drain
        # the queue until we find it (other event types are unlikely here but
        # we skip them defensively rather than assuming first = challenge).
        nonce = None
        while True:
            msg = await asyncio.wait_for(self._events.get(), timeout=10)
            if msg.get("event") == "connect.challenge":
                nonce = msg.get("payload", {}).get("nonce")
                break

        identity = self._identity
        device_id = identity["deviceId"]
        signed_at_ms = int(time.time() * 1000)
        token = GATEWAY_TOKEN or ""

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
                "id": CLIENT_ID,          # must be "gateway-client" (gateway allowlist)
                "displayName": "claw-client-py",
                "version": "1.0",
                "platform": sys.platform,
                "mode": CLIENT_MODE,      # "ui" = operator UI client
                "instanceId": device_id,  # stable ID for this client instance
            },
            "role": ROLE,
            "scopes": SCOPES,
            "auth": {"token": token} if token else None,
            "device": {
                "id": device_id,
                "publicKey": _pub_b64url(identity["publicKeyPem"]),  # raw Ed25519 pubkey, base64url
                "signature": signature,   # signs the auth payload string above
                "signedAt": signed_at_ms,
                "nonce": nonce,           # ties this signature to the challenge
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
            "deliver": True,  # trigger the agent immediately (vs. draft mode)
        })
        if not resp.get("ok"):
            raise RuntimeError(f"chat.send failed: {resp.get('error')}")


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

async def run(prompt: str, session_key: str) -> None:
    """
    Open a gateway connection, send the prompt, and stream the response.

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

    identity = _load_or_create_identity()
    async with websockets.connect(GATEWAY_URL) as ws:
        client = GatewayClient(ws, identity)
        await client.start()
        try:
            await client.connect()
            await client.send(session_key, prompt)

            # Track the runId so we can match the lifecycle:end event to the
            # correct run (other runs in other sessions could produce events too).
            run_id = None
            while True:
                msg = await client.next_event()
                event = msg.get("event", "")
                payload = msg.get("payload", {})

                if event == "agent" and payload.get("stream") == "lifecycle":
                    phase = payload.get("data", {}).get("phase")
                    if phase == "start":
                        run_id = payload.get("runId")
                    elif phase == "end":
                        if run_id is None or payload.get("runId") == run_id:
                            print()  # newline after the last streamed token
                            break

                elif event == "agent" and payload.get("stream") == "assistant":
                    # data.delta is the new characters added since the last event;
                    # data.text is the full accumulated text so far (we use delta).
                    delta = payload.get("data", {}).get("delta", "")
                    if delta:
                        print(delta, end="", flush=True)

                elif event == "chat.error":
                    print(f"\nAgent error: {payload}", file=sys.stderr)
                    sys.exit(1)
        finally:
            await client.stop()


def main() -> None:
    prompt, session_key = parse_args()
    asyncio.run(run(prompt, session_key))


if __name__ == "__main__":
    main()
