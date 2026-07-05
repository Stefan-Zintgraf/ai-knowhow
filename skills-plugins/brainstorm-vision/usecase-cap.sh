#!/usr/bin/env bash
#
# UserPromptSubmit hook: enforce the brainstorm-vision use-case cap.
#
# Unlike scope-steer.sh (which only re-injects advisory text), this hook is a
# HARD GATE. When the number of use-cases newly added in the current sitting
# reaches `max_new_use_cases` (from config.md), it exits 2 — which makes Claude
# Code DISCARD the human's prompt and show our stderr to them. The model never
# sees the prompt, so no amount of "just keep going" gets past it.
#
# The count is computed here from the .wip.md on disk every turn, so it can't
# rot out of the model's context. The baseline (use-case count at the start of
# this sitting) is written by the skill to the state file below; delta =
# current - baseline = use-cases added THIS sitting.
#
# Resume without a deadlock: the lock records the session_id that hit the cap.
# Only that session is blocked. After /clear, a fresh session has a new id, so
# its first prompt (the resume) passes, the skill resets the baseline, and the
# stale lock is cleared. You must start a new sitting to continue.

set -euo pipefail

PROJ="$CLAUDE_PROJECT_DIR"
STATE="$PROJ/brainstorm_usecase_cap.state"   # WIP=<path> / BASELINE=<int>, written by the skill
LOCK="$PROJ/brainstorm_usecase_cap.lock"      # holds the session_id frozen at the cap
FLAG="$PROJ/brainstorm_scope_boundary_on.md"  # "a brainstorm session is active" signal (shared)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$SCRIPT_DIR/config.md"

# --- read the hook payload and pull out the session id ----------------------
INPUT="$(cat 2>/dev/null || true)"
SID="$(printf '%s' "$INPUT" | tr -d '\n' \
  | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"

pause_msg() {
  cat >&2 <<EOF
🛑 brainstorm-vision use-case cap reached — this sitting is paused.

You've added the maximum use-cases configured for one sitting
(max_new_use_cases in the skill's config.md). Further prompts in THIS
session are being ignored on purpose, to force a fresh-context checkpoint.

To continue: /clear (or open a new session) and re-invoke the skill. It will
resume from the .wip.md, reset the per-sitting counter, and let you keep going.
EOF
}

# --- an existing lock takes priority ----------------------------------------
if [ -f "$LOCK" ]; then
  LOCKED_SID="$(cat "$LOCK" 2>/dev/null || true)"
  if [ -n "$SID" ] && [ "$SID" = "$LOCKED_SID" ]; then
    pause_msg
    exit 2                       # same capped session → hard-block every prompt
  fi
  # Different session id = a new sitting starting after /clear. Drop the stale
  # lock and let THIS first prompt through unconditionally — the baseline is
  # still stale, so counting now would just re-block the resume. The skill resets
  # the baseline on its first resume turn; enforcement picks up from the next one.
  rm -f "$LOCK"
  exit 0
fi

# --- gate: only active during a brainstorm session, and only if a cap is set --
[ -f "$FLAG" ]   || exit 0
[ -f "$CONFIG" ] || exit 0
[ -f "$STATE" ]  || exit 0        # no baseline yet → nothing to enforce (fail open)

read_cfg() {  # read_cfg <key> -> trimmed value, comments stripped
  grep -E "^[[:space:]]*$1[[:space:]]*:" "$CONFIG" 2>/dev/null | head -n1 \
    | sed -E "s/^[^:]*:[[:space:]]*//; s/[[:space:]]*#.*$//; s/[[:space:]]*$//"
}

MAX="$(read_cfg max_new_use_cases)"
WARN="$(read_cfg warn_before)"

# Disabled unless MAX is a positive integer.
case "$MAX" in
  ''|off|OFF|Off|0) exit 0 ;;
  *[!0-9]*)         exit 0 ;;    # non-numeric → treat as off
esac
case "$WARN" in *[!0-9]*|'') WARN=0 ;; esac

# --- read the baseline + wip path from state --------------------------------
WIP="$(sed -n 's/^WIP=//p' "$STATE" | head -n1)"
BASELINE="$(sed -n 's/^BASELINE=//p' "$STATE" | head -n1)"
case "$BASELINE" in *[!0-9]*|'') BASELINE=0 ;; esac
[ -n "$WIP" ] && [ -f "$WIP" ] || exit 0   # can't count → fail open

# --- count use-cases in the wip file, compute the delta ---------------------
CUR="$(grep -cE '^[[:space:]]*-[[:space:]]*\*\*UC[0-9]' "$WIP" 2>/dev/null || echo 0)"
DELTA=$(( CUR - BASELINE ))
[ "$DELTA" -lt 0 ] && DELTA=0

if [ "$DELTA" -ge "$MAX" ]; then
  [ -n "$SID" ] && printf '%s' "$SID" > "$LOCK"   # freeze this sitting
  pause_msg
  exit 2
fi

# --- advance notice inside the warn window ----------------------------------
if [ "$WARN" -gt 0 ] && [ "$DELTA" -ge $(( MAX - WARN )) ]; then
  REMAIN=$(( MAX - DELTA ))
  cat <<EOF
[brainstorm-vision] Use-case cap approaching: $DELTA of $MAX use-cases added
this sitting — $REMAIN more and the session will HARD-PAUSE for a fresh-context
checkpoint. Wind down toward a natural stopping point. On the turn you add
use-case number $MAX, first write the ## Resume notes and follow the Pause flow,
then stop — after that, further prompts are blocked until /clear + re-invoke.
EOF
fi

exit 0
