"""read_mailbox CLI (mocked HTTP + env).

Plan §9: CLI smoke via subprocess *or* in-process mocks; ``--login-only`` and list paths
are covered here with ``responses`` + ``main()``; ``--help`` uses subprocess (§9 style).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import responses

from kerio_mail.read_mailbox import (
    collect_mail_folder_ids,
    main,
)

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


def test_collect_mail_folder_ids() -> None:
    data = _load_json("folders_get_result.json")
    assert isinstance(data, dict)
    assert collect_mail_folder_ids(data) == ["fld-inbox", "fld-sent"]


def test_main_missing_env_exit(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Avoid loading workspace ``.env`` (use an empty env file)."""
    empty = tmp_path / "empty.env"
    empty.write_text("# no KERIO_* set\n", encoding="utf-8")
    monkeypatch.delenv("KERIO_BASE_URL", raising=False)
    monkeypatch.delenv("KERIO_USERNAME", raising=False)
    monkeypatch.delenv("KERIO_PASSWORD", raising=False)
    assert main(["--env-file", str(empty)]) == 2


@responses.activate
def test_login_only_success(kerio_env: None) -> None:
    responses.post(
        RPC,
        json={"jsonrpc": "2.0", "id": 1, "result": {"token": "t"}},
        status=200,
    )
    assert main(["--login-only"]) == 0
    assert len(responses.calls) == 1


@responses.activate
def test_login_only_rpc_error(kerio_env: None) -> None:
    responses.post(
        RPC,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "error": {"code": 401, "message": "bad"},
        },
        status=200,
    )
    assert main(["--login-only"]) == 1


@responses.activate
def test_list_folder_scoped_json_lines(kerio_env: None, capsys: pytest.CaptureFixture[str]) -> None:
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
    rc = main(
        [
            "--folder-id",
            "fld-inbox",
            "--page-size",
            "2",
            "--json-lines",
        ],
    )
    assert rc == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 5
    rows = [json.loads(line) for line in out]
    assert [r["id"] for r in rows] == ["m1", "m2", "m3", "m4", "m5"]


@responses.activate
def test_list_all_folders_uses_folders_get(kerio_env: None, capsys: pytest.CaptureFixture[str]) -> None:
    folders = {
        "list": [
            {
                "id": "fld-inbox",
                "parentId": "root",
                "name": "Inbox",
                "type": "FMail",
            },
        ],
    }
    one_page = {"list": [{"id": "m1", "subject": "Hello"}], "totalItems": 1}
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
        json={"jsonrpc": "2.0", "id": 3, "result": one_page},
        status=200,
    )
    rc = main(["--page-size", "50"])
    assert rc == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1
    assert "m1" in out[0] and "Hello" in out[0]


def test_page_size_invalid(kerio_env: None) -> None:
    assert main(["--page-size", "0", "--folder-id", "x"]) == 2


def test_read_mailbox_module_help_subprocess() -> None:
    """§9 subprocess smoke: ``python -m kerio_mail.read_mailbox --help`` (no network)."""
    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    r = subprocess.run(
        [sys.executable, "-m", "kerio_mail.read_mailbox", "--help"],
        capture_output=True,
        text=True,
        cwd=str(root),
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert "--login-only" in r.stdout
    assert "--json-lines" in r.stdout
