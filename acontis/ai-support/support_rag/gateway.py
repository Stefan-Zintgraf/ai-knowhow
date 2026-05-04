"""LLM Gateway client — `httpx` only (R-17: no OpenAI/Anthropic/Ollama SDKs)."""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping, Sequence
from typing import Any, Literal

import httpx

from support_rag.config import LlmGatewayConfig

logger = logging.getLogger(__name__)


def _http_err_detail(response: httpx.Response | None) -> str:
    if response is None:
        return ""
    try:
        t = response.text
    except Exception:  # noqa: BLE001
        return ""
    if not t:
        return ""
    return f" ({t[:1_200]!r}{'...' if len(t) > 1_200 else ''})"

EmbeddingKind = Literal["doc", "query"]


class LLMGatewayClient:
    def __init__(self, config: LlmGatewayConfig) -> None:
        self._config = config
        self._base = config.base_url.rstrip("/")
        to = httpx.Timeout(config.timeout_s)
        # Ollama first load on /api/embed is often much slower than LiteLLM; avoid ReadTimeout.
        ollama_to = httpx.Timeout(max(300.0, float(config.timeout_s)))
        self._ollama_base = (config.ollama_embed_base_url or "").strip().rstrip("/")
        self._ollama_model = (config.ollama_embed_model or "").strip()
        self._use_ollama_embed = bool(self._ollama_base and self._ollama_model)
        default_headers: dict[str, str] = {}
        k = (config.api_key or "").strip()
        if k:
            default_headers["Authorization"] = f"Bearer {k}"
        # Ignore system HTTP(S)_PROXY so local gateway is not sent through a corporate proxy.
        self._client = httpx.AsyncClient(
            base_url=self._base,
            timeout=to,
            headers=default_headers,
            trust_env=False,
        )
        self._sync = httpx.Client(
            base_url=self._base,
            timeout=to,
            headers=default_headers,
            trust_env=False,
        )
        # Direct Ollama /api/embed (no LiteLLM) — E2E-friendly; does not use gateway Authorization.
        self._ollama_client: httpx.Client | None = None
        self._ollama_aclient: httpx.AsyncClient | None = None
        if self._use_ollama_embed:
            self._ollama_client = httpx.Client(
                base_url=self._ollama_base,
                timeout=ollama_to,
                trust_env=False,
            )
            self._ollama_aclient = httpx.AsyncClient(
                base_url=self._ollama_base,
                timeout=ollama_to,
                trust_env=False,
            )

    async def aclose(self) -> None:
        await self._client.aclose()
        self._sync.close()
        if self._ollama_aclient is not None:
            await self._ollama_aclient.aclose()
        if self._ollama_client is not None:
            self._ollama_client.close()

    def close_sync(self) -> None:
        self._sync.close()
        if self._ollama_client is not None:
            self._ollama_client.close()

    def _ollama_trace_headers(
        self, trace_ctx: Mapping[str, str] | None
    ) -> dict[str, str]:
        h: dict[str, str] = {
            "Content-Type": "application/json",
            "X-Slot": self._config.embedding_slot,
        }
        if trace_ctx:
            for k, v in trace_ctx.items():
                if v:
                    h[k] = v
        return h

    @staticmethod
    def _parse_ollama_embed_response(data: dict[str, Any]) -> tuple[list[list[float]], str | None]:
        embs = data.get("embeddings")
        if not embs and isinstance(data.get("embedding"), list):
            embs = [data["embedding"]]
        if not isinstance(embs, list) or not embs:
            raise ValueError("Ollama embed response missing 'embeddings' list")
        m = data.get("model")
        mret = m if isinstance(m, str) else None
        if all(isinstance(x, (int, float)) for x in embs):
            return [[float(x) for x in embs]], mret
        out: list[list[float]] = []
        for e in embs:
            if isinstance(e, list) and (not e or all(isinstance(x, (int, float)) for x in e)):
                out.append([float(x) for x in e])  # type: ignore[misc, arg-type]
            else:
                raise ValueError("invalid embedding item from Ollama")
        return out, mret

    def _clip_ollama_inputs(self, texts: Sequence[str]) -> list[str]:
        lim = int(getattr(self._config, "ollama_embed_truncate_chars", 0) or 0)
        out: list[str] = []
        for t in texts:
            if lim > 0 and len(t) > lim:
                logger.debug(
                    "ollama embed: clipping input from %d to %d chars", len(t), lim
                )
                out.append(t[:lim])
            else:
                out.append(t)
        return out

    def _ollama_embed_direct_sync(
        self,
        texts: Sequence[str],
        *,
        trace_ctx: Mapping[str, str] | None,
    ) -> tuple[list[list[float]], str | None]:
        """One HTTP request per text: avoids batch + context-length issues on small models."""
        if not texts:
            return [], None
        assert self._ollama_client is not None
        clipped = self._clip_ollama_inputs(texts)
        all_vecs: list[list[float]] = []
        model_ret: str | None = None
        for t in clipped:
            body: dict[str, Any] = {
                "model": self._ollama_model,
                "input": t,
                "truncate": True,
            }
            r = self._ollama_client.post(
                "/api/embed",
                json=body,
                headers=self._ollama_trace_headers(trace_ctx),
            )
            if r.is_error:
                raise httpx.HTTPStatusError(
                    f"Error {r.status_code} for {r.request.url!r}{_http_err_detail(r)}",
                    request=r.request,
                    response=r,
                )
            vecs, m = self._parse_ollama_embed_response(r.json())
            all_vecs.extend(vecs)
            if m:
                model_ret = m
        return all_vecs, model_ret

    async def _ollama_embed_direct_async(
        self,
        texts: Sequence[str],
        *,
        trace_ctx: Mapping[str, str] | None,
    ) -> tuple[list[list[float]], str | None]:
        if not texts:
            return [], None
        assert self._ollama_aclient is not None
        clipped = self._clip_ollama_inputs(texts)
        all_vecs: list[list[float]] = []
        model_ret: str | None = None
        for t in clipped:
            body: dict[str, Any] = {
                "model": self._ollama_model,
                "input": t,
                "truncate": True,
            }
            r = await self._ollama_aclient.post(
                "/api/embed",
                json=body,
                headers=self._ollama_trace_headers(trace_ctx),
            )
            if r.is_error:
                raise httpx.HTTPStatusError(
                    f"Error {r.status_code} for {r.request.url!r}{_http_err_detail(r)}",
                    request=r.request,
                    response=r,
                )
            vecs, m = self._parse_ollama_embed_response(r.json())
            all_vecs.extend(vecs)
            if m:
                model_ret = m
        return all_vecs, model_ret

    def embed_sync(
        self,
        texts: Sequence[str],
        *,
        kind: EmbeddingKind,
        trace_ctx: Mapping[str, str] | None = None,
    ) -> tuple[list[list[float]], str | None]:
        """Synchronous embeddings for LlamaIndex sync embedding paths (no provider SDK)."""
        if self._use_ollama_embed and self._ollama_client is not None:
            return self._ollama_embed_direct_sync(texts, trace_ctx=trace_ctx)

        slot = self._config.embedding_slot
        body: dict[str, Any] = {"input": list(texts), "model": "embedding"}
        r = self._sync.post(
            "/v1/embeddings",
            json=body,
            headers=self._slot_headers(slot, trace_ctx),
        )
        if r.is_error:
            raise httpx.HTTPStatusError(
                f"Error {r.status_code} for {r.request.url!r}{_http_err_detail(r)}",
                request=r.request,
                response=r,
            )
        data = r.json()
        data_list = data.get("data", [])
        vecs = [
            item["embedding"]
            for item in sorted(data_list, key=lambda d: d.get("index", 0))
        ]
        return vecs, data.get("model")

    def chat_completion_sync(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        slot: str | None = None,
        max_tokens: int = 256,
        temperature: float = 0.2,
        json_mode: bool = False,
        trace_ctx: Mapping[str, str] | None = None,
    ) -> str:
        s = slot or self._config.retrieval_slot
        body: dict[str, Any] = {
            "model": "retrieval",
            "messages": list(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        r = self._sync.post(
            "/v1/chat/completions",
            json=body,
            headers=self._slot_headers(s, trace_ctx),
        )
        if r.is_error:
            raise httpx.HTTPStatusError(
                f"Error {r.status_code} for {r.request.url!r}{_http_err_detail(r)}",
                request=r.request,
                response=r,
            )
        data = r.json()
        return data["choices"][0]["message"]["content"] or ""

    def _slot_headers(
        self,
        slot: str,
        trace_ctx: Mapping[str, str] | None = None,
    ) -> dict[str, str]:
        h: dict[str, str] = {
            "Content-Type": "application/json",
            "X-Slot": slot,
        }
        if trace_ctx:
            for k, v in trace_ctx.items():
                if v:
                    h[k] = v
        return h

    async def embed(
        self,
        texts: Sequence[str],
        *,
        kind: EmbeddingKind,
        trace_ctx: Mapping[str, str] | None = None,
    ) -> tuple[list[list[float]], str | None]:
        """Embeddings via `/v1/embeddings` and `X-Slot: embedding` (R-15)."""
        if self._use_ollama_embed and self._ollama_aclient is not None:
            return await self._ollama_embed_direct_async(texts, trace_ctx=trace_ctx)

        slot = self._config.embedding_slot
        # Some gateways expect a body field for query vs document; Ollama/OpenAI is neutral.
        body: dict[str, Any] = {
            "input": list(texts),
            "model": "embedding",
        }
        r = await self._client.post(
            "/v1/embeddings",
            json=body,
            headers=self._slot_headers(slot, trace_ctx),
        )
        if r.is_error:
            raise httpx.HTTPStatusError(
                f"Error {r.status_code} for {r.request.url!r}{_http_err_detail(r)}",
                request=r.request,
                response=r,
            )
        data = r.json()
        data_list = data.get("data", [])
        vecs = [
            item["embedding"]
            for item in sorted(data_list, key=lambda d: d.get("index", 0))
        ]
        model = data.get("model")
        return vecs, model

    async def chat_completion(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        slot: str | None = None,
        model: str | None = None,
        max_tokens: int = 256,
        temperature: float = 0.2,
        json_mode: bool = False,
        trace_ctx: Mapping[str, str] | None = None,
    ) -> str:
        s = slot or self._config.chat_slot
        body_model = (model or self._config.chat_model or "retrieval").strip() or "retrieval"
        body: dict[str, Any] = {
            "model": body_model,
            "messages": list(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        r = await self._client.post(
            "/v1/chat/completions",
            json=body,
            headers=self._slot_headers(s, trace_ctx),
        )
        if r.is_error:
            raise httpx.HTTPStatusError(
                f"Error {r.status_code} for {r.request.url!r}{_http_err_detail(r)}",
                request=r.request,
                response=r,
            )
        data = r.json()
        return data["choices"][0]["message"]["content"] or ""

    async def describe_models(self) -> dict[str, Any]:
        """
        Best-effort metadata for `/rag/health`. Tries `GET /v1/models` (OpenAI-style),
        else returns `display_models` from static config.
        """
        def _static_fallback() -> dict[str, str]:
            return {
                "embedding": self._config.display_models.get("embedding") or "unknown",
                "retrieval_llm": self._config.display_models.get("retrieval_llm") or "unknown",
                "chat": self._config.display_models.get("chat")
                or self._config.display_models.get("retrieval_llm")
                or "unknown",
            }

        try:
            r = await self._client.get("/v1/models")
        except httpx.HTTPError:
            return _static_fallback()
        if r.status_code != 200:
            return _static_fallback()
        try:
            data = r.json()
        except json.JSONDecodeError:
            return _static_fallback()
        out: dict[str, str] = {}
        models = data.get("data", [])
        want_chat = (self._config.chat_model or "retrieval").strip() or "retrieval"
        for m in models:
            mid = str(m.get("id", ""))
            if "embed" in mid.lower() or m.get("object") == "model":
                if not out.get("embedding") and "embed" in mid.lower():
                    out["embedding"] = mid
            if not out.get("chat") and (mid == want_chat or want_chat in mid):
                out["chat"] = mid
        if not out.get("embedding"):
            out["embedding"] = self._config.display_models.get("embedding") or "unknown"
        if not out.get("retrieval_llm"):
            out["retrieval_llm"] = self._config.display_models.get("retrieval_llm") or "unknown"
        if not out.get("chat"):
            out["chat"] = self._config.display_models.get("chat") or out.get("retrieval_llm") or "unknown"
        return {**out, "raw": data}


class GatewayEmbedding:
    """
    Synchronous-style embedding callable used by indexing paths; wraps async in asyncio.run
    in worker thread — ingestion pipeline is async in our app, so we use async `embed` directly.
    """

    def __init__(self, gateway: LLMGatewayClient) -> None:
        self._g = gateway

    async def aembed(
        self,
        texts: list[str],
        *,
        kind: EmbeddingKind,
    ) -> tuple[list[list[float]], str | None]:
        return await self._g.embed(texts, kind=kind)
