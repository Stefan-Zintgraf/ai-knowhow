"""R-2: `_rrf_k_lists` merge order matches reciprocal-rank fusion scoring (PRD)."""

from __future__ import annotations

from llama_index.core.schema import TextNode

from support_rag.service import _rrf_k_lists


def _rrf_weight(rrf_k: int, rank: int) -> float:
    return 1.0 / (rrf_k + rank + 1)


def test_two_lists_merged_order_matches_rrf_rule() -> None:
    """Hand-checked scores: same recurrence as `support_rag/rrf.py` / `reciprocal_rank_fusion`."""
    rrf_k = 2
    a = TextNode(id_="a", text="A", metadata={})
    b = TextNode(id_="b", text="B", metadata={})
    c = TextNode(id_="c", text="C", metadata={})
    rank_lists = [
        ("l1", [a, b]),
        ("l2", [c, a]),
    ]
    expected_scores = {
        "a": _rrf_weight(rrf_k, 0) + _rrf_weight(rrf_k, 1),
        "b": _rrf_weight(rrf_k, 1),
        "c": _rrf_weight(rrf_k, 0),
    }
    out = _rrf_k_lists(rank_lists, rrf_k=rrf_k, cap=10)
    want_order = sorted(
        expected_scores,
        key=lambda k: (expected_scores[k], k),
        reverse=True,
    )
    assert [n.id_ for n in out] == want_order
