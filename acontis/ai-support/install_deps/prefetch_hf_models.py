#!/usr/bin/env python3
"""Pre-download Hugging Face assets used by support_rag (hybrid sparse + reranker).

Run from repo root after ``pip install -e ".[dev]"`` (or sentence-transformers + fastembed).

Ids match config.e2e.example.yaml and support_rag/service.py.
"""

from __future__ import annotations

import os

RERANKER = "BAAI/bge-reranker-v2-m3"
SPARSE = "Qdrant/bm25"


def main() -> int:
    print("Prefetching CrossEncoder (reranker)…", flush=True)
    from sentence_transformers import CrossEncoder

    CrossEncoder(RERANKER, device="cpu")
    print(f"  OK: {RERANKER}", flush=True)

    print("Prefetching fastembed sparse (BM25 for hybrid)…", flush=True)
    from fastembed import SparseTextEmbedding

    m = SparseTextEmbedding(SPARSE)
    _ = list(m.embed(["warmup query for local cache"]))
    print(f"  OK: {SPARSE}", flush=True)

    if os.environ.get("HF_TOKEN"):
        print("HF_TOKEN is set (optional; improves Hub rate limits).", flush=True)
    else:
        print("Tip: set HF_TOKEN if Hub downloads are slow or rate-limited.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
