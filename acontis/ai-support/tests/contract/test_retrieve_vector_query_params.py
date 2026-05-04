"""Contract: R-2 — `VectorStoreQuery` carries config `top_k_*` and hybrid fusion fields."""

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
async def test_dense_query_matches_retrieval_config(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    r = svc._config.retrieval
    captured: list[VectorStoreQuery] = []

    async def capture_aquery(
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        captured.append(query)
        return VectorStoreQueryResult(nodes=[])

    svc._stores["kb"].aquery = capture_aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    await svc.retrieve(
        RetrievalRequest(
            query="test query",
            top_k=6,
            namespaces=["kb"],
            rewrite=False,
            rerank=False,
            hybrid=False,
        ),
    )
    assert len(captured) == 1
    vq = captured[0]
    assert vq.mode == VectorStoreQueryMode.DEFAULT
    assert vq.similarity_top_k == r.top_k_dense


@pytest.mark.asyncio
async def test_hybrid_query_matches_retrieval_config_rrf_leg(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    r = svc._config.retrieval
    captured: list[VectorStoreQuery] = []

    async def capture_aquery(
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        captured.append(query)
        return VectorStoreQueryResult(nodes=[])

    svc._stores["kb"].aquery = capture_aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    await svc.retrieve(
        RetrievalRequest(
            query="test query",
            top_k=6,
            namespaces=["kb"],
            rewrite=False,
            rerank=False,
            hybrid=True,
        )
    )
    vq = captured[0]
    assert vq.mode == VectorStoreQueryMode.HYBRID
    assert vq.similarity_top_k == r.top_k_dense
    assert vq.sparse_top_k == r.top_k_sparse
    assert vq.hybrid_top_k == r.top_k_dense + r.top_k_sparse
    assert vq.alpha == 0.5
    # RRF merge uses `r.rrf_k` in `service._rrf_k_lists` — config is wired on the service
    assert r.rrf_k == svc._config.retrieval.rrf_k
    assert r.fusion == "rrf"
