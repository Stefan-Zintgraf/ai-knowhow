param(
    [string]$RepoRoot = ".",
    [Parameter(Mandatory)]
    [string]$ActiveWIJson,
    [Parameter(Mandatory)]
    [string]$FreshnessJson,
    [Parameter(Mandatory)]
    [string]$MapTestJson
)

$ErrorActionPreference = "Stop"

$activeWI  = $ActiveWIJson  | ConvertFrom-Json
$freshness = $FreshnessJson | ConvertFrom-Json
$mapTest   = $MapTestJson   | ConvertFrom-Json

$actions = [System.Collections.ArrayList]@()

# Priority 1: tripwire_halt set
if ($activeWI.found -and $activeWI.tripwire_halt -eq $true) {
    [void]$actions.Add([ordered]@{
        priority = 1
        reason   = "tripwire_halt is set"
        cmd      = "/triage-idea --remode"
    })
}

# Priority 2: stale rule-skill map
if ($mapTest.rule_skill_map.stale -eq $true) {
    [void]$actions.Add([ordered]@{
        priority = 2
        reason   = "rule-skill map is stale"
        cmd      = "/update-rule-skill-map"
    })
}

# Priority 3: stale skill inputs
foreach ($skill in $freshness.skills) {
    if ($skill.stale_input -eq $true) {
        [void]$actions.Add([ordered]@{
            priority = 3
            reason   = "skill input stale: $($skill.name)"
            cmd      = "/draft-skill-input $($skill.name)"
        })
    }
}

# Priority 4: stale compiled (input fresh)
foreach ($skill in $freshness.skills) {
    if ($skill.stale_compiled -eq $true -and $skill.stale_input -ne $true) {
        [void]$actions.Add([ordered]@{
            priority = 4
            reason   = "compiled skill stale: $($skill.name)"
            cmd      = "/make-skill $($skill.name)"
        })
    }
}

$fallbackNextTodo = $null

# Priority 5: all current — find first unchecked item in work items section
if ($actions.Count -eq 0) {
    $planPath = Join-Path $RepoRoot "coding_plan.md"
    if (Test-Path $planPath) {
        $planLines = Get-Content $planPath
        $inWorkItems = $false
        foreach ($line in $planLines) {
            if ($line -match '^### work items') {
                $inWorkItems = $true
                continue
            }
            if ($inWorkItems -and $line -match '^#{1,4} ') { break }
            if ($inWorkItems -and $line -match '^\- \[ \] (.+)$') {
                $fallbackNextTodo = $Matches[1].Trim()
                break
            }
        }
        if ($null -eq $fallbackNextTodo) {
            $fallbackNextTodo = "all work items complete"
        }
        [void]$actions.Add([ordered]@{
            priority = 5
            reason   = "all skills current"
            cmd      = $fallbackNextTodo
        })
    }
}

$topAction = if ($actions.Count -gt 0) { $actions[0] } else { $null }

@{
    actions           = $actions.ToArray()
    top_action        = $topAction
    fallback_next_todo = $fallbackNextTodo
} | ConvertTo-Json -Depth 5
