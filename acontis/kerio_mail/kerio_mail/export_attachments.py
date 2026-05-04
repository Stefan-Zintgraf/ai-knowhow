"""CLI: export attachments for one message via ``Mails.exportAttachments`` + HTTP GET (``Download.url``)."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from kerio_mail.client import KerioClient, KerioRpcError
from kerio_mail.mail import attachment_ids_from_mail, first_mail_from_get_by_id
from kerio_mail.read_mailbox import (
    application_from_env,
    require_env_for_session,
)


def file_download_from_export_result(raw: Any) -> dict[str, Any] | None:
    """Extract ``Download`` dict (``url``, ``name``, ``length``) from ``Mails.exportAttachments`` result."""
    if not isinstance(raw, dict):
        return None
    fd = raw.get("fileDownload")
    if isinstance(fd, dict) and fd.get("url"):
        return fd
    if raw.get("url"):
        return raw
    return None


def pick_attachment_ids(
    mail: Mapping[str, Any],
    *,
    filter_ids: Sequence[str] | None,
) -> list[str] | None:
    """
    Return attachment id list for export.

    If ``filter_ids`` is non-empty, only ids present on the mail are kept; returns ``None`` if
    any requested id is missing.
    """
    all_ids = attachment_ids_from_mail(mail)
    if not filter_ids:
        return all_ids
    want = {str(x).strip() for x in filter_ids if str(x).strip()}
    if not want:
        return all_ids
    have = set(all_ids)
    missing = want - have
    if missing:
        return None
    return [i for i in all_ids if i in want]


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Kerio webmail: download attachments as a zip for one message "
            "(Mails.getById, Mails.exportAttachments, GET Download.url; credentials from .env)."
        ),
    )
    p.add_argument(
        "--env-file",
        type=Path,
        default=None,
        help="Path to .env (default: search from cwd).",
    )
    p.add_argument(
        "--mail-id",
        required=True,
        metavar="ID",
        help="Global mail id (same as list / read_mailbox output).",
    )
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        metavar="PATH",
        help="Write zip to this path (default: Download.name in current directory).",
    )
    p.add_argument(
        "--attachment-id",
        dest="attachment_ids",
        action="append",
        default=[],
        metavar="ID",
        help="Export only these attachment ids (repeatable). Default: all attachments on the mail.",
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

    mail_id = (args.mail_id or "").strip()
    if not mail_id:
        print("--mail-id must be non-empty.", file=sys.stderr)
        return 2

    base, username, password, verify = session
    client = KerioClient(base, verify_ssl=verify)
    app = application_from_env()

    try:
        client.login(username, password, application=app)
    except (KerioRpcError, OSError, requests.RequestException) as e:
        print(str(e), file=sys.stderr)
        return 1

    try:
        raw = client.mails_get_by_id([mail_id])
    except (KerioRpcError, OSError, requests.RequestException) as e:
        print(str(e), file=sys.stderr)
        return 1

    mail = first_mail_from_get_by_id(raw)
    if not mail:
        print(
            "Mail not found or Mails.getById errors (check id and permissions).",
            file=sys.stderr,
        )
        return 1

    filt = [str(x) for x in args.attachment_ids] if args.attachment_ids else None
    ids = pick_attachment_ids(mail, filter_ids=filt)
    if ids is None:
        print(
            "One or more --attachment-id values are not on this message.",
            file=sys.stderr,
        )
        return 1
    if not ids:
        print("No attachments to export for this message.", file=sys.stderr)
        return 1

    try:
        exp = client.mails_export_attachments(ids)
    except (KerioRpcError, OSError, requests.RequestException) as e:
        print(str(e), file=sys.stderr)
        return 1

    dl = file_download_from_export_result(exp)
    if not dl:
        print(f"Unexpected Mails.exportAttachments result: {exp!r}", file=sys.stderr)
        return 1

    url = str(dl.get("url", "")).strip()
    if not url:
        print("Download url missing in export result.", file=sys.stderr)
        return 1

    name = str(dl.get("name", "attachments.zip")).strip() or "attachments.zip"
    out_path = args.output
    if out_path is None:
        out_path = Path(os.getcwd()) / name

    try:
        data = client.download_get(url)
    except (OSError, requests.RequestException) as e:
        print(str(e), file=sys.stderr)
        return 1

    try:
        out_path.write_bytes(data)
    except OSError as e:
        print(str(e), file=sys.stderr)
        return 1

    print(str(out_path.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
