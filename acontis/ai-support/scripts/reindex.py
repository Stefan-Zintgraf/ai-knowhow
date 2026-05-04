"""
Operational helper: re-index from a JSONL export of {namespace, id, text, metadata}.

Usage (from repository root, with dependencies installed):
  RAG_ADMIN_TOKEN=... py -3.12 scripts/reindex.py /path/to/export.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import httpx


def main() -> None:
    p = argparse.ArgumentParser(
        description="Re-index from a JSONL export of {namespace, id, text, metadata}.",
    )
    p.add_argument(
        "export_path",
        help="Path to JSONL export (one object per line: id, text, optional namespace/metadata).",
    )
    args = p.parse_args()
    path = args.export_path
    base = os.environ.get("RAG_MCP_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    tok = os.environ.get("RAG_ADMIN_TOKEN", "")
    if not tok:
        print("set RAG_ADMIN_TOKEN", file=sys.stderr)
        sys.exit(1)
    ns = "kb"
    batch: list[dict[str, object]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            ns = str(row.get("namespace", "kb"))
            batch.append(
                {
                    "id": row["id"],
                    "text": row["text"],
                    "metadata": row.get("metadata") or {},
                }
            )
    r = httpx.post(
        f"{base}/rag/index/{ns}",
        json={"docs": batch},
        headers={
            "Authorization": f"Bearer {tok}",
        },
        timeout=3600.0,
    )
    print(r.status_code, r.text)
    r.raise_for_status()


if __name__ == "__main__":
    main()
