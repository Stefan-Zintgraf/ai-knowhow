"""Contract: R-4 — query rewrite via `chat_completion_sync`; at most 3 alts; HyDE off by default.

HTTP **X-Slot** on sync chat (rewrite + HyDE) via `httpx.MockTransport` (see also
`test_service_gateway_roundtrip` R-16 rewrite + slot test).
"""

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
    """`RAGService` with TCP-free gateway; record outbound `httpx` (see service roundtrip)."""
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
async def test_rewrite_adds_alternatives_capped(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    svc._config.retrieval.query_rewrite.enabled = True
    svc._config.retrieval.query_rewrite.n_alternatives = 3
    svc._config.retrieval.hyde.enabled = False

    calls: list[VectorStoreQuery] = []

    async def aquery(
        q: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        calls.append(q)
        return VectorStoreQueryResult(nodes=[TextNode(id_="n1", text="x", metadata={})])

    svc._stores["kb"].aquery = aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    # Four alternatives in JSON, service keeps first 3
    body = '{"alternatives": ["alt-a", "alt-b", "alt-c", "alt-d"]}'
    with patch.object(
        svc._gateway,
        "chat_completion_sync",
        return_value=body,
    ) as m_chat:
        res, _ = await svc.retrieve(
            RetrievalRequest(
                query="original",
                top_k=6,
                namespaces=["kb"],
                rewrite=True,
                rerank=False,
            )
        )
    m_chat.assert_called()
    # 1 core + 3 alts = 4 embed / query passes
    assert len(calls) == 4
    assert res.rewritten_queries == ["alt-a", "alt-b", "alt-c"]


@pytest.mark.asyncio
async def test_hyde_off_no_extra_hypothetical_call(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    assert svc._config.retrieval.hyde.enabled is False
    calls: list[VectorStoreQuery] = []

    async def aquery(
        q: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        calls.append(q)
        return VectorStoreQueryResult(nodes=[])

    svc._stores["kb"].aquery = aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    h_chat = MagicMock(
        return_value='{"alternatives": []}',
    )
    h_hyde = MagicMock(return_value="should not be used when hyde off")
    with (
        patch.object(svc._gateway, "chat_completion_sync", h_chat),
        patch.object(svc, "_hyde", h_hyde),
    ):
        await svc.retrieve(
            RetrievalRequest(
                query="q",
                top_k=6,
                namespaces=["kb"],
                rewrite=True,
                rerank=False,
            )
        )
    h_hyde.assert_not_called()


@pytest.mark.asyncio
async def test_rewrite_httpx_sets_x_slot_r4() -> None:
    """R-4: rewrite chat uses `X-Slot` = `llm_gateway.retrieval_slot` on the sync client."""
    captured: list[httpx.Request] = []
    cfg = AppConfig()
    cfg.llm_gateway = LlmGatewayConfig(
        base_url="http://gw.test",
        timeout_s=5.0,
        embedding_slot="e-slot",
        retrieval_slot="r4-offline-rewrite",
    )
    cfg.retrieval.hyde.enabled = False
    cfg.retrieval.query_rewrite.enabled = True
    cfg.retrieval.query_rewrite.n_alternatives = 1

    async def aquery(
        _q: VectorStoreQuery,
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
            await svc.retrieve(
                RetrievalRequest(
                    query="q",
                    top_k=2,
                    namespaces=["kb"],
                    rewrite=True,
                    rerank=True,
                ),
            )
    chat_reqs = [r for r in captured if "completions" in str(r.url.path)]
    assert len(chat_reqs) >= 1
    assert chat_reqs[0].headers.get("X-Slot") == "r4-offline-rewrite"


@pytest.mark.asyncio
async def test_hyde_on_httpx_sets_x_slot_r4() -> None:
    """R-4: with HyDE enabled, hypothetical completion uses the same `X-Slot` as retrieval LLM."""
    captured: list[httpx.Request] = []
    cfg = AppConfig()
    dsize = cfg.qdrant.vector_size
    cfg.llm_gateway = LlmGatewayConfig(
        base_url="http://gw.test",
        timeout_s=5.0,
        embedding_slot="e-slot",
        retrieval_slot="r4-hyde-only",
    )
    cfg.retrieval.hyde.enabled = True
    cfg.retrieval.query_rewrite.enabled = False

    def transport_handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        p = str(request.url.path)
        if p.endswith("/v1/embeddings") or p == "/v1/embeddings":
            return httpx.Response(
                200,
                json={"data": [{"embedding": [0.0] * dsize, "index": 0}], "model": "m"},
            )
        if p.endswith("/v1/chat/completions") or p == "/v1/chat/completions":
            return httpx.Response(
                200,
                json={
                    "choices": [
                        {"message": {"content": "Hypothetical support answer for tests."}}
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

    mock_index = MagicMock()
    mock_store = MagicMock()
    q_inst = MagicMock()
    q_inst.get_collections.return_value = MagicMock()
    q_async = MagicMock()
    q_async.close = AsyncMock()
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

        svc = RAGService(cfg)
        try:

            async def aquery(
                _query: VectorStoreQuery,
                **kwargs: Any,
            ) -> VectorStoreQueryResult:
                return VectorStoreQueryResult(
                    nodes=[TextNode(id_="n1", text="t", metadata={"parent_id": "p"})]
                )

            svc._stores["kb"].aquery = aquery
            svc._stores["tickets"].aquery = aquery
            with patch.object(svc, "_ce", return_value=MagicMock()) as m_ce:
                m_ce.return_value.predict = MagicMock(
                    return_value=np.array([0.5], dtype=np.float32)
                )
                await svc.retrieve(
                    RetrievalRequest(
                        query="q",
                        top_k=2,
                        namespaces=["kb"],
                        rewrite=False,
                        rerank=True,
                    ),
                )
        finally:
            await svc.aclose()

    chat_reqs = [r for r in captured if "completions" in str(r.url.path)]
    assert len(chat_reqs) == 1
    assert chat_reqs[0].headers.get("X-Slot") == "r4-hyde-only"
