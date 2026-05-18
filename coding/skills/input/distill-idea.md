# Authoring Prompt: `distill-idea` Skill (A11)

## Metadata

```yaml
skill_id: A11
skill_name: distill-idea
phase: ide
status: todo
workflow_ref: W15
depends_on: []
feeds_into: [A1-grill-me]
```

---

## Source Documents

Read all of the following before writing the skill. The skill must faithfully encode every rule and constraint found in these sources — no invention, no omission.

| File | Relevant sections |
|------|-------------------|
| `gr/gr_idea.md` | All — Idea1 through Idea7, Apply When, Anti-Patterns, Notes on Interaction |
| `phases.md` | `ide` phase entry (§1), phase sequence diagram (§4) |
| `guardrails.md` | §3.32 (core rule), §3.29 (collapse / phase-skip), §4.19 (routing index entry) |

---

## Skill Behaviors

The skill must implement the following behaviors in the order listed:

1. **Collapse check (3.29 / Idea1).**  
   If the input artifact (brief, ticket, memo) already contains 3–6 explicit goals, emit a one-line confirmation ("Brief already names goals: [list]. Proceeding to `aln` with these.") and stop. Do not run the full distillation pass.

2. **Distillation pass.**  
   Read the raw input (Slack note, ticket, email, verbal transcript, or any freeform brief). Produce a draft list of **3–6 major goals** from it. Each goal names *what the work must serve*, not *how*.

3. **Detail-leak strip (Idea2).**  
   Scan the draft goal list. Remove or defer to `aln`/`prd` any goal that contains:
   - module names, file paths, or API shapes
   - UX specifics (screens, components, layouts)
   - acceptance criteria
   - tech choices (library X, pattern Y)
   - effort or timeline estimates  
   For each stripped item, append a one-line note: "Deferred to [aln/prd]: [item]."

4. **Negative goal capture (Idea3).**  
   Identify explicit exclusions in the brief ("not a mobile app", "no real-time updates"). Promote them to the goal list as negative goals. They count toward the 3–6 budget when they materially shape the work.

5. **Count gate (Idea1).**  
   If draft count < 3: flag that the brief may be too narrow for goal-shaped framing; suggest going to `aln` directly with the brief as-is.  
   If draft count > 6: prompt the human to merge or drop goals before proceeding.

6. **HITL handoff (Idea4).**  
   Present the draft goal list to the human for edit / accept / reject. Do not proceed to `aln` until the human explicitly accepts the list. Forbidden: auto-accepting, summarizing the list as "done", or assuming acceptance after a brief acknowledgement.

7. **Handoff to `aln` (Idea6).**  
   Once the human accepts, output the confirmed goal list as the input to the `aln` phase. State clearly: "Goal list confirmed. Starting `aln` grilling now." Do not write any file to the working tree (Idea7 — no `idea/<topic>.md`).

---

## Constraints

These constraints must be encoded as hard rules in the skill, not as soft suggestions:

- **No detail leakage**: module names, APIs, UX specifics, acceptance criteria, tech choices, estimates are forbidden in the goal list.
- **No file output**: the skill produces no in-tree artifact. The goal list is ephemeral; it feeds `aln` and is eventually folded into the PRD's Goals section.
- **HITL only**: no AFK execution. The skill must wait for human acceptance before handing off.
- **No jump to `prd`**: the goal list seeds `aln` grilling; it does not replace `aln`. Any path that skips `aln` violates §3.21.
- **Collapse, not skip**: when upstream brief already names goals, the skill collapses to a confirmation, it does not silently skip (§3.29).

---

## Output Format (for the generated skill)

The output skill (`skills/output/distill-idea.md`) must be a Claude Code SKILL.md — a single markdown prompt file that:

- Opens with a one-paragraph role statement for the agent.
- Has an ordered "Steps" section mapping to the 7 behaviors above.
- Includes a "Hard Rules" section that mirrors the Constraints above, in brief imperative form.
- Includes a short "Handoff" section describing what to say/do when passing control to `aln`.
- Does **not** include implementation details, code, or file I/O instructions — the skill is a prompt, not a script.
- Is terse: one sentence per step is enough. Expand only where ambiguity would cause wrong behavior.
