"""
POST a few KB documents to a running RAG service (for smoke tests).

Usage (repo root, tokens set):
  RAG_SERVICE_TOKEN=... RAG_ADMIN_TOKEN=... RAG_MCP_BASE_URL=http://127.0.0.1:8080 \
    py -3.12 scripts/seed_kb.py
"""

from __future__ import annotations

import argparse
import os
import sys

import httpx


def main() -> None:
    argparse.ArgumentParser(
        description="POST fixed smoke KB documents to /rag/index/kb (requires RAG_ADMIN_TOKEN).",
    ).parse_args()
    base = os.environ.get("RAG_MCP_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    tok = os.environ.get("RAG_ADMIN_TOKEN", "")
    if not tok:
        print("set RAG_ADMIN_TOKEN", file=sys.stderr)
        sys.exit(1)
    docs = {
        "docs": [
            {
                "id": "doc-smoke-1",
                "text": "The EtherCAT master stack supports redundancy on ring topology. " * 3,
                "metadata": {
                    "source_uri": "https://kb.example/ethercat-ring",
                    "product": "ecmaster",
                    "lang": "en",
                    "created_at": 1700000000,
                },
            }
        ]
    }
    r = httpx.post(
        f"{base}/rag/index/kb",
        json=docs,
        headers={"Authorization": f"Bearer {tok}"},
        timeout=300.0,
    )
    print(r.status_code, r.text)
    r.raise_for_status()


if __name__ == "__main__":
    main()
