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

# --- Rule-skill map ---
$mapRel    = "skills/rule_skill_map.md"
$mapExists = Test-Path (Join-Path $RepoRoot $mapRel)
$mapLatest = if ($mapExists) { Get-LastCommit $mapRel $RepoRoot } else { $null }

$grDir   = Join-Path $RepoRoot "gr"
$grFiles = Get-ChildItem $grDir -Filter "*.md" -ErrorAction SilentlyContinue
$grLatest = $null
foreach ($f in $grFiles) {
    $t = Get-LastCommit ("gr/" + $f.Name) $RepoRoot
    if ($null -ne $t -and ($null -eq $grLatest -or $t -gt $grLatest)) { $grLatest = $t }
}

$mapStale = $false
if ($null -ne $grLatest) {
    $mapStale = (-not $mapExists) -or ($null -eq $mapLatest) -or ($grLatest -gt $mapLatest)
}

$ruleSkillMap = [ordered]@{
    exists           = $mapExists
    stale            = $mapStale
    map_last_commit  = if ($null -ne $mapLatest) { $mapLatest.ToString("o") } else { $null }
    gr_latest_commit = if ($null -ne $grLatest)  { $grLatest.ToString("o")  } else { $null }
    cmd              = if ($mapStale) { "/update-rule-skill-map" } else { $null }
}

# --- Build source_last_commit map from SkillsJson ---
$sourceMap = @{}
foreach ($skill in $skills) {
    $sourceLatest = $null
    foreach ($doc in @($skill.source_docs)) {
        $t = Get-LastCommit $doc.Replace('\','/') $RepoRoot
        if ($null -ne $t -and ($null -eq $sourceLatest -or $t -gt $sourceLatest)) { $sourceLatest = $t }
    }
    $sourceMap[$skill.name] = $sourceLatest
}

# --- Test fixtures ---
$testBaseDir = Join-Path $RepoRoot "skills/test"
$testDirs    = Get-ChildItem $testBaseDir -Directory -ErrorAction SilentlyContinue
$testFixtures = [System.Collections.ArrayList]@()

foreach ($dir in $testDirs) {
    $skillName     = $dir.Name
    $compiledRel   = "skills/output/$skillName.md"
    $compiledExists = Test-Path (Join-Path $RepoRoot $compiledRel)

    $fixtureFiles  = Get-ChildItem $dir.FullName -File -ErrorAction SilentlyContinue
    $fixturesExist = ($fixtureFiles.Count -gt 0)

    $fixturesLatest = $null
    foreach ($f in $fixtureFiles) {
        $t = Get-LastCommit ("skills/test/$skillName/" + $f.Name) $RepoRoot
        if ($null -ne $t -and ($null -eq $fixturesLatest -or $t -gt $fixturesLatest)) { $fixturesLatest = $t }
    }

    $sourceLatest = if ($sourceMap.ContainsKey($skillName)) { $sourceMap[$skillName] } else { $null }

    $sourceNewerThanFixtures = $null
    if ($null -ne $sourceLatest -and $fixturesExist) {
        $sourceNewerThanFixtures = ($null -eq $fixturesLatest) -or ($sourceLatest -gt $fixturesLatest)
    }

    $entry = [ordered]@{
        name                      = $skillName
        fixtures_exist            = $fixturesExist
        compiled_exists           = $compiledExists
        source_newer_than_fixtures = $sourceNewerThanFixtures
        fixtures_last_commit      = if ($null -ne $fixturesLatest) { $fixturesLatest.ToString("o") } else { $null }
    }

    if ($fixturesExist -and -not $compiledExists) {
        $entry['cmd_compile'] = "skill not compiled"
    } elseif ($fixturesExist -and $sourceNewerThanFixtures -eq $true) {
        $entry['cmd'] = "/draft-skill-tests $skillName"
    }

    [void]$testFixtures.Add($entry)
}

@{
    rule_skill_map = $ruleSkillMap
    test_fixtures  = $testFixtures.ToArray()
} | ConvertTo-Json -Depth 5
