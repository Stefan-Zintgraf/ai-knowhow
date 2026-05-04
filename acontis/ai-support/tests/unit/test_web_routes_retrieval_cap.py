"""Unit tests: _cap_retrieval_payload (ui_chat include_retrieval + size caps)."""

from __future__ import annotations

import pytest

from support_rag.schemas import ChunkResult, RetrievalResponse
from support_rag.web_routes import _cap_retrieval_payload


def test_cap_retrieval_truncates_text_by_char_cap() -> None:
    long = "x" * 100
    r = RetrievalResponse(
        chunks=[
            ChunkResult(
                id="1",
                text=long,
                metadata={},
                parent_id="p",
                score=0.5,
            )
        ],
        rewritten_queries=[],
        debug={"source": "anything_llm"},
    )
    out, truncated = _cap_retrieval_payload(
        r, char_cap=50, max_chunks=20
    )
    assert truncated is True
    assert "…[truncated]" in out["chunks"][0]["text"]
    assert len(out["chunks"][0]["text"]) < len(long) + 20
    assert out["debug"]["source"] == "anything_llm"


def test_cap_retrieval_limits_chunk_count() -> None:
    chunks = [
        ChunkResult(
            id=str(i),
            text="a",
            metadata={},
            parent_id="p",
            score=0.1,
        )
        for i in range(30)
    ]
    r = RetrievalResponse(
        chunks=chunks,
        rewritten_queries=["q1"],
        debug={},
    )
    out, truncated = _cap_retrieval_payload(
        r, char_cap=10_000, max_chunks=5
    )
    assert truncated is True
    assert len(out["chunks"]) == 5
    assert out["rewritten_queries"] == ["q1"]


def test_vector_search_uses_metadata_doc_source_for_parent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import httpx

    from support_rag import anythingllm_client as m
    from support_rag.config import AnythingLlmConfig
    from support_rag.schemas import RetrievalRequest

    alm = AnythingLlmConfig(
        base_url="http://127.0.0.1:9",
        api_key="k" * 12,
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "id": "c1",
                        "text": "body",
                        "metadata": {"docSource": "from-docSource"},
                        "score": 0.5,
                    }
                ],
            },
        )

    _Real = httpx.Client

    def fake_client(*_a: object, **_kw: object) -> httpx.Client:
        return _Real(
            transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:9"
        )

    monkeypatch.setattr(m.httpx, "Client", fake_client)
    r = m.vector_search(alm, slug="ws", query="q", req=RetrievalRequest(query="q"))
    assert r.chunks[0].parent_id == "from-docSource"
