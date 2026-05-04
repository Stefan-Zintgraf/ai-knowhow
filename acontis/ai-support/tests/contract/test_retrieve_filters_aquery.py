"""Contract: R-5 — `RetrievalRequest.filters` reach `aquery` as `qdrant_filters`."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import (
    VectorStoreQuery,
    VectorStoreQueryResult,
)

from support_rag.qfilter import to_qdrant_filter
from support_rag.schemas import RetrievalRequest


@pytest.mark.asyncio
async def test_filters_passed_to_aquery(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    cap_filters: list[Any] = []

    async def capture_aquery(
        query: VectorStoreQuery,
        *,
        qdrant_filters: Any = None,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        cap_filters.append(qdrant_filters)
        return VectorStoreQueryResult(
            nodes=[TextNode(id_="n1", text="x", metadata={})],
        )

    svc._stores["kb"].aquery = capture_aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )

    flt: dict[str, Any] = {"product": "ecat"}
    req = RetrievalRequest(
        query="q",
        top_k=6,
        namespaces=["kb"],
        filters=flt,
        rewrite=False,
        rerank=False,
    )
    await svc.retrieve(req)
    assert len(cap_filters) == 1
    expect = to_qdrant_filter(flt)
    assert cap_filters[0] == expect
