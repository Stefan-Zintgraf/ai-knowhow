# Coding

Notes and working documents on using **AI coding agents** safely in large, production-critical brownfield systems. Focus: the guardrails, phases, and workflows that surround an agent — not the tools themselves.

## Purpose

Develop a reusable system of guardrails and a phased planning workflow that constrains AI coding agents enough to make them trustworthy in real, complex codebases — instead of relying on vibe coding.

## Key Documents

| File                                               | Role                                                                               |
| -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [ai_coding_challenges.md](ai_coding_challenges.md) | Problem motivation — risks of coding agents in brownfield systems                  |
| [guardrails.md](guardrails.md)                     | Core rules + routing index to `gr/` detail docs                                    |
| [phases.md](phases.md)                             | Phase definitions (`ide → aln → res → pro → prd → iss → ral/par → qa → rev → ica`) |
| [coding_plan.md](coding_plan.md)                   | Operationalization tracker — skills, hooks, templates status                       |

## Folder Structure

```
gr/                  guardrail detail docs (one per category, loaded on demand)
wf/                  workflow docs (one per complex phase)
tpl/                 templates (PRD, issue, variant presentation, …)
skills/input/        skill authoring prompts (source, tool-managed)
skills/output/       compiled skill files (artifacts, tool-managed)
skills/test/         test fixture pairs per skill
.claude/skills/      meta-skills: skill authoring & project management
```

### `.claude/skills/` — meta-skills

Skills that drive the skill authoring pipeline and project dashboard:

Skills are listed in the order they are executed during a guardrail update (see [tutorial.md § Use-Case 2](tutorial.md#use-case-2-update-skills-after-guardrail-change)):

| Skill                   | Purpose                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------- |
| `draft-skill-input`     | Reads source docs and drafts an authoring prompt at `skills/input/<name>-in.md`.              |
|                         | Confirms skill name, strips phase-management concerns, requires HITL before writing.          |
| `compile-skill`         | Distils `skills/input/<name>-in.md` into a runtime skill at `skills/output/<name>.md`.        |
|                         | Detects input and spec-version drift; runs a self-check after writing. HITL on overwrite.     |
| `make-skill`            | Full build loop: draft → compile → verify requirements coverage → fix gaps (max 3 rounds).    |
|                         | Wraps `draft-skill-input` + `compile-skill`; preferred shortcut for step 3 of the workflow.   |
| `draft-skill-tests`     | Derives scenarios from source docs, proposes fixture pairs, gets human approval, then         |
|                         | writes `skills/test/<name>/input<NNN>.md` + `output<NNN>.md`. Does not run fixtures.          |
| `test-skill`            | Executes a compiled skill inline — freeform (live HITL) or fixture mode                       |
|                         | (runs `skills/test/<name>/test-plan.md`; LLM-as-judge, human confirms each verdict).          |
| `update-rule-skill-map` | Scans `gr/*.md`, `wf/*.md`, and `phases.md` for named rules; adds or corrects                 |
|                         | `Skills:` annotation lines per the `coding_plan.md` tables. Never invents mappings.           |
| `status`                | Runs 4 PowerShell scripts: reports current WI + phase, skill input/output staleness,          |
|                         | rule-skill map freshness, and next action. Saves to `.claude/skills/status/latest_status.md`. |
| `distill-idea`          | Extracts 3–6 major goals from a raw brief; no implementation details allowed.                 |
|                         | Persists to `plan/<WI>/idea.md` + `plan/<WI>/status_idea.md`. Entry point for a new work-item.|

> `skills/input/` and `skills/output/` are tool-managed — do not hand-edit.

## Guardrail update workflow

See [tutorial.md](tutorial.md) for the full step-by-step guide (new skill creation + guardrail update workflow).

Quick reference (skills run in this order):

```
1. Edit  gr/gr_<category>.md  (or guardrails.md)
2. /make-skill <name>          (per affected skill — draft → compile → verify)
3. /draft-skill-tests <name>   (if observable behavior changed)
4. /test-skill <name>          (run fixtures)
5. /update-rule-skill-map      (refresh Skills: annotations)
6. /status                     (verify all ✓)
```

## Status

Guardrail docs and phases: largely complete. Skills operationalizing the phases: in progress — see `coding_plan.md`.
