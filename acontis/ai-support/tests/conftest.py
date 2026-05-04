"""Shared pytest configuration — markers, skips, and offline RAG fixtures."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

_RUN_INTEGRATION = os.environ.get("RUN_INTEGRATION", "").lower() in ("1", "true", "yes")
_RUN_E2E_PRIVACY = os.environ.get("RUN_E2E_PRIVACY", "").lower() in ("1", "true", "yes")
_RUN_NFR6_COMPOSE = os.environ.get("RUN_NFR6_COMPOSE", "").lower() in ("1", "true", "yes")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    skip_int = pytest.mark.skip(
        reason="set RUN_INTEGRATION=1 to run integration / requires_services tests",
    )
    skip_e2e = pytest.mark.skip(
        reason="set RUN_E2E_PRIVACY=1 for e2e_privacy; see runbook allow-remote-false-e2e",
    )
    skip_nfr6 = pytest.mark.skip(
        reason="set RUN_INTEGRATION=1 and RUN_NFR6_COMPOSE=1; see README (NFR-6 compose restart)",
    )
    for item in items:
        marks = {m.name for m in item.iter_markers()}
        if ("integration" in marks or "requires_services" in marks) and not _RUN_INTEGRATION:
            item.add_marker(skip_int)
        if "e2e_privacy" in marks and not _RUN_E2E_PRIVACY:
            item.add_marker(skip_e2e)
        if "nfr6_compose" in marks and (not _RUN_INTEGRATION or not _RUN_NFR6_COMPOSE):
            item.add_marker(skip_nfr6)


@pytest.fixture
def app_config() -> Any:
    from support_rag.config import AppConfig

    return AppConfig()


@pytest.fixture
def rag_service_offline(app_config: Any) -> Iterator[Any]:
    """`RAGService` with Qdrant / index construction mocked — no live services."""
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
        from support_rag.service import RAGService

        svc = RAGService(app_config)
        try:
            yield svc
        finally:
            asyncio.run(svc.aclose())
