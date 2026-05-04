#Requires -Version 5.1
<#
.SYNOPSIS
  Kerio mail tools: creates Tools/kerio_mail/.venv, upgrades pip, installs requirements.txt,
  then pip install -e . (editable kerio-mail-read package).

  Uses Python 3.12 explicitly (py -3.12 on Windows). Install 3.12 and ensure the launcher is on PATH.
#>
$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Venv = Join-Path $ScriptDir '.venv'

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3.12 -m venv $Venv
}
elseif (Get-Command python3.12 -ErrorAction SilentlyContinue) {
    & python3.12 -m venv $Venv
}
else {
    throw "Python 3.12 not found. Install Python 3.12 and ensure 'py -3.12' works, or add python3.12.exe to PATH."
}
if ($LASTEXITCODE -ne 0) {
    throw "python -m venv failed with exit code $LASTEXITCODE."
}

$pyExe = Join-Path $Venv 'Scripts\python.exe'
$req = Join-Path $ScriptDir 'requirements.txt'
if (-not (Test-Path $req)) {
    throw "requirements.txt not found: $req"
}

# Use python -m pip (reliable on Windows; direct pip.exe can fail when upgrading itself)
& $pyExe -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "pip install --upgrade pip failed with exit code $LASTEXITCODE."
}

& $pyExe -m pip install -r $req
if ($LASTEXITCODE -ne 0) {
    throw "pip install -r requirements.txt failed with exit code $LASTEXITCODE."
}

Push-Location $ScriptDir
try {
    & $pyExe -m pip install -e .
    if ($LASTEXITCODE -ne 0) {
        throw "pip install -e . failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

Write-Host 'Virtual environment created; kerio-mail-read installed in editable mode.'
Write-Host 'Optional dev deps: pip install -r requirements-dev.txt'
Write-Host "Activate in PowerShell: . `"$ScriptDir\venv_activate.ps1`""
Write-Host "Activate in cmd.exe:     $ScriptDir\venv_activate.bat"
