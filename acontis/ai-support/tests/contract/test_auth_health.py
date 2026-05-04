"""Contract: `GET /rag/health` — 200 + JSON with valid service bearer.

401 matrix: `test_protected_routes_401.py`."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.requests import Request
from starlette.testclient import TestClient


class _FakeRAGForHealth:
    async def health(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "version": "0.0.0-test",
            "contract_version": "1.0",
            "capabilities": {
                "hybrid": True,
                "rerank": True,
                "graph": False,
                "namespaces": ["kb", "tickets"],
            },
            "models": {
                "embedding": "mock",
                "retrieval_llm": "mock",
                "chat": "mock",
                "reranker": "mock",
            },
            "stores": {"qdrant": "ok"},
        }


def test_rag_health_auth_bearer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "contract-test-service-token")
    monkeypatch.setenv("RAG_ADMIN_TOKEN", "contract-test-admin-token")

    fake_startup_rag = MagicMock()
    fake_startup_rag.aclose = AsyncMock()

    with patch("support_rag.app.RAGService", return_value=fake_startup_rag):
        from support_rag.app import app, get_service

        def _override_get_service(_request: Request) -> Any:
            return _FakeRAGForHealth()

        app.dependency_overrides[get_service] = _override_get_service
        try:
            with TestClient(app) as client:
                r2 = client.get(
                    "/rag/health",
                    headers={"Authorization": "Bearer contract-test-service-token"},
                )
                assert r2.status_code == 200
                data = r2.json()
                assert data.get("contract_version") == "1.0"
                assert "capabilities" in data
                assert data["capabilities"]["graph"] is False
        finally:
            app.dependency_overrides.clear()
