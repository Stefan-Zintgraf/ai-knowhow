"""Unit: LLMGatewayClient passes trace W3C + Langfuse headers to gateway `post` (NFR-4)."""

from __future__ import annotations

import contextlib
from collections.abc import Iterator
from unittest.mock import patch

import httpx

from support_rag.config import LlmGatewayConfig
from support_rag.gateway import LLMGatewayClient

_httpx_AsyncClient = httpx.AsyncClient
_httpx_Client = httpx.Client


def test_slot_headers_merges_traceparent_from_trace_ctx() -> None:
    g = LLMGatewayClient(
        LlmGatewayConfig(
            base_url="http://127.0.0.1:9",
            timeout_s=1.0,
        )
    )
    try:
        h = g._slot_headers(  # noqa: SLF001 — public seam for NFR-4
            "embedding",
            trace_ctx={"traceparent": "00-0af7651916cd43dd8448ed2113c0eaa7-b7ad6b7179203337-01"},
        )
        assert h.get("traceparent") == "00-0af7651916cd43dd8448ed2113c0eaa7-b7ad6b7179203337-01"
        assert h.get("X-Slot") == "embedding"
    finally:
        g.close_sync()


@contextlib.contextmanager
def _mocked_gateway(
    config: LlmGatewayConfig,
) -> Iterator[tuple[LLMGatewayClient, list[httpx.Request]]]:
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
            return httpx.Response(200, json={"choices": [{"message": {"content": "ok"}}]})
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


def test_embed_post_includes_langfuse_and_traceparent_nfr4() -> None:
    lf = "x-langfuse-trace-id"
    tp = "00-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-bbbbbbbbbbbbbbbb-01"
    cfg = LlmGatewayConfig(
        base_url="http://gateway.test",
        timeout_s=5.0,
    )
    with _mocked_gateway(cfg) as (g, captured):
        # Mirror `app._trace_ctx` keys: Langfuse name + W3C traceparent
        ctx = {lf: "lf-xyz", "traceparent": tp}
        g.embed_sync(["x"], kind="doc", trace_ctx=ctx)
    assert len(captured) == 1
    assert captured[0].headers.get("X-Slot") == "embedding"
    assert captured[0].headers.get(lf) == "lf-xyz"
    assert captured[0].headers.get("traceparent") == tp


def test_chat_completion_sync_includes_langfuse_and_traceparent_nfr4() -> None:
    lf = "x-langfuse-trace-id"
    tp = "00-0af7651916cd43dd8448ed2113c0eaa7-b7ad6b7179203337-01"
    cfg = LlmGatewayConfig(
        base_url="http://gateway.test",
        timeout_s=5.0,
    )
    with _mocked_gateway(cfg) as (g, captured):
        ctx = {lf: "id-1", "traceparent": tp}
        g.chat_completion_sync(
            [{"role": "user", "content": "hi"}],
            trace_ctx=ctx,
        )
    assert len(captured) == 1
    assert captured[0].headers.get("X-Slot") == "retrieval_llm"
    assert captured[0].headers.get(lf) == "id-1"
    assert captured[0].headers.get("traceparent") == tp
