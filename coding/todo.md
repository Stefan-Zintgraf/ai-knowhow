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
  Prompt: 
  Run the draft-skill-input skill to create a new skill input file distill-idea-in.md for the W15 row in todo.md.
  The skill input file then shall be compiled using the compile-skill skill which creates the distill-idea.md output file.
  Compare it with the reference distill-idea-ref.md file and adjust the draft-skill-input skill if possible to make the match perfect.
  Finally, the distill-idea.md skill shall be tested using the test-skill skill with the following input: 
  AI-driven mail handling. Goals: search mails by NL prompt, draft replies, use mail content as a knowledge base for Q&A.





 




### Workflows table

| #    | Pocock title               | Category                   | Status          | skill | hook   | Pocock reference skill                     | Maps to                               |
| ---- | -------------------------- | -------------------------- | --------------- | ----- | ------ | ------------------------------------------ | ------------------------------------- |
| W15  | Idea Phase                 | **NEW Phase**              | done            | A11   | —      | none — Pocock phase 1 (7-phases doc)       | `ide` added, `gr_idea.md` drafted,    |
|      |                            |                            |                 |       |        |                                            | §3.32 + §4.19 added                   |
| W1   | Grilled Design Concept     | Phase                      | todo            | A1    | —      | "grill me" skill                           | `aln` (exists)                        |
| W13  | Research Caching           | Phase (optional)           | wip             | A10   | TBD    | none named — Pocock phase 2                | `res` added, `gr_res.md` drafted,     |
|      |                            |                            |                 |       |        | + `research.md` cache                      | §3.27 + §4.17 added                   |
| W14a | Sandbox Retirement         | Enforcement (W14)          | todo            | —     | TBD    | none                                       | adapt W13's `owner-issue`+Q11 to dirs |
| W14b | Variant Template           | Template (C6, W14)         | done            | —     | —      | none                                       | see [C6](tpl/tpl_var_pres.md)         |
| W14c | Res→Pro Fact Persistence   | Decision (D-new, W14)      | done            | —     | —      | none                                       | `res`/`pro` boundary                  |
| W14d | Rejected-Variant→align-concept | Wiring (W14)           | done (contract) | —     | —      | none                                       | A1 (`align-concept`) integration      |
| W14e | Prototype Skill            | **NEW Phase** / Skill (A9) | wip             | A9    | —      | none (Pocock phase 3)                      | `pro` added, `gr_proto.md`            |
|      |                            |                            |                 |       |        |                                            | + `wf/wf_proto.md`                    |
| W2   | PRD                        | Phase                      | todo            | A2    | —      | "write a PRD" skill                        | `prd` (exists)                        |
| W3   | Issue DAG                  | Phase                      | todo            | A3    | —      | "PRD to issues" skill                      | `iss` (exists)                        |
| W4   | Ralph Once Loop            | Execution mode             | todo            | A4    | —      | `/ralph` skill (`~/.claude/skills/ralph/`) | variant of `ral`                      |
| W5   | AFK Implementation Loop    | Phase                      | blocked         | A4    | B4, B8 | none — `afk.sh` loop script (not a skill)  | `ral` (exists), D4 open               |
| W10  | Parallel Agents            | Execution mode             | blocked         | A5    | —      | none — Sand Castle orchestration tool      | `par` (exists), substrate TBD         |
|      |                            |                            |                 |       |        | (not a skill)                              |                                       |
| W6   | Agentic TDD                | Technique                  | done            | —     | B1     | —                                          | `gr/gr_tdd.md` + §4.16 routing        |
| W8   | Manual QA                  | **NEW Phase**              | wip             | A8    | —      | none — human-driven phase                  | `qa` added, `gr_qa.md` drafted        |
|      |                            |                            |                 |       |        | in Pocock's walkthrough                    |                                       |
| W7   | Fresh-Context Review       | Phase                      | todo            | A6    | B3     | none named —                               | `rev` (exists)                        |
|      |                            |                            |                 |       |        | "fresh-context automated review"           |                                       |
| W9   | Deep-Module Architecture   | Phase/Initiative           | todo            | A7    | —      | "improve codebase architecture" skill      | `ica` (exists), D7 open               |
| W12a | Review Standards Sources   | Manual / Audit             | todo            | —     | —      | —                                          | `standards_guardrails_sources.md`     |
| W12b | Standards Descriptions     | Rule/Convention            | todo            | TBD   | —      | —                                          | Op14b + `gr/` description quality     |
|      |                            |                            |                 |       |        |                                            | + skill preconditions                 |
| W12c | Standards Hook Enforcement | Rule/Convention            | todo            | —     | B1     | —                                          | B1 routing-step enforcer              |

### Phase Skills table

| #   | Skill name             | Phase | Status  | Source doc                                                   | Workflow ref | Depends on                    |
| --- | ---------------------- | ----- | ------- | ------------------------------------------------------------ | ------------ | ----------------------------- |
| A11 | `distill-idea`         | `ide` | todo    | [gr_idea.md](gr/gr_idea.md)                                  | W15          | —                             |
| A1  | `align-concept`        | `aln` | todo    | [gr_algn.md](gr/gr_algn.md)                                  | W1           | —                             |
| A10 | `do-research`          | `res` | todo    | [gr_res.md](gr/gr_res.md)                                    | W13          | B10, C7 (template)            |
| A9  | `prototype`            | `pro` | todo    | [gr_proto.md](gr/gr_proto.md), [wf_proto.md](wf/wf_proto.md) | W14e         | W14a (sandbox), W14b (C6 tpl) |
| A2  | `compose-prd`          | `prd` | todo    | [gr_algn.md](gr/gr_algn.md)                                  | W2           | A1, C1 (template), D3 ✓       |
| A3  | `prd-to-dag`           | `iss` | todo    | [gr_tdd.md](gr/gr_tdd.md)                                    | W3           | A2, C2 (template)             |
| A4  | `afk-loop`             | `ral` | todo    | [gr_tdd.md](gr/gr_tdd.md)                                    | W4, W5       | A3, D4 (sandbox)              |
| A5  | `parallel-loop`        | `par` | blocked | —                                                            | W10          | D4 (sandbox), substrate TBD   |
| A8  | `qa`                   | `qa`  | wip     | [gr_qa.md](gr/gr_qa.md)                                      | W8           | A4, C5 (template)             |
| A6  | `review`               | `rev` | todo    | [gr_rev.md](gr/gr_rev.md)                                    | W7           | B2, B3, B6, B7                |
| A7  | `arch-review`          | `ica` | todo    | [gr_mod.md](gr/gr_mod.md)                                    | W9           | D7 (proactive vs reactive)    |

### Cross-Cutting Skills / Hooks table

| #   | Name                           | Form            | Status | Source doc                                                          | Applies to          | Used by         |
| --- | ------------------------------ | --------------- | ------ | ------------------------------------------------------------------- | ------------------- | --------------- |
| B1  | `routing-step-enforcer`        | hook (pre-task) | todo   | [guardrails.md §5](guardrails.md)                                   | all phases          | all impl skills |
| B2  | `push-standards-to-reviewer`   | skill           | todo   | [gr_rev.md](gr/gr_rev.md) Rev2; Op14b                               | `rev`               | A6              |
| B3  | `fresh-context-for-review`     | hook            | todo   | [gr_rev.md](gr/gr_rev.md) Rev1; 3.18                                | `rev`               | A6              |
| B4  | `hitl-afk-label-gate`          | hook (pre-task) | todo   | [guardrails.md](guardrails.md) Gov5a, 3.20                          | `iss`, `ral`, `par` | A3, A4, A5      |
| B5  | `hidden-constraint-checklist`  | skill           | todo   | [gr_algn.md](gr/gr_algn.md) Aln6; [gr_rev.md](gr/gr_rev.md) Rev7    | `aln`, `rev`        | A1, A6          |
| B6  | `module-depth-check`           | skill           | todo   | [gr_mod.md](gr/gr_mod.md) M7; Rev6                                  | `rev`, `ica`        | A6, A7          |
| B7  | `fabrication-check`            | skill           | todo   | [guardrails.md](guardrails.md) Op13; [gr_rev.md](gr/gr_rev.md) Rev8 | `rev`               | A6              |
| B8  | `generated-code-volume-gate`   | hook (pre-edit) | todo   | [guardrails.md](guardrails.md) Op11                                 | `ral`, `par`        | A4, A5          |
| B9  | `persistent-context-minimizer` | skill / audit   | todo   | [guardrails.md](guardrails.md) Op14a, 3.17                          | all (maintenance)   | —               |
| B10 | `subagent-for-exploration`     | skill           | todo   | [gr_algn.md](gr/gr_algn.md) Aln7                                    | `aln`, `res`        | A1, A10         |

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

### W14. Prototype Phase (broadened scope)

- Status: **wip** (phase + core rule + detail doc + workflow doc done; remaining work split into W14a–W14e, each handled in a fresh session).
- Category: **Phase (optional)** — code `pro`. Optional sequential between `aln`/`res` and `prd`; entry from either `aln` (design ambiguity) or `res` (build-to-learn spike). HITL only (Pro6).
- Pocock reference: phase 3 of the 7-phases doc (see [the-7-phases-of-ai-driven-development.md](the-7-phases-of-ai-driven-development.md)) — "Prototype as Taste-Imposition Step" + "Prototype Variant Generation". No named Pocock skill.
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
- Dependency: W14a (sandbox retirement) and W14b (variant template) should be resolved first or in parallel.

### W15. Idea Phase

- Status: **wip** (phase + core rule + detail doc done; skill pending).
- Category: **Phase** — code `ide`. Sequential, **first** phase before `aln`. HITL only (Idea4). Output is `plan/<WI>/idea.md` + `plan/<WI>/status_idea.md` (Idea7); retired with `plan/<WI>/` at WI close per 3.33. PRD Goals section folds it but does not replace it.
- Pocock reference: phase 1 of the 7-phases doc (see [the-7-phases-of-ai-driven-development.md](the-7-phases-of-ai-driven-development.md)) — no named Pocock skill.
- Exists: phase `ide` in [phases.md](phases.md); core rule 3.32 + routing §4.19 in [guardrails.md](guardrails.md); detail doc [gr/gr_idea.md](gr/gr_idea.md) (Idea1–Idea7).
- Missing: skill `distill-idea` (new **A11**) — distills brief / ticket / Slack note into 3–6 major goals, strips detail leaks (Idea2), captures negative goals (Idea3), HITL by construction (Idea4); collapse handling per 3.29 when upstream brief already names goals explicitly (one-line confirmation instead of full pass); writes `plan/<WI>/idea.md` + `plan/<WI>/status_idea.md` per Idea7.
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

- Status: todo.
- Category: **Phase**.
- Pocock reference skill: **"grill me"** skill (walkthrough §0:13:45–0:21:43, gamification brief demo).
- Exists: phase `aln` (`phases.md`); guardrail set `gr/gr_algn.md`; skill A1 `align-concept` listed.
- Missing: skill implementation (A1), hidden-constraint checklist enforcement (B5), subagent dispatch (B10), AFK domain-transcript path (Aln11).
- Pocock skill as additional input: load Pocock's "grill me" walkthrough excerpt (§0:13:45–0:21:43) as source when authoring A1 via `draft-skill-input` → `compile-skill`.
- Next: build A1 skill, wire B5/B10 hooks. No new phase or guardrail.

### W2. PRD

- Status: todo.
- Category: **Phase**.
- Pocock reference skill: **"write a PRD"** skill (walkthrough §0:28:38–0:36:00; fills a PRD template after interviewing).
- Exists: phase `prd` (`phases.md`); skill A2 `compose-prd` listed; PRD template C1 listed.
- Missing: A2 implementation, C1 canonical template content, decision D3 (PRD retention vs. archive).
- Pocock skill as additional input: load Pocock's "write a PRD" walkthrough excerpt (§0:28:38–0:36:00) as source when authoring A2.
- Next: resolve D3, then build C1 + A2. No new phase or guardrail.

### W3. Issue DAG

- Status: todo.
- Category: **Phase**.
- Pocock reference skill: **"PRD to issues"** skill (walkthrough §0:38:49–0:51:38; emits vertical-slice issues with blockers).
- Exists: phase `iss`; skill A3 `prd-to-dag` listed; issue template C2 listed; HITL/AFK gate B4 listed.
- Missing: A3 implementation, C2 template content, vertical-vs-horizontal slicing rule (currently implicit only).
- Pocock skill as additional input: load Pocock's "PRD to issues" walkthrough excerpt (§0:38:49–0:51:38) as source when authoring A3.
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
- Pocock reference skill: **none named** — described as the "fresh-context automated review" technique (walkthrough §1:05:24–1:06:27); no canonical Pocock skill shipped.
- Exists: phase `rev`; `gr/gr_rev.md`; skill A6 `review`; cross-cutting B2 (push standards), B3 (fresh context), B6 (module-depth), B7 (fabrication check).
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
- Exists: phase `ica`; `gr/gr_mod.md`; skill A7 `arch-review`; B6 module-depth check; D7 (proactive `ica` before feature work) open.
- Missing: A7 implementation; D7 decision (guardrail mandate vs. workflow tip).
- Pocock skill as additional input: load Pocock's "improve codebase architecture" walkthrough excerpt (§1:21:08–1:23:04) as source when authoring A7.
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
- Source: `gr/gr_algn.md`. Pocock skill as additional input: "grill me" (walkthrough §0:13:45–0:21:43) — feed into `draft-skill-input` when authoring.

### A2. `compose-prd` skill (phase: `prd`)

- Status: todo.
- Behavior: summarizes alignment transcript into a destination PRD using a fixed template (problem, user problem, solution, user stories, implementation decisions, testing decisions, out-of-scope, module map).
- Constraint: PRD summarizes alignment; does not replace it (Aln13).
- Source: `gr/gr_algn.md`, workflow doc §0:28:38–0:36:00. Pocock skill as additional input: "write a PRD" (same excerpt) — feed into `draft-skill-input` when authoring.

### A3. `prd-to-dag` skill (phase: `iss`)

- Status: todo.
- Behavior: turns PRD into independently grabbable issues with explicit blocking edges, HITL/AFK tags (Gov5a), and vertical-slice preference over horizontal-layer slicing.
- Output: a DAG, not a sequential list.
- TDD sizing constraint: each issue must be sized so it maps to a small set of distinct Reds (one testable behavior per Red). Vague issues that resist single-Red framing fail the sizing check — split or re-grill. Source: `gr_tdd.md` TDD7.
- Source: workflow doc §0:38:49–0:51:38. Pocock skill as additional input: "PRD to issues" (same excerpt) — feed into `draft-skill-input` when authoring.

### A4. `afk-loop` skill (phase: `ral`)

- Status: todo.
- Behavior: picks the next available AFK issue, implements via TDD, runs feedback loops, commits, repeats until a sentinel.
- Preconditions enforced: AFK eligibility per Gov5a, push/pull respected (Op14b). On `ral` entry, pull `gr/gr_tdd.md` before first test or src edit (see `gr_tdd.md` "Pulling This Document" #2).
- Source: workflow doc §0:51:44–0:58:14. Pocock skill as additional input: `~/.claude/skills/ralph/SKILL.md` (once-by-default reference impl) — feed into `draft-skill-input` when authoring.

### A5. `parallel-loop` skill (phase: `par`)

- Status: blocked.
- Blocker: pick orchestration substrate (Sand Castle vs. own worktree+sandbox driver).
- Behavior: planner selects N parallel issues, each in a sandboxed worktree, with reviewer-and-merger agents downstream.
- Source: workflow doc §1:29:47–1:32:39.

### A6. `review` skill (phase: `rev`)

- Status: todo.
- Behavior: clears context (Rev1), pushes routed standards (Rev2, Op14b), reads tests first (Rev4), explicit module-depth assessment (Rev6, gr_mod.md M7), hidden-constraint coverage statement (Rev7), structured output (Rev11).
- Constraint: same-process fresh context (current setup); reviewer-agent split is a later option.
- Source: `gr/gr_rev.md`.

### A7. `arch-review` skill (phase: `ica`)

- Status: todo.
- Behavior: scans codebase for shallow-module opportunities, proposes consolidations behind deeper interfaces, prioritizes by testability gap.
- Source: `gr/gr_mod.md`, workflow doc §1:21:08–1:23:04. Pocock skill as additional input: "improve codebase architecture" (same excerpt) — feed into `draft-skill-input` when authoring.

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

- Status: todo.
- Decision pending: retain in repo vs close-as-done in issue tracker (workflow doc §1:23:04–1:25:15 documentation rot concern).

### C6. Prototype variant presentation template

- Status: **done** (2026-05-18, see W14b).
- Artifact: [`tpl/tpl_var_pres.md`](tpl/tpl_var_pres.md).
- Purpose: machine-parseable shape for prototype variant output (Pro2/Pro4/Pro7/Pro8). Skill (W14e/A9) emits; human picker consumes.
- Slot: C5 reserved for W8 QA notes template; C6 is the next free slot.

### C8. Idea file template

- Status: **done** (2026-05-20).
- Artifact: [`tpl/tpl_idea.md`](tpl/tpl_idea.md).
- Purpose: single parse target for downstream consumers (A1 align-concept reads goals to anchor grilling; A2 compose-prd folds into PRD Goals section; A6 review verifies coverage; A8 qa runs Q11 retirement lint).
- Shape: pair of files under `plan/<WI>/` — `idea.md` (markdown body, no frontmatter, `# Goals` heading, numbered 3–6 entries with `Non-goal:` prefix for negatives, optional `Stripped detail:` lines) + `status_idea.md` (frontmatter only: `status`, `updated`, `owner-issue`).
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

---

## E. Validation / Experiments (from Pocock doc)

- E1. Grill-me on a real ambiguous ticket. Measure: assumptions surfaced, post-implementation scope changes.
- E2. PRD summarization fidelity check — second agent or human compares PRD to grilling transcript.
- E3. Vertical vs horizontal slicing — implement one feature both ways, compare rework.
- E4. Push vs pull standards — measure standards violations per PR before/after.
- E5. Module-depth refactor — run `arch-review` on the repo, measure test-boundary count and cross-module import count before/after.
