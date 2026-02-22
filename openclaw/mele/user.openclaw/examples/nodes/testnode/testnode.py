"""
OpenClaw example node: testnode.echo

Connects to the local Gateway WebSocket, registers a custom "testnode.echo"
command, and replies to invoke requests with a greeting.

Usage:
    pip install websockets cryptography python-dotenv
    python testnode.py

Reads OPENCLAW_GATEWAY_TOKEN (and other overrides) from .env next to this script.

After the node connects and is paired (local connections are auto-approved),
invoke it from the CLI:

    openclaw nodes invoke --node <nodeId> --command testnode.echo \
        --params '{"text":"world"}'
"""

import asyncio
import hashlib
import json
import os
import pathlib
import time
import uuid

from dotenv import load_dotenv
import websockets
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

load_dotenv(pathlib.Path(__file__).resolve().parent / ".env")

GATEWAY_HOST = os.environ.get("OPENCLAW_GATEWAY_HOST", "127.0.0.1")
GATEWAY_PORT = os.environ.get("OPENCLAW_GATEWAY_PORT", "18789")
GATEWAY_TOKEN = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
GATEWAY_URL = f"ws://{GATEWAY_HOST}:{GATEWAY_PORT}"

PROTOCOL_VERSION = 3
_state_dir = os.environ.get("OPENCLAW_STATE_DIR") or os.path.join(
    os.path.expanduser("~"), ".openclaw"
)
IDENTITY_FILE = os.path.join(
    _state_dir, "examples", "nodes", "testnode", "identity.json"
)

# Gateway only accepts known client ids (see GATEWAY_CLIENT_IDS); use node-host for custom nodes.
NODE_CLIENT_ID = "node-host"
NODE_DISPLAY_NAME = "Testnode Node (Python)"


def base64url_encode(data: bytes) -> str:
    import base64

    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_identity() -> dict:
    private_key = Ed25519PrivateKey.generate()
    private_pem = private_key.private_bytes(
        Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
    ).decode()
    public_pem = private_key.public_key().public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    ).decode()
    raw_public = private_key.public_key().public_bytes(
        Encoding.Raw, PublicFormat.Raw
    )
    device_id = hashlib.sha256(raw_public).hexdigest()
    return {
        "version": 1,
        "deviceId": device_id,
        "publicKeyPem": public_pem,
        "privateKeyPem": private_pem,
        "createdAtMs": int(time.time() * 1000),
    }


def load_or_create_identity() -> dict:
    if os.path.exists(IDENTITY_FILE):
        with open(IDENTITY_FILE) as f:
            data = json.load(f)
            if data.get("version") == 1 and data.get("deviceId") and data.get("privateKeyPem"):
                return data

    identity = generate_identity()
    os.makedirs(os.path.dirname(IDENTITY_FILE), exist_ok=True)
    with open(IDENTITY_FILE, "w") as f:
        json.dump(identity, f, indent=2)
    os.chmod(IDENTITY_FILE, 0o600)
    return identity


def sign_payload(private_pem: str, payload: str) -> str:
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

    key = load_pem_private_key(private_pem.encode(), password=None)
    signature = key.sign(payload.encode())
    return base64url_encode(signature)


def public_key_raw_b64url(public_pem: str) -> str:
    from cryptography.hazmat.primitives.serialization import load_pem_public_key

    pub = load_pem_public_key(public_pem.encode())
    raw = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    return base64url_encode(raw)


def build_device_auth_payload(
    device_id: str,
    client_id: str,
    client_mode: str,
    role: str,
    scopes: list[str],
    signed_at_ms: int,
    token: str,
    nonce: str | None,
) -> str:
    version = "v2" if nonce else "v1"
    parts = [
        version,
        device_id,
        client_id,
        client_mode,
        role,
        ",".join(scopes),
        str(signed_at_ms),
        token,
    ]
    if version == "v2":
        parts.append(nonce or "")
    return "|".join(parts)


class TestnodeNode:
    def __init__(self):
        self.identity = load_or_create_identity()
        self.pending: dict[str, asyncio.Future] = {}
        self.connected = False

    async def run(self):
        while True:
            try:
                await self._connect()
            except (
                websockets.exceptions.ConnectionClosed,
                OSError,
                asyncio.TimeoutError,
            ) as exc:
                print(f"Connection lost: {exc}. Reconnecting in 3s...")
                self.connected = False
                await asyncio.sleep(3)

    async def _connect(self):
        print(f"Connecting to {GATEWAY_URL} ...")
        async with websockets.connect(
            GATEWAY_URL, max_size=25 * 1024 * 1024
        ) as ws:
            self.ws = ws
            async for raw in ws:
                msg = json.loads(raw)
                msg_type = msg.get("type")

                if msg_type == "event":
                    await self._handle_event(msg)
                elif msg_type == "res":
                    self._handle_response(msg)

    async def _handle_event(self, msg: dict):
        event = msg.get("event")

        if event == "connect.challenge":
            nonce = msg.get("payload", {}).get("nonce")
            # Don't await: the message loop must keep reading to receive the connect "res".
            asyncio.create_task(self._send_connect(nonce))

        elif event == "node.invoke.request":
            await self._handle_invoke(msg.get("payload", {}))

        elif event == "tick":
            pass  # keepalive — no action needed, connection stays alive

    def _handle_response(self, msg: dict):
        req_id = msg.get("id")
        if req_id and req_id in self.pending:
            future = self.pending.pop(req_id)
            if not future.done():
                if msg.get("ok"):
                    future.set_result(msg.get("payload"))
                else:
                    future.set_exception(
                        Exception(f"Request failed: {msg.get('error')}")
                    )

    async def _request(self, method: str, params: dict) -> dict:
        req_id = str(uuid.uuid4())
        frame = {"type": "req", "id": req_id, "method": method, "params": params}
        future = asyncio.get_event_loop().create_future()
        self.pending[req_id] = future
        await self.ws.send(json.dumps(frame))
        return await asyncio.wait_for(future, timeout=30)

    async def _send_connect(self, nonce: str | None):
        identity = self.identity
        device_id = identity["deviceId"]
        signed_at_ms = int(time.time() * 1000)
        token = GATEWAY_TOKEN or ""
        role = "node"
        scopes: list[str] = []

        auth_payload = build_device_auth_payload(
            device_id=device_id,
            client_id=NODE_CLIENT_ID,
            client_mode="node",
            role=role,
            scopes=scopes,
            signed_at_ms=signed_at_ms,
            token=token,
            nonce=nonce,
        )
        signature = sign_payload(identity["privateKeyPem"], auth_payload)

        params = {
            "minProtocol": PROTOCOL_VERSION,
            "maxProtocol": PROTOCOL_VERSION,
            "client": {
                "id": NODE_CLIENT_ID,
                "displayName": NODE_DISPLAY_NAME,
                "version": "0.1.0",
                "platform": "linux",
                "mode": "node",
                "instanceId": device_id,
            },
            "role": role,
            "scopes": scopes,
            "caps": ["testnode"],
            "commands": ["testnode.echo"],
            "permissions": {},
            "auth": {"token": token} if token else None,
            "device": {
                "id": device_id,
                "publicKey": public_key_raw_b64url(identity["publicKeyPem"]),
                "signature": signature,
                "signedAt": signed_at_ms,
                "nonce": nonce,
            },
        }
        # Remove None auth to avoid sending {"auth": null}
        if params["auth"] is None:
            del params["auth"]

        try:
            result = await self._request("connect", params)
            self.connected = True
            print(f"Connected! Node ID: {device_id}")
            if result:
                policy = result.get("policy", {})
                tick_interval = policy.get("tickIntervalMs", 30000)
                print(f"  Protocol: {result.get('protocol')}")
                print(f"  Tick interval: {tick_interval}ms")
                auth_info = result.get("auth")
                if auth_info and auth_info.get("deviceToken"):
                    print("  Device token issued (pairing approved)")
        except Exception as exc:
            print(f"Connect failed: {exc}")
            raise

    async def _handle_invoke(self, payload: dict):
        request_id = payload.get("id", "")
        node_id = payload.get("nodeId", "")
        command = payload.get("command", "")
        params_json = payload.get("paramsJSON")

        if not request_id or not command:
            return

        params = json.loads(params_json) if params_json else {}
        print(f"Invoke: {command} params={params}")

        if command == "testnode.echo":
            text = params.get("text", "")
            result_payload = {"message": f"Hello from Testnode (Python)! You said: {text}"}
            await self._send_invoke_result(
                request_id=request_id,
                node_id=node_id,
                ok=True,
                payload_json=json.dumps(result_payload),
            )
        else:
            await self._send_invoke_result(
                request_id=request_id,
                node_id=node_id,
                ok=False,
                error={"code": "UNKNOWN_COMMAND", "message": f"Unknown command: {command}"},
            )

    async def _send_invoke_result(
        self,
        request_id: str,
        node_id: str,
        ok: bool,
        payload_json: str | None = None,
        error: dict | None = None,
    ):
        params: dict = {
            "id": request_id,
            "nodeId": node_id,
            "ok": ok,
        }
        if payload_json is not None:
            params["payloadJSON"] = payload_json
        if error is not None:
            params["error"] = error

        try:
            await self._request("node.invoke.result", params)
        except Exception:
            pass  # invoke results are best-effort


async def main():
    node = TestnodeNode()
    await node.run()


if __name__ == "__main__":
    asyncio.run(main())
