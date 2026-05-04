"""Unit tests: _redact_for_browser (plan §7a)."""

from __future__ import annotations

import json
import os

import pytest

from support_rag.config import AppConfig, _redact_for_browser, _merge_rag_env_over_yaml


def test_redact_blanks_api_keys_in_dump() -> None:
    c = AppConfig()
    c.llm_gateway.api_key = "gateway-key-min-8c"
    c.anything_llm.api_key = "anything-llm-key-8b"
    raw = c.model_dump(mode="json")
    r = _redact_for_browser(raw, cfg=c)
    assert r["llm_gateway"]["api_key"] == ""
    assert r["anything_llm"]["api_key"] == ""


def test_redact_strips_substrings_in_nested_strings() -> None:
    c = AppConfig()
    c.llm_gateway.api_key = "supersecretgwkey1"
    c.web_ui.message_draft = "token supersecretgwkey1 in text"
    raw = c.model_dump(mode="json")
    r = _redact_for_browser(raw, cfg=c)
    s = json.dumps(r, ensure_ascii=True)
    assert "supersecretgwkey1" not in s
    assert "token [REDACTED] in text" in s or "REDACTED" in s


def test_merge_env_anything_llm() -> None:
    os.environ["RAG_ANYTHING_LLM__API_KEY"] = "from-env-alm-9chars"
    os.environ["RAG_ANYTHING_LLM__BASE_URL"] = "http://alm.local:3001"
    try:
        m = _merge_rag_env_over_yaml({})
        assert m.get("anything_llm", {}).get("api_key") == "from-env-alm-9chars"
        assert m.get("anything_llm", {}).get("base_url") == "http://alm.local:3001"
    finally:
        del os.environ["RAG_ANYTHING_LLM__API_KEY"]
        del os.environ["RAG_ANYTHING_LLM__BASE_URL"]


def test_config_has_anything_llm_defaults() -> None:
    c = AppConfig()
    assert c.anything_llm.base_url.startswith("http")
    assert c.web_ui.anythingllm_models_source == "alm_desktop"
    assert 1 <= c.web_ui.top_k <= 32
