"""R-15/R-16: `X-Slot` on gateway requests from LLMGatewayClient (offline, no network)."""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import Iterator
from unittest.mock import patch

import httpx

# Patch replaces `httpx.AsyncClient` on the module; keep real constructors for test doubles.
_httpx_AsyncClient = httpx.AsyncClient
_httpx_Client = httpx.Client

from support_rag.config import LlmGatewayConfig  # noqa: E402
from support_rag.gateway import LLMGatewayClient  # noqa: E402


@contextlib.contextmanager
def _mocked_gateway(
    config: LlmGatewayConfig,
) -> Iterator[tuple[LLMGatewayClient, list[httpx.Request]]]:
    """Use `httpx.MockTransport` so no TCP; capture every outgoing request."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        p = request.url.path
        if p == "/v1/embeddings" or p.endswith("/v1/embeddings"):
            return httpx.Response(
                200,
                json={"data": [{"embedding": [0.0], "index": 0}], "model": "m"},
            )
        if p == "/v1/chat/completions" or p.endswith("/v1/chat/completions"):
            return httpx.Response(
                200,
                json={"choices": [{"message": {"content": "ok"}}]},
            )
        return httpx.Response(404, json={"error": p})

    transport = httpx.MockTransport(handler)

    def async_client(*args: object, **kwargs: object) -> httpx.AsyncClient:
        k = dict(kwargs)
        k["transport"] = transport
        return _httpx_AsyncClient(*args, **k)  # type: ignore[misc,arg-type]

    def sync_client(*args: object, **kwargs: object) -> httpx.Client:
        k = dict(kwargs)
        k["transport"] = transport
        return _httpx_Client(*args, **k)  # type: ignore[misc,arg-type]

    with (
        patch("support_rag.gateway.httpx.AsyncClient", side_effect=async_client),
        patch("support_rag.gateway.httpx.Client", side_effect=sync_client),
    ):
        g = LLMGatewayClient(config)
        try:
            yield g, captured
        finally:
            g.close_sync()


def test_embed_async_sets_x_slot_from_embedding_slot() -> None:
    cfg = LlmGatewayConfig(
        base_url="http://gateway.test",
        timeout_s=5.0,
        embedding_slot="custom-embed",
        retrieval_slot="llm-a",
    )
    with _mocked_gateway(cfg) as (g, captured):

        async def _run() -> None:
            try:
                await g.embed(["x"], kind="query")
            finally:
                await g.aclose()

        asyncio.run(_run())
    assert len(captured) == 1
    assert captured[0].headers.get("X-Slot") == "custom-embed"


def test_embed_sync_sets_x_slot_from_embedding_slot() -> None:
    cfg = LlmGatewayConfig(
        base_url="http://gateway.test",
        timeout_s=5.0,
        embedding_slot="sync-embed-slot",
        retrieval_slot="llm-b",
    )
    with _mocked_gateway(cfg) as (g, captured):
        g.embed_sync(["y"], kind="doc")
    assert len(captured) == 1
    assert captured[0].headers.get("X-Slot") == "sync-embed-slot"


def test_chat_completion_async_uses_chat_slot_x_slot() -> None:
    async def _run() -> None:
        cfg = LlmGatewayConfig(
            base_url="http://gateway.test",
            timeout_s=5.0,
            embedding_slot="e",
            retrieval_slot="retrieval-llm-slot",
            chat_slot="ui-chat-slot",
        )
        with _mocked_gateway(cfg) as (g, captured):
            try:
                await g.chat_completion(
                    [{"role": "user", "content": "hi"}],
                )
            finally:
                await g.aclose()
        assert len(captured) == 1
        assert captured[0].headers.get("X-Slot") == "ui-chat-slot"
        b = json.loads(captured[0].content.decode())
        assert b.get("model") == "retrieval"  # default chat_model

    asyncio.run(_run())


def test_chat_completion_async_body_uses_config_chat_model() -> None:
    async def _run() -> None:
        cfg = LlmGatewayConfig(
            base_url="http://gateway.test",
            timeout_s=5.0,
            chat_slot="chat_llm",
            chat_model="chat",
        )
        with _mocked_gateway(cfg) as (g, captured):
            try:
                await g.chat_completion(
                    [{"role": "user", "content": "hi"}],
                )
            finally:
                await g.aclose()
        assert len(captured) == 1
        b = json.loads(captured[0].content.decode())
        assert b.get("model") == "chat"

    asyncio.run(_run())


def test_chat_completion_sync_uses_retrieval_slot_x_slot() -> None:
    cfg = LlmGatewayConfig(
        base_url="http://gateway.test",
        timeout_s=5.0,
        embedding_slot="e",
        retrieval_slot="default-llm",
    )
    with _mocked_gateway(cfg) as (g, captured):
        g.chat_completion_sync(
            [{"role": "user", "content": "hi"}],
        )
    assert len(captured) == 1
    assert captured[0].headers.get("X-Slot") == "default-llm"


def test_chat_completion_explicit_slot_header() -> None:
    cfg = LlmGatewayConfig(
        base_url="http://gateway.test",
        timeout_s=5.0,
        embedding_slot="e",
        retrieval_slot="default-llm",
    )
    with _mocked_gateway(cfg) as (g, captured):
        g.chat_completion_sync(
            [{"role": "user", "content": "q"}],
            slot="override-slot",
        )
    assert len(captured) == 1
    assert captured[0].headers.get("X-Slot") == "override-slot"
