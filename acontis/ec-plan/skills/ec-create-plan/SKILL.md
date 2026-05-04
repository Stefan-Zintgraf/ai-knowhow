---
name: ec-create-plan
description: Create a step-wise implementation plan in the EC plan style (strategy, architecture, overview, step files, implementation prompt) via a Q&A-driven discussion with the user. Use when the user asks to "create a plan", "set up a plan", "make an EC plan", "start a new ec plan", or otherwise wants a resumable multi-step implementation contract with per-step gates and session isolation.
---

# ec-create-plan

Guide the user through creating an EC-style implementation plan: a dedicated folder of markdown documents that decomposes a non-trivial task into small, independently executable, gated steps, each performed in its own session.

The authoritative specification of this plan style is **[`ec-plan/plan_rules.md`](../ec-plan/plan_rules.md)** (sibling to this skill: copy the whole `skills/` tree so `ec-plan` stays next to `ec-create-plan`). Read it once on first use of this skill. Blank templates live in **[`ec-plan/templates/`](../ec-plan/templates/)**.

## Quick start

1. Read [`../ec-plan/plan_rules.md`](../ec-plan/plan_rules.md) if you have not read it in this session.
2. Use `AskQuestion` to gather the inputs listed in **Discovery** below. Ask in small batches; do not overwhelm the user.
3. Propose the plan structure (folder name, which optional docs to include, rough step breakdown) and confirm before writing files.
4. Generate the files per **Output** below, filling templates from `ec-plan/templates/` with the gathered answers.
5. End by showing the user the list of files created and the first step's `Status: [ ]` so they know what to run next.

Do not implement the first step in the same session. Plan creation and plan execution are separate sessions.

## Discovery (Q&A)

Use `AskQuestion` for structured answers; fall back to conversational if needed. Keep questions focused — batch related ones.

### Round 1 — task shape

Ask these (at minimum):

- **Task description.** What is the goal, in 1–3 sentences? (free text)
- **Task scope.** `["Small (1–3 steps, single file set)", "Medium (4–8 steps, multiple artifacts)", "Large (9+ steps or multi-phase)"]`.
- **Plan folder location.** Where should the plan folder live? (absolute or repo-relative path)
- **Plan name / prefix.** Short identifier, lowercase with underscores (e.g. `auth_migration_plan`).

If the user answers "Small", warn them that EC plans are usually overkill for tiny tasks; offer to just do the task or to proceed anyway.

### Round 2 — optional documents

Ask which optional documents to include. Default recommendations come from `plan_rules.md §2.1`:

- **Include a strategy document?** `["Yes — there are meaningful trade-offs / principles to pin down", "No — approach is obvious"]`
- **Include an architecture document?** `["Yes — structure / data model / boundaries are non-trivial", "No — structure is obvious from the steps"]`
- **Include a separate test strategy document?** `["Yes — multiple test layers / backends", "No — fold gates into step files"]`
- **Will there be conditional rework / interlude steps?** `["Yes — upstream churn can invalidate earlier steps", "No"]`

### Round 3 — execution context

- **Repository root** (absolute path).
- **Feature / implementation directory** where scripts, data, and configs will live (must be outside the plan folder).
- **Shell** `["bash", "powershell", "zsh", "other"]`.
- **Primary runtime(s)** (Python, Node, Java, …; versions if they matter).
- **Version control.** Confirm git is in use (required for the session protocol's `git status` / `git log` checks).

### Round 4 — step breakdown

- **Proposed steps.** Ask the user to list or sketch the steps. Offer to propose a breakdown first from the task description if they're stuck.
- **Acceptance criteria.** What must be true for the whole plan to be "done"? (2–6 bullet points.)
- **Scope guardrails.** Anything that must NOT be changed, or must be preserved? (e.g. don't migrate partially, don't rewrite test contracts.)
- **Single source of truth.** If the plan tracks per-item progress in a data artifact (registry, inventory, fixture set), what is that artifact and what status fields does it need?

If the user is unsure, offer a draft breakdown based on the task. Do not write files until the user confirms the step list.

## Design before writing

Before creating any files, summarize in chat:

- Plan folder path and name.
- Which documents will be created (overview, step1..N, implementation_prompt, plus any of strategy / architecture / test_strategy / rework).
- Ordered step titles with a one-line focus each.
- Acceptance criteria.

Ask for confirmation. Make corrections. Only then proceed to file generation.

## Output — files to create

Generate these files under `<plan folder>/`. Start every file from the matching template in `ec-plan/templates/` (read the template with `Read`, then `Write` the filled-in version).

Required:

- `<plan_name>.md` — overview, from `overview_template.md`. Fill purpose, workspace conventions, acceptance criteria, **execution order table** with every step (all `[ ]`), version control rule, scope guardrails, related docs list (remove links to docs that aren't being created).
- `<plan_name>.step<N>.md` — one per step, from `step_template.md`. Fill status, session rule, prerequisites (reference prior step(s) or "none"), goal, tasks, verifiable result, automated gate, notes for the agent.
- `implementation_prompt.md` — from `implementation_prompt_template.md`. Fill task name, paths, shell, runtime. Keep it short (≤ 50 lines).

Optional (only if confirmed in Round 2):

- `<plan_name>.strategy.md` — from `strategy_template.md`.
- `<plan_name>.architecture.md` — from `architecture_template.md`.
- `<plan_name>.test_strategy.md` — simple layered-gate doc; no template, write inline.
- `<plan_name>.rework_pre_step<N>.md` — from `rework_template.md`.

## Writing quality checklist

Apply these while generating files:

- **Step sizing.** Each step completable in one session (~1–4 hours). Split oversized steps into `stepN`, `stepNb`, `stepNc` (as in the reference plan).
- **Gates are executable.** Quote exact commands. If a gate is manual, say "Manual primary gate" and list supplementary automated checks.
- **Artifacts are named.** Every item in "Verifiable result" must name a concrete path or condition.
- **No forward references to steps that don't exist.** Each prerequisite points at a step file that is actually in the plan.
- **Overview table is complete.** Every step file has a corresponding row; ordering matches file numbering. Every row starts as `[ ]`.
- **Strategy / architecture stay read-only.** If you include them, add the note "read-only during execution; plan/step files are authoritative".
- **Plan folder holds docs only.** All implementation outputs go to the feature directory, not into the plan folder. State this in the overview's workspace conventions.
- **Destructive-VCS and bypass-gate guardrails.** Include them in both the overview's scope guardrails and the implementation prompt's constraints (see `plan_rules.md §11`).

## Final output to the user

When done, list:

1. The plan folder path.
2. Every file created.
3. A note: "Start implementation in a **new** session. In that session, open `implementation_prompt.md` to begin Step 1" (or mention the `ec-impl` skill if the user uses it).

Do **not** start implementation in the same session.

## Common variations

- **Plan without strategy.** Omit strategy file; put necessary rationale snippets inline in the overview's `## Purpose`.
- **Plan without architecture.** Inline the data model / artifact paths in the overview's `## Key deliverables` and in the step(s) that produce them.
- **Single-phase plan.** Skip phase exit sections in the overview.
- **Plan that evolves.** Leave room for `stepNb` / `stepNc` insertions. It is normal for a plan to grow interlude steps once implementation reveals complexity.

## Anti-patterns to avoid

- Generating files before the user has confirmed the step list.
- Writing 10+ steps when the task is small — prefer fewer, larger-but-still-sessioned steps, or drop the EC plan style entirely.
- Copy-pasting strategy content into every step file — link instead.
- Giving steps vague gates like "run the tests" without a concrete command.
- Forgetting to instruct the agent to stop after one step (this belongs in the implementation prompt and the step's session rule).

## Reference

- Style source plan: `ger_mode_cmds_plan2/` (authoritative copy under `ec-plan/ger_mode_cmds_plan2/` in this repo, or your `tools-talon/.../ger_mode_cmds_plan2/`) — read `ger_mode_cmds_plan2.md`, `implementation_prompt.md`, and a step file for a worked example.
- Rules: [`../ec-plan/plan_rules.md`](../ec-plan/plan_rules.md)
- Templates: [`../ec-plan/templates/`](../ec-plan/templates/)
