# Step 3 — Pytest e2e_privacy (live RAG on 127.0.0.1:8080).
# Requires: stack from runbook + Step 2 green; tokens must match the running RAG process.
# Usage: powershell -File tests\e2e\scripts\Run-E2E-Privacy-Tests.ps1

$ErrorActionPreference = "Stop"
# tests/e2e/scripts -> repo root (three levels up)
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")

Push-Location $Root
try {
    $env:RUN_E2E_PRIVACY = "1"
    if (-not $env:RAG_SERVICE_TOKEN) { $env:RAG_SERVICE_TOKEN = "dev-service" }
    if (-not $env:RAG_ADMIN_TOKEN) { $env:RAG_ADMIN_TOKEN = "dev-admin" }
    if (-not $env:E2E_RAG_BASE_URL) { $env:E2E_RAG_BASE_URL = "http://127.0.0.1:8080" }

    & py -3.12 -m pytest (Join-Path $Root "tests\e2e") -m e2e_privacy -q
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
