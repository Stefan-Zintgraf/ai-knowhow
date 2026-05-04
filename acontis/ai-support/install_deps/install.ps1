# Install Ollama, Qdrant (portable), LiteLLM venv, support_rag Python deps, Ollama models, and HF model cache.
# Run from repo root:  powershell -ExecutionPolicy Bypass -File install_deps\install.ps1
# Requires: Windows 10+, winget (for Ollama), py -3.12 on PATH, network for GitHub and Hugging Face.
param(
    [switch] $SkipOllama,
    [switch] $SkipQdrant,
    [switch] $SkipOllamaPull,
    [switch] $SkipLiteLLM,
    [switch] $SkipSupportRagPip,
    [switch] $SkipHF
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$ToolsQdrant = Join-Path $PSScriptRoot "_tools\qdrant"
$OllamaModels = @("all-minilm", "llama3.2:1b")

function Test-Cmd {
    param([string] $Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

Write-Host "Repo: $RepoRoot"

if (-not $SkipOllama) {
    if (Test-Cmd ollama) {
        Write-Host "Ollama already on PATH, skipping winget."
    } else {
        if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
            throw "winget not found. Install the App Installer / Ollama manually from https://ollama.com/download"
        }
        Write-Host "Installing Ollama via winget…"
        winget install -e --id Ollama.Ollama --accept-source-agreements --accept-package-agreements
        $ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama"
        if (Test-Path $ollamaPath) { $env:Path = "$ollamaPath;$env:Path" }
    }
}

if (-not $SkipQdrant) {
    $qExe = Join-Path $ToolsQdrant "qdrant.exe"
    if (Test-Path $qExe) {
        Write-Host "Qdrant already present: $qExe"
    } else {
        Write-Host "Downloading Qdrant (Windows)…"
        New-Item -ItemType Directory -Force -Path $ToolsQdrant | Out-Null
        $rel = Invoke-RestMethod -Uri "https://api.github.com/repos/qdrant/qdrant/releases/latest" -Headers @{ "User-Agent" = "install_deps" }
        $zipName = "qdrant-x86_64-pc-windows-msvc.zip"
        $asset = $rel.assets | Where-Object { $_.name -eq $zipName } | Select-Object -First 1
        if (-not $asset) { throw "Could not find $zipName in latest Qdrant release." }
        $zipPath = Join-Path $env:TEMP "qdrant-win.zip"
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zipPath
        Expand-Archive -Path $zipPath -DestinationPath $ToolsQdrant -Force
        Remove-Item $zipPath -ErrorAction SilentlyContinue
        if (-not (Test-Path $qExe)) { throw "qdrant.exe not found after extract under $ToolsQdrant" }
        Write-Host "Qdrant installed to: $qExe  (add folder to PATH or run from this directory)"
    }
}

if (-not $SkipLiteLLM) {
    $VenvE2e = Join-Path $RepoRoot ".venv-e2e"
    if (-not (Test-Path $VenvE2e)) {
        & py -3.12 -m venv $VenvE2e
    }
    $pip = Join-Path $VenvE2e "Scripts\pip.exe"
    & $pip install -U pip
    & $pip install -U "litellm[proxy]"
    Write-Host "LiteLLM venv: $VenvE2e  (activate, then: litellm --config docs\litellm-ollama-e2e.example.yaml --port 4000)"
}

if (-not $SkipSupportRagPip) {
    Set-Location $RepoRoot
    & py -3.12 -m pip install -U pip
    & py -3.12 -m pip install -e ".[dev]"
    Write-Host "support-rag dev install OK (active Python: py -3.12)"
}

$ollamaExe = "ollama"
$cand = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
if (-not (Test-Cmd ollama) -and (Test-Path $cand)) { $ollamaExe = $cand }
if (-not $SkipOllamaPull) {
    if ((Test-Cmd ollama) -or (Test-Path $cand)) {
        foreach ($m in $OllamaModels) {
            Write-Host "ollama pull $m"
            if (Test-Cmd ollama) { & ollama pull $m } else { & $cand pull $m }
        }
    } else {
        Write-Warning "ollama not on PATH; open a new terminal and run: ollama pull all-minilm; ollama pull llama3.2:1b"
    }
}

if (-not $SkipHF) {
    Set-Location $RepoRoot
    & py -3.12 (Join-Path $PSScriptRoot "prefetch_hf_models.py")
}

Write-Host "Done. See install_deps\README.md for how to start each component."
