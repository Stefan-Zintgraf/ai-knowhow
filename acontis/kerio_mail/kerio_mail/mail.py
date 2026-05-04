"""Mail and folder listing helpers (Kerio Client API: Folders.get, Mails.get, Mails.getById)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from kerio_mail.client import KerioClient


def find_drafts_folder_id(folders_result: Mapping[str, Any]) -> str | None:
    """
    Return the Drafts folder id from ``Folders.get`` ``list``.

    Prefer ``subType`` ``FSubDrafts`` (Kerio IDL); fall back to folder name Drafts/Draft.
    """
    raw = folders_result.get("list")
    if not isinstance(raw, list):
        return None
    for item in raw:
        if isinstance(item, dict) and item.get("subType") == "FSubDrafts" and item.get("id") is not None:
            return str(item["id"])
    for item in raw:
        if not isinstance(item, dict) or item.get("id") is None:
            continue
        name = str(item.get("name", "")).strip().lower()
        if name in ("drafts", "draft"):
            return str(item["id"])
    return None


def iter_mails_pages(
    client: KerioClient,
    folder_ids: Sequence[Any],
    *,
    page_size: int = 50,
    base_query: Mapping[str, Any] | None = None,
) -> Iterator[dict[str, Any]]:
    """
    Call ``Mails.get`` repeatedly with ``SearchQuery.start`` / ``limit`` until all items are fetched.

    Yields each RPC result dict (typically ``list`` + ``totalItems``). Requires login (``X-Token``).
    """
    if page_size < 1:
        raise ValueError("page_size must be >= 1")

    base: dict[str, Any] = dict(base_query) if base_query else {}
    start = int(base.pop("start", 0))
    query: dict[str, Any] = {**base, "limit": page_size}

    while True:
        query["start"] = start
        result = client.mails_get(list(folder_ids), query)
        if not isinstance(result, dict):
            raise TypeError("Mails.get result must be a dict")
        items = result.get("list") or []
        total_raw = result.get("totalItems")
        total = int(total_raw) if total_raw is not None else 0

        yield result

        if not items:
            break
        start += len(items)
        if total > 0 and start >= total:
            break
        if total_raw is None and len(items) < page_size:
            break


def first_mail_from_get_by_id(result: Any) -> dict[str, Any] | None:
    """First mail from ``Mails.getById`` JSON-RPC ``result`` dict, or ``None`` if missing / errors."""
    if not isinstance(result, dict):
        return None
    errs = result.get("errors")
    if isinstance(errs, list) and len(errs) > 0:
        return None
    mails = result.get("result")
    if not isinstance(mails, list) or not mails:
        return None
    first = mails[0]
    return dict(first) if isinstance(first, dict) else None


def attachment_ids_from_mail(mail: Mapping[str, Any]) -> list[str]:
    """Collect global attachment ids from a full ``Mail`` (``Mails.getById``)."""
    raw = mail.get("attachments")
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, dict) and item.get("id") is not None:
            out.append(str(item["id"]))
    return out
