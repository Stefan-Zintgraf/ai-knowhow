"""NFR-6: two RAGService instances are separate objects (offline doubles)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from support_rag.config import AppConfig
from support_rag.service import RAGService


def _offline_rag() -> RAGService:
    mock_index = MagicMock()
    mock_store = MagicMock()
    q_inst = MagicMock()
    q_inst.get_collections.return_value = MagicMock()
    with (
        patch("support_rag.service.QdrantClient", return_value=q_inst),
        patch("support_rag.service.AsyncQdrantClient") as m_async,
        patch("support_rag.service.QdrantVectorStore", return_value=mock_store),
        patch(
            "support_rag.service.VectorStoreIndex.from_vector_store",
            return_value=mock_index,
        ),
    ):
        q_async = MagicMock()
        q_async.close = AsyncMock()
        m_async.return_value = q_async
        return RAGService(AppConfig())


@pytest.mark.asyncio
async def test_two_sequential_lifecycles_different_objects() -> None:
    a = _offline_rag()
    b = _offline_rag()
    try:
        assert a is not b
        assert a._qdrant is not b._qdrant
        assert a._indices is not b._indices
    finally:
        await a.aclose()
        await b.aclose()
