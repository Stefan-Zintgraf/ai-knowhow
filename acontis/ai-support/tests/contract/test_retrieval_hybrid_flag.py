"""Contract: per-request hybrid flag selects HYBRID vs DEFAULT vector query mode."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest
from llama_index.core.vector_stores.types import (
    VectorStoreQuery,
    VectorStoreQueryMode,
    VectorStoreQueryResult,
)

from support_rag.schemas import RetrievalRequest


@pytest.mark.asyncio
async def test_retrieve_dense_uses_default_mode(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    captured: list[VectorStoreQuery] = []

    async def capture_aquery(
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        captured.append(query)
        return VectorStoreQueryResult(nodes=[])

    svc._stores["kb"].aquery = capture_aquery
    svc._gateway.embed = AsyncMock(return_value=([ [0.0] * svc._config.qdrant.vector_size ], "m"))

    req = RetrievalRequest(
        query="test query",
        top_k=6,
        namespaces=["kb"],
        rewrite=False,
        rerank=False,
        hybrid=False,
    )
    await svc.retrieve(req)
    assert len(captured) == 1
    assert captured[0].mode == VectorStoreQueryMode.DEFAULT
    assert captured[0].similarity_top_k == svc._config.retrieval.top_k_dense


@pytest.mark.asyncio
async def test_retrieve_hybrid_uses_hybrid_mode(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    captured: list[VectorStoreQuery] = []

    async def capture_aquery(
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        captured.append(query)
        return VectorStoreQueryResult(nodes=[])

    svc._stores["kb"].aquery = capture_aquery
    svc._gateway.embed = AsyncMock(return_value=([ [0.0] * svc._config.qdrant.vector_size ], "m"))

    req = RetrievalRequest(
        query="test query",
        top_k=6,
        namespaces=["kb"],
        rewrite=False,
        rerank=False,
        hybrid=True,
    )
    await svc.retrieve(req)
    assert len(captured) == 1
    assert captured[0].mode == VectorStoreQueryMode.HYBRID


@pytest.mark.asyncio
async def test_retrieve_hybrid_none_follows_config(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    captured: list[VectorStoreQuery] = []

    async def capture_aquery(
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        captured.append(query)
        return VectorStoreQueryResult(nodes=[])

    svc._stores["kb"].aquery = capture_aquery
    svc._gateway.embed = AsyncMock(return_value=([ [0.0] * svc._config.qdrant.vector_size ], "m"))

    svc._config.retrieval.hybrid = False
    req = RetrievalRequest(
        query="q",
        top_k=6,
        namespaces=["kb"],
        rewrite=False,
        rerank=False,
        hybrid=None,
    )
    await svc.retrieve(req)
    assert captured[0].mode == VectorStoreQueryMode.DEFAULT

    captured.clear()
    svc._config.retrieval.hybrid = True
    await svc.retrieve(req)
    assert captured[0].mode == VectorStoreQueryMode.HYBRID
