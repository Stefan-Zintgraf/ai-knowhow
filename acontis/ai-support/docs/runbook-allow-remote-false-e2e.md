# Runbook: §2.8(5) local-only E2E (LiteLLM → Ollama → support_rag)

This runbook matches `spec-mvp1-allow-remote-false-acceptance.md` and `config.e2e.example.yaml`.

**Intended environment:** **Everything on your machine** — **no Docker** for this flow. You run **Ollama**, **LiteLLM** (Python/`pip`), **Qdrant** (see below), and **support_rag** (uvicorn) as local processes. **Default `127.0.0.1` ports:** LiteLLM **4000**, **support_rag** **8080**, Qdrant **6333**.

## 1. Stack (what talks to what)

```text
support_rag  --OpenAI API shape-->  LiteLLM  :4000  --Ollama API-->  Ollama  :11434
      |
      +-------------------- Qdrant :6333 (vectors) ----
```

- **`support_rag`** only calls **`llm_gateway.base_url`** (LiteLLM at port **4000**). It does **not** call Ollama’s API directly.
- **Local-only policy:** the LiteLLM config must list **only** Ollama-backed models (see `docs/litellm-ollama-e2e.example.yaml`) — no cloud API keys in that file.
- **FR-23** `allow_remote` in `support_prd.md` is enforced **at the gateway**; for this runbook, “no cloud” means **only** Ollama routes in that LiteLLM file.

## 2. Prereqs

| Component | What to do |
|----------|------------|
| **Python** | 3.11 or 3.12 (see project `README.md`) |
| **Ollama** | Install from [ollama.com](https://ollama.com); `ollama serve` → `http://127.0.0.1:11434` |
| **Models** | `ollama pull all-minilm` and `ollama pull llama3.2:1b` |
| **Qdrant** | **No Docker in this runbook** — use a [Qdrant release binary](https://github.com/qdrant/qdrant/releases) and start it so **`http://127.0.0.1:6333`** answers, *or* install Qdrant by another non-Docker method you prefer. The RAG app only needs a reachable `qdrant.url`. |
| **LiteLLM** | Install with **pip** (see §3) — **not** a Docker image for this guide. |

Check embedding size (must match `qdrant.vector_size: 384` in the E2E config):

```bash
ollama show all-minilm
```

## 2.1 What is `X-Slot`? (optional — you can keep it simple)

`support_rag` sends an HTTP **header** on gateway calls, e.g. `X-Slot: embedding` for embeddings and `X-Slot: retrieval_llm` for chat. That matches **R-15 / R-16** in the PRD.

**Simplest path for you:** you do **not** need to configure LiteLLM to *route by* that header. The example `docs/litellm-ollama-e2e.example.yaml` routes by the JSON **`model`** field the client already sends: **`embedding`** and **`retrieval`**. Those names map to the Ollama models. **Ignore `X-Slot` on the LiteLLM side** unless you later add a custom plugin.

## 3. Install and start LiteLLM (local, latest)

1. In a venv (recommended):

   ```bash
   py -3.12 -m venv .venv-e2e
   .\.venv-e2e\Scripts\activate
   py -3.12 -m pip install -U "litellm[proxy]"
   ```

   On Linux/macOS: `source .venv-e2e/bin/activate` instead of `activate`.

2. Copy and edit the example:

   ```bash
   cp docs/litellm-ollama-e2e.example.yaml litellm-e2e.local.yaml
   ```

   Keep **`model_list`** pointing only to `http://127.0.0.1:11434` and **no** cloud `api_key` entries.

3. Start the proxy (port **4000**):

   ```bash
   litellm --config litellm-e2e.local.yaml --port 4000
   ```

4. Optional: `curl -sS http://127.0.0.1:4000/health`

**Version note:** this guide targets **“latest”** LiteLLM from PyPI. If a future release breaks the YAML shape, check [LiteLLM config docs](https://docs.litellm.ai/docs/proxy/configs) and adjust `litellm-e2e.local.yaml`.

## 3.1 Does LiteLLM require an API key? (how to find out)

**Default for this runbook:** no key — `LLMGatewayClient` does not send a LiteLLM `Authorization` header.

**To see if *your* proxy requires auth:**

1. Open your **`litellm-e2e.local.yaml`** — if you (or a template) set **`general_settings.master_key`**, the proxy will expect clients to pass that key. **Remove** `master_key` for local-only dev smoke unless you need it.
2. After starting LiteLLM, call: `curl -sS -o NUL -w "%{http_code}" http://127.0.0.1:4000/health` (or open `/v1/models` in a browser). If unauthenticated calls get **200**, you are fine for `support_rag` as-is. If you get **401/403** on API routes, you must either **drop the key from config** (simplest) or add a **future** `support_rag` feature to send an optional `Authorization` header to LiteLLM.
3. Read the terminal output when LiteLLM starts; it often prints whether a master key is set.

**Bottom line for “I don’t know”:** use **no** `master_key` in `litellm-e2e.local.yaml` for the simplest local loop.

## 4. Configure and start support_rag

1. **Config:** `cp config.e2e.example.yaml config.e2e.yaml` (or point `RAG_CONFIG` at a copy you manage).

2. **Env (PowerShell):**

   ```powershell
   $env:RAG_CONFIG = "config.e2e.yaml"
   $env:RAG_SERVICE_TOKEN = "dev-service"
   $env:RAG_ADMIN_TOKEN = "dev-admin"
   $env:RAG_LLM_GATEWAY__BASE_URL = "http://127.0.0.1:4000"
   $env:RAG_QDRANT__URL = "http://127.0.0.1:6333"
   ```

   **Bash:**

   ```bash
   export RAG_CONFIG=config.e2e.yaml
   export RAG_SERVICE_TOKEN=dev-service
   export RAG_ADMIN_TOKEN=dev-admin
   export RAG_LLM_GATEWAY__BASE_URL=http://127.0.0.1:4000
   export RAG_QDRANT__URL=http://127.0.0.1:6333
   ```

3. **Start RAG** (from repo root, with project dev deps installed):

   ```bash
   py -3.12 -m uvicorn support_rag.app:app --host 0.0.0.0 --port 8080
   ```

4. **Health (PowerShell):** replace token if needed.

   ```powershell
   curl.exe -sS -H "Authorization: Bearer $env:RAG_SERVICE_TOKEN" "http://127.0.0.1:8080/rag/health"
   ```

## 5. Preflight (when `scripts/e2e_gateway_preflight.py` exists)

Loads `RAG_CONFIG`, uses `LLMGatewayClient` against LiteLLM, checks embed + chat. Exit **0** when the stack is healthy.

## 6. Minimal smoke: index + retrieve

**Bash** (set `RAG_SERVICE_TOKEN` / `RAG_ADMIN_TOKEN` first):

```bash
curl -sS -X POST "http://127.0.0.1:8080/rag/index/kb" \
  -H "Authorization: Bearer $RAG_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"docs":[{"id":"e2e-smoke-1","text":"Short smoke document for local E2E.","metadata":{}}]}'
```

```bash
curl -sS -X POST "http://127.0.0.1:8080/rag/retrieve" \
  -H "Authorization: Bearer $RAG_SERVICE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"smoke","namespace":"kb","top_k":3}'
```

Expect **HTTP 200** and valid JSON.

## 7. Evidence (local-only)

- LiteLLM started from `litellm-e2e.local.yaml` with **only** Ollama `api_base` in `model_list`.
- No cloud LLM calls required for the smoke; config review is enough for sign-off in dev.
- Ollama shows load during the test (`ollama ps` or logs).

## 8. Example: preflight failure text (for implementers)

```text
E2E preflight failed.

1) LiteLLM not reachable at http://127.0.0.1:4000
   - pip install: litellm --config litellm-e2e.local.yaml --port 4000

2) Ollama / models
   ollama serve
   ollama pull all-minilm
   ollama pull llama3.2:1b

3) Embedding dim: ollama show all-minilm  (expect 384 with default config)

4) Qdrant at http://127.0.0.1:6333
```

## 9. Decisions (recorded)

| Topic | Choice |
|-------|--------|
| LiteLLM | **Local** — install via **pip**; start with **`litellm` CLI**; **not** Docker. |
| LiteLLM version | **Latest** from PyPI (`pip install -U`); if YAML breaks, adjust with upstream docs. |
| Auth | **Prefer no `master_key`** for simplest loop; use §3.1 if you need to verify. |
| Routing | **By JSON `model` names `embedding` / `retrieval`** in `docs/litellm-ollama-e2e.example.yaml`; **`X-Slot` not required** on LiteLLM for this runbook. |
| Docker | **Not used** in this runbook (RAG, LiteLLM, Ollama local; Qdrant via binary or your non-Docker install). |
| Registry | **N/A** — Ollama and LiteLLM run locally. |

## 10. Pytest `e2e_privacy`

```bash
set RUN_E2E_PRIVACY=1
py -3.12 -m pytest -m e2e_privacy -q
```

**GitLab (self-hosted `rag-mvp1-eval`):** job `e2e_privacy_allow_remote` in `.gitlab-ci.yml` runs the preflight script and the same `e2e_privacy` tests on a **schedule** / **Run pipeline** / **API** (not on merge requests by default). Set `RAG_CONFIG`, `RAG_SERVICE_TOKEN`, and `RAG_ADMIN_TOKEN` in CI variables — see [README — MVP1 eval + perf CI](../README.md#mvp1-eval--perf-ci-gitlab).

---

## Links

- Spec: `_bmad-output/implementation-artifacts/spec-mvp1-allow-remote-false-acceptance.md`
- RAG E2E config: `config.e2e.example.yaml`
- LiteLLM example: `docs/litellm-ollama-e2e.example.yaml`
