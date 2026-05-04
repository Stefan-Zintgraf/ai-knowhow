"""Contract: index/delete routes create OpenTelemetry spans (NFR-4)."""

from __future__ import annotations

import json
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.requests import Request
from starlette.testclient import TestClient


@contextmanager
def _mock_get_tracer():
    """In-process: assert span names without mutating the global TracerProvider."""
    mock_tracer = MagicMock()
    mock_cm = MagicMock()
    mock_tracer.start_as_current_span.return_value = mock_cm
    with patch("support_rag.app.trace.get_tracer", return_value=mock_tracer):
        yield mock_tracer


def test_index_and_delete_routes_create_spans(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "contract-test-service-token")
    monkeypatch.setenv("RAG_ADMIN_TOKEN", "contract-test-admin-token")

    fake = MagicMock()
    fake.index = AsyncMock()
    fake.delete = AsyncMock()
    fake.aclose = AsyncMock()

    with _mock_get_tracer() as mock_tracer, patch(
        "support_rag.app.RAGService", return_value=fake
    ):
        from support_rag.app import app, get_service

        def _override_s(request: Request):
            return fake

        app.dependency_overrides[get_service] = _override_s
        try:
            with TestClient(app) as client:
                r_i = client.post(
                    "/rag/index/kb",
                    json={"docs": [{"id": "d1", "text": "hello", "metadata": {}}]},
                    headers={"Authorization": "Bearer contract-test-admin-token"},
                )
                assert r_i.status_code == 200, r_i.text

                r_d = client.request(
                    "DELETE",
                    "/rag/index/kb",
                    content=json.dumps({"ids": ["d1"]}),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer contract-test-admin-token",
                    },
                )
                assert r_d.status_code == 200, r_d.text
        finally:
            app.dependency_overrides.clear()

    names = [c.args[0] for c in mock_tracer.start_as_current_span.call_args_list]
    assert "rag.index" in names
    assert "rag.delete" in names
