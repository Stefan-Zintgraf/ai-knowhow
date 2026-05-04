"""Live Qdrant + gateway: R-5 metadata filters, R-11 delete, R-12 replace-by-id, §2.8#4 erasure.

Requires ``RUN_INTEGRATION=1`` (see ``tests/conftest.py``). Also needs:

- Reachable Qdrant: ``RAG_QDRANT__URL`` or ``QDRANT_URL`` (else ``AppConfig`` / YAML default).
- Working LLM gateway for embeddings: ``RAG_LLM_GATEWAY__BASE_URL`` and optional ``RAG_LLM_GATEWAY__API_KEY``,
  plus YAML or env for ``vector_size`` matching the gateway embedding model.

Uses an isolated ``collection_prefix`` per test module run to avoid clobbering shared collections.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator

import pytest
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse

from support_rag.config import AppConfig, QueryRewriteConfig, load_config
from support_rag.schemas import IngestDocument, RetrievalRequest
from support_rag.service import RAGService


def _itest_app_config() -> AppConfig:
    base = load_config()
    prefix = f"support_rag_itest_{uuid.uuid4().hex[:12]}_"
    qconf = base.qdrant.model_copy(update={"collection_prefix": prefix})
    rq = base.retrieval.query_rewrite.model_copy(update={"enabled": False})
    hy = base.retrieval.hyde.model_copy(update={"enabled": False})
    rconf = base.retrieval.model_copy(
        update={
            "rerank_enabled": False,
            "hybrid": False,
            "query_rewrite": rq,
            "hyde": hy,
        }
    )
    return base.model_copy(update={"qdrant": qconf, "retrieval": rconf})


def _count_ref_doc(client: QdrantClient, cfg: AppConfig, namespace: str, parent_id: str) -> int:
    cname = f"{cfg.qdrant.collection_prefix}{namespace}"
    try:
        r = client.count(
            collection_name=cname,
            count_filter=qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="ref_doc_id",
                        match=qmodels.MatchValue(value=parent_id),
                    )
                ]
            ),
            exact=True,
        )
        return int(r.count)
    except UnexpectedResponse as exc:
        if exc.status_code == 404:
            return 0
        raise


@pytest.fixture
async def isolated_live_rag() -> AsyncIterator[tuple[RAGService, QdrantClient, AppConfig]]:
    cfg = _itest_app_config()
    client = QdrantClient(url=cfg.qdrant.url, timeout=120.0)
    svc = RAGService(cfg)
    try:
        yield svc, client, cfg
    finally:
        await svc.aclose()
        for ns in ("kb", "tickets"):
            cname = f"{cfg.qdrant.collection_prefix}{ns}"
            try:
                client.delete_collection(collection_name=cname)
            except Exception:
                pass
        client.close()


@pytest.mark.requires_services
@pytest.mark.asyncio
async def test_r5_filters_hit_and_miss_live(isolated_live_rag: tuple[RAGService, QdrantClient, AppConfig]) -> None:
    svc, _client, _cfg = isolated_live_rag
    doc_id = "r5-doc-1"
    marker = "MVP1_R5_FILTER_LIVE_MARKER"
    text = (
        f"{marker} EtherCAT master redundancy ENI cycle time. "
        + " ".join(f"seg{n}" for n in range(120))
    )
    await svc.index(
        "kb",
        [
            IngestDocument(
                id=doc_id,
                text=text,
                metadata={
                    "product": "mvp1_ec_filter",
                    "lang": "en",
                    "status": "open",
                    "created_at": 1_704_067_200,
                },
            )
        ],
        trace_ctx={},
    )
    base_req = RetrievalRequest(
        query=f"{marker} EtherCAT",
        top_k=8,
        namespaces=["kb"],
        rewrite=False,
        rerank=False,
        hybrid=False,
    )
    res_open, _ = await svc.retrieve(base_req, trace_ctx={})
    assert res_open.chunks, "expected hits without contradictory filters"
    assert all(c.parent_id == doc_id for c in res_open.chunks)

    res_hit, _ = await svc.retrieve(
        base_req.model_copy(update={"filters": {"product": "mvp1_ec_filter"}}),
        trace_ctx={},
    )
    assert res_hit.chunks
    assert all(
        str(c.metadata.get("product")) == "mvp1_ec_filter" for c in res_hit.chunks
    )

    res_miss, _ = await svc.retrieve(
        base_req.model_copy(update={"filters": {"product": "mvp1_ec_other"}}),
        trace_ctx={},
    )
    assert not res_miss.chunks


@pytest.mark.requires_services
@pytest.mark.asyncio
async def test_r11_delete_removes_points_live(isolated_live_rag: tuple[RAGService, QdrantClient, AppConfig]) -> None:
    svc, client, cfg = isolated_live_rag
    doc_id = "r11-doc-1"
    text = "R11_DELETE_LIVE " + " ".join(f"w{n}" for n in range(80))
    await svc.index(
        "kb",
        [IngestDocument(id=doc_id, text=text, metadata={"product": "p11"})],
        trace_ctx={},
    )
    n_before = _count_ref_doc(client, cfg, "kb", doc_id)
    assert n_before > 0
    await svc.delete("kb", [doc_id], trace_ctx={})
    n_after = _count_ref_doc(client, cfg, "kb", doc_id)
    assert n_after == 0


@pytest.mark.requires_services
@pytest.mark.asyncio
async def test_r12_reindex_replaces_content_live(
    isolated_live_rag: tuple[RAGService, QdrantClient, AppConfig],
) -> None:
    svc, _client, _cfg = isolated_live_rag
    doc_id = "r12-doc-1"
    old_marker = "R12_UNIQUE_OLD_CONTENT"
    new_marker = "R12_UNIQUE_NEW_CONTENT"
    long_old = f"{old_marker} " + " ".join(f"old{n}" for n in range(200))
    short_new = f"{new_marker} " + " ".join(f"new{n}" for n in range(80))

    await svc.index(
        "kb",
        [IngestDocument(id=doc_id, text=long_old, metadata={"product": "r12"})],
        trace_ctx={},
    )
    pre_old, _ = await svc.retrieve(
        RetrievalRequest(
            query=old_marker,
            top_k=6,
            namespaces=["kb"],
            rewrite=False,
            rerank=False,
            hybrid=False,
        ),
        trace_ctx={},
    )
    assert pre_old.chunks

    await svc.index(
        "kb",
        [IngestDocument(id=doc_id, text=short_new, metadata={"product": "r12"})],
        trace_ctx={},
    )
    post_old, _ = await svc.retrieve(
        RetrievalRequest(
            query=old_marker,
            top_k=6,
            namespaces=["kb"],
            rewrite=False,
            rerank=False,
            hybrid=False,
        ),
        trace_ctx={},
    )
    assert not post_old.chunks, "old generation should be replaced"

    post_new, _ = await svc.retrieve(
        RetrievalRequest(
            query=new_marker,
            top_k=6,
            namespaces=["kb"],
            rewrite=False,
            rerank=False,
            hybrid=False,
        ),
        trace_ctx={},
    )
    assert post_new.chunks
    assert all(new_marker in c.text for c in post_new.chunks)


@pytest.mark.requires_services
@pytest.mark.asyncio
async def test_erasure_retrieve_empty_after_delete_live(
    isolated_live_rag: tuple[RAGService, QdrantClient, AppConfig],
) -> None:
    svc, _client, _cfg = isolated_live_rag
    doc_id = "erase-doc-1"
    marker = "ERASURE_LIVE_MARKER"
    text = f"{marker} support content " + " ".join(f"x{n}" for n in range(60))
    await svc.index(
        "kb",
        [IngestDocument(id=doc_id, text=text, metadata={"product": "erase_p"})],
        trace_ctx={},
    )
    pre, _ = await svc.retrieve(
        RetrievalRequest(
            query=marker,
            top_k=4,
            namespaces=["kb"],
            filters={"parent_id": doc_id},
            rewrite=False,
            rerank=False,
            hybrid=False,
        ),
        trace_ctx={},
    )
    assert pre.chunks

    await svc.delete("kb", [doc_id], trace_ctx={})

    post, _ = await svc.retrieve(
        RetrievalRequest(
            query=marker,
            top_k=4,
            namespaces=["kb"],
            filters={"parent_id": doc_id},
            rewrite=False,
            rerank=False,
            hybrid=False,
        ),
        trace_ctx={},
    )
    assert not post.chunks
