---
name: Dual-RAG E2E and documentation
overview: PowerShell E2E stack (AnythingLLM Desktop, `Wait-ForPort`, dual-RAG `/ui` probe), runbook with stable anchors, tests, and shared limitations for operators.
todos:
  - id: e2e-ps1
    content: "Start-E2E-Stack: AnythingLLM.exe, -SkipAnythingLLM, Wait-ForPort -TimeoutSec, /ui/ readiness, summary line; Stop: Get-Process AnythingLLM | Stop-Process -Force"
    status: pending
  - id: docs
    content: "Runbook docs/e2e-anythingllm.md (stable anchors for UI links)"
    status: pending
isProject: false
---

# Dual-RAG: E2E scripts, runbook, tests

## Execution boundary (manual handoff)

- **Start this plan only** when the user (or a new agent session) **explicitly** targets this file. It is **not** a mandatory next step after the config or UI plan in the same run.
- **In scope:** E2E PowerShell, runbook, tests, limitations in this file. **Stop when done.** There is no “plan 4” in this set.
- **Prerequisite (typical):** config + UI changes land first (see the other two plans); the user may still run **only** this file for doc/script-only updates — do not pull in UI code unless the user asked.

**Related (reference):** [dual_rag_config.plan.md](dual_rag_config.plan.md) · [dual_rag_ui.plan.md](dual_rag_ui.plan.md) — for context only, not to be implemented here unless the user’s instruction includes them.

---

## 3b. E2E stack: explicit dual-RAG web UI (same process)

The browser UI is **not** a separate process. It is served by the same Uvicorn app as the RAG API (`support_rag.app:app` → [`../support_rag/web_routes.py`](../support_rag/web_routes.py)), gated by `RAG_ENABLE_WEB_UI`.

**Start ([`../tests/e2e/scripts/Start-E2E-Stack.ps1`](../tests/e2e/scripts/Start-E2E-Stack.ps1) + [`../tests/e2e/scripts/Start-RAG.ps1`](../tests/e2e/scripts/Start-RAG.ps1))**

- Stack already “starts” the web UI when `support_rag` starts; no second `Start-Process` for HTTP.
- Set `RAG_ENABLE_WEB_UI=1` in the E2E RAG process environment.
- After `Wait-ForPort` / successful `/rag/health`, **readiness** for HTML: `GET http://127.0.0.1:<RagPort>/ui/` (or `/ui` redirect), expect 200/302.
- Print a **summary line**, e.g. `Web UI (dual-RAG chat): http://127.0.0.1:<RagPort>/ui/`.

**Stop ([`../tests/e2e/scripts/Stop-E2E-Stack.ps1`](../tests/e2e/scripts/Stop-E2E-Stack.ps1) + [`../tests/e2e/scripts/Stop-RAG.ps1`](../tests/e2e/scripts/Stop-RAG.ps1))**

- Stopping **`$RagPort`** stops REST **and** `/ui` (one OS process). Messaging: e.g. “Stopping support_rag (REST + browser UI on same port).”

**Optional follow-up:** separate Uvicorn for UI would need its own port — **out of scope**.

---

## 4. E2E scripts — AnythingLLM (no Docker)

**Constraint:** no Docker for AnythingLLM. **Goal:** normal E2E flow does not require manual AnythingLLM start/stop. Extend [`Start-E2E-Stack.ps1`](../tests/e2e/scripts/Start-E2E-Stack.ps1) and [`Stop-E2E-Stack.ps1`](../tests/e2e/scripts/Stop-E2E-Stack.ps1).

**Allows vs requires**

- **One-time:** install [AnythingLLM Desktop](https://docs.useanything.com/installation-desktop/windows) or discoverable EXE. No daily manual start/stop.
- **Each run:** if port not listening, `Start-Process` Desktop; on stop, kill by process name (best for Electron).

**Windows (verified pattern)**

- Electron process name: **`AnythingLLM`** (multiple children, same name).
- **Default path:** `"$env:LOCALAPPDATA\Programs\AnythingLLM\AnythingLLM.exe"`. Start: `Start-Process` that path.
- **Readiness:** poll **port 3001** (or `$AnythingLlmPort`) until open; ~1s interval, **min ~30s** budget, **90–120s** for cold start.
- **Stop:** `Get-Process -Name "AnythingLLM" -ErrorAction SilentlyContinue | Stop-Process -Force` (Electron often needs `-Force`). Optionally confirm port closed.
- Port must align with `anything_llm.base_url` in config; script parameter for non-default.

**Executable resolution (fail with install instructions if missing)**

1. Param `-AnythingLlmExePath` (or similar).  
2. Env e.g. `ANYTHINGLLM_DESKTOP_EXE` (runbook + `.env.example`).  
3. Default `LOCALAPPDATA\Programs\…\AnythingLLM.exe` if `Test-Path`.  
4. Else throw.

**Start** (inline in `Start-E2E-Stack.ps1` or optional `Start-AnythingLLM.ps1`):

- Params: `[int]$AnythingLlmPort` (default 3001), exe override, `[switch]$SkipAnythingLLM`, `[int]$AnythingLlmStartTimeoutSec` (default ≥30, document 90+ for first boot).  
- If `Test-TcpOpen` on port → log “already running”.  
- Else `Start-Process` resolved exe → poll port until open or timeout. **Extend** [`../tests/e2e/scripts/E2E-Stack-Helpers.ps1`](../tests/e2e/scripts/E2E-Stack-Helpers.ps1) `Wait-ForPort` with **`-TimeoutSec`**; else inline `Test-NetConnection` loop.  
- Optional: HTTP `GET` `/api/v1/system` after TCP (same probe as `alm_provider_summary`).  
- Print: `AnythingLLM API: http://127.0.0.1:<port>/` and pointer to workspace + API key in app.

**Stop** (`Stop-E2E-Stack.ps1`):

- Params: `$AnythingLlmPort`, `[switch]$SkipAnythingLLM`.  
- **Order (example):** after `Stop-RAG` and LiteLLM, stop AnythingLLM by **process name**, then Qdrant, Ollama (match repo’s actual order if different).  
- Runbook: `-SkipAnythingLlm` when Desktop must stay up; process-name stop still works if port was customized.

---

## 5. Documentation

- Add or extend: e.g. [`../docs/e2e-anythingllm.md`](../docs/e2e-anythingllm.md) (or section in `runbook-allow-remote-false-e2e`). **Stable anchor IDs** (UI `chat-context` links):

| Anchor | Content |
|--------|---------|
| `#one-time-setup` | Install; `%LOCALAPPDATA%\…\AnythingLLM.exe`; `ANYTHINGLLM_DESKTOP_EXE` if non-default. |
| `#workspace-and-key` | Workspace slug, API key in AnythingLLM. |
| `#option-a-alm-desktop-only` | Option A — models only in Desktop. |
| `#option-b-via-litellm-gateway` | Option B — LLM + embedder → `llm_gateway.base_url` + key. |
| `#option-b-verify` | Verify Option B behavior, troubleshooting, host match. |
| `#completion-orthogonality` | A/B vs `anythingllm_completion` (gateway vs native). |
| `#start-anythingllm` | Script launch, `-SkipAnythingLLM`. |
| `#litellm-key` | Key source; not echoed in UI. |
| `#secrets-policy` | Operator-facing; enforcement in [dual_rag_config.plan.md §7a](dual_rag_config.plan.md#7a-secrets-policy-single-source-of-truth). |

- Repo: `RAG_CONFIG` e2e yaml `anything_llm` + key env. **Startup order:** Ollama → Qdrant → LiteLLM → **AnythingLLM** (script) → `support_rag`.

---

## 6. Tests (lightweight)

- **Unit tests:** AnythingLLM JSON → `RetrievalResponse`; `ui_chat` response serialization with `include_retrieval` and caps.  
- **Optional:** integration if AnythingLLM absent → skip. Optional Playwright: [`../tests/e2e/scripts/e2e_web_ui_ingest_playwright.py`](../tests/e2e/scripts/e2e_web_ui_ingest_playwright.py) pattern.

---

## 7. Limitations and explicit non-goals

**Limitations (tooltips + runbook + [dual_rag_config.plan.md](dual_rag_config.plan.md) where noted):**

- **Metadata filters ignored** when `rag_source=anythingllm` — WARN, `meta.filters_applied=false`.  
- **No hybrid + rerank** in AnythingLLM `vector-search`.  
- **One ALM `workspace_slug`** — not joint `kb` + `tickets`.  
- **Native completion may double-retrieve** if no “no RAG” / completion-only mode — document at `#completion-orthogonality`.  
- **ALM ingest** idempotency: local map file; delete map → full re-ingest.  
- **Verify Option B** is best-effort (no secret keys read from ALM; host match informational).

**Non-goals:** Docker for AnythingLLM; auto-mutate ALM provider files from `support_rag` (spike only); **streaming** native chat (MVP non-streaming).

**Secrets in UI / responses — enforcement:** [dual_rag_config.plan.md §7a](dual_rag_config.plan.md#7a-secrets-policy-single-source-of-truth).

## Implementation order (this plan)

7. E2E script changes; runbook with anchors; tests; keep limitations aligned with the other two plans (by reading them if needed, **not** by re-implementing them in this run unless requested).

**End of the dual-RAG plan set** — there is no further plan file to continue to automatically.
