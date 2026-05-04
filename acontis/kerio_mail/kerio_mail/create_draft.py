"""CLI: create a draft message via ``Mails.create`` (Drafts folder from ``Folders.get``)."""

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
from kerio_mail.mail import find_drafts_folder_id
from kerio_mail.read_mailbox import (
    application_from_env,
    require_env_for_session,
)


def build_draft_mail(
    *,
    folder_id: str,
    subject: str,
    body: str,
    to_address: str | None = None,
) -> dict[str, Any]:
    """
    Build a ``Mail`` dict for ``Mails.create`` — unsent draft in ``folder_id``.

    Body is a single ``ctTextPlain`` displayable part per Kerio ``DisplayableMimePart``.
    """
    mail: dict[str, Any] = {
        "folderId": folder_id,
        "subject": subject,
        "displayableParts": [
            {
                "contentType": "ctTextPlain",
                "content": body,
            },
        ],
        # IDL: unfinished message — avoid MDN side effects when saving draft
        "isMDNSent": True,
    }
    if to_address:
        addr = to_address.strip()
        if addr:
            mail["to"] = [{"name": "", "address": addr}]
    return mail


def first_created_id(create_result: Any) -> str | None:
    """Extract first new mail id from ``Mails.create`` JSON-RPC ``result`` object."""
    if not isinstance(create_result, dict):
        return None
    ids = create_result.get("result")
    if isinstance(ids, list) and ids:
        first = ids[0]
        if isinstance(first, str):
            return first
        if isinstance(first, dict) and first.get("id") is not None:
            return str(first["id"])
    return None


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Kerio webmail: create a draft via Mails.create (credentials from .env).",
    )
    p.add_argument(
        "--env-file",
        type=Path,
        default=None,
        help="Path to .env (default: search from cwd).",
    )
    p.add_argument(
        "--subject",
        default="",
        help="Draft subject (default: empty).",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--body",
        default=None,
        help="Draft body text (UTF-8).",
    )
    g.add_argument(
        "--body-file",
        type=Path,
        default=None,
        help="Read draft body from this file (UTF-8).",
    )
    p.add_argument(
        "--to",
        dest="to_address",
        default=None,
        metavar="ADDRESS",
        help="Optional To address (draft with recipient filled in).",
    )
    p.add_argument(
        "--folder-id",
        default=None,
        metavar="ID",
        help="Drafts folder id (skip Folders.get). Default: resolve Drafts via Folders.get.",
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

    body: str
    if args.body_file is not None:
        try:
            body = args.body_file.read_text(encoding="utf-8")
        except OSError as e:
            print(str(e), file=sys.stderr)
            return 2
    else:
        body = args.body or ""

    base, username, password, verify = session
    client = KerioClient(base, verify_ssl=verify)
    app = application_from_env()

    try:
        client.login(username, password, application=app)
    except (KerioRpcError, OSError, requests.RequestException) as e:
        print(str(e), file=sys.stderr)
        return 1

    if args.folder_id:
        folder_id = args.folder_id.strip()
        if not folder_id:
            print("--folder-id must be non-empty when set.", file=sys.stderr)
            return 2
    else:
        try:
            folders = client.folders_get()
        except (KerioRpcError, OSError, requests.RequestException) as e:
            print(str(e), file=sys.stderr)
            return 1
        fid = find_drafts_folder_id(folders if isinstance(folders, dict) else {})
        if not fid:
            print(
                "Could not find Drafts folder (no subType FSubDrafts / name Drafts). "
                "Use --folder-id.",
                file=sys.stderr,
            )
            return 1
        folder_id = fid

    mail = build_draft_mail(
        folder_id=folder_id,
        subject=args.subject,
        body=body,
        to_address=args.to_address,
    )

    try:
        raw = client.mails_create([mail])
    except (KerioRpcError, OSError, requests.RequestException) as e:
        print(str(e), file=sys.stderr)
        return 1

    if isinstance(raw, Mapping):
        errs = raw.get("errors")
        if isinstance(errs, list) and len(errs) > 0:
            print(f"Mails.create errors: {errs!r}", file=sys.stderr)
            return 1

    new_id = first_created_id(raw)
    if not new_id:
        print(f"Unexpected Mails.create result: {raw!r}", file=sys.stderr)
        return 1

    print(new_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
