<#
.SYNOPSIS
  Sends a WhatsApp message via the local whatsapp_client HTTP API.

.DESCRIPTION
  Calls POST /send with JSON body. API key: -ApiKey, then env WHATSAPP_SENDER_API_KEY, then API_KEY from .env next to this script.

.EXAMPLE
  .\send-whatsapp.ps1 -Number "4915111111111" -Message "Hello"

.EXAMPLE
  .\send-whatsapp.ps1 -Number "4915111111111" -Message "Hi" -BaseUrl "http://127.0.0.1:3000" -ApiKey "your-key"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string] $Number,

    [Parameter(Mandatory = $false)]
    [string] $Message,

    [Parameter(Mandatory = $false)]
    [string] $BaseUrl = "http://127.0.0.1:3000",

    [Parameter(Mandatory = $false)]
    [string] $ApiKey = $env:WHATSAPP_SENDER_API_KEY
)

function Get-DotEnvValue {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path,
        [Parameter(Mandatory = $true)]
        [string] $Key
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }
    foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
        $t = $line.Trim()
        if ($t -eq '' -or $t.StartsWith('#')) {
            continue
        }
        if ($t -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
            $k = $Matches[1]
            if ($k -ne $Key) {
                continue
            }
            $v = $Matches[2].Trim()
            if (
                ($v.Length -ge 2 -and $v.StartsWith('"') -and $v.EndsWith('"')) -or
                ($v.Length -ge 2 -and $v.StartsWith("'") -and $v.EndsWith("'"))
            ) {
                $v = $v.Substring(1, $v.Length - 2)
            }
            return $v
        }
    }
    return $null
}

function Show-Usage {
    Write-Host @"
Send a WhatsApp message through the whatsapp_client REST API.

Usage:
  .\send-whatsapp.ps1 -Number <digits-only> -Message <text> [-BaseUrl <url>] [-ApiKey <key>]

Parameters:
  -Number   Target phone number, digits only (no +), 7-15 digits, must be in ALLOWED_NUMBERS.
  -Message  Message body to send.
  -BaseUrl  API root URL (default: http://127.0.0.1:3000).
  -ApiKey   Value for x-api-key header. If omitted: WHATSAPP_SENDER_API_KEY, then API_KEY from .env in this script folder.

Prerequisites:
  - whatsapp_client is running (node index.js).
  - .env has API_KEY and the target number is in ALLOWED_NUMBERS.

Example:
  .\send-whatsapp.ps1 -Number '4915111111111' -Message 'Hello from PowerShell!'
"@
}

if ([string]::IsNullOrWhiteSpace($Number) -or [string]::IsNullOrWhiteSpace($Message)) {
    Show-Usage
    exit 1
}

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
    $envFile = Join-Path $PSScriptRoot '.env'
    $fromEnvFile = Get-DotEnvValue -Path $envFile -Key 'API_KEY'
    if (-not [string]::IsNullOrWhiteSpace($fromEnvFile)) {
        $ApiKey = $fromEnvFile
    }
}

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
    Write-Error "Missing API key. Pass -ApiKey, set WHATSAPP_SENDER_API_KEY, or set API_KEY in .env next to this script ($PSScriptRoot\.env)."
    exit 1
}

$uri = $BaseUrl.TrimEnd('/') + '/send'
$payload = @{
    number  = $Number.Trim()
    message = $Message
} | ConvertTo-Json -Compress

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Body $payload `
        -ContentType 'application/json; charset=utf-8' `
        -Headers @{ 'x-api-key' = $ApiKey }
    if ($response.success) {
        Write-Host "OK: message queued/sent (success=true)."
    } else {
        Write-Warning "API returned success=false: $($response | ConvertTo-Json -Compress)"
        exit 1
    }
} catch {
    $err = $_.Exception.Message
    if ($_.ErrorDetails -and $_.ErrorDetails.Message) {
        $err = $_.ErrorDetails.Message
    }
    Write-Error "Request failed: $err"
    exit 1
}
