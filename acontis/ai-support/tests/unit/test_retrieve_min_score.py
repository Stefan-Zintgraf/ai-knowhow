"""Unit: R-7 — `min_score` filters reranked chunks; empty response valid."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pytest
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import (
    VectorStoreQuery,
    VectorStoreQueryResult,
)

from support_rag.schemas import RetrievalRequest


@pytest.mark.asyncio
async def test_min_score_excludes_low_rerank_scores(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    n1 = TextNode(id_="n1", text="a", metadata={"parent_id": "p1"})
    n2 = TextNode(id_="n2", text="b", metadata={"parent_id": "p1"})

    async def aquery(
        _query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        return VectorStoreQueryResult(nodes=[n1, n2])

    svc._stores["kb"].aquery = aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    ce = MagicMock()
    ce.predict = MagicMock(
        return_value=np.array([-8.0, 8.0], dtype=np.float32),
    )
    with patch.object(svc, "_ce", return_value=ce):
        req = RetrievalRequest(
            query="q",
            top_k=6,
            namespaces=["kb"],
            rewrite=False,
            rerank=True,
            min_score=0.5,
        )
        res, _ = await svc.retrieve(req)
    # Lower sigmoid score dropped
    assert len(res.chunks) == 1
    assert res.chunks[0].id == "n2"

    with patch.object(svc, "_ce", return_value=ce):
        req2 = RetrievalRequest(
            query="q",
            top_k=6,
            namespaces=["kb"],
            rewrite=False,
            rerank=True,
            min_score=0.99999,
        )
        res2, _ = await svc.retrieve(req2)
    assert res2.chunks == []


@pytest.mark.asyncio
async def test_all_chunks_dropped_still_200_in_service(rag_service_offline: Any) -> None:
    """Empty chunk list is valid (early exit path not used when merged non-empty but filtered)."""
    svc = rag_service_offline
    n1 = TextNode(id_="n1", text="a", metadata={})
    async def aquery(
        _query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        return VectorStoreQueryResult(nodes=[n1])

    svc._stores["kb"].aquery = aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    ce = MagicMock()
    ce.predict = MagicMock(return_value=np.array([-5.0], dtype=np.float32))
    with patch.object(svc, "_ce", return_value=ce):
        res, _ = await svc.retrieve(
            RetrievalRequest(
                query="q",
                top_k=6,
                namespaces=["kb"],
                rewrite=False,
                rerank=True,
                min_score=0.99,
            )
        )
    assert res.chunks == []
