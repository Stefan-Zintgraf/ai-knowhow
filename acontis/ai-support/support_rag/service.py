"""RAGService — ingest, delete, retrieve, health."""

from __future__ import annotations

import json
import logging
import math
import time
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import VectorStoreQuery, VectorStoreQueryMode
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient, QdrantClient
from qdrant_client.http import models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse
from sentence_transformers import CrossEncoder

from support_rag.chunking import chunk_kb, chunk_tickets
from support_rag.config import AppConfig
from support_rag.embeddings import GatewayEmbeddings
from support_rag.gateway import LLMGatewayClient
from support_rag.qfilter import to_qdrant_filter
from support_rag.rrf import make_rrf_fusion_fn
from support_rag.schemas import (
    ChunkResult,
    IngestDocument,
    RetrievalRequest,
    RetrievalResponse,
)

logger = logging.getLogger(__name__)

NAMESPACES = ("kb", "tickets")


def _rrf_k_lists(
    rank_lists: list[tuple[str, list[TextNode]]],
    rrf_k: int,
    cap: int,
) -> list[TextNode]:
    """Merge ranked lists by RRF; dedupe by node id; cap at `cap` nodes."""
    if not rank_lists:
        return []
    if len(rank_lists) == 1:
        return [t for t in rank_lists[0][1][:cap] if isinstance(t, TextNode)]
    scores: dict[str, float] = defaultdict(float)
    nodes: dict[str, TextNode] = {}
    for _source, rlist in rank_lists:
        for rank, n in enumerate(rlist):
            if not isinstance(n, TextNode):
                continue
            nid = n.id_ or n.node_id
            nodes[nid] = n
            scores[nid] += 1.0 / (rrf_k + rank + 1)
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:cap]
    return [nodes[i] for i, _ in top if i in nodes]


class RAGService:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._gateway = LLMGatewayClient(config.llm_gateway)
        self._embed = GatewayEmbeddings(self._gateway, model_name="gateway")
        self._qdrant = QdrantClient(url=config.qdrant.url)
        self._qdrant_async = AsyncQdrantClient(url=config.qdrant.url)
        rrf_k = config.retrieval.rrf_k
        dsize = config.qdrant.vector_size
        dist = qmodels.Distance.COSINE
        dconf = qmodels.VectorParams(size=dsize, distance=dist)
        fusion_fn = make_rrf_fusion_fn(rrf_k)
        self._stores: dict[str, QdrantVectorStore] = {}
        self._indices: dict[str, VectorStoreIndex] = {}
        for ns in NAMESPACES:
            cname = f"{config.qdrant.collection_prefix}{ns}"
            vs = QdrantVectorStore(
                collection_name=cname,
                client=self._qdrant,
                aclient=self._qdrant_async,
                enable_hybrid=True,
                fastembed_sparse_model="Qdrant/bm25",
                dense_config=dconf,
                hybrid_fusion_fn=fusion_fn,
                batch_size=20,
            )
            self._stores[ns] = vs
            storage = StorageContext.from_defaults(vector_store=vs)
            self._indices[ns] = VectorStoreIndex.from_vector_store(
                vector_store=vs,
                storage_context=storage,
                embed_model=self._embed,
            )
        self._cross_encoder: CrossEncoder | None = None
        self._ce_model = config.retrieval.reranker.model
        self._ce_device = config.retrieval.reranker.device

    def rebind_config(self, config: AppConfig) -> None:
        """Point live retrieval/chunking/cross-encoder state at ``config`` without new clients."""
        old_ce = (self._ce_model, self._ce_device)
        self._config = config
        self._ce_model = config.retrieval.reranker.model
        self._ce_device = config.retrieval.reranker.device
        if old_ce != (self._ce_model, self._ce_device):
            self._cross_encoder = None
        self._gateway._config = config.llm_gateway

    async def aclose(self) -> None:
        await self._gateway.aclose()
        self._qdrant.close()
        await self._qdrant_async.close()

    def _ce(self) -> CrossEncoder:
        if self._cross_encoder is None:
            self._cross_encoder = CrossEncoder(self._ce_model, device=self._ce_device)
        return self._cross_encoder

    async def _rewrite_queries(self, q: str, trace_ctx: Mapping[str, str] | None) -> list[str]:
        cfg = self._config.retrieval.query_rewrite
        if not cfg.enabled:
            return []
        n = max(0, min(cfg.n_alternatives, 5))
        if n == 0:
            return []
        msg = self._gateway.chat_completion_sync(
            [
                {
                    "role": "user",
                    "content": (
                        f"Given the user search query, return JSON with up to {n} short alternative"
                        f' queries. Format: {{"alternatives": ["..."]}}. Original query: {q!r}'
                    ),
                }
            ],
            max_tokens=256,
            temperature=0.2,
            json_mode=True,
            trace_ctx=trace_ctx,
        )
        alts: list[str] = []
        try:
            j = json.loads(msg)
            raw = j.get("alternatives", [])
            for x in raw:
                s = str(x).strip()
                if s and s not in alts and s != q:
                    alts.append(s)
        except (json.JSONDecodeError, TypeError, ValueError):
            logger.warning("query rewrite T parse failed, skipping alternatives")
        return alts[:n]

    async def _hyde(self, q: str, trace_ctx: Mapping[str, str] | None) -> str:
        t = self._gateway.chat_completion_sync(
            [
                {
                    "role": "user",
                    "content": (
                        "Write a short hypothetical answer (2–4 sentences) for a support KB for "
                        f"this question (no specific tickets):\n{q!r}"
                    ),
                }
            ],
            max_tokens=256,
            temperature=0.2,
            trace_ctx=trace_ctx,
        )
        return t.strip()

    async def _query_one(
        self,
        namespace: str,
        qstr: str,
        qvec: list[float] | None,
        qf: qmodels.Filter | None,
        *,
        use_hybrid: bool,
    ) -> list[TextNode]:
        r = self._config.retrieval
        vs = self._stores[namespace]
        if use_hybrid:
            vq = VectorStoreQuery(
                query_str=qstr,
                query_embedding=qvec,
                similarity_top_k=r.top_k_dense,
                sparse_top_k=r.top_k_sparse,
                mode=VectorStoreQueryMode.HYBRID,
                alpha=0.5,
                hybrid_top_k=r.top_k_dense + r.top_k_sparse,
            )
        else:
            vq = VectorStoreQuery(
                query_str=qstr,
                query_embedding=qvec,
                similarity_top_k=r.top_k_dense,
                mode=VectorStoreQueryMode.DEFAULT,
            )
        try:
            res = await vs.aquery(vq, qdrant_filters=qf)
        except UnexpectedResponse as exc:
            if exc.status_code == 404:
                logger.debug(
                    "Collection for namespace %s not yet created, returning empty",
                    namespace,
                )
                return []
            raise
        if not res.nodes:
            return []
        return [n for n in res.nodes if isinstance(n, TextNode)]

    async def retrieve(
        self,
        req: RetrievalRequest,
        trace_ctx: Mapping[str, str] | None = None,
    ) -> tuple[RetrievalResponse, float]:
        t_all = time.perf_counter()
        r = self._config.retrieval
        q0 = req.query
        n_final = min(req.top_k, r.top_k_final)
        qf = to_qdrant_filter(req.filters)

        rewritten: list[str] = []
        q_core = q0
        if r.hyde.enabled:
            h = await self._hyde(q0, trace_ctx)
            q_core = f"{q0}\n\nHypothetical context:\n{h}"
        queries = [q_core]
        if req.rewrite and r.query_rewrite.enabled:
            alts = await self._rewrite_queries(q0, trace_ctx)
            rewritten = alts
            queries = [q_core, *alts]

        # namespace filter from payload (optional) intersects with req.namespaces
        ns_in = [n for n in req.namespaces if n in NAMESPACES]
        if not ns_in:
            ns_in = list(NAMESPACES)

        use_hybrid = r.hybrid if req.hybrid is None else req.hybrid
        rank_lists: list[tuple[str, list[TextNode]]] = []
        for qstr in queries:
            qe, _ = await self._gateway.embed([qstr], kind="query", trace_ctx=trace_ctx)
            qv = qe[0]
            for ns in ns_in:
                nodes = await self._query_one(ns, qstr, qv, qf, use_hybrid=use_hybrid)
                label = f"{qstr!r}@{ns}"
                rank_lists.append((label, nodes))

        merged = _rrf_k_lists(
            rank_lists,
            rrf_k=r.rrf_k,
            cap=max(60, n_final * 10),
        )
        if not merged:
            return (
                RetrievalResponse(
                    chunks=[],
                    rewritten_queries=rewritten,
                    debug={
                        "timings_s": time.perf_counter() - t_all,
                        "candidates": 0,
                        "hybrid": use_hybrid,
                    },
                ),
                time.perf_counter() - t_all,
            )

        if req.rerank:
            ce = self._ce()
            pairs: list[tuple[str, str]] = [(q0, n.get_content()) for n in merged]
            raw_scores: Any = ce.predict(
                pairs,
                batch_size=16,
                show_progress_bar=False,
            )
            # normalize / sigmoid-like squeeze to 0-1
            if hasattr(raw_scores, "tolist"):
                sc = [float(s) for s in raw_scores.tolist()]  # type: ignore[union-attr]
            else:
                sc = [float(x) for x in list(raw_scores)]
            def _sig(x: float) -> float:
                return 1.0 / (1.0 + math.exp(-x))

            norm = [_sig(s) for s in sc]
            ranked = sorted(zip(merged, norm, strict=True), key=lambda x: x[1], reverse=True)
            if req.min_score is not None:
                ranked = [x for x in ranked if x[1] >= float(req.min_score)]
            take = min(n_final, len(ranked))
            out: list[ChunkResult] = []
            for n, s in ranked[:take]:
                md = {**(dict(n.metadata) if n.metadata is not None else {})}
                out.append(
                    ChunkResult(
                        id=n.id_ or n.node_id,
                        text=n.get_content(),
                        metadata=md,
                        parent_id=str(md.get("parent_id", "")),
                        score=s,
                    )
                )
        else:
            out = []
            for n in merged[:n_final]:
                md = {**(dict(n.metadata) if n.metadata is not None else {})}
                s = 1.0
                if req.min_score is not None and s < float(req.min_score):
                    continue
                out.append(
                    ChunkResult(
                        id=n.id_ or n.node_id,
                        text=n.get_content(),
                        metadata=md,
                        parent_id=str(md.get("parent_id", "")),
                        score=None,
                    )
                )
        dt = time.perf_counter() - t_all
        return (
            RetrievalResponse(
                chunks=out,
                rewritten_queries=rewritten,
                debug={
                    "timings_s": dt,
                    "candidates_merged": len(merged),
                    "rerank": req.rerank,
                    "hybrid": use_hybrid,
                },
            ),
            dt,
        )

    async def index(
        self,
        namespace: str,
        docs: Sequence[IngestDocument | dict[str, Any]],
        trace_ctx: Mapping[str, str] | None = None,
    ) -> None:
        if namespace not in NAMESPACES:
            raise ValueError("invalid namespace")
        to_del: set[str] = set()
        all_nodes: list[TextNode] = []
        for d in docs:
            doc: IngestDocument
            if isinstance(d, IngestDocument):
                doc = d
            else:
                doc = IngestDocument.model_validate(d)
            to_del.add(doc.id)
            if namespace == "kb":
                nodes = chunk_kb(self._config, doc, namespace)
            else:
                nodes = chunk_tickets(self._config, doc, namespace)
            all_nodes.extend(nodes)
        for pid in to_del:
            await self._delete_one(namespace, pid)
        idx = self._indices[namespace]
        if all_nodes:
            first = [all_nodes[0].get_content()]
            _, em = self._gateway.embed_sync(first, kind="doc", trace_ctx=trace_ctx)
            em_model_stamped = str(em or "unknown")
            for n in all_nodes:
                n.metadata = {**dict(n.metadata), "embedding_model": em_model_stamped}
            await idx.ainsert_nodes(all_nodes, show_progress=False)

    async def _delete_one(self, namespace: str, parent_id: str) -> None:
        cname = f"{self._config.qdrant.collection_prefix}{namespace}"
        try:
            self._qdrant.delete(
                collection_name=cname,
                points_selector=qmodels.FilterSelector(
                    filter=qmodels.Filter(
                        must=[
                            qmodels.FieldCondition(
                                key="ref_doc_id",
                                match=qmodels.MatchValue(value=parent_id),
                            )
                        ],
                    )
                ),
            )
        except UnexpectedResponse as exc:
            if exc.status_code == 404:
                logger.debug("Collection %s not yet created, nothing to delete", cname)
            else:
                raise

    async def delete(
        self,
        namespace: str,
        parent_ids: Sequence[str],
        trace_ctx: Mapping[str, str] | None = None,
    ) -> None:
        for pid in parent_ids:
            await self._delete_one(namespace, pid)

    async def chat_complete(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        max_tokens: int = 1024,
        temperature: float = 0.2,
        trace_ctx: Mapping[str, str] | None = None,
    ) -> str:
        """Call the local LLM gateway (retrieval slot) for one-shot / UI chat turns."""
        return await self._gateway.chat_completion(
            messages,
            max_tokens=max_tokens,
            temperature=temperature,
            trace_ctx=trace_ctx,
        )

    async def health(self) -> dict[str, Any]:
        st = "ok"
        try:
            self._qdrant.get_collections()
        except (ConnectionError, OSError, RuntimeError) as e:
            logger.warning("Qdrant health: %s", e)
            st = "degraded"
        m = await self._gateway.describe_models()
        r = self._config.retrieval
        return {
            "status": st,
            "version": self._config.service.version,
            "contract_version": "1.0",
            "capabilities": {
                "hybrid": r.hybrid,
                "rerank": r.rerank_enabled,
                "graph": False,
                "namespaces": list(NAMESPACES),
            },
            "models": {
                "embedding": str(m.get("embedding", "unknown")),
                "retrieval_llm": str(m.get("retrieval_llm", "unknown")),
                "chat": str(m.get("chat", "unknown")),
                "reranker": self._ce_model,
            },
            "stores": {"qdrant": st},
        }
