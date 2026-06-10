param(
    [string]$RepoRoot = ".",
    [string]$ArtifactsRoot = "plan"
)

$ErrorActionPreference = "Stop"

function Out-Result($hash) {
    $hash | ConvertTo-Json -Compress
}

$activePath = Join-Path $RepoRoot "$ArtifactsRoot/ACTIVE"

if (-not (Test-Path $activePath)) {
    Out-Result @{ found = $false; wi = $null; current_phase = $null; phase_status = $null; mode = $null; blockers = @(); tripwire_halt = $false; entered_at = $null; last_actor = $null; error = "no_active_file" }
    exit 0
}

$wi = (Get-Content $activePath -Raw).Trim()

if ($wi -eq "<none>" -or $wi -eq "") {
    Out-Result @{ found = $false; wi = $null; current_phase = $null; phase_status = $null; mode = $null; blockers = @(); tripwire_halt = $false; entered_at = $null; last_actor = $null; error = $null }
    exit 0
}

$phaseStatusPath = Join-Path $RepoRoot "$ArtifactsRoot/$wi/phase_status.md"

if (-not (Test-Path $phaseStatusPath)) {
    Out-Result @{ found = $true; wi = $wi; current_phase = $null; phase_status = $null; mode = $null; blockers = @(); tripwire_halt = $false; entered_at = $null; last_actor = $null; error = "phase_status_missing" }
    exit 0
}

$lines = Get-Content $phaseStatusPath
$inFrontmatter = $false
$fenceCount = 0
$yamlLines = @()

foreach ($line in $lines) {
    if ($line.Trim() -eq "---") {
        $fenceCount++
        if ($fenceCount -eq 1) { $inFrontmatter = $true; continue }
        if ($fenceCount -eq 2) { $inFrontmatter = $false; break }
    }
    if ($inFrontmatter) { $yamlLines += $line }
}

if ($fenceCount -lt 2) {
    Out-Result @{ found = $true; wi = $wi; current_phase = $null; phase_status = $null; mode = $null; blockers = @(); tripwire_halt = $false; entered_at = $null; last_actor = $null; error = "yaml_parse_error: no frontmatter fences found" }
    exit 0
}

$result = [ordered]@{
    found         = $true
    wi            = $wi
    current_phase = $null
    phase_status  = $null
    mode          = $null
    blockers      = @()
    tripwire_halt = $false
    entered_at    = $null
    last_actor    = $null
    error         = $null
}

$inBlockers = $false
$blockersArr = [System.Collections.ArrayList]@()

foreach ($line in $yamlLines) {
    if ($line -match '^(\w[\w_]*):\s*(.*)$') {
        $key = $Matches[1]
        $val = $Matches[2].Trim()
        $inBlockers = $false
        switch ($key) {
            'current_phase' { $result['current_phase'] = if ($val -eq '') { $null } else { $val } }
            'phase_status'  { $result['phase_status']  = $val }
            'mode'          { $result['mode']           = $val }
            'tripwire_halt' { $result['tripwire_halt']  = ($val -eq 'true') }
            'entered_at'    { $result['entered_at']     = $val }
            'last_actor'    { $result['last_actor']     = $val }
            'blockers' {
                if ($val -eq '' -or $val -eq '[]') {
                    $result['blockers'] = @()
                } else {
                    $inBlockers = $true
                }
            }
        }
    } elseif ($inBlockers -and $line -match '^\s*-\s*(.+)$') {
        [void]$blockersArr.Add($Matches[1].Trim())
        $result['blockers'] = $blockersArr.ToArray()
    }
}

Out-Result $result
