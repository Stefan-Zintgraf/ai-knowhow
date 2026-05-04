"""Smoke: support-rag MCP exposes R-19 tool identifiers (discoverable)."""

from __future__ import annotations

import asyncio


def test_mcp_r19_tool_names() -> None:
    import support_rag.mcp_server as m

    tools = asyncio.run(m.mcp.list_tools())
    names = {t.name for t in tools}
    assert names >= {"rag.health", "rag.retrieve", "rag.index"}
