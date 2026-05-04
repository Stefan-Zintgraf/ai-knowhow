"""
R-19 / R-20: MCP tool callables use the same REST paths and bearer rules as the HTTP API.

In-process with httpx.MockTransport (no stdio, no live RAG). Asserts `Authorization`
and URL/method; negative path for `rag.index` when `RAG_ADMIN_TOKEN` is unset.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import Iterator
from unittest.mock import patch

import httpx
import pytest

_httpx_AsyncClient = httpx.AsyncClient


@contextlib.contextmanager
def _patch_mcp_httpx(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[list[httpx.Request]]:
    """Force `RAG_MCP_BASE_URL` and valid tokens; capture MCP HTTP to MockTransport."""
    monkeypatch.setenv("RAG_MCP_BASE_URL", "http://mcp-binding.test:9")
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "test-service-bearer")
    monkeypatch.setenv("RAG_ADMIN_TOKEN", "test-admin-bearer")
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        p = request.url.path
        if p.rstrip("/").endswith("/rag/health"):
            return httpx.Response(200, json={"ok": True})
        if p.rstrip("/").endswith("/rag/retrieve"):
            return httpx.Response(
                200,
                text='{"chunks":[]}',
                headers={"content-type": "application/json"},
            )
        if "/rag/index/" in p:
            return httpx.Response(200, text="{}", headers={"content-type": "application/json"})
        return httpx.Response(404, json={"error": f"unexpected path {p}"})

    transport = httpx.MockTransport(handler)

    def async_client(*args: object, **kwargs: object) -> httpx.AsyncClient:
        k = dict(kwargs)
        k["transport"] = transport
        return _httpx_AsyncClient(*args, **k)  # type: ignore[misc,arg-type]

    with patch("support_rag.mcp_server.httpx.AsyncClient", side_effect=async_client):
        yield captured


def _bearer(h: httpx.Headers) -> str:
    a = h.get("Authorization", "")
    assert a.startswith("Bearer ")
    return a.removeprefix("Bearer ")


def test_rag_health_gets_with_service_bearer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import support_rag.mcp_server as m

    with _patch_mcp_httpx(monkeypatch) as captured:

        async def _run() -> str:
            return await m.rag_health()

        out = asyncio.run(_run())
    assert len(captured) == 1
    req = captured[0]
    assert req.method == "GET"
    assert str(req.url).rstrip("/").endswith("/rag/health")
    assert _bearer(req.headers) == "test-service-bearer"
    assert json.loads(out)["ok"] is True


@pytest.mark.parametrize("namespace", ("kb", "tickets"))
def test_rag_retrieve_posts_json_with_service_bearer(
    monkeypatch: pytest.MonkeyPatch,
    namespace: str,
) -> None:
    import support_rag.mcp_server as m

    with _patch_mcp_httpx(monkeypatch) as captured:

        async def _run() -> str:
            return await m.rag_retrieve(
                "hello",
                top_k=4,
                namespaces=[namespace],
                rewrite=False,
                rerank=True,
                min_score=0.1,
            )

        asyncio.run(_run())
    assert len(captured) == 1
    req = captured[0]
    assert req.method == "POST"
    assert str(req.url).rstrip("/").endswith("/rag/retrieve")
    assert _bearer(req.headers) == "test-service-bearer"
    assert req.headers.get("content-type", "").startswith("application/json")
    body = json.loads(req.content)
    assert body["query"] == "hello"
    assert body["top_k"] == 4
    assert body["namespaces"] == [namespace]
    assert body["rewrite"] is False
    assert body["rerank"] is True
    assert body["min_score"] == 0.1
    assert body.get("filters") is None


def test_rag_index_posts_with_admin_bearer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import support_rag.mcp_server as m

    with _patch_mcp_httpx(monkeypatch) as captured:
        docs = json.dumps([{"id": "a1", "text": "t"}])

        async def _run() -> str:
            return await m.rag_index("ns1", docs)

        asyncio.run(_run())
    assert len(captured) == 1
    req = captured[0]
    assert req.method == "POST"
    assert str(req.url).rstrip("/").endswith("/rag/index/ns1")
    assert _bearer(req.headers) == "test-admin-bearer"
    posted = json.loads(req.content) if req.content else {}
    assert posted["docs"] == [{"id": "a1", "text": "t"}]


def test_rag_index_missing_admin_token_raises_no_success_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    R-20: with only a service token configured, `rag_index` must not send an admin
    request. Current `mcp_server._h(service=False)` raises at header build time.
    """
    import support_rag.mcp_server as m

    monkeypatch.setenv("RAG_MCP_BASE_URL", "http://mcp-binding.test:9")
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "only-service")
    monkeypatch.delenv("RAG_ADMIN_TOKEN", raising=False)
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        captured.append(request)
        return httpx.Response(200, text="no")

    def async_client(*args: object, **kwargs: object) -> httpx.AsyncClient:
        k = dict(kwargs)
        k["transport"] = httpx.MockTransport(handler)
        return _httpx_AsyncClient(*args, **k)  # type: ignore[misc,arg-type]

    with patch("support_rag.mcp_server.httpx.AsyncClient", side_effect=async_client):
        with pytest.raises(RuntimeError, match="Set RAG_ADMIN_TOKEN"):
            asyncio.run(
                m.rag_index("ns1", json.dumps([{"id": "x", "text": "y"}])),
            )
    assert captured == []
