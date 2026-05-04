# Optional E2E smoke: preflight, Qdrant + RAG health, index + retrieve.
# Documented local-only Ollama path; do not use allow_remote: true in the LiteLLM file for this profile.
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root
if (-not $env:RAG_CONFIG) { $env:RAG_CONFIG = "config.e2e.yaml" }
& py -3.12 (Join-Path $Root "scripts/e2e_gateway_preflight.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$Base = if ($env:E2E_RAG_BASE_URL) { $env:E2E_RAG_BASE_URL } else { "http://127.0.0.1:8080" }
$Qd = if ($env:E2E_QDRANT_URL) { $env:E2E_QDRANT_URL } else { "http://127.0.0.1:6333" }
$st = $env:RAG_SERVICE_TOKEN
$ad = $env:RAG_ADMIN_TOKEN
if (-not $st -or -not $ad) { throw "set RAG_SERVICE_TOKEN and RAG_ADMIN_TOKEN" }

for ($i = 0; $i -lt 30; $i++) {
    try { Invoke-RestMethod -Uri "$Qd/collections" -Method Get -TimeoutSec 2 | Out-Null; break } catch { Start-Sleep -Seconds 1 }
}
$null = Invoke-RestMethod -Uri "$Qd/collections" -Method Get

$headersHealth = @{ Authorization = "Bearer $st" }
for ($i = 0; $i -lt 30; $i++) {
    try { Invoke-RestMethod -Uri "$Base/rag/health" -Headers $headersHealth -Method Get -TimeoutSec 2 | Out-Null; break } catch { Start-Sleep -Seconds 1 }
}
$null = Invoke-RestMethod -Uri "$Base/rag/health" -Headers $headersHealth -Method Get

$headersAd = @{
    Authorization = "Bearer $ad"
    "Content-Type"  = "application/json"
}
$bodyIdx = '{"docs":[{"id":"smoke-1","text":"hello smoke","metadata":{}}]}'
$null = Invoke-RestMethod -Uri "$Base/rag/index/kb" -Headers $headersAd -Method Post -Body $bodyIdx
$headersSt = @{
    Authorization = "Bearer $st"
    "Content-Type"  = "application/json"
}
$ret = Invoke-RestMethod -Uri "$Base/rag/retrieve" -Headers $headersSt -Method Post -Body '{"query":"hello","top_k":2}'
if (-not $ret.PSObject.Properties["chunks"]) { throw "retrieve JSON missing chunks" }
Write-Host "smoke_allow_remote OK"
