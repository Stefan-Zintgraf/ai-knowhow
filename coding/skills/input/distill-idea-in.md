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

## Scope

The skill does **one** thing: turn a raw brief into a confirmed list of 3–6 major goals, then report success.

The skill does **not**:

- Manage phase transitions or name downstream phases in its output.
- Hand off to, invoke, or describe `aln`, `prd`, or any other phase.
- Decide whether the workflow proceeds.

Phase orchestration is the caller's job. The skill's return is just: the goal list, plus a success signal.

---

## Self-Containment Mandate

The output skill must run **without** `gr/gr_idea.md`, `phases.md`, or `guardrails.md` in context or on disk. Every rule the skill needs at runtime must be **inlined** into the skill file. No links to source docs. No "see X" references. The skill is a leaf artifact.

Source docs below are author-time scaffolding only — read them, distill them, embed the distilled content into the skill.

---

## Source Documents (author-time only)

| File | Relevant sections |
|------|-------------------|
| `gr/gr_idea.md` | Idea1, Idea2, Idea3, Idea4, Idea5, Idea7 (Idea6 is phase-coupling — skip), Anti-Patterns |
| `guardrails.md` | §3.32 (substance of the rule — strip phase-routing language) |

Note: `phases.md` and §3.29 / §4.19 are phase-management concerns. Out of scope for this skill — do not embed.

---

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. Output is **3–6 major goals**.
2. **No details**: no module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or effort/timeline estimates.
3. **Negative goals are first-class** and count toward the 3–6 budget when they materially shape the work.
4. **HITL only** — no AFK execution. Wait for explicit human acceptance.
5. **Brief is input, not output** — even a clean brief gets restated as a goal list.
6. **Artifact written to `plan/<WI>/idea.md`** — on human acceptance, persist the confirmed goal list. `<WI>` is a unique work-item slug (e.g. `ai_mail`, `fix_crash_abc`). The skill prompts the human for `<WI>`, suggesting a slug derived from the brief; the human confirms or overrides. Create the directory if missing. No writes on failure.

---

## Skill Behaviors

In order:

1. **Pre-structured-input check (hybrid).**
   Heuristically scan the input for a candidate goal list (3–6 outcome-shaped bullets, no detail leakage). If it fires, ask the human: "Input already looks like 3–6 goals: [list]. Treat as the confirmed goal list, or run full distillation?" If the human picks "treat as confirmed," skip to step 6 with that list. Otherwise proceed. If the heuristic does not fire, proceed silently.

2. **Distillation pass.**
   Read the raw input (Slack note, ticket, email, transcript, freeform brief). Produce a draft list of 3–6 major goals. Each names *what the work must serve*, not *how*.

3. **Detail-leak strip.**
   Remove from the draft any goal containing module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or estimates. Append a one-line note per stripped item: "Stripped detail: [item]."

4. **Negative goal capture.**
   Identify explicit exclusions in the brief ("not a mobile app", "no real-time updates"). Promote them to the goal list as negative goals.

5. **Count gate.**
   If draft count < 3: report that the brief may be too narrow for goal-shaped framing and return without a goal list (success=false, reason="under-budget"). If draft count > 6: prompt the human to merge or drop goals before proceeding.

6. **HITL accept.**
   Present the draft list to the human for edit / accept / reject. Do not finalize until the human explicitly accepts. Forbidden: auto-accepting, treating brief acknowledgement as acceptance.

7. **Work-item slug + write.**
   Derive a candidate `<WI>` slug from the brief (short, snake_case, e.g. `ai_mail`, `fix_crash_abc`). Prompt the human: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Create `plan/<WI>/` if missing. Write the confirmed goal list to `plan/<WI>/idea.md`.

8. **Return.**
   Emit:
   - The confirmed goal list (numbered, one line each).
   - Path written: `plan/<WI>/idea.md`.
   - A success signal: `status: ok` plus one-line summary ("Produced N goals from brief.").
   On failure (under-budget, human rejected, no acceptance reached), write nothing and emit `status: not_produced` plus the reason. No phase names. No "next step" language.

---

## Constraints (must appear as Hard Rules inside the skill)

- **No detail leakage**: enumerated forbidden items above.
- **Single artifact**: on accept, write the goal list to `plan/<WI>/idea.md` and nowhere else. `<WI>` is human-confirmed before write. No writes on failure.
- **HITL only**: explicit human acceptance required.
- **No phase orchestration**: the skill does not name, invoke, or hand off to other phases or skills. Output is the goal list and a status signal — nothing more.

---

## Output Format (for the generated skill)

The output skill (`skills/output/distill-idea.md`) must be a Claude Code SKILL.md — a single self-contained markdown prompt file that:

- Opens with a one-paragraph role statement: this skill distills a raw brief into 3–6 major goals and returns them. It does not manage workflow phases.
- Contains an inlined **Hard Rules** block (the six rules above plus the four Constraints, brief imperative form). No "see guardrails.md §X" references.
- Has an ordered **Steps** section mapping to the 7 behaviors above (one sentence per step; expand only where ambiguity would cause wrong behavior).
- Has a **Return** section specifying the success/failure signal shape.
- Does **not** link to `gr/gr_idea.md`, `phases.md`, or `guardrails.md`. Does **not** mention `aln`, `prd`, or any other phase token.
- Passes the test: if the skill file were the only file in the repo, an agent reading it could still execute correctly.
