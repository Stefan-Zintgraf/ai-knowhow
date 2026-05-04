"""
MCP stdio server: proxies to the support-rag REST API (R-19, R-20).
Needs a running RAG service. Env: RAG_MCP_BASE_URL (default http://127.0.0.1:8080),
RAG_SERVICE_TOKEN, RAG_ADMIN_TOKEN.
"""

from __future__ import annotations

import json
import os

import httpx
from mcp.server.fastmcp import FastMCP

from support_rag.schemas import RetrievalRequest


def _base() -> str:
    return os.environ.get("RAG_MCP_BASE_URL", "http://127.0.0.1:8080").rstrip("/")


def _h(service: bool) -> dict[str, str]:
    if service:
        t = os.environ.get("RAG_SERVICE_TOKEN", "")
    else:
        t = os.environ.get("RAG_ADMIN_TOKEN", "")
    if not t:
        raise RuntimeError("Set RAG_SERVICE_TOKEN" if service else "Set RAG_ADMIN_TOKEN")
    return {"Authorization": f"Bearer {t}", "Content-Type": "application/json"}


mcp = FastMCP("support-rag")


@mcp.tool(name="rag.health")
async def rag_health() -> str:
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{_base()}/rag/health", headers=_h(True), timeout=60.0)
        r.raise_for_status()
        return json.dumps(r.json(), ensure_ascii=False)


@mcp.tool(name="rag.retrieve")
async def rag_retrieve(
    query: str,
    top_k: int = 6,
    namespaces: list[str] | None = None,
    rewrite: bool = True,
    rerank: bool = True,
    min_score: float | None = None,
) -> str:
    body = RetrievalRequest(
        query=query,
        top_k=top_k,
        namespaces=namespaces or ["kb", "tickets"],
        filters=None,
        rewrite=rewrite,
        rerank=rerank,
        min_score=min_score,
    )
    async with httpx.AsyncClient() as c:
        r = await c.post(
            f"{_base()}/rag/retrieve",
            content=body.model_dump_json(),
            headers=_h(True),
            timeout=120.0,
        )
        r.raise_for_status()
        return r.text


@mcp.tool(name="rag.index", description="Admin: index documents (requires RAG_ADMIN_TOKEN).")
async def rag_index(
    namespace: str,
    docs: str,
) -> str:
    """
    `docs`: JSON array of {id, text, metadata?} (IndexRequest docs list).
    """
    data = json.loads(docs) if isinstance(docs, str) else docs
    async with httpx.AsyncClient() as c:
        r = await c.post(
            f"{_base()}/rag/index/{namespace}",
            json={"docs": data},
            headers=_h(False),
            timeout=600.0,
        )
        r.raise_for_status()
        return r.text


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
