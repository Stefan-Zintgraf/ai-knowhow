"""R-8: POST /rag/index returns 422 for malformed IndexRequest bodies (no Qdrant)."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.requests import Request
from starlette.testclient import TestClient


@pytest.fixture
def admin_client(
    monkeypatch: pytest.MonkeyPatch,
) -> Any:
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "contract-test-service-token")
    monkeypatch.setenv("RAG_ADMIN_TOKEN", "contract-test-admin-token")
    fake_rag = MagicMock()
    fake_rag.aclose = AsyncMock()
    fake_rag.index = AsyncMock()
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


def _admin_headers() -> dict[str, str]:
    return {"Authorization": "Bearer contract-test-admin-token"}


def test_index_422_docs_not_list(admin_client: Any) -> None:
    client, fake_rag = admin_client
    r = client.post(
        "/rag/index/kb",
        json={"docs": "not-a-list"},
        headers=_admin_headers(),
    )
    assert r.status_code == 422
    fake_rag.index.assert_not_called()


def test_index_422_doc_missing_id(admin_client: Any) -> None:
    client, fake_rag = admin_client
    r = client.post(
        "/rag/index/kb",
        json={"docs": [{"text": "hello", "metadata": {}}]},
        headers=_admin_headers(),
    )
    assert r.status_code == 422
    fake_rag.index.assert_not_called()


def test_index_422_doc_missing_text(admin_client: Any) -> None:
    client, fake_rag = admin_client
    r = client.post(
        "/rag/index/kb",
        json={"docs": [{"id": "a", "metadata": {}}]},
        headers=_admin_headers(),
    )
    assert r.status_code == 422
    fake_rag.index.assert_not_called()


def test_index_422_wrong_metadata_type(admin_client: Any) -> None:
    client, fake_rag = admin_client
    r = client.post(
        "/rag/index/kb",
        json={"docs": [{"id": "a", "text": "x", "metadata": "not-obj"}]},
        headers=_admin_headers(),
    )
    assert r.status_code == 422
    fake_rag.index.assert_not_called()


def test_index_200_empty_docs_allowed(admin_client: Any) -> None:
    """Empty list is valid Pydantic; service no-ops (R-8 is invalid shapes, not empty batch)."""
    client, fake_rag = admin_client
    r = client.post(
        "/rag/index/kb",
        json={"docs": []},
        headers=_admin_headers(),
    )
    assert r.status_code == 200
    fake_rag.index.assert_awaited_once()
