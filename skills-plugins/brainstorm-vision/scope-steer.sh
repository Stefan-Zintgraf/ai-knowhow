#!/usr/bin/env bash
#
# UserPromptSubmit hook: re-inject the AI-Mail brainstorm scope steer on every
# prompt, so it never fades from context over a long session.
#
# Gated by a flag file in the repo root. The flag is always present and toggled
# by RENAMING it:
#   brainstorm_scope_boundary_off.md  -> steer OFF (default resting state)
#   brainstorm_scope_boundary_on.md   -> steer ON
# This hook stays silent unless the `_on` variant exists.
#
# For UserPromptSubmit, stdout from an exit-0 hook is added to the model's
# context — so we just print the steer text; no JSON needed.

set -euo pipefail

# The flag is per-repo local state, in the current submodule's root.
FLAG="$CLAUDE_PROJECT_DIR/brainstorm_scope_boundary_on.md"
# The steer text lives next to this script (the skill's canonical home),
# reached via the .claude/skills junction — resolve it relative to ourselves.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STEER="$SCRIPT_DIR/scope_boundary.md"

# Drain the hook's JSON payload on stdin; we don't need it.
cat >/dev/null 2>&1 || true

# Gate: stay silent unless a brainstorm session is active and the steer exists.
[ -f "$FLAG" ]  || exit 0
[ -f "$STEER" ] || exit 0

cat "$STEER"
