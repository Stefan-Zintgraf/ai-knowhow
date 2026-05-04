"""Wire shapes for RAG API — aligned with `support_prd.md` §12.5."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

Namespace = Literal["kb", "tickets"]


class IngestDocument(BaseModel):
    id: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class IndexRequest(BaseModel):
    docs: list[IngestDocument]


class DeleteRequest(BaseModel):
    ids: list[str]  # parent document ids in this namespace (support_prd wire format)


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 6
    namespaces: list[str] = Field(default_factory=lambda: ["kb", "tickets"])
    filters: dict[str, Any] | None = None
    rewrite: bool = True
    rerank: bool = True
    min_score: float | None = None
    hybrid: bool | None = None


class ChunkResult(BaseModel):
    id: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    parent_id: str
    score: float | None = None


class RetrievalResponse(BaseModel):
    chunks: list[ChunkResult]
    rewritten_queries: list[str] = Field(default_factory=list)
    debug: dict[str, Any] = Field(default_factory=dict)
