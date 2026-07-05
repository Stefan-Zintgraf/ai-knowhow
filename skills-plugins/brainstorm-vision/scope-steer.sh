#!/usr/bin/env bash
#
# UserPromptSubmit hook: re-inject the brainstorm scope steer on every
# prompt, so it never fades from context over a long session.
#
# Gated by a flag file in the repo root. The flag is always present and toggled
# by RENAMING it:
#   brainstorm_scope_boundary_off.md  -> steer OFF (default resting state)
#   brainstorm_scope_boundary_on.md   -> steer ON
# This hook stays silent unless the `_on` variant exists.
#
# The steer text is a STATIC template (scope_boundary.md) with an `{{ANCHOR}}`
# placeholder. The current anchor is NOT baked into any skill file — it is read
# live, every turn, from the session's `.wip.md` `## Vision scope`. A scope
# climb updates the `.wip.md` (the single source of truth) and needs no change
# to anything in the skill folder.
#
# For UserPromptSubmit, stdout from an exit-0 hook is added to the model's
# context — so we just print the steer text; no JSON needed.

set -euo pipefail

# The flag is per-repo local state, in the current submodule's root.
FLAG="$CLAUDE_PROJECT_DIR/brainstorm_scope_boundary_on.md"
# The steer template lives next to this script (the skill's canonical home),
# reached via the .claude/skills junction — resolve it relative to ourselves.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$SCRIPT_DIR/scope_boundary.md"

# Drain the hook's JSON payload on stdin; we don't need it.
cat >/dev/null 2>&1 || true

# Gate: stay silent unless a brainstorm session is active and the template exists.
[ -f "$FLAG" ]     || exit 0
[ -f "$TEMPLATE" ] || exit 0

# --- locate the session's .wip.md -------------------------------------------
# Primary: the path the use-case-cap state file records (exact, when a cap is
# configured). Fallback: the newest *.wip.md under docs/brainstorming/.
WIP=""
STATE="$CLAUDE_PROJECT_DIR/brainstorm_usecase_cap.state"
if [ -f "$STATE" ]; then
  WIP="$(sed -n 's/^WIP=//p' "$STATE" | head -n1)"
fi
if [ -z "$WIP" ] || [ ! -f "$WIP" ]; then
  WIP="$(ls -t "$CLAUDE_PROJECT_DIR"/docs/brainstorming/*.wip.md 2>/dev/null | head -n1 || true)"
fi

# --- derive the anchor line from `## Vision scope` --------------------------
# The anchor is the last `- **S<n>.**` bullet (climb order = concrete → anchor,
# so the highest rung IS the anchor). Fold its wrapped continuation lines into
# one and strip the trailing *(anchor)* tag.
ANCHOR=""
if [ -n "$WIP" ] && [ -f "$WIP" ]; then
  ANCHOR="$(awk '
    /^##[[:space:]]+Vision scope/ { inscope=1; next }
    inscope && /^##[[:space:]]/   { inscope=0 }
    !inscope { next }
    /^-[[:space:]]+\*\*S[0-9]+\./ {              # a scope bullet begins
      if (buf != "") last=buf
      buf=$0; next
    }
    buf != "" && /^[[:space:]]+[^[:space:]]/ {   # indented continuation
      sub(/^[[:space:]]+/, " "); buf=buf $0; next
    }
    buf != "" { last=buf; buf="" }               # any other line ends the bullet
    END { if (buf != "") last=buf; print last }
  ' "$WIP")"
fi

if [ -n "$ANCHOR" ]; then
  SN="$(printf '%s' "$ANCHOR" | sed -n 's/^-[[:space:]]*\*\*\(S[0-9]\+\)\..*/\1/p')"
  TEXT="$(printf '%s' "$ANCHOR" \
    | sed -E 's/^-[[:space:]]*\*\*S[0-9]+\.\*\*[[:space:]]*//' \
    | sed -E 's/\*\(anchor\)\*//g' \
    | sed -E 's/[[:space:]]+/ /g; s/^[[:space:]]+//; s/[[:space:]]+$//')"
  REPLACE="\`$SN\` — $TEXT"
else
  # Couldn't find or parse the anchor — degrade gracefully so steering still
  # fires; point the model at the source of truth instead of a stale value.
  REPLACE="see \`## Vision scope\` in the working \`.wip.md\`."
fi

# --- emit the template with the placeholder filled in -----------------------
# Bash parameter-expansion replace: does not treat & or \ in $REPLACE specially.
TEMPLATE_TEXT="$(cat "$TEMPLATE")"
printf '%s\n' "${TEMPLATE_TEXT//\{\{ANCHOR\}\}/$REPLACE}"
