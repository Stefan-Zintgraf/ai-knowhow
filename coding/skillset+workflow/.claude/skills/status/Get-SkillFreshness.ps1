param(
    [string]$RepoRoot = ".",
    [Parameter(Mandatory)]
    [string]$SkillsJson
)

$ErrorActionPreference = "Stop"

function Get-LastCommit {
    param([string]$RelPath, [string]$Root)
    $out = & git -C $Root log -1 --format="%aI" -- $RelPath 2>$null
    if ($LASTEXITCODE -ne 0) { return $null }
    $out = ($out -join "").Trim()
    if ([string]::IsNullOrEmpty($out)) { return $null }
    return [datetimeoffset]::Parse($out)
}

$skills = $SkillsJson | ConvertFrom-Json
$results = [System.Collections.ArrayList]@()

foreach ($skill in $skills) {
    $name      = $skill.name
    $id        = $skill.id
    $sourceDocs = @($skill.source_docs)

    $sourceLatest = $null
    foreach ($doc in $sourceDocs) {
        $t = Get-LastCommit $doc.Replace('\','/') $RepoRoot
        if ($null -ne $t -and ($null -eq $sourceLatest -or $t -gt $sourceLatest)) {
            $sourceLatest = $t
        }
    }

    $compiledRel = "skills/output/$name.md"
    $inputRel    = "skills/input/$name-in.md"

    $compiledExists = Test-Path (Join-Path $RepoRoot $compiledRel)
    $inputExists    = Test-Path (Join-Path $RepoRoot $inputRel)

    $compiledLatest = if ($compiledExists) { Get-LastCommit $compiledRel $RepoRoot } else { $null }
    $inputLatest    = if ($inputExists)    { Get-LastCommit $inputRel    $RepoRoot } else { $null }

    $staleCompiled = $false
    $staleInput    = $false
    $cmd      = $null
    $cmdInput = $null

    if ($null -ne $sourceLatest) {
        $staleCompiled = (-not $compiledExists) -or ($null -eq $compiledLatest) -or ($sourceLatest -gt $compiledLatest)
        $staleInput    = (-not $inputExists)    -or ($null -eq $inputLatest)    -or ($sourceLatest -gt $inputLatest)
        if ($staleCompiled -and -not $staleInput) { $cmd      = "/make-skill $name" }
        if ($staleInput)                          { $cmdInput = "/draft-skill-input $name" }
    }

    [void]$results.Add([ordered]@{
        id                   = $id
        name                 = $name
        compiled_exists      = $compiledExists
        input_exists         = $inputExists
        source_last_commit   = if ($null -ne $sourceLatest)   { $sourceLatest.ToString("o")   } else { $null }
        input_last_commit    = if ($null -ne $inputLatest)    { $inputLatest.ToString("o")    } else { $null }
        compiled_last_commit = if ($null -ne $compiledLatest) { $compiledLatest.ToString("o") } else { $null }
        stale_compiled       = $staleCompiled
        stale_input          = $staleInput
        cmd                  = $cmd
        cmd_input            = $cmdInput
    })
}

$anyStale = ($results | Where-Object { $_.stale_compiled -or $_.stale_input }).Count -gt 0

@{
    skills    = $results.ToArray()
    any_stale = [bool]$anyStale
} | ConvertTo-Json -Depth 5
