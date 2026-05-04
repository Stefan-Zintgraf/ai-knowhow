"""Contract: R-3 — `rerank=True` invokes cross-encoder; `rerank=False` skips it.

Rerank **ordering** (when `rerank=True`): the service normalizes each raw cross-encoder
score with a logistic sigmoid ``norm = 1 / (1 + exp(-raw))`` (see `support_rag.service`
`retrieve`), then sorts candidate chunks by ``norm`` **descending**. Ties are resolved by
Python's stable sort; tests use scores with strict ordering.
"""

from __future__ import annotations

import math
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
async def test_rerank_true_invokes_predict(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    n1 = TextNode(id_="n1", text="body1", metadata={"parent_id": "p"})

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
    ce.predict = MagicMock(return_value=np.array([1.0], dtype=np.float32))

    with patch.object(svc, "_ce", return_value=ce) as p_ce:
        await svc.retrieve(
            RetrievalRequest(
                query="q",
                top_k=6,
                namespaces=["kb"],
                rewrite=False,
                rerank=True,
            )
        )
    p_ce.assert_called()
    ce.predict.assert_called_once()


@pytest.mark.asyncio
async def test_rerank_false_skips_cross_encoder(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    n1 = TextNode(id_="n1", text="body1", metadata={"parent_id": "p"})

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
    ce.predict = MagicMock()

    with patch.object(svc, "_ce", return_value=ce) as p_ce:
        await svc.retrieve(
            RetrievalRequest(
                query="q",
                top_k=6,
                namespaces=["kb"],
                rewrite=False,
                rerank=False,
            )
        )
    p_ce.assert_not_called()
    ce.predict.assert_not_called()


@pytest.mark.asyncio
async def test_rerank_orders_chunks_by_sigmoid_scores_r3(rag_service_offline: Any) -> None:
    """Fixed `predict` raw scores -> chunk order = sort key sigmoid(raw), descending."""
    svc = rag_service_offline
    n1 = TextNode(id_="n1", text="body-one", metadata={"parent_id": "p"})
    n2 = TextNode(id_="n2", text="body-two", metadata={"parent_id": "p"})
    n3 = TextNode(id_="n3", text="body-three", metadata={"parent_id": "p"})

    async def aquery(
        _query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        return VectorStoreQueryResult(nodes=[n1, n2, n3])

    svc._stores["kb"].aquery = aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    # Pairs are (q, content) in merged order: n1, n2, n3
    raw = np.array([1.0, 2.0, 0.0], dtype=np.float32)
    ce = MagicMock()
    ce.predict = MagicMock(return_value=raw)

    def sig(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))

    with patch.object(svc, "_ce", return_value=ce):
        res, _ = await svc.retrieve(
            RetrievalRequest(
                query="q",
                top_k=3,
                namespaces=["kb"],
                rewrite=False,
                rerank=True,
            )
        )
    # Order by sig(raw): 2.0 > 1.0 > 0.0 -> n2, n1, n3
    assert [c.id for c in res.chunks] == ["n2", "n1", "n3"]
    assert [round(c.score or 0.0, 6) for c in res.chunks] == [
        round(sig(2.0), 6),
        round(sig(1.0), 6),
        round(sig(0.0), 6),
    ]


@pytest.mark.asyncio
async def test_rerank_min_score_filters_after_sigmoid_r3(rag_service_offline: Any) -> None:
    """When `min_score` is set, chunks below the sigmoid threshold are dropped."""
    svc = rag_service_offline
    n1 = TextNode(id_="n1", text="a", metadata={"parent_id": "p"})
    n2 = TextNode(id_="n2", text="b", metadata={"parent_id": "p"})

    async def aquery(
        _query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        return VectorStoreQueryResult(nodes=[n1, n2])

    svc._stores["kb"].aquery = aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    # Raw scores align with merged node order (n1, n2): n1 wins after rerank
    raw = np.array([2.0, 0.0], dtype=np.float32)
    ce = MagicMock()
    ce.predict = MagicMock(return_value=raw)

    def sig(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))

    s_hi, s_lo = sig(2.0), sig(0.0)
    mid = (s_hi + s_lo) / 2.0

    with patch.object(svc, "_ce", return_value=ce):
        res, _ = await svc.retrieve(
            RetrievalRequest(
                query="q",
                top_k=2,
                namespaces=["kb"],
                rewrite=False,
                rerank=True,
                min_score=mid,
            )
        )
    # Only the higher normalized score survives
    assert len(res.chunks) == 1
    assert res.chunks[0].id == "n1"
    assert res.chunks[0].score is not None
    assert res.chunks[0].score == pytest.approx(s_hi)
