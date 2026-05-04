#Requires -Version 5.1
<#
.SYNOPSIS
  Activates Tools/kerio_mail/.venv for Kerio JSON-RPC mail scripts.

  You must DOT-SOURCE this script so the environment persists:
    . .\venv_activate.ps1

  Running .\venv_activate.ps1 without the leading dot activates only a child scope.
#>
$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Activate = Join-Path $ScriptDir '.venv\Scripts\Activate.ps1'

if (-not (Test-Path $Activate)) {
    Write-Error "Activate.ps1 not found at $Activate. Run venv_install.ps1 first."
}

. $Activate
