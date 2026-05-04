"""R-12: re-index same parent_id triggers delete; distinct parents co-ingest in one batch."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from llama_index.core.schema import TextNode

from support_rag.schemas import IngestDocument
from support_rag.service import RAGService


@pytest.mark.asyncio
async def test_reingest_same_parent_id_calls_delete_each_time(
    app_config: Any, rag_service_offline: Any
) -> None:
    svc: RAGService = rag_service_offline
    idx = MagicMock()
    idx.ainsert_nodes = AsyncMock()
    svc._indices["kb"] = idx  # type: ignore[assignment]
    d1a = IngestDocument(
        id="parent-x",
        text="A. B. C. D. E. F. G. H. I. J. K. L. M. N. O. P. Q. R. S. T. U. V. W. X. Y. Z",
        metadata={},
    )
    d1b = IngestDocument(
        id="parent-x",
        text=(
            "A. B. C. D. E. F. G. H. I. J. K. L. M. N. O. P. Q. R. S. T. U. V. W. X. Y. Z. "
            "More."
        ),
        metadata={},
    )
    deleted: list[str] = []

    async def _del_one(_namespace: str, parent_id: str) -> None:
        deleted.append(parent_id)

    vlen = app_config.qdrant.vector_size
    svc._gateway.embed_sync = MagicMock(
        return_value=([[0.0] * vlen], "m1")
    )
    with patch.object(svc, "_delete_one", new=AsyncMock(side_effect=_del_one)):
        await svc.index("kb", [d1a], trace_ctx={})
        await svc.index("kb", [d1b], trace_ctx={})
    assert deleted == ["parent-x", "parent-x"]
    assert idx.ainsert_nodes.await_count == 2


@pytest.mark.asyncio
async def test_two_distinct_parent_ids_both_indexed(
    app_config: Any, rag_service_offline: Any
) -> None:
    svc: RAGService = rag_service_offline
    idx = MagicMock()
    idx.ainsert_nodes = AsyncMock()
    svc._indices["kb"] = idx  # type: ignore[assignment]
    a = IngestDocument(
        id="a1",
        text="A. B. C. D. E. F. G. H. I. J. K. L. M. N. O. P. Q. R. S. T. U. V. W. X. Y. Z",
        metadata={},
    )
    b = IngestDocument(
        id="b1",
        text="A. B. C. D. E. F. G. H. I. J. K. L. M. N. O. P. Q. R. S. T. U. V. W. X. Y. Z",
        metadata={},
    )
    deleted: list[str] = []

    async def _del_two(_namespace: str, parent_id: str) -> None:
        deleted.append(parent_id)

    vlen = app_config.qdrant.vector_size
    svc._gateway.embed_sync = MagicMock(
        return_value=([[0.0] * vlen], "m1")
    )
    with patch.object(svc, "_delete_one", new=AsyncMock(side_effect=_del_two)):
        await svc.index("kb", [a, b], trace_ctx={})
    assert set(deleted) == {"a1", "b1"}
    assert len(deleted) == 2
    assert idx.ainsert_nodes.await_count == 1
    all_nodes: list[TextNode] = []
    for call in idx.ainsert_nodes.await_args_list:
        all_nodes.extend(call[0][0])
    parent_ids = {n.metadata.get("parent_id") for n in all_nodes if n.metadata}
    assert "a1" in parent_ids and "b1" in parent_ids
