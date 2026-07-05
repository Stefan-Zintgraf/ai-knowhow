# Use-case cap — hard-stop hook

The **use-case cap** (see [`GLOSSARY.md`](GLOSSARY.md)) is enforced by a second `UserPromptSubmit` hook, `usecase-cap.sh`, alongside the scope-steer hook. Where scope-steering only *re-injects text*, this hook is a **hard gate**: on reaching the cap it exits with code **2**, which makes Claude Code **discard the human's prompt** (the model never sees it) and show the hook's message to the user.

Two properties make it robust:

- **The hook counts, not the model.** Every turn it counts `UC…` lines in the `.wip.md` on disk and subtracts a **baseline** (the count when this sitting began); `delta = current − baseline` = use-cases added *this sitting*.
- **Session-scoped lock.** When the cap is hit the hook writes the current `session_id` to a lock file and blocks every further prompt *in that session*. After `/clear`, the new session has a different id: its first prompt passes (the lock is stale and dropped), the skill resets the baseline, and enforcement resumes from the next turn.

## Files (all in `$CLAUDE_PROJECT_DIR`, local state — gitignore them)

- `brainstorm_usecase_cap.state` — written by the skill: two lines, `WIP=<abs path to the .wip.md>` and `BASELINE=<use-case count at sitting start>`.
- `brainstorm_usecase_cap.lock` — written by the hook: the `session_id` frozen at the cap. Absent = not capped.
- Gated on the shared `brainstorm_scope_boundary_on.md` flag (a brainstorm session is active) and on `config.md` (`max_new_use_cases` set and numeric). Cap off or state missing → the hook is silent (fails open).

## The skill's responsibilities

- **At sitting start (session start AND every resume):** after the `.wip.md` path is settled, write `brainstorm_usecase_cap.state` with `WIP` and `BASELINE` = the current count of `UC…` lines in that file (0 for a brand-new file). This reset is what gives each sitting a fresh budget. On resume this is the **first thing to do**, before generating — the hook gives a fresh session exactly one free prompt to reset the baseline before it starts counting again.
- **On the warn turn / at the cap:** the hook prints an advance-notice steer inside the warn window; when you add the use-case that reaches the cap, write the `## Resume notes` and follow the Pause flow *before* stopping, so the pause is graceful. If you don't, the next prompt is hard-blocked anyway and resume reconstructs from the `.wip.md`.

## Verify (at session start, right after writing the state file)

- **A — registration.** Read `$CLAUDE_PROJECT_DIR/.claude/settings.json` and confirm a `UserPromptSubmit` entry whose command references `usecase-cap.sh`. Absent → the cap isn't enforced in this repo (fresh clones may lack it); fall back to inline self-discipline and tell the user.
- **B — self-test.** With the flag on, a state file whose `BASELINE` is far below the current `UC` count (so `delta ≥ max`), and a dummy `session_id`, confirm the hook exits 2:

  ```bash
  echo '{"session_id":"selftest"}' | \
    CLAUDE_PROJECT_DIR="$CLAUDE_PROJECT_DIR" \
    bash "$CLAUDE_PROJECT_DIR/.claude/skills/brainstorm-vision/usecase-cap.sh"; echo "exit=$?"
  ```

  Remove the `brainstorm_usecase_cap.lock` the self-test writes afterwards.

On a failed check, name it, note the session still enforces the cap inline (just without the hard gate), and ask whether to continue or fix the hook first.
