#!/usr/bin/env python3
"""
NFR-1 / NFR-2 smoke: p95 single-retrieve latency and 5-way concurrent success.

Lives on the self-hosted / scheduled GitLab path with a real stack. Default is
report-only (exit 0). Set NFR_ENFORCE=1 to fail when p95 exceeds NFR_P95_BUDGET_SEC
or any concurrent call errors.

Env:
  RAG_SERVICE_TOKEN   — required
  NFR_ENFORCE         — "1" / "true" to exit non-zero on SLO breach
  NFR_P95_BUDGET_SEC  — default 2.0 (PRD)
  NFR_P95_SAMPLES     — default 20 sequential retrieves for p95
  NFR_CONCURRENT      — default 5 parallel requests (PRD)
  NFR_SMOKE_QUERY     — override question text; else first line of eval/golden/questions.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSONL = REPO_ROOT / "eval" / "golden" / "questions.jsonl"


def _p95_ms(samples_ms: list[float]) -> float:
    if not samples_ms:
        return 0.0
    s = sorted(samples_ms)
    idx = int(math.ceil(0.95 * len(s))) - 1
    return s[max(0, idx)]


def _one_retrieve(
    base: str,
    headers: dict[str, str],
    query: str,
    namespace: str,
) -> None:
    body = {
        "query": query,
        "top_k": 6,
        "namespaces": [namespace],
        "rewrite": False,
        "rerank": True,
        "hybrid": True,
    }
    with httpx.Client() as client:
        r = client.post(f"{base}/rag/retrieve", json=body, headers=headers, timeout=120.0)
        r.raise_for_status()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--base-url",
        default=os.environ.get("RAG_EVAL_BASE_URL", "http://127.0.0.1:8080").rstrip("/"),
    )
    p.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL)
    args = p.parse_args()

    token = os.environ.get("RAG_SERVICE_TOKEN", "")
    if not token:
        print("RAG_SERVICE_TOKEN is required", file=sys.stderr)
        return 1

    enforce = os.environ.get("NFR_ENFORCE", "").lower() in ("1", "true", "yes")
    budget = float(os.environ.get("NFR_P95_BUDGET_SEC", "2.0"))
    n_seq = int(os.environ.get("NFR_P95_SAMPLES", "20"))
    n_par = int(os.environ.get("NFR_CONCURRENT", "5"))

    query: str
    namespace = "kb"
    env_q = os.environ.get("NFR_SMOKE_QUERY", "").strip()
    if env_q:
        query = env_q
    else:
        js = args.jsonl
        if not js.is_file():
            print(f"jsonl not found: {js}", file=sys.stderr)
            return 1
        with js.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                o = json.loads(line)
                query = str(o["q"])
                namespace = str(o.get("namespace", "kb"))
                break
            else:
                print("no questions in jsonl", file=sys.stderr)
                return 1

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    base = args.base_url
    samples_ms: list[float] = []

    for _ in range(n_seq):
        t0 = time.perf_counter()
        try:
            _one_retrieve(base, headers, query, namespace)
        except (httpx.HTTPError, OSError) as e:
            print(f"sequential request failed: {e}", file=sys.stderr)
            if enforce:
                return 1
            samples_ms.append(float("inf"))
            continue
        samples_ms.append((time.perf_counter() - t0) * 1000.0)

    finite = [x for x in samples_ms if x != float("inf")]
    p95 = _p95_ms(finite) / 1000.0 if finite else float("inf")

    conc_errors = 0
    with ThreadPoolExecutor(max_workers=n_par) as pool:
        futs = [
            pool.submit(_one_retrieve, base, headers, query, namespace) for _ in range(n_par)
        ]
        for f in as_completed(futs):
            try:
                f.result()
            except Exception as e:
                conc_errors += 1
                print(f"concurrent request failed: {e}", file=sys.stderr)

    print(
        f"nfr_retrieve_smoke: p95={p95:.3f}s (budget={budget}s)  "
        f"seq_samples={n_seq}  concurrent={n_par}  concurrent_errors={conc_errors}  "
        f"enforce={enforce}"
    )

    if not enforce:
        return 0

    ok = p95 <= budget and conc_errors == 0 and math.isfinite(p95)
    if not ok:
        print("NFR_ENFORCE: failed (p95 budget and/or zero concurrent errors)", file=sys.stderr)
        return 1
    print("NFR_ENFORCE: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
