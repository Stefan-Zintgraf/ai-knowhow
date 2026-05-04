"""CLI: login, list folders, page through mail with human or JSON-lines output."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from kerio_mail.client import KerioClient, KerioRpcError
from kerio_mail.mail import iter_mails_pages


def _truthy_env(name: str, default: bool = True) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() not in ("0", "false", "no", "off")


def application_from_env() -> dict[str, str]:
    return {
        "name": os.environ.get("KERIO_APP_NAME", "kerio-mail-read").strip() or "kerio-mail-read",
        "vendor": os.environ.get("KERIO_APP_VENDOR", "acontis").strip() or "acontis",
        "version": os.environ.get("KERIO_APP_VERSION", "1.0").strip() or "1.0",
    }


def require_env_for_session() -> tuple[str, str, str, bool] | None:
    """Return ``(base_url, username, password, verify_ssl)``, or ``None`` if unset."""
    base = os.environ.get("KERIO_BASE_URL", "").strip()
    user = os.environ.get("KERIO_USERNAME", "").strip()
    password = os.environ.get("KERIO_PASSWORD", "")
    if not base or not user or not password:
        print(
            "Missing required environment: KERIO_BASE_URL, KERIO_USERNAME, KERIO_PASSWORD "
            "(set in the environment or in a .env file).",
            file=sys.stderr,
        )
        return None
    verify = _truthy_env("KERIO_VERIFY_SSL", True)
    return base, user, password, verify


def collect_mail_folder_ids(folders_result: Mapping[str, Any]) -> list[str]:
    """Folder ids to scan: every ``id`` in ``Folders.get`` ``list``."""
    raw = folders_result.get("list")
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, dict) and item.get("id") is not None:
            out.append(str(item["id"]))
    return out


def _mail_sort_key(m: Mapping[str, Any]) -> tuple[Any, ...]:
    for key in ("date", "sentDate", "receivedDate", "modified"):
        v = m.get(key)
        if v is not None:
            return (0, v)
    return (1, m.get("id", ""))


def iter_all_mails(
    client: KerioClient,
    folder_ids: Sequence[str],
    *,
    page_size: int,
) -> Iterator[dict[str, Any]]:
    for fid in folder_ids:
        for page in iter_mails_pages(client, [fid], page_size=page_size):
            items = page.get("list") or []
            if not isinstance(items, list):
                continue
            for m in items:
                if isinstance(m, dict):
                    yield dict(m)


def format_line(mail: dict[str, Any], *, json_lines: bool) -> str:
    if json_lines:
        return json.dumps(mail, ensure_ascii=False)
    subj = str(mail.get("subject", "")).replace("\n", " ").replace("\r", "")
    mid = mail.get("id", "")
    date = (
        mail.get("date")
        or mail.get("sentDate")
        or mail.get("receivedDate")
        or mail.get("modified")
        or ""
    )
    return f"{mid}\t{date}\t{subj}"


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Kerio webmail: list messages via JSON-RPC (credentials from .env).",
    )
    p.add_argument(
        "--env-file",
        type=Path,
        default=None,
        help="Path to .env (default: search from cwd).",
    )
    p.add_argument(
        "--login-only",
        action="store_true",
        help="Log in and exit (validate credentials).",
    )
    p.add_argument(
        "--json-lines",
        action="store_true",
        help="Print one JSON object per line instead of tab-separated text.",
    )
    p.add_argument(
        "--folder-id",
        action="append",
        dest="folder_ids",
        default=None,
        metavar="ID",
        help="Restrict to this folder id (repeatable). Default: all mail folders.",
    )
    p.add_argument(
        "--page-size",
        type=int,
        default=50,
        metavar="N",
        help="Mails.get page size (default: 50).",
    )
    return p.parse_args(None if argv is None else list(argv))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.env_file is not None:
        load_dotenv(args.env_file)
    else:
        load_dotenv()

    session = require_env_for_session()
    if session is None:
        return 2
    base, username, password, verify = session
    if args.page_size < 1:
        print("--page-size must be >= 1", file=sys.stderr)
        return 2

    client = KerioClient(base, verify_ssl=verify)
    app = application_from_env()

    try:
        client.login(username, password, application=app)
    except (KerioRpcError, OSError, requests.RequestException) as e:
        print(str(e), file=sys.stderr)
        return 1

    if args.login_only:
        return 0

    if args.folder_ids:
        folder_ids = list(args.folder_ids)
    else:
        try:
            folders = client.folders_get()
        except (KerioRpcError, OSError, requests.RequestException) as e:
            print(str(e), file=sys.stderr)
            return 1
        folder_ids = collect_mail_folder_ids(folders if isinstance(folders, dict) else {})
        if not folder_ids:
            print("No mail folders found (empty Folders.get list).", file=sys.stderr)
            return 1

    try:
        mails = list(
            iter_all_mails(client, folder_ids, page_size=args.page_size),
        )
    except (KerioRpcError, OSError, requests.RequestException, TypeError) as e:
        print(str(e), file=sys.stderr)
        return 1

    mails.sort(key=_mail_sort_key)
    for m in mails:
        print(format_line(m, json_lines=args.json_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
