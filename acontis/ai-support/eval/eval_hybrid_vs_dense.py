#!/usr/bin/env python3
"""Golden-set eval: hybrid vs dense-only retrieval (live RAG + Qdrant + gateway)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import httpx

DEFAULT_JSONL = Path(__file__).resolve().parent / "golden" / "questions.jsonl"


def _hit(chunks: list[dict[str, object]], gold: str, top_k: int) -> bool:
    for c in chunks[:top_k]:
        if str(c.get("parent_id", "")) == gold:
            return True
    return False


def _retrieve(
    client: httpx.Client,
    base: str,
    headers: dict[str, str],
    *,
    query: str,
    namespace: str,
    top_k: int,
    hybrid: bool,
    rewrite: bool,
) -> list[dict[str, object]]:
    body = {
        "query": query,
        "top_k": top_k,
        "namespaces": [namespace],
        "rewrite": rewrite,
        "rerank": True,
        "hybrid": hybrid,
    }
    r = client.post(f"{base}/rag/retrieve", json=body, headers=headers, timeout=120.0)
    r.raise_for_status()
    data = r.json()
    chunks = data.get("chunks")
    if not isinstance(chunks, list):
        raise ValueError("retrieve response missing chunks list")
    return chunks  # type: ignore[return-value]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--base-url",
        default=os.environ.get("RAG_EVAL_BASE_URL", "http://127.0.0.1:8080").rstrip("/"),
    )
    p.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL)
    p.add_argument("--top-k", type=int, default=6)
    p.add_argument("--rewrite", action=argparse.BooleanOptionalAction, default=False)
    args = p.parse_args()

    token = os.environ.get("RAG_SERVICE_TOKEN", "")
    if not token:
        print("RAG_SERVICE_TOKEN is required", file=sys.stderr)
        return 1

    enforce = os.environ.get("ENFORCE_THRESHOLDS", "").lower() in ("1", "true", "yes")
    jsonl = args.jsonl
    if not jsonl.is_file():
        print(f"jsonl not found: {jsonl}", file=sys.stderr)
        return 1

    rows: list[dict[str, str]] = []
    with jsonl.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            rows.append(
                {
                    "q": str(o["q"]),
                    "gold_doc_id": str(o["gold_doc_id"]),
                    "namespace": str(o.get("namespace", "kb")),
                }
            )

    n = len(rows)
    if n == 0:
        print("no questions in jsonl", file=sys.stderr)
        return 1

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    hybrid_hits = 0
    dense_hits = 0

    with httpx.Client() as client:
        for row in rows:
            q = row["q"]
            gold = row["gold_doc_id"]
            ns = row["namespace"]
            try:
                h_chunks = _retrieve(
                    client,
                    args.base_url,
                    headers,
                    query=q,
                    namespace=ns,
                    top_k=args.top_k,
                    hybrid=True,
                    rewrite=args.rewrite,
                )
                d_chunks = _retrieve(
                    client,
                    args.base_url,
                    headers,
                    query=q,
                    namespace=ns,
                    top_k=args.top_k,
                    hybrid=False,
                    rewrite=args.rewrite,
                )
            except (httpx.HTTPError, ValueError) as e:
                print(f"request failed: {e}", file=sys.stderr)
                return 1
            if _hit(h_chunks, gold, args.top_k):
                hybrid_hits += 1
            if _hit(d_chunks, gold, args.top_k):
                dense_hits += 1

    h_rate = hybrid_hits / n
    d_rate = dense_hits / n
    print(f"questions: {n}  top_k: {args.top_k}  rewrite: {args.rewrite}")
    print(f"hybrid   hit@{args.top_k}: {hybrid_hits}/{n} ({100.0 * h_rate:.1f}%)")
    print(f"dense    hit@{args.top_k}: {dense_hits}/{n} ({100.0 * d_rate:.1f}%)")

    if d_rate > 0:
        lift = (h_rate - d_rate) / d_rate
        print(f"relative lift (hybrid vs dense): {100.0 * lift:.1f}%")
        enforce_ok = lift >= 0.10
    elif h_rate > 0:
        print("relative lift (hybrid vs dense): n/a (dense hit rate 0%; hybrid > 0)")
        enforce_ok = True
    else:
        print("relative lift (hybrid vs dense): n/a (both hit rates 0%)")
        enforce_ok = False

    if enforce:
        if not enforce_ok:
            print(
                "ENFORCE_THRESHOLDS: failed (need ≥10% relative lift when dense>0, "
                "or hybrid>0 when dense=0)",
                file=sys.stderr,
            )
            return 1
        print("ENFORCE_THRESHOLDS: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
