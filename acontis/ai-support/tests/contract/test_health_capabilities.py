"""Contract: `RAGService.health()` JSON shape matches MVP1 / PRD §2.8."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest


@pytest.mark.parametrize(
    "hybrid_rerank",
    [(True, True), (True, False), (False, True), (False, False)],
)
@pytest.mark.asyncio
async def test_health_capabilities_r14_matrix(
    rag_service_offline: Any, hybrid_rerank: tuple[bool, bool]
) -> None:
    """R-14: health flags track retrieval.hybrid and retrieval.rerank_enabled."""
    hybrid, rerank_enabled = hybrid_rerank
    svc = rag_service_offline
    svc._config.retrieval.hybrid = hybrid
    svc._config.retrieval.rerank_enabled = rerank_enabled
    svc._gateway.describe_models = AsyncMock(
        return_value={
            "embedding": "emb-contract",
            "retrieval_llm": "llm-contract",
            "chat": "chat-contract",
        }
    )
    body = await svc.health()
    assert body["status"] == "ok"
    assert body["contract_version"] == "1.0"
    cap = body["capabilities"]
    assert cap["hybrid"] is hybrid
    assert cap["rerank"] is rerank_enabled
    assert cap["graph"] is False


@pytest.mark.asyncio
async def test_health_capabilities_ok(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    svc._gateway.describe_models = AsyncMock(
        return_value={
            "embedding": "emb-contract",
            "retrieval_llm": "llm-contract",
            "chat": "chat-contract",
        }
    )
    body = await svc.health()
    assert body["status"] == "ok"
    assert body["contract_version"] == "1.0"
    cap = body["capabilities"]
    assert cap["hybrid"] is svc._config.retrieval.hybrid
    assert cap["rerank"] is svc._config.retrieval.rerank_enabled
    assert cap["graph"] is False
    assert cap["namespaces"] == ["kb", "tickets"]
    assert "models" in body
    assert body["models"]["embedding"] == "emb-contract"
    assert body["models"]["retrieval_llm"] == "llm-contract"
    assert body["models"]["chat"] == "chat-contract"
    assert body["models"]["reranker"] == svc._config.retrieval.reranker.model
    assert body["stores"]["qdrant"] == "ok"


@pytest.mark.asyncio
async def test_health_degraded_when_qdrant_raises(rag_service_offline: Any) -> None:
    svc = rag_service_offline
    svc._qdrant.get_collections.side_effect = ConnectionError("qdrant down")
    svc._gateway.describe_models = AsyncMock(
        return_value={"embedding": "e", "retrieval_llm": "r", "chat": "c"}
    )
    body = await svc.health()
    assert body["status"] == "degraded"
    assert body["stores"]["qdrant"] == "degraded"
    assert body["capabilities"]["namespaces"] == ["kb", "tickets"]
