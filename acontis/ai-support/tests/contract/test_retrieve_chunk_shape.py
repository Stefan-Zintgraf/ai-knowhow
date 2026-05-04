"""Contract: R-6 — serialized chunk has `id`, `parent_id`, `score`, `metadata`."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import (
    VectorStoreQuery,
    VectorStoreQueryResult,
)

from support_rag.schemas import RetrievalRequest


@pytest.mark.asyncio
async def test_chunk_json_shape_non_rerank(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    node = TextNode(
        id_="chunk-99",
        text="hello world",
        metadata={"parent_id": "doc-1", "product": "x"},
    )

    async def aquery(
        _query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        return VectorStoreQueryResult(nodes=[node])

    svc._stores["kb"].aquery = aquery
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m"),
    )
    res, _ = await svc.retrieve(
        RetrievalRequest(
            query="q",
            top_k=6,
            namespaces=["kb"],
            rewrite=False,
            rerank=False,
        )
    )
    assert len(res.chunks) == 1
    c = res.chunks[0]
    assert c.id == "chunk-99"
    assert c.text == "hello world"
    assert c.parent_id == "doc-1"
    assert c.metadata.get("product") == "x"
    assert c.score is None
    dumped = c.model_dump()
    for key in ("id", "text", "parent_id", "metadata", "score"):
        assert key in dumped
