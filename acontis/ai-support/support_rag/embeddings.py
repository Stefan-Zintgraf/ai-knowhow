"""Gateway-backed `BaseEmbedding` — all dense vectors go through LLM Gateway (R-15)."""

from __future__ import annotations

from typing import Any

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.bridge.pydantic import Field

from support_rag.gateway import LLMGatewayClient


class GatewayEmbeddings(BaseEmbedding):
    """Dense embeddings via `/v1/embeddings` + `X-Slot: embedding`."""

    gateway: Any = Field(description="LLMGatewayClient", exclude=True)

    @classmethod
    def class_name(cls) -> str:
        return "GatewayEmbeddings"

    def __init__(
        self,
        gateway: LLMGatewayClient,
        model_name: str = "gateway",
        **kwargs: Any,
    ) -> None:
        kwargs["model_name"] = model_name
        super().__init__(gateway=gateway, **kwargs)

    def _get_query_embedding(self, query: str) -> list[float]:
        vecs, _ = self.gateway.embed_sync([query], kind="query")
        return vecs[0]

    async def _aget_query_embedding(self, query: str) -> list[float]:
        vecs, _ = await self.gateway.embed([query], kind="query")
        return vecs[0]

    def _get_text_embedding(self, text: str) -> list[float]:
        vecs, _ = self.gateway.embed_sync([text], kind="doc")
        return vecs[0]

    async def _aget_text_embedding(self, text: str) -> list[float]:
        vecs, _ = await self.gateway.embed([text], kind="doc")
        return vecs[0]

    def _get_text_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vecs, _ = self.gateway.embed_sync(list(texts), kind="doc")
        return vecs

    async def _aget_text_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vecs, _ = await self.gateway.embed(list(texts), kind="doc")
        return vecs

    async def _aget_text_embeddings_rate_limited(self, texts: list[str]) -> list[list[float]]:
        return await self._aget_text_embeddings(texts)
