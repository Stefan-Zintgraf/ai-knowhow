"""Unit: `qfilter.to_qdrant_filter` (R-5) → Qdrant `Filter` shapes."""

from __future__ import annotations

from qdrant_client import models

from support_rag.qfilter import to_qdrant_filter


def test_empty_or_none_yields_none() -> None:
    assert to_qdrant_filter(None) is None
    assert to_qdrant_filter({}) is None


def test_scalar_equality() -> None:
    f = to_qdrant_filter({"product": "ec_master", "namespace": "kb"})
    assert f is not None
    assert len(f.must) == 2
    keys = {c.key for c in f.must}
    assert keys == {"product", "namespace"}
    for c in f.must:
        if c.key == "product":
            assert isinstance(c.match, models.MatchValue)
            assert c.match.value == "ec_master"  # type: ignore[union-attr]
        if c.key == "namespace":
            assert isinstance(c.match, models.MatchValue)
            assert c.match.value == "kb"  # type: ignore[union-attr]


def test_in_as_list() -> None:
    f = to_qdrant_filter({"lang": ["de", "en", "fr"]})
    assert f is not None
    assert len(f.must) == 1
    c = f.must[0]
    assert c.key == "lang"
    assert isinstance(c.match, models.MatchAny)
    assert list(c.match.any) == ["de", "en", "fr"]  # type: ignore[union-attr]


def test_in_with_dollar_key() -> None:
    f = to_qdrant_filter({"status": {"$in": ["open", "closed"]}})
    assert f is not None
    c = f.must[0]
    assert c.key == "status"
    assert isinstance(c.match, models.MatchAny)
    assert list(c.match.any) == ["open", "closed"]  # type: ignore[union-attr]


def test_created_at_range_dollar_gte_lte() -> None:
    """Qdrant `Range` uses numeric bounds in this client version."""
    f = to_qdrant_filter(
        {
            "created_at": {
                "$gte": 1704067200.0,
                "$lte": 1735603199.0,
            }
        }
    )
    assert f is not None
    assert len(f.must) == 1
    c = f.must[0]
    assert c.key == "created_at"
    r = c.range
    assert r is not None
    assert r.gte == 1704067200.0  # type: ignore[union-attr]
    assert r.lte == 1735603199.0  # type: ignore[union-attr]


def test_created_at_range_short_keys() -> None:
    f = to_qdrant_filter({"created_at": {"gte": 1, "lte": 2}})
    assert f is not None
    c = f.must[0]
    r = c.range
    assert r is not None
    assert r.gte == 1  # type: ignore[union-attr]
    assert r.lte == 2  # type: ignore[union-attr]


def test_created_at_gte_only() -> None:
    f = to_qdrant_filter({"created_at": {"$gte": 1000}})
    assert f is not None
    c = f.must[0]
    r = c.range
    assert r is not None
    assert r.gte == 1000  # type: ignore[union-attr]
    assert r.lte is None  # type: ignore[union-attr]


def test_created_at_lte_only() -> None:
    f = to_qdrant_filter({"created_at": {"$lte": 2000}})
    assert f is not None
    c = f.must[0]
    r = c.range
    assert r is not None
    assert r.gte is None  # type: ignore[union-attr]
    assert r.lte == 2000  # type: ignore[union-attr]


def test_unknown_keys_dropped_others_kept() -> None:
    f = to_qdrant_filter({"not_allowed": 1, "parent_id": "p-1"})
    assert f is not None
    assert len(f.must) == 1
    assert f.must[0].key == "parent_id"
    assert isinstance(f.must[0].match, models.MatchValue)
    assert f.must[0].match.value == "p-1"  # type: ignore[union-attr]


def test_all_disallowed_or_null_yields_none() -> None:
    assert to_qdrant_filter({"foo": 1, "bar": 2}) is None
    assert to_qdrant_filter({"product": None, "lang": None}) is None
