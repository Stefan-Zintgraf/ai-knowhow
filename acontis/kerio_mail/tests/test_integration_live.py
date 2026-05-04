"""Live Kerio Client API smoke tests (optional)."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from kerio_mail.client import KerioClient
from kerio_mail.read_mailbox import application_from_env


def _truthy_verify_ssl() -> bool:
    raw = os.environ.get("KERIO_VERIFY_SSL")
    if raw is None or raw.strip() == "":
        return True
    return raw.strip().lower() not in ("0", "false", "no", "off")


@pytest.fixture(scope="module")
def live_creds() -> tuple[str, str, str, bool]:
    root = Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env")
    base = os.environ.get("KERIO_BASE_URL", "").strip()
    user = os.environ.get("KERIO_USERNAME", "").strip()
    password = os.environ.get("KERIO_PASSWORD", "")
    if not base or not user or not password:
        pytest.skip("Set KERIO_BASE_URL, KERIO_USERNAME, KERIO_PASSWORD in .env")
    return base, user, password, _truthy_verify_ssl()


@pytest.mark.integration
def test_session_login_returns_token(live_creds: tuple[str, str, str, bool]) -> None:
    base, user, password, verify = live_creds
    client = KerioClient(base, verify_ssl=verify)
    token = client.login(user, password, application=application_from_env())
    assert isinstance(token, str) and len(token) > 0


@pytest.mark.integration
def test_folders_get_after_login(live_creds: tuple[str, str, str, bool]) -> None:
    base, user, password, verify = live_creds
    client = KerioClient(base, verify_ssl=verify)
    client.login(user, password, application=application_from_env())
    result = client.folders_get()
    assert isinstance(result, dict)
    assert "list" in result
    assert isinstance(result["list"], list)
