# Step 2 — Gateway preflight: same checks as scripts/e2e_gateway_preflight.py (LiteLLM embed + chat).
# Note: preflight only calls LiteLLM (llm_gateway.base_url, e.g. :4000). It does not use support_rag :8080.
# Requires: LiteLLM + Ollama + models per docs/runbook-allow-remote-false-e2e.md (LiteLLM must be running in another window)
# Usage: from anywhere, powershell -File tests\e2e\scripts\Run-E2E-Preflight.ps1

$ErrorActionPreference = "Stop"
# tests/e2e/scripts -> repo root (three levels up)
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")

Push-Location $Root
try {
    # Preflight defaults to config.e2e.yaml and falls back to config.e2e.example.yaml (see e2e_gateway_preflight.py).
    # If LiteLLM is not on port 4000:  $env:RAG_LLM_GATEWAY__BASE_URL = "http://127.0.0.1:YOUR_PORT"
    # If the proxy returns 401:        $env:RAG_LLM_GATEWAY__API_KEY = "<same as LITELLM master_key>"
    if (-not $env:RAG_CONFIG) { $env:RAG_CONFIG = "config.e2e.yaml" }

    & py -3.12 (Join-Path $Root "scripts\e2e_gateway_preflight.py")
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
