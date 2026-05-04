"""Unit tests: AnythingLLM client (httpx transport mocks)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from support_rag.config import AnythingLlmConfig, AppConfig, WebUiState
from support_rag.anythingllm_client import resolve_workspace_effective
from support_rag.schemas import RetrievalRequest


def _transport_for_vector_search() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/api/v1/workspace/ws/vector-search" in str(request.url)
        _body = json.loads(request.content.decode())
        assert _body["query"] == "q1"
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "id": "c1",
                        "text": "hello",
                        "metadata": {
                            "title": "t.txt",
                        },
                        "score": 0.9,
                    }
                ],
            },
        )

    return httpx.MockTransport(handler)


def test_vector_search_maps_to_retrieval_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from support_rag import anythingllm_client as m

    alm = AnythingLlmConfig(
        base_url="http://127.0.0.1:9",
        api_key="k" * 12,
    )

    _RealClient = httpx.Client

    def fake_client(*_a: Any, **_kw: Any) -> httpx.Client:
        return _RealClient(
            transport=_transport_for_vector_search(), base_url="http://127.0.0.1:9"
        )

    monkeypatch.setattr(m.httpx, "Client", fake_client)
    req = RetrievalRequest(query="q1", top_k=3, filters={"x": 1})
    r = m.vector_search(alm, slug="ws", query="q1", top_n=4, req=req)
    assert r.chunks[0].text == "hello"
    assert r.chunks[0].parent_id == "t.txt"
    assert r.debug.get("filters_applied") is False
    assert r.debug.get("filters_ignored") is True
    assert r.debug.get("source") == "anything_llm"


def test_vector_search_no_filters_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    from support_rag import anythingllm_client as m

    alm = AnythingLlmConfig(base_url="http://x", api_key="k" * 9)

    _RealClient = httpx.Client

    def fake_client(*_a: Any, **_kw: Any) -> httpx.Client:
        return _RealClient(
            transport=_transport_for_vector_search(), base_url="http://x"
        )

    monkeypatch.setattr(m.httpx, "Client", fake_client)
    r = m.vector_search(alm, slug="ws", query="q1", req=None)
    assert len(r.chunks) == 1
    assert r.debug["filters_ignored"] is False


def test_workspace_chat_parses_text_response(monkeypatch: pytest.MonkeyPatch) -> None:
    from support_rag import anythingllm_client as m

    alm = AnythingLlmConfig(base_url="http://x", api_key="")

    def handler(request: httpx.Request) -> httpx.Response:
        assert b"mode" in request.content
        return httpx.Response(
            200,
            json={
                "textResponse": "ok",
                "type": "textResponse",
                "error": None,
            },
        )

    _RealClient = httpx.Client

    def fake_client(*_a: Any, **_kw: Any) -> httpx.Client:
        return _RealClient(
            transport=httpx.MockTransport(lambda r: handler(r)), base_url="http://x"
        )

    monkeypatch.setattr(m.httpx, "Client", fake_client)
    text, meta = m.workspace_chat(alm, slug="ws", message="hi")
    assert text == "ok"
    assert meta.get("alm_chat_mode")


def test_resolve_workspace_slug_lists_first_when_empty_or_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from support_rag import anythingllm_client as m

    alm = AnythingLlmConfig(
        base_url="http://127.0.0.1:9",
        api_key="k" * 12,
        workspace_slug="",
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert "/api/v1/workspaces" in str(request.url)
        return httpx.Response(
            200,
            json={"workspaces": [{"slug": "first-ws", "name": "First"}]},
        )

    _RealClient = httpx.Client

    def fake_client(*_a: Any, **_kw: Any) -> httpx.Client:
        return _RealClient(
            transport=httpx.MockTransport(lambda r: handler(r)),
            base_url="http://127.0.0.1:9",
        )

    monkeypatch.setattr(m.httpx, "Client", fake_client)
    assert m.resolve_workspace_slug(alm, override="", configured="") == "first-ws"
    assert m.resolve_workspace_slug(alm, override="", configured="default") == "first-ws"
    assert m.resolve_workspace_slug(alm, override="", configured="my-slug") == "my-slug"
    assert m.resolve_workspace_slug(alm, override="ovr", configured="x") == "ovr"


def test_format_alm_http_error_403() -> None:
    from support_rag.anythingllm_client import format_alm_http_error

    r = httpx.Request("GET", "http://x")
    resp = httpx.Response(403, request=r, text="nope")
    exc = httpx.HTTPStatusError("m", request=r, response=resp)
    s = format_alm_http_error(exc)
    assert "API key" in s or "403" in s


def test_ingest_idempotent_skips_same_hash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from support_rag.anythingllm_client import ingest_raw_text_idempotent

    state = tmp_path / "st.json"
    ac = AppConfig(
        anything_llm=AnythingLlmConfig(
            base_url="http://127.0.0.1:9", workspace_slug="ws", api_key=""
        ),
        web_ui=WebUiState(
            anythingllm_ingest_state_path=str(state),
        ),
    )
    n = 0

    def fake_raw(*_a: Any, **_k: Any) -> dict[str, Any]:
        nonlocal n
        n += 1
        return {
            "success": True,
            "documents": [
                {
                    "location": "custom-documents/x.json",
                }
            ],
        }

    def fake_update(*_a: Any, **_k: Any) -> dict[str, Any]:
        return {}

    monkeypatch.setattr("support_rag.anythingllm_client.raw_text_upload", fake_raw)
    monkeypatch.setattr("support_rag.anythingllm_client.update_embeddings", fake_update)
    a1 = ingest_raw_text_idempotent(
        ac, logical_key="k1", text="content", document_title="T"
    )
    assert a1.get("skipped") is False
    a2 = ingest_raw_text_idempotent(
        ac, logical_key="k1", text="content", document_title="T"
    )
    assert a2.get("skipped") is True
    assert n == 1


def test_resolve_workspace_effective_override_and_configured() -> None:
    s, r = resolve_workspace_effective("ovr", "cfg", ["a", "b"], list_failed=False)
    assert s == "ovr" and r == "override"
    s2, r2 = resolve_workspace_effective("", "my-ws", ["a"], list_failed=False)
    assert s2 == "my-ws" and r2 == "configured"
    s3, r3 = resolve_workspace_effective("", "default", ["first"], list_failed=False)
    assert s3 == "first" and r3 == "implicit_first"
    s4, r4 = resolve_workspace_effective("", "", ["first"], list_failed=False)
    assert s4 == "first" and r4 == "implicit_first"


def test_resolve_workspace_effective_none_when_empty_or_list_failed() -> None:
    s, r = resolve_workspace_effective("", "", [], list_failed=False)
    assert s == "" and r == "none"
    s2, r2 = resolve_workspace_effective("", "", ["x"], list_failed=True)
    assert s2 == "" and r2 == "none"


def test_alm_error_message_request_error() -> None:
    from support_rag.anythingllm_client import alm_error_message

    e = httpx.ConnectError("refused", request=httpx.Request("GET", "http://x"))
    s = alm_error_message(e)
    assert "unreachable" in s.lower() or "ConnectError" in s
