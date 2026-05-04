"""Offline tests for `scripts/retrieve_to_file.py` (mocked httpx)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest


def _load_retrieve() -> object:
    root = Path(__file__).resolve().parents[2]
    path = root / "scripts" / "retrieve_to_file.py"
    spec = importlib.util.spec_from_file_location("retrieve_to_file_cli", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


rt = _load_retrieve()


def test_build_request_body_defaults() -> None:
    b = rt.build_request_body(
        query="q",
        top_k=3,
        namespaces=None,
        filters=None,
        rewrite=True,
        rerank=True,
        min_score=None,
        hybrid=None,
    )
    assert b["query"] == "q" and b["top_k"] == 3
    assert "namespaces" not in b


def test_build_request_body_with_filters() -> None:
    b = rt.build_request_body(
        query="q",
        top_k=6,
        namespaces=["kb"],
        filters={"namespace": "kb"},
        rewrite=False,
        rerank=False,
        min_score=0.1,
        hybrid=True,
    )
    assert b["namespaces"] == ["kb"]
    assert b["filters"] == {"namespace": "kb"}
    assert b["rewrite"] is False
    assert b["min_score"] == 0.1
    assert b["hybrid"] is True


def test_main_writes_file_on_200(tmp_path: Path, monkeypatch) -> None:
    out = tmp_path / "out.json"
    payload = {"chunks": [], "rewritten_queries": [], "debug": {}}

    def fake_post(*_a, **_kw):
        return httpx.Response(200, json=payload)

    monkeypatch.setenv("RAG_SERVICE_TOKEN", "tok")
    monkeypatch.setenv("RAG_MCP_BASE_URL", "http://127.0.0.1:8080")
    monkeypatch.setattr(rt.sys, "argv", ["r", "--query", "test query", "--out", str(out)])
    with patch.object(rt.httpx, "post", side_effect=fake_post):
        rt.main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data == payload


def test_main_exits_on_http_error(tmp_path: Path, monkeypatch) -> None:
    out = tmp_path / "out.json"

    def fake_post(*_a, **_kw):
        return httpx.Response(500, text="boom")

    monkeypatch.setenv("RAG_SERVICE_TOKEN", "tok")
    monkeypatch.setattr(
        rt.sys, "argv", ["r", "--query", "q", "--out", str(out)]
    )
    with patch.object(rt.httpx, "post", side_effect=fake_post):
        with pytest.raises(SystemExit) as se:
            rt.main()
    assert se.value.code == 1
    assert not out.exists()
