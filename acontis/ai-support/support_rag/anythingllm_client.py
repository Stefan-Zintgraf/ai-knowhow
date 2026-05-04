"""HTTP client for AnythingLLM ``/api/v1`` (vector-search, workspace chat, ingest)."""

from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any, Literal

WorkspaceSlugEffectiveResolution = Literal[
    "override", "configured", "implicit_first", "none"
]
from urllib.parse import urlparse

import httpx

from support_rag.config import AnythingLlmConfig, AppConfig
from support_rag.schemas import ChunkResult, RetrievalRequest, RetrievalResponse

logger = logging.getLogger(__name__)

# ``chat`` uses the prompt as the user turn (rolling history) and is the least bad option when the
# message is already augmented with retrieval context; ``query`` would re-search the vector DB.
# AnythingLLM may still attach workspace context — see ``meta.alm_double_retrieval_risk``.
ALM_WORKSPACE_CHAT_MODE_AUGMENTED: Literal["chat"] = "chat"

DEFAULT_ALM_INGEST_STATE_PATH = "var/anythingllm_ingest_state.json"


def _base(base_url: str) -> str:
    return (base_url or "").strip().rstrip("/")


def _headers(api_key: str) -> dict[str, str]:
    h = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    t = (api_key or "").strip()
    if t:
        h["Authorization"] = f"Bearer {t}"
    return h


# Config/web_ui "default" was a placeholder; AnythingLLM workspaces use slugs from the app (e.g. sample-workspace).
_LEGACY_AUTO_WORKSPACE_SLUGS = frozenset(("", "default"))


def list_workspace_slugs(alm: AnythingLlmConfig, base_url: str | None = None) -> list[str]:
    """GET ``/api/v1/workspaces`` — slugs in API order (typically creation order)."""
    url = f"{_base(base_url or alm.base_url)}/api/v1/workspaces"
    with httpx.Client(timeout=alm.timeout_s) as client:
        r = client.get(url, headers=_headers(alm.api_key))
        r.raise_for_status()
    data = r.json()
    out: list[str] = []
    arr = data.get("workspaces") if isinstance(data, dict) else None
    if isinstance(arr, list):
        for item in arr:
            if not isinstance(item, dict):
                continue
            s = item.get("slug")
            if isinstance(s, str):
                t = s.strip()
                if t:
                    out.append(t)
    return out


def resolve_workspace_effective(
    override: str,
    configured: str,
    slugs: list[str],
    *,
    list_failed: bool,
) -> tuple[str, WorkspaceSlugEffectiveResolution]:
    """
    Same rules as :func:`resolve_workspace_slug`, but uses a pre-fetched workspace
    list. When the implicit (first-workspace) path is needed but listing failed or
    returned no slugs, returns ``("", "none")``.
    """
    o = (override or "").strip()
    if o:
        return o, "override"
    c = (configured or "").strip()
    if c and c not in _LEGACY_AUTO_WORKSPACE_SLUGS:
        return c, "configured"
    if list_failed or not slugs:
        return "", "none"
    return slugs[0], "implicit_first"


def resolve_workspace_slug(
    alm: AnythingLlmConfig,
    *,
    override: str = "",
    configured: str = "",
    base_url: str | None = None,
) -> str:
    """
    Pick the workspace slug for vector-search, chat, and ingest.

    If ``override`` is set, it wins. If ``configured`` is set and is not a legacy
    auto placeholder (empty or the string ``default``), it is used. Otherwise the
    first workspace returned by AnythingLLM is used.
    """
    o = (override or "").strip()
    if o:
        return o
    c = (configured or "").strip()
    if c and c not in _LEGACY_AUTO_WORKSPACE_SLUGS:
        return c
    slugs = list_workspace_slugs(alm, base_url=base_url)
    slug, res = resolve_workspace_effective(
        override, configured, slugs, list_failed=False
    )
    if res == "none":
        raise ValueError(
            "AnythingLLM has no workspaces. Create a workspace in AnythingLLM Desktop, "
            "or set anything_llm.workspace_slug (or the Web UI override) to your workspace slug."
        )
    return slug


def _slug_from_config(app_config: AppConfig) -> str:
    return resolve_workspace_slug(
        app_config.anything_llm,
        override=app_config.web_ui.anythingllm_workspace_slug_override or "",
        configured=app_config.anything_llm.workspace_slug or "",
    )


def format_alm_http_error(exc: httpx.HTTPStatusError) -> str:
    """Normalize AnythingLLM HTTP errors for UI / logs."""
    r = exc.response
    code = r.status_code if r is not None else "?"
    tail = ""
    try:
        if r is not None and r.text:
            tail = (r.text[:800] + ("…" if len(r.text) > 800 else "")).strip()
    except Exception:
        tail = ""
    if r is not None and r.status_code == 403:
        return "AnythingLLM rejected the API key (403). Set RAG_ANYTHING_LLM__API_KEY to a valid key."
    if r is not None and r.status_code == 404:
        return "AnythingLLM returned 404 (workspace or path). Check workspace slug and API version."
    if tail:
        return f"AnythingLLM HTTP {code}: {tail}"
    return f"AnythingLLM HTTP {code}"


def format_httpx_connect_error(exc: httpx.RequestError) -> str:
    return (
        f"AnythingLLM unreachable ({type(exc).__name__}: {exc}). "
        "Check anything_llm.base_url and that Desktop/server is running."
    )


def alm_error_message(exc: BaseException) -> str:
    if isinstance(exc, httpx.HTTPStatusError):
        return format_alm_http_error(exc)
    if isinstance(exc, httpx.RequestError):
        return format_httpx_connect_error(exc)
    return str(exc)[:2_000]


_URL_LIKE = re.compile(r"^https?://", re.I)


def litellm_gateway_reachable(
    base_url: str,
    *,
    api_key: str = "",
    timeout_s: float = 5.0,
) -> bool | None:
    """``GET {base}/health`` with optional Bearer. Returns ``None`` on unexpected errors."""
    b = _base(base_url)
    if not b:
        return None
    h = {"Accept": "application/json"}
    k = (api_key or "").strip()
    if k:
        h["Authorization"] = f"Bearer {k}"
    try:
        with httpx.Client(timeout=timeout_s, trust_env=False) as client:
            r = client.get(f"{b}/health", headers=h)
        return 200 <= r.status_code < 300
    except httpx.RequestError:
        return False
    except Exception:
        logger.exception("litellm_gateway_reachable")
        return None


def get_system_settings(alm: AnythingLlmConfig, *, base_url: str | None = None) -> dict[str, Any]:
    """``GET /api/v1/system`` → JSON (raises on HTTP error)."""
    url = f"{_base(base_url or alm.base_url)}/api/v1/system"
    with httpx.Client(timeout=alm.timeout_s, trust_env=False) as client:
        r = client.get(url, headers=_headers(alm.api_key))
        r.raise_for_status()
    data = r.json()
    return data if isinstance(data, dict) else {}


def try_get_system_settings(
    alm: AnythingLlmConfig, *, base_url: str | None = None
) -> tuple[dict[str, Any] | None, str | None]:
    """
    Like :func:`get_system_settings`, but returns ``(data, None)`` on success or
    ``(None, human-readable error)`` on failure (for Web UI verify flows).
    """
    try:
        return get_system_settings(alm, base_url=base_url), None
    except httpx.HTTPStatusError as e:
        return None, format_alm_http_error(e)
    except httpx.RequestError as e:
        return None, format_httpx_connect_error(e)
    except Exception as e:
        logger.exception("try_get_system_settings")
        tail = str(e).strip()
        if len(tail) > 400:
            tail = tail[:400] + "…"
        return None, f"Unexpected error reading AnythingLLM /api/v1/system: {tail}"


def _walk_url_hosts(obj: Any, *, out_hosts: set[str]) -> None:
    """Collect hostnames from http(s) string values; skip likely-secret keys."""
    if isinstance(obj, str):
        s = obj.strip()
        if _URL_LIKE.search(s):
            try:
                hst = (urlparse(s).hostname or "").lower()
                if hst:
                    out_hosts.add(hst)
            except Exception:
                pass
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            lk = str(k).lower()
            if any(
                x in lk
                for x in (
                    "apikey",
                    "secret",
                    "password",
                    "token",
                    "bearer",
                    "authorization",
                )
            ):
                continue
            if isinstance(v, bool):
                continue
            _walk_url_hosts(v, out_hosts=out_hosts)
    elif isinstance(obj, list):
        for x in obj[:50]:
            _walk_url_hosts(x, out_hosts=out_hosts)


def summarize_alm_system_for_ui(
    data: dict[str, Any],
) -> tuple[str | None, str | None, list[str]]:
    """
    Returns ``(alm_provider_summary, alm_chat_mode_default, url_hosts)`` with no secrets.

    ``url_hosts`` are hostnames from http(s) values under ``settings`` (for gateway comparison).
    """
    settings = data.get("settings")
    if not isinstance(settings, dict):
        return None, None, []
    out_hosts: set[str] = set()
    parts: list[str] = []
    prov = settings.get("LLMProvider")
    if prov is not None and not isinstance(prov, bool):
        p = str(prov).strip()
        if p:
            parts.append(f"LLM={p[:80]}")
    _walk_url_hosts(settings, out_hosts=out_hosts)
    emb = settings.get("EmbeddingEngine")
    if emb is not None and not isinstance(emb, bool):
        e = str(emb).strip()
        if e:
            parts.append(f"Emb={e[:80]}")
    summary = ", ".join(parts[:12]) if parts else None
    mode = None
    for k in ("chatMode", "defaultChatMode", "chat_mode"):
        v = settings.get(k)
        if isinstance(v, str) and v.strip():
            mode = v.strip()[:64]
            break
    hosts = sorted(out_hosts)
    return summary, mode, hosts


def option_b_host_match(
    llm_gateway_base_url: str,
    alm_url_hosts: list[str],
) -> bool:
    g = (llm_gateway_base_url or "").strip()
    if not g or not alm_url_hosts:
        return False
    try:
        want = (urlparse(g if "://" in g else f"http://{g}").hostname or "").lower()
    except Exception:
        return False
    if not want:
        return False
    return any(h == want for h in alm_url_hosts)


def vector_search(
    alm: AnythingLlmConfig,
    *,
    slug: str,
    query: str,
    top_n: int | None = None,
    score_threshold: float | None = None,
    req: RetrievalRequest | None = None,
    base_url: str | None = None,
) -> RetrievalResponse:
    """
    ``POST /api/v1/workspace/{slug}/vector-search`` → :class:`RetrievalResponse`.

    If ``req.filters`` is set, a warning is logged; ``debug`` notes ``filters_applied: false``
    (AnythingLLM does not honor Support RAG metadata filters on this endpoint).
    """
    url = f"{_base(base_url or alm.base_url)}/api/v1/workspace/{slug}/vector-search"
    body: dict[str, Any] = {
        "query": query,
        "topN": int(top_n if top_n is not None else alm.top_n),
        "scoreThreshold": float(
            score_threshold if score_threshold is not None else alm.score_threshold
        ),
    }
    filters_ignored = bool(req and req.filters)
    if filters_ignored:
        logger.warning(
            "AnythingLLM vector-search ignores retrieval filters; dropping filters for this call."
        )
    timeout = alm.timeout_s
    with httpx.Client(timeout=timeout) as client:
        r = client.post(url, headers=_headers(alm.api_key), json=body)
        r.raise_for_status()
        data = r.json()
    results = data.get("results")
    if not isinstance(results, list):
        results = []
    chunks: list[ChunkResult] = []
    for row in results:
        if not isinstance(row, dict):
            continue
        cid = str(row.get("id") or "")
        text = str(row.get("text") or "")
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        parent = str(
            meta.get("title")
            or meta.get("docSource")
            or meta.get("chunkSource")
            or cid
        )
        score = row.get("score")
        if score is not None and not isinstance(score, (int, float)):
            try:
                score = float(score)
            except (TypeError, ValueError):
                score = None
        chunks.append(
            ChunkResult(
                id=cid,
                text=text,
                metadata=dict(meta),
                parent_id=parent,
                score=score,
            )
        )
    msg = (data.get("message") or "") if isinstance(data, dict) else ""
    return RetrievalResponse(
        chunks=chunks,
        rewritten_queries=[],
        debug={
            "source": "anything_llm",
            "endpoint": "vector-search",
            "filters_applied": False,
            "filters_ignored": filters_ignored,
            "vector_search_message": msg,
        },
    )


def workspace_chat(
    alm: AnythingLlmConfig,
    *,
    slug: str,
    message: str,
    mode: str | None = None,
    session_id: str | None = None,
    base_url: str | None = None,
) -> tuple[str, dict[str, Any]]:
    """
    ``POST /api/v1/workspace/{slug}/chat`` (non-streaming).

    Returns ``(text_response, meta)``. ``meta`` includes ``alm_chat_mode`` and
    ``alm_double_retrieval_risk`` (true when the chosen mode is not guaranteed to skip vector lookup).
    """
    resolved = mode or ALM_WORKSPACE_CHAT_MODE_AUGMENTED
    url = f"{_base(base_url or alm.base_url)}/api/v1/workspace/{slug}/chat"
    body: dict[str, Any] = {
        "message": message,
        "mode": resolved,
        "reset": True,
    }
    if session_id:
        body["sessionId"] = session_id
    # query mode forces vector DB use; automatic may tool-call. ``chat`` is best-effort for pre-filled context.
    double_risk = resolved != "chat"
    timeout = alm.timeout_s
    with httpx.Client(timeout=timeout) as client:
        r = client.post(url, headers=_headers(alm.api_key), json=body)
        r.raise_for_status()
        data = r.json()
    text: str | None = None
    if isinstance(data, dict):
        tr = data.get("textResponse")
        if tr is not None:
            text = str(tr)
        err = data.get("error")
        if err and str(err).lower() not in ("null", "none", ""):
            text = (text or "") + ("\n" if text else "") + f"[AnythingLLM error: {err}]"
    if text is None:
        text = ""
    meta: dict[str, Any] = {
        "alm_chat_mode": resolved,
        "alm_double_retrieval_risk": double_risk,
        "raw_keys": list(data.keys()) if isinstance(data, dict) else [],
    }
    return text, meta


def _load_json_path(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        raw = path.read_text(encoding="utf-8")
        d = json.loads(raw)
        return d if isinstance(d, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _save_json_path(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def update_embeddings(
    alm: AnythingLlmConfig,
    *,
    slug: str,
    adds: list[str] | None = None,
    deletes: list[str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """``POST /api/v1/workspace/{slug}/update-embeddings``."""
    url = f"{_base(base_url or alm.base_url)}/api/v1/workspace/{slug}/update-embeddings"
    body = {
        "adds": list(adds or []),
        "deletes": list(deletes or []),
    }
    with httpx.Client(timeout=alm.timeout_s) as client:
        r = client.post(url, headers=_headers(alm.api_key), json=body)
        r.raise_for_status()
        return r.json() if r.text else {}


def raw_text_upload(
    alm: AnythingLlmConfig,
    *,
    text_content: str,
    title: str,
    add_to_workspaces: str = "",
    extra_metadata: dict[str, Any] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """``POST /api/v1/document/raw-text``."""
    url = f"{_base(base_url or alm.base_url)}/api/v1/document/raw-text"
    metadata: dict[str, Any] = {"title": title}
    if extra_metadata:
        metadata.update(extra_metadata)
    body = {
        "textContent": text_content,
        "addToWorkspaces": add_to_workspaces,
        "metadata": metadata,
    }
    with httpx.Client(timeout=alm.timeout_s) as client:
        r = client.post(url, headers=_headers(alm.api_key), json=body)
        r.raise_for_status()
    return r.json()


def document_upload(
    alm: AnythingLlmConfig,
    *,
    file_path: Path,
    add_to_workspaces: str = "",
    metadata: dict[str, Any] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """``POST /api/v1/document/upload`` (multipart file)."""
    url = f"{_base(base_url or alm.base_url)}/api/v1/document/upload"
    p = Path(file_path)
    files = {"file": (p.name, p.read_bytes(), "application/octet-stream")}
    data: dict[str, str] = {}
    if add_to_workspaces:
        data["addToWorkspaces"] = add_to_workspaces
    if metadata:
        data["metadata"] = json.dumps(metadata, ensure_ascii=True)
    h = {k: v for k, v in _headers(alm.api_key).items() if k != "Content-Type"}
    with httpx.Client(timeout=alm.timeout_s) as client:
        r = client.post(url, headers=h, data=data, files=files)
        r.raise_for_status()
    return r.json()


def ingest_raw_text_idempotent(
    app_config: AppConfig,
    *,
    logical_key: str,
    text: str,
    document_title: str,
    state_path: str | None = None,
) -> dict[str, Any]:
    """
    Ingest text via raw-text, with JSON idempotency (hash per logical_key).

    If content unchanged, returns ``{"skipped": true, ...}``.

    If content changed and a previous ``location`` is known, calls ``update-embeddings`` with
    ``deletes`` before uploading the new document.
    """
    alm = app_config.anything_llm
    slug = _slug_from_config(app_config)
    sp = state_path or app_config.web_ui.anythingllm_ingest_state_path or DEFAULT_ALM_INGEST_STATE_PATH
    p = Path(sp)
    store = _load_json_path(p)
    docs = store.get("by_key")
    if not isinstance(docs, dict):
        docs = {}
    h = _sha256_text(text)
    prev = docs.get(logical_key)
    if isinstance(prev, dict) and prev.get("sha256") == h:
        return {
            "skipped": True,
            "logical_key": logical_key,
            "sha256": h,
            "location": prev.get("location"),
        }
    old_loc = None
    if isinstance(prev, dict):
        old_loc = prev.get("location")
    if isinstance(old_loc, str) and old_loc and prev.get("sha256") != h:
        try:
            update_embeddings(
                alm,
                slug=slug,
                deletes=[old_loc],
            )
        except httpx.HTTPError as e:
            logger.warning("ALM update-embeddings delete failed (continuing): %s", e)

    out = raw_text_upload(
        alm,
        text_content=text,
        title=document_title,
        add_to_workspaces=slug,
    )
    loc: str | None = None
    if isinstance(out, dict) and out.get("success") and isinstance(out.get("documents"), list):
        d0 = out["documents"][0] if out["documents"] else None
        if isinstance(d0, dict):
            loc = d0.get("location")
            if isinstance(loc, str):
                docs[logical_key] = {"sha256": h, "location": loc, "title": document_title}
                store["by_key"] = docs
                _save_json_path(p, store)
    return {
        "skipped": False,
        "logical_key": logical_key,
        "sha256": h,
        "api": out,
        "state_path": str(p),
    }
