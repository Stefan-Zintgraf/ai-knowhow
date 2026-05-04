#Requires -Version 5.1
<#
.SYNOPSIS
  Deactivates the Kerio mail tools venv in PowerShell (if Activate.ps1 was used).

  Dot-source for consistency:
    . .\venv_deactivate.ps1
#>
if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}
else {
    Write-Warning 'No venv appears active (deactivate not defined). Nothing to do.'
}
