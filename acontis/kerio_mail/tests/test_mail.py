"""Folders.get, Mails.get, Mails.getById, and paging (mocked HTTP)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import responses

from kerio_mail.client import KerioClient
from kerio_mail.mail import iter_mails_pages

BASE = "https://mail.example.test"
RPC = f"{BASE}/webmail/api/jsonrpc/"
_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_json(name: str) -> object:
    with open(_FIXTURES / name, encoding="utf-8") as f:
        return json.load(f)


@responses.activate
def test_folders_get_returns_list() -> None:
    result_body = _load_json("folders_get_result.json")
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": result_body},
        status=200,
    )
    c = KerioClient(BASE)
    c.login("u", "p", application={"name": "n", "vendor": "v", "version": "1"})
    out = c.folders_get()
    assert out == result_body
    assert len(out["list"]) == 2
    body = json.loads(responses.calls[1].request.body)
    assert body["method"] == "Folders.get"
    assert body["params"] == {}


@responses.activate
def test_mails_get_by_id() -> None:
    result_body = _load_json("mails_get_by_id_result.json")
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": result_body},
        status=200,
    )
    c = KerioClient(BASE)
    c.login("u", "p", application={"name": "n", "vendor": "v", "version": "1"})
    out = c.mails_get_by_id(["m1"])
    assert out == result_body
    body = json.loads(responses.calls[1].request.body)
    assert body["method"] == "Mails.getById"
    assert body["params"]["ids"] == ["m1"]


@responses.activate
def test_iter_mails_pages_three_requests() -> None:
    p1 = _load_json("mails_get_page_1.json")
    p2 = _load_json("mails_get_page_2.json")
    p3 = _load_json("mails_get_page_3.json")
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": p1},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 3, "result": p2},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 4, "result": p3},
        status=200,
    )
    c = KerioClient(BASE)
    c.login("u", "p", application={"name": "n", "vendor": "v", "version": "1"})
    pages = list(iter_mails_pages(c, ["fld-inbox"], page_size=2))
    assert len(pages) == 3
    assert [m["id"] for m in pages[0]["list"]] == ["m1", "m2"]
    assert [m["id"] for m in pages[1]["list"]] == ["m3", "m4"]
    assert [m["id"] for m in pages[2]["list"]] == ["m5"]

    bodies = [json.loads(r.request.body) for r in responses.calls[1:]]
    assert bodies[0]["method"] == "Mails.get"
    assert bodies[0]["params"]["folderIds"] == ["fld-inbox"]
    assert bodies[0]["params"]["query"]["start"] == 0
    assert bodies[0]["params"]["query"]["limit"] == 2
    assert bodies[1]["params"]["query"]["start"] == 2
    assert bodies[2]["params"]["query"]["start"] == 4


def test_iter_mails_pages_rejects_zero_page_size() -> None:
    c = KerioClient(BASE)
    with pytest.raises(ValueError, match="page_size"):
        next(iter(iter_mails_pages(c, ["x"], page_size=0)))
