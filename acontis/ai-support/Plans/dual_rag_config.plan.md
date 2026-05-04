---
name: Dual-RAG config and client
overview: AppConfig + WebUiState for dual-RAG, `anythingllm_client.py` (vector-search, workspace_chat, ingest + idempotency), secrets redaction, YAML samples, and config-focused limitations.
todos:
  - id: config-models
    content: "AppConfig anything_llm + WebUiState (anythingllm_models_source, anythingllm_completion, retrieval_chunk_char_cap, top_k/top_n bounds); FIELD_SETTINGS_META + YAML; _redact_for_browser (§7a)"
    status: pending
  - id: alm-client
    content: "anythingllm_client.py: vector_search (filters_applied note), workspace_chat + mode constant, ingest + idempotency map; error helpers; unit tests"
    status: pending
isProject: false
---

# Dual-RAG: configuration and AnythingLLM client

## Execution boundary (manual handoff)

- **In scope for this file only:** the sections below (configuration, `anythingllm_client` library, secrets **§7a**). **Stop when they are done** (or blocked).
- **Do not automatically continue** to [dual_rag_ui.plan.md](dual_rag_ui.plan.md) or [dual_rag_e2e.plan.md](dual_rag_e2e.plan.md). The next plan is **not** a follow-up step in the same agent run. The user starts a **new** chat/agent and explicitly points it at the next plan (or re-opens it) when they are ready.
- **The index below is for reference and navigation only**, not an instruction to implement those documents in this session.

## Index (related plans — not auto-run)

- **[`dual_rag_ui.plan.md`](dual_rag_ui.plan.md)** — `UIChatBody`, `ui_chat` branching, `GET /ui/api/chat-context`, `POST` verify + ingest routes, `web_routes` HTML/JS, operator UX, error display. **Run in a separate session when the user requests it.**
- **[`dual_rag_e2e.plan.md`](dual_rag_e2e.plan.md)** — E2E PowerShell (AnythingLLM Desktop, `Wait-ForPort`), runbook anchors, tests, full limitations and non-goals. **Run in a separate session when the user requests it.**

---

## 1. Configuration model

- Add an optional **`anything_llm`** section to [`../support_rag/config.py`](../support_rag/config.py) `AppConfig`, e.g.:
  - `base_url` (default `http://127.0.0.1:3001`)
  - `api_key` (optional; prefer reading from env via existing `RAG_` pattern, e.g. `RAG_ANYTHING_LLM__API_KEY` or a dedicated env name in `Field(validation_alias=...)`)
  - `workspace_slug` (string; the workspace to query for `vector-search`)
  - `score_threshold` / `top_n` caps aligned with AnythingLLM request body
- Extend [`WebUiState`](../support_rag/config.py) for **UI-only** persistence:
  - **`anythingllm_models_source`**: `Literal["alm_desktop", "litellm_gateway"]` (default **`alm_desktop`**) — Option A vs B for how **AnythingLLM itself** obtains LLM + embedding models.
  - **`anythingllm_completion`**: `Literal["gateway", "anythingllm_native"]` (default **`gateway`**) — when using AnythingLLM retrieval, whether `ui_chat` uses `chat_complete` or AnythingLLM workspace chat (see UI plan for UX).
  - Plus: `show_retrieval_context`, `top_k`, `anythingllm_top_n`, `anythingllm_score_threshold`, optional workspace slug override, AnythingLLM ingest block fields, `retrieval_chunk_char_cap`.
- Update [`../config.example.yaml`](../config.example.yaml) and [`../config.e2e.example.yaml`](../config.e2e.example.yaml) (if present) with commented `anything_llm` defaults.
- Extend [`WebUiPatch`](../support_rag/web_routes.py) and [`FIELD_SETTINGS_META`](../support_rag/config.py) for new `web_ui` fields.

**Security:** Never return the AnythingLLM API key to the browser; keep it server-side in config/env only (same pattern as LLM gateway key). Full policy: **§7a** below; runbook and operator copy: [dual_rag_e2e.plan.md](dual_rag_e2e.plan.md#5-documentation) and [§7](dual_rag_e2e.plan.md#7-limitations-and-explicit-non-goals).

---

## 2. AnythingLLM client module (library)

[`../support_rag/anythingllm_client.py`](../support_rag/anythingllm_client.py):

- `vector_search(...)` — `POST {base}/api/v1/workspace/{slug}/vector-search`. **Note:** AnythingLLM does **not** honor `RetrievalRequest.filters`. MVP: ignore + WARN; set `filters_applied: false` in synthetic `RetrievalResponse.debug`.
- **`workspace_chat(...)`** — `httpx` to AnythingLLM’s **non-streaming** workspace chat (path/body from live **`/api/docs`**, e.g. `POST /api/v1/workspace/{slug}/chat`). Pass the same augmented user string as gateway mode. **Mode decision (avoid double retrieval):** prefer a mode that suppresses server-side re-retrieval; wire constant; **fallback** document honestly ([dual_rag_e2e.plan.md](dual_rag_e2e.plan.md#7-limitations-and-explicit-non-goals)). Return `meta.alm_chat_mode` for the UI path.
- **Ingest helpers** — `raw-text` / `document/upload` + `update-embeddings`; idempotency map and delete-old-doc on change (see UI plan item “Ingest to AnythingLLM” for `var/anythingllm_ingest_state.json` and operator docs).
- Map `vector_search` `results[]` → synthetic [`RetrievalResponse`](../support_rag/schemas.py).

**Shared error helpers** (consumed by UI routes): normalize ALM/LiteLLM errors with messages used by the UI plan’s error table.

---

## 7a. Secrets policy (single source of truth)

The following **never** appear in browser-bound JSON from any UI route, nor in front-end JS:

- AnythingLLM API key, LiteLLM master key, provider keys from ALM, any `Authorization` value, `RAG_*__API_KEY`, etc.

**Enforcement:** `_redact_for_browser(payload)` on UI-bound responses; assert no configured secret substrings; unit-test with synthetic values.

---

## Config-side limitations (AnythingLLM retrieval)

- **Metadata `filters` ignored** for `vector-search` (WARN + `meta.filters_applied=false`). Full list: [dual_rag_e2e.plan.md](dual_rag_e2e.plan.md#7-limitations-and-explicit-non-goals).
- **Hybrid + rerank** not available through AnythingLLM’s API; **single `workspace_slug`** for ALM (vs joint namespaces in Support RAG).

## Implementation order (this plan)

1. `AppConfig` + `WebUiState` + YAML + `WebUiPatch` + `_redact_for_browser`.  
2. `anythingllm_client.py` + error helpers + unit tests.  

**End of this plan.** Do not open or implement [dual_rag_ui.plan.md](dual_rag_ui.plan.md) or [dual_rag_e2e.plan.md](dual_rag_e2e.plan.md) unless the user explicitly starts a new run for one of them.

**If and when a later run targets the UI plan:** the config/client work in this file should be merged or in place; that handoff is **user-controlled**, not automatic.
