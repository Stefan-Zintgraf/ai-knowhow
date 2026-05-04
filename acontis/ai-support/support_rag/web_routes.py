"""Optional browser UI: one-shot LLM chat, optional RAG, folder ingest (in-process)."""

from __future__ import annotations

import asyncio
import html
import json
import logging
import os
import re
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, field_validator

from support_rag.anythingllm_client import (
    ALM_WORKSPACE_CHAT_MODE_AUGMENTED,
    alm_error_message,
    ingest_raw_text_idempotent,
    list_workspace_slugs,
    litellm_gateway_reachable,
    option_b_host_match,
    resolve_workspace_effective,
    resolve_workspace_slug,
    summarize_alm_system_for_ui,
    try_get_system_settings,
    vector_search,
    workspace_chat,
)
from support_rag.config import (
    FIELD_SETTINGS_META,
    AppConfig,
    LlmGatewayConfig,
    WebUiState,
    _merge_rag_env_over_yaml,
    _read_yaml_config,
    _redact_for_browser,
    merge_config_patch_into_file,
    merge_web_ui_into_config_file,
    risk_notes_for_qdrant_shape_patch,
    risky_settings_if_unconfirmed,
    settings_patch_needs_rag_rebuild,
)
from support_rag.deps import (
    _trace_ctx,
    _ui_use_server_tokens_from_env,
    get_service,
    require_admin_ui,
    require_service_ui,
)
from support_rag.folder_ingest import (
    _DEFAULT_BATCH,
    _DEFAULT_PATTERNS,
    collect_docs,
    index_local_folder_inprocess,
)
from support_rag.schemas import RetrievalRequest, RetrievalResponse
from support_rag.service import RAGService

logger = logging.getLogger(__name__)

_NS: tuple[str, ...] = ("kb", "tickets")
_SUPPORT_RAG_TOP_K_MAX = 20
_ANYTHINGLLM_TOP_N_MAX = 12
_RETRIEVAL_CHUNKS_DEFAULT = 20
_RETRIEVAL_CHUNKS_HARD = 50


def _opt_b_blocks_chat_alm() -> str:
    return (
        "Option B (Desktop models via this project's llm_gateway) cannot be combined with "
        "chat model source 'AnythingLLM' — redundant routing. Use Option A, or set Chat model "
        "source to llm_gateway."
    )


def _ui_chat_effective_block(
    wu: WebUiState, lg: LlmGatewayConfig, health: dict[str, Any]
) -> dict[str, Any]:
    """
    What the Web UI chat will use, mirroring ``POST /ui/api/chat`` for **saved** ``web_ui``.

    Option A/B (``anythingllm_models_source``) is **not** the Support RAG retrieve path; it only
    documents how AnythingLLM Desktop should point its own LLM/embedder.
    """
    models = health.get("models") if isinstance(health, dict) else None
    ret_label = "unknown"
    chat_label = "unknown"
    if isinstance(models, dict):
        ret_label = str(models.get("retrieval_llm", "unknown"))
        chat_label = str(models.get("chat", "unknown"))
    use_service_gateway = wu.chat_model_source == "llm_gateway"
    route: Literal["llm_gateway", "anythingllm_native"] = (
        "llm_gateway" if use_service_gateway else "anythingllm_native"
    )
    out: dict[str, Any] = {
        "completion_route": route,
        "saved_use_rag": wu.use_rag,
        "saved_rag_source": wu.rag_source,
        "saved_chat_model_source": wu.chat_model_source,
        "saved_anythingllm_completion": wu.anythingllm_completion,
        "option_a_b_does_not_affect_this": True,
    }
    if route == "llm_gateway":
        out["llm_gateway"] = {
            "body_model": lg.chat_model,
            "chat_model": lg.chat_model,
            "x_slot": lg.chat_slot,
            "chat_label": chat_label,
            "retrieval_slot": lg.retrieval_slot,
            "retrieval_body_model": "retrieval",
            "retrieval_llm_label": ret_label,
        }
    return out


def _chat_context_anythingllm_block(
    *,
    cfg: AppConfig,
    wu: WebUiState,
    alm: AnythingLlmConfig,
) -> dict[str, Any]:
    """Workspace fields for GET /ui/api/chat-context (single source with resolve_workspace_effective)."""
    available: list[str] = []
    list_err: str | None = None
    try:
        available = list_workspace_slugs(alm)
    except Exception as e:
        logger.warning("chat-context: list_workspace_slugs failed: %s", e)
        list_err = alm_error_message(e)
        if len(list_err) > 500:
            list_err = list_err[:500] + "…"

    ov_raw = wu.anythingllm_workspace_slug_override or ""
    cfg_slug_raw = alm.workspace_slug or ""
    slug_meta, eff_res = resolve_workspace_effective(
        ov_raw,
        cfg_slug_raw,
        available,
        list_failed=(list_err is not None),
    )
    if eff_res == "none":
        ws = (ov_raw.strip() or cfg_slug_raw.strip() or "")
    else:
        ws = slug_meta

    out: dict[str, Any] = {
        "config_workspace_slug": cfg_slug_raw,
        "override_workspace_slug": ov_raw.strip(),
        "effective_workspace_slug": ws,
        "workspace_slug": ws,
        "available_workspace_slugs": available,
        "effective_resolution": eff_res,
    }
    if list_err:
        out["workspace_list_error"] = list_err
    return out


def _alm_resolution_hint_for_ui(eff_res: str) -> str:
    """Mirror ``_almResolutionHint`` in embedded Web UI script (keep copy in sync)."""
    if eff_res == "override":
        return "via override"
    if eff_res == "configured":
        return "via config"
    if eff_res == "implicit_first":
        return "via first workspace from AnythingLLM"
    return (
        "could not resolve — set YAML, override, or ensure AnythingLLM has a workspace"
    )


def _format_effective_workspace_line(effective_slug: str, eff_res: str) -> str:
    """Same wording as ``hydrateAlmWorkspaceFromContext`` in the Web UI script."""
    slug = (effective_slug or "").strip()
    slug_disp = slug if slug else "—"
    return f"Effective workspace: {slug_disp} — {_alm_resolution_hint_for_ui(eff_res)}"


def _public_base_url(url: str) -> str:
    """Scheme + host (+ port) only; no userinfo or path (for browser display)."""
    s = (url or "").strip()
    if not s:
        return ""
    if "://" not in s:
        s = "http://" + s
    p = urlparse(s)
    if p.scheme and p.netloc:
        host = p.netloc.split("@")[-1]
        return f"{p.scheme}://{host}".rstrip("/")
    return s.split("@")[-1]


def _verify_gateway_user_message(lit_ok: bool | None, gw_display: str) -> str:
    d = (gw_display or "").strip() or "(llm_gateway not configured)"
    if lit_ok is True:
        return f"Gateway: OK — GET {d}/health succeeded."
    if lit_ok is False:
        return (
            "Gateway: not OK — /health did not return success for "
            f"{d}. Start the gateway, match llm_gateway.base_url to its address, "
            "and set RAG_LLM_GATEWAY__API_KEY if the proxy requires a key."
        )
    return (
        f"Gateway: unknown — could not determine health for {d} (unexpected error; see server logs)."
    )


def _cap_retrieval_payload(
    resp: RetrievalResponse,
    *,
    char_cap: int,
    max_chunks: int,
) -> tuple[dict[str, Any], bool]:
    """Cap chunk text length and chunk count; ``meta.retrieval_truncated`` when needed."""
    lim = max(1, min(max_chunks, _RETRIEVAL_CHUNKS_HARD))
    truncated = False
    raw = resp.chunks
    if len(raw) > lim:
        truncated = True
        raw = raw[:lim]
    chunks_out: list[dict[str, Any]] = []
    for c in raw:
        t = c.text
        if len(t) > char_cap:
            truncated = True
            t = t[:char_cap] + "…[truncated]"
        chunks_out.append(
            {
                "id": c.id,
                "text": t,
                "metadata": c.metadata,
                "parent_id": c.parent_id,
                "score": c.score,
            }
        )
    return (
        {
            "chunks": chunks_out,
            "rewritten_queries": list(resp.rewritten_queries),
            "debug": dict(resp.debug),
        },
        truncated,
    )


def _httpx_error_payload(exc: BaseException) -> dict[str, Any]:
    detail = str(exc)[:2_000]
    http_status: int | None = None
    body_snippet = ""
    if isinstance(exc, httpx.HTTPStatusError) and exc.response is not None:
        http_status = int(exc.response.status_code)
        try:
            body_snippet = (exc.response.text or "")[:800]
        except Exception:
            body_snippet = ""
    return {
        "detail": detail,
        "http_status": http_status,
        "body_snippet": body_snippet,
    }


def _log_ui_chat(
    *,
    request_id: str,
    rag_source: str,
    completion_route: str,
    top_k: int | None,
    top_n: int | None,
    score_threshold: float | None,
    latency_ms_total: float,
    latency_ms_retrieval: float | None,
    latency_ms_completion: float | None,
    retrieval_count: int,
) -> None:
    logger.info(
        json.dumps(
            {
                "event": "ui_chat",
                "request_id": request_id,
                "rag_source": rag_source,
                "completion_route": completion_route,
                "top_k": top_k,
                "top_n": top_n,
                "score_threshold": score_threshold,
                "latency_ms_total": round(latency_ms_total, 3),
                "latency_ms_retrieval": None
                if latency_ms_retrieval is None
                else round(latency_ms_retrieval, 3),
                "latency_ms_completion": None
                if latency_ms_completion is None
                else round(latency_ms_completion, 3),
                "retrieval_count": retrieval_count,
            },
            default=str,
        )
    )

# Top-level ``AppConfig`` keys allowed in ``PUT /ui/api/settings`` body (excluding ``confirmed``)
_SETTINGS_ROOT_KEYS: frozenset[str] = frozenset(
    {
        "service",
        "llm_gateway",
        "qdrant",
        "retrieval",
        "chunking",
        "chunker_version",
        "observability",
        "web_ui",
        "anything_llm",
    }
)


async def _apply_settings_live(
    request: Request, new_cfg: AppConfig, patch: dict[str, Any]
) -> None:
    """Persisted YAML is already written; update in-process config and RAG service."""
    app = request.app
    lock = getattr(app.state, "settings_lock", None)
    if lock is None:
        raise HTTPException(500, "app state missing settings_lock")
    async with lock:
        if settings_patch_needs_rag_rebuild(patch):
            new_rag = RAGService(new_cfg)
            old = app.state.rag
            app.state.rag = new_rag
            app.state.config = new_cfg
            await old.aclose()
        else:
            app.state.config = new_cfg
            app.state.rag.rebind_config(new_cfg)


# Second <script> block for settings UI (kept as raw string: no f-string brace escaping)
_UI_SETTINGS_SCRIPT = r"""
<script>
(function() {
  const _order = ["service","llm_gateway","qdrant","retrieval","chunking","chunker_version","observability","web_ui","anything_llm"];
  function _walkObject(obj, pathPrefix, container, fieldMeta) {
    for (const k of Object.keys(obj).sort()) {
      const p = pathPrefix ? (pathPrefix + "." + k) : k;
      const v = obj[k];
      if (v !== null && typeof v === "object" && !Array.isArray(v)) {
        const sub = document.createElement("fieldset");
        const leg = document.createElement("legend");
        leg.textContent = k;
        sub.appendChild(leg);
        _walkObject(v, p, sub, fieldMeta);
        container.appendChild(sub);
      } else {
        const m = (fieldMeta && fieldMeta[p]) || {};
        const sp = document.createElement("span");
        sp.className = "hint";
        sp.setAttribute("title", m.hint || "");
        sp.textContent = "?";
        const label = document.createElement("label");
        if (typeof v === "boolean") {
          const inp = document.createElement("input");
          inp.type = "checkbox";
          inp.dataset.path = p;
          inp.checked = !!v;
          label.appendChild(inp);
          label.appendChild(document.createTextNode(" " + k + " "));
          label.appendChild(sp);
        } else {
          label.appendChild(document.createTextNode(k + " "));
          label.appendChild(sp);
          const inp = document.createElement("input");
          inp.type = (typeof v === "number") ? "number" : "text";
          if (typeof v === "number") { inp.step = "any"; }
          inp.dataset.path = p;
          inp.value = (v === null || v === undefined) ? "" : String(v);
          label.appendChild(inp);
        }
        container.appendChild(label);
      }
    }
  }
  function _buildForm(cfg, fieldMeta) {
    const el = document.getElementById("settingsRoot");
    if (!el) { return; }
    el.textContent = "";
    for (const sec of _order) {
      if (cfg[sec] == null) { continue; }
      const fs = document.createElement("fieldset");
      const leg = document.createElement("legend");
      leg.textContent = sec;
      fs.appendChild(leg);
      _walkObject(cfg[sec], sec, fs, fieldMeta);
      el.appendChild(fs);
    }
  }
  function _setPath(path, val, out) {
    const parts = path.split(".");
    let c = out;
    for (let i = 0; i < parts.length - 1; i++) {
      const a = parts[i];
      if (c[a] == null || typeof c[a] !== "object" || Array.isArray(c[a])) { c[a] = {}; }
      c = c[a];
    }
    c[parts[parts.length - 1]] = val;
  }
  function _collectPatch() {
    const out = {};
    const el = document.getElementById("settingsRoot");
    if (!el) { return out; }
    for (const inp of el.querySelectorAll("input[data-path]")) {
      const p = inp.dataset.path;
      if (!p) { continue; }
      let v;
      if (inp.type === "checkbox") { v = inp.checked; }
      else {
        const t = (inp.value || "").trim();
        if (t === "") { v = ""; }
        else if (inp.type === "number" && inp.step === "any") { v = parseFloat(t); if (Number.isNaN(v)) { v = null; } }
        else if (inp.type === "number") { v = parseInt(t, 10); if (Number.isNaN(v)) { v = null; } }
        else { v = t; }
      }
      _setPath(p, v, out);
    }
    return out;
  }
  async function _loadSettings() {
    const st = document.getElementById("settingsStatus");
    if (!st) { return; }
    try {
      const h = (typeof hhdr === "function") ? hhdr() : { "Content-Type": "application/json" };
      const r = await fetch("/ui/api/settings", { method: "GET", headers: h });
      if (!r.ok) { st.textContent = " Could not load (HTTP " + r.status + "). Check service token."; return; }
      const d = await r.json();
      _buildForm(d.config, d.field_meta);
      st.textContent = "";
    } catch (e) { st.textContent = " " + (e && e.message || e); }
  }
  async function _saveSettings(confirmed) {
    const st = document.getElementById("settingsStatus");
    if (!st) { return; }
    const hAdm = (typeof adminHdr === "function") ? adminHdr() : { "Content-Type": "application/json" };
    if (!hAdm["Authorization"]) { st.textContent = " Set admin token in the form to save."; return; }
    st.textContent = " Saving…";
    const patch = _collectPatch();
    const body = Object.assign({ confirmed: !!confirmed }, patch);
    try {
      const r = await fetch("/ui/api/settings", { method: "PUT", headers: hAdm, body: JSON.stringify(body) });
      const j = await r.json().catch(function() { return {}; });
      if (r.status === 409) {
        const w = (j.warnings && j.warnings.length) ? j.warnings.join("\n") : "Confirm?";
        if (window.confirm("Confirm: " + w)) { await _saveSettings(true); } else { st.textContent = " Cancelled."; }
        return;
      }
      if (!r.ok) { throw new Error((j && j.detail) || r.statusText); }
      st.textContent = " Saved. " + ((j.warnings && j.warnings.length) ? j.warnings.join(" ") : "");
      if (j.config) { _buildForm(j.config, j.field_meta || {}); }
    } catch (e) { st.textContent = " Error: " + (e && e.message || e); }
  }
  const b = document.getElementById("bSettingsSave");
  if (b) { b.onclick = function() { _saveSettings(false); }; }
  _loadSettings();
})();
</script>
"""


def _ui_hide_token_fields(request: Request) -> bool:
    cfg = request.app.state.config
    s = os.environ.get(cfg.service.service_token_env, "")
    a = os.environ.get(cfg.service.admin_token_env, "")
    if not (s and a):
        return False
    return _ui_use_server_tokens_from_env(request)


def _build_index_html(request: Request) -> str:
    cfg = request.app.state.config
    wu = cfg.web_ui
    initial = wu.model_dump()
    alm_boot_ctx = _chat_context_anythingllm_block(cfg=cfg, wu=wu, alm=cfg.anything_llm)
    boot = {
        "authFromEnv": _ui_hide_token_fields(request),
        "configPath": getattr(request.app.state, "config_path", ""),
        "webUi": initial,
        "anythingllmContext": alm_boot_ctx,
    }
    boot_json = json.dumps(boot, ensure_ascii=True)
    auth_block = """  <p class="muted">Paste bearer tokens (session only, not sent to a third party). Set <code>RAG_SERVICE_TOKEN</code> and <code>RAG_ADMIN_TOKEN</code> in the server environment to hide this section. No conversation history: each message is a single request.</p>
  <fieldset id="fsauth">
    <legend>Authentication</legend>
    <label>Service token (RAG retrieve + chat) <input id="svctok" type="password" autocomplete="off" placeholder="RAG service bearer"/></label>
    <label>Admin token (folder ingest) <input id="admtok" type="password" autocomplete="off" placeholder="RAG admin bearer"/></label>
  </fieldset>"""
    if _ui_hide_token_fields(request):
        auth_block = """  <p class="muted">Using <code>RAG_SERVICE_TOKEN</code> and <code>RAG_ADMIN_TOKEN</code> from the server environment (e.g. <code>.env</code>). No conversation history: each message is a single request. Form values are saved to the active config file when you edit them.</p>"""

    kb_sel = "selected" if wu.namespace == "kb" else ""
    t_sel = "selected" if wu.namespace == "tickets" else ""
    fpath = html.escape(wu.folder_path or "", quote=True)
    msg_esc = html.escape(wu.message_draft or "", quote=False)
    use_rag_chk = " checked" if wu.use_rag else ""
    r_sr = " checked" if wu.rag_source == "support_rag" else ""
    r_alm = " checked" if wu.rag_source == "anythingllm" else ""
    m_ad = " checked" if wu.anythingllm_models_source == "alm_desktop" else ""
    m_lg = " checked" if wu.anythingllm_models_source == "llm_gateway" else ""
    c_chat_gw = " checked" if wu.chat_model_source == "llm_gateway" else ""
    c_chat_alm = " checked" if wu.chat_model_source == "anythingllm" else ""
    sctx = " checked" if wu.show_retrieval_context else ""
    sth_s = (
        "" if wu.anythingllm_score_threshold is None else str(wu.anythingllm_score_threshold)
    )
    cfg_alm_slug = html.escape((cfg.anything_llm.workspace_slug or ""), quote=False)
    _eff_slug = alm_boot_ctx.get("effective_workspace_slug") or ""
    _eff_res = str(alm_boot_ctx.get("effective_resolution") or "none")
    alm_effective_html = html.escape(
        _format_effective_workspace_line(str(_eff_slug), _eff_res), quote=False
    )
    alm_folder = html.escape(wu.alm_ingest_folder_name or "", quote=True)
    alm_fpath = html.escape(wu.alm_ingest_folder_path or "", quote=True)
    a_k = int(wu.top_k)
    a_n = int(wu.anythingllm_top_n)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Support RAG — UI</title>
  <style>
    :root {{ font-family: system-ui, sans-serif; line-height: 1.4; }}
    body {{ max-width: 44rem; margin: 1.5rem auto; padding: 0 1rem; color: #1a1a1a; }}
    h1 {{ font-size: 1.25rem; }}
    fieldset {{ border: 1px solid #ccc; border-radius: 6px; padding: 0.75rem 1rem; margin-bottom: 1rem; }}
    legend {{ padding: 0 0.35rem; }}
    label {{ display: block; font-size: 0.85rem; margin-top: 0.4rem; }}
    input[type=text], input[type=password] {{ width: 100%; max-width: 32rem; box-sizing: border-box; padding: 0.35rem 0.5rem; }}
    textarea {{ width: 100%; min-height: 5rem; box-sizing: border-box; }}
    .row {{ display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; margin: 0.4rem 0; }}
    button {{ padding: 0.35rem 0.75rem; cursor: pointer; }}
    .muted {{ color: #555; font-size: 0.85rem; }}
    #alm_ingest_msg {{ white-space: pre-wrap; }}
    .out {{ white-space: pre-wrap; background: #f5f5f5; border-radius: 6px; padding: 0.75rem; min-height: 2rem; word-break: break-word; }}
    .err {{ color: #a20; word-break: break-word; }}
    a.nav {{ color: #05a; }}
    .hint {{ cursor: help; border: 1px solid #999; border-radius: 50%; font-size: 0.7rem; display: inline-block; width: 1.1em; height: 1.1em; text-align: center; line-height: 1.1em; margin-left: 0.2rem; vertical-align: text-top; }}
    #settings fieldset fieldset {{ margin-top: 0.4rem; border-style: dashed; }}
    .statusline {{ font-size: 0.85rem; padding: 0.5rem 0.6rem; background: #f0f0f0; border-radius: 6px; margin-bottom: 0.75rem; }}
    .oplinks {{ display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; margin: 0.5rem 0 0.75rem; font-size: 0.9rem; }}
    .oplinks a {{ min-height: 2.5rem; display: inline-flex; align-items: center; color: #05a; }}
    .is-hidden {{ display: none !important; }}
    .verify-ok {{ color: #060; font-weight: 500; }}
    .verify-warn {{ color: #a60; font-weight: 500; }}
    .verify-err {{ color: #a20; font-weight: 500; }}
    #verifyst.verify-msg {{ white-space: pre-wrap; display: inline-block; max-width: 56rem; margin-top: 0.35rem; vertical-align: top; line-height: 1.35; }}
    .panel {{ max-height: 16rem; overflow: auto; font-size: 0.8rem; background: #fafafa; border: 1px solid #ddd; border-radius: 4px; padding: 0.5rem; }}
    button {{ min-height: 2.5rem; min-width: 2.5rem; }}
  </style>
</head>
<body>
  <h1>Support RAG</h1>
  <p class="oplinks" id="jumprow">
    <a class="nav" href="#fchat">Chat</a>
    <a class="nav" href="#workspace-alm">AnythingLLM workspace</a>
    <a class="nav" href="#fingest">Ingest (local)</a>
    <a class="nav" href="#falmingest">Ingest (AnythingLLM)</a>
    <a class="nav" href="#settings">Settings (YAML)</a>
  </p>
{auth_block}
  <p id="statusline" class="statusline muted" role="status">Loading status…</p>
  <p class="oplinks" id="oplinks"></p>
  <fieldset id="foptab" aria-labelledby="leg-optab">
    <legend id="leg-optab">Model source (Option A / B)</legend>
    <p class="muted">For <strong>AnythingLLM Desktop</strong> only: how you point its own LLM + embedder (built-ins vs this project&rsquo;s <code>llm_gateway</code> at <code>llm_gateway.base_url</code>). Option A/B does <strong>not</strong> change Support RAG retrieval; use <a class="nav" href="#fchat">Chat</a> &rarr; <em>Chat model source</em> for where the user reply is generated.</p>
    <div class="row" role="radiogroup" aria-label="AnythingLLM model source">
      <label><input type="radio" name="models_src" value="alm_desktop" data-ui="anythingllm_models_source"{m_ad}/> Option A: AnythingLLM Desktop only (models in Desktop)</label>
    </div>
    <div class="row">
      <label><input type="radio" name="models_src" value="llm_gateway" data-ui="anythingllm_models_source"{m_lg}/> Option B: llm_gateway (set LLM/embedder in Desktop to this project&rsquo;s gateway)</label>
    </div>
    <div id="panel_optb" class="row is-hidden">
      <p class="muted">Verify that Desktop points at the same gateway host as <code>llm_gateway</code> in this service&rsquo;s config.</p>
      <button type="button" id="bverifyb">Verify Option B</button>
      <span id="verifyst" class="muted" role="status"></span>
    </div>
    <div id="workspace-alm" style="margin-top:0.75rem;padding:0.75rem;border:1px solid #ccc;border-radius:6px;background:#fafafa">
      <p class="muted" style="margin-top:0"><strong>AnythingLLM workspace</strong> — slug used for AnythingLLM vector search, workspace chat, and ingest (separate from Option A/B LLM routing above).</p>
      <p class="muted">Config (<code>anything_llm.workspace_slug</code>): <span id="alm_cfg_slug_display">{cfg_alm_slug}</span></p>
      <div class="row" role="radiogroup" aria-label="AnythingLLM workspace mode">
        <label><input type="radio" name="alm_ws_mode" id="alm_ws_mode_auto" value="auto" data-testid="workspace-mode-automatic"/> Automatic (follow YAML when set, else first workspace from AnythingLLM)</label>
      </div>
      <div class="row">
        <label><input type="radio" name="alm_ws_mode" id="alm_ws_mode_override" value="override" data-testid="workspace-mode-override"/> Override workspace (persisted in <code>web_ui</code>)</label>
      </div>
      <div id="alm_ws_override_panel" class="row is-hidden" style="flex-direction:column;align-items:stretch;gap:0.35rem">
        <label>Workspace from AnythingLLM
          <select id="alm_ws_sel" data-testid="workspace-slug-select" style="max-width:24rem"></select>
        </label>
        <label>Custom slug (if not in list)
          <input id="alm_ws_manual" type="text" data-testid="workspace-slug-manual" placeholder="e.g. my-workspace" style="max-width:24rem" autocomplete="off"/>
        </label>
      </div>
      <p id="alm_ws_list_warn" class="verify-warn is-hidden" role="status"></p>
      <p id="alm_effective_status" class="muted" data-testid="workspace-effective-line">{alm_effective_html}</p>
    </div>
  </fieldset>
  <fieldset id="fchat" aria-labelledby="leg-chat">
    <legend id="leg-chat">Chat</legend>
    <p id="chatRouteHint" class="muted" role="status">Loading which completion path and model the chat will use…</p>
    <div class="row">
      <span>RAG source</span>
      <label><input type="radio" name="ragsource" value="support_rag" data-ui="rag_source"{r_sr}/> Support RAG (Qdrant)</label>
      <label><input type="radio" name="ragsource" value="anythingllm" data-ui="rag_source"{r_alm}/> AnythingLLM (vector search)</label>
    </div>
    <div class="row">
      <label><input type="checkbox" id="userag"{use_rag_chk} data-ui="use_rag" /> Use retrieval (RAG) to augment the prompt</label>
    </div>
    <fieldset class="is-hidden" id="fret_srr" style="border-style:dashed;padding:0.5rem">
      <legend>Support RAG retrieval</legend>
      <label>top_k (max {_SUPPORT_RAG_TOP_K_MAX})
        <input type="number" id="itopk" min="1" max="{_SUPPORT_RAG_TOP_K_MAX}" step="1" value="{a_k}"/>
      </label>
    </fieldset>
    <fieldset class="is-hidden" id="fret_alm" style="border-style:dashed;padding:0.5rem">
      <legend>AnythingLLM retrieval</legend>
      <label>topN (max {_ANYTHINGLLM_TOP_N_MAX})
        <input type="number" id="itopn" min="1" max="{_ANYTHINGLLM_TOP_N_MAX}" step="1" value="{a_n}"/>
      </label>
      <label>score threshold (0–1)
        <input type="text" id="iscore" inputmode="decimal" placeholder="from config" value="{html.escape(sth_s, quote=True)}" style="max-width:8rem"/>
      </label>
    </fieldset>
    <div class="row">
      <label><input type="checkbox" id="ishowret"{sctx} data-ui="show_retrieval_context" /> Show retrieved context in the response (JSON / chunks)</label>
    </div>
    <fieldset style="border-style:dashed;padding:0.5rem" aria-labelledby="leg-chatsrc">
      <legend id="leg-chatsrc">Chat model source</legend>
      <p class="muted">Where the Web UI sends the <strong>user reply</strong> (not Option A/B above). RAG <em>rewrite</em> / HyDe still use <code>llm_gateway.retrieval_slot</code> and body model <code>retrieval</code> when those features are on.</p>
      <div class="row" role="radiogroup" aria-label="Chat model source">
        <label><input type="radio" name="chat_src" value="llm_gateway" data-ui="chat_model_source" data-testid="chat-src-llm-gateway"{c_chat_gw}/> This service &rarr; <code>llm_gateway</code> (X-Slot + model from /rag/health)</label>
        <label><input type="radio" name="chat_src" value="anythingllm" data-ui="chat_model_source" data-testid="chat-src-anythingllm"{c_chat_alm}/> AnythingLLM workspace chat</label>
      </div>
      <p id="optbChatHint" class="muted is-hidden" data-testid="optb-disabled-hint">With Option B, Desktop is already wired to this project&rsquo;s gateway; routing chat through AnythingLLM would be circular and is disabled. Use Option A or choose <code>llm_gateway</code> for chat.</p>
    </fieldset>
    <label>Message <textarea id="msg" data-ui="message_draft" placeholder="Your question...">{msg_esc}</textarea></label>
    <div class="row">
      <button type="button" id="bsend">Send to LLM</button>
    </div>
    <p class="muted">Assistant reply</p>
    <div id="out" class="out" aria-live="polite"></div>
    <p class="muted is-hidden" id="retl">Retrieved context (sanitized; may be truncated)</p>
    <div id="retout" class="panel is-hidden" aria-label="retrieval output"></div>
    <p id="cherr" class="err" role="alert"></p>
  </fieldset>
  <fieldset id="fingest" aria-labelledby="leg-ingest">
    <legend id="leg-ingest">Index folder (local to server &rarr; Qdrant)</legend>
    <div class="row">
      <label style="flex:1;min-width:12rem">Local path
        <input id="fpath" type="text" value="{fpath}" placeholder="e.g. C:\\\\docs or /home/u/kb" autocomplete="off"/>
      </label>
    </div>
    <div class="row">
      <label>Namespace
        <select id="fns">
          <option value="kb" {kb_sel}>kb</option>
          <option value="tickets" {t_sel}>tickets</option>
        </select>
      </label>
    </div>
    <div class="row">
      <button type="button" id="binge">Start embedding / ingest</button>
    </div>
    <p id="ingmsg" class="muted"></p>
  </fieldset>
  <fieldset id="falmingest" aria-labelledby="leg-alm">
    <legend id="leg-alm">Ingest folder to AnythingLLM workspace</legend>
    <p class="muted">Uploads text files as raw documents to the configured AnythingLLM workspace. Uses idempotency state on the server. Admin token required.</p>
    <div class="row">
      <label style="flex:1;min-width:12rem">Local path
        <input id="fpath_alm" type="text" value="{alm_fpath}" placeholder="e.g. C:\\\\docs" autocomplete="off"/>
      </label>
    </div>
    <div class="row">
      <label>Optional folder label (for titles) <input id="alm_fld" type="text" value="{alm_folder}" placeholder="server folder name" data-ui="alm_ingest_folder_name"/></label>
    </div>
    <p class="muted">Workspace: uses <a class="nav" href="#workspace-alm">AnythingLLM workspace</a> above (same effective slug for ingest, chat, and vector search).</p>
    <div class="row">
      <button type="button" id="balm_ingest">Ingest to AnythingLLM</button>
    </div>
    <p id="alm_ingest_msg" class="muted" role="status"></p>
  </fieldset>
  <fieldset id="settings">
    <legend>Configuration (YAML)</legend>
    <p class="muted">Values come from the active config file. Hover <span class="hint" style="position:static; display: inline-block;">?</span> for help. Save uses the <strong>admin</strong> token. <span id="settingsStatus"></span></p>
    <div id="settingsRoot"><p class="muted">Loading…</p></div>
    <div class="row" style="margin-top:0.5rem">
      <button type="button" id="bSettingsSave">Save settings</button>
    </div>
  </fieldset>
  <script>
  window.__RAG_UI__ = {boot_json};
  const $ = (id) => document.getElementById(id);
  function hhdr() {{
    const t = ($("svctok") && $("svctok").value) || "";
    const h = {{ "Content-Type": "application/json" }};
    if (t) h["Authorization"] = "Bearer " + t;
    return h;
  }}
  function adminHdr() {{
    const t = ($("admtok") && $("admtok").value) || "";
    const h = {{ "Content-Type": "application/json" }};
    if (t) h["Authorization"] = "Bearer " + t;
    return h;
  }}
  let _saveT = null;
  let _pendingUiPatch = null;
  function saveUiPatch(patch) {{
    _pendingUiPatch = Object.assign({{}}, _pendingUiPatch || {{}}, patch);
    if (_saveT) clearTimeout(_saveT);
    _saveT = setTimeout(async () => {{
      const body = _pendingUiPatch;
      _pendingUiPatch = null;
      _saveT = null;
      if (!body || Object.keys(body).length === 0) return;
      try {{
        const r = await fetch("/ui/api/web-ui", {{ method: "PUT", headers: hhdr(), body: JSON.stringify(body) }});
        if (!r.ok) {{ const j = await r.json().catch(() => ({{}})); throw new Error((j && j.detail) || r.statusText); }}
        loadChatContext();
      }} catch (e) {{ console.warn("save web-ui", e); }}
    }}, 400);
  }}
  let _ctx = null;
  function setChatRouteHint(ctx) {{
    const el = $("chatRouteHint");
    if (!el) return;
    const u = ctx && ctx.ui_chat_effective;
    if (!u) {{ el.textContent = ""; return; }}
    if (u.completion_route === "anythingllm_native") {{
      el.textContent = "With saved Chat settings, the reply uses AnythingLLM workspace chat (model is whatever AnythingLLM has selected). Option A/B only affects the Desktop — not this path.";
    }} else {{
      const g = u.llm_gateway || {{}};
      const chatL = g.chat_label ? g.chat_label : "unknown";
      const rlab = g.retrieval_llm_label ? g.retrieval_llm_label : "unknown";
      const xslot = g.x_slot != null ? g.x_slot : "";
      const cms = g.chat_model != null ? g.chat_model : "retrieval";
      const rslot = g.retrieval_slot != null ? g.retrieval_slot : "";
      el.textContent = "User chat: body model '" + cms + "', header X-Slot: " + xslot + ". Label: " + chatL + ". Query rewrite / HyDe (if enabled) use X-Slot " + rslot + " and body model 'retrieval' (label " + rlab + ").";
    }}
  }}
  function _almResolutionHint(res) {{
    if (res === "override") return "via override";
    if (res === "configured") return "via config";
    if (res === "implicit_first") return "via first workspace from AnythingLLM";
    return "could not resolve — set YAML, override, or ensure AnythingLLM has a workspace";
  }}
  function syncAlmWorkspacePanel() {{
    const ovm = document.querySelector('input[name="alm_ws_mode"][value="override"]');
    const pan = $("alm_ws_override_panel");
    if (pan && ovm) pan.classList.toggle("is-hidden", !ovm.checked);
  }}
  function persistAlmWorkspaceOverrideFromFields() {{
    const ovm = document.querySelector('input[name="alm_ws_mode"][value="override"]');
    if (!ovm || !ovm.checked) return;
    const manual = ($("alm_ws_manual") && $("alm_ws_manual").value || "").trim();
    const sel = ($("alm_ws_sel") && $("alm_ws_sel").value || "").trim();
    const slug = manual || sel;
    saveUiPatch({{ anythingllm_workspace_slug_override: slug }});
  }}
  function hydrateAlmWorkspaceFromContext(ctx) {{
    const a = ctx && ctx.anythingllm || {{}};
    const cfgEl = $("alm_cfg_slug_display");
    if (cfgEl) {{
      const cs = a.config_workspace_slug;
      cfgEl.textContent = (cs != null && String(cs).trim() !== "") ? String(cs) : "(empty — first workspace or override)";
    }}
    const warn = $("alm_ws_list_warn");
    if (warn) {{
      const err = a.workspace_list_error || "";
      if (err) {{ warn.textContent = "Could not list workspaces: " + err; warn.classList.remove("is-hidden"); }}
      else {{ warn.textContent = ""; warn.classList.add("is-hidden"); }}
    }}
    const sel = $("alm_ws_sel");
    const manual = $("alm_ws_manual");
    const slugs = Array.isArray(a.available_workspace_slugs) ? a.available_workspace_slugs : [];
    if (sel) {{
      sel.textContent = "";
      const o0 = document.createElement("option");
      o0.value = ""; o0.textContent = "—"; sel.appendChild(o0);
      for (const s of slugs) {{
        const op = document.createElement("option");
        op.value = s; op.textContent = s; sel.appendChild(op);
      }}
    }}
    const ovr = (a.override_workspace_slug || "").trim();
    const autoR = $("alm_ws_mode_auto");
    const ovR = $("alm_ws_mode_override");
    if (ovr) {{
      if (ovR) ovR.checked = true;
      if (autoR) autoR.checked = false;
      if (manual && sel) {{
        if (slugs.indexOf(ovr) >= 0) {{ sel.value = ovr; manual.value = ""; }}
        else {{ sel.value = ""; manual.value = ovr; }}
      }}
    }} else {{
      if (autoR) autoR.checked = true;
      if (ovR) ovR.checked = false;
      if (manual) manual.value = "";
      if (sel) sel.value = "";
    }}
    const effEl = $("alm_effective_status");
    if (effEl) {{
      const slug = a.effective_workspace_slug || "";
      const res = a.effective_resolution || "none";
      effEl.textContent = "Effective workspace: " + (slug || "—") + " — " + _almResolutionHint(res);
    }}
    syncAlmWorkspacePanel();
  }}
  async function loadChatContext() {{
    const st = $("statusline");
    if (!st) return;
    try {{
      const r = await fetch("/ui/api/chat-context", {{ headers: hhdr() }});
      if (!r.ok) {{ st.textContent = "Could not load chat context (HTTP " + r.status + ")."; if ($("chatRouteHint")) $("chatRouteHint").textContent = ""; return; }}
      _ctx = await r.json();
      setChatRouteHint(_ctx);
      hydrateAlmWorkspaceFromContext(_ctx);
      const a = _ctx.anythingllm || {{}};
      const g = _ctx.llm_gateway || {{}};
      const lit = (g.litellm_reachable === true) ? "reachable" : (g.litellm_reachable === false) ? "unreachable" : "unknown";
      let line = (a.base_url_display || "—") + " · ALM: ";
      line += a.alm_provider_summary ? a.alm_provider_summary : "Mode A/B = guidance only — verify in AnythingLLM Desktop.";
      line += " · Gateway: " + lit;
      st.textContent = line;
      const op = $("oplinks");
      if (op && _ctx.ui && _ctx.ui.links) {{
        op.textContent = "";
        for (const L of _ctx.ui.links) {{
          const ela = document.createElement("a");
          ela.href = L.url; ela.className = "nav"; ela.target = "_blank"; ela.rel = "noopener noreferrer";
          ela.textContent = L.label; op.appendChild(ela);
        }}
      }}
    }} catch (e) {{ st.textContent = "Status: " + (e && e.message || e); }}
  }}
  function getRagSource() {{ const g = document.querySelector("input[name=ragsource]:checked"); return g ? g.value : "support_rag"; }}
  function getModelsSource() {{ const g = document.querySelector("input[name=models_src]:checked"); return g ? g.value : "alm_desktop"; }}
  function getChatSrc() {{ const g = document.querySelector("input[name=chat_src]:checked"); return g ? g.value : "llm_gateway"; }}
  function syncRagPanel() {{
    const ur = $("userag");
    const use = ur && ur.checked;
    const rs = getRagSource();
    const fsr = $("fret_srr");
    const falm = $("fret_alm");
    if (fsr) fsr.classList.toggle("is-hidden", !use || rs !== "support_rag");
    if (falm) falm.classList.toggle("is-hidden", !use || rs !== "anythingllm");
  }}
  function syncOptBAndChat() {{
    const ms = getModelsSource();
    const p = $("panel_optb");
    const bv = $("bverifyb");
    if (p) p.classList.toggle("is-hidden", ms !== "llm_gateway");
    if (bv) bv.disabled = (ms !== "llm_gateway");
    const hint = $("optbChatHint");
    const almRadio = document.querySelector("input[name=chat_src][value=anythingllm]");
    if (ms === "llm_gateway") {{
      if (almRadio) {{ almRadio.disabled = true; if (almRadio.checked) document.querySelector("input[name=chat_src][value=llm_gateway]").click(); }}
      if (hint) hint.classList.remove("is-hidden");
    }} else {{
      if (almRadio) almRadio.disabled = false;
      if (hint) hint.classList.add("is-hidden");
    }}
  }}
  function hydrateFromBoot() {{
    const b = window.__RAG_UI__;
    if (!b || !b.webUi) return;
    const u = b.webUi;
    const fa = $("fpath_alm");
    if (fa && typeof u.alm_ingest_folder_path === "string") fa.value = u.alm_ingest_folder_path;
    const af = $("alm_fld");
    if (af && typeof u.alm_ingest_folder_name === "string") af.value = u.alm_ingest_folder_name;
    const ovrBoot = (u.anythingllm_workspace_slug_override || "").trim();
    const autoR = $("alm_ws_mode_auto");
    const ovR = $("alm_ws_mode_override");
    if (ovrBoot) {{
      if (ovR) ovR.checked = true;
      if (autoR) autoR.checked = false;
      const manual = $("alm_ws_manual");
      const sel = $("alm_ws_sel");
      if (manual) manual.value = ovrBoot;
      if (sel) sel.value = "";
    }} else {{
      if (autoR) autoR.checked = true;
      if (ovR) ovR.checked = false;
      if ($("alm_ws_manual")) $("alm_ws_manual").value = "";
    }}
    syncAlmWorkspacePanel();
    const fp = $("fpath");
    if (fp && typeof u.folder_path === "string") fp.value = u.folder_path;
    const ns = $("fns");
    if (ns && u.namespace) ns.value = u.namespace;
    const msg = $("msg");
    if (msg && typeof u.message_draft === "string") msg.value = u.message_draft;
    const ur = $("userag");
    if (ur && typeof u.use_rag === "boolean") ur.checked = u.use_rag;
    const isr = $("ishowret");
    if (isr && typeof u.show_retrieval_context === "boolean") isr.checked = u.show_retrieval_context;
    const itk = $("itopk");
    if (itk && typeof u.top_k === "number") itk.value = String(u.top_k);
    const itn = $("itopn");
    if (itn && typeof u.anythingllm_top_n === "number") itn.value = String(u.anythingllm_top_n);
    const isc = $("iscore");
    if (isc) {{
      if (u.anythingllm_score_threshold == null) isc.value = "";
      else isc.value = String(u.anythingllm_score_threshold);
    }}
    for (const el of document.querySelectorAll("input[name=models_src]")) {{
      el.checked = (el.value === u.anythingllm_models_source);
    }}
    for (const el of document.querySelectorAll("input[name=ragsource]")) {{
      el.checked = (el.value === u.rag_source);
    }}
    for (const el of document.querySelectorAll("input[name=chat_src]")) {{
      el.checked = (el.value === (u.chat_model_source || "llm_gateway"));
    }}
  }}
  hydrateFromBoot();
  const _bootAlmCtx = (window.__RAG_UI__ || {{}}).anythingllmContext;
  if (_bootAlmCtx) {{
    hydrateAlmWorkspaceFromContext({{ anythingllm: _bootAlmCtx }});
  }}
  for (const el of document.querySelectorAll("input[name=models_src]")) {{
    el.addEventListener("change", function() {{ saveUiPatch({{ anythingllm_models_source: this.value }}); syncOptBAndChat(); }});
  }}
  for (const el of document.querySelectorAll("input[name=ragsource]")) {{
    el.addEventListener("change", function() {{ saveUiPatch({{ rag_source: this.value }}); syncRagPanel(); }});
  }}
  for (const el of document.querySelectorAll("input[name=chat_src]")) {{
    el.addEventListener("change", function() {{
      if (this.value === "anythingllm" && getModelsSource() === "llm_gateway") return;
      saveUiPatch({{ chat_model_source: this.value }});
    }});
  }}
  const _fp = $("fpath");
  if (_fp) _fp.addEventListener("input", () => saveUiPatch({{ folder_path: _fp.value }}));
  const _fpalm = $("fpath_alm");
  if (_fpalm) _fpalm.addEventListener("input", () => saveUiPatch({{ alm_ingest_folder_path: _fpalm.value }}));
  const _fns = $("fns");
  if (_fns) _fns.addEventListener("change", () => saveUiPatch({{ namespace: _fns.value }}));
  const _ur = $("userag");
  if (_ur) _ur.addEventListener("change", () => {{ saveUiPatch({{ use_rag: _ur.checked }}); syncRagPanel(); }});
  const _msg = $("msg");
  if (_msg) _msg.addEventListener("input", () => saveUiPatch({{ message_draft: _msg.value }}));
  const _itk = $("itopk");
  if (_itk) _itk.addEventListener("input", () => {{ const v = parseInt(_itk.value, 10); if (!Number.isNaN(v)) saveUiPatch({{ top_k: v }}); }});
  const _itn = $("itopn");
  if (_itn) _itn.addEventListener("input", () => {{ const v = parseInt(_itn.value, 10); if (!Number.isNaN(v)) saveUiPatch({{ anythingllm_top_n: v }}); }});
  const _isc = $("iscore");
  if (_isc) _isc.addEventListener("input", () => {{
    const t = (_isc.value || "").trim();
    if (t === "") saveUiPatch({{ anythingllm_score_threshold: null }});
    else {{ const x = parseFloat(t); if (!Number.isNaN(x)) saveUiPatch({{ anythingllm_score_threshold: x }}); }}
  }});
  const _isr = $("ishowret");
  if (_isr) _isr.addEventListener("change", () => saveUiPatch({{ show_retrieval_context: _isr.checked }}));
  for (const el of document.querySelectorAll('input[name="alm_ws_mode"]')) {{
    el.addEventListener("change", function() {{
      syncAlmWorkspacePanel();
      if (this.value === "auto") {{
        saveUiPatch({{ anythingllm_workspace_slug_override: "" }});
      }} else {{
        persistAlmWorkspaceOverrideFromFields();
      }}
    }});
  }}
  const _almSel = $("alm_ws_sel");
  if (_almSel) _almSel.addEventListener("change", () => persistAlmWorkspaceOverrideFromFields());
  const _almMan = $("alm_ws_manual");
  if (_almMan) _almMan.addEventListener("input", () => persistAlmWorkspaceOverrideFromFields());
  const _af = $("alm_fld");
  if (_af) _af.addEventListener("input", () => saveUiPatch({{ alm_ingest_folder_name: _af.value }}));
  syncRagPanel();
  syncOptBAndChat();
  loadChatContext();
  if ($("bverifyb")) $("bverifyb").onclick = async () => {{
    const st = $("verifyst");
    const br = String.fromCharCode(10);
    const docHint = "Docs: docs/e2e-anythingllm.md#option-b-via-litellm-gateway";
    if (st) {{ st.textContent = "Checking…"; st.className = "verify-msg muted"; }}
    try {{
      const r = await fetch("/ui/api/anythingllm/verify-option-b", {{ method: "POST", headers: adminHdr() }});
      const j = await r.json();
      if (!r.ok) throw new Error((j && j.detail) || r.statusText);
      const litOk = (j.litellm_reachable === true);
      const almOk = (j.anythingllm_ok === true);
      const hostOk = (j.host_match === true);
      let cls = "verify-msg verify-err";
      if (litOk && almOk && hostOk) cls = "verify-msg verify-ok";
      else if (litOk && almOk) cls = "verify-msg verify-warn";
      if (st) {{
        st.className = cls;
        const lines = [j.litellm_message, j.anythingllm_message, j.host_match_message].filter(Boolean);
        st.textContent = lines.join(br);
        if (!(litOk && almOk && hostOk)) st.textContent += br + br + docHint;
      }}
      loadChatContext();
    }} catch (e) {{ if (st) {{ st.className = "verify-msg verify-err"; st.textContent = (e && e.message) || String(e); }} }}
  }};
  if ($("balm_ingest")) $("balm_ingest").onclick = async () => {{
    const m = $("alm_ingest_msg");
    m.textContent = "";
    const h = adminHdr();
    const path = ($("fpath_alm") && $("fpath_alm").value || "").trim();
    if (!path) {{ m.textContent = "Enter a folder path."; return; }}
    m.textContent = "Ingesting to AnythingLLM…";
    const body = {{ path, server_folder_name: ($("alm_fld") && $("alm_fld").value) || "" }};
    try {{
      const r = await fetch("/ui/api/ingest-folder-anythingllm", {{ method: "POST", headers: h, body: JSON.stringify(body) }});
      const j = await r.json();
      if (!r.ok) throw new Error((j && j.detail) || r.statusText);
      let line = "Done: ingested " + (j.ingested != null ? j.ingested : 0) + ", skipped " + (j.skipped || 0) + ", errors: " + (j.errors && j.errors.length || 0);
      if (j.errors && j.errors.length) line += "\\n" + j.errors.join("\\n");
      m.textContent = line;
    }} catch (e) {{ m.textContent = "Error: " + (e && e.message || e); }}
  }};
  $("binge") && ($("binge").onclick = async () => {{
    const msg = $("ingmsg");
    msg.textContent = "";
    const h = adminHdr();
    const path = ($("fpath") && $("fpath").value || "").trim();
    if (!path) {{ msg.textContent = "Enter a folder path."; return; }}
    const namespace = ($("fns") && $("fns").value) || "kb";
    msg.textContent = "Ingesting…";
    try {{
      const r = await fetch("/ui/api/ingest-folder", {{ method: "POST", headers: h, body: JSON.stringify({{ path, namespace }}) }});
      const j = await r.json();
      if (!r.ok) throw new Error((j && j.detail) || r.statusText);
      msg.textContent = "Done: " + (j.indexed != null ? ("indexed " + j.indexed + " parent doc(s), skipped " + (j.n_skip || 0)) : JSON.stringify(j));
    }} catch (e) {{
      msg.textContent = "Error: " + (e && e.message || e);
    }}
  }});
  $("bsend") && ($("bsend").onclick = async () => {{
    const errEl = $("cherr");
    const out = $("out");
    const retl = $("retl");
    const retout = $("retout");
    errEl.textContent = "";
    out.textContent = "";
    if (retl) retl.classList.add("is-hidden");
    if (retout) {{ retout.classList.add("is-hidden"); retout.textContent = ""; }}
    const h = hhdr();
    const text = ($("msg") && $("msg").value || "").trim();
    if (!text) {{ errEl.textContent = "Enter a message."; return; }}
    const useRag = $("userag") && $("userag").checked;
    const rs = getRagSource();
    const payload = {{ message: text, use_rag: useRag, include_retrieval: ($("ishowret") && $("ishowret").checked) || false, rag_source: rs }};
    payload.chat_model_source = (getChatSrc() === "anythingllm") ? "anythingllm" : "llm_gateway";
    if (useRag && rs === "support_rag") {{
      const k = parseInt($("itopk") && $("itopk").value, 10);
      if (!Number.isNaN(k)) payload.top_k = k;
    }}
    if (useRag && rs === "anythingllm") {{
      const n = parseInt($("itopn") && $("itopn").value, 10);
      if (!Number.isNaN(n)) payload.top_n = n;
      const sc = ($("iscore") && $("iscore").value || "").trim();
      if (sc !== "") {{
        const x = parseFloat(sc);
        if (!Number.isNaN(x)) payload.score_threshold = x;
      }}
    }}
    try {{
      const r = await fetch("/ui/api/chat", {{ method: "POST", headers: h, body: JSON.stringify(payload) }});
      const j = await r.json().catch(() => ({{}}));
      if (!r.ok) {{
        const parts = [];
        if (j.detail) {{ if (typeof j.detail === "string") parts.push(j.detail); else if (j.detail) parts.push(String(j.detail)); }}
        if (j.http_status != null) parts.push("HTTP " + j.http_status);
        if (j.body_snippet) parts.push(String(j.body_snippet).slice(0, 500));
        throw new Error(parts.join(" — ") || r.statusText);
      }}
      out.textContent = (j && j.reply) != null ? j.reply : "";
      if (j.retrieval) {{
        if (retl) retl.classList.remove("is-hidden");
        if (retout) {{ retout.classList.remove("is-hidden"); retout.textContent = JSON.stringify(j.retrieval, null, 2); }}
      }}
    }} catch (e) {{
      errEl.textContent = (e && e.message) || String(e);
    }}
  }});
  </script>""" + _UI_SETTINGS_SCRIPT + """
</body>
</html>
"""


class UIChatBody(BaseModel):
    message: str = Field(min_length=1, max_length=120_000)
    use_rag: bool = False
    rag_source: Literal["support_rag", "anythingllm"] | None = None
    chat_model_source: Literal["llm_gateway", "anythingllm"] | None = None
    top_k: int | None = Field(default=None, ge=1, le=32)
    top_n: int | None = Field(default=None, ge=1, le=100)
    score_threshold: float | None = Field(default=None, ge=0.0, le=1.0)
    include_retrieval: bool = False

    @field_validator("score_threshold", mode="before")
    @classmethod
    def _empty_score(cls, v: Any) -> Any:
        if v is None or v == "":
            return None
        return v


class UIFolderIngestBody(BaseModel):
    path: str = Field(min_length=1, max_length=4_096)
    namespace: Literal["kb", "tickets"] = "kb"

    @field_validator("path")
    @classmethod
    def strip_path(cls, v: str) -> str:
        return v.strip()


class WebUiPatch(BaseModel):
    folder_path: str | None = None
    namespace: Literal["kb", "tickets"] | None = None
    use_rag: bool | None = None
    message_draft: str | None = None
    rag_source: Literal["support_rag", "anythingllm"] | None = None
    anythingllm_models_source: Literal["alm_desktop", "llm_gateway"] | None = None
    chat_model_source: Literal["llm_gateway", "anythingllm"] | None = None
    anythingllm_completion: Literal["gateway", "anythingllm_native"] | None = None
    show_retrieval_context: bool | None = None
    top_k: int | None = Field(default=None, ge=1, le=32)
    anythingllm_top_n: int | None = Field(default=None, ge=1, le=100)
    anythingllm_score_threshold: float | None = None
    anythingllm_workspace_slug_override: str | None = None
    retrieval_chunk_char_cap: int | None = Field(default=None, ge=256, le=200_000)
    anythingllm_ingest_state_path: str | None = None
    alm_ingest_folder_name: str | None = None  # default folder label for ALM ingest
    alm_ingest_folder_path: str | None = None

    @field_validator("anythingllm_models_source", mode="before")
    @classmethod
    def _patch_coerce_llm_gateway_name(cls, v: Any) -> Any:
        if v == "litellm_gateway":
            return "llm_gateway"
        return v


class UIAnythingLlmIngestBody(BaseModel):
    path: str = Field(min_length=1, max_length=4_096)
    server_folder_name: str = ""
    workspace_slug: str | None = None

    @field_validator("path", "server_folder_name", "workspace_slug")
    @classmethod
    def _strip_s(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return v.strip()


def _augmented_content(user_message: str, resp: Any) -> str:
    if not resp.chunks:
        return (
            "The following knowledge base search returned no passages. "
            "Answer using general knowledge as needed.\n\n"
            f"User question: {user_message}"
        )
    parts: list[str] = []
    for c in resp.chunks[:10]:
        parts.append(f"[{c.parent_id}]\n{c.text}\n")
    block = "\n---\n".join(parts)
    return (
        "Use the following context from the support knowledge base when it helps. "
        "If it is not relevant, answer from general knowledge.\n\n"
        f"{block}\n\nUser question: {user_message}"
    )


def build_ui_router() -> APIRouter:
    r = APIRouter(prefix="/ui", tags=["ui"])

    @r.get("/")
    async def ui_index(request: Request) -> HTMLResponse:
        return HTMLResponse(_build_index_html(request))

    @r.get("/api/web-ui")
    async def get_web_ui(
        request: Request,
        _s: str = Depends(require_service_ui),
    ) -> JSONResponse:
        p = getattr(request.app.state, "config_path", "")
        wu = request.app.state.config.web_ui.model_dump()
        return JSONResponse(
            {
                "config_path": p,
                "web_ui": wu,
                "auth_from_env": _ui_hide_token_fields(request),
            }
        )

    @r.put("/api/web-ui")
    async def put_web_ui(
        body: WebUiPatch,
        request: Request,
        _s: str = Depends(require_service_ui),
    ) -> JSONResponse:
        cfg = request.app.state.config
        cur = dict(cfg.web_ui.model_dump())
        for k, v in body.model_dump(exclude_unset=True).items():
            if v is not None:
                cur[k] = v
        try:
            new_state = WebUiState(**cur)
        except Exception as e:
            raise HTTPException(400, str(e)[:1_000]) from e
        cpath = getattr(request.app.state, "config_path", None)
        if not cpath:
            raise HTTPException(500, "config file path not set (RAG_CONFIG)")
        pp = Path(cpath)
        if not pp.is_file():
            raise HTTPException(500, f"config file not found: {cpath}")
        try:
            merge_web_ui_into_config_file(cpath, new_state.model_dump())
        except OSError as e:
            raise HTTPException(500, f"failed to write config: {e}") from e
        cfg.web_ui = new_state
        return JSONResponse(
            {
                "config_path": cpath,
                "web_ui": new_state.model_dump(),
            }
        )

    @r.get("/api/settings")
    async def get_settings(
        request: Request,
        _s: str = Depends(require_service_ui),
    ) -> JSONResponse:
        cfg = request.app.state.config
        return JSONResponse(
            {
                "config": _redact_for_browser(
                    cfg.model_dump(mode="json"), cfg=cfg
                ),
                "field_meta": FIELD_SETTINGS_META,
            }
        )

    @r.put("/api/settings")
    async def put_settings(
        request: Request,
        _a: str = Depends(require_admin_ui),
    ) -> JSONResponse:
        raw = await request.json()
        if not isinstance(raw, dict):
            raise HTTPException(400, "expected JSON object")
        body: dict[str, Any] = dict(raw)
        confirmed = bool(body.pop("confirmed", False))
        for k in body:
            if k not in _SETTINGS_ROOT_KEYS:
                raise HTTPException(
                    400,
                    f"unknown or disallowed key: {k!r} (use top-level config sections only)",
                )
        patch: dict[str, Any] = {k: v for k, v in body.items() if v is not None}
        if not patch:
            raise HTTPException(400, "empty patch (nothing to update)")
        w_block = risky_settings_if_unconfirmed(patch, confirmed=confirmed)
        if w_block:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "require_confirmation": True,
                    "warnings": w_block,
                },
            )
        cpath = getattr(request.app.state, "config_path", None)
        if not cpath:
            raise HTTPException(500, "config file path not set (RAG_CONFIG)")
        pp = Path(cpath)
        if not pp.is_file():
            raise HTTPException(500, f"config file not found: {cpath}")
        try:
            merge_config_patch_into_file(cpath, patch)
        except OSError as e:
            raise HTTPException(500, f"failed to write config: {e}") from e
        merged_root = _read_yaml_config(str(cpath)) or {}
        try:
            new_cfg = AppConfig(**_merge_rag_env_over_yaml(merged_root))
        except Exception as e:
            raise HTTPException(400, f"invalid config after merge: {e!s}") from e
        try:
            await _apply_settings_live(request, new_cfg, patch)
        except Exception as e:
            logger.exception("apply settings live")
            raise HTTPException(500, str(e)[:2_000]) from e
        notes = risk_notes_for_qdrant_shape_patch(patch)
        return JSONResponse(
            {
                "config": _redact_for_browser(
                    new_cfg.model_dump(mode="json"), cfg=new_cfg
                ),
                "warnings": notes,
                "field_meta": FIELD_SETTINGS_META,
            }
        )

    @r.get("/api/chat-context")
    async def chat_context(
        request: Request,
        _s: str = Depends(require_service_ui),
        service: Any = Depends(get_service),
    ) -> JSONResponse:
        cfg = request.app.state.config
        wu = cfg.web_ui
        alm = cfg.anything_llm
        lg = cfg.llm_gateway
        try:
            health = await service.health()
        except Exception as e:
            logger.warning("chat-context: service.health failed: %s", e)
            health = {}
        alm_base = _public_base_url(alm.base_url)
        gw_base = _public_base_url(lg.base_url)
        alm_workspace = await asyncio.to_thread(
            lambda: _chat_context_anythingllm_block(cfg=cfg, wu=wu, alm=alm),
        )

        litellm_reachable: bool | None = None
        try:
            litellm_reachable = await asyncio.to_thread(
                litellm_gateway_reachable,
                lg.base_url,
                api_key=lg.api_key,
            )
        except Exception:
            litellm_reachable = None

        alm_sum: str | None = None
        alm_mode: str | None = None
        raw_alm, alm_load_err = await asyncio.to_thread(try_get_system_settings, alm)
        if raw_alm is not None:
            alm_sum, alm_mode, _h = summarize_alm_system_for_ui(raw_alm)
        elif alm_load_err:
            alm_sum = alm_load_err[:280]
            alm_mode = None

        docs_url = f"{alm_base}/api/docs" if alm_base else ""
        ui_chat_effective = _ui_chat_effective_block(wu, lg, health if isinstance(health, dict) else {})
        payload: dict[str, Any] = {
            "rag_source": wu.rag_source,
            "ui_chat_effective": ui_chat_effective,
            "anythingllm": {
                "models_source": wu.anythingllm_models_source,
                "chat_model_source": wu.chat_model_source,
                "anythingllm_completion": wu.anythingllm_completion,
                "base_url_display": alm_base,
                "alm_provider_summary": alm_sum,
                "alm_chat_mode_default": alm_mode,
                **alm_workspace,
            },
            "llm_gateway": {
                "base_url_display": gw_base,
                "litellm_reachable": litellm_reachable,
            },
            "retrieval_caps": {
                "support_rag_top_k_max": _SUPPORT_RAG_TOP_K_MAX,
                "anythingllm_top_n_max": _ANYTHINGLLM_TOP_N_MAX,
                "retrieval_chunk_char_cap": wu.retrieval_chunk_char_cap,
            },
            "ui": {
                "show_retrieval_context": wu.show_retrieval_context,
                "links": [
                    {"label": "AnythingLLM API docs", "url": docs_url},
                    {
                        "label": "Runbook (Option A)",
                        "url": "docs/e2e-anythingllm.md#option-a-alm-desktop-only",
                    },
                    {
                        "label": "Runbook (Option B)",
                        "url": "docs/e2e-anythingllm.md#option-b-via-litellm-gateway",
                    },
                    {"label": "Support RAG health", "url": "/rag/health"},
                ],
            },
        }
        resp = JSONResponse(payload)
        resp.headers["Cache-Control"] = "no-store"
        return resp

    @r.post("/api/chat")
    async def ui_chat(
        body: UIChatBody,
        request: Request,
        _t: str = Depends(require_service_ui),
        service: Any = Depends(get_service),
    ) -> JSONResponse:
        cfg = request.app.state.config
        wu = cfg.web_ui
        alm = cfg.anything_llm
        req_id = str(uuid.uuid4())
        t0 = time.perf_counter()
        ctx = _trace_ctx(request)
        user_text = body.message
        rs = (body.rag_source or wu.rag_source).strip()
        if rs not in ("support_rag", "anythingllm"):
            rs = "support_rag"

        top_k = int(body.top_k) if body.top_k is not None else int(wu.top_k)
        top_k = min(max(1, top_k), _SUPPORT_RAG_TOP_K_MAX)
        top_n = int(body.top_n) if body.top_n is not None else int(wu.anythingllm_top_n)
        top_n = min(max(1, top_n), _ANYTHINGLLM_TOP_N_MAX, int(alm.top_n))
        sth: float | None = body.score_threshold
        if sth is None and wu.anythingllm_score_threshold is not None:
            sth = float(wu.anythingllm_score_threshold)
        if sth is None:
            sth = float(alm.score_threshold)

        cms: Literal["llm_gateway", "anythingllm"] = (
            body.chat_model_source
            if body.chat_model_source is not None
            else wu.chat_model_source
        )
        if wu.anythingllm_models_source == "llm_gateway" and cms == "anythingllm":
            raise HTTPException(
                status_code=400,
                detail=_opt_b_blocks_chat_alm(),
            )

        rresp: RetrievalResponse | None = None
        final_user: str = user_text
        reply: str = ""
        comp_route = "n/a"
        rsrc_out: str = "none"
        lat_r: float | None = None
        lat_c: float | None = None
        meta_ex: dict[str, Any] = {
            "filters_applied": False,
            "retrieval_truncated": False,
            "request_id": req_id,
        }
        retrieval_count = 0
        t_total: float

        try:
            if not body.use_rag:
                if cms == "llm_gateway":
                    t_c0 = time.perf_counter()
                    reply = await service.chat_complete(
                        [{"role": "user", "content": final_user}],
                        max_tokens=2048,
                        temperature=0.2,
                        trace_ctx=ctx,
                    )
                    lat_c = (time.perf_counter() - t_c0) * 1000
                    comp_route = "llm_gateway"
                else:
                    slug = await asyncio.to_thread(
                        resolve_workspace_slug,
                        alm,
                        override=wu.anythingllm_workspace_slug_override or "",
                        configured=alm.workspace_slug or "",
                    )
                    t_c0 = time.perf_counter()
                    reply, alm_wmeta = await asyncio.to_thread(
                        workspace_chat,
                        alm,
                        slug=slug,
                        message=final_user,
                        mode=ALM_WORKSPACE_CHAT_MODE_AUGMENTED,
                    )
                    lat_c = (time.perf_counter() - t_c0) * 1000
                    comp_route = "anythingllm_native"
                    m = alm_wmeta.get("alm_chat_mode")
                    if m:
                        meta_ex["alm_chat_mode"] = str(m)
                rsrc_out = "none"
            elif rs == "support_rag":
                t_r0 = time.perf_counter()
                rreq = RetrievalRequest(
                    query=user_text,
                    top_k=top_k,
                    namespaces=list(_NS),
                )
                rresp, _ = await service.retrieve(
                    rreq, trace_ctx=ctx,
                )
                lat_r = (time.perf_counter() - t_r0) * 1000
                retrieval_count = len(rresp.chunks)
                final_user = _augmented_content(user_text, rresp)
                if cms == "llm_gateway":
                    t_c0 = time.perf_counter()
                    reply = await service.chat_complete(
                        [{"role": "user", "content": final_user}],
                        max_tokens=2048,
                        temperature=0.2,
                        trace_ctx=ctx,
                    )
                    lat_c = (time.perf_counter() - t_c0) * 1000
                    comp_route = "llm_gateway"
                else:
                    slug = await asyncio.to_thread(
                        resolve_workspace_slug,
                        alm,
                        override=wu.anythingllm_workspace_slug_override or "",
                        configured=alm.workspace_slug or "",
                    )
                    t_c0 = time.perf_counter()
                    reply, alm_wmeta = await asyncio.to_thread(
                        workspace_chat,
                        alm,
                        slug=slug,
                        message=final_user,
                        mode=ALM_WORKSPACE_CHAT_MODE_AUGMENTED,
                    )
                    lat_c = (time.perf_counter() - t_c0) * 1000
                    comp_route = "anythingllm_native"
                    m2 = alm_wmeta.get("alm_chat_mode")
                    if m2:
                        meta_ex["alm_chat_mode"] = str(m2)
                rsrc_out = "support_rag"
            else:
                slug = await asyncio.to_thread(
                    resolve_workspace_slug,
                    alm,
                    override=wu.anythingllm_workspace_slug_override or "",
                    configured=alm.workspace_slug or "",
                )
                vreq = RetrievalRequest(
                    query=user_text,
                    top_k=1,
                    namespaces=["kb"],
                )
                t_r0 = time.perf_counter()
                rresp = await asyncio.to_thread(
                    vector_search,
                    alm,
                    slug=slug,
                    query=user_text,
                    top_n=top_n,
                    score_threshold=sth,
                    req=vreq,
                )
                lat_r = (time.perf_counter() - t_r0) * 1000
                retrieval_count = len(rresp.chunks)
                fa = rresp.debug.get("filters_applied")
                if isinstance(fa, bool):
                    meta_ex["filters_applied"] = fa
                final_user = _augmented_content(user_text, rresp)
                if cms == "llm_gateway":
                    t_c0 = time.perf_counter()
                    reply = await service.chat_complete(
                        [{"role": "user", "content": final_user}],
                        max_tokens=2048,
                        temperature=0.2,
                        trace_ctx=ctx,
                    )
                    lat_c = (time.perf_counter() - t_c0) * 1000
                    comp_route = "llm_gateway"
                else:
                    t_c0 = time.perf_counter()
                    reply, alm_wmeta = await asyncio.to_thread(
                        workspace_chat,
                        alm,
                        slug=slug,
                        message=final_user,
                        mode=ALM_WORKSPACE_CHAT_MODE_AUGMENTED,
                    )
                    lat_c = (time.perf_counter() - t_c0) * 1000
                    comp_route = "anythingllm_native"
                    m = alm_wmeta.get("alm_chat_mode")
                    if m:
                        meta_ex["alm_chat_mode"] = str(m)
                rsrc_out = "anythingllm"
        except ValueError as e:
            t_total = (time.perf_counter() - t0) * 1000
            _log_ui_chat(
                request_id=req_id,
                rag_source=rs,
                completion_route="error",
                top_k=top_k if (body.use_rag and rs == "support_rag") else None,
                top_n=top_n if (body.use_rag and rs == "anythingllm") else None,
                score_threshold=sth if (body.use_rag and rs == "anythingllm") else None,
                latency_ms_total=t_total,
                latency_ms_retrieval=lat_r,
                latency_ms_completion=lat_c,
                retrieval_count=retrieval_count,
            )
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content={"detail": str(e)},
            )
        except httpx.HTTPError as e:
            t_total = (time.perf_counter() - t0) * 1000
            _log_ui_chat(
                request_id=req_id,
                rag_source=rs,
                completion_route="error",
                top_k=top_k if (body.use_rag and rs == "support_rag") else None,
                top_n=top_n if (body.use_rag and rs == "anythingllm") else None,
                score_threshold=sth if (body.use_rag and rs == "anythingllm") else None,
                latency_ms_total=t_total,
                latency_ms_retrieval=lat_r,
                latency_ms_completion=lat_c,
                retrieval_count=retrieval_count,
            )
            pl = _httpx_error_payload(e)
            if "detail" not in pl or not pl.get("detail"):
                pl["detail"] = alm_error_message(e)
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=pl,
            )
        except Exception as e:
            logger.exception("ui chat")
            t_total = (time.perf_counter() - t0) * 1000
            _log_ui_chat(
                request_id=req_id,
                rag_source=rs,
                completion_route="error",
                top_k=top_k if (body.use_rag and rs == "support_rag") else None,
                top_n=top_n if (body.use_rag and rs == "anythingllm") else None,
                score_threshold=sth if (body.use_rag and rs == "anythingllm") else None,
                latency_ms_total=t_total,
                latency_ms_retrieval=lat_r,
                latency_ms_completion=lat_c,
                retrieval_count=retrieval_count,
            )
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content={
                    "detail": str(e)[:2_000],
                    "http_status": None,
                    "body_snippet": "",
                },
            )

        t_total = (time.perf_counter() - t0) * 1000
        _log_ui_chat(
            request_id=req_id,
            rag_source=rsrc_out,
            completion_route=comp_route,
            top_k=top_k if (body.use_rag and rs == "support_rag") else None,
            top_n=top_n if (body.use_rag and rs == "anythingllm") else None,
            score_threshold=sth if (body.use_rag and rs == "anythingllm") else None,
            latency_ms_total=t_total,
            latency_ms_retrieval=lat_r,
            latency_ms_completion=lat_c,
            retrieval_count=retrieval_count,
        )

        out: dict[str, Any] = {
            "reply": reply,
            "completion_route": comp_route,
            "rag_source": rsrc_out,
            "meta": meta_ex,
        }
        if body.include_retrieval and rresp is not None:
            cap_d, tr = _cap_retrieval_payload(
                rresp,
                char_cap=wu.retrieval_chunk_char_cap,
                max_chunks=_RETRIEVAL_CHUNKS_DEFAULT,
            )
            out["retrieval"] = cap_d
            meta_ex["retrieval_truncated"] = tr
        return JSONResponse(out)

    @r.post("/api/anythingllm/verify-option-b")
    async def verify_option_b(
        request: Request,
        _a: str = Depends(require_admin_ui),
    ) -> JSONResponse:
        cfg = request.app.state.config
        lg = cfg.llm_gateway
        alm = cfg.anything_llm
        gw_display = _public_base_url(lg.base_url)
        lit_ok: bool | None = None
        try:
            lit_ok = await asyncio.to_thread(
                litellm_gateway_reachable,
                lg.base_url,
                api_key=lg.api_key,
            )
        except Exception:
            lit_ok = None
        lit_msg = _verify_gateway_user_message(lit_ok, gw_display)

        raw, alm_err = await asyncio.to_thread(try_get_system_settings, alm)
        alm_hosts: list[str] = []
        alm_provider_seen: str | None = None
        anythingllm_ok = False
        if raw is not None:
            anythingllm_ok = True
            alm_provider_seen, _mode, alm_hosts = summarize_alm_system_for_ui(raw)
            if alm_provider_seen:
                alm_msg = f"AnythingLLM: settings OK — {alm_provider_seen}."
            else:
                alm_msg = "AnythingLLM: settings OK — no LLM/embedder labels in API response (still read URLs if present)."
        else:
            err = (alm_err or "unknown error").strip()
            alm_msg = (
                "AnythingLLM: cannot read settings — "
                f"{err} "
                "Check anything_llm.base_url, RAG_ANYTHING_LLM__API_KEY, and that Desktop is running."
            )

        host_match: bool | None
        if not anythingllm_ok:
            host_match = None
            host_msg = (
                "Gateway vs Desktop: skipped — fix AnythingLLM /api/v1/system access, then run verify again."
            )
        elif not (lg.base_url or "").strip():
            host_match = None
            host_msg = "Gateway vs Desktop: skipped — llm_gateway.base_url is empty in this service config."
        elif not alm_hosts:
            host_match = False
            host_msg = (
                "Gateway vs Desktop: no http(s) URLs in AnythingLLM settings to compare. "
                "In Desktop, set LLM and embedder base URLs to this project’s llm_gateway (LiteLLM proxy)."
            )
        else:
            ok = option_b_host_match(lg.base_url, alm_hosts)
            host_match = ok
            g_raw = (lg.base_url or "").strip()
            try:
                want = (
                    urlparse(g_raw if "://" in g_raw else f"http://{g_raw}").hostname or ""
                ).lower()
            except Exception:
                want = ""
            hosts_txt = ", ".join(alm_hosts)
            if ok:
                host_msg = (
                    f"Gateway vs Desktop: match — gateway host «{want}» appears in Desktop settings ({hosts_txt})."
                )
            else:
                host_msg = (
                    f"Gateway vs Desktop: mismatch — config gateway host «{want}»; "
                    f"Desktop URL hosts: {hosts_txt}. Point Desktop at the same host as llm_gateway.base_url."
                )

        return JSONResponse(
            {
                "litellm_reachable": lit_ok,
                "litellm_message": lit_msg,
                "anythingllm_ok": anythingllm_ok,
                "anythingllm_message": alm_msg,
                "alm_provider_seen": alm_provider_seen,
                "host_match": host_match,
                "host_match_message": host_msg,
                "verified_at": datetime.now(UTC).isoformat(),
            }
        )

    @r.post("/api/ingest-folder")
    async def ui_ingest(
        body: UIFolderIngestBody,
        request: Request,
        _a: str = Depends(require_admin_ui),
        service: Any = Depends(get_service),
    ) -> JSONResponse:
        # Basic path hardening: no control chars
        p = body.path
        if re.search(r"[\x00-\x1f\x7f]", p):
            raise HTTPException(400, "path contains control characters")
        try:
            root = Path(p).expanduser()
        except (OSError, ValueError) as e:
            raise HTTPException(400, f"invalid path: {e}") from e
        try:
            out = await index_local_folder_inprocess(
                service,
                root,
                body.namespace,
                include_patterns=_DEFAULT_PATTERNS,
                batch_size=_DEFAULT_BATCH,
                trace_ctx=_trace_ctx(request),
            )
        except Exception as e:
            d = str(e)[:1_500]
            if isinstance(e, httpx.HTTPStatusError) and e.response is not None:
                tail = (e.response.text or "")[:1_500]
                if tail:
                    d = f"{d}\n--- gateway body ---\n{tail}"
            logger.exception("ui ingest")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=d[:2_000],
            ) from e
        err = out.get("error")
        if err:
            raise HTTPException(400, str(err) if isinstance(err, str) else str(err))
        return JSONResponse(
            {
                "indexed": int(out.get("indexed", 0) or 0),
                "n_skip": int(out.get("n_skip", 0) or 0),
                "n_read_err": int(out.get("n_read_err", 0) or 0),
                "ok": bool(out.get("ok", True)),
            }
        )

    @r.post("/api/ingest-folder-anythingllm")
    async def ui_ingest_anythingllm(
        body: UIAnythingLlmIngestBody,
        request: Request,
        _a: str = Depends(require_admin_ui),
    ) -> JSONResponse:
        p = body.path
        if re.search(r"[\x00-\x1f\x7f]", p):
            raise HTTPException(400, "path contains control characters")
        try:
            root = Path(p).expanduser()
        except (OSError, ValueError) as e:
            raise HTTPException(400, f"invalid path: {e}") from e
        cfg = request.app.state.config
        wu = cfg.web_ui
        st_path = wu.anythingllm_ingest_state_path
        prefix = (body.server_folder_name or wu.alm_ingest_folder_name or "").strip()

        def _ingest_sync() -> dict[str, Any]:
            if not root.is_dir():
                return {"ok": False, "error": f"not a directory: {root}"}
            docs, n_skip, n_read_err, _msg = collect_docs(root, _DEFAULT_PATTERNS)
            n_ok = 0
            n_skip_alm = 0
            n_err = 0
            err_list: list[str] = []
            for d in docs:
                meta = d.get("metadata") if isinstance(d.get("metadata"), dict) else {}
                rel = str(meta.get("file_path", d.get("id", "")))
                logical_key = rel or str(d.get("id", ""))
                text = str(d.get("text", ""))
                title = f"{prefix}/{rel}" if prefix else rel
                if not text.strip():
                    continue
                try:
                    r = ingest_raw_text_idempotent(
                        cfg,
                        logical_key=logical_key,
                        text=text,
                        document_title=title,
                        state_path=st_path,
                    )
                except httpx.HTTPError as e:
                    n_err += 1
                    err_list.append(f"{rel}: {alm_error_message(e)}")
                    if len(err_list) > 30:
                        break
                    continue
                if r.get("skipped"):
                    n_skip_alm += 1
                else:
                    n_ok += 1
            return {
                "ok": n_err == 0,
                "ingested": n_ok,
                "skipped": n_skip_alm,
                "replaced": 0,
                "n_skip_fs": n_skip,
                "n_read_err": n_read_err,
                "errors": err_list,
            }

        out = await asyncio.to_thread(_ingest_sync)
        if out.get("error"):
            raise HTTPException(400, str(out["error"]))
        # Persist slug + folder path so chat vector-search uses the same workspace as ingest, and
        # the AnythingLLM ingest form reloads like the Qdrant path field.
        cpath = getattr(request.app.state, "config_path", None)
        if cpath:
            pp = Path(cpath)
            if pp.is_file():
                cur = dict(cfg.web_ui.model_dump())
                cur["alm_ingest_folder_path"] = str(root)
                try:
                    new_state = WebUiState(**cur)
                    merge_web_ui_into_config_file(cpath, new_state.model_dump())
                    cfg.web_ui = new_state
                except Exception as e:
                    logger.warning("persist web_ui after ALM ingest: %s", e)
        return JSONResponse(out)

    return r


def root_page_router() -> APIRouter:
    """Redirect / to /ui/ for a friendlier bookmarket."""
    a = APIRouter()

    @a.get("/", include_in_schema=False)
    async def _root() -> Any:
        from fastapi.responses import RedirectResponse

        return RedirectResponse("/ui/", status_code=302)

    return a


def is_web_ui_enabled() -> bool:
    v = os.environ.get("RAG_ENABLE_WEB_UI", "1").lower()
    return v in ("1", "true", "yes", "on")
