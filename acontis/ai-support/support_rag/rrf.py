"""Reciprocal Rank Fusion for dense+sparse `VectorStoreQueryResult` (PRD: fusion rrf, rrf_k)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from llama_index.core.schema import BaseNode
from llama_index.core.vector_stores import VectorStoreQueryResult


def reciprocal_rank_fusion(
    dense_result: VectorStoreQueryResult,
    sparse_result: VectorStoreQueryResult,
    **kwargs: Any,
) -> VectorStoreQueryResult:
    """
    RRF: score(node) = sum 1 / (k + rank_i) across rankings.
    `top_k` caps how many unique nodes to return after sorting by score.
    `rrf_k` is the RRF offset (PRD default 60).
    """
    rrf_k = int(kwargs.get("rrf_k", 60))
    top_k = int(kwargs.get("top_k", 60))
    if top_k < 1:
        top_k = 1

    scores: dict[str, float] = defaultdict(float)
    nodes: dict[str, BaseNode] = {}

    def walk(result: VectorStoreQueryResult) -> None:
        if not result.nodes:
            return
        for rank, node in enumerate(result.nodes):
            nid = node.node_id
            nodes[nid] = node
            scores[nid] += 1.0 / (rrf_k + rank + 1)

    walk(dense_result)
    walk(sparse_result)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    if not ranked:
        return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])
    out_nodes = [nodes[nid] for nid, _ in ranked if nid in nodes]
    out_sims = [s for _, s in ranked]
    return VectorStoreQueryResult(
        nodes=out_nodes,
        similarities=out_sims,
        ids=[n.node_id for n in out_nodes],
    )


def make_rrf_fusion_fn(rrf_k: int):
    def fn(
        dr: VectorStoreQueryResult,
        sr: VectorStoreQueryResult,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        kws = {**kwargs, "rrf_k": rrf_k}
        return reciprocal_rank_fusion(dr, sr, **kws)

    return fn
