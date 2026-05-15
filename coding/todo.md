# TODO: Operationalize Guardrails as Skills

Purpose: convert the guardrails and workflow documents from prose-on-paper into enforceable behavior in the agent runtime. Each item below is a candidate **skill** (Claude Code `/skill` or equivalent), **hook**, **subagent**, or **prompt template**. The aim is to minimize always-on context cost (Op14a) by pulling detail only when triggered.

Source documents:

- `guardrails.md` — core rules + routing index.
- `gr/gr_*.md` — detail per category.
- `AI_Coding_Workflow.md` — phase flow and roles.
- `phases.md` — phase definitions.
- `videos/matt_pocock_full_walkthrough_workflow_gpt55pro.md` — workflow source.

---

## Table of Contents

- [Status legend](#status-legend)
- [Workflows](#workflows)
  - No new skill needed:
    - [W6. Agentic TDD](#w6-agentic-tdd)
    - [W11. Front-End Prototype](#w11-front-end-prototype)
    - [W12. Coding Standards Push/Pull](#w12-coding-standards-pushpull)
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
  - [A1. `grill-me` skill (phase: `aln`)](#a1-grill-me-skill-phase-aln)
  - [A2. `write-prd` skill (phase: `prd`)](#a2-write-prd-skill-phase-prd)
  - [A3. `decompose-issues` skill (phase: `iss`)](#a3-decompose-issues-skill-phase-iss)
  - [A4. `ralph-loop` skill (phase: `ral`)](#a4-ralph-loop-skill-phase-ral)
  - [A5. `parallel-loop` skill (phase: `par`)](#a5-parallel-loop-skill-phase-par)
  - [A6. `review` skill (phase: `rev`)](#a6-review-skill-phase-rev)
  - [A7. `improve-architecture` skill (phase: `ica`)](#a7-improve-architecture-skill-phase-ica)
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
- [C. Templates and Conventions](#c-templates-and-conventions)
  - [C1. PRD template](#c1-prd-template)
  - [C2. Issue template with HITL/AFK tag and blocking edges](#c2-issue-template-with-hitlafk-tag-and-blocking-edges)
  - [C3. Review output template](#c3-review-output-template)
  - [C4. Alignment-transcript artifact format](#c4-alignment-transcript-artifact-format)
- [D. Open Questions / Decisions Before Building](#d-open-questions--decisions-before-building)
- [E. Validation / Experiments (from Pocock doc)](#e-validation--experiments-from-pocock-doc)

---

## Status legend

- `todo` — not started.
- `wip` — in progress.
- `done` — implemented and tested.
- `blocked` — needs a decision first.

---

## Workflows

Source: `videos/matt_pocock_full_walkthrough_workflow_gpt55pro.md` §"Workflows and Methods" (12 items, W1–W12).

Pocock's 12 items mix **phases** (sequential delivery steps), **techniques** (used inside a phase), **execution modes** (variants of an impl phase), and **rules/conventions** (cross-cutting). Categorization summary:

Order below: items with **no new skill required** first, then items that **need a new skill**.

| #           | Pocock title               | Category         | Status  | New skill?      | Pocock reference skill                              | Maps to                        |
| ----------- | -------------------------- | ---------------- | ------- | --------------- | --------------------------------------------------- | ------------------------------ |
| W6          | Agentic TDD                | Technique        | done    | no (guardrail)  | —                                                   | `gr/gr_tdd.md` + §4.16 routing |
| W11         | Front-End Prototype        | Technique        | done    | no (rule Aln17) | —                                                   | inside `aln` — Aln17           |
| PreW12, W12 | Coding Standards push/pull | Rule/Convention  | todo    | no              | —                                                   | guardrail Op14b (exists)       |
| W1          | Grilled Design Concept     | Phase            | todo    | yes (A1)        | "grill me" skill                                    | `aln` (exists)                 |
| W2          | PRD                        | Phase            | todo    | yes (A2)        | "write a PRD" skill                                 | `prd` (exists)                 |
| W3          | Issue DAG                  | Phase            | todo    | yes (A3)        | "PRD to issues" skill                               | `iss` (exists)                 |
| W4          | Ralph Once Loop            | Execution mode   | todo    | yes (A4)        | `/ralph` skill (`~/.claude/skills/ralph/`)          | variant of `ral`               |
| W5          | AFK Implementation Loop    | Phase            | blocked | yes (A4)        | none — `afk.sh` loop script (not a skill)           | `ral` (exists), D4 open        |
| W7          | Fresh-Context Review       | Phase            | todo    | yes (A6)        | none named — "fresh-context automated review"       | `rev` (exists)                 |
| W8          | Manual QA                  | **NEW Phase**    | wip     | yes (A8)        | none — human-driven phase in Pocock's walkthrough   | `qa` added, `gr_qa.md` drafted |
| W9          | Deep-Module Architecture   | Phase/Initiative | todo    | yes (A7)        | "improve codebase architecture" skill               | `ica` (exists), D7 open        |
| W10         | Parallel Agents            | Execution mode   | blocked | yes (A5)        | none — Sand Castle orchestration tool (not a skill) | `par` (exists), substrate TBD  |

Each item below: **what exists**, **what's missing**, **next step**. Detail per item handled in a fresh chat context.

Beyond the 12 items, the orchestration that chains them (e.g., `grill-me` → `write-prd` → `decompose-issues`) remains a separate concern — a future `workflow.md` + `wf/` folder is a candidate, mirroring the `guardrails.md` + `gr/` split. Not started.

---

### No new skill needed

### W6. Agentic TDD

- Status: **done** (guardrail authored; skill-precondition wiring follows when A4 is built).
- Category: **Technique** (used inside `ral`/`par`).
- Artifact: [`gr/gr_tdd.md`](gr/gr_tdd.md) — Red-Green-Refactor loop, false-green verification (TDD2), fail-for-right-reason (TDD3), minimum-code Green (TDD4), mandatory Refactor (TDD5), mock discipline (TDD6), one-Red-at-a-time (TDD7), FE/visual applicability (TDD8), no retroactive tests (TDD9), refactor must not change behavior (TDD10).
- Pull-enforcement: §4.16 routing index entry in `guardrails.md` (Opt A) + A4 `ralph-loop` skill precondition (Opt B, pending A4 build). Hook-based enforcement (Opt C) deferred.
- Side-edits: T12/T12a removed from `gr_testing_verification.md` (single source of truth); §3.22 link retargeted to `gr_tdd.md`; §9 parallel table row updated to `TDD1, TDD2`.
- Follow-up: when A4 (`ralph-loop`) skill is built, its prompt must load `gr_tdd.md` on `ral` entry before first edit (TDD section "Pulling This Document" #2).

### W11. Front-End Prototype

- Status: **done** (Aln17 added to `gr_alignment.md`).
- Category: **Technique** (used inside `aln`).
- Artifacts:
  - [`gr/gr_alignment.md`](gr/gr_alignment.md) Aln17 — short rule: prototype decision made in `aln`, scope-limited to genuinely visual ambiguity, output feeds Aln12/Aln15.
  - [`wf/wf_fe_prototype.md`](wf/wf_fe_prototype.md) — full workflow: when/inputs/steps/outputs/tradeoffs/failure modes. First entry in the new `wf/` folder (see todo.md preamble).
- Resolves: D8 (artifact form = rule + workflow doc, not skill).
- Side-effect: seeds the `workflow.md` + `wf/` split foreshadowed in the workflows section preamble. `workflow.md` index doc not yet written.
- Follow-up: when more workflow docs land (W6 TDD already detailed inline in `gr/gr_tdd.md` — different pattern), decide whether to retro-create `workflow.md` index.

### Pre-W12. Review standards guardrails sources

- Status: todo
- see standards_guardrails_sources.md

### W12. Coding Standards Push/Pull

- Status: todo (rule exists; discoverability audit + enforcement pending).
- Category: **Rule / Convention** (cross-cutting).
- Exists: guardrail Op14b (push for review, pull for impl); B2 (push to reviewer); B9 (persistent-context minimizer); routing index in `guardrails.md` §5.
- Missing: enforcement of skill discoverability (Op14b failure mode: implementer doesn't pull because skills are poorly described); audit of `gr/gr_*.md` description quality.
- Next: review `gr/` descriptions for retrievability; consider B1 (routing-step enforcer) as enforcement. No new phase. No new guardrail.

### New skill needed

### W1. Grilled Design Concept

- Status: todo.
- Category: **Phase**.
- Pocock reference skill: **"grill me"** skill (walkthrough §0:13:45–0:21:43, gamification brief demo).
- Exists: phase `aln` (`phases.md`); guardrail set `gr/gr_alignment.md`; skill A1 `grill-me` listed.
- Missing: skill implementation (A1), hidden-constraint checklist enforcement (B5), subagent dispatch (B10), AFK domain-transcript path (Aln11).
- Next: build A1 skill, wire B5/B10 hooks. No new phase or guardrail.

### W2. PRD

- Status: todo.
- Category: **Phase**.
- Pocock reference skill: **"write a PRD"** skill (walkthrough §0:28:38–0:36:00; fills a PRD template after interviewing).
- Exists: phase `prd` (`phases.md`); skill A2 `write-prd` listed; PRD template C1 listed.
- Missing: A2 implementation, C1 canonical template content, decision D3 (PRD retention vs. archive).
- Next: resolve D3, then build C1 + A2. No new phase or guardrail.

### W3. Issue DAG

- Status: todo.
- Category: **Phase**.
- Pocock reference skill: **"PRD to issues"** skill (walkthrough §0:38:49–0:51:38; emits vertical-slice issues with blockers).
- Exists: phase `iss`; skill A3 `decompose-issues` listed; issue template C2 listed; HITL/AFK gate B4 listed.
- Missing: A3 implementation, C2 template content, vertical-vs-horizontal slicing rule (currently implicit only).
- Next: write C2, build A3. Consider explicit guardrail "vertical-slice preference" or keep inside skill prompt.

### W4. Ralph Once Loop

- Status: todo.
- Category: **Execution mode** (variant of `ral`).
- Reference skill: **`/ralph`** at `~/.claude/skills/ralph/SKILL.md` — global skill that implements once-by-default ("Do exactly ONE change and stop"), with many-mode delegated via `/loop 5m /ralph`. The once/many split is two composed tools, not a mode flag.
- Exists: phase `ral` covers Ralph Loop generally; `/ralph` global skill provides the reference implementation.
- Missing: A4 (`ralph-loop` skill) for this project's `ral` phase — should inherit `/ralph`'s once-by-default + `/loop` composition pattern rather than invent a `--once` flag. AFK preconditions (Gov5a) and push/pull (Op14b) wiring still needed.
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
- Pocock reference skill: **none named** — described as the "fresh-context automated review" technique (walkthrough §1:05:24–1:06:27); no canonical Pocock skill shipped.
- Exists: phase `rev`; `gr/gr_review.md`; skill A6 `review`; cross-cutting B2 (push standards), B3 (fresh context), B6 (module-depth), B7 (fabrication check).
- Missing: A6 implementation; reviewer-as-separate-process decision (D2) — currently same-process fresh context.
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
- Pocock reference skill: **"improve codebase architecture"** skill (walkthrough §1:21:08–1:23:04; scans for shallow modules / consolidation opportunities).
- Exists: phase `ica`; `gr/gr_modules.md`; skill A7 `improve-architecture`; B6 module-depth check; D7 (proactive `ica` before feature work) open.
- Missing: A7 implementation; D7 decision (guardrail mandate vs. workflow tip).
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

### A1. `grill-me` skill (phase: `aln`)

- Status: todo.
- Behavior: one question at a time, walks decision branches, recommends an answer per question, raises hidden-constraint checklist before closing (Aln6), supports domain-transcript input (Aln11), uses a subagent for codebase exploration (Aln7).
- Output: alignment transcript + agreed module map (Aln12).
- Source: `gr/gr_alignment.md`. External reference: Pocock "grill me" skill.

### A2. `write-prd` skill (phase: `prd`)

- Status: todo.
- Behavior: summarizes alignment transcript into a destination PRD using a fixed template (problem, user problem, solution, user stories, implementation decisions, testing decisions, out-of-scope, module map).
- Constraint: PRD summarizes alignment; does not replace it (Aln13).
- Source: `gr/gr_alignment.md`, workflow doc §0:28:38–0:36:00.

### A3. `decompose-issues` skill (phase: `iss`)

- Status: todo.
- Behavior: turns PRD into independently grabbable issues with explicit blocking edges, HITL/AFK tags (Gov5a), and vertical-slice preference over horizontal-layer slicing.
- Output: a DAG, not a sequential list.
- TDD sizing constraint: each issue must be sized so it maps to a small set of distinct Reds (one testable behavior per Red). Vague issues that resist single-Red framing fail the sizing check — split or re-grill. Source: `gr_tdd.md` TDD7.
- Source: workflow doc §0:38:49–0:51:38.

### A4. `ralph-loop` skill (phase: `ral`)

- Status: todo.
- Behavior: picks the next available AFK issue, implements via TDD, runs feedback loops, commits, repeats until a sentinel.
- Preconditions enforced: AFK eligibility per Gov5a, push/pull respected (Op14b). On `ral` entry, pull `gr/gr_tdd.md` before first test or src edit (see `gr_tdd.md` "Pulling This Document" #2).
- Source: workflow doc §0:51:44–0:58:14.

### A5. `parallel-loop` skill (phase: `par`)

- Status: blocked.
- Blocker: pick orchestration substrate (Sand Castle vs. own worktree+sandbox driver).
- Behavior: planner selects N parallel issues, each in a sandboxed worktree, with reviewer-and-merger agents downstream.
- Source: workflow doc §1:29:47–1:32:39.

### A6. `review` skill (phase: `rev`)

- Status: todo.
- Behavior: clears context (Rev1), pushes routed standards (Rev2, Op14b), reads tests first (Rev4), explicit module-depth assessment (Rev6, gr_modules.md M7), hidden-constraint coverage statement (Rev7), structured output (Rev11).
- Constraint: same-process fresh context (current setup); reviewer-agent split is a later option.
- Source: `gr/gr_review.md`.

### A7. `improve-architecture` skill (phase: `ica`)

- Status: todo.
- Behavior: scans codebase for shallow-module opportunities, proposes consolidations behind deeper interfaces, prioritizes by testability gap.
- Source: `gr/gr_modules.md`, workflow doc §1:21:08–1:23:04.

---

## B. Cross-Cutting Skills / Hooks

### B1. Routing-step enforcer

- Status: todo.
- Behavior: before any planning or implementation, emit the required routing block (`guardrails.md` §5) — relevant categories with reasons, considered-but-excluded with reasons.
- Form: pre-task hook or prompt-prefix skill.

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
- Source: `gr/gr_modules.md`.

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

---

## C. Templates and Conventions

### C1. PRD template

- Status: todo.
- Behavior: canonical template referenced by `write-prd` — includes module map, out-of-scope, testing decisions.

### C2. Issue template with HITL/AFK tag and blocking edges

- Status: todo.

### C3. Review output template

- Status: todo.
- Source: Rev11.

### C4. Alignment-transcript artifact format

- Status: todo.
- Decision pending: retain in repo vs close-as-done in issue tracker (workflow doc §1:23:04–1:25:15 documentation rot concern).

---

## D. Open Questions / Decisions Before Building

- D1. Skill substrate — Claude Code skills only, or also `AGENTS.md`-style instructions, or both? Affects how push/pull is implemented.
- D2. Reviewer process — confirmed: same process, fresh context (current). Reassess once Sand-Castle-style orchestration is in scope.
- D3. PRD retention — keep in repo (risk: doc rot) vs. close in issue tracker. Default position: do not keep PRDs in working tree; archive via closed issues.
- D4. AFK sandbox — pick a sandboxing approach (Docker, Windows job objects, worktree-only). Affects Gov11 and `ralph-loop` precondition.
- D5. Model selection per role — confirm pattern (stronger model for review, faster for implementation) and how it is enforced.
- D6. Token-status visibility — adopt a status-line / token-meter so context proximity to dumb zone is visible (Pocock Experiment 1).
- D7. Proactive `ica` before feature work — Pocock's #1 recommendation: run `improve-codebase-architecture` *before* starting new feature work, not only reactively. Currently tracked as a skill (A7) and phase (`ica` in `phases.md`), but no guardrail mandates or suggests running it proactively. Decision: guardrail-level rule, workflow guidance, or leave as skill-level suggestion?
- D8. **Resolved** (2026-05-15) — added as Aln17 in `gr/gr_alignment.md`. Throwaway 2–3 FE prototypes when visual/UX ambiguity blocks alignment; decision made in `aln`. Skill form rejected (over-prescription risk).

---

## E. Validation / Experiments (from Pocock doc)

- E1. Grill-me on a real ambiguous ticket. Measure: assumptions surfaced, post-implementation scope changes.
- E2. PRD summarization fidelity check — second agent or human compares PRD to grilling transcript.
- E3. Vertical vs horizontal slicing — implement one feature both ways, compare rework.
- E4. Push vs pull standards — measure standards violations per PR before/after.
- E5. Module-depth refactor — run `improve-architecture` on the repo, measure test-boundary count and cross-module import count before/after.
