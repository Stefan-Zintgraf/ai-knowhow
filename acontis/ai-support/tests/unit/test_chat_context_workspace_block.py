"""Unit tests: _chat_context_anythingllm_block (workspace resolution payload)."""

from __future__ import annotations

import pytest

from support_rag.config import AnythingLlmConfig, AppConfig, WebUiState
from support_rag.web_routes import _chat_context_anythingllm_block


def test_chat_context_workspace_block_implicit_first(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "support_rag.web_routes.list_workspace_slugs",
        lambda _alm: ["w1", "w2"],
    )
    cfg = AppConfig(
        anything_llm=AnythingLlmConfig(
            base_url="http://127.0.0.1:9",
            api_key="k" * 8,
            workspace_slug="",
        ),
        web_ui=WebUiState(anythingllm_workspace_slug_override=""),
    )
    b = _chat_context_anythingllm_block(cfg=cfg, wu=cfg.web_ui, alm=cfg.anything_llm)
    assert b["effective_resolution"] == "implicit_first"
    assert b["effective_workspace_slug"] == "w1"
    assert b["available_workspace_slugs"] == ["w1", "w2"]
    assert "workspace_list_error" not in b


def test_chat_context_workspace_block_override_wins(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "support_rag.web_routes.list_workspace_slugs",
        lambda _alm: ["w1"],
    )
    cfg = AppConfig(
        anything_llm=AnythingLlmConfig(
            base_url="http://127.0.0.1:9",
            api_key="k" * 8,
            workspace_slug="yaml-slug",
        ),
        web_ui=WebUiState(anythingllm_workspace_slug_override="ovr"),
    )
    b = _chat_context_anythingllm_block(cfg=cfg, wu=cfg.web_ui, alm=cfg.anything_llm)
    assert b["effective_resolution"] == "override"
    assert b["effective_workspace_slug"] == "ovr"


def test_chat_context_workspace_block_list_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def boom(_alm: AnythingLlmConfig) -> list[str]:
        raise RuntimeError("nope")

    monkeypatch.setattr("support_rag.web_routes.list_workspace_slugs", boom)
    cfg = AppConfig(
        anything_llm=AnythingLlmConfig(
            base_url="http://127.0.0.1:9",
            api_key="k" * 8,
            workspace_slug="",
        ),
        web_ui=WebUiState(anythingllm_workspace_slug_override=""),
    )
    b = _chat_context_anythingllm_block(cfg=cfg, wu=cfg.web_ui, alm=cfg.anything_llm)
    assert b["effective_resolution"] == "none"
    assert b.get("workspace_list_error")
