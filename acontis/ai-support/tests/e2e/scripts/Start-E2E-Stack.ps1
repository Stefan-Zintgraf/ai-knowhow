# Start the local E2E stack: Ollama, Qdrant, LiteLLM, AnythingLLM Desktop (optional), support_rag.
# All services are started in separate processes so this script can finish
# and print status. Default ports: AnythingLLM 3001, LiteLLM 4000, RAG 8080, Qdrant 6333, Ollama 11434.
#
# Prereq: ollama, Qdrant release binary (on PATH or -QdrantPath),
#   `py -3.12 -m pip install -U "litellm[proxy]"` (base `litellm` is not enough for the proxy; needs backoff, etc.),
#   project dev deps for uvicorn, models. Same local-process stack as docs/runbook-allow-remote-false-e2e.md
#   E2E Ollama models (all-minilm, llama3.2:1b): pull only when not already local (see Ensure-E2EOllamaModels).
#
# RAG (support_rag) is started by Start-RAG.ps1 — do not duplicate that logic here.
#
# -Logs: write each process stdout/stderr to tests/e2e/logs/e2e-<name>.(stdout|stderr).log (for debugging),
#   including AnythingLLM Desktop (e2e-anythingllm.*.log). Without -Logs, services stay quiet on this console
#   (AnythingLLM uses shell launch so Electron/Node does not inherit PowerShell and flood [backend] lines).
# Spawns a tiny .cmd that runs: start "" /B <exe> <args> 1>... 2>...  then exit. That detaches the server
# (unlike "cmd /c long-running-app 1>... 2>..." which can block cmd / or confuse lifetime while waiting).
# With -Logs, Python is started via the resolved python.exe from `py -3.12` (not "py" "-3.12" ...), because
# cmd "start" can mangle the -3.12 token (breaks at the dot) and the interpreter gets wrong flags.
#
# -Preflight: after the stack is up, run the same gateway check as tests\e2e\scripts\Run-E2E-Preflight.ps1
#   (scripts\e2e_gateway_preflight.py). Fails the script on non-zero exit. Sets RAG_LLM_GATEWAY__BASE_URL
#   to match -LiteLLmPort. Uses py -3.12 like the standalone preflight script.

#Requires -Version 5.1
[CmdletBinding()]
param(
    [int]$OllamaPort = 11434,
    [int]$QdrantPort = 6333,
    [int]$LiteLLmPort = 4000,
    [int]$RagPort = 8080,
    [string]$QdrantPath = "qdrant",
    [int]$StartTimeoutSec = 120,
    [int]$AnythingLlmPort = 3001,
    [string]$AnythingLlmExePath = "",
    [int]$AnythingLlmStartTimeoutSec = 90,
    [switch]$SkipAnythingLlm,
    [switch]$Logs,  # also: -logs (case-insensitive)
    [switch]$SkipOllamaPull,
    [switch]$Preflight,
    [Alias('h')][switch]$Help,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$E2EHelpRest = $null
)

$__e2eHelpWanted = $Help -or ($null -ne $E2EHelpRest -and ($E2EHelpRest | Where-Object { $_ -in @('--help', '-h', '-?', '/?') }))
if ($__e2eHelpWanted) {
    Write-Host @'
Start-E2E-Stack.ps1 - start local E2E stack: Ollama, Qdrant, LiteLLM, optional AnythingLLM, support_rag (via Start-RAG.ps1).

Default ports: AnythingLLM 3001, LiteLLM 4000, RAG 8080, Qdrant 6333, Ollama 11434.

  powershell -File tests\e2e\scripts\Start-E2E-Stack.ps1 [options]

Options (non-exhaustive):
  -OllamaPort, -QdrantPort, -LiteLLmPort, -RagPort   Port overrides
  -QdrantPath        Qdrant binary path or name on PATH
  -StartTimeoutSec   Wait for each service to listen
  -AnythingLlmPort, -AnythingLlmExePath, -AnythingLlmStartTimeoutSec
  -SkipAnythingLlm   Do not start AnythingLLM Desktop
  -SkipOllamaPull   Skip ollama model pull (ensure E2E models present)
  -Logs              Log each process (incl. AnythingLLM) to tests/e2e/logs
  -Preflight         After the stack is up, run scripts/e2e_gateway_preflight.py (fails on error)
  -Help, -h, --help  Show this help

'@
    exit 0
}
Remove-Variable __e2eHelpWanted -ErrorAction SilentlyContinue

$ErrorActionPreference = "Stop"

# tests/e2e/scripts -> repo root (three levels up)
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

# LiteLLM proxy prints a Unicode banner at startup; without UTF-8, Windows consoles (e.g. cp1252) can throw
# UnicodeEncodeError and the proxy exits before listening — looks like a port timeout. Child processes inherit.
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

. (Join-Path $PSScriptRoot "E2E-Stack-Helpers.ps1")

$LitellmConfig = Join-Path $Root "docs\litellm-ollama-e2e.example.yaml"

Write-Host "Repo root: $Root" -ForegroundColor Cyan
$E2ePy312 = $null
if ($Logs) {
    $env:PYTHONUNBUFFERED = "1"
    $env:PYTHONIOENCODING = "utf-8"
    Write-Host "Logging enabled: $E2eLogDir (stdout/stderr per service)" -ForegroundColor Cyan
    $o = & py -3.12 -c "import sys; print(sys.executable)" 2>&1
    if (-not $?) { throw "py -3.12 is required for -Logs. Output: $o" }
    $line = if ($o -is [string]) { $o } else { ($o | Select-Object -First 1) }
    $E2ePy312 = if ($line) { $line.ToString().Trim() } else { [string]($o | Out-String).Trim() }
    if (-not (Test-Path -LiteralPath $E2ePy312)) {
        throw "For -Logs, could not resolve Python 3.12 [invalid path: '$E2ePy312']. Output was: $o"
    }
    Write-Host "Python 3.12 for -Logs: $E2ePy312" -ForegroundColor DarkGray
}
# Resolve which Python has litellm (may differ from 3.12 if only installed globally in another version).
# litellm >= 1.80 dropped __main__; use litellm.proxy.proxy_cli instead of -m litellm.
$LitellmPyVer = $null
$LitellmPyExe = $null
$prevEAP = $ErrorActionPreference; $ErrorActionPreference = "SilentlyContinue"
foreach ($ver in @("3.12", "3.14", "3.13", "3.11")) {
    & py -$ver -c "import litellm" 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $LitellmPyVer = $ver
        if ($Logs) {
            $exeLine = & py -$ver -c "import sys; print(sys.executable)" 2>&1
            $LitellmPyExe = if ($exeLine -is [string]) { $exeLine.Trim() } else { ($exeLine | Select-Object -First 1).ToString().Trim() }
        }
        break
    }
}
$ErrorActionPreference = $prevEAP
if (-not $LitellmPyVer) {
    throw "No Python with 'litellm' package found. Install: py -3.12 -m pip install -U 'litellm[proxy]'"
}
# pip install litellm alone omits proxy extras; proxy CLI exits with ModuleNotFoundError (e.g. backoff).
& py -$LitellmPyVer -c "import backoff" 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "LiteLLM proxy extra missing (e.g. 'backoff'). The proxy will exit immediately. Install: py -$LitellmPyVer -m pip install -U 'litellm[proxy]'"
}
Write-Host "LiteLLM Python: py -$LitellmPyVer$(if ($LitellmPyExe) { " ($LitellmPyExe)" })" -ForegroundColor DarkGray
Write-Host ""

# --- Ollama ---
if (Test-TcpOpen -Port $OllamaPort) {
    Write-Host "Ollama: already running on $OllamaPort" -ForegroundColor DarkGray
} else {
    $ollamaExe = Resolve-OllamaExe
    if (-not $ollamaExe) {
        throw "Ollama not found (PATH, merged registry PATH, or default install under LocalAppData/Program Files). Install from https://ollama.com"
    }
    Start-E2EProcess -Name "ollama" -FilePath $ollamaExe -CommandArgs @("serve") -LogToFiles:$Logs
    Write-Host "Ollama: started (serve)" -ForegroundColor Yellow
    Wait-ForPort -Label "Ollama" -Port $OllamaPort -TimeoutSec $StartTimeoutSec
}
if (-not $SkipOllamaPull) {
    $ex = Resolve-OllamaExe
    try {
        Ensure-E2EOllamaModels -OllamaExe $ex
    } catch {
        Write-Host "Ollama model pull failed: $($_.Exception.Message). Re-run with -SkipOllamaPull if you manage models manually." -ForegroundColor Red
        throw
    }
} else {
    Write-Host "Ollama: skipped model pull (-SkipOllamaPull). Ensure all-minilm and llama3.2:1b are present." -ForegroundColor DarkYellow
}

# --- Qdrant (local binary; see runbook for install) ---
if (Test-TcpOpen -Port $QdrantPort) {
    Write-Host "Qdrant: already running on $QdrantPort" -ForegroundColor DarkGray
} else {
    $exe = if ((Test-Path -LiteralPath $QdrantPath) -and (Test-Path -LiteralPath $QdrantPath -PathType Leaf)) {
        (Resolve-Path -LiteralPath $QdrantPath).Path
    } else {
        Resolve-Cmd $QdrantPath
    }
    if (-not $exe) {
        throw "Qdrant not found: '$QdrantPath'. Add to machine/user PATH, or pass -QdrantPath to the full .exe. Install: https://github.com/qdrant/qdrant/releases"
    }
    Start-E2EProcess -Name "qdrant" -FilePath $exe -LogToFiles:$Logs
    Write-Host "Qdrant: started" -ForegroundColor Yellow
    Wait-ForPort -Label "Qdrant" -Port $QdrantPort -TimeoutSec $StartTimeoutSec
}

# --- LiteLLM ---
if (Test-TcpOpen -Port $LiteLLmPort) {
    Write-Host "LiteLLM: port $LiteLLmPort in use (assuming proxy already running)" -ForegroundColor DarkGray
} else {
    if (-not (Test-Path -LiteralPath $LitellmConfig)) {
        throw "LiteLLM config missing: $LitellmConfig"
    }
    if ($Logs) {
        Start-E2EProcess -Name "litellm" -FilePath $LitellmPyExe -LogToFiles -CommandArgs @(
            "-m", "litellm.proxy.proxy_cli", "--config", $LitellmConfig, "--port", "$LiteLLmPort"
        )
    } else {
        Start-E2EProcess -Name "litellm" -FilePath "py" -CommandArgs @(
            "-$LitellmPyVer", "-m", "litellm.proxy.proxy_cli", "--config", $LitellmConfig, "--port", "$LiteLLmPort"
        )
    }
    Write-Host "LiteLLM: started on port $LiteLLmPort" -ForegroundColor Yellow
    Wait-ForPort -Label "LiteLLM" -Port $LiteLLmPort -TimeoutSec $StartTimeoutSec
}

# Align support_rag → AnythingLLM HTTP API with script port (env overrides YAML for this session)
$env:RAG_ANYTHING_LLM__BASE_URL = "http://127.0.0.1:$AnythingLlmPort"

# --- AnythingLLM Desktop (local API; no Docker). Order: after LiteLLM, before support_rag ---
if (-not $SkipAnythingLlm) {
    if (Test-TcpOpen -Port $AnythingLlmPort) {
        Write-Host "AnythingLLM: already listening on $AnythingLlmPort" -ForegroundColor DarkGray
    } else {
        $almExe = Resolve-AnythingLlmDesktopExe -ExplicitPath $AnythingLlmExePath
        Start-AnythingLLMDesktop -ExePath $almExe -LogToFiles:$Logs
        Write-Host "AnythingLLM: started Desktop ($almExe)" -ForegroundColor Yellow
        Write-Host "AnythingLLM: waiting for TCP $AnythingLlmPort (first cold start can need 90-120s)..." -ForegroundColor DarkGray
        Wait-ForPort -Label "AnythingLLM" -Port $AnythingLlmPort -TimeoutSec $AnythingLlmStartTimeoutSec
    }
    try {
        $sys = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$AnythingLlmPort/api/v1/system" -TimeoutSec 10
        Write-Host "AnythingLLM /api/v1/system: $($sys.StatusCode)" -ForegroundColor DarkGreen
    } catch {
        Write-Host "AnythingLLM /api/v1/system: not ready - $($_.Exception.Message)" -ForegroundColor DarkYellow
    }
    Write-Host "AnythingLLM API: http://127.0.0.1:$AnythingLlmPort/  (create keys in Desktop, Entwickler-API or API keys - not in external browser)" -ForegroundColor Cyan
    Write-Host "  Ingest/vector: set RAG_ANYTHING_LLM__API_KEY in repo .env, then restart support_rag. Web UI: http://127.0.0.1:$RagPort/ui/" -ForegroundColor DarkGray
} else {
    Write-Host "AnythingLLM: skipped (-SkipAnythingLlm). If you use anything_llm in RAG_CONFIG, set RAG_ANYTHING_LLM__BASE_URL=$($env:RAG_ANYTHING_LLM__BASE_URL)" -ForegroundColor DarkYellow
}

# --- support_rag (Start-RAG.ps1: env, uvicorn, /rag/health + /ui/ probe) ---
& (Join-Path $PSScriptRoot "Start-RAG.ps1") -RagPort $RagPort -LiteLLmPort $LiteLLmPort -QdrantPort $QdrantPort `
    -StartTimeoutSec $StartTimeoutSec -RagConfig "config.e2e.yaml" -RagServiceToken "dev-service" -RagAdminToken "dev-admin" -Logs:$Logs
if (-not $?) { throw "Start-RAG.ps1 failed." }

Write-Host ""
Write-Host "E2E stack: all processes started. TCP listeners:" -ForegroundColor Green
Write-Host "  Ollama:       127.0.0.1:$OllamaPort"
Write-Host "  Qdrant:       127.0.0.1:$QdrantPort"
Write-Host "  LiteLLM:      127.0.0.1:$LiteLLmPort  (e.g. GET /health)"
if (-not $SkipAnythingLlm) {
    Write-Host "  AnythingLLM:  127.0.0.1:$AnythingLlmPort  (e.g. GET /api/v1/system)"
} else {
    Write-Host "  AnythingLLM:  (skipped - ensure Desktop matches RAG_ANYTHING_LLM__BASE_URL)"
}
Write-Host "  support_rag:  127.0.0.1:$RagPort  (GET /rag/health, Web UI /ui/ same process)"
Write-Host "Web UI (dual-RAG chat): http://127.0.0.1:$RagPort/ui/" -ForegroundColor Green
Write-Host ""

try {
    $h4000 = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$LiteLLmPort/health" -TimeoutSec 5
    Write-Host "LiteLLM /health: $($h4000.StatusCode)" -ForegroundColor DarkGreen
} catch {
    Write-Host "LiteLLM /health: could not reach (proxy may still be binding - retry manually)." -ForegroundColor DarkYellow
}

if ($Preflight) {
    $env:RAG_LLM_GATEWAY__BASE_URL = "http://127.0.0.1:$LiteLLmPort"
    if (-not $env:RAG_CONFIG) { $env:RAG_CONFIG = "config.e2e.yaml" }
    Write-Host ""
    Write-Host "E2E gateway preflight: running scripts\e2e_gateway_preflight.py (py -3.12) ..." -ForegroundColor Cyan
    & py -3.12 (Join-Path $Root "scripts\e2e_gateway_preflight.py")
    if ($LASTEXITCODE -ne 0) {
        throw "E2E preflight failed (exit $LASTEXITCODE). See scripts/e2e_gateway_preflight.py and the runbook."
    }
    Write-Host "E2E gateway preflight: OK" -ForegroundColor Green
}

exit 0

} finally {
    Pop-Location
}
