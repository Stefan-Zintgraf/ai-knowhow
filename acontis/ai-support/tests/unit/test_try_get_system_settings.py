"""Unit tests: try_get_system_settings returns readable errors (no bare exception type names)."""

from __future__ import annotations

from unittest.mock import patch

import httpx

from support_rag.anythingllm_client import try_get_system_settings
from support_rag.config import AnythingLlmConfig


def test_try_get_system_settings_success() -> None:
    data = {"settings": {"LLMProvider": "x"}}
    with patch(
        "support_rag.anythingllm_client.get_system_settings",
        return_value=data,
    ):
        raw, err = try_get_system_settings(AnythingLlmConfig())
    assert raw == data
    assert err is None


def test_try_get_system_settings_403_message() -> None:
    req = httpx.Request("GET", "http://127.0.0.1:3001/api/v1/system")
    resp = httpx.Response(403, request=req)
    exc = httpx.HTTPStatusError("forbidden", request=req, response=resp)
    with patch(
        "support_rag.anythingllm_client.get_system_settings",
        side_effect=exc,
    ):
        raw, err = try_get_system_settings(AnythingLlmConfig())
    assert raw is None
    assert err is not None
    assert "403" in err
    assert "API key" in err or "key" in err.lower()


def test_try_get_system_settings_connect_error_message() -> None:
    with patch(
        "support_rag.anythingllm_client.get_system_settings",
        side_effect=httpx.ConnectError("Connection refused"),
    ):
        raw, err = try_get_system_settings(AnythingLlmConfig())
    assert raw is None
    assert err is not None
    assert "unreachable" in err.lower() or "Connection" in err
