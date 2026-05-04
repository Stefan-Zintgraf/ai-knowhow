"""NFR-6: after API container (`support-rag`) restarts, health smoke still succeeds.

Requires Docker, `docker compose`, a running stack, and:
  `RUN_INTEGRATION=1` `RUN_NFR6_COMPOSE=1`

Set `NFR6_BASE_URL` (default `http://127.0.0.1:8080`) and `RAG_SERVICE_TOKEN` to match
`docker-compose.yaml` (default token `dev-service` if unset in env).
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

import httpx
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_COMPOSE_FILE = _REPO_ROOT / "docker-compose.yaml"
_API_SERVICE = "support-rag"
_DEFAULT_BASE = "http://127.0.0.1:8080"
_HEALTH = "/rag/health"
_TIMEOUT_SEC = 120
_POLL_SEC = 2.0


def _base_url() -> str:
    return (os.environ.get("NFR6_BASE_URL") or _DEFAULT_BASE).rstrip("/")


def _bearer() -> str:
    return (os.environ.get("RAG_SERVICE_TOKEN") or "dev-service").strip()


def _wait_health(client: httpx.Client, headers: dict[str, str], deadline: float) -> None:
    while time.time() < deadline:
        try:
            r = client.get(f"{_base_url()}{_HEALTH}", headers=headers, timeout=5.0)
        except (httpx.ConnectError, httpx.ReadError, httpx.WriteError):
            time.sleep(_POLL_SEC)
            continue
        if r.status_code == 200:
            return
        time.sleep(_POLL_SEC)
    msg = (
        f"expected 200 from GET {_HEALTH} within {_TIMEOUT_SEC}s after restart; "
        f"last base {_base_url()}"
    )
    raise AssertionError(msg)


@pytest.mark.nfr6_compose
@pytest.mark.requires_services
def test_nfr6_restart_support_rag_then_health_ok() -> None:
    if not _COMPOSE_FILE.is_file():
        pytest.skip(f"missing compose file: {_COMPOSE_FILE}")

    base = _base_url()
    token = _bearer()
    headers = {"Authorization": f"Bearer {token}"}

    with httpx.Client() as client:
        try:
            pre = client.get(f"{base}{_HEALTH}", headers=headers, timeout=10.0)
        except (httpx.ConnectError, httpx.ReadError) as e:
            pytest.skip(f"stack not up at {base}: {e}")
        if pre.status_code != 200:
            pytest.skip(
                f"health not 200 before restart (got {pre.status_code}); bring stack up first",
            )

    try:
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                str(_COMPOSE_FILE),
                "restart",
                _API_SERVICE,
            ],
            cwd=str(_REPO_ROOT),
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except FileNotFoundError:
        pytest.skip("docker CLI not on PATH")
    except subprocess.CalledProcessError as e:
        pytest.fail(
            f"docker compose restart failed: {e.stderr or e.stdout or e!r}",
        )

    deadline = time.time() + _TIMEOUT_SEC
    with httpx.Client() as client:
        _wait_health(client, headers, deadline)
        r = client.get(f"{base}{_HEALTH}", headers=headers, timeout=10.0)
        assert r.status_code == 200
        data = r.json()
        assert data.get("status") == "ok"
        assert "contract_version" in data
