# Start only support_rag (uvicorn) for local dev / E2E. Expects Qdrant + LiteLLM already reachable
# at the URLs you pass (same defaults as Start-E2E-Stack.ps1). Default: RAG 8080, LiteLLM 4000, Qdrant 6333.
#
# Used by Start-E2E-Stack.ps1. Can be run alone after the backing services are up.
# With -Logs, Python is started via the resolved python.exe from `py -3.12` (see Start-E2E-Stack header).

#Requires -Version 5.1
param(
    [int]$RagPort = 8080,
    [int]$LiteLLmPort = 4000,
    [int]$QdrantPort = 6333,
    [int]$StartTimeoutSec = 120,
    [string]$RagConfig = "config.e2e.yaml",
    [string]$RagServiceToken = "dev-service",
    [string]$RagAdminToken = "dev-admin",
    [switch]$Logs
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
$E2eLogDir = Join-Path $Root "tests\e2e\logs"

Push-Location $Root
try {

# IDE shells may miss global PATH; merge once so Get-Command matches a normal console.
$__p = @(
    @([Environment]::GetEnvironmentVariable("Path", "Machine") -split ";")
    @([Environment]::GetEnvironmentVariable("Path", "User") -split ";")
    @($env:Path -split ";")
) | ForEach-Object { if ($_) { $_.Trim() } } | Where-Object { $_ } | Select-Object -Unique
$env:Path = [string]::Join(";", $__p)
Remove-Variable __p -ErrorAction SilentlyContinue

. (Join-Path $PSScriptRoot "E2E-Stack-Helpers.ps1")

$E2ePy312 = $null
if ($Logs) {
    $env:PYTHONUNBUFFERED = "1"
    $env:PYTHONIOENCODING = "utf-8"
    Write-Host "Start-RAG: logging to $E2eLogDir (stdout/stderr per service)" -ForegroundColor Cyan
    $o = & py -3.12 -c "import sys; print(sys.executable)" 2>&1
    if (-not $?) { throw "py -3.12 is required for -Logs. Output: $o" }
    $line = if ($o -is [string]) { $o } else { ($o | Select-Object -First 1) }
    $E2ePy312 = if ($line) { $line.ToString().Trim() } else { [string]($o | Out-String).Trim() }
    if (-not (Test-Path -LiteralPath $E2ePy312)) {
        throw "For -Logs, could not resolve Python 3.12 [invalid path: '$E2ePy312']. Output was: $o"
    }
    Write-Host "Start-RAG: Python 3.12 for -Logs: $E2ePy312" -ForegroundColor DarkGray
}

$env:RAG_CONFIG = $RagConfig
$env:RAG_SERVICE_TOKEN = $RagServiceToken
$env:RAG_ADMIN_TOKEN = $RagAdminToken
# Optional /ui/ can call APIs without pasting these into the browser (see web_routes + deps require_*_ui).
$env:RAG_UI_AUTH_FROM_ENV = "1"
# Same Uvicorn app serves REST and /ui/ (dual-RAG chat); do not disable for E2E.
$env:RAG_ENABLE_WEB_UI = "1"
$env:RAG_LLM_GATEWAY__BASE_URL = "http://127.0.0.1:$LiteLLmPort"
$env:RAG_QDRANT__URL = "http://127.0.0.1:$QdrantPort"

Write-Host "Repo root: $Root" -ForegroundColor Cyan
Write-Host "Start-RAG: RAG_CONFIG=$RagConfig, service URL http://127.0.0.1:$RagPort" -ForegroundColor Cyan
Write-Host ""

if (Test-TcpOpen -Port $RagPort) {
    Write-Host "support_rag: port $RagPort in use (assuming app already running)" -ForegroundColor DarkGray
} else {
    if (-not (Test-Path (Join-Path $Root $RagConfig)) -and -not (Test-Path (Join-Path $Root "config.e2e.example.yaml"))) {
        Write-Host "Warning: $RagConfig not found. Copy from config.e2e.example.yaml per runbook if startup fails." -ForegroundColor DarkYellow
    }
    if ($Logs) {
        $iu = & $E2ePy312 -c "import uvicorn" 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python 3.12 has no 'uvicorn' package. Install project dev dependencies or: py -3.12 -m pip install -U uvicorn`n$iu"
        }
        Start-E2EProcess -Name "support_rag" -FilePath $E2ePy312 -LogToFiles -CommandArgs @(
            "-m", "uvicorn", "support_rag.app:app", "--host", "127.0.0.1", "--port", "$RagPort"
        )
    } else {
        Start-E2EProcess -Name "support_rag" -FilePath "py" -CommandArgs @(
            "-3.12", "-m", "uvicorn", "support_rag.app:app", "--host", "127.0.0.1", "--port", "$RagPort"
        )
    }
    Write-Host "support_rag: started (uvicorn)" -ForegroundColor Yellow
    Wait-ForPort -Label "support_rag" -Port $RagPort -TimeoutSec $StartTimeoutSec
}

Write-Host ""
Write-Host "Start-RAG: process ready. support_rag: 127.0.0.1:$RagPort  (GET /rag/health with Bearer service token)" -ForegroundColor Green
$tok = $env:RAG_SERVICE_TOKEN
try {
    $h = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$RagPort/rag/health" -Headers @{ Authorization = "Bearer $tok" } -TimeoutSec 5
    Write-Host "support_rag /rag/health: $($h.StatusCode)" -ForegroundColor DarkGreen
} catch {
    Write-Host "support_rag /rag/health: not ready yet (app may need a few more seconds or config). $($_.Exception.Message)" -ForegroundColor DarkYellow
}

# HTML Web UI readiness (same process as REST; GET /ui/ expected 200, or redirect)
$uiUrl = "http://127.0.0.1:$RagPort/ui/"
$uiCode = 0
try {
    $ui = Invoke-WebRequest -UseBasicParsing -Uri $uiUrl -TimeoutSec 10
    $uiCode = [int]$ui.StatusCode
} catch {
    $resp = $_.Exception.Response
    if ($null -ne $resp) {
        try { $uiCode = [int]$resp.StatusCode } catch { $uiCode = 0 }
    }
}
if ($uiCode -in @(200, 301, 302, 303, 307, 308)) {
    Write-Host "support_rag Web UI /ui/: HTTP $uiCode" -ForegroundColor DarkGreen
} else {
    Write-Host "support_rag Web UI /ui/: probe uncertain (HTTP $uiCode). Check RAG_ENABLE_WEB_UI and logs." -ForegroundColor DarkYellow
}
Write-Host "Web UI (dual-RAG chat): $uiUrl" -ForegroundColor Green

exit 0

} finally {
    Pop-Location
}
