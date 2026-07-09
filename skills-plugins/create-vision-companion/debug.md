# Stepping mode (debug)

A debugging aid layered *over* the normal workflow; it changes nothing else. Activate it when the user asks to run with debugging/stepping, and record `debug: on` in the bundle's `_status.md` (absence means off - run state lives in the bundle, never in the skill's own files).

While active, the AFK rule is *suspended*: after **every** phase completes (its draft, its critic pass, and its `_status.md` update - i.e. the phase is a clean checkpoint), **halt and surface** to the human:

1. State which phase just finished, the file(s) it wrote, and any residuals it logged to `decisions.md`.
2. Ask the human exactly this choice before continuing:
   - **Continue, keep debugging on** - proceed to the next phase, then halt again after it.
   - **Continue, turn debugging off** - set `debug: off` in `_status.md`, then run the remaining phases straight through to Phase 12 with no further per-phase halts (the Phase 11 human review still applies).
   - **Stop here** - pause the build (follow Pause and resume in `SKILL.md`).
3. Only act after the human answers. Turning debugging off mid-run takes effect immediately - the *next* phase and all after it run without halting.

Hard blockers (Phase 0) and the Phase 11 human review still apply regardless of the flag. The per-phase halt is *in addition to* those, not a replacement.
