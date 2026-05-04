# Stop only the support_rag process (listener on the RAG port). Same default port as Start-RAG / Start-E2E-Stack.
# Used by Stop-E2E-Stack.ps1; can be run alone.

#Requires -Version 5.1
param(
    [int]$RagPort = 8080
)

$ErrorActionPreference = "Continue"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")

Push-Location $Root
try {

. (Join-Path $PSScriptRoot "E2E-Stack-Helpers.ps1")

Write-Host "Stop-RAG: stopping support_rag (REST and browser /ui/ share the same port and process) (repo $Root)" -ForegroundColor Cyan
Write-Host ""

Stop-PortListener -Label "support_rag" -Port $RagPort

Write-Host ""
Write-Host "Stop-RAG: done." -ForegroundColor Green
exit 0

} finally {
    Pop-Location
}
