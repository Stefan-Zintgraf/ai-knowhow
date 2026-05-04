# Plan Rules (Meta Plan)

Rules for creating and executing step-wise implementation plans in the "EC plan" style (derived from `ger_mode_cmds_plan2`).

The pattern decomposes a non-trivial implementation task into small, independently executable, verifiable steps. Each step runs in its own conversation (session), produces committed artifacts, and is gated by an automated (or explicitly manual) check.

**Location:** This file lives in the `ec-plan` folder next to the `ec-create-plan` and `ec-impl` skills. When you copy the `skills` tree to another project, keep `ec-plan/` in place so both skills can resolve `../ec-plan/plan_rules.md` and `../ec-plan/templates/`.

---

## 1. When to use this pattern

Use it when **any** of the following hold:

- The task spans multiple files, phases, or sessions (roughly ≥ 3 non-trivial steps).
- Work must be resumable across conversations without loss of state.
- Intermediate artifacts (scripts, data, fixtures) are committed and reused.
- You want strict scope control: the agent does one step, commits, stops.

Do **not** use it for single-session tasks, throwaway experiments, or pure Q&A work.

---

## 2. Plan folder layout

All plan documents live in one folder, named after the plan (e.g. `my_feature_plan/`). Implementation artifacts (scripts, data, configs) live **outside** this folder, in the feature/project directory.

```
<plan_name>/
├── <plan_name>.md                   # REQUIRED — overview / execution contract
├── <plan_name>.step1.md             # REQUIRED — one file per step
├── <plan_name>.step2.md
├── ...
├── <plan_name>.stepN.md
├── implementation_prompt.md         # REQUIRED — session protocol for the agent
├── <plan_name>.strategy.md          # OPTIONAL — "why": rationale, principles, risks
├── <plan_name>.architecture.md      # OPTIONAL — "what": structure, data model, boundaries
├── <plan_name>.test_strategy.md     # OPTIONAL — gates per test layer (can fold into steps)
├── <plan_name>.rework_pre_stepN.md  # OPTIONAL — conditional interlude step(s)
└── <plan_name>.manual_tests.md      # OPTIONAL — notes for manual verification
```

### 2.1 Which optional docs to include

| Task characteristic | Include strategy? | Include architecture? | Include test strategy? |
|---------------------|-------------------|-----------------------|------------------------|
| Multiple plausible approaches, significant trade-offs | Yes | Often yes | Depends |
| Defines long-lived structure (data model, runtime boundary) | Sometimes | Yes | Sometimes |
| Simple linear refactor with obvious approach | No | No | Inline in steps |
| Heavy test surface with multiple backends/layers | Sometimes | Sometimes | Yes |

When a document is omitted, the overview and step files must still cover its content implicitly (at least acceptance criteria and automated gates).

---

## 3. Core principles

1. **One step = one session.** An implementation session reads the docs, does exactly one step, commits, updates status, then stops.
2. **Every step has a gate.** Either an automated command, or an explicit manual check documented in the step file.
3. **Status is dual-tracked.** Each step file carries a `Status: [ ]` / `[x]` header; the overview has the execution-order table with the same checkbox. Both must be updated together.
4. **Plan files are execution authoritative.** If strategy/architecture text conflicts with the plan or a step file, the plan/step wins. Strategy/architecture are read-only references during execution.
5. **Implementation artifacts live outside the plan folder.** The plan folder holds documentation only.
6. **Agents must not bypass gates, edit unrelated code, or rewrite inventory/contracts to force a gate green.** If blocked, stop and ask the user.
7. **Resumable on disk.** All progress lives in committed files or well-defined state files; a killed session loses at most the current in-flight work.

---

## 4. Overview document (`<plan_name>.md`) — required sections

### 4.1 Structure

1. **Title + purpose.** One paragraph, linking to strategy/architecture when present.
2. **Session rule.** State that each step runs in its own session: read overview + current step (+ architecture/test strategy if present), do the step, run gate, commit, mark `[x]`, stop.
3. **Entry / ordering constraints** (if any): conditional rework steps, phase exit gates, states that block later steps.
4. **Workspace conventions:** repo root, feature directory, where implementation outputs live, shell, any environment assumptions.
5. **Acceptance criteria (global).** Numbered list of conditions that define "the whole plan is done".
6. **Phase exit criteria** (if the plan is multi-phase): what must be true before starting Phase N+1.
7. **Key deliverables table.** `File | Created in | Role`.
8. **Execution order table.** `Step | File | Focus | Gate | Status` — the single source of truth for "what is next". The **first unchecked row** is the next implementation target (subject to entry/ordering rules above).
9. **Version control rule.** A step is complete only when: all verifiable-result boxes checked, required artifacts committed, status flipped in both step file and this table.
10. **Scope guardrails.** Explicit "do not" list (don't partially migrate, don't tune per-item during global phase, don't rewrite contracts to pass gates, etc.).
11. **Related documents.** Links to strategy, architecture, test strategy, rework files, manual tests.

### 4.2 Execution order table — format

```
| Step | File                    | Focus                          | Gate                           | Status |
|------|-------------------------|--------------------------------|--------------------------------|--------|
| 1    | [step1](...step1.md)    | <short phrase>                 | <command or "manual primary">  | [x]    |
| 2    | [step2](...step2.md)    | <short phrase>                 | <command>                      | [ ]    |
```

Interlude/rework rows are inserted in order (e.g. `Pre-5`, `5b`, `5c`). N/A rows still get `[x]` with a one-line reason in the step file.

---

## 5. Step file (`<plan_name>.step<N>.md`) — required sections

Keep step files small (~50–200 lines). Each step should be completable in a single session. If a step grows larger than a day's work, split it (e.g. `step5`, `step5b`, `step5c`).

### 5.1 Required sections, in order

1. **Title.** `# Step <N> — <short name>`
2. **`Status: [ ]` / `[x]`**
3. **Session rule.** One line: "Complete this step, run the automated gate, commit, mark `[x]`, then stop."
4. **Prerequisites.** Reference the step(s) or gates that must be green before starting. If this is an optional/interlude step, state N/A conditions.
5. **Goal.** One short paragraph: what this step produces and why.
6. **Tasks.** Numbered list of concrete implementation actions.
7. **Verifiable result.** Checkbox list of concrete artifacts / conditions (paths, file names, fields populated, tests green).
8. **Automated gate.** Exact command(s) the agent must run. If primary gate is manual, say so and list supplementary automated checks.
9. **Notes for the agent.** Policy constraints, common pitfalls, "do not" items specific to this step.

### 5.2 Good step hygiene

- **Reference other steps by relative link** (`[step5](<plan_name>.step5.md)`) so navigation works in any viewer.
- **Quote exact command strings** so the agent copies them verbatim.
- **Name every artifact produced** (relative path) so the verifiable result is unambiguous.
- **State the fallback** if the gate fails: iterate, flag, escalate to user.
- **Do not duplicate strategy rationale** — link to it instead.

---

## 6. Implementation prompt (`implementation_prompt.md`) — required sections

This is the text the agent reads at the **start of every implementation session**. It is the runtime contract.

### 6.1 Required content

1. **One-line context.** "You are continuing work on <task name>."
2. **Session protocol** (numbered):
   1. Read these files in order: overview (find next `[ ]` in execution table), the step file, architecture (if present), test strategy (if present).
   2. Run `git status` and `git log --oneline -10` to confirm prior steps are committed and tree is clean.
   3. Implement **only** the current step. Run its automated gate. Commit all new/changed artifacts. Mark `[x]` in both the step file's Status and the overview's execution table. Then **stop**.
3. **Constraints.** Where implementation output goes; what must not be modified without an explicit step calling for it; forbidden shortcuts (e.g. "do not rewrite test contracts to force a gate green"); do not proceed to the next step; do not skip the gate; if blocked or unclear, stop and ask.
4. **Workspace block.** Repo root, feature directory, plan folder (read-only unless updating status), shell, runtime info (Python, Node, etc.).

Keep the prompt short (≤ 50 lines). It must fit easily in a new conversation's first message.

---

## 7. Strategy document (optional, `<plan_name>.strategy.md`)

Include when there are meaningful trade-offs, principles to pin down, or risks the execution docs should not repeat.

Recommended sections:

1. Goal and date.
2. Problem analysis (what's broken, why, observed patterns).
3. Planning principles (ordered preferences; "smallest effective intervention first").
4. Strategy overview (phase pipeline, high-level flow).
5. Detailed phase descriptions (only enough to justify the step structure).
6. Redesign / transformation rules.
7. Implementation: files and scripts (overview only — the file map is authoritative in architecture).
8. Execution order summary (mirrors overview table but narratively).
9. Automation boundaries (what's automated vs human).
10. Risk mitigation.
11. Success metrics.

Explicitly mark the strategy as **read-only during execution**. If strategy and plan conflict, the plan is authoritative.

---

## 8. Architecture document (optional, `<plan_name>.architecture.md`)

Include when structure is non-obvious, when freezing a contract (data model, runtime boundary, module layout), or when multiple scripts/services must agree on boundaries.

Recommended sections:

1. Goal.
2. Problem boundary (hard constraints: model limits, API contracts, compatibility).
3. Pipeline overview (ASCII or mermaid).
4. Single source of truth: the authoritative data artifact (schema, field semantics, status fields).
5. Module and script boundaries (table: artifact | responsibility).
6. Compatibility rules (legacy code, deprecation paths).
7. Matching / normalization / invariant logic.
8. Corpus or external-system alignment.
9. File map (authoritative list of implementation deliverables).
10. Storage / persistence policy (what's committed, what's ignored, lifecycle).
11. Key decisions (table: # | question | resolution).
12. Risk-driven constraints.
13. Rejected alternatives.

---

## 9. Interlude / rework steps (optional)

When upstream churn can invalidate earlier steps (e.g. inventory changes), define a **conditional rework step** (pattern: `<plan_name>.rework_pre_step<N>.md`). It runs when specific triggers fire; otherwise it is marked N/A.

Required fields:

- **Triggers** — explicit list of conditions that force running the rework.
- **Ordered sequence** — which prior steps to redo, in order, until stable.
- **N/A rule** — how to mark the row `[x]` when triggers do not apply (one-line commit note is enough).

The rework step itself is a single session; it stops after commit. The next planned step starts in a **new** session.

---

## 10. Status fields inside artifacts (data model pattern)

When the plan tracks progress per item in a data artifact (registry, inventory, fixture set), prefer **multiple narrow status fields** over one overloaded `status`. Example from the reference plan: `tts_status` (Phase 1) and `real_voice_status` (Phase 2) instead of one field that mixes both.

Each status field:

- Has a documented state machine (allowed values, transitions, which step sets which value).
- Has a documented blocking rule ("Phase 2 entry requires `tts_status` in none of: `needs_manual_redesign`, `manual_redesign_pass`, `text_corpus_pass`").
- Is never rewritten by automation to bypass a gate.

---

## 11. Scope guardrails that belong in every plan

Adapt and keep the spirit of these in the overview's "Scope guardrails" section:

- Do not accept work on synthetic evidence when the plan requires real/runtime evidence.
- Do not tune per-item when the design is a global pass.
- Do not migrate partially when unresolved items exist.
- Do not rewrite the source-of-truth artifact (registry, inventory, contracts) to force a gate green; resolve via the documented escalation path, or stop and ask.
- Do not run destructive VCS operations (e.g. `git restore`, `git checkout --`, hard resets) on tracked data without explicit user consent — uncommitted operator edits may be lost.

---

## 12. Execution contract (summary for the agent)

When executing a plan in this style:

1. Open the overview. Find the first `[ ]` in the execution table, respecting entry rules and interlude ordering.
2. Open that step file. Read prerequisites; confirm they are green (check statuses + `git log`).
3. Read architecture and test strategy if present.
4. Execute only the tasks in the step. Produce only the listed artifacts.
5. Run the automated gate exactly as written. If it fails, iterate **within the step** or stop and ask — do not mutate contracts or skip the gate.
6. Commit. Update `Status: [x]` in both the step file and the overview's table.
7. Stop. Do not start the next step.

If any of the following occur, stop and ask the user instead of guessing: unclear requirement, missing prerequisite, gate fails for reasons the step does not anticipate, temptation to modify an artifact the step did not list.

---

## 13. Templates

Minimal templates live in `./templates/` alongside this file:

- `overview_template.md`
- `step_template.md`
- `implementation_prompt_template.md`
- `strategy_template.md` (optional doc)
- `architecture_template.md` (optional doc)
- `rework_template.md` (optional interlude step)

Copy a template, rename with the plan-specific prefix, fill in the sections. Remove unused optional sections rather than leaving placeholders.
