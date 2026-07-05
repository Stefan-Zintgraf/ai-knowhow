# Scope-steering hook

Some repos ship a `UserPromptSubmit` hook that re-injects the scope boundary every turn so it never fades over a long session. The steer text is a **static template** (`scope_boundary.md`); the hook fills its anchor placeholder each turn by reading the current **anchor** live from the session's `.wip.md` `## Vision scope`. So a scope **climb** touches only the `.wip.md` — **nothing in the skill folder ever changes when the scope changes.** It is gated by a flag file in the **current git submodule's root** (`$CLAUDE_PROJECT_DIR`), toggled by renaming:

- `brainstorm_scope_boundary_on.md` → steering ON
- `brainstorm_scope_boundary_off.md` → steering OFF (resting state)

**At session start**, ensure steering is ON in `$CLAUDE_PROJECT_DIR`:

- if `brainstorm_scope_boundary_off.md` exists → rename it to `brainstorm_scope_boundary_on.md`;
- else if neither exists → create `brainstorm_scope_boundary_on.md` (contents irrelevant; only its existence matters).

**Verify (right after turning ON, at session start).** Run these checks autonomously — no need to ask the user unless one fails:

- **A — registration (static).** Read `$CLAUDE_PROJECT_DIR/.claude/settings.json` and confirm a `UserPromptSubmit` entry whose command references `scope-steer.sh`. Absent → the hook isn't installed in this repo (fresh clones may lack it).
- **B — script self-test (dynamic).** With the flag ON, run the script once with empty stdin and confirm it emits the steer (non-empty stdout containing the sentinel `DIVERGENT vision session`):

  ```bash
  CLAUDE_PROJECT_DIR="$CLAUDE_PROJECT_DIR" \
    bash "$CLAUDE_PROJECT_DIR/.claude/skills/brainstorm-vision/scope-steer.sh" </dev/null
  ```

  Empty output or an error → the script, its path, or `scope_boundary.md` is broken. The output should carry a resolved **Anchor (current scope):** line and contain **no** literal `{{ANCHOR}}` placeholder — if the placeholder survives, the hook couldn't locate the `.wip.md` (it will still fire, pointing the model at `## Vision scope` as a fallback).
- **C — live firing (next turn, best-effort).** A and B prove the wiring is correct on disk, but the *running* session only loads hooks at startup — if settings.json was edited after launch, it won't fire until a restart. So on the user's **first reply**, check whether the steer text was actually re-injected into that turn's context. If A+B passed but the steer didn't appear, tell the user the session predates the hook and needs a Claude Code restart.

**On any failed check:** name which check failed, note that this skill still enforces scope discipline inline (so the session is safe — just more exposed to context rot over a long session), and ask whether to **continue anyway** or **fix the hook first**. Don't silently proceed.

**At session end** — and equally when the session is **paused** — rename `brainstorm_scope_boundary_on.md` back to `brainstorm_scope_boundary_off.md` so steering doesn't bleed into unrelated work. **Resuming** a paused session re-runs the same start logic, turning it back ON.
