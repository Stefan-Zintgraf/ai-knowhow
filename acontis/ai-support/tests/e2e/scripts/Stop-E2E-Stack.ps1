# Stop the local E2E stack: same ports as Start-E2E-Stack.ps1 (by listener PID).
# Stops support_rag, LiteLLM, AnythingLLM Desktop (by process name), Qdrant, Ollama.
#
# RAG is stopped by Stop-RAG.ps1 (single implementation).
#
# This kills whatever is listening on those ports. If you use the same host for
# unrelated work on 11434/6333/3001/4000/8080, set custom ports in *both* scripts or
# stop services manually.

#Requires -Version 5.1
[CmdletBinding()]
param(
    [int]$OllamaPort = 11434,
    [int]$QdrantPort = 6333,
    [int]$LiteLLmPort = 4000,
    [int]$RagPort = 8080,
    [int]$AnythingLlmPort = 3001,
    [switch]$SkipAnythingLlm,
    [Alias('h')][switch]$Help,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$E2EHelpRest = $null
)

$__e2eHelpWanted = $Help -or ($null -ne $E2EHelpRest -and ($E2EHelpRest | Where-Object { $_ -in @('--help', '-h', '-?', '/?') }))
if ($__e2eHelpWanted) {
    Write-Host @'
Stop-E2E-Stack.ps1 - stop the local E2E stack: support_rag, LiteLLM, AnythingLLM, Qdrant, Ollama
(listeners on the ports below; see Start-E2E-Stack for defaults).

  powershell -File tests\e2e\scripts\Stop-E2E-Stack.ps1 [options]

Options:
  -OllamaPort, -QdrantPort, -LiteLLmPort, -RagPort, -AnythingLlmPort   Port overrides (must match start)
  -SkipAnythingLlm   Do not stop AnythingLLM Desktop
  -Help, -h, --help  Show this help

'@
    exit 0
}
Remove-Variable __e2eHelpWanted -ErrorAction SilentlyContinue

$ErrorActionPreference = "Continue"

# tests/e2e/scripts -> repo root
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")

Push-Location $Root
try {

. (Join-Path $PSScriptRoot "E2E-Stack-Helpers.ps1")

Write-Host "Stop-E2E-Stack: stopping listeners (repo $Root)" -ForegroundColor Cyan
Write-Host ""

# Order: RAG, LiteLLM, AnythingLLM (process), then Qdrant, Ollama
& (Join-Path $PSScriptRoot "Stop-RAG.ps1") -RagPort $RagPort
Stop-PortListener -Label "LiteLLM" -Port $LiteLLmPort
if ($SkipAnythingLlm) {
    Stop-AnythingLlmDesktop -Port $AnythingLlmPort -Skip
} else {
    Stop-AnythingLlmDesktop -Port $AnythingLlmPort
}
Stop-PortListener -Label "Qdrant"  -Port $QdrantPort
Stop-PortListener -Label "Ollama"  -Port $OllamaPort

Write-Host ""
Write-Host "Stop-E2E-Stack: done." -ForegroundColor Green
exit 0

} finally {
    Pop-Location
}
