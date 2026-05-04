"""Contract: chunking produces identical node ids for the same ingest document (R-10)."""

from __future__ import annotations

from support_rag.chunking import chunk_kb, chunk_tickets
from support_rag.config import AppConfig
from support_rag.schemas import IngestDocument


def test_chunk_kb_ids_stable_across_runs() -> None:
    cfg = AppConfig()
    doc = IngestDocument(
        id="parent-1",
        text="First sentence. Second sentence. Third sentence here.",
        metadata={"source_uri": "https://example.com/a"},
    )
    ids_a = [n.id_ for n in chunk_kb(cfg, doc, "kb")]
    ids_b = [n.id_ for n in chunk_kb(cfg, doc, "kb")]
    assert ids_a == ids_b
    assert len(ids_a) >= 1


def test_chunk_tickets_qa_ids_stable_across_runs() -> None:
    cfg = AppConfig()
    doc = IngestDocument(
        id="ticket-42",
        text="",
        metadata={
            "qa_pairs": [
                {"question": "Why?", "resolution": "Because."},
            ]
        },
    )
    ids_a = [n.id_ for n in chunk_tickets(cfg, doc, "tickets")]
    ids_b = [n.id_ for n in chunk_tickets(cfg, doc, "tickets")]
    assert ids_a == ids_b
    assert len(ids_a) >= 1
