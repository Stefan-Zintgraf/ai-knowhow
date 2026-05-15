# TODO: Operationalize Guardrails as Skills

Purpose: convert the guardrails and workflow documents from prose-on-paper into enforceable behavior in the agent runtime. Each item below is a candidate **skill** (Claude Code `/skill` or equivalent), **hook**, **subagent**, or **prompt template**. The aim is to minimize always-on context cost (Op14a) by pulling detail only when triggered.

Source documents:

- `guardrails.md` — core rules + routing index.
- `gr/gr_*.md` — detail per category.
- `AI_Coding_Workflow.md` — phase flow and roles.
- `phases.md` — phase definitions.
- `videos/matt_pocock_full_walkthrough_workflow_gpt55pro.md` — workflow source.

---

## Status legend

- `todo` — not started.
- `wip` — in progress.
- `done` — implemented and tested.
- `blocked` — needs a decision first.

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
- Source: workflow doc §0:38:49–0:51:38.

### A4. `ralph-loop` skill (phase: `ral`)

- Status: todo.
- Behavior: picks the next available AFK issue, implements via TDD, runs feedback loops, commits, repeats until a sentinel.
- Preconditions enforced: AFK eligibility per Gov5a, push/pull respected (Op14b).
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

---

## E. Validation / Experiments (from Pocock doc)

- E1. Grill-me on a real ambiguous ticket. Measure: assumptions surfaced, post-implementation scope changes.
- E2. PRD summarization fidelity check — second agent or human compares PRD to grilling transcript.
- E3. Vertical vs horizontal slicing — implement one feature both ways, compare rework.
- E4. Push vs pull standards — measure standards violations per PR before/after.
- E5. Module-depth refactor — run `improve-architecture` on the repo, measure test-boundary count and cross-module import count before/after.
