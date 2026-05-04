from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any, Iterable, Literal

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceConfig(BaseModel):
    bind: str = "0.0.0.0:8080"
    service_token_env: str = "RAG_SERVICE_TOKEN"
    admin_token_env: str = "RAG_ADMIN_TOKEN"
    version: str = "0.1.0"
    langfuse_header_name: str = "x-langfuse-trace-id"


class LlmGatewayConfig(BaseModel):
    base_url: str = "http://127.0.0.1:4000"
    # Sent as Authorization: Bearer … when set (e.g. LiteLLM `general_settings.master_key`).
    api_key: str = ""
    timeout_s: float = 30.0
    embedding_slot: str = "embedding"
    retrieval_slot: str = "retrieval_llm"
    # X-Slot for async UI chat (`chat_completion`); defaults to same string as retrieval_slot if unset.
    chat_slot: str = "retrieval_llm"
    # JSON `model` field for async UI chat only; RAG-internal sync calls keep `model: "retrieval"`.
    chat_model: str = "retrieval"
    # When both are set, dense embeddings use Ollama HTTP ``POST {base}/api/embed`` and skip
    # LiteLLM (avoids proxy/Ollama 400s on some LiteLLM versions). Chat still uses ``base_url``.
    ollama_embed_base_url: str = ""
    ollama_embed_model: str = ""
    # Per-string character cap before calling Ollama. LlamaIndex uses MetadataMode.EMBED, so
    # strings include metadata + body; small models (e.g. all-minilm) can reject ~1k+ chars of
    # token-dense text. 0 = no cap.
    ollama_embed_truncate_chars: int = 512
    display_models: dict[str, str] = Field(
        default_factory=lambda: {"embedding": "", "retrieval_llm": "", "chat": ""}
    )

    @field_validator("display_models", mode="before")
    @classmethod
    def _display_models_default_chat(cls, v: Any) -> Any:
        if v is None:
            return {"embedding": "", "retrieval_llm": "", "chat": ""}
        if isinstance(v, dict) and "chat" not in v:
            return {**v, "chat": ""}
        return v


class QdrantConfig(BaseModel):
    url: str = "http://127.0.0.1:6333"
    collection_prefix: str = "support_rag_"
    vector_size: int = 1024
    distance: str = "cosine"


class QueryRewriteConfig(BaseModel):
    enabled: bool = True
    n_alternatives: int = 3


class HydeConfig(BaseModel):
    enabled: bool = False


class RerankerConfig(BaseModel):
    model: str = "BAAI/bge-reranker-v2-m3"
    device: str = "cpu"


class RetrievalConfig(BaseModel):
    hybrid: bool = True
    rerank_enabled: bool = True
    top_k_dense: int = 30
    top_k_sparse: int = 30
    top_k_final: int = 6
    fusion: str = "rrf"
    rrf_k: int = 60
    query_rewrite: QueryRewriteConfig = Field(default_factory=QueryRewriteConfig)
    hyde: HydeConfig = Field(default_factory=HydeConfig)
    reranker: RerankerConfig = Field(default_factory=RerankerConfig)


class KbChunkingConfig(BaseModel):
    strategy: str = "sentence_window"
    chunk_size: int = 512
    window_size: int = 3


class TicketsChunkingConfig(BaseModel):
    strategy: str = "qa_pair"


class ChunkingConfig(BaseModel):
    kb: KbChunkingConfig = Field(default_factory=KbChunkingConfig)
    tickets: TicketsChunkingConfig = Field(default_factory=TicketsChunkingConfig)


class ChunkerVersionConfig(BaseModel):
    kb: str = "kb-v2"
    tickets: str = "tickets-v1"


class ObservabilityConfig(BaseModel):
    otel_endpoint: str = ""
    service_name: str = "support-rag"


class AnythingLlmConfig(BaseModel):
    """AnythingLLM HTTP API (Desktop or server) for vector search / workspace chat / ingest."""

    base_url: str = "http://127.0.0.1:3001"
    # Prefer ``RAG_ANYTHING_LLM__API_KEY`` (or YAML); never returned to the browser.
    api_key: str = ""
    workspace_slug: str = ""
    score_threshold: float = Field(default=0.25, ge=0.0, le=1.0)
    top_n: int = Field(default=4, ge=1, le=100)
    timeout_s: float = 60.0


class WebUiState(BaseModel):
    """Browser UI field persistence (read/written to the same YAML as ``RAG_CONFIG``)."""

    folder_path: str = ""
    namespace: str = "kb"
    use_rag: bool = False
    message_draft: str = ""
    # --- Dual-RAG / AnythingLLM (UI-only persistence; no secrets) ---
    rag_source: Literal["support_rag", "anythingllm"] = "support_rag"
    # How AnythingLLM Desktop points its own LLM/embedder (not the Support RAG retrieve path).
    anythingllm_models_source: Literal["alm_desktop", "llm_gateway"] = "alm_desktop"
    # Where the Web UI sends the **user reply** (this service's gateway vs AnythingLLM workspace chat).
    chat_model_source: Literal["llm_gateway", "anythingllm"] = "llm_gateway"
    # Deprecated mirror of chat_model_source for older YAML; kept in sync by validator.
    anythingllm_completion: Literal["gateway", "anythingllm_native"] = "gateway"
    show_retrieval_context: bool = True
    top_k: int = Field(default=6, ge=1, le=32)
    anythingllm_top_n: int = Field(default=4, ge=1, le=100)
    anythingllm_score_threshold: float | None = None
    anythingllm_workspace_slug_override: str = ""
    retrieval_chunk_char_cap: int = Field(default=2000, ge=256, le=200_000)
    anythingllm_ingest_state_path: str = "var/anythingllm_ingest_state.json"
    alm_ingest_folder_name: str = ""
    alm_ingest_folder_path: str = ""

    @field_validator("namespace")
    @classmethod
    def _ns(cls, v: str) -> str:
        s = (v or "kb").strip()
        if s not in ("kb", "tickets"):
            raise ValueError("namespace must be kb or tickets")
        return s

    @field_validator("anythingllm_score_threshold")
    @classmethod
    def _alm_score(cls, v: float | None) -> float | None:
        if v is None:
            return None
        if not 0.0 <= v <= 1.0:
            raise ValueError("anythingllm_score_threshold must be between 0 and 1")
        return v

    @field_validator("anythingllm_models_source", mode="before")
    @classmethod
    def _coerce_models_source_yaml(cls, v: Any) -> Any:
        if v == "litellm_gateway":
            return "llm_gateway"
        return v

    @model_validator(mode="before")
    @classmethod
    def _migrate_chat_model_source(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        d = dict(data)
        if d.get("anythingllm_models_source") == "litellm_gateway":
            d["anythingllm_models_source"] = "llm_gateway"
        if "chat_model_source" not in d or d.get("chat_model_source") is None:
            ac = d.get("anythingllm_completion", "gateway")
            if ac == "anythingllm_native":
                d["chat_model_source"] = "anythingllm"
            else:
                d["chat_model_source"] = "llm_gateway"
        return d

    @model_validator(mode="after")
    def _option_b_ban_and_sync_completion(self) -> WebUiState:
        if self.anythingllm_models_source == "llm_gateway" and self.chat_model_source == "anythingllm":
            raise ValueError(
                "Invalid web_ui: Option B (Desktop models via this project's llm_gateway) cannot "
                "be combined with chat model source 'AnythingLLM' (redundant / easy-to-misconfigure "
                "routing). Use Option A for Desktop-only models, or set Chat model source to "
                "llm_gateway."
            )
        new_comp: Literal["gateway", "anythingllm_native"] = (
            "anythingllm_native" if self.chat_model_source == "anythingllm" else "gateway"
        )
        if new_comp == self.anythingllm_completion:
            return self
        return self.model_copy(update={"anythingllm_completion": new_comp})


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RAG_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    service: ServiceConfig = Field(default_factory=ServiceConfig)
    llm_gateway: LlmGatewayConfig = Field(default_factory=LlmGatewayConfig)
    qdrant: QdrantConfig = Field(default_factory=QdrantConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    chunker_version: ChunkerVersionConfig = Field(default_factory=ChunkerVersionConfig)
    observability: ObservabilityConfig = Field(default_factory=ObservabilityConfig)
    web_ui: WebUiState = Field(default_factory=WebUiState)
    anything_llm: AnythingLlmConfig = Field(default_factory=AnythingLlmConfig)


# --- Web UI settings: tooltips and live-reload impact (dotted path -> metadata) ---
# "impact" is informational: rebuild vs rebind (see settings_patch_needs_rag_rebuild).

FIELD_SETTINGS_META: dict[str, dict[str, str]] = {
    # service
    "service.bind": {
        "hint": "Uvicorn bind host:port (takes effect after full process restart).",
        "impact": "none",
    },
    "service.service_token_env": {
        "hint": "Name of the environment variable holding the RAG service bearer token.",
        "impact": "none",
    },
    "service.admin_token_env": {
        "hint": "Name of the environment variable holding the admin/bearer for ingest.",
        "impact": "none",
    },
    "service.version": {
        "hint": "Service version string (informational; sent in health as applicable).",
        "impact": "none",
    },
    "service.langfuse_header_name": {
        "hint": "HTTP header to forward as trace id for Langfuse (e.g. x-langfuse-trace-id).",
        "impact": "rebind",
    },
    # llm gateway
    "llm_gateway.base_url": {
        "hint": "Base URL of the LiteLLM (or OpenAI-compatible) proxy for chat and embeddings.",
        "impact": "rebuild",
    },
    "llm_gateway.api_key": {
        "hint": (
            "Optional Bearer for the gateway (e.g. LiteLLM master key). "
            "Not used for direct Ollama /api/embed."
        ),
        "impact": "rebuild",
    },
    "llm_gateway.timeout_s": {
        "hint": "HTTP timeout in seconds for gateway and Ollama embed clients.",
        "impact": "rebuild",
    },
    "llm_gateway.embedding_slot": {
        "hint": "Slot label for embedding model routing (e.g. embedding).",
        "impact": "rebuild",
    },
    "llm_gateway.retrieval_slot": {
        "hint": "X-Slot for RAG-internal LLM calls (query rewrite, HyDe); JSON model body uses 'retrieval'.",
        "impact": "rebuild",
    },
    "llm_gateway.chat_slot": {
        "hint": (
            "X-Slot for Web UI async chat (`chat_completion`); JSON `model` uses chat_model. "
            "Defaults to retrieval_llm when unset in older configs."
        ),
        "impact": "rebuild",
    },
    "llm_gateway.chat_model": {
        "hint": (
            "LiteLLM `model_name` sent as JSON `model` for UI chat only; RAG-internal sync stays `retrieval`."
        ),
        "impact": "rebuild",
    },
    "llm_gateway.ollama_embed_base_url": {
        "hint": (
            "If set with ollama_embed_model, embeds go direct to Ollama /api/embed "
            "(bypassing LiteLLM for embeds)."
        ),
        "impact": "rebuild",
    },
    "llm_gateway.ollama_embed_model": {
        "hint": "Ollama embedding model name (e.g. all-minilm, nomic-embed-text).",
        "impact": "rebuild",
    },
    "llm_gateway.ollama_embed_truncate_chars": {
        "hint": (
            "Max characters per string before Ollama embed; 0 = no clip. "
            "Small models (e.g. all-minilm) often need ~512."
        ),
        "impact": "in_place",
    },
    "llm_gateway.display_models.embedding": {
        "hint": "Label for UI/health when /v1/models is unavailable.",
        "impact": "in_place",
    },
    "llm_gateway.display_models.retrieval_llm": {
        "hint": "Label for the RAG-internal / rewrite LLM in health display.",
        "impact": "in_place",
    },
    "llm_gateway.display_models.chat": {
        "hint": "Label for the Web UI chat path in /rag/health when /v1/models is unavailable.",
        "impact": "in_place",
    },
    # qdrant
    "qdrant.url": {
        "hint": "Qdrant HTTP API base URL.",
        "impact": "rebuild",
    },
    "qdrant.collection_prefix": {
        "hint": (
            "Prefix for collection names (namespaces: kb, tickets). "
            "Changing it requires re-indexing."
        ),
        "impact": "rebuild",
        "risk": "Changing collection prefix does not migrate data; re-ingest to new collections.",
    },
    "qdrant.vector_size": {
        "hint": (
            "Dense vector dimension (must match embedding model output). "
            "Re-ingest if you change."
        ),
        "impact": "rebuild",
        "risk": "Existing vectors have the old size; re-index after changing.",
    },
    "qdrant.distance": {
        "hint": "Vector distance in Qdrant (e.g. cosine). Must match how collections were created.",
        "impact": "rebuild",
        "risk": "Distance mismatch breaks existing points; re-create collections if needed.",
    },
    # retrieval
    "retrieval.hybrid": {
        "hint": "If true, combine dense and sparse (BM25) search.",
        "impact": "rebind",
    },
    "retrieval.rerank_enabled": {
        "hint": "If true, cross-encode rerank top candidates after fusion.",
        "impact": "rebind",
    },
    "retrieval.top_k_dense": {
        "hint": "How many dense hits to consider before fusion.",
        "impact": "rebind",
    },
    "retrieval.top_k_sparse": {
        "hint": "How many sparse (BM25) hits to consider before fusion.",
        "impact": "rebind",
    },
    "retrieval.top_k_final": {
        "hint": "Cap on chunks returned after merge/rerank.",
        "impact": "rebind",
    },
    "retrieval.fusion": {
        "hint": "Fusion method (e.g. rrf for reciprocal rank fusion).",
        "impact": "rebind",
    },
    "retrieval.rrf_k": {
        "hint": "RRF constant k for score smoothing.",
        "impact": "rebind",
    },
    "retrieval.query_rewrite.enabled": {
        "hint": "If true, the gateway LLM rewrites the query for extra retrieval runs.",
        "impact": "rebind",
    },
    "retrieval.query_rewrite.n_alternatives": {
        "hint": "Up to this many alternative queries (capped in code).",
        "impact": "rebind",
    },
    "retrieval.hyde.enabled": {
        "hint": "HyDE-style expansion (if implemented in service).",
        "impact": "rebind",
    },
    "retrieval.reranker.model": {
        "hint": "CrossEncoder model name (sentence-transformers) for reranking.",
        "impact": "rebind",
    },
    "retrieval.reranker.device": {
        "hint": "Torch device for reranker (cpu or cuda).",
        "impact": "rebind",
    },
    # chunking
    "chunking.kb.strategy": {
        "hint": (
            "Chunking strategy for kb (e.g. sentence_window). Affects the next ingest."
        ),
        "impact": "rebind",
    },
    "chunking.kb.chunk_size": {
        "hint": "Token/window size for kb chunks. Affects the next ingest.",
        "impact": "rebind",
    },
    "chunking.kb.window_size": {
        "hint": "Sentence window size (sentence_window strategy). Affects the next ingest.",
        "impact": "rebind",
    },
    "chunking.tickets.strategy": {
        "hint": "Strategy for the tickets namespace. Affects the next ingest.",
        "impact": "rebind",
    },
    "chunker_version.kb": {
        "hint": "Bumped when kb chunking contract changes; part of id hashing.",
        "impact": "rebind",
    },
    "chunker_version.tickets": {
        "hint": "Bumped when tickets chunking contract changes.",
        "impact": "rebind",
    },
    # observability
    "observability.otel_endpoint": {
        "hint": (
            "OTLP gRPC endpoint for OpenTelemetry. Empty = no export. "
            "A full process restart may be needed to apply."
        ),
        "impact": "rebind",
    },
    "observability.service_name": {
        "hint": "OTel service name for traces/metrics.",
        "impact": "rebind",
    },
    # web_ui (same file; advanced users)
    "web_ui.folder_path": {
        "hint": "Default folder for local Qdrant ingest; saved with the form.",
        "impact": "rebind",
    },
    "web_ui.alm_ingest_folder_path": {
        "hint": "Last folder path for “Ingest to AnythingLLM”; saved like folder_path.",
        "impact": "rebind",
    },
    "web_ui.namespace": {
        "hint": "Default namespace kb or tickets.",
        "impact": "rebind",
    },
    "web_ui.use_rag": {
        "hint": "Default: augment chat with retrieval.",
        "impact": "rebind",
    },
    "web_ui.message_draft": {
        "hint": "Draft message persisted in config (optional).",
        "impact": "rebind",
    },
    "web_ui.anythingllm_models_source": {
        "hint": (
            "Option A/B: how AnythingLLM Desktop points its own LLM + embedder — not the Support RAG retrieve path."
        ),
        "impact": "rebind",
    },
    "web_ui.chat_model_source": {
        "hint": (
            "Where the Web UI sends the user reply: this service's llm_gateway vs AnythingLLM workspace chat."
        ),
        "impact": "rebind",
    },
    "web_ui.anythingllm_completion": {
        "hint": (
            "Legacy mirror of chat_model_source; prefer chat_model_source. Synced on save."
        ),
        "impact": "rebind",
    },
    "web_ui.show_retrieval_context": {
        "hint": "If true, show retrieved chunks / citations in the UI (when the UI plan enables it).",
        "impact": "rebind",
    },
    "web_ui.top_k": {
        "hint": "Top-k for Support RAG retrieval in the browser chat flow (1–32).",
        "impact": "rebind",
    },
    "web_ui.anythingllm_top_n": {
        "hint": "Top-N for AnythingLLM vector-search (1–100); server may still cap per workspace.",
        "impact": "rebind",
    },
    "web_ui.anythingllm_score_threshold": {
        "hint": "Optional ALM similarity floor (0–1); empty = use anything_llm.score_threshold in YAML.",
        "impact": "rebind",
    },
    "web_ui.anythingllm_workspace_slug_override": {
        "hint": "If set, use this workspace slug instead of anything_llm.workspace_slug for ALM calls.",
        "impact": "rebind",
    },
    "web_ui.retrieval_chunk_char_cap": {
        "hint": "Max characters of retrieved text to inject into the augmented prompt (per chunk / total TBD in UI).",
        "impact": "rebind",
    },
    "web_ui.anythingllm_ingest_state_path": {
        "hint": "Path (relative to CWD or absolute) for ALM raw-text idempotency JSON (var/…).",
        "impact": "rebind",
    },
    # anything_llm
    "anything_llm.base_url": {
        "hint": "AnythingLLM HTTP base (e.g. Desktop http://127.0.0.1:3001). No trailing path.",
        "impact": "rebuild",
    },
    "anything_llm.api_key": {
        "hint": "AnythingLLM API Bearer (set in env RAG_ANYTHING_LLM__API_KEY preferred). Never sent to the browser.",
        "impact": "rebuild",
    },
    "anything_llm.workspace_slug": {
        "hint": "Workspace slug for vector-search, chat, ingest. Empty or the literal default uses the first workspace from AnythingLLM's API list.",
        "impact": "rebuild",
    },
    "anything_llm.score_threshold": {
        "hint": "Default scoreThreshold for vector-search (0–1) when the UI does not override.",
        "impact": "rebuild",
    },
    "anything_llm.top_n": {
        "hint": "Default topN for vector-search (1–100) when the UI does not override.",
        "impact": "rebuild",
    },
    "anything_llm.timeout_s": {
        "hint": "HTTP timeout for AnythingLLM client calls (seconds).",
        "impact": "rebuild",
    },
}


def _collect_ui_secret_substrings(cfg: AppConfig | None = None) -> set[str]:
    """Substrings that must not appear in browser-bound config JSON (plan §7a)."""
    out: set[str] = set()
    if cfg is not None:
        for v in (cfg.llm_gateway.api_key, cfg.anything_llm.api_key):
            t = (v or "").strip()
            if len(t) >= 8:
                out.add(t)
    for k, v in os.environ.items():
        if not v or len(v.strip()) < 8:
            continue
        ku = k.upper()
        vt = v.strip()
        if ku.startswith("RAG_") and (
            "__API_KEY" in ku
            or ku.endswith(("_TOKEN", "_SECRET"))
            or "_MASTER_KEY" in ku
        ):
            out.add(vt)
        if ku in (
            "LITELLM_MASTER_KEY",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "ANTHROPIC_AUTH_TOKEN",
        ):
            out.add(vt)
    return out


def _blank_known_api_key_fields(tree: dict[str, Any]) -> None:
    for name in ("llm_gateway", "anything_llm"):
        block = tree.get(name)
        if isinstance(block, dict) and "api_key" in block:
            block["api_key"] = ""


def _redact_secret_substrings_in_values(obj: Any, secrets: set[str]) -> Any:
    if not secrets:
        return obj
    if isinstance(obj, str):
        out = obj
        for s in sorted(secrets, key=len, reverse=True):
            if s and s in out:
                out = out.replace(s, "[REDACTED]")
        return out
    if isinstance(obj, list):
        return [_redact_secret_substrings_in_values(x, secrets) for x in obj]
    if isinstance(obj, dict):
        return {
            k: _redact_secret_substrings_in_values(v, secrets) for k, v in obj.items()
        }
    return obj


def _redact_for_browser(
    payload: Any,
    *,
    cfg: AppConfig | None = None,
    extra_secrets: Iterable[str] | None = None,
) -> Any:
    """Recursively redact secrets so UI JSON does not expose keys or known env material (plan §7a)."""
    tree: Any
    if isinstance(payload, dict):
        tree = copy.deepcopy(payload)
        _blank_known_api_key_fields(tree)
    else:
        tree = copy.deepcopy(payload)
    secrets = _collect_ui_secret_substrings(cfg)
    if extra_secrets is not None:
        for e in extra_secrets:
            t = (e or "").strip()
            if len(t) >= 8:
                secrets.add(t)
    return _redact_secret_substrings_in_values(tree, secrets)


# Llm keys that require new httpx / Ollama clients
_LLM_REBUILD_KEYS = frozenset(
    {
        "base_url",
        "api_key",
        "timeout_s",
        "embedding_slot",
        "retrieval_slot",
        "chat_slot",
        "chat_model",
        "ollama_embed_base_url",
        "ollama_embed_model",
    }
)

_RISKY_PATH_PREFIXES: tuple[str, ...] = (
    "qdrant.vector_size",
    "qdrant.collection_prefix",
    "qdrant.distance",
)


def _read_yaml_config(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _merge_rag_env_over_yaml(initial: dict[str, Any]) -> dict[str, Any]:
    """Override YAML with ``RAG_*`` env (``AppConfig(**yaml)`` does not do this alone)."""
    out = dict(initial)
    gw = os.environ.get("RAG_LLM_GATEWAY__BASE_URL", "").strip()
    if gw:
        lg = dict(out.get("llm_gateway") or {})
        lg["base_url"] = gw
        out["llm_gateway"] = lg
    gk = os.environ.get("RAG_LLM_GATEWAY__API_KEY", "").strip()
    if gk:
        lg = dict(out.get("llm_gateway") or {})
        lg["api_key"] = gk
        out["llm_gateway"] = lg
    oeb = os.environ.get("RAG_LLM_GATEWAY__OLLAMA_EMBED_BASE_URL", "").strip()
    if oeb:
        lg = dict(out.get("llm_gateway") or {})
        lg["ollama_embed_base_url"] = oeb
        out["llm_gateway"] = lg
    oem = os.environ.get("RAG_LLM_GATEWAY__OLLAMA_EMBED_MODEL", "").strip()
    if oem:
        lg = dict(out.get("llm_gateway") or {})
        lg["ollama_embed_model"] = oem
        out["llm_gateway"] = lg
    oetc = os.environ.get("RAG_LLM_GATEWAY__OLLAMA_EMBED_TRUNCATE_CHARS", "").strip()
    if oetc.isdigit():
        lg = dict(out.get("llm_gateway") or {})
        lg["ollama_embed_truncate_chars"] = int(oetc)
        out["llm_gateway"] = lg
    qu = os.environ.get("RAG_QDRANT__URL", "").strip()
    if qu:
        qd = dict(out.get("qdrant") or {})
        qd["url"] = qu
        out["qdrant"] = qd
    ab = os.environ.get("RAG_ANYTHING_LLM__BASE_URL", "").strip()
    if ab:
        alm = dict(out.get("anything_llm") or {})
        alm["base_url"] = ab
        out["anything_llm"] = alm
    aak = os.environ.get("RAG_ANYTHING_LLM__API_KEY", "").strip()
    if aak:
        alm = dict(out.get("anything_llm") or {})
        alm["api_key"] = aak
        out["anything_llm"] = alm
    aws = os.environ.get("RAG_ANYTHING_LLM__WORKSPACE_SLUG", "").strip()
    if aws:
        alm = dict(out.get("anything_llm") or {})
        alm["workspace_slug"] = aws
        out["anything_llm"] = alm
    ato = os.environ.get("RAG_ANYTHING_LLM__TIMEOUT_S", "").strip()
    if ato:
        try:
            alm = dict(out.get("anything_llm") or {})
            alm["timeout_s"] = float(ato)
            out["anything_llm"] = alm
        except ValueError:
            pass
    return out


def deep_merge(base: Any, patch: Any) -> Any:
    """Recursively merge ``patch`` into ``base`` (dicts only; other types replace)."""
    if not isinstance(base, dict) or not isinstance(patch, dict):
        return patch
    out = dict(base)
    for k, v in patch.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def merge_config_patch_into_file(path: str | Path, patch: dict[str, Any]) -> None:
    """Deep-merge ``patch`` into the root YAML and write.

    Top-level keys match ``AppConfig`` sections.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"config file not found: {p}")
    root = _read_yaml_config(str(p)) or {}
    merged = deep_merge(root, patch)
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            merged,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )


def merge_web_ui_into_config_file(
    path: str | Path,
    updates: dict[str, Any],
) -> None:
    """Merge ``updates`` into the ``web_ui`` key of a YAML file; other keys are preserved."""
    merge_config_patch_into_file(path, {"web_ui": updates})


def list_leaf_dotted_paths(obj: Any, prefix: str = "") -> set[str]:
    """Dotted paths for JSON leaves (str, int, float, bool, None) and dicts of strings."""
    if isinstance(obj, dict):
        if not obj:
            return {prefix} if prefix else set()
        out: set[str] = set()
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                out |= list_leaf_dotted_paths(v, p)
            else:
                out.add(p)
        return out
    if prefix:
        return {prefix}
    return set()


def _flatten_patch_to_prefixes(patch: dict[str, Any], prefix: str = "") -> set[str]:
    """Dotted key paths for leaves present in a patch (only paths ending at leaves)."""
    return list_leaf_dotted_paths(patch, prefix)


def settings_patch_needs_rag_rebuild(patch: dict[str, Any]) -> bool:
    """True if the patch requires replacing ``RAGService`` (new HTTP/Qdrant clients or indices)."""
    if "qdrant" in patch and isinstance(patch["qdrant"], dict) and patch["qdrant"]:
        return True
    r = patch.get("retrieval")
    if isinstance(r, dict) and (("fusion" in r) or ("rrf_k" in r)):
        # QdrantVectorStore holds hybrid_fusion_fn built from rrf_k at init
        return True
    lg = patch.get("llm_gateway")
    if isinstance(lg, dict) and lg:
        for k in lg:
            if k in _LLM_REBUILD_KEYS:
                return True
    return False


def risky_settings_if_unconfirmed(
    patch: dict[str, Any], *, confirmed: bool
) -> list[str]:
    """
    If a risky Qdrant shape field is in the patch and the client did not send
    ``confirmed: true``, return warning strings (for HTTP 409 + ``require_confirmation``).
    """
    if confirmed:
        return []
    return _risk_messages_for_qdrant_shape_patch(patch)


def _risk_messages_for_qdrant_shape_patch(patch: dict[str, Any]) -> list[str]:
    pfx = _flatten_patch_to_prefixes(patch)
    w: list[str] = []
    for rp in _RISKY_PATH_PREFIXES:
        if not any(p == rp or p.startswith(rp + ".") for p in pfx):
            continue
        m = FIELD_SETTINGS_META.get(rp, {})
        r = m.get("risk") if isinstance(m, dict) else None
        if r:
            w.append(r)
    return w


def risk_notes_for_qdrant_shape_patch(patch: dict[str, Any]) -> list[str]:
    """Non-empty info strings for risky Qdrant fields touched (for 200 response body)."""
    return _risk_messages_for_qdrant_shape_patch(patch)


def _load_dotenv_files() -> None:
    # Load from repo root (parent of the `support_rag` package) first so tokens and
    # gateway keys apply even when uvicorn is started with a CWD outside the project.
    # Then load CWD `.env` so a local working-directory override can still set vars.
    repo = Path(__file__).resolve().parent.parent
    load_dotenv(repo / ".env")
    load_dotenv()


def load_config(path: str | None = None) -> AppConfig:
    # Does not override existing process env (shell exports win).
    _load_dotenv_files()
    p = path or os.environ.get("RAG_CONFIG", "config.yaml")
    initial: dict[str, Any] = _read_yaml_config(p)
    if not initial and Path("config.example.yaml").is_file() and p == "config.yaml":
        # dev convenience: no config.yaml present
        initial = _read_yaml_config("config.example.yaml")
    return AppConfig(**_merge_rag_env_over_yaml(initial))
