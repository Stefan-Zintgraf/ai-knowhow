"""Contract: `POST/DELETE /rag/index/{namespace}` — admin 200/400 and delete.

NFR-7 unauthorized: `test_protected_routes_401.py`.

Uses `starlette.testclient.TestClient` (same as `test_auth_health.py`) so FastAPI
`lifespan` runs. `httpx` 0.28’s `ASGITransport` is async-only and does not expose a
sync transport context compatible with `httpx.Client` + lifespan without extra
helpers (`asgi_lifespan`, `AsyncClient`).
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.requests import Request
from starlette.testclient import TestClient

_DOC = {
    "docs": [{"id": "doc-1", "text": "hello", "metadata": {}}],
}


@pytest.fixture
def admin_client(
    monkeypatch: pytest.MonkeyPatch,
) -> Any:
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "contract-test-service-token")
    monkeypatch.setenv("RAG_ADMIN_TOKEN", "contract-test-admin-token")
    fake_rag = MagicMock()
    fake_rag.aclose = AsyncMock()
    fake_rag.index = AsyncMock()
    fake_rag.delete = AsyncMock()
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


def test_post_index_200_admin_bearer_mocks(admin_client: Any) -> None:
    client, fake_rag = admin_client
    r = client.post(
        "/rag/index/kb",
        json=_DOC,
        headers={"Authorization": "Bearer contract-test-admin-token"},
    )
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
    fake_rag.index.assert_awaited_once()
    call = fake_rag.index.await_args
    assert call[0][0] == "kb"
    assert len(call[0][1]) == 1


def test_post_index_400_bad_namespace_with_admin(admin_client: Any) -> None:
    client, fake_rag = admin_client
    r = client.post(
        "/rag/index/bad",
        json=_DOC,
        headers={"Authorization": "Bearer contract-test-admin-token"},
    )
    assert r.status_code == 400
    fake_rag.index.assert_not_called()


def test_delete_index_200_admin_bearer_mocks(admin_client: Any) -> None:
    client, fake_rag = admin_client
    r1 = client.request(
        "DELETE",
        "/rag/index/kb",
        json={"ids": ["parent-a"]},
        headers={"Authorization": "Bearer contract-test-admin-token"},
    )
    assert r1.status_code == 200
    assert r1.json() == {"status": "ok"}
    fake_rag.delete.assert_awaited_once()
    del_call = fake_rag.delete.await_args
    assert del_call[0][0] == "kb"
    assert list(del_call[0][1]) == ["parent-a"]
