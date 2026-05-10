#!/usr/bin/env bash
# note: on Windows claude is using git bash!

# powershell.exe -NoProfile -File ~/.claude/statusline.ps1

json=$(cat)

if [ -z "$json" ]; then
  printf '...'
  exit 0
fi

py_script="
import sys, json, re

try:
    data = json.load(sys.stdin)
except:
    data = {}

def get(d, *keys):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d

parts = []

cwd = get(data, 'cwd')
if cwd is not None:
    segs = [s for s in re.split(r'[/\\\\]', cwd) if s]
    parts.append(('.../' + '/'.join(segs[-4:])) if len(segs) > 4 else '/'.join(segs))

model = get(data, 'model', 'display_name')
if model is not None:
    parts.append(model)

effort = get(data, 'effort', 'level')
if effort is not None:
    parts.append('effort:' + str(effort))

thinking = get(data, 'thinking', 'enabled')
if thinking is not None:
    parts.append('think:on' if thinking else 'think:off')

fast = get(data, 'fast_mode')
if fast is not None:
    parts.append('fast:on' if fast else 'fast:off')

cost = get(data, 'cost', 'total_cost_usd')
if cost is not None:
    parts.append('\$' + str(round(cost, 2)))

used = get(data, 'context_window', 'used_percentage')
if used is not None:
    parts.append('ctx:' + str(round(used)) + '%')

five = get(data, 'rate_limits', 'five_hour', 'used_percentage')
five_reset = get(data, 'rate_limits', 'five_hour', 'resets_at')
if five is not None:
    five_str = '5h:' + str(round(five)) + '%'
    if five_reset is not None:
        try:
            from datetime import datetime, timezone as tz
            secs = int(five_reset - datetime.now(tz.utc).timestamp())
            if secs > 0:
                h, rem = divmod(secs, 3600)
                m = rem // 60
                five_str += '/' + (str(h) + 'h' + str(m) + 'm' if h > 0 else str(m) + 'm')
        except:
            pass
    parts.append(five_str)

week = get(data, 'rate_limits', 'seven_day', 'used_percentage')
week_reset = get(data, 'rate_limits', 'seven_day', 'resets_at')
if week is not None:
    week_str = '7d:' + str(round(week)) + '%'
    if week_reset is not None:
        try:
            from datetime import datetime, timezone as tz
            secs7 = int(week_reset - datetime.now(tz.utc).timestamp())
            if secs7 > 0:
                d, rem = divmod(secs7, 86400)
                h = rem // 3600
                week_str += '/' + (str(d) + 'd' + str(h) + 'h' if d > 0 else str(h) + 'h')
        except:
            pass
    parts.append(week_str)

print('  '.join(parts) if parts else '...', end='')
"

if command -v jq &>/dev/null; then
  out=$(printf '%s' "$json" | jq -r '
    [
      (if .cwd then
        (.cwd | gsub("\\\\"; "/") | split("/") | map(select(. != ""))) as $parts |
        if ($parts | length) > 4 then ".../" + ($parts[-4:] | join("/"))
        else $parts | join("/") end
      else empty end),
      (.model.display_name // empty),
      (if .effort.level then "effort:\(.effort.level)" else empty end),
      (if .thinking.enabled != null then (if .thinking.enabled then "think:on" else "think:off" end) else empty end),
      (if .fast_mode != null then (if .fast_mode then "fast:on" else "fast:off" end) else empty end),
      (if .cost.total_cost_usd != null then "$\((.cost.total_cost_usd * 100 | round) / 100)" else empty end),
      (if .context_window.used_percentage != null then "ctx:\(.context_window.used_percentage | round)%" else empty end),
      (if .rate_limits.five_hour.used_percentage != null then
        (.rate_limits.five_hour.used_percentage | round | tostring) as $pct |
        (if .rate_limits.five_hour.resets_at != null then
          ((.rate_limits.five_hour.resets_at - now) | floor) as $secs |
          if $secs > 0 then
            "/" + (if ($secs / 3600 | floor) > 0 then "\($secs / 3600 | floor)h\(($secs % 3600 / 60) | floor)m" else "\(($secs % 3600 / 60) | floor)m" end)
          else "" end
        else "" end) as $rem |
        "5h:\($pct)%\($rem)"
      else empty end),
      (if .rate_limits.seven_day.used_percentage != null then
        (.rate_limits.seven_day.used_percentage | round | tostring) as $pct |
        (if .rate_limits.seven_day.resets_at != null then
          ((.rate_limits.seven_day.resets_at - now) | floor) as $secs |
          if $secs > 0 then
            "/" + (if ($secs / 86400 | floor) > 0 then "\($secs / 86400 | floor)d\(($secs % 86400 / 3600) | floor)h" else "\(($secs % 86400 / 3600) | floor)h" end)
          else "" end
        else "" end) as $rem |
        "7d:\($pct)%\($rem)"
      else empty end)
    ] | map(select(. != null and . != "")) | if length > 0 then join("  ") else "..." end
  ')
elif command -v python3 &>/dev/null; then
  out=$(printf '%s' "$json" | python3 -c "$py_script")
elif command -v python &>/dev/null; then
  out=$(printf '%s' "$json" | python -c "$py_script")
else
  out=$(printf '%s' "$json" | powershell.exe -NoProfile -File ~/.claude/statusline.ps1)
fi

printf '%s' "${out:-...}"
