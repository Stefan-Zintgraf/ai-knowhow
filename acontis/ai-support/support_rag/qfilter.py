"""Map PRD `filters` JSON to Qdrant `Filter` (R-5)."""

from __future__ import annotations

from typing import Any

from qdrant_client import models

ALLOWED = frozenset({"product", "lang", "created_at", "status", "namespace", "parent_id"})


def to_qdrant_filter(filters: dict[str, Any] | None) -> models.Filter | None:
    if not filters:
        return None
    must: list[models.FieldCondition] = []
    for key, val in filters.items():
        if key not in ALLOWED or val is None:
            continue
        if key == "created_at" and isinstance(val, dict):
            ge = val.get("$gte", val.get("gte"))
            le = val.get("$lte", val.get("lte"))
            if ge is not None and le is not None:
                must.append(
                    models.FieldCondition(
                        key="created_at",
                        range=models.Range(
                            gte=ge,
                            lte=le,
                        ),
                    )
                )
            elif ge is not None:
                must.append(
                    models.FieldCondition(
                        key="created_at",
                        range=models.Range(gte=ge),
                    )
                )
            elif le is not None:
                must.append(
                    models.FieldCondition(
                        key="created_at",
                        range=models.Range(lte=le),
                    )
                )
            continue
        if isinstance(val, list) or (isinstance(val, dict) and "$in" in val):
            opts = val["$in"] if isinstance(val, dict) and "$in" in val else val
            if not isinstance(opts, list):
                continue
            must.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchAny(any=opts),
                )
            )
        else:
            must.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=val),
                )
            )
    if not must:
        return None
    return models.Filter(must=must)
