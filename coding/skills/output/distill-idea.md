---
name: distill-idea
description: Distill a raw brief, backlog item, ticket, or vague stakeholder ask into a list of 3–6 major goals (positive + negative) that anchor downstream grilling. Conversational output only — no files written.
compiled-against: compile-skill v2.1.0
source: skills/input/distill-idea-in.md
source-sha256: 5617a77bea1b77fe0a77a1ad0f4fcd5be3decc04f6c3dc73de93f4acf8f48e43
source-modified: 2026-05-20 15:41
compiled: 2026-05-20 16:01
---

`distill-idea` is the `ide`-phase skill that turns a raw brief, backlog item, Slack note, ticket, or vague stakeholder ask into a list of **3–6 major goals** (positive and negative) that anchor downstream grilling. The deliverable is ephemeral and conversational — the skill frames *what the work must serve*, never *how*, and stops as soon as the human accepts the goal list. HITL only by construction.

## Hard Rules

- MUST produce between 3 and 6 goals, inclusive — never fewer than 3, never more than 6.
- If fewer than 3 candidate goals emerge, MUST stop and report "too narrow for goal framing; proceed to `aln` directly with the brief" — do not pad.
- If more than 6 candidate goals emerge, MUST merge / decompose internally to land in [3, 6] before presenting — never present a >6 list and ask the human to trim.
- Each goal names *what the work must serve*, never *how*.
- MUST NOT include module names, file paths, API shapes, UX specifics (screens, components, layouts), acceptance criteria, tech choices (library X, pattern Y), or effort/timeline estimates in any goal.
- If such a detail leaks from the brief, MUST strip it from the goal and note it once as "deferred to aln/prd" — never silently retain.
- MUST surface explicit non-goals (negative goals) as first-class entries, counting toward the 3–6 budget when they materially shape the work.
- MUST treat the brief as input, not output — restate even when the brief reads well; the act of distilling surfaces missing goals and unstated assumptions.
- HITL only. MUST NOT finalize without explicit human acceptance. No autonomous-mode acceptance. Silence is not acceptance.
- MUST NOT write any file in the working tree. Output is conversational only.
- MUST NOT produce design, PRD, issue, or research content.
- MUST NOT invoke or recommend a next phase beyond returning the goal list — control returns to the caller.
- Collapse mode: if the upstream artifact already names 3–6 explicit goals, MUST NOT run a full distillation pass — quote them back, ask the human to accept or amend, stop.

## Steps

1. **Read the brief.** Take the raw brief inline, pasted, or as referenced by the human.
2. **Collapse check.** Scan the brief for an explicit goal list of 3–6 items. If found, quote them back verbatim, ask the human to confirm or amend in one turn, and stop on acceptance. Skip steps 3–7.
3. **Distill.** Identify the small set of intents (positive and negative) the work must serve. Strip every implementation detail per the Hard Rules; hold each stripped detail for the closing "deferred to aln/prd" note.
4. **Size.** If candidates < 3, report "too narrow for goal framing; proceed to `aln` directly with the brief" and stop. If candidates > 6, merge / decompose internally to land in [3, 6] before presenting.
5. **Present.** Show the proposed 3–6 goal list to the human as a numbered list — one sentence per goal, no nested bullets, no detail. Mark negative goals explicitly (`Non-goal: …`). Append the one-line "deferred to aln/prd" note if any details were stripped.
6. **HITL loop.** Wait for explicit human accept / edit / reject. Iterate on edits. Do not assume silence is acceptance.
7. **Return.** On accept, emit the final goal list as the skill's return value (conversational text). Do not write any file. Do not invoke `aln` or any other phase — return control to the caller.

## Return

Conversational return shape:

- A numbered list of 3–6 goals, one sentence each, with negative goals prefixed `Non-goal:`.
- Optionally followed by a single line: `Deferred to aln/prd: <comma-separated stripped details>` if anything was stripped during distillation.

Failure signals:

- Under budget: one-line report `Too narrow for goal framing; proceed to aln directly with the brief.` and stop.
- Human rejects the draft: stay in the HITL loop until accept / edit / explicit abandon.
- Collapse hit: one-line quote of the existing 3–6 goals plus a confirm/amend prompt; stop on acceptance.
