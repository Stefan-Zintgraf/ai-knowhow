"""Contract: `POST /rag/retrieve` — valid bearer + JSON body shape (R-1).

401: `test_protected_routes_401.py`."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.requests import Request
from starlette.testclient import TestClient

from support_rag.schemas import ChunkResult, RetrievalResponse


def _ok_response() -> RetrievalResponse:
    return RetrievalResponse(
        chunks=[
            ChunkResult(
                id="c1",
                text="t",
                metadata={"k": 1},
                parent_id="p1",
                score=0.5,
            )
        ],
        rewritten_queries=[],
        debug={"hybrid": True},
    )


@pytest.fixture
def retrieve_client(
    monkeypatch: pytest.MonkeyPatch,
) -> Any:
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "contract-test-service-token")
    monkeypatch.setenv("RAG_ADMIN_TOKEN", "contract-test-admin-token")
    fake_rag = MagicMock()
    fake_rag.aclose = AsyncMock()
    fake_rag.retrieve = AsyncMock(
        return_value=(_ok_response(), 0.01),
    )
    with patch("support_rag.app.RAGService", return_value=fake_rag):
        from support_rag.app import app, get_service

        def _override_get_service(_request: Request) -> Any:
            return fake_rag

        app.dependency_overrides[get_service] = _override_get_service
        try:
            with TestClient(app) as client:
                yield client, fake_rag
        finally:
            app.dependency_overrides.clear()


def test_post_retrieve_200_shape(retrieve_client: Any) -> None:
    client, fake_rag = retrieve_client
    r = client.post(
        "/rag/retrieve",
        json={"query": "hello", "top_k": 2},
        headers={"Authorization": "Bearer contract-test-service-token"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "chunks" in data
    assert "rewritten_queries" in data
    assert "debug" in data
    assert len(data["chunks"]) == 1
    ch0 = data["chunks"][0]
    for key in ("id", "text", "metadata", "parent_id", "score"):
        assert key in ch0
    fake_rag.retrieve.assert_awaited_once()
