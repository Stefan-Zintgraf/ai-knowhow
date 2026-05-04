"""R-18: CrossEncoder path.

**Merge gate:** `test_reranker_model_id_frozen_on_service` (run with `pytest -m "not slow"`;
no Hub download).

**Optional:** `test_r18_cross_encoder_instantiate_smoke` is `@pytest.mark.slow` and may skip
when Hub is unreachable or `TRANSFORMERS_OFFLINE=1`. See README and `.gitlab-ci.yml`.
"""

from __future__ import annotations

import os
from typing import Any

import pytest
from sentence_transformers import CrossEncoder

from support_rag.service import RAGService


def test_reranker_model_id_frozen_on_service(rag_service_offline: Any) -> None:
    """R-18: `RAGService` uses `retrieval.reranker.model` when `_ce()` loads `CrossEncoder`."""
    svc: RAGService = rag_service_offline
    assert svc._ce_model == svc._config.retrieval.reranker.model
    assert isinstance(svc._ce_model, str) and len(svc._ce_model) > 0


@pytest.mark.slow
def test_r18_cross_encoder_instantiate_smoke() -> None:
    if os.environ.get("TRANSFORMERS_OFFLINE", "").lower() in ("1", "true", "yes"):
        pytest.skip("TRANSFORMERS_OFFLINE set; skip model download (CI-friendly)")
    try:
        ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")
        scores = ce.predict([["doc", "q"]], show_progress_bar=False)
    except Exception as exc:  # noqa: BLE001 — optional Hub load; skip when offline/unauthorized
        pytest.skip(f"CrossEncoder load skipped (Hub/cache): {exc}")
    assert len(scores) == 1
