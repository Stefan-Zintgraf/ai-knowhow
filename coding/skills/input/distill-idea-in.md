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

The skill does **one** thing: distill a raw brief / backlog item / stakeholder ask into a confirmed list of 3–6 major goals and persist it to `plan/<WI>/idea.md`.

The skill does **not**:

- Manage workflow phases or decide what runs next.
- Produce design, specification, module map, or acceptance criteria.
- Name, invoke, or hand off to other skills.
- Write to any path other than `plan/<WI>/idea.md` and `plan/<WI>/status_idea.md`.

Phase orchestration is the caller's job. The skill's return is just: the confirmed goal list, the paths written, and a status signal.

---

## Self-Containment Mandate

The output skill must run **without** `gr/gr_idea.md`, `guardrails.md`, or `phases.md` in context or on disk. Every rule the skill needs at runtime must be **inlined** into the skill file. No links to source docs. No "see X" references. The skill is a leaf artifact.

Source docs below are author-time scaffolding only — read them, distill them, embed the distilled content into the skill.

---

## Source Documents (author-time only)

| File            | Relevant sections                                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------------- |
| `gr/gr_idea.md` | Idea1–Idea7 (substantive rules: 3–6 budget, no details, negative goals, HITL, brief-is-input, persistence shape) |
| `guardrails.md` | §3.32 (substance only; collapse-mode language stripped), §3.33 (retirement; owner-issue field requirement)       |

Note: `phases.md` and `guardrails.md` §4.19 are phase-routing concerns — out of scope for this skill, do not embed. `guardrails.md` §3.29 collapse-mode is a caller concern; the only carry-over here is that an already-shaped input gets an explicit human choice (treat-as-confirmed vs. run full pass), never a silent short-circuit. The Idea6 hand-off statement and any "feeds aln" language are phase orchestration and must NOT appear in the output skill.

---

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. Output is 3–6 major goals.
2. No detail leakage: no module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or effort/timeline estimates in the goal list.
3. Negative goals are first-class and count toward the 3–6 budget when they materially shape the work.
4. **HITL only.** No AFK execution. Wait for explicit human acceptance.
5. The brief is input, not output — even a clean brief gets restated as a goal list.
6. Single artifact. On accept, write the goal list to `plan/<WI>/idea.md` and nowhere else. `<WI>` is human-confirmed before write. No writes on failure.
7. Always emit/update `plan/<WI>/status_idea.md` alongside a successful artifact write per the status spec in Steps. One status file per artifact — never a shared `status.md`. Human-only `done`. Never auto-flip.
8. `owner-issue:` is mandatory in `status_idea.md` frontmatter — the WI anchor for 3.33 retirement. Prompt the human; accept `#TBD` only with an explicit warning that Q11 merge-gate will fail until replaced.
9. No phase orchestration. Do not name, invoke, or hand off to other phases or skills. Output is the goal list and a status signal — nothing more.

---

## Skill Behaviors

In order:

1. **Pre-structured-input check.**
   Heuristically scan the input for a candidate goal list (3–6 outcome-shaped bullets, no detail leakage). If it fires, ask the human: "Input already looks like 3–6 goals: [list]. Treat as the confirmed goal list, or run full distillation?" If the human picks "treat as confirmed," skip to the HITL accept step with that list. Otherwise proceed. If the heuristic does not fire, proceed silently.

2. **Distillation pass.**
   Read the raw input. Produce a draft list of 3–6 major goals. Each goal names *what the work must serve*, not *how*.

3. **Detail-leak strip.**
   Remove any goal containing module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or estimates. Append a one-line note per stripped item using the exact format: `Stripped detail: <item>` (one per item, no phase names).

4. **Negative goal capture.**
   Identify explicit exclusions in the brief ("not a mobile app", "no real-time updates"). Promote them to the goal list as negative goals. They count toward the 3–6 budget when they materially shape the work.

5. **Count gate.**
   If draft count < 3: report that the brief may be too narrow for goal-shaped framing and return without a goal list (`status: not_produced`, `reason: under-budget`). If draft count > 6: prompt the human to merge or drop goals before proceeding. Forbidden phrases in failure strings: any phase token, `proceed to <phase>`, `deferred to <phase>`, `next phase`.

6. **HITL accept.**
   Present the draft list to the human for edit / accept / reject. Do not finalize until the human explicitly accepts. Forbidden: auto-accepting, treating brief acknowledgement as acceptance.

7. **Work-item slug + owner-issue + write.**
   Derive a candidate `<WI>` slug from the brief (short, snake_case — e.g. `ai_mail`, `fix_crash_abc`). Prompt the human: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Then prompt: "Owner issue (e.g. `#123`)?" — required; the WI anchor for 3.33 retirement. If the human has no issue number yet, accept a placeholder `#TBD` and warn that retirement enforcement (Q11 merge-gate) will fail until replaced. Create `plan/<WI>/` if missing. Write the confirmed goal list to `plan/<WI>/idea.md`.

8. **Status file write.**
   Write/update `plan/<WI>/status_idea.md` with frontmatter:
   
   ```
   ---
   status: wip
   updated: <today YYYY-MM-DD>
   owner-issue: <#NNN or #TBD>
   ---
   ```
   
   Rules: (a) refresh `updated:` to today on every run; (b) default `status: wip` after a successful artifact write; (c) ask the human "mark done?" at the end of every run UNLESS it is absolutely obvious and undoubtable that the artifact is still open/wip (e.g. under-budget failure, human rejected the draft, no human acceptance reached, count gate not passed) — in those clear-incomplete cases skip the prompt; flip to `done` only on explicit human yes, never auto-flip; (d) preserve an existing `done` unless the human explicitly reopens — on reopen, flip `done → wip` (never back to `open`). On failure runs (no artifact written), do NOT create or modify `status_idea.md`.

9. **Return.**
   Emit:
   
   - The confirmed goal list (numbered, one line each).
   - Path written: `plan/<WI>/idea.md`.
   - Status file: `plan/<WI>/status_idea.md` (`status: wip` unless human confirmed `done`).
   - `status: ok` plus a one-line summary: "Produced N goals from brief."
     On failure (under-budget, human rejected, no acceptance reached): write nothing (no `idea.md`, no `status_idea.md`); emit `status: not_produced` plus the reason. No phase names. No "next step" / "proceed to" / "deferred to" language anywhere in the failure string.

---

## Constraints (must appear as Hard Rules inside the skill)

- **3–6 budget**: fewer than 3 → `status: not_produced`, `reason: under-budget`; more than 6 → human merges/drops before proceeding.
- **No detail leakage**: strip module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, estimates.
- **Negative goals are first-class**: count toward the 3–6 budget.
- **HITL only**: explicit human acceptance required.
- **Single artifact**: write only `plan/<WI>/idea.md` (+ companion `plan/<WI>/status_idea.md`). No writes on failure.
- **owner-issue mandatory**: `status_idea.md` frontmatter MUST carry `owner-issue:`. Prompt the human at write-time; accept `#TBD` only with an explicit warning that Q11 merge-gate retirement enforcement will fail until replaced.
- **Human-only `done`**: never auto-flip; on reopen, `done → wip` (never back to `open`).
- **No phase orchestration**: the skill does not name, invoke, or hand off to other phases or skills. Output is the goal list and a status signal — nothing more.

---

## Output Format (for the generated skill)

The output skill (`skills/output/distill-idea.md`) must be a Claude Code SKILL.md — a single self-contained markdown prompt file that:

- Opens with a one-paragraph role statement: this skill distills a raw brief into 3–6 major goals and writes the confirmed list to `plan/<WI>/idea.md`. It does not manage workflow phases, name downstream work, or decide whether anything proceeds.
- Contains an inlined **Hard Rules** block (the rules above plus the Constraints, brief imperative form). No "see <doc> §X" references.
- Has an ordered **Steps** section mapping to the behaviors above (one sentence per step; expand only where ambiguity would cause wrong behavior).
- Includes the artifact path `plan/<WI>/idea.md`, the status file path `plan/<WI>/status_idea.md`, the full frontmatter spec (`status` + `updated` + `owner-issue` on the anchor), and the state-machine rules inlined verbatim from Step 8.
- Has a **Return** section specifying the success/failure signal shape.
- Does **not** link to `gr/gr_idea.md`, `guardrails.md`, or `phases.md`. Does **not** mention any phase token anywhere in the body outside its `Metadata.phase` field: `aln`, `prd`, `iss`, `res`, `pro`, `qa`, `rev`, `ica`, `ral`, `par`, `ide`. This applies to Rules, Steps, Return, prose, examples, anti-pattern bullets, and failure messages.
- Does **not** contain forbidden phrasings: `proceed to <phase>`, `deferred to <phase>`, `hand off to <phase>`, `feeds into <phase>`, `next phase`. Use `status: not_produced` + `reason:` for failure outcomes; use `Stripped detail: <item>` (per item) for leak notes.
- Passes the test: if the skill file were the only file in the repo, an agent reading it could still execute correctly.
