"""
Walk a folder of text files and index into the RAG service.

Used by `scripts/ingest_folder.py` (HTTP) and the optional web UI (in-process `RAGService.index`).
"""

from __future__ import annotations

import fnmatch
import os
import sys
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from support_rag.service import RAGService
else:
    RAGService = Any

import httpx

from support_rag.schemas import IngestDocument

# IDs longer than this use a short `h<hex>` id; the full path is in `metadata["file_path"]`.
_MAX_ID_LEN = 256
_DEFAULT_PATTERNS = ("*.md", "*.txt", "*.rst")
_DEFAULT_BATCH = 32


def _is_under_root(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _safe_doc_id(relative_posix: str) -> str:
    """Relative path with `/`; if too long, use stable hash of full string."""
    if len(relative_posix) <= _MAX_ID_LEN:
        return relative_posix
    import hashlib

    h = hashlib.sha256(relative_posix.encode("utf-8")).hexdigest()[:24]
    return f"h{h}"


def _iter_files_impl(
    root: Path,
    include_patterns: tuple[str, ...],
) -> Iterator[tuple[Path, str, str | None, str | None, str | None]]:
    """Yields (path, doc_id, err, text, rel_str). err set => skip (doc_id may be set for logs)."""
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(
        str(root), topdown=True, followlinks=False
    ):
        base = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not (base / d).is_symlink()]

        for name in sorted(filenames):
            p = base / name
            if p.is_symlink():
                yield (p, "", "symlink", None, None)
                continue
            if not _is_under_root(root, p):
                yield (p, "", "outside_root", None, None)
                continue
            if not any(fnmatch.fnmatch(name, pat) for pat in include_patterns):
                continue
            rel = p.resolve().relative_to(root)
            rel_str = rel.as_posix()
            doc_id = _safe_doc_id(rel_str)
            try:
                text = p.read_text(encoding="utf-8")
            except OSError as e:
                yield (p, doc_id, f"read: {e}", None, rel_str)
                continue
            except UnicodeDecodeError:
                yield (p, doc_id, "utf-8", None, rel_str)
                continue
            yield (p, doc_id, None, text, rel_str)


def collect_docs(
    root: Path,
    include_patterns: tuple[str, ...],
) -> tuple[list[dict[str, object]], int, int, list[str]]:
    """
    Returns (docs, n_skip, n_read_err, messages).
    n_read_err: utf-8 / OSError on a file that matched the include glob.
    """
    docs: list[dict[str, object]] = []
    seen: set[str] = set()
    n_skip = 0
    n_read_err = 0
    messages: list[str] = []
    for p, doc_id, err, text, rel_str in _iter_files_impl(root, include_patterns):
        if err is not None:
            n_skip += 1
            if err not in ("symlink", "outside_root"):
                n_read_err += 1
            messages.append(f"skip {p}: {err}")
            continue
        if text is None or rel_str is None:
            continue
        if doc_id in seen:
            messages.append(
                f"warning: duplicate id after normalization, keeping first: {doc_id} ({p})"
            )
            continue
        seen.add(doc_id)
        uris = f"file://{p.resolve().as_posix()}"
        docs.append(
            {
                "id": doc_id,
                "text": text,
                "metadata": {
                    "file_path": rel_str,
                    "source_uri": uris,
                },
            }
        )
    return docs, n_skip, n_read_err, messages


def post_batches(
    base_url: str,
    admin_token: str,
    namespace: str,
    docs: list[dict[str, object]],
    batch_size: int,
) -> None:
    url = f"{base_url.rstrip('/')}/rag/index/{namespace}"
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }
    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        r = httpx.post(url, json={"docs": batch}, headers=headers, timeout=3600.0)
        r.raise_for_status()


def enrich_metadata(
    docs: list[dict[str, object]], *, lang: str | None, product: str | None
) -> None:
    if not (lang or product):
        return
    for d in docs:
        md = d.get("metadata")
        if isinstance(md, dict):
            if lang:
                md["lang"] = lang
            if product:
                md["product"] = product


async def index_local_folder_inprocess(
    service: RAGService,
    root: Path,
    namespace: str,
    *,
    include_patterns: tuple[str, ...] = _DEFAULT_PATTERNS,
    batch_size: int = _DEFAULT_BATCH,
    trace_ctx: Mapping[str, str] | None = None,
) -> dict[str, object]:
    """
    Ingest all collected docs under `root` using in-process `RAGService.index` in batches.
    """
    if namespace not in ("kb", "tickets"):
        raise ValueError("namespace must be kb or tickets")
    try:
        root = root.resolve()
    except OSError as e:
        return {"ok": False, "error": f"resolve path: {e}", "indexed": 0}
    if not root.is_dir():
        return {"ok": False, "error": f"not a directory: {root}", "indexed": 0}
    if not _is_under_root(root, root):
        return {"ok": False, "error": "invalid root path", "indexed": 0}

    docs, n_skip, n_read_err, messages = collect_docs(root, include_patterns)
    for m in messages:
        print(m, file=sys.stderr)

    if not docs:
        return {
            "ok": n_read_err == 0,
            "indexed": 0,
            "n_skip": n_skip,
            "n_read_err": n_read_err,
            "messages": messages,
        }

    n_indexed = 0
    bs = max(1, batch_size)
    for i in range(0, len(docs), bs):
        batch = docs[i : i + bs]
        inst: Sequence[IngestDocument | dict[str, object]] = [
            IngestDocument.model_validate(b) for b in batch
        ]
        await service.index(namespace, inst, trace_ctx=trace_ctx)
        n_indexed += len(batch)

    return {
        "ok": True,
        "indexed": n_indexed,
        "n_skip": n_skip,
        "n_read_err": n_read_err,
        "messages": messages,
    }
