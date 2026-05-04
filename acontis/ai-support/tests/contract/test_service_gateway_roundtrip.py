"""R-15/R-16: service retrieve drives async embed and rewrite (MockTransport)."""

from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import numpy as np
import pytest
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import (
    VectorStoreQuery,
    VectorStoreQueryResult,
)

from support_rag.config import AppConfig, LlmGatewayConfig
from support_rag.schemas import RetrievalRequest

_httpx_AsyncClient = httpx.AsyncClient
_httpx_Client = httpx.Client


@contextlib.asynccontextmanager
async def _rag_with_mock_http(
    app_config: AppConfig, captured: list[httpx.Request]
) -> AsyncIterator[Any]:
    """Build `RAGService` with TCP-free gateway; all outbound `httpx` calls recorded."""
    mock_index = MagicMock()
    mock_store = MagicMock()
    q_inst = MagicMock()
    q_inst.get_collections.return_value = MagicMock()
    q_async = MagicMock()
    q_async.close = AsyncMock()

    dsize = app_config.qdrant.vector_size

    def transport_handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        p = str(request.url.path)
        if p.endswith("/v1/embeddings") or p == "/v1/embeddings":
            return httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "embedding": [0.0] * dsize,
                            "index": 0,
                        }
                    ],
                    "model": "m",
                },
            )
        if p.endswith("/v1/chat/completions") or p == "/v1/chat/completions":
            return httpx.Response(
                200,
                json={
                    "choices": [
                        {
                            "message": {
                                "content": '{"alternatives": ["a1", "a2"]}',
                            }
                        }
                    ]
                },
            )
        if p.endswith("/v1/models") or p == "/v1/models":
            return httpx.Response(200, json={"data": []})
        return httpx.Response(404, json={"error": p})

    transport = httpx.MockTransport(transport_handler)

    def async_client(*args: object, **kwargs: object) -> httpx.AsyncClient:
        k = dict(kwargs)
        k["transport"] = transport
        return _httpx_AsyncClient(*args, **k)  # type: ignore[misc,arg-type]

    def sync_client(*args: object, **kwargs: object) -> httpx.Client:
        k = dict(kwargs)
        k["transport"] = transport
        return _httpx_Client(*args, **k)  # type: ignore[misc,arg-type]

    with (
        patch("support_rag.service.QdrantClient", return_value=q_inst),
        patch("support_rag.service.AsyncQdrantClient", return_value=q_async),
        patch("support_rag.service.QdrantVectorStore", return_value=mock_store),
        patch(
            "support_rag.service.VectorStoreIndex.from_vector_store",
            return_value=mock_index,
        ),
        patch("support_rag.gateway.httpx.AsyncClient", side_effect=async_client),
        patch("support_rag.gateway.httpx.Client", side_effect=sync_client),
    ):
        from support_rag.service import RAGService

        svc = RAGService(app_config)
        try:
            yield svc
        finally:
            await svc.aclose()


@pytest.mark.asyncio
async def test_retrieve_async_embed_uses_x_slot_and_trace_r15() -> None:
    captured: list[httpx.Request] = []
    lf = "x-langfuse-trace-id"
    cfg = AppConfig()
    cfg.service.langfuse_header_name = lf
    cfg.llm_gateway = LlmGatewayConfig(
        base_url="http://gw.test",
        timeout_s=5.0,
        embedding_slot="service-embed",
        retrieval_slot="service-llm",
    )
    cfg.retrieval.hyde.enabled = False
    cfg.retrieval.query_rewrite.enabled = False

    async def aquery(
        _query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        return VectorStoreQueryResult(
            nodes=[TextNode(id_="n1", text="t", metadata={"parent_id": "p"})]
        )

    async with _rag_with_mock_http(cfg, captured) as svc:
        svc._stores["kb"].aquery = aquery
        svc._stores["tickets"].aquery = aquery
        with patch.object(svc, "_ce", return_value=MagicMock()) as m_ce:
            m_ce.return_value.predict = MagicMock(
                return_value=np.array([0.5], dtype=np.float32)
            )
            trace = {
                lf: "trace-abc",
                "traceparent": (
                    "00-12345678901234567890123456789012-1234567890123456-01"
                ),
            }
            await svc.retrieve(
                RetrievalRequest(
                    query="q",
                    top_k=2,
                    namespaces=["kb"],
                    rewrite=False,
                    rerank=True,
                ),
                trace_ctx=trace,
            )

    embed_reqs = [r for r in captured if "embeddings" in str(r.url.path)]
    assert len(embed_reqs) >= 1
    r0 = embed_reqs[0]
    assert r0.headers.get("X-Slot") == "service-embed"
    assert r0.headers.get(lf) == "trace-abc"
    assert r0.headers.get("traceparent") == trace["traceparent"]


@pytest.mark.asyncio
async def test_retrieve_rewrite_chat_uses_retrieval_slot_and_trace_r16() -> None:
    captured: list[httpx.Request] = []
    lf = "x-langfuse-trace-id"
    cfg = AppConfig()
    cfg.service.langfuse_header_name = lf
    cfg.llm_gateway = LlmGatewayConfig(
        base_url="http://gw.test",
        timeout_s=5.0,
        embedding_slot="e-slot",
        retrieval_slot="r-slot-rewrite",
    )
    cfg.retrieval.hyde.enabled = False
    cfg.retrieval.query_rewrite.enabled = True
    cfg.retrieval.query_rewrite.n_alternatives = 2

    async def aquery(
        _query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        return VectorStoreQueryResult(
            nodes=[TextNode(id_="n1", text="t", metadata={"parent_id": "p"})]
        )

    async with _rag_with_mock_http(cfg, captured) as svc:
        svc._stores["kb"].aquery = aquery
        svc._stores["tickets"].aquery = aquery
        with patch.object(svc, "_ce", return_value=MagicMock()) as m_ce:
            m_ce.return_value.predict = MagicMock(
                return_value=np.array([0.5], dtype=np.float32)
            )
            trace = {
                lf: "lf-99",
                "traceparent": "00-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-bbbbbbbbbbbbbbbb-01",
            }
            await svc.retrieve(
                RetrievalRequest(
                    query="q",
                    top_k=2,
                    namespaces=["kb"],
                    rewrite=True,
                    rerank=True,
                ),
                trace_ctx=trace,
            )

    chat_reqs = [r for r in captured if "completions" in str(r.url.path)]
    assert len(chat_reqs) >= 1
    c0 = chat_reqs[0]
    assert c0.headers.get("X-Slot") == "r-slot-rewrite"
    assert c0.headers.get(lf) == "lf-99"
    assert c0.headers.get("traceparent") == trace["traceparent"]
