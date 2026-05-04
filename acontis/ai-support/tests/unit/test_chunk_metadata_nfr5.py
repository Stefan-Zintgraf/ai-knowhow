"""NFR-5: chunker_version and embedding model id on chunk metadata after index()."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from support_rag.chunking import chunk_kb, chunk_tickets
from support_rag.config import AppConfig
from support_rag.schemas import IngestDocument
from support_rag.service import RAGService


def test_chunk_kb_and_tickets_metadata_include_chunker_version() -> None:
    cfg = AppConfig()
    d_kb = IngestDocument(
        id="p1",
        text="One. Two. Three. Four. Five. Six. Seven. Eight. Nine. Ten",
        metadata={},
    )
    for n in chunk_kb(cfg, d_kb, "kb"):
        assert n.metadata is not None
        assert n.metadata.get("chunker_version") == cfg.chunker_version.kb
        assert n.metadata.get("parent_id") == "p1"
    d_t = IngestDocument(
        id="t1",
        text="",
        metadata={"qa_pairs": [{"question": "Q?", "resolution": "A!"}]},
    )
    for n in chunk_tickets(cfg, d_t, "tickets"):
        assert n.metadata is not None
        assert n.metadata.get("chunker_version") == cfg.chunker_version.tickets


@pytest.mark.asyncio
async def test_index_stamps_embedding_model_on_all_nodes(
    app_config: AppConfig, rag_service_offline: Any
) -> None:
    """RAGService.index stamps `embedding_model` from the gateway (first text batch)."""
    svc: RAGService = rag_service_offline
    long_text = " ".join(
        f"{c}." for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c
    )  # enough sentences for >1 kb chunk
    doc = IngestDocument(id="d1", text=long_text, metadata={})
    idx = MagicMock()
    ainsert = AsyncMock()
    idx.ainsert_nodes = ainsert
    idx.as_query_engine = MagicMock()
    idx.as_retriever = MagicMock()
    svc._indices["kb"] = idx  # type: ignore[assignment]
    embed_model = "gateway-model-xyz"
    svc._gateway.embed_sync = MagicMock(
        return_value=([[0.0] * app_config.qdrant.vector_size], embed_model)
    )
    with patch.object(svc, "_delete_one", new=AsyncMock()):
        await svc.index("kb", [doc], trace_ctx={})
    ainsert.assert_awaited()
    first_batch = ainsert.await_args[0][0]
    assert len(first_batch) >= 1
    for n in first_batch:
        assert n.metadata is not None
        assert n.metadata.get("chunker_version") == app_config.chunker_version.kb
        assert n.metadata.get("embedding_model") == embed_model
