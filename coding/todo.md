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
      - [W14d. Rejected-Variant Capture into grill-me](#w14d-rejected-variant-capture-into-grill-me)
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
  - [C6. Prototype variant presentation template](#c6-prototype-variant-presentation-template)
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

| #    | Pocock title               | Category                   | Status          | skill     | hook | Pocock reference skill                              | Maps to                                                                 |
| ---- | -------------------------- | -------------------------- | --------------- | --------- | ---- | --------------------------------------------------- | ----------------------------------------------------------------------- |
| W6   | Agentic TDD                | Technique                  | done            | no        | rcmd | —                                                   | `gr/gr_tdd.md` + §4.16 routing                                          |
| W14a | Sandbox Retirement         | Enforcement (W14)          | todo            | no        | yes  | none                                                | adapt W13's `owner-issue`+Q11 to directories                            |
| W14b | Variant Template           | Template (C6, W14)         | done            | no        | no   | none                                                | C6 = [tpl/tpl_variant_presentation.md](tpl/tpl_variant_presentation.md) |
| W14c | Res→Pro Fact Persistence   | Decision (D-new, W14)      | done            | no        | no   | none                                                | `res`/`pro` boundary                                                    |
| W14d | Rejected-Variant→grill-me  | Wiring (W14)               | done (contract) | no        | no   | none                                                | A1 (`grill-me`) integration                                             |
| W14e | Prototype Skill            | **NEW Phase** / Skill (A9) | wip             | yes (new) | no   | none (Pocock phase 3)                               | `pro` added, `gr_prototype.md` + `wf/wf_prototype.md`                   |
| W12a | Review Standards Sources   | Manual / Audit             | todo            | no        | no   | —                                                   | `standards_guardrails_sources.md`                                       |
| W12b | Standards Descriptions     | Rule/Convention            | todo            | rcmd      | no   | —                                                   | Op14b + `gr/` description quality + skill preconditions                 |
| W12c | Standards Hook Enforcement | Rule/Convention            | todo            | no        | rcmd | —                                                   | B1 routing-step enforcer                                                |
| W1   | Grilled Design Concept     | Phase                      | todo            | yes (poc) | no   | "grill me" skill                                    | `aln` (exists)                                                          |
| W2   | PRD                        | Phase                      | todo            | yes (poc) | no   | "write a PRD" skill                                 | `prd` (exists)                                                          |
| W3   | Issue DAG                  | Phase                      | todo            | yes (poc) | no   | "PRD to issues" skill                               | `iss` (exists)                                                          |
| W4   | Ralph Once Loop            | Execution mode             | todo            | yes (poc) | no   | `/ralph` skill (`~/.claude/skills/ralph/`)          | variant of `ral`                                                        |
| W5   | AFK Implementation Loop    | Phase                      | blocked         | yes (new) | rcmd | none — `afk.sh` loop script (not a skill)           | `ral` (exists), D4 open                                                 |
| W7   | Fresh-Context Review       | Phase                      | todo            | yes (new) | rcmd | none named — "fresh-context automated review"       | `rev` (exists)                                                          |
| W8   | Manual QA                  | **NEW Phase**              | wip             | yes (new) | no   | none — human-driven phase in Pocock's walkthrough   | `qa` added, `gr_qa.md` drafted                                          |
| W9   | Deep-Module Architecture   | Phase/Initiative           | todo            | yes (poc) | no   | "improve codebase architecture" skill               | `ica` (exists), D7 open                                                 |
| W10  | Parallel Agents            | Execution mode             | blocked         | yes (new) | no   | none — Sand Castle orchestration tool (not a skill) | `par` (exists), substrate TBD                                           |
| W13  | Research Caching           | Phase (optional)           | wip             | yes (new) | yes  | none named — Pocock phase 2 + `research.md` cache   | `res` added, `gr_research.md` drafted, §3.27 + §4.17 added              |

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

### W14. Prototype Phase (broadened scope)

- Status: **wip** (phase + core rule + detail doc + workflow doc done; remaining work split into W14a–W14e, each handled in a fresh session).
- Category: **Phase (optional)** — code `pro`. Optional sequential between `aln`/`res` and `prd`; entry from either `aln` (design ambiguity) or `res` (build-to-learn spike). HITL only (Pro6).
- Pocock reference: phase 3 of the 7-phases doc (see [the-7-phases-of-ai-driven-development.md](the-7-phases-of-ai-driven-development.md)) — "Prototype as Taste-Imposition Step" + "Prototype Variant Generation". No named Pocock skill.
- Exists: phase `pro` in [phases.md](phases.md); core rule 3.28 + routing §4.18 + parallel-table row in [guardrails.md](guardrails.md); detail doc [gr/gr_prototype.md](gr/gr_prototype.md) (Pro1–Pro8); workflow doc [wf/wf_prototype.md](wf/wf_prototype.md) covering all three flavors; cross-ref Res10 in [gr/gr_research.md](gr/gr_research.md).
- Trigger gate (Pro1): irreversibility OR cost asymmetry. Replaces the deleted Aln17 "genuinely visual" gate.
- Flavors (Pro2): FE/UX, architecture, integration — one flavor per `pro` invocation.
- Remaining work: see W14a (sandbox retirement), W14b (variant template), W14c (res→pro fact persistence), W14d (rejected-variant→grill-me wiring), W14e (skill).
- Resolves: D8-bis (prototype as phase, not technique). Pocock alignment confirmed.

### W14a. Sandbox Retirement Enforcement

- Status: **todo** (fresh session).
- Parent: W14.
- Behavior: design and implement retirement enforcement for prototype sandbox **directories** (not single files). Adapt W13's pattern: `owner-issue` provenance field in a manifest file at the sandbox root + `qa` Q11-style merge-gate check that fails if any sandbox path survives merge without its owner-issue being closed. Sandbox = directory, so the check must walk directory trees, not just grep for a file header.
- Source: W13 resolution (see `consider_7_phases_todo.md` Item 8); Pro3 (deletion rule); gr_prototype.md.

### W14b. Variant Presentation Template

- Status: **done** (2026-05-18).
- Parent: W14.
- Slot: **C6**. C5 reserved for W8 QA notes template.
- Artifact: [`tpl/tpl_variant_presentation.md`](tpl/tpl_variant_presentation.md) — first template in a new `tpl/` folder (parallel to `gr/`, `wf/`).
- Format: YAML frontmatter (machine-parseable schema) + markdown body (human-readable). Skill (W14e) owns YAML; human edits body only.
- Pro4 enforcement: schema **omits** `recommendation`/`preferred`/`best`/`agent_pick`/`score`/`ranking` fields and **lists them as forbidden** (schema rejects). Body rules forbid subjective vocabulary (better, worse, cleaner, simpler, recommended, preferred, ideally, obviously, clearly, the right/wrong choice). Reviewer (`rev`) flags any occurrence.
- Pro7 coverage: per-variant `hidden_constraints` block requires all 7 classes (security, permissions, retention, migrations, observability, api_compat, concurrency) marked covered / not_applicable / missing. `blocking_constraint` set when any = missing.
- Pro8 coverage: `captured_responses` field on each variant for integration flavor; no synthetic-payload field.
- Cross-refs: `gr/gr_prototype.md` Pro4 + `wf/wf_prototype.md` step 5 point at C6 as the artifact.
- Validation hooks (deferred to D1): schema lint (forbidden fields, variant count, trigger flag, hidden-constraint completeness); vocabulary lint (body subjective terms); sandbox-retirement gate hook to W14a via `owner_issue` field.
- Dependents: W14e (A9 skill emits this); W14d (rejected-variant artifact for grill-me intake — `decision_outcome.rejected` is the carry).

### W14c. Res→Pro Fact Persistence Decision

- Status: **done** (2026-05-18).
- Parent: W14.
- Decision: **Option B — caller-persists, applied symmetrically to all callers.** `pro` emits exactly one artifact (C6 variant doc, [`tpl/tpl_variant_presentation.md`](tpl/tpl_variant_presentation.md)) with chosen variant marked and `captured_responses` populated where applicable. The caller (`aln`/`res`/`prd`) reads C6 on return and updates its own files: `aln` → Aln12 module map + Aln15; `res` → `research/<topic>.md` under existing `owner-issue` (Res4) header; `prd` → implementation-decisions section + rejected-alternatives. `pro` never writes any caller's files directly.
- Rationale: keeps `pro` caller-agnostic (one behavior, no conditional write-mode per caller); each phase keeps ownership of its file conventions; one handoff surface (C6) instead of three.
- Edits: `gr/gr_prototype.md` Pro5 (rewritten — symmetric caller-persists for all three callers); `gr/gr_research.md` Res10 (concrete Stripe-webhook handoff example); `wf/wf_prototype.md` step 7 (rewritten — same symmetric rule).
- Affects: A9 (W14e) skill prompt must emit C6 artifact only — must NOT write `research/<topic>.md`, Aln12, Aln15, or PRD sections directly. Caller does the writing.

### W14d. Rejected-Variant Capture into grill-me

- Status: **done — contract** (2026-05-18). Skill wiring lands when A1 is built (W1).
- Parent: W14.
- Artifact format: reuses C6 (`tpl/tpl_variant_presentation.md`) `decision_outcome.rejected[]` + `rationale_by_human` — no new artifact needed.
- Intake contract (gr_alignment.md Aln15, expanded section "Intake from `pro`"): on `aln` resume after `pro` exit, A1 reads `<sandbox_path>/variants.md` **before** sandbox deletion; for each rejected id appends an Aln15 entry citing variant summary + observable losing facts + `rationale_by_human`; updates Aln12; signals capture complete to unblock Pro3 deletion. Fail-closed if C6 unreadable or `decision_outcome.chosen` null.
- Replay contract: existing Aln15 entries load as grilling context; A1 does not re-propose rejected options — cites prior rejection if branch reopened.
- Ordering enforced: gr_prototype.md Pro3 + wf_prototype.md step 8 now block sandbox deletion until caller capture signals complete.
- Edits: `gr/gr_alignment.md` Aln15 (expanded with intake + replay contracts); `gr/gr_prototype.md` Pro3 (ordering with caller capture); `wf/wf_prototype.md` step 8 (fail-closed); `tpl/tpl_variant_presentation.md` Notes on Interaction (caller-persists + read-before-delete).
- Depends on: W14e (A9 emits C6 — schema already defined). W1 (A1 implementation) consumes this contract.

### W14e. Prototype Skill (A9)

- Status: **todo** (fresh session).
- Parent: W14.
- Behavior: `prototype` skill that (1) asks Pro1 trigger-gate questions (irreversibility / cost asymmetry), (2) generates 2–3 variants per the chosen flavor (Pro2: FE/UX, architecture, integration), (3) runs Pro7 hidden-constraint check on each variant, (4) presents variants to human with observable-facts-only framing (Pro4), (5) captures Aln15 negative decisions for rejected variants, (6) enforces Pro3 deletion of sandbox code after decision.
- Maps to: A9 (new skill slot); source docs `gr/gr_prototype.md`, `wf/wf_prototype.md`.
- Dependency: W14a (sandbox retirement) and W14b (variant template) should be resolved first or in parallel.

### W13. Research Caching

- Status: **wip** (phase + core rule + detail doc + retirement enforcement done; skill, template pending).
- Category: **Phase (optional)** — code `res`. Optional sequential between `aln` and `prd`; can also fire mid-`aln` when grilling stalls on external-dependency facts.
- Pocock reference: phase 2 of the 7-phases doc (see [the-7-phases-of-ai-driven-development.md](the-7-phases-of-ai-driven-development.md)) — no named Pocock skill.
- Exists: phase `res` in [phases.md](phases.md); core rule 3.27 + routing §4.17 in [guardrails.md](guardrails.md); detail doc [gr/gr_research.md](gr/gr_research.md); subagent dispatch B10 (existing); retirement enforcement = `owner-issue` provenance field (Res4) + pre-commit lint + `qa` Q11 merge-gate check (resolved 2026-05-18, see `consider_7_phases_todo.md` Item 8).
- Missing: skill `do-research` (new A9?) — gathers facts via subagent, writes `research/<topic>.md` with Res4 provenance header; template (new C6?) for the research file shape including the `owner-issue` field; decision on whether `iss` decomposition should reference the research file path explicitly; pre-commit lint implementation (mechanical, deferred to substrate decision D1).
- Next: build A9 + C6; wire B10 dispatch into A1 (`grill-me`) so alignment can spawn research without leaving `aln`; implement the `owner-issue` lint once skill substrate (D1) is settled.

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

### C6. Prototype variant presentation template

- Status: **done** (2026-05-18, see W14b).
- Artifact: [`tpl/tpl_variant_presentation.md`](tpl/tpl_variant_presentation.md).
- Purpose: machine-parseable shape for prototype variant output (Pro2/Pro4/Pro7/Pro8). Skill (W14e/A9) emits; human picker consumes.
- Slot: C5 reserved for W8 QA notes template; C6 is the next free slot.

---

## D. Open Questions / Decisions Before Building

- D1. Skill substrate — Claude Code skills only, or also `AGENTS.md`-style instructions, or both? Affects how push/pull is implemented.
- D2. Reviewer process — confirmed: same process, fresh context (current). Reassess once Sand-Castle-style orchestration is in scope.
- D3. **Resolved** (2026-05-17, enforcement closed 2026-05-18) — answered by guardrail 3.24: PRDs are stored externally (e.g. GitHub Issues) and closed when done; not retained in working tree. Same shape extended to research files by 3.27 (deleted at sprint/feature close). Enforcement: pre-commit lint (PRD paths forbidden in-tree; research files require `owner-issue` field) + `qa` Q11 merge-gate check verifies owner-issue close triggers research deletion. See `consider_7_phases_todo.md` Item 8.
- D4. AFK sandbox — pick a sandboxing approach (Docker, Windows job objects, worktree-only). Affects Gov11 and `ralph-loop` precondition.
- D5. Model selection per role — confirm pattern (stronger model for review, faster for implementation) and how it is enforced.
- D6. Token-status visibility — adopt a status-line / token-meter so context proximity to dumb zone is visible (Pocock Experiment 1).
- D7. Proactive `ica` before feature work — Pocock's #1 recommendation: run `improve-codebase-architecture` *before* starting new feature work, not only reactively. Currently tracked as a skill (A7) and phase (`ica` in `phases.md`), but no guardrail mandates or suggests running it proactively. Decision: guardrail-level rule, workflow guidance, or leave as skill-level suggestion?
- D8. **Resolved** (2026-05-15) — added as Aln17 in `gr/gr_alignment.md`. Throwaway 2–3 FE prototypes when visual/UX ambiguity blocks alignment; decision made in `aln`. Skill form rejected (over-prescription risk).
- D9. QA loop convergence — currently human-verdict (3.30 / Q9). Decide later whether to add a mechanized option: typed acceptance-criteria checklist tied to PRD template C1, hard-gated. Postponed until C1 lands and a few QA sessions are observed. Trigger to revisit: repeated drift in pass verdicts or AFK-mode runs needing gate-able criteria.

---

## E. Validation / Experiments (from Pocock doc)

- E1. Grill-me on a real ambiguous ticket. Measure: assumptions surfaced, post-implementation scope changes.
- E2. PRD summarization fidelity check — second agent or human compares PRD to grilling transcript.
- E3. Vertical vs horizontal slicing — implement one feature both ways, compare rework.
- E4. Push vs pull standards — measure standards violations per PR before/after.
- E5. Module-depth refactor — run `improve-architecture` on the repo, measure test-boundary count and cross-module import count before/after.
