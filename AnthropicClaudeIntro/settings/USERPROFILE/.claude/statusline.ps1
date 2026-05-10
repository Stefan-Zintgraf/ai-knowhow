$json = $null
if ([Console]::IsInputRedirected) {
    try { $json = [Console]::In.ReadToEnd() } catch {}
}

# logging (for debugging)
# $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
# $entry = "[$timestamp]`nargs: $($args -join ' | ')`nstdin: $json`n`n"
# [System.IO.File]::AppendAllText("$env:USERPROFILE\.claude\status.log", $entry)

$model = $null
$thinking = $null
$effort = $null
$cost = $null
$fast = $null
$session = $null
$used = $null
$five = $null
$fiveReset = $null
$week = $null
$weekReset = $null

if ($json) {
    try { $data = $json | ConvertFrom-Json } catch {}
    if ($data) {
        if ($null -ne $data.model.display_name)                    { $model   = $data.model.display_name }
        if ($null -ne $data.thinking.enabled)                      { $thinking = if ($data.thinking.enabled) { "think:on" } else { "think:off" } }
        if ($null -ne $data.effort.level)                          { $effort  = "effort:$($data.effort.level)" }
        if ($null -ne $data.cost.total_cost_usd)                   { $cost    = "$([math]::Round($data.cost.total_cost_usd, 2))" }
        if ($null -ne $data.fast_mode)                             { $fast    = if ($data.fast_mode) { "fast:on" } else { "fast:off" } }
        if ($null -ne $data.cwd) {
            $parts2 = $data.cwd -split '[/\\]' | Where-Object { $_ -ne '' }
            $session = if ($parts2.Count -gt 4) { '.../' + ($parts2[-4..-1] -join '/') } else { $parts2 -join '/' }
        }
        if ($null -ne $data.context_window.used_percentage)        { $used    = [math]::Round($data.context_window.used_percentage) }
        if ($null -ne $data.rate_limits.five_hour.used_percentage) { $five    = [math]::Round($data.rate_limits.five_hour.used_percentage) }
        if ($null -ne $data.rate_limits.seven_day.used_percentage) { $week    = [math]::Round($data.rate_limits.seven_day.used_percentage) }
        if ($null -ne $data.rate_limits.seven_day.resets_at) {
            try {
                $resetAt7 = [DateTimeOffset]::FromUnixTimeSeconds($data.rate_limits.seven_day.resets_at)
                $remaining7 = $resetAt7 - [DateTimeOffset]::UtcNow
                if ($remaining7.TotalHours -gt 0) {
                    $d = [math]::Floor($remaining7.TotalDays)
                    $h = $remaining7.Hours
                    $weekReset = if ($d -gt 0) { "${d}d${h}h" } else { "${h}h" }
                }
            } catch {}
        }
        if ($null -ne $data.rate_limits.five_hour.resets_at) {
            try {
                $resetAt = [DateTimeOffset]::FromUnixTimeSeconds($data.rate_limits.five_hour.resets_at)
                $remaining = $resetAt - [DateTimeOffset]::UtcNow
                if ($remaining.TotalMinutes -gt 0) {
                    $h = [math]::Floor($remaining.TotalHours)
                    $m = $remaining.Minutes
                    $fiveReset = if ($h -gt 0) { "${h}h${m}m" } else { "${m}m" }
                }
            } catch {}
        }
    }
}

$parts = @()
if ($null -ne $session) { $parts += $session }
if ($null -ne $model)   { $parts += $model }
if ($null -ne $effort)  { $parts += $effort }
if ($null -ne $thinking){ $parts += $thinking }
if ($null -ne $fast)    { $parts += $fast }
if ($null -ne $cost)    { $parts += "`$$cost" }
if ($null -ne $used)    { $parts += "ctx:${used}%" }
if ($null -ne $five) {
    $fiveStr = "5h:${five}%"
    if ($null -ne $fiveReset) { $fiveStr += "/${fiveReset}" }
    $parts += $fiveStr
}
if ($null -ne $week) {
    $weekStr = "7d:${week}%"
    if ($null -ne $weekReset) { $weekStr += "/${weekReset}" }
    $parts += $weekStr
}

$out = if ($parts.Count -gt 0) { $parts -join "  " } else { "..." }
[Console]::Out.Write($out)
