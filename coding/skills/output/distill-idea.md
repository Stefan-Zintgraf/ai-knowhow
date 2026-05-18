# Skill: distill-idea

Phase `ide`. Distill a raw brief, backlog item, or stakeholder ask into 3–6 major goals that anchor the `aln` grilling session. No details, no design, no output files — just the small set of intents the work must serve.

---

## Steps

1. **Collapse check.** If the input already contains 3–6 explicit goals, emit: "Brief already names goals: [list]. Proceeding to `aln` with these." Stop here.

2. **Distill.** Read the raw input. Draft 3–6 major goals. Each goal names *what the work must serve*, not *how*.

3. **Strip detail leaks.** Remove any goal containing module names, file paths, API shapes, UX specifics (screens, components, layouts), acceptance criteria, tech choices, or estimates. For each stripped item append: "Deferred to [aln/prd]: [item]."

4. **Capture negative goals.** Explicit exclusions ("not a mobile app", "no real-time updates") become first-class goals. They count toward the 3–6 budget when they materially shape the work.

5. **Count gate.** Fewer than 3: flag — brief may be too narrow; suggest going to `aln` with the brief as-is. More than 6: prompt the human to merge or drop goals before continuing.

6. **HITL handoff.** Present the draft goal list. Wait for the human to edit, accept, or reject. Do not proceed until acceptance is explicit.

7. **Hand off to `aln`.** Output the confirmed goal list and state: "Goal list confirmed. Starting `aln` grilling now."

---

## Hard Rules

- No module names, API shapes, UX specifics, acceptance criteria, tech choices, or estimates in the goal list.
- No in-tree artifact. The goal list is ephemeral — it feeds `aln` and is folded into the PRD's Goals section. Do not create any file.
- HITL only. Never proceed without explicit human acceptance.
- The goal list seeds `aln` — it does not replace it. Never jump to `prd` from here.
- Collapse (one-line confirmation), never silent skip, when the upstream brief already names goals.

---

## Handoff

After the human accepts the goal list:

> Goal list confirmed. Starting `aln` grilling now.

Pass the accepted goal list as context to the `aln` / `grill-me` skill. The grilling session will walk every branch of every goal — the goal list narrows what is grilled, it does not shortcut the grilling.
