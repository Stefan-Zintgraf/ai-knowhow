"""Ollama direct embed: one request per string + optional char clip (all-minilm context)."""

from __future__ import annotations

import json

import httpx

from support_rag.config import LlmGatewayConfig
from support_rag.gateway import LLMGatewayClient


def test_ollama_embed_sync_one_request_per_text() -> None:
    bodies: list[dict[str, object]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        b = json.loads(request.content.decode("utf-8"))
        bodies.append(b)
        return httpx.Response(
            200,
            json={
                "model": "all-minilm",
                "embeddings": [[0.1, 0.2]],
            },
        )

    transport = httpx.MockTransport(handler)
    cfg = LlmGatewayConfig(
        base_url="http://127.0.0.1:4000",
        ollama_embed_base_url="http://127.0.0.1:11434",
        ollama_embed_model="all-minilm",
    )
    g = LLMGatewayClient(cfg)
    g._ollama_client.close()
    g._ollama_client = httpx.Client(
        transport=transport, base_url="http://127.0.0.1:11434", trust_env=False
    )
    try:
        vecs, m = g.embed_sync(["a", "b"], kind="doc")
        assert len(vecs) == 2
        assert m == "all-minilm"
        assert len(bodies) == 2
        assert bodies[0]["input"] == "a"
        assert bodies[1]["input"] == "b"
    finally:
        g.close_sync()


def test_ollama_clip_long_input() -> None:
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        b = json.loads(request.content.decode("utf-8"))
        calls.append(str(b.get("input", "")))
        return httpx.Response(
            200,
            json={"model": "m", "embeddings": [[0.0]]},
        )

    transport = httpx.MockTransport(handler)
    cfg = LlmGatewayConfig(
        base_url="http://127.0.0.1:4000",
        ollama_embed_base_url="http://127.0.0.1:11434",
        ollama_embed_model="all-minilm",
        ollama_embed_truncate_chars=12,
    )
    g = LLMGatewayClient(cfg)
    g._ollama_client.close()
    g._ollama_client = httpx.Client(
        transport=transport, base_url="http://127.0.0.1:11434", trust_env=False
    )
    try:
        long = "x" * 100
        g.embed_sync([long], kind="doc")
        assert len(calls) == 1
        assert len(calls[0]) == 12
    finally:
        g.close_sync()
