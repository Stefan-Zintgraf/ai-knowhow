"""Live E2E: minimal index + retrieve on a running RAG (LiteLLM + Ollama + Qdrant behind it).

Set `RUN_E2E_PRIVACY=1` and run with the stack in `docs/runbook-allow-remote-false-e2e.md`
(LiteLLM 4000, RAG 8080, Qdrant 6333). `RAG_CONFIG` should point at the same `llm_gateway.base_url`
as the running RAG (e.g. `config.e2e.yaml`).

Also set `RAG_SERVICE_TOKEN` and `RAG_ADMIN_TOKEN` to match the running `support_rag` process.
"""

from __future__ import annotations

import os
from typing import Any

import httpx
import pytest

_E2E_BASE = os.environ.get("E2E_RAG_BASE_URL", "http://127.0.0.1:8080")
_DOC: dict[str, Any] = {
    "docs": [{"id": "e2e-privacy-1", "text": "hello e2e privacy", "metadata": {}}],
}


@pytest.mark.e2e_privacy
@pytest.mark.usefixtures("e2e_gateway_preflight")
def test_index_and_retrieve_httpx_200() -> None:
    st = os.environ.get("RAG_SERVICE_TOKEN", "")
    ad = os.environ.get("RAG_ADMIN_TOKEN", "")
    if not st or not ad:
        pytest.skip("set RAG_SERVICE_TOKEN and RAG_ADMIN_TOKEN to match the live RAG process")

    with httpx.Client(base_url=_E2E_BASE, timeout=120.0) as c:
        h = c.get("/rag/health", headers={"Authorization": f"Bearer {st}"})
        assert h.status_code == 200, h.text

        idx = c.post(
            "/rag/index/kb",
            headers={"Authorization": f"Bearer {ad}"},
            json=_DOC,
        )
        assert idx.status_code == 200, idx.text

        r = c.post(
            "/rag/retrieve",
            headers={"Authorization": f"Bearer {st}"},
            json={"query": "hello e2e", "top_k": 2},
        )
        assert r.status_code == 200, r.text
        data = r.json()
        assert "chunks" in data
        # Non-deterministic; allow empty or non-empty.
        assert isinstance(data["chunks"], list)
