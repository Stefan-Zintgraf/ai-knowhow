"""
Walk a folder of text files and POST them to `POST /rag/index/{namespace}` (admin token).

Default files: `*.md`, `*.txt`, `*.rst` (UTF-8). Symlinks and paths outside `--root` are
skipped. Long relative paths use a short stable hash for `id`; the full path stays in
`metadata["file_path"]`.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from support_rag.folder_ingest import (
    _DEFAULT_BATCH,
    _DEFAULT_PATTERNS,
    _is_under_root,
    _safe_doc_id,
    collect_docs,
    enrich_metadata,
    post_batches,
)

# Re-export for tests that load this module
__all__ = [
    "collect_docs",
    "post_batches",
    "_is_under_root",
    "_safe_doc_id",
    "main",
]


def main() -> None:
    p = argparse.ArgumentParser(
        description="Index all matching text files under a folder into RAG (POST /rag/index).",
    )
    p.add_argument(
        "--root",
        type=Path,
        required=True,
        help="Root directory to walk (resolved; files must stay under it).",
    )
    p.add_argument(
        "--namespace",
        choices=("kb", "tickets"),
        default="kb",
    )
    p.add_argument(
        "--include",
        action="append",
        default=None,
        metavar="GLOB",
        help=f"File name glob, repeatable (default: {', '.join(_DEFAULT_PATTERNS)}).",
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=_DEFAULT_BATCH,
        help=f"Max documents per HTTP request (default {_DEFAULT_BATCH}).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="List document ids; do not POST.",
    )
    p.add_argument(
        "--lang",
        default=None,
        help="If set, add metadata.lang.",
    )
    p.add_argument(
        "--product",
        default=None,
        help="If set, add metadata.product.",
    )
    args = p.parse_args()
    patterns: tuple[str, ...] = tuple(
        args.include if args.include is not None else _DEFAULT_PATTERNS
    )

    try:
        root = args.root.resolve()
    except OSError as e:
        print(f"resolve --root: {e}", file=sys.stderr)
        sys.exit(1)

    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        sys.exit(1)

    docs, n_skip, n_read_err, msg_lines = collect_docs(root, patterns)
    for m in msg_lines:
        print(m, file=sys.stderr)

    enrich_metadata(docs, lang=args.lang, product=args.product)

    if not docs:
        print("0 files; nothing to index", file=sys.stderr)
        sys.exit(1 if n_read_err > 0 else 0)

    if args.dry_run:
        for d in docs:
            print(f"id={d['id']}", file=sys.stderr)
        print(
            f"dry-run: {len(docs)} doc(s), {n_skip} skipped; no POST",
            file=sys.stderr,
        )
        sys.exit(0)

    base = os.environ.get("RAG_MCP_BASE_URL", "http://127.0.0.1:8080")
    tok = os.environ.get("RAG_ADMIN_TOKEN", "")
    if not tok:
        print("set RAG_ADMIN_TOKEN", file=sys.stderr)
        sys.exit(1)

    try:
        import httpx

        post_batches(
            base, tok, args.namespace, docs, max(1, args.batch_size)
        )
    except httpx.HTTPStatusError as e:
        print(
            f"HTTP {e.response.status_code}: {e.response.text[:500]}",
            file=sys.stderr,
        )
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"request failed: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"ok: indexed {len(docs)} parent doc(s) in namespace {args.namespace}")


if __name__ == "__main__":
    main()
