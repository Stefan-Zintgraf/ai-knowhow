"""export_attachments CLI (mocked HTTP + env)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import responses

from kerio_mail.export_attachments import (
    file_download_from_export_result,
    main,
    pick_attachment_ids,
)
from kerio_mail.mail import attachment_ids_from_mail, first_mail_from_get_by_id

BASE = "https://mail.example.test"
RPC = f"{BASE}/webmail/api/jsonrpc/"
ZIP_URL = "https://mail.example.test/webmail/download/export.zip?sid=abc"
_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_json(name: str) -> object:
    with open(_FIXTURES / name, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def kerio_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KERIO_BASE_URL", BASE)
    monkeypatch.setenv("KERIO_USERNAME", "u")
    monkeypatch.setenv("KERIO_PASSWORD", "p")


def test_attachment_ids_from_mail() -> None:
    data = _load_json("mails_get_by_id_with_attachments.json")
    assert isinstance(data, dict)
    m = first_mail_from_get_by_id(data)
    assert m is not None
    assert attachment_ids_from_mail(m) == ["att-1", "att-2"]


def test_file_download_from_export_result_wrapped() -> None:
    raw = _load_json("mails_export_attachments_result.json")
    assert isinstance(raw, dict)
    fd = file_download_from_export_result(raw)
    assert fd is not None
    assert fd["name"] == "export.zip"
    assert "export.zip" in fd["url"]


def test_file_download_from_export_result_flat() -> None:
    fd = file_download_from_export_result(
        {"url": "https://x/z.zip", "name": "z.zip", "length": 1},
    )
    assert fd is not None
    assert fd["url"] == "https://x/z.zip"


def test_pick_attachment_ids_subset() -> None:
    mail = {"attachments": [{"id": "a"}, {"id": "b"}]}
    assert pick_attachment_ids(mail, filter_ids=None) == ["a", "b"]
    assert pick_attachment_ids(mail, filter_ids=["b"]) == ["b"]
    assert pick_attachment_ids(mail, filter_ids=["a", "b"]) == ["a", "b"]
    assert pick_attachment_ids(mail, filter_ids=["nope"]) is None


@responses.activate
def test_export_attachments_writes_zip(
    kerio_env: None,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    by_id = _load_json("mails_get_by_id_with_attachments.json")
    export_res = _load_json("mails_export_attachments_result.json")
    zip_bytes = b"PK\x03\x04fake"
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": by_id},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 3, "result": export_res},
        status=200,
    )
    responses.get(ZIP_URL, body=zip_bytes, status=200)

    out_file = tmp_path / "out.zip"
    rc = main(
        [
            "--mail-id",
            "mail-with-att",
            "--output",
            str(out_file),
        ],
    )
    assert rc == 0
    assert out_file.read_bytes() == zip_bytes
    assert capsys.readouterr().out.strip() == str(out_file.resolve())

    bodies = [json.loads(r.request.body) for r in responses.calls if r.request.method == "POST"]
    assert bodies[1]["method"] == "Mails.getById"
    assert bodies[2]["method"] == "Mails.exportAttachments"
    assert bodies[2]["params"]["attachmentIds"] == ["att-1", "att-2"]


@responses.activate
def test_export_attachments_one_attachment_id(
    kerio_env: None,
    tmp_path: Path,
) -> None:
    by_id = _load_json("mails_get_by_id_with_attachments.json")
    export_res = _load_json("mails_export_attachments_result.json")
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": by_id},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 3, "result": export_res},
        status=200,
    )
    responses.get(ZIP_URL, body=b"x", status=200)

    out_file = tmp_path / "one.zip"
    assert (
        main(
            [
                "--mail-id",
                "mail-with-att",
                "--attachment-id",
                "att-2",
                "-o",
                str(out_file),
            ],
        )
        == 0
    )
    last_rpc = json.loads(
        [c for c in responses.calls if c.request.method == "POST"][-1].request.body,
    )
    assert last_rpc["params"]["attachmentIds"] == ["att-2"]


@responses.activate
def test_export_attachments_no_attachments(kerio_env: None, capsys: pytest.CaptureFixture[str]) -> None:
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
                "errors": [],
                "result": [{"id": "m", "subject": "x", "attachments": []}],
            },
        },
        status=200,
    )
    assert main(["--mail-id", "m"]) == 1
    assert "No attachments" in capsys.readouterr().err


@responses.activate
def test_export_attachments_bad_attachment_filter(
    kerio_env: None,
    capsys: pytest.CaptureFixture[str],
) -> None:
    by_id = _load_json("mails_get_by_id_with_attachments.json")
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": by_id},
        status=200,
    )
    assert main(["--mail-id", "mail-with-att", "--attachment-id", "missing"]) == 1
    assert "not on this message" in capsys.readouterr().err


def test_export_attachments_module_help_subprocess() -> None:
    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    r = subprocess.run(
        [sys.executable, "-m", "kerio_mail.export_attachments", "--help"],
        capture_output=True,
        text=True,
        cwd=str(root),
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert "--mail-id" in r.stdout
    assert "--attachment-id" in r.stdout
