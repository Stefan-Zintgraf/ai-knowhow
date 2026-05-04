"""
Call `POST /rag/retrieve` and write the JSON response to a file (service token).

Suitable for golden fixtures, diffs, and quick manual tests.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import httpx


def build_request_body(
    query: str,
    top_k: int,
    namespaces: list[str] | None,
    filters: dict | None,
    rewrite: bool,
    rerank: bool,
    min_score: float | None,
    hybrid: bool | None,
) -> dict:
    b: dict = {
        "query": query,
        "top_k": top_k,
        "rewrite": rewrite,
        "rerank": rerank,
    }
    if namespaces is not None:
        b["namespaces"] = namespaces
    if filters is not None:
        b["filters"] = filters
    if min_score is not None:
        b["min_score"] = min_score
    if hybrid is not None:
        b["hybrid"] = hybrid
    return b


def main() -> None:
    p = argparse.ArgumentParser(
        description="POST /rag/retrieve and write RetrievalResponse JSON to a file.",
    )
    p.add_argument(
        "--query",
        default=None,
        help="Query string (default: read stdin if omitted).",
    )
    p.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output path (UTF-8 JSON).",
    )
    p.add_argument("--top-k", type=int, default=6)
    p.add_argument(
        "--namespaces",
        default=None,
        help='Comma-separated namespaces, e.g. "kb" or "kb,tickets". Default: server default.',
    )
    p.add_argument(
        "--filters",
        default=None,
        help="JSON object string for `filters` (e.g. '{\"namespace\":\"kb\"}').",
    )
    p.add_argument("--min-score", type=float, default=None)
    p.add_argument(
        "--no-rewrite", action="store_true", help="Set rewrite: false (default: true)."
    )
    p.add_argument(
        "--no-rerank", action="store_true", help="Set rerank: false (default: true)."
    )
    p.add_argument(
        "--hybrid",
        action="store_true",
        help="Set hybrid: true (omit to leave request default for hybrid).",
    )
    p.add_argument(
        "--no-hybrid",
        action="store_true",
        help="Set hybrid: false",
    )
    args = p.parse_args()

    q = args.query
    if q is None or q == "":
        q = sys.stdin.read().strip()
    if not q:
        print("no query: pass --query or pipe stdin", file=sys.stderr)
        sys.exit(1)

    namespaces: list[str] | None = None
    if args.namespaces is not None and args.namespaces.strip() != "":
        namespaces = [n.strip() for n in args.namespaces.split(",") if n.strip()]

    filters: dict | None = None
    if args.filters is not None and args.filters.strip() != "":
        try:
            raw = json.loads(args.filters)
        except json.JSONDecodeError as e:
            print(f"invalid --filters JSON: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(raw, dict):
            print("--filters must be a JSON object", file=sys.stderr)
            sys.exit(1)
        filters = raw

    hybrid: bool | None = None
    if args.no_hybrid and args.hybrid:
        print("use only one of --hybrid / --no-hybrid", file=sys.stderr)
        sys.exit(1)
    if args.no_hybrid:
        hybrid = False
    elif args.hybrid:
        hybrid = True

    body = build_request_body(
        query=q,
        top_k=args.top_k,
        namespaces=namespaces,
        filters=filters,
        rewrite=not args.no_rewrite,
        rerank=not args.no_rerank,
        min_score=args.min_score,
        hybrid=hybrid,
    )
    out_path = args.out
    if out_path.exists() and not out_path.is_file():
        print(f"--out is not a file: {out_path}", file=sys.stderr)
        sys.exit(1)

    base = os.environ.get("RAG_MCP_BASE_URL", "http://127.0.0.1:8080")
    token = os.environ.get("RAG_SERVICE_TOKEN", "")
    if not token:
        print("set RAG_SERVICE_TOKEN", file=sys.stderr)
        sys.exit(1)

    r = httpx.post(
        f"{base.rstrip('/')}/rag/retrieve",
        json=body,
        headers={"Authorization": f"Bearer {token}"},
        timeout=300.0,
    )
    if r.is_error:
        print(
            f"HTTP {r.status_code}: {r.text[:2000]}",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        data = r.json()
    except json.JSONDecodeError as e:
        print(f"invalid JSON in response: {e}", file=sys.stderr)
        sys.exit(1)
    out_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
