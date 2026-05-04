"""RAGService: delete for `parent_id` then retrieve excludes it (PRD §2.8 #4) — offline doubles."""

from __future__ import annotations

import types
from typing import Any
from unittest.mock import AsyncMock

import pytest
from llama_index.core.schema import TextNode
from qdrant_client import models as qmodels

from support_rag.schemas import RetrievalRequest
from support_rag.service import RAGService


def _text_node() -> TextNode:
    n = TextNode(
        id_="n1",
        text="chunk body",
    )
    n.metadata = {"parent_id": "p-erase-1", "ref_doc_id": "p-erase-1"}
    return n


@pytest.mark.asyncio
async def test_delete_then_retrieve_excludes_parent(rag_service_offline: Any) -> None:
    svc: RAGService = rag_service_offline
    state: dict[str, bool] = {"erased": False}
    delete_spy: list[tuple[str, str]] = []

    async def fake_q_one(
        self: RAGService,
        namespace: str,
        _q: str,
        _qv: list[float] | None,
        _qf: qmodels.Filter | None,
        *,
        use_hybrid: bool,
    ) -> list[TextNode]:
        assert namespace == "kb"
        if state["erased"]:
            return []
        return [_text_node()]

    async def fake_delete_one(
        self: RAGService, namespace: str, parent_id: str
    ) -> None:
        delete_spy.append((namespace, parent_id))
        if parent_id == "p-erase-1":
            state["erased"] = True

    svc._query_one = types.MethodType(fake_q_one, svc)  # type: ignore[method-assign]
    svc._delete_one = types.MethodType(fake_delete_one, svc)  # type: ignore[method-assign]
    svc._gateway.embed = AsyncMock(
        return_value=([[0.0] * svc._config.qdrant.vector_size], "m")
    )
    ret_pre = await svc.retrieve(
        RetrievalRequest(
            query="q",
            top_k=3,
            namespaces=["kb"],
            rewrite=False,
            rerank=False,
            hybrid=False,
        )
    )
    assert [c.parent_id for c in ret_pre[0].chunks] == ["p-erase-1"]

    await svc.delete("kb", ["p-erase-1"], trace_ctx={})
    assert delete_spy == [("kb", "p-erase-1")]

    ret_post = await svc.retrieve(
        RetrievalRequest(
            query="q",
            top_k=3,
            namespaces=["kb"],
            rewrite=False,
            rerank=False,
            hybrid=False,
        )
    )
    assert ret_post[0].chunks == []
