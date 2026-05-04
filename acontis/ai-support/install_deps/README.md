# install_deps — E2E stack (Ollama, Qdrant, LiteLLM, Python deps, model prefetch)

**Windows (PowerShell, from repo root):**

```powershell
powershell -ExecutionPolicy Bypass -File install_deps\install.ps1
```

**Linux / macOS (bash):**

```bash
chmod +x install_deps/install.sh
./install_deps/install.sh
```

**What it does**

- **Ollama** — `winget install Ollama.Ollama` (Windows) or the [official install](https://ollama.com) / Homebrew (macOS with Homebrew).
- **Qdrant** — downloads the latest Qdrant release binary into `install_deps/_tools/qdrant/` (portable, not a system install).
- **LiteLLM** — creates or updates `/.venv-e2e` in the **repo root** and `pip install "litellm[proxy]"` (match `docs/runbook-allow-remote-false-e2e.md`).
- **support_rag** — `pip install -e ".[dev]"` with `py -3.12` (or `python3.12` on Linux).
- **Ollama models** — `ollama pull all-minilm` and `ollama pull llama3.2:1b` (same as `config.e2e.example.yaml`).
- **Hugging Face cache** — runs `prefetch_hf_models.py` to download **local inference** assets: `BAAI/bge-reranker-v2-m3` and fastembed `Qdrant/bm25` (hybrid + rerank; requires network for first download). Optional: set `HF_TOKEN` for higher Hub rate limits.

**Skip parts (Windows)** — use switches: `-SkipOllama`, `-SkipQdrant`, `-SkipOllamaPull`, `-SkipLiteLLM`, `-SkipSupportRagPip`, `-SkipHF`.

**Skip parts (bash)** — set env, e.g. `SKIP_OLLAMA=1 ./install_deps/install.sh` (same `SKIP_*` names as in `install.sh`).

**Start services** — after this, start Ollama, Qdrant, LiteLLM, and `uvicorn` per `docs/runbook-allow-remote-false-e2e.md` and `tests/e2e/scripts/Start-E2E-Stack.ps1` (template).

**Python version** — scripts expect **3.12** (see `pyproject.toml`).
