#!/usr/bin/env bash
# Install Ollama, Qdrant (portable), LiteLLM venv, support_rag Python deps, Ollama models, and HF model cache.
# Usage:  chmod +x install_deps/install.sh && ./install_deps/install.sh
# Options: SKIP_OLLAMA=1 SKIP_QDRANT=1 SKIP_OLLAMA_PULL=1 SKIP_LITELLM=1 SKIP_SUPPORT_RAG_PIP=1 SKIP_HF=1
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS_QDRANT="$ROOT/install_deps/_tools/qdrant"
LATEST="https://api.github.com/repos/qdrant/qdrant/releases/latest"

error() { echo "error: $*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

echo "Repo: $ROOT"

if [[ "${SKIP_OLLAMA:-0}" != "1" ]]; then
  if have ollama; then
    echo "Ollama already on PATH, skipping install."
  else
    if [[ "$(uname -s)" == "Darwin" ]]; then
      if have brew; then
        echo "Installing Ollama via Homebrew…"
        brew install ollama
      else
        error "Install Ollama from https://ollama.com/download (or install Homebrew first)."
      fi
    else
      echo "Installing Ollama via ollama.com script…"
      curl -fsSL https://ollama.com/install.sh | sh
    fi
  fi
fi

if [[ "${SKIP_QDRANT:-0}" != "1" ]]; then
  if [[ -x "$TOOLS_QDRANT/qdrant" ]]; then
    echo "Qdrant already present: $TOOLS_QDRANT/qdrant"
  else
    echo "Downloading Qdrant…"
    mkdir -p "$TOOLS_QDRANT"
    uname_s="$(uname -s)"
    uname_m="$(uname -m)"
    asset=""
    if [[ "$uname_s" == "Darwin" && "$uname_m" == "arm64" ]]; then
      asset="qdrant-aarch64-apple-darwin.tar.gz"
    elif [[ "$uname_s" == "Darwin" ]]; then
      asset="qdrant-x86_64-apple-darwin.tar.gz"
    else
      asset="qdrant-x86_64-unknown-linux-musl.tar.gz"
    fi
    url="$(
      curl -fsSL -H "User-Agent: install_deps" "$LATEST" | python3 -c \
        "import json,sys; r=json.load(sys.stdin); a=sys.argv[1]; w=[x for x in r['assets'] if x['name']==a]; assert w; print(w[0]['browser_download_url'])" \
        "$asset"
    )"
    tmp="$(mktemp)"
    curl -fsSL "$url" -o "$tmp"
    tar -xzf "$tmp" -C "$TOOLS_QDRANT"
    rm -f "$tmp"
    if [[ ! -f "$TOOLS_QDRANT/qdrant" ]]; then
      qbin="$(find "$TOOLS_QDRANT" -type f -name qdrant 2>/dev/null | head -n 1)"
      if [[ -n "$qbin" ]]; then mv "$qbin" "$TOOLS_QDRANT/qdrant"; fi
    fi
    [[ -f "$TOOLS_QDRANT/qdrant" ]] || error "qdrant binary missing after extract"
    chmod +x "$TOOLS_QDRANT/qdrant"
    echo "Qdrant: $TOOLS_QDRANT/qdrant  (add to PATH or run from this directory)"
  fi
fi

if [[ "${SKIP_LITELLM:-0}" != "1" ]]; then
  VENV_E2E="$ROOT/.venv-e2e"
  if [[ ! -d "$VENV_E2E" ]]; then
    ( command -v py >/dev/null 2>&1 && py -3.12 -m venv "$VENV_E2E" ) || \
    ( command -v python3.12 >/dev/null 2>&1 && python3.12 -m venv "$VENV_E2E" ) || \
    error "Need py -3.12 or python3.12 to create $VENV_E2E"
  fi
  # shellcheck source=/dev/null
  source "$VENV_E2E/bin/activate"
  pip install -U pip
  pip install -U "litellm[proxy]"
  echo "LiteLLM venv: $VENV_E2E"
  deactivate
fi

if [[ "${SKIP_SUPPORT_RAG_PIP:-0}" != "1" ]]; then
  cd "$ROOT"
  ( command -v py >/dev/null 2>&1 && py -3.12 -m pip install -U pip && py -3.12 -m pip install -e ".[dev]" ) || \
  ( have python3.12 && python3.12 -m pip install -U pip && python3.12 -m pip install -e ".[dev]" ) || \
  error "Install Python 3.12 and pip, then: pip install -e \".[dev]\" from repo root"
fi

if [[ "${SKIP_OLLAMA_PULL:-0}" != "1" ]]; then
  if have ollama; then
    ollama pull all-minilm
    ollama pull llama3.2:1b
  else
    echo "warning: ollama not on PATH; run: ollama pull all-minilm && ollama pull llama3.2:1b" >&2
  fi
fi

if [[ "${SKIP_HF:-0}" != "1" ]]; then
  cd "$ROOT"
  ( command -v py >/dev/null 2>&1 && py -3.12 "install_deps/prefetch_hf_models.py" ) || \
  ( have python3.12 && python3.12 "install_deps/prefetch_hf_models.py" ) || \
  error "prefetch: need py -3.12 or python3.12 with deps installed (pip install -e .)"
fi

echo "Done. See install_deps/README.md for how to start each component."
