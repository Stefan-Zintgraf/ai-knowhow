# Authoring Prompt: `distill-idea` Skill (A11)

## Metadata

```yaml
skill_id: A11
skill_name: distill-idea
phase: ide
status: todo
workflow_ref: W15
depends_on: []
feeds_into: [A1-align-concept]
```

---

## Scope

The skill does **one** thing: turn a raw brief into a confirmed list of 3–6 major goals, persist them to `plan/<WI>/idea.md`, and report success.

The skill does **not**:

- Manage workflow transitions or name downstream phases in its output.
- Hand off to, invoke, or describe any other skill or phase.
- Decide whether the work proceeds after the artifact is written.

Phase orchestration is the caller's job. The skill's return is just: the goal list, the artifact path, plus a status signal.

---

## Self-Containment Mandate

The output skill must run **without** `gr/gr_idea.md`, `tpl/tpl_idea.md`, `phases.md`, or `guardrails.md` in context or on disk. Every rule the skill needs at runtime must be **inlined** into the skill file. No links to source docs. No "see X" references. The skill is a leaf artifact.

Source docs below are author-time scaffolding only — read them, distill them, embed the distilled content into the skill.

---

## Source Documents (author-time only)

| File              | Relevant sections                                                                                                          |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `gr/gr_idea.md`   | Idea1, Idea2, Idea3, Idea4, Idea5, Idea7 (Idea6 is phase-coupling — skip), Anti-Patterns (drop bullets that name phases)   |
| `tpl/tpl_idea.md` | File Naming, `idea.md` Shape rules, `status_idea.md` frontmatter fields, State Machine (drop the Retirement/Q11 paragraph) |

Note: `phases.md`, `guardrails.md` §3.29 (collapse-mode), §3.33 (retirement orchestration), and §4.19 (routing) are phase-management concerns. Out of scope for this skill — do not embed.

---

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. Output is **3–6 major goals**.
2. **No details**: no module names, file paths, API shapes, UX specifics (screens, components, layouts), acceptance criteria, tech choices (library X, pattern Y), or effort/timeline estimates inside any goal.
3. **Negative goals are first-class** and count toward the 3–6 budget when they materially shape the work. Prefix exactly `Non-goal: ` (capital N, space after colon).
4. **HITL only** — no AFK execution. Wait for explicit human acceptance.
5. **Brief is input, not output** — even a clean brief gets restated as a goal list.
6. **Single canonical artifact.** On accept, write the goal list to `plan/<WI>/idea.md` and nowhere else. `<WI>` is a human-confirmed snake_case slug. No `idea/<topic>.md`, no shared `idea.md`, no `<WI>.md` at the repo root. No writes on failure.
7. **Status file always paired.** On every successful artifact write, write/update `plan/<WI>/status_idea.md` with frontmatter `status` + `updated` + `owner-issue`. Human-only `done`; never auto-flip. `owner-issue:` mandatory.

---

## Skill Behaviors

In order:

1. **Pre-structured-input check.**
   Heuristically scan the input for a candidate goal list (3–6 outcome-shaped bullets, no detail leakage). If it fires, ask the human via an explicit choice prompt: "Input already looks like 3–6 goals: [list]. Treat as the confirmed goal list, or run full distillation?" — never silently quote-back-and-confirm. If "treat as confirmed", skip to step 6 with that list. Otherwise proceed. If the heuristic does not fire, proceed silently.

2. **Distillation pass.**
   Read the raw input (Slack note, ticket, email, transcript, freeform brief). Produce a draft list of 3–6 major goals. Each names *what the work must serve*, not *how*. One sentence per goal. No nested bullets. No prose paragraphs.

3. **Detail-leak strip.**
   Remove from each draft goal any module name, file path, API shape, UX specific, acceptance criterion, tech choice, or estimate. Append a one-line note per stripped item using the exact format: `Stripped detail: <item>` (one per item, no phase names — never "deferred to <phase>").

4. **Negative goal capture.**
   Identify explicit exclusions in the brief ("not a mobile app", "no real-time updates", "no migration from system X"). Promote them to the goal list as negative goals using the `Non-goal: ` prefix. They count toward the 3–6 budget when they materially shape the work.

5. **Count gate.**
   If draft count < 3: return `status: not_produced` with `reason: under-budget` and a one-line note that the brief may be too narrow for goal-shaped framing. **Forbidden phrases in the failure string**: any phase token, `proceed to <phase>`, `deferred to <phase>`, `next phase`. If draft count > 6: prompt the human to merge or drop goals before proceeding.

6. **HITL accept.**
   Present the draft list to the human for edit / accept / reject. Do not finalize until the human explicitly accepts. Forbidden: auto-accepting, treating brief acknowledgement as acceptance.

7. **Artifact write.**
   Derive a candidate `<WI>` slug from the brief (short, snake_case — e.g. `ai_mail`, `fix_crash_abc`). Prompt the human: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Then prompt: "Owner issue (e.g. `#123`)?" — required; the WI anchor. If the human has no issue number yet, accept a placeholder `#TBD` and explicitly warn that Q11 merge-gate retirement enforcement will fail until replaced. Create `plan/<WI>/` if missing. Write the confirmed goal list to `plan/<WI>/idea.md` under the literal heading `# Goals`, numbered entries, one sentence each.

8. **Status file write.**
   Write/update `plan/<WI>/status_idea.md` with frontmatter:
   ```
   ---
   status: open|wip|done
   updated: <today YYYY-MM-DD>
   owner-issue: #NNN   # mandatory on the anchor artifact; siblings inherit
   ---
   ```
   Rules: (a) refresh `updated:` to today on every run; (b) default `status: wip` after a successful artifact write; (c) ask the human "mark done?" at end of run UNLESS the run is a clear-incomplete (under-budget, human rejected, no acceptance) — in those cases skip the prompt; flip to `done` only on explicit human yes, never auto-flip; (d) preserve existing `done` unless the human explicitly reopens — on reopen, flip `done → wip` (never back to `open`). On failure runs (no artifact written), do NOT create or modify `status_idea.md`.

9. **Return.**
   Emit:
   - The confirmed goal list (numbered, one line each).
   - Path written: `plan/<WI>/idea.md`.
   - Status file: `plan/<WI>/status_idea.md` (`status: wip` unless human confirmed `done`).
   - A success signal: `status: ok` plus one-line summary ("Produced N goals from brief.").
   On failure (under-budget, human rejected, no acceptance reached), emit `status: not_produced` plus the reason. Write nothing. No phase names. No "next step" / "proceed to" / "deferred to" language anywhere in the failure string.

---

## Constraints (must appear as Hard Rules inside the skill)

- **No detail leakage**: enumerated forbidden items above.
- **Single canonical artifact path**: `plan/<WI>/idea.md`. No alternative locations. No writes on failure.
- **Status file paired**: every successful artifact write produces/updates `plan/<WI>/status_idea.md` per the spec in Step 8. One status file per artifact — never a shared `status.md`.
- **HITL only**: explicit human acceptance required.
- **owner-issue mandatory**: `status_idea.md` frontmatter MUST carry `owner-issue:`. Prompt the human at write-time; accept `#TBD` only with an explicit warning that merge-gate retirement enforcement will fail until replaced.
- **No phase orchestration**: the skill does not name, invoke, or hand off to other phases or skills. Output is the goal list, the artifact path, and a status signal — nothing more.

---

## Output Format (for the generated skill)

The output skill (`skills/output/distill-idea.md`) must be a Claude Code SKILL.md — a single self-contained markdown prompt file that:

- Opens with a one-paragraph role statement: this skill distills a raw brief into 3–6 major goals and writes them to `plan/<WI>/idea.md`. It does not manage workflow phases.
- Contains an inlined **Hard Rules** block (the seven Rules above plus the Constraints, brief imperative form). No "see gr_idea.md §X" / "see guardrails.md §X" references.
- Has an ordered **Steps** section mapping to the 9 behaviors above (one sentence per step; expand only where ambiguity would cause wrong behavior).
- Includes the artifact path (`plan/<WI>/idea.md`), the status file path (`plan/<WI>/status_idea.md`), the full frontmatter spec (`status` + `updated` + `owner-issue` on the anchor), and the state-machine rules inlined verbatim.
- Has a **Return** section specifying the success/failure signal shape.
- Does **not** link to `gr/gr_idea.md`, `tpl/tpl_idea.md`, `phases.md`, or `guardrails.md`. Does **not** mention any phase token anywhere in the body outside its `Metadata.phase` field: `aln`, `prd`, `iss`, `res`, `pro`, `qa`, `rev`, `ica`, `ral`, `par`, `ide`. This applies to Rules, Steps, Return, prose, examples, anti-pattern bullets, and failure messages.
- Does **not** contain forbidden phrasings: `proceed to <phase>`, `deferred to <phase>`, `hand off to <phase>`, `feeds into <phase>`, `next phase`. Use `status: not_produced` + `reason:` for failure outcomes; use `Stripped detail: <item>` (per item) for leak notes.
- Passes the test: if the skill file were the only file in the repo, an agent reading it could still execute correctly.
