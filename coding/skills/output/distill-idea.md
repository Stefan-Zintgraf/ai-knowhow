---
name: distill-idea
description: Distill a raw brief into 3–6 major goals and persist the confirmed list to plan/<WI>/idea.md. Use at the very start of a new work-item.
compiled-against: compile-skill v2.1.0
source: skills/input/distill-idea-in.md
source-sha256: f0ce9d4900480e8ca37715f2baf4480ef27529866097851a1885e4c16a553c31
source-modified: 2026-05-20 16:53
compiled: 2026-05-20 16:53
---

# Skill: distill-idea

This skill distills a raw brief into 3–6 major goals and writes the confirmed list to `plan/<WI>/idea.md`. It does not manage workflow phases, name downstream work, or decide whether anything proceeds.

---

## Steps

1. **Pre-structured-input check.** Heuristically scan the input for a candidate goal list (3–6 outcome-shaped bullets, no detail leakage). If it fires, ask the human via an explicit choice prompt: "Input already looks like 3–6 goals: [list]. Treat as the confirmed goal list, or run full distillation?" — never silently quote-back-and-confirm. If "treat as confirmed", skip to step 6 with that list. Otherwise proceed. If the heuristic does not fire, proceed silently.

2. **Distillation pass.** Read the raw input (Slack note, ticket, email, transcript, freeform brief). Produce a draft list of 3–6 major goals. Each names *what the work must serve*, not *how*. One sentence per goal. No nested bullets. No prose paragraphs.

3. **Detail-leak strip.** Remove from each draft goal any module name, file path, API shape, UX specific, acceptance criterion, tech choice, or estimate. Append a one-line note per stripped item using the exact format: `Stripped detail: <item>` (one per item, no phase names).

4. **Negative goal capture.** Identify explicit exclusions in the brief ("not a mobile app", "no real-time updates", "no migration from system X"). Promote them to the goal list as negative goals using the `Non-goal: ` prefix (capital N, space after colon). They count toward the 3–6 budget when they materially shape the work.

5. **Count gate.** If draft count < 3: return `status: not_produced` with `reason: under-budget` and a one-line note that the brief may be too narrow for goal-shaped framing. If draft count > 6: prompt the human to merge or drop goals before proceeding.

6. **HITL accept.** Present the draft list to the human for edit / accept / reject. Do not finalize until the human explicitly accepts. Forbidden: auto-accepting, treating brief acknowledgement as acceptance.

7. **Work-item slug + owner-issue + write.** Derive a candidate `<WI>` slug from the brief (short, snake_case — e.g. `ai_mail`, `fix_crash_abc`). Prompt the human: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Then prompt: "Owner issue (e.g. `#123`)?" — required; the WI anchor. If the human has no issue number yet, accept a placeholder `#TBD` and explicitly warn that Q11 merge-gate retirement enforcement will fail until replaced. Create `plan/<WI>/` if missing. Write the confirmed goal list to `plan/<WI>/idea.md` under the literal heading `# Goals`, numbered entries, one sentence each.

8. **Status update.** Write/update `plan/<WI>/status_idea.md` with frontmatter:
   ```
   ---
   status: open | wip | done
   updated: <today YYYY-MM-DD>
   owner-issue: <#NNN or #TBD>
   ---
   ```
   Rules: (a) refresh `updated:` to today on every run; (b) default `status: wip` after a successful artifact write; (c) ask the human "mark done?" at end of every run UNLESS it is absolutely obvious and undoubtable that the artifact is still open/wip (e.g. under-budget failure, human rejected the draft, no human acceptance reached, count gate not passed) — in those clear-incomplete cases skip the prompt; flip to `done` only on explicit human yes, never auto-flip; (d) preserve an existing `done` unless the human explicitly reopens — on reopen, flip `done → wip` (never back to `open`). On failure runs (no artifact written), do not create or modify `status_idea.md`.

9. **Return.** Emit the confirmed goal list (numbered, one line each), the path written, plus the success signal — see Return section.

---

## Hard Rules

- Output is 3–6 major goals.
- No detail leakage: no module names, file paths, API shapes, UX specifics (screens, components, layouts), acceptance criteria, tech choices (library X, pattern Y), or effort/timeline estimates inside any goal.
- Negative goals are first-class and count toward the 3–6 budget when they materially shape the work. Prefix exactly `Non-goal: `.
- HITL only. No AFK execution. Wait for explicit human acceptance.
- The brief is input, not output — even a clean brief gets restated as a goal list.
- Single canonical artifact. On accept, write the goal list to `plan/<WI>/idea.md` and nowhere else. `<WI>` is a human-confirmed snake_case slug. No `idea/<topic>.md`, no shared `idea.md`, no `<WI>.md` at the repo root. No writes on failure.
- Status file paired. Always emit/update `plan/<WI>/status_idea.md` alongside a successful artifact write per the spec in Step 8. One status file per artifact — never a shared `status.md`. Human-only `done`. Never auto-flip.
- `owner-issue:` is mandatory in `status_idea.md` frontmatter — the WI anchor. Prompt the human; accept `#TBD` only with an explicit warning that Q11 merge-gate will fail until replaced.
- No phase orchestration. Do not name, invoke, or hand off to other skills. Output is the goal list, the artifact path, and a status signal — nothing more.

---

## Return

On success:

- The confirmed goal list, numbered, one line each.
- Path written: `plan/<WI>/idea.md`.
- Status file: `plan/<WI>/status_idea.md` (`status: wip` unless human confirmed `done`).
- `status: ok` plus a one-line summary: "Produced N goals from brief."

On failure (under-budget, human rejected, no acceptance reached):

- Write nothing (no `idea.md`, no `status_idea.md`).
- `status: not_produced` plus the reason.
