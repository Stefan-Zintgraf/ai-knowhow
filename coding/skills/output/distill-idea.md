---
name: distill-idea
description: Distill a raw brief into 3–6 major goals and persist the confirmed list to plan/<WI>/idea.md. Use at the very start of a new work-item.
compiled-against: compile-skill v1.2.0
source: skills/input/distill-idea-in.md
source-sha256: 160f1e413c1fc32325f5859e8725b017989418a038723eecc17a740be931a66a
source-modified: 2026-05-20 10:11
compiled: 2026-05-20 11:02
---

# Skill: distill-idea

This skill distills a raw brief into 3–6 major goals and writes the confirmed list to `plan/<WI>/idea.md`. It does not manage workflow phases, name downstream work, or decide whether anything proceeds.

---

## Steps

1. **Pre-structured-input check.** Heuristically scan the input for a candidate goal list (3–6 outcome-shaped bullets, no detail leakage). If it fires, ask the human: "Input already looks like 3–6 goals: [list]. Treat as the confirmed goal list, or run full distillation?" If the human picks "treat as confirmed," skip to step 6 with that list. Otherwise proceed. If the heuristic does not fire, proceed silently.

2. **Distillation pass.** Read the raw input. Produce a draft list of 3–6 major goals. Each goal names *what the work must serve*, not *how*.

3. **Detail-leak strip.** Remove any goal containing module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or estimates. Append a one-line note per stripped item: "Stripped detail: [item]."

4. **Negative goal capture.** Identify explicit exclusions in the brief ("not a mobile app", "no real-time updates"). Promote them to the goal list as negative goals. They count toward the 3–6 budget when they materially shape the work.

5. **Count gate.** If draft count < 3: report that the brief may be too narrow for goal-shaped framing and return without a goal list (`status: not_produced`, reason: `under-budget`). If draft count > 6: prompt the human to merge or drop goals before proceeding.

6. **HITL accept.** Present the draft list to the human for edit / accept / reject. Do not finalize until the human explicitly accepts. Forbidden: auto-accepting, treating brief acknowledgement as acceptance.

7. **Work-item slug + write.** Derive a candidate `<WI>` slug from the brief (short, snake_case, e.g. `ai_mail`, `fix_crash_abc`). Prompt the human: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Create `plan/<WI>/` if missing. Write the confirmed goal list to `plan/<WI>/idea.md`.

8. **Status update.** Write/update `plan/<WI>/status.md` with frontmatter:
   ```
   ---
   status: wip
   updated: <today YYYY-MM-DD>
   ---
   ```
   Rules: (a) refresh `updated:` to today on every run; (b) default `status: wip` after a successful artifact write; (c) if you judge the goal list complete and final, ask the human "mark done?" — flip to `done` only on explicit yes, never auto-flip; (d) preserve an existing `done` unless the human explicitly reopens — on reopen, flip `done → wip` (never back to `open`). On failure runs (no artifact written), do not create or modify `status.md`.

9. **Return.** Emit the confirmed goal list (numbered, one line each), the path written, plus the success signal — see Return section.

---

## Hard Rules

- Output is 3–6 major goals.
- No detail leakage: no module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or effort/timeline estimates in the goal list.
- Negative goals are first-class and count toward the 3–6 budget when they materially shape the work.
- HITL only. No AFK execution. Wait for explicit human acceptance.
- The brief is input, not output — even a clean brief gets restated as a goal list.
- Single artifact. On accept, write the goal list to `plan/<WI>/idea.md` and nowhere else. `<WI>` is human-confirmed before write. No writes on failure.
- Always emit/update `plan/<WI>/status.md` alongside a successful artifact write per the status spec in Step 8. Human-only `done`. Never auto-flip.
- No phase orchestration. Do not name, invoke, or hand off to other phases or skills. Output is the goal list and a status signal — nothing more.

---

## Return

On success:

- The confirmed goal list, numbered, one line each.
- Path written: `plan/<WI>/idea.md`.
- Status file: `plan/<WI>/status.md` (`status: wip` unless human confirmed `done`).
- `status: ok` plus a one-line summary: "Produced N goals from brief."

On failure (under-budget, human rejected, no acceptance reached):

- Write nothing (no `idea.md`, no `status.md`).
- `status: not_produced` plus the reason.
- No phase names. No "next step" language.
