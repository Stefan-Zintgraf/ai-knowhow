"""Optional (!RUN_INTEGRATION) live Qdrant: list collections (R-11, R-14 touchpoints).

Full §2.8#4 over HTTP is manual/E2E; offline path remains test_service_delete_erasure.
"""

from __future__ import annotations

import os

import pytest
from qdrant_client import QdrantClient

from support_rag.config import AppConfig


def _qdrant_url() -> str:
    u = (os.environ.get("RAG_QDRANT__URL") or os.environ.get("QDRANT_URL") or "").strip()
    if u:
        return u
    return AppConfig().qdrant.url


@pytest.mark.requires_services
def test_live_qdrant_lists_collections() -> None:
    url = _qdrant_url()
    client = QdrantClient(url=url, timeout=10.0)
    cols = client.get_collections()
    assert cols is not None
    assert hasattr(cols, "collections")


@pytest.mark.requires_services
def test_r14_qdrant_reachable_for_health_stores() -> None:
    """R-14: live Qdrant responds (partial proxy for health `stores.qdrant`)."""
    url = _qdrant_url()
    client = QdrantClient(url=url, timeout=10.0)
    r = client.get_collections()
    assert r.collections is not None  # not asserting non-empty: fresh installs may have none
