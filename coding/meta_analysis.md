# Meta-Analysis: BMAD / bmad-builder, AIUP & HumanLayer RPI vs. this coding-workflow project

**Date:** 2026-05-30 (HumanLayer RPI section added 2026-05-31)
**Why this exists:** the question "should we use BMAD or AIUP?" came up while choosing a workflow for a *different* project (`ai-mail`); the HumanLayer RPI assessment was added when that ecosystem entered the same `ai-mail` selection. This document captures what we learned about how those ecosystems relate to **this** project — the coding-workflow builder defined in [coding_plan.md](coding_plan.md), [phases.md](phases.md), and `guardrails.md`/`gr/`. It is a build-vs-borrow assessment, not a decision to adopt anything.

---

## The frame that drives every conclusion: two layers

This project is not "a workflow." It is two stacked things, and BMAD/AIUP relate to each differently:

1. **Method layer** — the phase model (`ide→aln→res?→pro?→prd→iss→ral/par→qa` + `rev`/`ica`), the 3-mode triage, and the Pocock-sourced *quality discipline* in `guardrails.md`/`gr/` (context-minimization Op14a, pull-not-push routing, TDD-as-spine, fresh-context review, hidden-constraint sweeps, fabrication checks, deep modules). **This is the project's IP.**
2. **Builder layer** — the toolchain that *manufactures* skills (`draft-skill-input → compile-skill → test-skill/make-skill`, regression fixtures, rule→skill maps, freshness tracking) + the `/phase`/`/triage-idea` state machine + the unbuilt "generic workflow builder" track ([coding_plan.md](coding_plan.md) L319–325).

**bmad-builder competes only with the builder layer. AIUP competes only with parts of the method layer (the artifact-producing phases). HumanLayer RPI competes only with parts of the method layer (it is a rival *phase model* + a set of worked cross-cutting subagents) and — unlike BMB — does NOT touch the builder layer at all (it manufactures nothing; its commands are hand-written prose).** Keep that split in mind for everything below.

---

## BMAD / bmad-builder (BMB)

**What it is.** A module within BMAD for *creating* BMAD agents/workflows/modules: Agent Builder, Workflow Builder, Module Builder, a template system, validation tools, and testing utilities. Interactive Q&A ("no manual file editing") that emits ready-to-use skill folders. Agents are persona-shaped (John/Mary/Winston…). Docs: <https://bmad-builder-docs.bmad-method.org/>.

**Where it overlaps.** Squarely with the **builder layer** — BMB is, on paper, the thing we are hand-rolling (skill scaffolding + validation + testing + module packaging).

**Where it may fit (borrow, not adopt).**
- The **Module Builder / domain-packaging pattern** is a worked example of our unbuilt "generic workflow builder" track (domain config → phases → skill bindings → reusable module). Worth studying *before* designing `domain.yaml` / `docs/agents/domain.md`.

**Where it does NOT fit (reject wholesale adoption).**
- **Loses our best innovation.** Our skills are *compiled artifacts* — derived from source guardrail docs, with input/output **regression tests** and staleness detection. BMB *generates* skills via Q&A; it does not give a `source-docs → compile → test → regenerate` pipeline traceable to our rules. Adopting BMB trades away testability + regenerability.
- **Paradigm clash with Op14a (context minimization) and pull-not-push.** BMAD agents are persona-heavy with larger always-on instructions — the opposite of our lean-context design, and the same role ceremony already rejected for solo work.
- **Worst ROI exactly where it overlaps.** The builder/state-machine layer is our *most mature* part (`/phase`, `/triage-idea`, `/distill-idea`, `status`, `visualize`, test harness — built/wip). Almost everything still unbuilt is method-layer (A-skills, B-hooks, C-templates). "Adopt BMB" = discard the working builder to author the missing method skills with a foreign, less-rigorous builder.

**Where to look.** bmad-builder docs → Module Builder + the "Build Your First Module" tutorial, *only* as a blueprint for domain-packaging. Do not install/adopt.

---

## AIUP / aiup-core

**What it is.** The AI Unified Process — spec-driven, RUP-derived (Inception/Elaboration/Construction/Transition), "no code without a use case; no merge without a test traceable to a requirement." Ships Claude Code plugins. `aiup-core` (stack-agnostic) = 5 markdown-producing skills: `/requirements`, `/entity-model`, `/use-case-diagram`, `/use-case-spec`, `/reverse-engineer`. `aiup-vaadin-jooq` (the Construction/testing half) is hard-wired to Java/Vaadin/jOOQ. Docs: <https://unifiedprocess.ai/>, marketplace: <https://github.com/AI-Unified-Process/marketplace>.

**Where it overlaps.** Parts of our **method layer** — specifically the artifact-producing phases (`prd`/`iss` neighborhood; `compose-prd` A2, `prd-to-dag` A3) and the domain-model gap.

**Why it's a closer cousin than BMAD.** AIUP shares our core values: file-based artifacts, stable IDs, traceability, commit-`docs/`-as-memory, review-between-steps, context-light. It is *not* persona-heavy.

**Where it may fit (borrow ready-made skills).**
- **`/entity-model`** — a maintained, tool-agnostic implementation of a domain-model step we don't have. Produces the Mermaid ER + attribute tables.
- **`/use-case-spec`** — a templated, traceable spec producer that maps onto the `prd`/`iss` artifact work (A2/A3) currently sitting as *unbuilt todos*.
- Borrowing these lets our builder effort focus only where we hold a real opinion AIUP lacks (grilling/triage/TDD-AFK/review/deep-modules — the Pocock differentiators).

**Where it does NOT fit.**
- The **Construction/testing half (`aiup-vaadin-jooq`) is stack-locked** (Java/Vaadin/jOOQ) — useless as a general coding-workflow engine.
- AIUP has **no validation/challenge step** (no grill-me equivalent), no context-minimization machinery, no AFK/parallel execution model — i.e. it does not touch our method's most opinionated parts.

**Where to look.** `aiup-core/skills/entity-model/SKILL.md` and `aiup-core/skills/use-case-spec/SKILL.md` in the marketplace repo — read the bodies, assess as borrowable artifact producers for the `prd`/`iss` phases.

---

## HumanLayer RPI + FIC (Research-Plan-Implement)

**What it is.** The `.claude/` directory shipped in `humanlayer/humanlayer` (cloned locally at `C:\PROJ\github\humanlayer`): a drop-in set of Claude Code slash commands (`/research_codebase`, `/create_plan`, `/implement_plan`, `/iterate_plan`, `/validate_plan`, `/commit`, `/describe_pr`, `/create_handoff`, `/resume_handoff`, + `_nt` no-thoughts variants) plus six read-only research **sub-agents** (`codebase-locator`, `codebase-analyzer`, `codebase-pattern-finder`, `thoughts-locator`, `thoughts-analyzer`, `web-search-researcher`). The method is **Research → Plan → Implement** with **Frequent Intentional Compaction (FIC)** underneath: design the workflow around context management, keep window utilization at 40–60% by distilling each phase into a markdown artifact (`thoughts/shared/{research,plans,handoffs}/`) before the next. Apache-2; the sibling repos are `12-factor-agents` (principles) and `advanced-context-engineering-for-coding-agents` (the methodology doc). The `humanlayer` SDK (`require_approval`) is deprecated; CodeLayer (an orchestration IDE) is the company's current product — neither is relevant to *this* project.

**Where it overlaps.** Parts of our **method layer** — it is a **rival phase model**: `create_plan` ≈ our `aln`/`prd` neighborhood; `implement_plan` (phase-gated, pauses for human verification, splits automated vs manual success criteria) ≈ our `ral`/`par` + HITL gates; `validate_plan` ≈ our `rev`. Its **FIC** is a worked operationalization of our most-cited principle, **Op14a (context minimization)**. Its six research sub-agents are battle-tested implementations of two of our *unbuilt* cross-cutting rows — **B10 (`subagent-for-exploration`)** and **B11 (`subagent-for-artifact-drafting`)**.

**Why it's a cousin (and how it differs from the other two).** Shares our values like AIUP does — file-based artifacts, commit-`docs/`-as-memory (the `thoughts/` tree), review-between-steps, context-light by design — and goes further on one axis we care about: it is **natively Claude Code** (commands + sub-agents), which is the exact substrate this project targets. Crucially, **it does not compete with the builder layer at all**: RPI manufactures nothing, so (unlike BMB) adopting pieces of it costs us no builder maturity.

**Where it may fit (borrow worked artifacts).**
- **The six research sub-agents (`.claude/agents/`)** — ready-made, "documentarian-not-critic", isolated-context-window implementations of **B10/B11**, which currently sit as unbuilt todos. Strongest borrow: read the agent bodies and assess against our Aln7 (subagent-for-exploration) and Aln17/Adr5 (subagent-for-artifact-drafting) sources.
- **The `implement_plan` phase-gate pattern** — per-phase pause + automated-vs-manual success-criteria split — as a concrete shape for **A4 (`afk-loop`, W5)** and our HITL/AFK label gate (B4).
- **FIC** — a documented, externally-validated (300k-LOC Rust) operationalization of **Op14a**; cite it as a reference in `guardrails.md`/`gr/` rather than reinventing the rationale.

**Where it does NOT fit (reject wholesale adoption).**
- **No compiled-and-tested-skill model — same loss as BMB.** RPI commands are hand-written prose with no `source-docs → compile → regression-test → regenerate` pipeline. Adopting them wholesale trades away testability + regenerability, exactly the IP MA4 protects.
- **Fixed 3-phase pipeline; no triage/mode system, no idea/prototype phases.** Our 3-mode entry triage (`/triage-idea`) and `ide`/`pro` phases are differentiators RPI lacks — it assumes you already know you're implementing.
- **No grilling / adversarial step.** `create_plan` is "skeptical" but not `grill-me`/`grill-with-docs` adversarial; our hardest method opinion is absent.
- **Brownfield-optimized.** FIC's headline value is large *existing* codebases; for a greenfield workflow-builder it is mostly the sub-agents + the phase-gate discipline that transfer, not the compaction superpower.

**Where to look.** `C:\PROJ\github\humanlayer\.claude\agents\*.md` (the six sub-agents — primary borrow target for B10/B11) and `\.claude\commands\create_plan.md` + `implement_plan.md` (phase model + success-criteria split). Methodology doc: `humanlayer/advanced-context-engineering-for-coding-agents/ace-fca.md`. Borrow the sub-agents + phase-gate pattern; do not adopt the command set wholesale.

---

## Cross-cutting risk: meta-overkill

The original goal that spawned all of this (Pareto, fun, no overkill, ship results that can be enhanced) sits in tension with the framework's current size: a ~900-line plan, ~13 skills, ~11 hooks, ~8 templates, ~10 open decisions — **most still unbuilt**. The *mature* parts are infrastructure (state machine, test harness); the parts that would actually let the framework be *used* (align → spec → issues → TDD loop) are mostly the missing ones. The framework is most valuable the moment it is *good enough to run on one real project*, not the moment it is complete. A "good-enough cut line" is worth defining explicitly.

---

## Recommended actions (referenced by coding_plan.md todos)

- **MA1 — Borrow-vs-author gap analysis.** For each unbuilt A-skill (A1–A10), mark: *borrow* (aiup-core `/entity-model`, `/use-case-spec`; Pocock originals `grill-me`, `to-prd`, `to-issues`, `review`, `prototype`, `tdd`, `ralph`) vs. *author via our toolchain* (only where it encodes an opinion nothing off-the-shelf has). Output: a table that says where to keep building and where to stop reinventing.
- **MA2 — Study BMB module-packaging as a blueprint.** Read bmad-builder's Module Builder + "Build Your First Module" before designing the `domain.yaml` / domain-layer extraction ([coding_plan.md](coding_plan.md) L319–325). Borrow structure, do not adopt the tool.
- **MA3 — Evaluate aiup-core `/entity-model` + `/use-case-spec` as borrowable artifact producers** for the `prd`/`iss` neighborhood (A2/A3), instead of authoring from scratch. Read the two SKILL.md bodies; judge fit against our templates (C1 PRD, C2 issue) and traceability conventions.
- **MA4 — Record the "no wholesale BMAD/BMB" decision.** Capture as a D-item or ADR: rejected because of context-min/persona paradigm clash + loss of the compiled-and-tested-skill model; builder layer already mature. Keeps the decision from being relitigated.
- **MA5 — Scope-control / "good-enough" cut line.** Re-evaluate framework size against the Pareto/fun/no-overkill goals; define the minimal phase-skill set that makes the framework usable end-to-end on one real project, and defer the rest.
- **MA6 — Evaluate HumanLayer RPI's six research sub-agents as borrowable B10/B11 implementations.** Read `C:\PROJ\github\humanlayer\.claude\agents\*.md` (`codebase-locator`, `codebase-analyzer`, `codebase-pattern-finder`, `thoughts-locator`, `thoughts-analyzer`, `web-search-researcher`); judge the documentarian-not-critic + isolated-context-window pattern against our B10 (`subagent-for-exploration`, source Aln7) and B11 (`subagent-for-artifact-drafting`, source Aln17/Adr5) instead of authoring from scratch. See [meta_analysis.md](meta_analysis.md) §"HumanLayer RPI + FIC".
- **MA7 — Borrow RPI's `implement_plan` phase-gate pattern + cite FIC for Op14a; fold the "no wholesale RPI" rationale into MA4.** Adopt the per-phase-pause + automated-vs-manual success-criteria split as the concrete shape for A4 (`afk-loop`, W5) and the B4 HITL/AFK gate; cite FIC as the worked operationalization of Op14a in `guardrails.md`/`gr/`. Extend the MA4 decision record: RPI rejected for wholesale adoption for the same reason as BMB (no compiled-and-tested-skill model) plus its fixed pipeline / missing triage-mode + grilling step. See [meta_analysis.md](meta_analysis.md) MA7.
