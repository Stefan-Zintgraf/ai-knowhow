"""KerioClient login and JSON-RPC errors (mocked HTTP)."""

from __future__ import annotations

import json

import pytest
import requests
import responses

from kerio_mail.client import KerioClient, KerioRpcError

BASE = "https://mail.example.test"
RPC = f"{BASE}/webmail/api/jsonrpc/"


@responses.activate
def test_login_sets_token_and_sends_x_token_on_next_call() -> None:
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "abc123"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": {"list": []}},
        status=200,
    )

    c = KerioClient(BASE)
    tok = c.login(
        "user@example.test",
        "secret",
        application={"name": "t", "vendor": "v", "version": "1"},
    )
    assert tok == "abc123"
    assert c.session.headers.get("X-Token") == "abc123"

    c.call("Folders.get", {})
    assert len(responses.calls) == 2
    body = json.loads(responses.calls[1].request.body)
    assert body["method"] == "Folders.get"
    assert responses.calls[1].request.headers.get("X-Token") == "abc123"


@responses.activate
def test_login_jsonrpc_error_raises() -> None:
    responses.post(
        RPC,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "error": {"code": 401, "message": "Invalid credentials"},
        },
        status=200,
    )
    c = KerioClient(BASE)
    with pytest.raises(KerioRpcError) as ei:
        c.login("u", "p", application={"name": "t", "vendor": "v", "version": "1"})
    assert ei.value.error["code"] == 401
    assert c.token is None


@responses.activate
def test_http_error_propagates() -> None:
    responses.post(RPC, body="Gateway Timeout", status=504)
    c = KerioClient(BASE)
    with pytest.raises(requests.HTTPError):
        c.call("Session.login", {})


@responses.activate
def test_mails_export_attachments() -> None:
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "result": {
                "fileDownload": {
                    "url": "https://mail.example.test/z.zip",
                    "name": "z.zip",
                    "length": 1,
                },
            },
        },
        status=200,
    )
    c = KerioClient(BASE)
    c.login("u", "p", application={"name": "n", "vendor": "v", "version": "1"})
    out = c.mails_export_attachments(["a1", "a2"])
    assert isinstance(out, dict)
    assert out["fileDownload"]["name"] == "z.zip"
    body = json.loads(responses.calls[1].request.body)
    assert body["method"] == "Mails.exportAttachments"
    assert body["params"]["attachmentIds"] == ["a1", "a2"]


@responses.activate
def test_download_get_relative_url() -> None:
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.get(
        f"{BASE}/webmail/dl/file.zip",
        body=b"zipdata",
        status=200,
    )
    c = KerioClient(BASE)
    c.login("u", "p", application={"name": "n", "vendor": "v", "version": "1"})
    data = c.download_get("/webmail/dl/file.zip")
    assert data == b"zipdata"
    assert responses.calls[1].request.url.rstrip("/").endswith("/webmail/dl/file.zip")
