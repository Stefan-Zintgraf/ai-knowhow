"""create_draft CLI (mocked HTTP + env)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import responses

from kerio_mail.create_draft import (
    build_draft_mail,
    first_created_id,
    main,
)
from kerio_mail.mail import find_drafts_folder_id

BASE = "https://mail.example.test"
RPC = f"{BASE}/webmail/api/jsonrpc/"
_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_json(name: str) -> object:
    with open(_FIXTURES / name, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def kerio_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KERIO_BASE_URL", BASE)
    monkeypatch.setenv("KERIO_USERNAME", "u")
    monkeypatch.setenv("KERIO_PASSWORD", "p")


def test_find_drafts_folder_id_by_subtype() -> None:
    data = _load_json("folders_with_drafts.json")
    assert isinstance(data, dict)
    assert find_drafts_folder_id(data) == "fld-drafts"


def test_find_drafts_folder_id_by_name_fallback() -> None:
    data = {
        "list": [
            {"id": "x", "name": "Inbox", "subType": "FSubInbox"},
            {"id": "fld-name-drafts", "name": "Drafts", "type": "FMail"},
        ],
    }
    assert find_drafts_folder_id(data) == "fld-name-drafts"


def test_build_draft_mail() -> None:
    m = build_draft_mail(
        folder_id="f1",
        subject="Hi",
        body="Line1\n",
        to_address="a@b.test",
    )
    assert m["folderId"] == "f1"
    assert m["subject"] == "Hi"
    assert m["isMDNSent"] is True
    assert m["displayableParts"][0]["contentType"] == "ctTextPlain"
    assert m["displayableParts"][0]["content"] == "Line1\n"
    assert m["to"] == [{"name": "", "address": "a@b.test"}]


def test_first_created_id() -> None:
    data = _load_json("mails_create_result.json")
    assert isinstance(data, dict)
    assert first_created_id(data) == "draft-new-id-99"


def test_first_created_id_nested_object() -> None:
    assert first_created_id({"errors": [], "result": [{"id": "z"}]}) == "z"


@responses.activate
def test_create_draft_resolves_folder_and_prints_id(
    kerio_env: None,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    folders = _load_json("folders_with_drafts.json")
    create_res = _load_json("mails_create_result.json")
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": folders},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 3, "result": create_res},
        status=200,
    )
    body_file = tmp_path / "b.txt"
    body_file.write_text("hello", encoding="utf-8")
    rc = main(
        [
            "--body-file",
            str(body_file),
            "--subject",
            "Subj",
        ],
    )
    assert rc == 0
    assert capsys.readouterr().out.strip() == "draft-new-id-99"
    assert len(responses.calls) == 3
    last = json.loads(responses.calls[2].request.body)
    assert last["method"] == "Mails.create"
    params = last["params"]
    assert "mails" in params
    assert len(params["mails"]) == 1
    assert params["mails"][0]["folderId"] == "fld-drafts"
    assert params["mails"][0]["subject"] == "Subj"


@responses.activate
def test_create_draft_explicit_folder(kerio_env: None, capsys: pytest.CaptureFixture[str]) -> None:
    create_res = _load_json("mails_create_result.json")
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": create_res},
        status=200,
    )
    rc = main(
        [
            "--folder-id",
            "my-drafts",
            "--body",
            "x",
        ],
    )
    assert rc == 0
    assert capsys.readouterr().out.strip() == "draft-new-id-99"
    assert len(responses.calls) == 2
    last = json.loads(responses.calls[1].request.body)
    assert last["params"]["mails"][0]["folderId"] == "my-drafts"


@responses.activate
def test_create_draft_no_drafts_folder(kerio_env: None, capsys: pytest.CaptureFixture[str]) -> None:
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": {"list": []}},
        status=200,
    )
    assert main(["--body", "x"]) == 1
    err = capsys.readouterr().err
    assert "Could not find Drafts folder" in err


@responses.activate
def test_create_draft_non_empty_errors_list(kerio_env: None, capsys: pytest.CaptureFixture[str]) -> None:
    folders = _load_json("folders_with_drafts.json")
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 2, "result": folders},
        status=200,
    )
    responses.post(
        RPC,
        json={
            "jsonrpc": "2.0",
            "id": 3,
            "result": {"errors": [{"code": 42, "message": "quota"}], "result": []},
        },
        status=200,
    )
    assert main(["--body", "x"]) == 1
    assert "Mails.create errors" in capsys.readouterr().err


def test_create_draft_module_help_subprocess() -> None:
    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    r = subprocess.run(
        [sys.executable, "-m", "kerio_mail.create_draft", "--help"],
        capture_output=True,
        text=True,
        cwd=str(root),
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert "--body-file" in r.stdout
    assert "--folder-id" in r.stdout
