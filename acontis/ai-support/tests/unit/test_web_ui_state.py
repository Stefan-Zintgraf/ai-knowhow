"""WebUiState coercion and Option B + chat rules."""

from __future__ import annotations

import pytest

from support_rag.config import WebUiState


def test_litellm_gateway_coerced_to_llm_gateway() -> None:
    w = WebUiState.model_validate(
        {"anythingllm_models_source": "litellm_gateway", "anythingllm_completion": "gateway"}
    )
    assert w.anythingllm_models_source == "llm_gateway"
    assert w.chat_model_source == "llm_gateway"


def test_option_b_plus_chat_anythingllm_raises() -> None:
    with pytest.raises(ValueError, match="Option B"):
        WebUiState(
            anythingllm_models_source="llm_gateway",
            chat_model_source="anythingllm",
        )


def test_chat_model_source_migrated_from_anythingllm_completion() -> None:
    w = WebUiState.model_validate({"anythingllm_completion": "anythingllm_native"})
    assert w.chat_model_source == "anythingllm"
