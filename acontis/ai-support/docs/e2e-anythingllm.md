# AnythingLLM and E2E (Windows)

This runbook supports **dual-RAG** flows: Support RAG (Qdrant + hybrid) and **AnythingLLM** `vector-search` / workspace chat, driven from the same **Web UI** (`/ui/`) as the REST API. Startup order: **Ollama → Qdrant → LiteLLM → AnythingLLM → support_rag** (see `tests/e2e/scripts/Start-E2E-Stack.ps1`).

---

<h2 id="ports">Which port is which (default E2E)</h2>

| Port | Service | What to open |
| --- | --- | --- |
| **8080** | **support_rag** (this project) | Web UI: `http://127.0.0.1:8080/ui/` — chat, local Qdrant ingest, “Ingest to AnythingLLM” button. |
| **3001** | **AnythingLLM Desktop HTTP API** | Used by `support_rag` as `anything_llm.base_url` for `/api/v1/...` calls. **Not** the Support RAG site. On **Desktop**, you usually **cannot** use an external browser on `http://127.0.0.1:3001/settings/...` to get the in-app settings UI; that often returns **Not Found**. Configure API keys **inside the AnythingLLM application window** (see below). API docs: `http://127.0.0.1:3001/api/docs` (if exposed). |
| **4000** | LiteLLM proxy | Gateway for models/embeddings. |
| **6333** | Qdrant | Vector DB for Support RAG. |
| **11434** | Ollama | Local models. |

`Start-E2E-Stack.ps1` defaults: `-RagPort 8080`, `-AnythingLlmPort 3001`, `-LiteLLmPort 4000`, etc.

---

<h2 id="one-time-setup">One-time setup</h2>

1. Install [AnythingLLM Desktop for Windows](https://docs.useanything.com/installation-desktop/windows).
2. Default install path: `%LOCALAPPDATA%\Programs\AnythingLLM\AnythingLLM.exe` (e.g. `C:\Users\<you>\AppData\Local\Programs\AnythingLLM\AnythingLLM.exe`).
3. If the app lives elsewhere, set either:
   - Environment variable `ANYTHINGLLM_DESKTOP_EXE` to the full path of `AnythingLLM.exe`, or
   - Parameter `-AnythingLlmExePath` on `Start-E2E-Stack.ps1`.
4. Repository config: set `RAG_CONFIG=config.e2e.yaml` (or your file) and define `anything_llm` + tokens. The E2E script sets `RAG_ANYTHING_LLM__BASE_URL` to `http://127.0.0.1:<AnythingLlmPort>` so the port matches `-AnythingLlmPort` (default **3001**).

Non-default ports must match **`anything_llm.base_url`** in YAML (or the `RAG_ANYTHING_LLM__BASE_URL` override) and the stack scripts.

---

<h2 id="workspace-and-key">Workspace and API key</h2>

- Create or open a **workspace** in AnythingLLM Desktop. Note the **workspace slug** (settings / URL as documented in the app).
- **Developer API keys** live only in the **AnythingLLM app** (not on the Support RAG port). Open the **gear / Instanzeinstellungen** sidebar and find **Entwickler-API** (German UI) or **API keys** (English) — the route is `/settings/api-keys` inside the app, not a separate website. Use **Neuen API-Schlüssel generieren** / **Generate**, then set **`RAG_ANYTHING_LLM__API_KEY`** in `.env` (preferred) or YAML; it is **never** sent to the browser (see [Secrets policy](#secrets-policy)). If that menu entry is missing, scroll the settings list or update AnythingLLM Desktop.

Map **`workspace_slug`** in `config.e2e.yaml` under `anything_llm` to that workspace, or use the Web UI **AnythingLLM workspace** control under **Model source (Option A / B)** on `/ui/`:

- **Automatic** clears `web_ui.anythingllm_workspace_slug_override` so resolution follows **`anything_llm.workspace_slug`** when set (non-empty and not the legacy placeholder `default`), then the **first workspace** returned by AnythingLLM’s `GET /api/v1/workspaces`.
- **Override workspace** sets the same override field to a slug chosen from the workspace list and/or typed as a **custom slug**.

The read-only line shows the YAML `anything_llm.workspace_slug` from the active config; the status line shows the **effective** slug and whether it came from override, config, or the first listed workspace. **Ingest to AnythingLLM** uses that same effective workspace (there is no separate per-ingest slug field).

---

<h2 id="option-a-alm-desktop-only">Option A — models only in Desktop</h2>

**Option A** (`alm_desktop`): configure **LLM and embedding models** only inside AnythingLLM Desktop. LiteLLM may still be used for Support RAG’s own `chat_complete` path when you choose **gateway** completion (see [Completion vs Option A/B](#completion-orthogonality)).

The Web UI’s A/B section is **guidance** unless you use **Verify Option B**; model routing is defined in the Desktop app.

---

<h2 id="option-b-via-litellm-gateway">Option B — LLM and embedder via LiteLLM gateway</h2>

**Option B** (`llm_gateway` in `web_ui`, legacy YAML `litellm_gateway` is coerced on load): in AnythingLLM, point the **LLM and embedder** at this project’s gateway — same `llm_gateway.base_url` (and key, if your proxy requires it) as in `config` / `.env` (`RAG_LLM_GATEWAY__BASE_URL`, `RAG_LLM_GATEWAY__API_KEY`).

This keeps a single local gateway for both Support RAG and AnythingLLM provider calls when configured in the Desktop UI.

Use [Verify Option B](#option-b-verify) in the Web UI to best-effort check reachability; it does not read third-party API keys from AnythingLLM.

---

<h2 id="option-b-verify">Verify Option B and troubleshooting</h2>

- In `/ui/`, with **Option B** selected, use **Verify Option B** (admin). It checks LiteLLM reachability and summarizes AnythingLLM system settings if the API is available.
- **Host match** information is best-effort: compare the LiteLLM base URL in config with the hosts AnythingLLM reports so that gateway URLs are not accidentally pointed at the wrong machine.
- If verification fails, confirm AnythingLLM Desktop is running, **`anything_llm.base_url`** matches the API port, and **`RAG_ANYTHING_LLM__API_KEY`** is valid (403/401 in logs).

---

<h2 id="completion-orthogonality">Completion vs Option A and B</h2>

- **Option A / B** only describe how **AnythingLLM** obtains models (Desktop vs via LiteLLM). They are **orthogonal** to **`anythingllm_completion`** in the Web UI.
- When **RAG source = AnythingLLM** and **Use RAG** is on:
  - **Gateway** (`gateway`): completion uses Support Rag → `chat_complete` → LiteLLM, after AnythingLLM `vector-search` has augmented the prompt.
  - **Native** (`anythingllm_native`): completion uses AnythingLLM **workspace chat** (not the LiteLLM gateway for that call).
- **When `use_rag` is off**, the UI always uses **gateway** `chat_complete` (AnythingLLM retrieval is skipped); the native/gateway RAG setting does not apply.
- **Double-retrieval risk:** in **native** mode, the workspace may run its own RAG in addition to the already-augmented message — see limitations in the dual-RAG plan; there is no streaming native chat in MVP.

---

<h2 id="start-anythingllm">Script launch and <code>-SkipAnythingLlm</code></h2>

- `Start-E2E-Stack.ps1` starts AnythingLLM Desktop if **TCP on `-AnythingLlmPort`** (default 3001) is closed: resolves `AnythingLLM.exe` ([One-time setup](#one-time-setup)), then **`Wait-ForPort`** with **`-AnythingLlmStartTimeoutSec`** (default **90**; first cold start may need 90–120s).
- Use **`-SkipAnythingLlm`** when you already have Desktop running and must not spawn or kill the app (e.g. debugging a long session). `Stop-E2E-Stack.ps1` supports **`-SkipAnythingLlm`** so the AnythingLLM process is left running while the rest of the stack stops.
- Stopping: **`Stop-E2E-Stack.ps1`** runs **`Get-Process -Name "AnythingLLM" | Stop-Process -Force`** (unless skip). That stops the **HTTP API** for Desktop as well, since it shares the Electron process.

---

<h2 id="litellm-key">LiteLLM key</h2>

- If the LiteLLM proxy requires a key, set **`RAG_LLM_GATEWAY__API_KEY`** in `.env` or environment. The Web UI and JSON responses do **not** echo this value (see [Secrets policy](#secrets-policy)).

---

<h2 id="secrets-policy">Secrets policy (operator-facing)</h2>

- **Do not** paste API keys into the Web UI. Use `.env` / OS environment: **`RAG_SERVICE_TOKEN`**, **`RAG_ADMIN_TOKEN`**, **`RAG_LLM_GATEWAY__API_KEY`**, **`RAG_ANYTHING_LLM__API_KEY`**, etc.
- Enforcement and redaction of browser-bound JSON are defined in the product config plan (single source of truth for “never leak secrets in UI responses”).

---

## Limitations (short)

- **Metadata filters** are ignored for AnythingLLM `vector-search` (logged; `meta.filters_applied=false`).
- **No hybrid + rerank** in AnythingLLM’s `vector-search` API.
- **One `workspace_slug`** in AnythingLLM (not joint `kb` + `tickets` in one call).
- **ALM ingest** idempotency uses a local map file; delete the map to force full re-upload.
- **Docker** for AnythingLLM is not used in this E2E path.

For full detail, see `Plans/dual_rag_e2e.plan.md` and `Plans/dual_rag_config.plan.md` in the repository.

---

## See also

- `docs/runbook-allow-remote-false-e2e.md` — broader local stack.
- `tests/e2e/scripts/Start-E2E-Stack.ps1` / `Stop-E2E-Stack.ps1` — process order and ports.
