# TODO: Operationalize Guardrails as Skills

Purpose: convert the guardrails and workflow documents from prose-on-paper into enforceable behavior in the agent runtime. Each item below is a candidate **skill** (Claude Code `/skill` or equivalent), **hook**, **subagent**, or **prompt template**. The aim is to minimize always-on context cost (Op14a) by pulling detail only when triggered.

Source documents:

- `guardrails.md` — core rules + routing index.
- `gr/gr_*.md` — detail per category.
- `AI_Coding_Workflow.md` — phase flow and roles.
- `phases.md` — phase definitions.
- `videos/matt_pocock_full_walkthrough_workflow_gpt55pro.md` — workflow source.
- `..\skills-plugins\matt_pocock_skills\skills\<category>\<name>\SKILL.md` — Pocock reference skill bodies (categories: `engineering`, `productivity`, `in-progress`, `misc`, `personal`, `deprecated`). The walkthrough names are dated; the **current Pocock skill filenames are authoritative** (see [Pocock skill index](#pocock-skill-index) below).

## Pocock skill index (authoritative names, May 2026)

When a row in any table cites a "Pocock reference skill", the **current** SKILL.md is the source of truth — not the walkthrough phrasing. Index:

| Pocock skill                    | Path                                                        | Walkthrough phrasing                  |
| ------------------------------- | ----------------------------------------------------------- | ------------------------------------- |
| `grill-me`                      | `skills/productivity/grill-me/SKILL.md`                     | "grill me" (generic)                  |
| `grill-with-docs`               | `skills/engineering/grill-with-docs/SKILL.md`               | (new — grills against CONTEXT.md/ADR) |
| `to-prd`                        | `skills/engineering/to-prd/SKILL.md`                        | "write a PRD"                         |
| `to-issues`                     | `skills/engineering/to-issues/SKILL.md`                     | "PRD to issues"                       |
| `tdd`                           | `skills/engineering/tdd/SKILL.md`                           | Agentic TDD                           |
| `prototype`                     | `skills/engineering/prototype/SKILL.md`                     | (new — was unnamed in walkthrough)    |
| `review`                        | `skills/in-progress/review/SKILL.md`                        | "fresh-context automated review"      |
| `improve-codebase-architecture` | `skills/engineering/improve-codebase-architecture/SKILL.md` | "improve codebase architecture"       |
| `diagnose`                      | `skills/engineering/diagnose/SKILL.md`                      | (new — bug/perf diagnosis loop)       |
| `triage`                        | `skills/engineering/triage/SKILL.md`                        | (new — issue triage state machine)    |
| `zoom-out`                      | `skills/engineering/zoom-out/SKILL.md`                      | (new — broaden context)               |
| `handoff`                       | `skills/productivity/handoff/SKILL.md`                      | (new — session handoff)               |
| `write-a-skill`                 | `skills/productivity/write-a-skill/SKILL.md`                | (meta — relevant to our draft-skill)  |
| `caveman`                       | `skills/productivity/caveman/SKILL.md`                      | (style mode — already used here)      |

`/ralph` (referenced by W4) is a **separate** plugin, not part of `matt_pocock_skills` — keep its existing path note.

### Rule: New-skill authoring MUST load Pocock content

When authoring **any** new skill listed in this todo (A1–A11, B-series, etc.), the author chain (`draft-skill-input` → `compile-skill`) **must read the actual SKILL.md body** of every Pocock skill listed in the row's "Pocock reference skill" column — not only the walkthrough excerpt. Walkthrough phrasing is a hint; the current Pocock SKILL.md is the canonical externally-evolved reference. If the Pocock skill has been renamed, deprecated, or split, follow the rename / drop the obsolete reference / load all current splits.

Enforcement: `draft-skill-input` Step 4 (source-doc reading) is extended to include this — see that skill's SKILL.md.

---

## Table of Contents

- [Status legend](#status-legend)
- [Workflows](#workflows)
  - No new skill needed:
    - [W6. Agentic TDD](#w6-agentic-tdd)
    - [W14. Prototype Phase (broadened scope)](#w14-prototype-phase-broadened-scope)
      - [W14a. Sandbox Retirement Enforcement](#w14a-sandbox-retirement-enforcement)
      - [W14b. Variant Presentation Template](#w14b-variant-presentation-template)
      - [W14c. Res→Pro Fact Persistence Decision](#w14c-respro-fact-persistence-decision)
      - [W14d. Rejected-Variant Capture into align-concept](#w14d-rejected-variant-capture-into-align-concept)
      - [W14e. Prototype Skill (A9)](#w14e-prototype-skill-a9)
    - [W13. Research Caching](#w13-research-caching)
    - [W12a. Review Standards Guardrails Sources](#w12a-review-standards-guardrails-sources)
    - [W12b. Coding Standards – Descriptions + Preconditions (A+C)](#w12b-coding-standards--descriptions--preconditions-ac)
    - [W12c. Coding Standards – B1 Hook Enforcement](#w12c-coding-standards--b1-hook-enforcement)
  - New skill needed:
    - [W1. Grilled Design Concept](#w1-grilled-design-concept)
    - [W2. PRD](#w2-prd)
    - [W3. Issue DAG](#w3-issue-dag)
    - [W4. Ralph Once Loop](#w4-ralph-once-loop)
    - [W5. AFK Implementation Loop](#w5-afk-implementation-loop)
    - [W7. Fresh-Context Review](#w7-fresh-context-review)
    - [W8. Manual QA](#w8-manual-qa)
    - [W9. Deep-Module Architecture](#w9-deep-module-architecture)
    - [W10. Parallel Agents](#w10-parallel-agents)
- [A. Phase Skills (one per phase in `phases.md`)](#a-phase-skills-one-per-phase-in-phasesmd)
  - [A1. `align-concept` skill (phase: `aln`)](#a1-align-concept-skill-phase-aln)
  - [A2. `compose-prd` skill (phase: `prd`)](#a2-compose-prd-skill-phase-prd)
  - [A3. `prd-to-dag` skill (phase: `iss`)](#a3-prd-to-dag-skill-phase-iss)
  - [A4. `afk-loop` skill (phase: `ral`)](#a4-afk-loop-skill-phase-ral)
  - [A5. `parallel-loop` skill (phase: `par`)](#a5-parallel-loop-skill-phase-par)
  - [A6. `review` skill (phase: `rev`)](#a6-review-skill-phase-rev)
  - [A7. `arch-review` skill (phase: `ica`)](#a7-arch-review-skill-phase-ica)
- [B. Cross-Cutting Skills / Hooks](#b-cross-cutting-skills--hooks)
  - [B1. Routing-step enforcer](#b1-routing-step-enforcer)
  - [B2. Push-standards-to-reviewer](#b2-push-standards-to-reviewer)
  - [B3. Fresh-context-for-review](#b3-fresh-context-for-review)
  - [B4. HITL/AFK label gate](#b4-hitl-afk-label-gate)
  - [B5. Hidden-constraint checklist (alignment + review)](#b5-hidden-constraint-checklist-alignment--review)
  - [B6. Module-depth check](#b6-module-depth-check)
  - [B7. Fabrication check (Op13) as positive review step](#b7-fabrication-check-op13-as-positive-review-step)
  - [B8. Generated-code volume gate](#b8-generated-code-volume-gate)
  - [B9. Persistent-context minimizer](#b9-persistent-context-minimizer)
  - [B10. Subagent-for-exploration](#b10-subagent-for-exploration)
  - [B11. Subagent-for-artifact-drafting](#b11-subagent-for-artifact-drafting)
- [C. Templates and Conventions](#c-templates-and-conventions)
  - [C1. PRD template](#c1-prd-template)
  - [C2. Issue template with HITL/AFK tag and blocking edges](#c2-issue-template-with-hitlafk-tag-and-blocking-edges)
  - [C3. Review output template](#c3-review-output-template)
  - [C4. Alignment-transcript artifact format](#c4-alignment-transcript-artifact-format)
  - [C5. QA notes template](#c5-qa-notes-template)
  - [C6. Prototype variant presentation template](#c6-prototype-variant-presentation-template)
  - [C7. Research file template](#c7-research-file-template)
  - [C8. Idea file template](#c8-idea-file-template)
- [D. Open Questions / Decisions Before Building](#d-open-questions--decisions-before-building)
- [E. Validation / Experiments (from Pocock doc)](#e-validation--experiments-from-pocock-doc)

---

## Status

### Legend

- `todo` — not started.
- `wip` — in progress.
- `done` — implemented and tested.
- `blocked` — needs a decision first.

### work items

- [x] compile-skill 

- [x] test-skill (without the link)

- [x] draft-skill skill

### Phase Transition Mechanism (design session 2026-05-22)

Source: discussion settling how a fresh session learns "where we are + what's next" and how phase/mode transitions are recorded. Closes the gap noted while reading `phases.md`: mode-triage (Idea8) had no skill — `distill-idea` explicitly carves out Idea8–11 as caller concern.

**Artifacts folder convention.** All artifact paths in this document (and in `phases.md`, `guardrails.md`, `gr/*.md`, `tpl/*.md`) use `<artifacts>/` as the root folder for WI artifacts, the ACTIVE pointer, and INDEX.md. `<artifacts>` defaults to `plan` but is caller-supplied — skills receive it as an optional input parameter and pass it through to file operations. When no folder is given, `plan` is used.

**Settled decisions:**

- **State file**: `<artifacts>/<WI>/phase_status.md` — B-style (mutable `Current` block + reverse-chronological history, newest on top). Schema lives in a new template (see C-row below).
- **`Current` block fields**: `wi`, `issue`, `mode`, `current_phase`, `phase_status` (in-progress | blocked | awaiting-hitl | exited), `entered_at`, `next_phase` (computed at read), `blockers`, `tripwire_halt`, `last_actor`.
- **`next_phase` = hybrid**: file stores inputs only (`mode`, `current_phase`, `phase_status`, optional flags like `needs_research`, `pro_gate_tripped`); the value is computed at read time by `/phase status` against `phases.md` §4 chains. No persisted pointer = no drift.
- **Active-WI pointer**: `<artifacts>/ACTIVE` — single-line file containing `<N>_<slug>` or sentinel `<none>` (never absent). Written by agent at issue emission (Idea9). Cleared to `<none>` at WI close as part of the 3.33 retirement ritual. Q11 merge-gate lint: pointer must be empty OR point to an existing `<artifacts>/<N>_<slug>/` at PR-merge time. Worktree-scoped iff a worktree exists, else repo-global.
- **Write discipline**: a single dedicated skill `/phase` owns all writes to `phase_status.md` + `<artifacts>/ACTIVE`. Phase skills never touch these files directly; they call `/phase enter <code>` and `/phase exit <code>`. Centralizes schema, lint, HITL ack, tripwire-halt guard.
- **Fresh-session UX**: explicit — human runs `/phase status` to surface "current_phase, next_phase, blockers". No SessionStart hook, no CLAUDE.md auto-read (keeps always-on context cost low per Op14a). The skill reads `<artifacts>/ACTIVE` → reads that WI's `phase_status.md` → computes `next_phase`.
- **Idea8/Idea11 ownership**: a new `/triage-idea` skill (Idea8 = entry triage, Idea11 = mid-WI re-triage). Reusable: re-triage after 3.37 tripwire halt calls `/triage-idea --remode` alone, no re-distillation. Reverses the original carve-out only in the sense that Idea8–11 now have a skill home — `distill-idea` keeps its single responsibility (goal distillation).
- **Resulting `ide` chain by mode**:
  - direct-edit: `/phase enter ide` → `/triage-idea` → `/phase exit ide` (no `<artifacts>/<WI>/` created; issue body is the record).
  - mini / full: `/phase enter ide` → `/triage-idea` → `/distill-idea` → `/phase exit ide`.
  - mid-WI re-triage (Idea11): `/triage-idea --remode` standalone.

**New rows to add (tracking only — bodies not built yet):**

- **A-table**: `A12. /phase` (subcommands enter/exit/status) — covers W15a below. `A13. /triage-idea` — covers Idea8 + Idea11; called from `/phase enter ide` and standalone mid-WI.
- **B-table**: B1 routing-step-enforcer remains valid but its scope narrows — `/phase` skill is primary enforcement; B1 becomes the belt-and-suspenders hook that nags when a phase skill exits without calling `/phase exit`.
- **C-table**: `Cn. phase_status.md template` (`tpl/tpl_phase_status.md`) — frontmatter + `Current` block schema + history-section format.
- **W-table**: **W15a. Phase Transition Mechanism** — implements `/phase`, `/triage-idea`, `<artifacts>/ACTIVE` contract, `tpl_phase_status.md`. W15 reverts from `done` → `wip` (Idea8–11 skill home now in scope under W15a; `distill-idea` rework already pending from 2026-05-22 follow-up above).
- **D-table**: open question — does `status_idea.md` (Idea7) get folded into `phase_status.md`, or do both coexist with a pointer? Tentative: fold, with Idea7 rewritten to point at `phase_status.md`'s `Current` block.

**Enforcement chain (target):**

1. `/phase enter <code>` — checks: mode legal for this phase? Previous phase exited cleanly? Tripwire-halt clear?
2. `/phase exit <code>` — checks: phase-required artifacts present (e.g., `aln` exit requires `context.md` touched or ADR written per Aln17)? HITL ack recorded?
3. `/phase status` — read-only, computes `next_phase` from inputs.
4. B1 hook (later) — warns if a phase skill (A-row) ran but no `/phase` call followed in the same turn.

**Follow-up checklist (fresh session):**

- [x] Add A-table row **A12. `/phase`** (subcommands `enter` / `exit` / `status`; sole writer of `phase_status.md` + `<artifacts>/ACTIVE`). Source doc: this section. Workflow ref: W15a.
- [x] Add A-table row **A13. `/triage-idea`** (Idea8 entry triage + Idea11 mid-WI re-triage; `--remode` flag for standalone use). Source doc: `gr/gr_idea.md` Idea8–Idea11. Workflow ref: W15, W15a.
- [x] Add C-table row **`tpl_phase_status.md`** at `tpl/tpl_phase_status.md` — frontmatter + `Current` block schema + history-section format (B-style, reverse-chrono). Used by: A12, A13. Workflow ref: W15a.
- [x] Add D-table open question: **Idea7 `status_idea.md` migration** — fold into `phase_status.md` (tentative) vs. coexist with pointer. Blocks A12 schema lock-in.
- [x] Update B1 row in B-table — narrow scope to "belt-and-suspenders hook: warn if phase skill ran without `/phase` call in same turn." Source: this section.

- [x] Ideas to maybe add into gr_idea.md → added as Idea12 (Concept Sharpening). Kept 5 fields (problem, target user, core value, key assumptions, open questions) as persistent Context section in idea.md. Dropped 4 fields (working title, pitch = ephemeral; smallest useful version = Idea2 violation; current alternatives = res phase). "What makes it interesting" merged into core value.

- [x] **Rule-to-skill ownership annotations across source docs.** The skill toolchain (`draft-skill-tests`, `draft-skill-input`, `compile-skill`, `make-skill`) reads source docs (`gr/*.md`, `wf/*.md`, `phases.md`, `coding_plan.md`) to derive requirements for a target skill. Currently, rules within a source doc have no annotation saying which skill(s) they belong to. The mapping is n:m — one doc can serve multiple skills, and one skill pulls from multiple docs. Without rule-level ownership, toolchain skills cannot filter: they pick up all rules in a source doc even when only a subset belongs to the target skill, producing incorrect test fixtures or inflated requirement inventories. **Fix:** add a `Skills:` annotation (list of skill names, e.g., `Skills: distill-idea, triage-idea`) to each named rule/topic in every source doc (`gr/*.md` rules like `Idea1`, `Idea8`; `wf/*.md` steps; `phases.md` phase–skill bindings; `coding_plan.md` checklist items). Then update `draft-skill-tests` Step 1 (requirements inventory) to filter the inventory to only rules annotated with the target skill's ID. Same filter applies to `draft-skill-input` Step 4, `compile-skill` requirement checking, and `make-skill` Step 6a verification. The `coding_plan.md` Phase Skills table `Source doc` column already narrows by doc + rule range (e.g., "gr_idea.md Idea8–Idea11") — the annotation makes that narrowing machine-readable at the rule level inside the doc itself.

- [x] build A12 (`/phase` skill) — prerequisite for the two items below; see Phase Skills table for full spec
  - blocks: current-phase highlight in visualize-phase-chains; "Current WI + phase" block in status skill
  - [x] `/draft-skill-tests phase` — source docs: `coding_plan.md` §"Phase Transition Mechanism", `phases.md` §4+§5, `guardrails.md` §3.37, `gr/gr_idea.md` Idea8–Idea11
  - [x] `/make-skill phase` — internally chains `draft-skill-input` → `compile-skill` → test against fixtures; iterate until pass

- [x] visualize phase chains
  - render `phases.md` §4 sequence as an interactive diagram (not static ASCII)
  - show per-phase skill status (todo/wip/done/blocked) from `coding_plan.md` Phase Skills table
  - highlight current phase from `<artifacts>/ACTIVE` + `phase_status.md` `Current` block
  - show optional phases (`res`, `pro`) as conditional branches, gated by their entry flags (`needs_research`, `pro_gate_tripped`)
  - **lightest viable form**: a single-file HTML page (`phase-diagram.html` in repo root, next to `phases.md`) generated by a skill that reads `phases.md` + `coding_plan.md` + `<artifacts>/ACTIVE` — no server, no framework, open in browser
  - **blocked by**: A12 (`/phase`) for live state; usable before A12 as a static build-progress view

- [x] create status skill
  - **goal**: compact dashboard — current WI + phase, skill freshness, next action; one invocation replaces manually reading coding_plan.md + phase_status.md + git log
  - **goal**: use as many scripts as possible to make the skill deterministic (Powershell)
  - **script interface spec**: `plan/coding_workflow/skills/status/script-interfaces.md` (complete)
  - **implementation plan** — 3 steps:
    1. write 4 PowerShell scripts in `scripts/status/` per spec (no LLM involvement)
    2. wire into a `/status` skill that: parses Phase Skills table → builds `-SkillsJson` → invokes scripts → formats dashboard markdown
    3. register as user-invocable skill in CLAUDE.md
  - **scripts** (all emit JSON, all deterministic — see spec for full interfaces):
    - `Get-ActiveWI.ps1` — reads `<artifacts>/ACTIVE` + `phase_status.md` YAML frontmatter → `{wi, current_phase, phase_status, mode, blockers, tripwire_halt, error}`
    - `Get-SkillFreshness.ps1` — git timestamp comparison: source docs vs `skills/output/<name>.md` and `skills/input/<name>-in.md` → per-skill `{stale_compiled, stale_input, cmd}`
    - `Get-MapAndTestFreshness.ps1` — rule-skill map staleness (`gr/*.md` vs `skills/rule_skill_map.md`) + test fixture staleness (`skills/test/<name>/` vs source docs)
    - `Get-NextAction.ps1` — consumes outputs of above 3 scripts → priority-ordered action list
  - **what the LLM does** (not scriptable):
    - parse Phase Skills table from coding_plan.md into `-SkillsJson` (markdown table format may evolve)
    - format final dashboard as markdown (sections: Current WI, Skill Freshness, Next Action)
    - handle "A12 not yet built" warning: check `skills/output/phase.md` existence; if missing, skip WI block + print warning
  - **current WI + phase** (requires A12):
    - read `<artifacts>/ACTIVE` → resolve `<artifacts>/<WI>/phase_status.md` → print `current_phase`, `phase_status`, `mode`, `blockers`, `tripwire_halt`
    - if `<artifacts>/ACTIVE` = `<none>`: report "no active WI — run `/triage-idea` to start"
    - if A12 not yet built: skip this block, print warning
  - **skill freshness check** — for each skill listed in coding_plan.md Phase Skills table:
    - compare `git log -1 --format=%aI` of its source docs (`gr/*.md`, `wf/*.md`, `phases.md`) vs `skills/output/<name>.md`
    - if any source doc newer than compiled skill → flag as stale: "source changed, rerun `/make-skill <name>`"
    - if source doc changed but `skills/input/<name>-in.md` also stale → flag as stale input: "rerun `/draft-skill-input` first"
  - **rule-skill map freshness**: if any `gr/*.md` modified since `skills/rule_skill_map.md` last touched → flag: "run `/update-rule-skill-map`"
  - **test file check** — for each `skills/test/<name>/`:
    - if test fixtures exist but compiled skill is missing → flag: "skill not compiled"
    - if source docs newer than test fixtures → flag: "fixtures may be stale, rerun `/draft-skill-tests <name>`"
  - **next action** — priority order:
    1. any `tripwire_halt` set → surface blocker + `/triage-idea --remode`
    2. any stale rule-skill map → `/update-rule-skill-map`
    3. any stale skill inputs → `/draft-skill-input <name>` (list all)
    4. any stale compiled skills → `/make-skill <name>` (list all)
    5. all skills current → find first `- [ ]` item in coding_plan.md work items section, print it as next step
  - **output format**: sections (Current WI, Skill Freshness, Next Action); each stale item one line with the exact command to fix it
  
- [ ] re-create skills in output/skills (because of artifacts output folder dynamic now)
  - phase, next: test-skill phase
  - triage-idea: test-skill triage-idea
  - distill-idea: test-skill distill-idea


- [ ] check the workflow, specifically phases/idea - seems to be inconsistend or strange (start with triage instead of distill)

- [ ] create/update test files for triage-idea

- [ ] create/update test files for distill-idea

- [ ] in PRD or Issues phase: enforce to split the idea into reasonable independent modules 
  - maybe workflow then will be applied to each of the modules
  - check if free or open source solutions exist that make sense to integrate (solutions to enhance, libraries etc.)


- [ ] Create test cases at `skills/test/phase/` (paired `inputNNN.md` / `outputNNN.md` per `skills/test/distill-idea/` convention) covering: `enter` with legal mode, `enter` with mode mismatch (must reject), `exit` without required artifacts (must reject), `status` read on fresh WI, `status` read with tripwire_halt set, transition into optional phase (`res`/`pro` gate flags).
- [ ] Build A12 (`/phase`) end-to-end via `/make-skill phase` (chains `draft-skill-input` → `compile-skill` → test against `skills/test/phase/`, loops until pass). Source docs: this section, `gr/gr_idea.md`, `phases.md` §4, `guardrails.md` §3.37.
- [ ] Create test cases at `skills/test/triage-idea/` covering: 4-axis scoring on a trivial brief (expect `direct-edit`), tripwire surface in brief (expect `full`), `--remode` mid-WI upgrade with audit-trail append, HITL ack absent (must reject silent pick), Idea10 exploration-budget overflow (expect auto-recommend `mini`).
- [ ] Build A13 (`/triage-idea`) end-to-end via `/make-skill triage-idea` (chains `draft-skill-input` → `compile-skill` → test against `skills/test/triage-idea/`, loops until pass). Source docs: `gr/gr_idea.md` Idea8–11, `guardrails.md` §3.29 + §3.37, this section.
- [ ] Draft `tpl/tpl_phase_status.md` (the template itself, not the C-row tracking it).
- [ ] Define `<artifacts>/ACTIVE` Q11 merge-gate lint rule — add to `gr/gr_qa.md` (Q11 family) or wherever merge-gate checks live.
- [ ] Re-check `distill-idea-in.md` carve-out (L23, L51): with A13 now owning Idea8–11, the carve-out language stays valid — confirm no rewording needed when redrafting per 2026-05-22 follow-up above.

---

- [ ] coding_workflow: idea.md regeneration test (see idea_recreation.md)
  
  - [wip] /make-skill skill:  closed-loop drafting, compiling, testing skill iteration
    - change in coding_plan.md, guardrails.md, gr_xxxx.md etc.
    - /draft-skill-input A11/A1/...  --> skill/input/XXX-in.md
    - /compile-skill A11/A1/...  --> skill/output/XXX.md
    - check if all requirements from coding_plan.md, guardrails.md, gr_xxxx.md etc. are fulfilled (check item by item, especially the ones in the gr_XXX.md documents)
    - if something is missing: adjust /draft-skill-input skill or update input files (in case of updating input files, human confirmation is required)
    - if ok, then test the new skill using the test-skill skill
      - pre-condition: test files for the skill exist
      - test files are located in skills/test/XXXX (XXXX is the skill name)
      - input files given to the skill are input000.md, input001.md, etc.
      - result files that are a reference to the skill output are output000.md, output001.md, etc.
      - test shall then check if the generated output matches the test output files
      - if test fails, fix with same strategy as for the draft/compile step

- [ ] re-run grill-with-docs pocock original skill with this repo, check result

- [~] Update workflow/guardrails/skills-to-use based on: https://www.youtube.com/watch?v=6BB6exR8Zd8 
  
  - [x] **partial (2026-05-21)**: doc layer landed 
    
    - `gr/gr_adr.md` new; `gr_domain_language.md` L8+L9 added; 
    - `gr_algn.md` Aln17 added; 
    - `guardrails.md` §3.34/3.35 + §4.20 + §9 parallel rows added; 
    - `phases.md` `aln` description updated to note `context.md`/ADR maintenance).
  
  - [~] **Skill layer pending** 
    
    - **(2026-05-21)** Contracts for A1 settled in this /grill-with-docs session — see W1 "Contracts settled" block. `idea.md` consumption resolved (Aln8 extended: verbatim anchor + per-branch goal-tag + close-time coverage). W16 + W17 fold into A1 (Aln17 #5–#7).
    - `skills/input/align-concept-in*.md` and `skills/output/*.md` still deliberately not edited (user constraint).

- [x] update sequence in workflows table — W16 (ADR) + W17 (context.md) confirmed as sub-rules A1 implements per Aln17; both stay as separate rows for tracking but their work is gated by W1 (A1) build.

- [ ] Call draft-skill-input for all missing (or to be updated) skills

- [x] /grill-with-docs session 2026-05-22 — entry-triage design settled (C1–C12). **Migrated to detail docs** same session: Idea8/9/10/11 (`gr/gr_idea.md`), TDD11 (`gr/gr_tdd.md`), Aln19 (`gr/gr_algn.md`), Q12 (`gr/gr_qa.md`), new core rule §3.37 + amended §3.22/§3.29 + §9 parallel rows (`guardrails.md`). `plan/coding_workflow/idea.md` cleaned (Settled Contracts section replaced with pointer); `idea_ref.md` re-snapshotted from the cleaned file as the distill-idea baseline.

- [x] run-skill stores output in `./skills/run/plan/` (caller-supplied `<artifacts>` = `./skills/run/plan`)


- [ ] **Follow-up from 2026-05-22 contracts:** redraft `skills/input/distill-idea-in.md` via `draft-skill-input` against the *updated* anchor docs (Idea8–Idea11 now in gr_idea.md); recompile via `compile-skill`. Diff new `distill-idea` output against `plan/coding_workflow/idea_ref.md` to assess skill-chain determinism. The skill's job is goal distillation; if its output diverges from the goals in `idea_ref.md`, that is the signal — not whether C1–C12 appear in the output (they live in detail docs now, not in `idea.md`).

- [ ] implement all required skills,hooks,templates including related test files and, if needed, additional workflow files etc. for the below workflow table 

- [ ] make this project to a generic workflow builder
  - **Blocked**: finish at least A12 (`/phase`) first — it's the cleanest separation point with zero coding-specific content; extracting before it exists means extracting a moving target.
  - [ ] define `domain.yaml` / `domain.md` — declares phase list, per-phase skill bindings, triage axis labels, and which guardrail docs apply; replaces hardcoded coding assumptions in `phases.md` and the 4-axis triage matrix
  - [ ] extract framework layer from domain layer — `draft-skill-input` reads coding-specific source docs directly; add domain-neutral "which docs apply to this phase" indirection (the `Skills:` annotation work already in progress is the foundation)
  - [ ] add `/init-workflow <domain>` bootstrap skill — scaffolds `phases.md`, `guardrails.md`, and `gr/` stubs from a domain config; equivalent of what currently requires manual setup
  - [ ] parameterize triage matrix axes — "existing test coverage" → "existing validation coverage"; axis labels in domain config, not hardcoded in `gr_idea.md`


---

### Workflows table

| #    | Pocock title                   | Category                   | Status          | skill    | hook       | Pocock reference skill                       | Maps to                               |
| ---- | ------------------------------ | -------------------------- | --------------- | -------- | ---------- | -------------------------------------------- | ------------------------------------- |
| W15  | Idea Phase                     | **NEW Phase**              | wip             | A11, A13 | —          | none — Pocock phase 1 (7-phases doc)         | `ide` added, `gr_idea.md` drafted,    |
|      |                                |                            |                 |          |            |                                              | §3.32 + §4.19 added; Idea8/11 home    |
|      |                                |                            |                 |          |            |                                              | now in A13 (`/triage-idea`)           |
| W15a | Phase Transition Mechanism     | **NEW Infra**              | todo            | A12, A13 | B1 (later) | none                                         | `/phase` skill + `<artifacts>/ACTIVE` +      |
|      |                                |                            |                 |          |            |                                              | `tpl_phase_status.md`; see section    |
|      |                                |                            |                 |          |            |                                              | "Phase Transition Mechanism" above    |
| W1   | Grilled Design Concept         | Phase                      | todo            | A1       | —          | `grill-me` + `grill-with-docs`               | `aln` (exists)                        |
| W13  | Research Caching               | Phase (optional)           | wip             | A10      | TBD        | none named — Pocock phase 2                  | `res` added, `gr_res.md` drafted,     |
|      |                                |                            |                 |          |            | + `research.md` cache                        | §3.27 + §4.17 added                   |
| W14a | Sandbox Retirement             | Enforcement (W14)          | todo            | —        | TBD        | none                                         | adapt W13's `owner-issue`+Q11 to dirs |
| W14b | Variant Template               | Template (C6, W14)         | done            | —        | —          | none                                         | see [C6](tpl/tpl_var_pres.md)         |
| W14c | Res→Pro Fact Persistence       | Decision (D-new, W14)      | done            | —        | —          | none                                         | `res`/`pro` boundary                  |
| W14d | Rejected-Variant→align-concept | Wiring (W14)               | done (contract) | —        | —          | none                                         | A1 (`align-concept`) integration      |
| W14e | Prototype Skill                | **NEW Phase** / Skill (A9) | wip             | A9       | —          | `prototype` (new in Pocock — load body)      | `pro` added, `gr_proto.md`            |
|      |                                |                            |                 |          |            |                                              | + `wf/wf_proto.md`                    |
| W2   | PRD                            | Phase                      | todo            | A2       | —          | `to-prd` (was "write a PRD")                 | `prd` (exists)                        |
| W3   | Issue DAG                      | Phase                      | todo            | A3       | —          | `to-issues` (was "PRD to issues") + `triage` | `iss` (exists)                        |
| W4   | Ralph Once Loop                | Execution mode             | todo            | A4       | —          | `/ralph` skill (`~/.claude/skills/ralph/`)   | variant of `ral`                      |
| W5   | AFK Implementation Loop        | Phase                      | blocked         | A4       | B4, B8     | none — `afk.sh` loop script (not a skill)    | `ral` (exists), D4 open               |
| W10  | Parallel Agents                | Execution mode             | blocked         | A5       | —          | none — Sand Castle orchestration tool        | `par` (exists), substrate TBD         |
|      |                                |                            |                 |          |            | (not a skill)                                |                                       |
| W6   | Agentic TDD                    | Technique                  | done            | —        | B1         | `tdd`                                        | `gr/gr_tdd.md` + §4.16 routing        |
| W8   | Manual QA                      | **NEW Phase**              | wip             | A8       | —          | none — human-driven phase                    | `qa` added, `gr_qa.md` drafted        |
|      |                                |                            |                 |          |            | in Pocock's walkthrough                      |                                       |
| W7   | Fresh-Context Review           | Phase                      | todo            | A6       | B3         | `review` (in-progress — load body)           | `rev` (exists)                        |
| W9   | Deep-Module Architecture       | Phase/Initiative           | todo            | A7       | —          | `improve-codebase-architecture`              | `ica` (exists), D7 open               |
| W12a | Review Standards Sources       | Manual / Audit             | todo            | —        | —          | —                                            | `standards_guardrails_sources.md`     |
| W12b | Standards Descriptions         | Rule/Convention            | todo            | TBD      | —          | —                                            | Op14b + `gr/` description quality     |
|      |                                |                            |                 |          |            |                                              | + skill preconditions                 |
| W12c | Standards Hook Enforcement     | Rule/Convention            | todo            | —        | B1         | —                                            | B1 routing-step enforcer              |
| W16  | ADR Capture (3.34)             | Rule/Convention            | wip             | —        | TBD        | `grill-with-docs`                            | `gr/gr_adr.md` added;                 |
|      |                                |                            |                 |          |            | — for the ADR-during-grilling pattern        | §3.34 + §4.20 + §9 row;               |
|      |                                |                            |                 |          |            |                                              | A1 must implement Aln17 ADR-drafting; |
|      |                                |                            |                 |          |            |                                              | A6 must verify Adr10 coverage         |
| W17  | context.md + CLAUDE.md         | Rule/Convention            | wip             | —        | —          | `grill-with-docs` (same)                     | `gr_domain_language.md`               |
|      | ptr (3.35)                     |                            |                 |          |            | — `context.md` is its anchor file            | L8+L9 added;                          |
|      |                                |                            |                 |          |            |                                              | §3.35 + §9 row;                       |
|      |                                |                            |                 |          |            |                                              | A1 must implement Aln17               |
|      |                                |                            |                 |          |            |                                              | read/update of `context.md`           |

### Phase Skills table

| #   | Skill name      | Phase | Status  | Source doc                                                   | Workflow ref | Depends on                    |
| --- | --------------- | ----- | ------- | ------------------------------------------------------------ | ------------ | ----------------------------- |
| A11 | `distill-idea`  | `ide` | todo    | [gr_idea.md](gr/gr_idea.md)                                  | W15          | —                             |
| A1  | `align-concept` | `aln` | todo    | [gr_algn.md](gr/gr_algn.md)                                  | W1           | —                             |
| A10 | `do-research`   | `res` | todo    | [gr_res.md](gr/gr_res.md)                                    | W13          | B10, C7 (template)            |
| A9  | `prototype`     | `pro` | todo    | [gr_proto.md](gr/gr_proto.md), [wf_proto.md](wf/wf_proto.md) | W14e         | W14a (sandbox), W14b (C6 tpl) |
| A2  | `compose-prd`   | `prd` | todo    | [gr_algn.md](gr/gr_algn.md)                                  | W2           | A1, C1 (template), D3 ✓       |
| A3  | `prd-to-dag`    | `iss` | todo    | [gr_tdd.md](gr/gr_tdd.md)                                    | W3           | A2, C2 (template)             |
| A4  | `afk-loop`      | `ral` | todo    | [gr_tdd.md](gr/gr_tdd.md)                                    | W4, W5       | A3, D4 (sandbox)              |
| A5  | `parallel-loop` | `par` | blocked | —                                                            | W10          | D4 (sandbox), substrate TBD   |
| A8  | `qa`            | `qa`  | wip     | [gr_qa.md](gr/gr_qa.md)                                      | W8           | A4, C5 (template)             |
| A6  | `review`        | `rev` | todo    | [gr_rev.md](gr/gr_rev.md)                                    | W7           | B2, B3, B6, B7                |
| A7  | `arch-review`   | `ica` | todo    | [gr_mod.md](gr/gr_mod.md)                                    | W9           | D7 (proactive vs reactive)    |
| A12 | `phase`         | —     | todo    | coding_plan.md §"Phase Transition Mechanism"                         | W15a         | —                             |
| A13 | `triage-idea`   | `ide` | todo    | [gr_idea.md](gr/gr_idea.md) Idea8–Idea11                     | W15, W15a    | A12                           |

### Cross-Cutting Skills / Hooks table

| #   | Name                             | Form            | Status | Source doc                                                          | Applies to          | Used by         |
| --- | -------------------------------- | --------------- | ------ | ------------------------------------------------------------------- | ------------------- | --------------- |
| B1  | `routing-step-enforcer`          | hook (pre-task) | todo   | [guardrails.md §5](guardrails.md); coding_plan.md §"Phase Transition Mechanism" | `ral`,`par` (narrowed) | A4, A5 (belt-and-suspenders: warn if phase skill ran without `/phase` call in same turn) |
| B2  | `push-standards-to-reviewer`     | skill           | todo   | [gr_rev.md](gr/gr_rev.md) Rev2; Op14b                               | `rev`               | A6              |
| B3  | `fresh-context-for-review`       | hook            | todo   | [gr_rev.md](gr/gr_rev.md) Rev1; 3.18                                | `rev`               | A6              |
| B4  | `hitl-afk-label-gate`            | hook (pre-task) | todo   | [guardrails.md](guardrails.md) Gov5a, 3.20                          | `iss`, `ral`, `par` | A3, A4, A5      |
| B5  | `hidden-constraint-checklist`    | skill           | todo   | [gr_algn.md](gr/gr_algn.md) Aln6; [gr_rev.md](gr/gr_rev.md) Rev7    | `aln`, `rev`        | A1, A6          |
| B6  | `module-depth-check`             | skill           | todo   | [gr_mod.md](gr/gr_mod.md) M7; Rev6                                  | `rev`, `ica`        | A6, A7          |
| B7  | `fabrication-check`              | skill           | todo   | [guardrails.md](guardrails.md) Op13; [gr_rev.md](gr/gr_rev.md) Rev8 | `rev`               | A6              |
| B8  | `generated-code-volume-gate`     | hook (pre-edit) | todo   | [guardrails.md](guardrails.md) Op11                                 | `ral`, `par`        | A4, A5          |
| B9  | `persistent-context-minimizer`   | skill / audit   | todo   | [guardrails.md](guardrails.md) Op14a, 3.17                          | all (maintenance)   | —               |
| B10 | `subagent-for-exploration`       | skill           | todo   | [gr_algn.md](gr/gr_algn.md) Aln7                                    | `aln`, `res`        | A1, A10         |
| B11 | `subagent-for-artifact-drafting` | skill           | todo   | [gr_algn.md](gr/gr_algn.md) Aln17; [gr_adr.md](gr/gr_adr.md) Adr5   | `aln`, `prd`, `rev` | A1, A2, A6      |

### Templates and Conventions table

| #   | Name                              | Status | Artifact                                   | Source doc                                     | Used by                 | Workflow ref |
| --- | --------------------------------- | ------ | ------------------------------------------ | ---------------------------------------------- | ----------------------- | ------------ |
| C1  | PRD template                      | todo   | —                                          | [gr_algn.md](gr/gr_algn.md)                    | A2                      | W2           |
| C2  | Issue template (HITL/AFK + edges) | todo   | —                                          | [gr_tdd.md](gr/gr_tdd.md)                      | A3                      | W3           |
| C3  | Review output template            | todo   | —                                          | [gr_rev.md](gr/gr_rev.md) Rev11                | A6                      | W7           |
| C4  | Alignment-transcript format       | todo   | —                                          | [gr_algn.md](gr/gr_algn.md) Aln12, Aln15       | A1                      | W1           |
| C5  | QA notes template                 | todo   | —                                          | [gr_qa.md](gr/gr_qa.md)                        | A8                      | W8           |
| C6  | Prototype variant template        | done   | [tpl/tpl_var_pres.md](tpl/tpl_var_pres.md) | [gr_proto.md](gr/gr_proto.md) Pro4, Pro7, Pro8 | A9, A1 (rejected carry) | W14b         |
| C7  | Research file template            | todo   | —                                          | [gr_res.md](gr/gr_res.md) Res4                 | A10                     | W13          |
| C8  | Idea file template                | done   | [tpl/tpl_idea.md](tpl/tpl_idea.md)         | [gr_idea.md](gr/gr_idea.md) Idea7              | A11, A1, A2, A6, A8     | W15          |
| C9  | Phase status template             | todo   | `tpl/tpl_phase_status.md`                  | coding_plan.md §"Phase Transition Mechanism"          | A12, A13                 | W15a         |

---

## Workflows

Source: `videos/matt_pocock_full_walkthrough_workflow_gpt55pro.md` §"Workflows and Methods" (12 items, W1–W12). Extensions from the 7-phases doc add `res` (W13), `pro` (W14/W14a–e), and `ide` (W15).

Pocock's 12 items mix **phases** (sequential delivery steps), **techniques** (used inside a phase), **execution modes** (variants of an impl phase), and **rules/conventions** (cross-cutting). Categorization summary:

Order below follows the typical phase sequence from `phases.md` §4: `aln → res → pro → prd → iss → ral/par → qa`, then cross-phase (`rev`, `ica`), then cross-cutting standards.

Each item below: **what exists**, **what's missing**, **next step**. Detail per item handled in a fresh chat context.

Beyond the 12 items, the orchestration that chains them (e.g., `align-concept` → `compose-prd` → `prd-to-dag`) remains a separate concern — a future `workflow.md` + `wf/` folder is a candidate, mirroring the `guardrails.md` + `gr/` split. Not started.

---

### No new skill needed

### W6. Agentic TDD

- Status: **done** (guardrail authored; skill-precondition wiring follows when A4 is built).
- Category: **Technique** (used inside `ral`/`par`).
- Artifact: [`gr/gr_tdd.md`](gr/gr_tdd.md) — Red-Green-Refactor loop, false-green verification (TDD2), fail-for-right-reason (TDD3), minimum-code Green (TDD4), mandatory Refactor (TDD5), mock discipline (TDD6), one-Red-at-a-time (TDD7), FE/visual applicability (TDD8), no retroactive tests (TDD9), refactor must not change behavior (TDD10).
- Pull-enforcement: §4.16 routing index entry in `guardrails.md` (Opt A) + A4 `afk-loop` skill precondition (Opt B, pending A4 build). Hook-based enforcement (Opt C) deferred.
- Side-edits: T12/T12a removed from `gr_testing_verification.md` (single source of truth); §3.22 link retargeted to `gr_tdd.md`; §9 parallel table row updated to `TDD1, TDD2`.
- Follow-up: when A4 (`afk-loop`) skill is built, its prompt must load `gr_tdd.md` on `ral` entry before first edit (TDD section "Pulling This Document" #2).
- Pocock skill as additional input (for B1 enforcement design + A4 wiring): load `tdd` SKILL.md body (`skills/engineering/tdd/SKILL.md`). Cross-check our TDD1–TDD10 against Pocock's red-green-refactor rules — discrepancies should be reconciled before B1 hook is built.

### W14. Prototype Phase (broadened scope)

- Status: **wip** (phase + core rule + detail doc + workflow doc done; remaining work split into W14a–W14e, each handled in a fresh session).
- Category: **Phase (optional)** — code `pro`. Optional sequential between `aln`/`res` and `prd`; entry from either `aln` (design ambiguity) or `res` (build-to-learn spike). HITL only (Pro6).
- Pocock reference: phase 3 of the 7-phases doc (see [the-7-phases-of-ai-driven-development.md](the-7-phases-of-ai-driven-development.md)) — "Prototype as Taste-Imposition Step" + "Prototype Variant Generation". **Pocock now ships a `prototype` skill** (`skills/engineering/prototype/SKILL.md`): routes between (a) a runnable terminal app for state/business-logic questions, or (b) several radically different UI variations toggleable from one route. Compare to our Pro2 flavors (FE/UX, architecture, integration) — Pocock collapses architecture+integration into the "terminal app" branch. Author A9 must load this SKILL.md and reconcile.
- Exists: phase `pro` in [phases.md](phases.md); core rule 3.28 + routing §4.18 + parallel-table row in [guardrails.md](guardrails.md); detail doc [gr/gr_proto.md](gr/gr_proto.md) (Pro1–Pro8); workflow doc [wf/wf_proto.md](wf/wf_proto.md) covering all three flavors; cross-ref Res10 in [gr/gr_res.md](gr/gr_res.md).
- Trigger gate (Pro1): irreversibility OR cost asymmetry. Replaces the deleted Aln17 "genuinely visual" gate.
- Flavors (Pro2): FE/UX, architecture, integration — one flavor per `pro` invocation.
- Remaining work: see W14a (sandbox retirement), W14b (variant template), W14c (res→pro fact persistence), W14d (rejected-variant→align-concept wiring), W14e (skill).
- Resolves: D8-bis (prototype as phase, not technique). Pocock alignment confirmed.

### W14a. Sandbox Retirement Enforcement

- Status: **todo** (fresh session).
- Parent: W14.
- Behavior: design and implement retirement enforcement for prototype sandbox **directories** (not single files). Adapt W13's pattern: `owner-issue` provenance field in a manifest file at the sandbox root + `qa` Q11-style merge-gate check that fails if any sandbox path survives merge without its owner-issue being closed. Sandbox = directory, so the check must walk directory trees, not just grep for a file header.
- Source: W13 resolution (see `consider_7_phases_todo.md` Item 8); Pro3 (deletion rule); gr_proto.md.

### W14b. Variant Presentation Template

- Status: **done** (2026-05-18).
- Parent: W14.
- Slot: **C6**. C5 reserved for W8 QA notes template.
- Artifact: [`tpl/tpl_var_pres.md`](tpl/tpl_var_pres.md) — first template in a new `tpl/` folder (parallel to `gr/`, `wf/`).
- Format: YAML frontmatter (machine-parseable schema) + markdown body (human-readable). Skill (W14e) owns YAML; human edits body only.
- Pro4 enforcement: schema **omits** `recommendation`/`preferred`/`best`/`agent_pick`/`score`/`ranking` fields and **lists them as forbidden** (schema rejects). Body rules forbid subjective vocabulary (better, worse, cleaner, simpler, recommended, preferred, ideally, obviously, clearly, the right/wrong choice). Reviewer (`rev`) flags any occurrence.
- Pro7 coverage: per-variant `hidden_constraints` block requires all 7 classes (security, permissions, retention, migrations, observability, api_compat, concurrency) marked covered / not_applicable / missing. `blocking_constraint` set when any = missing.
- Pro8 coverage: `captured_responses` field on each variant for integration flavor; no synthetic-payload field.
- Cross-refs: `gr/gr_proto.md` Pro4 + `wf/wf_proto.md` step 5 point at C6 as the artifact.
- Validation hooks (deferred to D1): schema lint (forbidden fields, variant count, trigger flag, hidden-constraint completeness); vocabulary lint (body subjective terms); sandbox-retirement gate hook to W14a via `owner_issue` field.
- Dependents: W14e (A9 skill emits this); W14d (rejected-variant artifact for align-concept intake — `decision_outcome.rejected` is the carry).

### W14c. Res→Pro Fact Persistence Decision

- Status: **done** (2026-05-18).
- Parent: W14.
- Decision: **Option B — caller-persists, applied symmetrically to all callers.** `pro` emits exactly one artifact (C6 variant doc, [`tpl/tpl_var_pres.md`](tpl/tpl_var_pres.md)) with chosen variant marked and `captured_responses` populated where applicable. The caller (`aln`/`res`/`prd`) reads C6 on return and updates its own files: `aln` → Aln12 module map + Aln15; `res` → `research/<topic>.md` under existing `owner-issue` (Res4) header; `prd` → implementation-decisions section + rejected-alternatives. `pro` never writes any caller's files directly.
- Rationale: keeps `pro` caller-agnostic (one behavior, no conditional write-mode per caller); each phase keeps ownership of its file conventions; one handoff surface (C6) instead of three.
- Edits: `gr/gr_proto.md` Pro5 (rewritten — symmetric caller-persists for all three callers); `gr/gr_res.md` Res10 (concrete Stripe-webhook handoff example); `wf/wf_proto.md` step 7 (rewritten — same symmetric rule).
- Affects: A9 (W14e) skill prompt must emit C6 artifact only — must NOT write `research/<topic>.md`, Aln12, Aln15, or PRD sections directly. Caller does the writing.

### W14d. Rejected-Variant Capture into align-concept

- Status: **done — contract** (2026-05-18). Skill wiring lands when A1 is built (W1).
- Parent: W14.
- Artifact format: reuses C6 (`tpl/tpl_var_pres.md`) `decision_outcome.rejected[]` + `rationale_by_human` — no new artifact needed.
- Intake contract (gr_algn.md Aln15, expanded section "Intake from `pro`"): on `aln` resume after `pro` exit, A1 reads `<sandbox_path>/variants.md` **before** sandbox deletion; for each rejected id appends an Aln15 entry citing variant summary + observable losing facts + `rationale_by_human`; updates Aln12; signals capture complete to unblock Pro3 deletion. Fail-closed if C6 unreadable or `decision_outcome.chosen` null.
- Replay contract: existing Aln15 entries load as grilling context; A1 does not re-propose rejected options — cites prior rejection if branch reopened.
- Ordering enforced: gr_proto.md Pro3 + wf_proto.md step 8 now block sandbox deletion until caller capture signals complete.
- Edits: `gr/gr_algn.md` Aln15 (expanded with intake + replay contracts); `gr/gr_proto.md` Pro3 (ordering with caller capture); `wf/wf_proto.md` step 8 (fail-closed); `tpl/tpl_var_pres.md` Notes on Interaction (caller-persists + read-before-delete).
- Depends on: W14e (A9 emits C6 — schema already defined). W1 (A1 implementation) consumes this contract.

### W14e. Prototype Skill (A9)

- Status: **todo** (fresh session).
- Parent: W14.
- Behavior: `prototype` skill that (1) asks Pro1 trigger-gate questions (irreversibility / cost asymmetry), (2) generates 2–3 variants per the chosen flavor (Pro2: FE/UX, architecture, integration), (3) runs Pro7 hidden-constraint check on each variant, (4) presents variants to human with observable-facts-only framing (Pro4), (5) captures Aln15 negative decisions for rejected variants, (6) enforces Pro3 deletion of sandbox code after decision.
- Maps to: A9 (new skill slot); source docs `gr/gr_proto.md`, `wf/wf_proto.md`.
- Pocock skill as additional input: load `prototype` SKILL.md body (`skills/engineering/prototype/SKILL.md`) when authoring A9.
- Dependency: W14a (sandbox retirement) and W14b (variant template) should be resolved first or in parallel.

### W15. Idea Phase

- Status: **wip** (phase + core rule + detail doc done; **charter widened 2026-05-22**; skill pending).
- Contracts settled (2026-05-22 /grill-with-docs session, full transcript in [plan/coding_workflow/idea.md](plan/coding_workflow/idea.md) "Settled Contracts" section — C1–C12):
  - **`ide` is the entry phase** — always runs; owns triage + (conditional) goal distillation + issue emission. (C1)
  - **Three modes** — `direct-edit` / `mini` / `full`, each with a fixed downstream phase sequence. (C2)
  - **4-axis triage matrix** — design ambiguity, blast radius, reversibility, existing test coverage; tripwire surfaces (3.29 list) force `full`. HITL approves mode. (C3)
  - **TDD exemption** — direct-edit may skip TDD if existing tests sufficient + HITL confirm; behavior-free changes verified by lint + spell-check + HITL eyeball. Amends 3.22 / TDD3. (C4)
  - **Issue invariant** — exactly one issue exists before any `ral`; `ide` emits for direct-edit/mini, `iss` for full. (C5)
  - **`<artifacts>/<WI>/` scales with mode** — direct-edit creates no files (issue is the record); mini/full create `<artifacts>/<N>_<slug>/`. (C6)
  - **Tripwire mid-task → halt + HITL** — candidate core rule 3.37; agent halts, does not edit, human picks narrow-with-approval or re-enter `ide`. (C7)
  - **Collapsed `aln` for mini** — keeps Aln6 sweep + Aln17 context.md/ADR; reduces grilling to 1–3 questions; skips Aln18 transcript file. Auto-upgrades to full on Adr1/Pro1/>3 unresolved. (C8)
  - **`<WI>` = `<N>_<slug>`** — N = GH issue number, slug from title; dedupe via `gh issue list --search` shown to human before create; `<artifacts>/INDEX.md` auto-generated. (C9)
  - **`ide`-time exploration** — B10 reused with ≤5-read budget; budget exceeded → mode upgrade to mini. (C10)
  - **`qa` shape by mode** — direct-edit folds qa into ral's verification record; mini = short qa; full = full qa. (C11)
  - **Mode transitions** — symmetric: either direction, either party may propose, HITL approves either direction. Silent change AND silent suppression both forbidden (3.16). (C12)
- Category: **Phase** — code `ide`. Sequential, **first** phase before `aln`. HITL only (Idea4). Output is `<artifacts>/<WI>/idea.md` + `<artifacts>/<WI>/status_idea.md` (Idea7); retired with `<artifacts>/<WI>/` at WI close per 3.33. PRD Goals section folds it but does not replace it. **Note (2026-05-22):** for `direct-edit` mode the GH issue body replaces `idea.md` — no `<artifacts>/<WI>/` files created (C6).
- Pocock reference: phase 1 of the 7-phases doc (see [the-7-phases-of-ai-driven-development.md](the-7-phases-of-ai-driven-development.md)) — no named Pocock skill.
- Exists: phase `ide` in [phases.md](phases.md); core rule 3.32 + routing §4.19 in [guardrails.md](guardrails.md); detail doc [gr/gr_idea.md](gr/gr_idea.md) (Idea1–Idea7).
- Missing: skill `distill-idea` (new **A11**) — distills brief / ticket / Slack note into 3–6 major goals, strips detail leaks (Idea2), captures negative goals (Idea3), HITL by construction (Idea4); collapse handling per 3.29 when upstream brief already names goals explicitly (one-line confirmation instead of full pass); writes `<artifacts>/<WI>/idea.md` + `<artifacts>/<WI>/status_idea.md` per Idea7.
- Template **C8** (`tpl/tpl_idea.md`) for `idea.md` + `status_idea.md` shape — consumed by A1/A2/A6/A8 + Q11 lint, so canonical shape lives outside the skill.
- Next: build A11 skill; wire as front of skill chain (A11 → A1 align-concept → A2 compose-prd → ...).

### W13. Research Caching

- Status: **wip** (phase + core rule + detail doc + retirement enforcement done; skill, template pending).
- Category: **Phase (optional)** — code `res`. Optional sequential between `aln` and `prd`; can also fire mid-`aln` when grilling stalls on external-dependency facts.
- Pocock reference: phase 2 of the 7-phases doc (see [the-7-phases-of-ai-driven-development.md](the-7-phases-of-ai-driven-development.md)) — no named Pocock skill.
- Exists: phase `res` in [phases.md](phases.md); core rule 3.27 + routing §4.17 in [guardrails.md](guardrails.md); detail doc [gr/gr_res.md](gr/gr_res.md); subagent dispatch B10 (existing); retirement enforcement = `owner-issue` provenance field (Res4) + pre-commit lint + `qa` Q11 merge-gate check (resolved 2026-05-18, see `consider_7_phases_todo.md` Item 8).
- Missing: skill `do-research` (new **A10** — A9 taken by W14e prototype) — gathers facts via subagent, writes `research/<topic>.md` with Res4 provenance header; template (new **C7** — C6 taken by W14b variant template) for the research file shape including the `owner-issue` field; decision on whether `iss` decomposition should reference the research file path explicitly; pre-commit lint implementation (mechanical, deferred to substrate decision D1).
- Next: build A10 + C7; wire B10 dispatch into A1 (`align-concept`) so alignment can spawn research without leaving `aln`; implement the `owner-issue` lint once skill substrate (D1) is settled.

### W12a. Review Standards Guardrails Sources

- Status: todo.
- Category: **Manual / Audit** (precondition for W12b).
- Behavior: review external sources before authoring/adjusting `gr/` descriptions. See [standards_guardrails_sources.md](standards_guardrails_sources.md).
- Next: complete the source review, then proceed to W12b.

### W12b. Coding Standards – Descriptions + Preconditions (A+C)

- Status: todo.
- Category: **Rule / Convention** (cross-cutting).
- Approach: (A) improve `gr/*.md` descriptions so routing step (§5) reliably surfaces the right doc; (C) each impl skill (A4, A6, A7, …) pulls its required `gr/*.md` files explicitly at entry — mirrors W6/A4 TDD pattern.
- Exists: guardrail Op14b (push for review, pull for impl); B2 (push to reviewer); routing index `guardrails.md` §5.
- Missing: audit of `gr/` description quality for retrievability; explicit pull steps wired into impl skills as they are built.
- Next: audit `gr/` descriptions; add pull steps to A4, A6, A7 as each skill is authored. No new phase. No new guardrail. Skill optional (rcmd).

### W12c. Coding Standards – B1 Hook Enforcement

- Status: todo (deferred until skill substrate D1 settled).
- Category: **Rule / Convention** (cross-cutting).
- Approach: (B) pre-task hook (B1) fires before any edit, emits routing block, forces agent to state relevant categories + reasons before touching code. Enforces pull even in ad-hoc sessions outside a named skill — the only option that does.
- Depends on: D1 (skill substrate); W12b (descriptions must be good enough for B1 routing to be meaningful).
- Next: resolve D1, then build B1. No new skill.

### New skill needed

### W1. Grilled Design Concept

- Status: **contracts settled (2026-05-21)** — implementation pending.
- Category: **Phase**.
- Pocock reference skills: **`grill-me`** (`skills/productivity/grill-me/SKILL.md`) — generic Socratic stress-test; **`grill-with-docs`** (`skills/engineering/grill-with-docs/SKILL.md`) — same but reads `CONTEXT.md` / `docs/adr/` and updates them inline. A1 needs **both bodies**: `grill-me` for the questioning loop, `grill-with-docs` for the doc-anchored module-map update (Aln12).
- Walkthrough excerpt: §0:13:45–0:21:43 (gamification brief demo) — historical only.
- Exists: phase `aln` (`phases.md`); guardrail set `gr/gr_algn.md` (incl. **Aln17 — `/grill-with-docs` pattern**: stream-write `context.md` + B11 sub-agent ADR drafting; **Aln18** — alignment transcript artifact `<artifacts>/<WI>/algn_transcript.md`); skill A1 `align-concept` listed; doc-layer contracts `gr/gr_adr.md` and `gr_domain_language.md` L8+L9 (W16 + W17); core rule 3.36 (retire alignment transcripts).
- Contracts settled (this round, /grill-with-docs session 2026-05-21):
  - **idea.md consumption (Aln8 extended):** verbatim anchor + per-branch goal-tag + close-time coverage report; uncovered goals block close.
  - **Aln6 / B5 hidden-constraint sweep:** always fires at close; three outcomes (covered / not-applicable / missing); `missing` blocks close.
  - **Aln7 / B10 dispatch:** hybrid — minimal proactive narrow brief at start (modules / tests / context-term occurrences), reactive on demand; skip proactive if `idea.md` already names modules.
  - **Aln17 #4 near-match challenge:** always challenge on lexical *and* semantic neighbors before any `context.md` add.
  - **Aln17 #5 context.md write:** stream-write, one diff per change, HITL accept per change; no batching.
  - **Aln17 #6 ADR gate:** ask first ("ADR-worthy?") on plausible Adr1 hit; draft on yes.
  - **Aln17 #7 ADR drafting:** dispatch B11 sub-agent with verbatim-rationale brief; synchronous wait; grilling pauses until draft returns.
  - **C4 transcript artifact (Aln18):** `<artifacts>/<WI>/algn_transcript.md` + `<artifacts>/<WI>/status_algn_transcript.md`; retire with WI per 3.36.
  - **AFK domain-transcript path (Aln11):** dropped — `aln` is HITL-only per 3.20; Aln11 transcripts are HITL inputs only, not an AFK execution path.
- Missing: skill implementation (A1) wiring the settled contracts above; B5, B10, B11 sub-skills/hooks; C4 artifact lint. Note: existing `skills/input/align-concept-in.noPocockRef.md` and `skills/output/*.md` deliberately not touched (user constraint) — future `align-concept-in.md` will fold the settled contracts in.
- Pocock skill as additional input: load **both** SKILL.md bodies (`grill-me` + `grill-with-docs`) and the walkthrough excerpt when authoring A1 via `draft-skill-input` → `compile-skill`.
- Next: build A1 skill against the settled contracts; wire B5/B10/B11.

### W2. PRD

- Status: todo.
- Category: **Phase**.
- Pocock reference skill: **`to-prd`** (`skills/engineering/to-prd/SKILL.md`) — renamed from "write a PRD"; turns conversation context into a PRD and publishes to issue tracker.
- Walkthrough excerpt: §0:28:38–0:36:00 — historical only.
- Exists: phase `prd` (`phases.md`); skill A2 `compose-prd` listed; PRD template C1 listed.
- Missing: A2 implementation, C1 canonical template content, decision D3 (PRD retention vs. archive).
- Pocock skill as additional input: load `to-prd` SKILL.md body **and** the walkthrough excerpt when authoring A2. Note: `to-prd` already publishes to the issue tracker (matches D3 resolution: PRDs stored externally).
- Next: resolve D3, then build C1 + A2. No new phase or guardrail.

### W3. Issue DAG

- Status: todo.
- Category: **Phase**.
- Pocock reference skills: **`to-issues`** (`skills/engineering/to-issues/SKILL.md`) — renamed from "PRD to issues"; tracer-bullet vertical slices, publishes to issue tracker. Also relevant: **`triage`** (`skills/engineering/triage/SKILL.md`) — issue state-machine + AFK-prep that downstream consumes; load its body to understand the issue shape `to-issues` emits and that A4 picks up.
- Walkthrough excerpt: §0:38:49–0:51:38 — historical only.
- Exists: phase `iss`; skill A3 `prd-to-dag` listed; issue template C2 listed; HITL/AFK gate B4 listed.
- Missing: A3 implementation, C2 template content, vertical-vs-horizontal slicing rule (currently implicit only).
- Pocock skill as additional input: load `to-issues` + `triage` SKILL.md bodies and the walkthrough excerpt when authoring A3.
- Next: write C2, build A3. Consider explicit guardrail "vertical-slice preference" or keep inside skill prompt.

### W4. Ralph Once Loop

- Status: todo.
- Category: **Execution mode** (variant of `ral`).
- Reference skill: **`/ralph`** at `~/.claude/skills/ralph/SKILL.md` — global skill that implements once-by-default ("Do exactly ONE change and stop"), with many-mode delegated via `/loop 5m /ralph`. The once/many split is two composed tools, not a mode flag.
- Exists: phase `ral` covers Ralph Loop generally; `/ralph` global skill provides the reference implementation.
- Missing: A4 (`afk-loop` skill) for this project's `ral` phase — should inherit `/ralph`'s once-by-default + `/loop` composition pattern rather than invent a `--once` flag. AFK preconditions (Gov5a) and push/pull (Op14b) wiring still needed.
- Pocock skill as additional input: load `~/.claude/skills/ralph/SKILL.md` as source when authoring A4 (canonical reference impl of the once/many split).
- Next: build A4 mirroring `/ralph` semantics, wired to project guardrails. No new phase. No new guardrail.

### W5. AFK Implementation Loop

- Status: blocked (D4 — sandbox approach).
- Category: **Phase** (the autonomous variant of `ral`).
- Pocock reference skill: **none** — Pocock uses an `afk.sh` Bash loop / Docker-sandbox script, not a named skill (walkthrough §0:51:44–0:58:14).
- Exists: phase `ral`; skill A4 listed; HITL/AFK gate B4; sandbox decision D4 open.
- Missing: A4 implementation; sandbox decision D4 unresolved.
- Next: resolve D4, then build A4. No new phase.

### W7. Fresh-Context Review

- Status: todo.
- Category: **Phase**.
- Pocock reference skill: **`review`** (`skills/in-progress/review/SKILL.md`) — now shipped (status: in-progress in Pocock's repo). Reviews changes since a fixed point on two axes (Standards + Spec) via parallel sub-agents. Supersedes the walkthrough's "fresh-context automated review" (§1:05:24–1:06:27).
- Exists: phase `rev`; `gr/gr_rev.md`; skill A6 `review`; cross-cutting B2 (push standards), B3 (fresh context), B6 (module-depth), B7 (fabrication check).
- Missing: A6 implementation; reviewer-as-separate-process decision (D2) — currently same-process fresh context. Pocock's parallel-sub-agents shape may resolve D2.
- Pocock skill as additional input: load `review` SKILL.md body when authoring A6; compare its parallel-sub-agents split to our B2/B3/B6/B7 wiring.
- Next: build A6 with B2/B3/B6/B7 wired. No new phase or guardrail.

### W8. Manual QA

- Status: wip (phase + skeleton guardrail done; skill, template, registration pending).
- Category: **NEW Phase** — code `qa`. **Sequential**, mandatory after `ral` / `par`. Verify bucket. Human triages each finding into fix-now (loop back to `iss`) or backlog (does not block).
- Pocock reference skill: **none** — Pocock treats manual QA as a deliberately human-driven phase ("taste preservation"), not an agent skill.
- Exists: phase `qa` added to `phases.md` (sequential §1, Verify bucket §3, sequence diagram §4); skeleton `gr/gr_qa.md` drafted.
- Missing: `gr_qa.md` rules fleshed out; registration in `guardrails.md` §4 (next free 4.x slot); QA notes template (new entry under §C); skill `qa` (new A8?); decision on whether QA gating applies to AFK loops differently than HITL loops.
- Next: flesh out `gr_qa.md` rules; register in `guardrails.md` §4; add A8 skill placeholder; add C5 QA notes template placeholder.

### W9. Deep-Module Architecture

- Status: todo (D7 open — proactive vs. reactive).
- Category: **Phase / Initiative** (cross-phase).
- Pocock reference skill: **`improve-codebase-architecture`** (`skills/engineering/improve-codebase-architecture/SKILL.md`) — informed by CONTEXT.md + docs/adr/, finds deepening opportunities. (Walkthrough §1:21:08–1:23:04.)
- Exists: phase `ica`; `gr/gr_mod.md`; skill A7 `arch-review`; B6 module-depth check; D7 (proactive `ica` before feature work) open.
- Missing: A7 implementation; D7 decision (guardrail mandate vs. workflow tip).
- Pocock skill as additional input: load `improve-codebase-architecture` SKILL.md body **and** the walkthrough excerpt when authoring A7.
- Next: resolve D7, then build A7. No new phase.

### W10. Parallel Agents

- Status: blocked (substrate decision — Sand Castle vs. own driver; also D4).
- Category: **Execution mode** (variant of impl).
- Pocock reference skill: **none** — Pocock uses **Sand Castle**, a TypeScript orchestration tool (worktrees + Docker sandboxes + planner/reviewer/merger agents), not a named skill (walkthrough §1:29:47–1:32:39).
- Exists: phase `par`; skill A5 `parallel-loop` listed (status: blocked).
- Missing: orchestration substrate decision (Sand Castle vs. own driver), sandbox decision D4, planner+merger sub-skills.
- Next: unblock A5 by picking substrate. No new phase or guardrail.

---

## A. Phase Skills (one per phase in `phases.md`)

### A1. `align-concept` skill (phase: `aln`)

- Status: todo.
- Behavior: one question at a time, walks decision branches, recommends an answer per question, raises hidden-constraint checklist before closing (Aln6), supports domain-transcript input (Aln11), uses a subagent for codebase exploration (Aln7).
- Output: alignment transcript + agreed module map (Aln12).
- Source: `gr/gr_algn.md`. Pocock skill as additional input: load **both** `grill-me` (`skills/productivity/grill-me/SKILL.md`) and `grill-with-docs` (`skills/engineering/grill-with-docs/SKILL.md`) SKILL.md bodies, plus walkthrough §0:13:45–0:21:43 — feed into `draft-skill-input` when authoring.

### A2. `compose-prd` skill (phase: `prd`)

- Status: todo.
- Behavior: summarizes alignment transcript into a destination PRD using a fixed template (problem, user problem, solution, user stories, implementation decisions, testing decisions, out-of-scope, module map).
- Constraint: PRD summarizes alignment; does not replace it (Aln13).
- Source: `gr/gr_algn.md`, workflow doc §0:28:38–0:36:00. Pocock skill as additional input: load `to-prd` SKILL.md body (`skills/engineering/to-prd/SKILL.md`) + the walkthrough excerpt — feed into `draft-skill-input` when authoring.

### A3. `prd-to-dag` skill (phase: `iss`)

- Status: todo.
- Behavior: turns PRD into independently grabbable issues with explicit blocking edges, HITL/AFK tags (Gov5a), and vertical-slice preference over horizontal-layer slicing.
- Output: a DAG, not a sequential list.
- TDD sizing constraint: each issue must be sized so it maps to a small set of distinct Reds (one testable behavior per Red). Vague issues that resist single-Red framing fail the sizing check — split or re-grill. Source: `gr_tdd.md` TDD7.
- Source: workflow doc §0:38:49–0:51:38. Pocock skill as additional input: load `to-issues` (`skills/engineering/to-issues/SKILL.md`) + `triage` (`skills/engineering/triage/SKILL.md`) SKILL.md bodies + walkthrough excerpt — feed into `draft-skill-input` when authoring.

### A4. `afk-loop` skill (phase: `ral`)

- Status: todo.
- Behavior: picks the next available AFK issue, implements via TDD, runs feedback loops, commits, repeats until a sentinel.
- Preconditions enforced: AFK eligibility per Gov5a, push/pull respected (Op14b). On `ral` entry, pull `gr/gr_tdd.md` before first test or src edit (see `gr_tdd.md` "Pulling This Document" #2).
- Source: workflow doc §0:51:44–0:58:14. Pocock skill as additional input: `~/.claude/skills/ralph/SKILL.md` (once-by-default reference impl, separate plugin) + `tdd` SKILL.md body (`skills/engineering/tdd/SKILL.md`) — feed into `draft-skill-input` when authoring.

### A5. `parallel-loop` skill (phase: `par`)

- Status: blocked.
- Blocker: pick orchestration substrate (Sand Castle vs. own worktree+sandbox driver).
- Behavior: planner selects N parallel issues, each in a sandboxed worktree, with reviewer-and-merger agents downstream.
- Source: workflow doc §1:29:47–1:32:39.

### A6. `review` skill (phase: `rev`)

- Status: todo.
- Behavior: clears context (Rev1), pushes routed standards (Rev2, Op14b), reads tests first (Rev4), explicit module-depth assessment (Rev6, gr_mod.md M7), hidden-constraint coverage statement (Rev7), structured output (Rev11).
- Constraint: same-process fresh context (current setup); reviewer-agent split is a later option.
- Source: `gr/gr_rev.md`. Pocock skill as additional input: load `review` SKILL.md body (`skills/in-progress/review/SKILL.md`) — its parallel-sub-agents (Standards / Spec) shape is directly relevant to A6 design and D2.

### A7. `arch-review` skill (phase: `ica`)

- Status: todo.
- Behavior: scans codebase for shallow-module opportunities, proposes consolidations behind deeper interfaces, prioritizes by testability gap.
- Source: `gr/gr_mod.md`, workflow doc §1:21:08–1:23:04. Pocock skill as additional input: load `improve-codebase-architecture` SKILL.md body (`skills/engineering/improve-codebase-architecture/SKILL.md`) + walkthrough excerpt — feed into `draft-skill-input` when authoring.

### A12. `phase` skill (cross-phase infrastructure)

- Status: todo.
- Behavior: subcommands `enter` / `exit` / `status`. Sole writer of `phase_status.md` + `<artifacts>/ACTIVE`. Checks on enter: mode legal for phase? Previous phase exited cleanly? Tripwire-halt clear? Checks on exit: phase-required artifacts present? HITL ack recorded? `status` is read-only, computes `next_phase` from inputs against `phases.md` §4 chains.
- Source: coding_plan.md §"Phase Transition Mechanism"; `phases.md` §4; `guardrails.md` §3.37.
- Workflow ref: W15a.
- Template: C9 (`tpl/tpl_phase_status.md`).

### A13. `triage-idea` skill (phase: `ide`)

- Status: todo.
- Behavior: Idea8 entry triage (4-axis scoring: design ambiguity, blast radius, reversibility, existing test coverage; tripwire surfaces force `full`; HITL approves mode) + Idea11 mid-WI re-triage. `--remode` flag for standalone use (e.g., after 3.37 tripwire halt — no re-distillation needed). Outputs mode selection (`direct-edit` / `mini` / `full`) with audit trail.
- Source: `gr/gr_idea.md` Idea8–Idea11; `guardrails.md` §3.29, §3.37.
- Workflow ref: W15, W15a.
- Depends on: A12 (`/phase` must exist for `enter`/`exit` calls).

---

## B. Cross-Cutting Skills / Hooks

### B1. Routing-step enforcer

- Status: todo.
- Behavior: **narrowed** — belt-and-suspenders hook: warn if a phase skill (A-row) ran without a `/phase` call in the same turn. Primary enforcement now lives in A12 (`/phase`); B1 is the safety net, not the primary gate.
- Form: pre-task hook.
- Source: coding_plan.md §"Phase Transition Mechanism".

### B2. Push-standards-to-reviewer

- Status: todo.
- Behavior: on entering `rev`, load the routed `gr/gr_*.md` documents into context up front (push). Inverse of implementer default.
- Source: Op14b, Rev2.

### B3. Fresh-context-for-review

- Status: todo.
- Behavior: enforce a context clear (or session boundary) before review. Block review-in-same-context.
- Source: Rev1, 3.18.

### B4. HITL/AFK label gate

- Status: todo.
- Behavior: a task without an HITL/AFK label fails the precondition. AFK label requires the eligibility checklist (resolved decisions, no high-risk surface, sandbox present, automatable verification).
- Source: Gov5a, 3.20.

### B5. Hidden-constraint checklist (alignment + review)

- Status: todo.
- Behavior: reusable checklist applied in `aln` close-out (Aln6) and `rev` (Rev7). For each class — security, perms, retention, migrations, observability, API compat, concurrency — produces an explicit covered / not-applicable / missing statement.

### B6. Module-depth check

- Status: todo.
- Behavior: applied in `rev` (Rev6) and `ica` (A7). Heuristics: file-count delta, cross-module import delta, public-interface size, test-boundary placement.
- Source: `gr/gr_mod.md`.

### B7. Fabrication check (Op13) as positive review step

- Status: todo.
- Behavior: in review, every imported symbol, config key, error code, CLI flag, and library API in the diff is verified against the actual source.
- Source: Op13, Rev8.

### B8. Generated-code volume gate

- Status: todo.
- Behavior: Op11 thresholds enforced as a pre-edit gate. Crossing the threshold stops and asks.
- Source: Op11.

### B9. Persistent-context minimizer

- Status: todo.
- Behavior: audit and shrink the always-on context (system prompt, project AI rules) to only universal items. Detail docs are pulled.
- Source: Op14a, 3.17.

### B10. Subagent-for-exploration

- Status: todo.
- Behavior: when grilling or planning needs codebase facts, dispatch a subagent with isolated context that returns a summary. Caller's context stays clean.
- Source: Aln7, workflow doc §0:13:45–0:21:43.

### B11. Subagent-for-artifact-drafting

- Status: todo.
- Behavior: when the caller needs to produce a bounded long-form artifact (ADR draft in Adr5 format, PRD section, review summary), dispatch a subagent with a self-contained brief and await its returned draft. Caller's context stays lean; rationale-as-spoken is preserved by passing verbatim human rationale in the brief.
- Brief contract (for ADR drafting from `aln`): decision statement; the three Adr1 facts (why hard-to-reverse, why surprising, what tradeoff); human's verbatim rationale (paraphrase forbidden); relevant `context.md` neighborhood (only terms involved); any Aln15 rejected options already captured for this decision.
- Synchronous wait: caller pauses until the draft returns. Async drafting forbidden (reintroduces batching failure mode — a draft hanging over later grilling questions).
- Distinct from B10: B10 fetches facts (read-only exploration); B11 produces artifacts (write-side drafting).
- Source: Aln17 (ADR drafting in-session); 3.17 push/pull; Op14a; 3.25 clear-context-over-compaction.
- Applies to: `aln` (ADR drafts during grilling), `prd` (PRD-section drafting from alignment transcript), `rev` (review-summary drafting).
- Used by: A1 (ADR drafts mid-grilling), A2 (PRD section expansion), A6 (review output composition).

---

## C. Templates and Conventions

### C1. PRD template

- Status: todo.
- Behavior: canonical template referenced by `compose-prd` — includes module map, out-of-scope, testing decisions.

### C2. Issue template with HITL/AFK tag and blocking edges

- Status: todo.

### C3. Review output template

- Status: todo.
- Source: Rev11.

### C4. Alignment-transcript artifact format

- Status: **contract settled (2026-05-21)**; lint hook pending.
- Decision: **repo, WI-scoped, retire-with-WI** — parallel to C8 (idea file). Paired files under `<artifacts>/<WI>/`: `algn_transcript.md` (body) + `status_algn_transcript.md` (frontmatter: `status: wip|done`, `updated`, `owner-issue`). Retired with `<artifacts>/<WI>/` at WI close per Core rule 3.36 (added 2026-05-21), verified by Q11 lint.
- Rationale: transcript is the *source* artifact (A2 / A6 / A8 consume it); PRD composed by A2 is its *destination summary* per Aln13. Agent consumption is cheaper against a local repo file than via issue-tracker API. Pattern parallels C8 (idea.md) exactly — paired body + status frontmatter, `owner-issue` provenance, WI-lifetime retirement.
- Source: `gr/gr_algn.md` Aln18; `guardrails.md` §3.36 + §9 parallel row.
- Used by: A1 (emits), A2 / A6 / A8 (consume); Q11 lint (`status_algn_transcript.md` frontmatter + `<artifacts>/<WI>/` deletion check).
- Next: A1 emit-path during build; Q11 lint extension to cover `algn_transcript.md` shape (mechanical, after skill substrate D1 settled).

### C6. Prototype variant presentation template

- Status: **done** (2026-05-18, see W14b).
- Artifact: [`tpl/tpl_var_pres.md`](tpl/tpl_var_pres.md).
- Purpose: machine-parseable shape for prototype variant output (Pro2/Pro4/Pro7/Pro8). Skill (W14e/A9) emits; human picker consumes.
- Slot: C5 reserved for W8 QA notes template; C6 is the next free slot.

### C8. Idea file template

- Status: **done** (2026-05-20).
- Artifact: [`tpl/tpl_idea.md`](tpl/tpl_idea.md).
- Purpose: single parse target for downstream consumers (A1 align-concept reads goals to anchor grilling; A2 compose-prd folds into PRD Goals section; A6 review verifies coverage; A8 qa runs Q11 retirement lint).
- Shape: pair of files under `<artifacts>/<WI>/` — `idea.md` (markdown body, no frontmatter, `# Goals` heading, numbered 3–6 entries with `Non-goal:` prefix for negatives, optional `Stripped detail:` lines) + `status_idea.md` (frontmatter only: `status`, `updated`, `owner-issue`).
- Source: [gr_idea.md](gr/gr_idea.md) Idea7; retirement [guardrails.md](guardrails.md) §3.33; Q11 lint [gr_qa.md](gr/gr_qa.md).
- Used by: A11 (emits), A1, A2, A6, A8 (consume); Q11 lint (status_idea.md frontmatter).
- Workflow ref: W15.
- Pattern parallel: mirrors C6 (variant template) — paired machine-shape + human-body, `owner-issue` provenance, owner-close retirement.
- Next: A11 skill rewrite (`distill-idea-in.md` → recompile `distill-idea.md`) references this template instead of inlining the shape.

---

## D. Open Questions / Decisions Before Building

- D1. Skill substrate — Claude Code skills only, or also `AGENTS.md`-style instructions, or both? Affects how push/pull is implemented.
- D2. Reviewer process — confirmed: same process, fresh context (current). Reassess once Sand-Castle-style orchestration is in scope.
- D3. **Resolved** (2026-05-17, enforcement closed 2026-05-18) — answered by guardrail 3.24: PRDs are stored externally (e.g. GitHub Issues) and closed when done; not retained in working tree. Same shape extended to research files by 3.27 (deleted at sprint/feature close). Enforcement: pre-commit lint (PRD paths forbidden in-tree; research files require `owner-issue` field) + `qa` Q11 merge-gate check verifies owner-issue close triggers research deletion. See `consider_7_phases_todo.md` Item 8.
- D4. AFK sandbox — pick a sandboxing approach (Docker, Windows job objects, worktree-only). Affects Gov11 and `afk-loop` precondition.
- D5. Model selection per role — confirm pattern (stronger model for review, faster for implementation) and how it is enforced.
- D6. Token-status visibility — adopt a status-line / token-meter so context proximity to dumb zone is visible (Pocock Experiment 1).
- D7. Proactive `ica` before feature work — Pocock's #1 recommendation: run `improve-codebase-architecture` *before* starting new feature work, not only reactively. Currently tracked as a skill (A7) and phase (`ica` in `phases.md`), but no guardrail mandates or suggests running it proactively. Decision: guardrail-level rule, workflow guidance, or leave as skill-level suggestion?
- D8. **Resolved** (2026-05-15) — added as Aln17 in `gr/gr_algn.md`. Throwaway 2–3 FE prototypes when visual/UX ambiguity blocks alignment; decision made in `aln`. Skill form rejected (over-prescription risk).
- D9. QA loop convergence — currently human-verdict (3.30 / Q9). Decide later whether to add a mechanized option: typed acceptance-criteria checklist tied to PRD template C1, hard-gated. Postponed until C1 lands and a few QA sessions are observed. Trigger to revisit: repeated drift in pass verdicts or AFK-mode runs needing gate-able criteria.
- D10. **Idea7 `status_idea.md` migration** — fold into `phase_status.md` (tentative) vs. coexist with pointer. Tentative decision: fold, with Idea7 rewritten to point at `phase_status.md`'s `Current` block. Blocks A12 schema lock-in. Source: coding_plan.md §"Phase Transition Mechanism".

---

## F. Unmapped Pocock skills (consider for future rows)

Pocock skills not currently referenced by any W/A/B/C row. Each is a candidate for adoption, partial-borrow, or explicit reject. Decide per-skill; add a row when adopting.

| Pocock skill                 | Path                                              | Possible mapping / use                                                                                                                   |
| ---------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `diagnose`                   | `skills/engineering/diagnose/SKILL.md`            | New cross-cutting skill for bug/perf loops — currently no phase or skill covers this. Candidate B-series row or new phase `dia`.         |
| `triage`                     | `skills/engineering/triage/SKILL.md`              | Feeds W3 (`to-issues`) and B4 (HITL/AFK gate). Already cited from W3; consider a standalone wrapper if our issue tracker shape diverges. |
| `zoom-out`                   | `skills/engineering/zoom-out/SKILL.md`            | Cross-cutting B-series candidate — broaden context before any major decision. Maps loosely to B9 (persistent-context minimizer) inverse. |
| `handoff`                    | `skills/productivity/handoff/SKILL.md`            | Cross-cutting — session compaction for long-running `ral`/`par` flows. Candidate B-series row.                                           |
| `write-a-skill`              | `skills/productivity/write-a-skill/SKILL.md`      | Meta — compare to our `draft-skill-input` + `compile-skill` + `test-skill` chain. Audit for missed authoring patterns.                   |
| `caveman`                    | `skills/productivity/caveman/SKILL.md`            | Already adopted (see project CLAUDE.md). No row needed.                                                                                  |
| `git-guardrails-claude-code` | `skills/misc/git-guardrails-claude-code/SKILL.md` | Candidate for B-series (commit hygiene) — relates to Op11/B8.                                                                            |
| `setup-pre-commit`           | `skills/misc/setup-pre-commit/SKILL.md`           | Relevant for W12c (B1 hook enforcement substrate) and the pre-commit lint mentioned in W13/D3.                                           |
| `migrate-to-shoehorn`        | `skills/misc/migrate-to-shoehorn/SKILL.md`        | Project-specific (TS); not applicable.                                                                                                   |
| `scaffold-exercises`         | `skills/misc/scaffold-exercises/SKILL.md`         | Education-domain; not applicable.                                                                                                        |
| `edit-article`               | `skills/personal/edit-article/SKILL.md`           | Not applicable to coding workflow.                                                                                                       |
| `obsidian-vault`             | `skills/personal/obsidian-vault/SKILL.md`         | Related to the `capture` skill already loaded; revisit if knowledge-base flow is added.                                                  |

Deprecated (do NOT reference, kept in `skills/deprecated/`): `design-an-interface`, `qa` (Pocock's old), `request-refactor-plan`, `ubiquitous-language`, `triage-issue`. Note that **our** `qa` phase (W8) is unrelated to Pocock's deprecated `qa` skill.

## E. Validation / Experiments (from Pocock doc)

- E1. Grill-me on a real ambiguous ticket. Measure: assumptions surfaced, post-implementation scope changes.
- E2. PRD summarization fidelity check — second agent or human compares PRD to grilling transcript.
- E3. Vertical vs horizontal slicing — implement one feature both ways, compare rework.
- E4. Push vs pull standards — measure standards violations per PR before/after.
- E5. Module-depth refactor — run `arch-review` on the repo, measure test-boundary count and cross-module import count before/after.
- E6. **Deferred decision — `draft-skill-input` Step 6 strip default.** Today Step 6 defaults to strip phase-management rules from the source `gr/*.md`. This serves most skills but silently loses rules a phase-owning entry skill legitimately owns (Idea8 triage, Idea9 issue invariant, Idea10 budget, Idea11 transitions). Current workaround: for `distill-idea` only, the input is hand-tuned against a `_ref` baseline (`skills/input/distill-idea-in_ref.md`). Upgrade trigger: as soon as a second phase skill is identified as phase-owning-orchestration, switch `draft-skill-input` to the **hybrid** design — add `ownership: phase-only | phase-owns-orchestration` flag to each `coding_plan.md` skill row; flagged skills get default-include + per-rule HITL classify in Step 6; unflagged skills keep today's default-strip. Measure (when triggered): per-skill rule-coverage delta between fresh draft and `_ref` baseline, by `IdeaN`/`AlnN`/etc. anchor.
