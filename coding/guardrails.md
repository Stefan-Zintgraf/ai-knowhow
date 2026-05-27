# AI Coding Guardrails

Purpose: Compact overview of core rules and routing index to detailed guardrail documents.

---

## 1. Core Idea

Guardrails are **constraints that protect system intent** — not a coding style guide.

This document is intentionally small. It contains:

- A short framing (mental model).
- A small set of **core** rules that apply to every task.
- A **routing index** of guardrail categories with pointers to detail documents (`gr/gr_*.md`).

The AI agent does not read every detail document by default. It identifies which categories apply to the current task and loads only those.

Applies to both greenfield and brownfield work. Context-specific emphasis lives in [gr/gr_brownfield.md](gr/gr_brownfield.md) and [gr/gr_greenfield.md](gr/gr_greenfield.md).

---

## 2. Mental Model

```
AI coding quality = Context × Constraints × Verification × Human judgment
```

Weakness in any factor creates risk. The guardrails address **Constraints**; the workflow document addresses **Context** and **Human judgment**; verification rules address **Verification**.

---

## 3. Core Rules

Apply to every AI-assisted planning or implementation task. Each entry is a headline plus a one-line rule. Detail and nuance live in the referenced category document.

**Phase relevance.** Each rule carries a `Fires:` line showing how strongly the rule applies in each workflow bucket. Values: `none`, `low`, `medium`, `high`. Buckets are **Plan**, **Implement**, **Verify**. Workflow phases (ide, aln, res, pro, prd, iss, ral, par, qa, rev, ica) and their mapping to these buckets are defined in [phases.md](phases.md). A rule never disappears — `none` means the rule rarely produces decisions in that bucket, not that it can be ignored.

### 3.1 Minimize Scope

Fires: Plan=high, Implement=medium, Verify=none
The agent must actively narrow the task to the smallest useful, verifiable change. On a new project, orientation scope (sketch, vocabulary, target slice) may be broader than change scope — but the first deliverable is still the smallest useful slice. See [gr/gr_governance.md](gr/gr_governance.md) and [gr/gr_greenfield.md](gr/gr_greenfield.md).

### 3.2 Do Not Mix Concerns

Fires: Plan=high, Implement=high, Verify=low
Feature work, bug fixes, refactoring, formatting, migrations, dependency upgrades, and architectural changes must not be combined in one change. See [gr/gr_coding_style.md](gr/gr_coding_style.md).

### 3.3 Respect Existing Behavior

Fires: Plan=high, Implement=high, Verify=medium
Existing behavior is treated as intentional until proven otherwise. See [gr/gr_brownfield.md](gr/gr_brownfield.md).

### 3.4 Make Assumptions Visible

Fires: Plan=high, Implement=medium, Verify=low
Distinguish facts (from code, tests, docs, user input) from assumptions and open questions. See [gr/gr_governance.md](gr/gr_governance.md).

### 3.5 Avoid Speculative Design

Fires: Plan=high, Implement=high, Verify=none
No abstractions, frameworks, extension points, or generic mechanisms for hypothetical future needs. See [gr/gr_coding_style.md](gr/gr_coding_style.md).

### 3.6 Verify Changes

Fires: Plan=medium, Implement=low, Verify=high
Every change must state how it is verified (tests, static analysis, build, manual review, acceptance criteria). See [gr/gr_testing_verification.md](gr/gr_testing_verification.md).

### 3.7 Stop on High-Risk Decisions

Fires: Plan=high, Implement=high, Verify=medium
The agent must pause and ask before public API changes, data migrations, security-sensitive changes, safety-critical logic changes, concurrency changes, or broad architecture changes. See [gr/gr_governance.md](gr/gr_governance.md).

### 3.8 No Hardcoded Secrets

Fires: Plan=low, Implement=high, Verify=medium
Secrets, tokens, keys, credentials must never appear in source, tests, fixtures, logs, or commit history. See [gr/gr_security_compliance.md](gr/gr_security_compliance.md).

### 3.9 No Bypass of Existing Abstraction

Fires: Plan=medium, Implement=high, Verify=low
The agent must not circumvent an existing abstraction, layer, or anti-corruption boundary without explicit approval. See [gr/gr_architecture.md](gr/gr_architecture.md).

### 3.10 Preserve Public API Compatibility

Fires: Plan=high, Implement=high, Verify=medium
Public API shape and behavior must remain compatible unless the task explicitly authorizes a breaking change. See [gr/gr_architecture.md](gr/gr_architecture.md).

### 3.11 No Silent Dependency Changes

Fires: Plan=medium, Implement=high, Verify=low
Adding, removing, or upgrading third-party dependencies requires explicit approval. See [gr/gr_dependencies.md](gr/gr_dependencies.md).

### 3.12 Provide Verification Evidence

Fires: Plan=none, Implement=low, Verify=high
The final response must contain a concise diff summary plus the verification result (commands run, tests passed, checks performed). See [gr/gr_operational.md](gr/gr_operational.md).

### 3.13 Use Domain Language Consistently

Fires: Plan=high, Implement=high, Verify=low
Terms from the project's ubiquitous language must be used as defined; forbidden synonyms must not be introduced. See [gr/gr_domain_language.md](gr/gr_domain_language.md).

### 3.14 No Fabrication

Fires: Plan=high, Implement=high, Verify=medium
The agent must not invent APIs, function names, file paths, library symbols, or configuration values. Unverifiable references are flagged as assumptions, never stated as facts. See [gr/gr_operational.md](gr/gr_operational.md).

### 3.15 Read Before Write

Fires: Plan=high, Implement=high, Verify=medium
The agent reads the affected code and its callers in the current session before proposing or making a change. Edits to unread code must be flagged, not silently performed. See [gr/gr_operational.md](gr/gr_operational.md).

### 3.16 Disagree Visibly

Fires: Plan=high, Implement=high, Verify=high
When the agent believes a user instruction violates a guardrail, contradicts evidence, or risks regression, it states the disagreement with reasoning before complying. Silent compliance is forbidden. See [gr/gr_governance.md](gr/gr_governance.md).

### 3.17 Push for Reviewer, Pull for Implementer
I
Fires: Plan=low, Implement=medium, Verify=high
Coding-standard and guardrail detail documents are **pulled** on demand by the implementer (kept out of the always-on context) and **pushed** into the reviewer's context up front. Always-on context is kept minimal so work starts in the smart zone. See [gr/gr_operational.md](gr/gr_operational.md) (Op14a, Op14b) and [gr/gr_rev.md](gr/gr_rev.md).

### 3.18 Review Runs in a Fresh Context

Fires: Plan=none, Implement=low, Verify=high
Review of a change is performed in a context that does not contain the implementer's prior conversation, plan, or scratch reasoning. Same-context self-review is forbidden because it produces self-justification, not review. See [gr/gr_rev.md](gr/gr_rev.md) (Rev1).

### 3.19 Prefer Deep Modules

Fires: Plan=high, Implement=medium, Verify=high
Modules expose small interfaces and hide significant functionality. Shallow modules with many small pieces and tangled cross-dependencies are an anti-pattern, especially because AI tends to default to width. Module-shape decisions are made in alignment/PRD, checked explicitly in review. See [gr/gr_mod.md](gr/gr_mod.md).

### 3.20 Declare Autonomy: HITL vs AFK

Fires: Plan=high, Implement=high, Verify=medium
Every task is labeled human-in-the-loop or AFK at the start. `aln` and `prd` are HITL-only. AFK requires resolved decisions, no high-risk surface, sandboxed blast radius, and automatable verification. Silent promotion HITL → AFK is forbidden. See [gr/gr_governance.md](gr/gr_governance.md) (Gov5a).

### 3.21 Reach Alignment Before Planning Artifacts

Fires: Plan=high, Implement=low, Verify=none
Before a PRD, issue decomposition, or implementation begins, the agent and human reach a shared **design concept** via a grilling pass: one question at a time, branches walked, hidden constraints (security, permissions, retention, migrations, observability, API compat, concurrency) explicitly raised. The PRD summarizes alignment; it does not replace it. See [gr/gr_algn.md](gr/gr_algn.md).

### 3.22 Strict Test-Driven Development (TDD)

Fires: Plan=low, Implement=high, Verify=high
The agent must write failing tests before writing implementation code (Red-Green-Refactor), including for frontend/visual tasks. Writing tests after the fact is forbidden. **Exemption:** in `direct-edit` mode (per 3.29 / gr_idea.md Idea8), TDD may be relaxed under HITL-confirmed carve-outs: carve-out A (behavior-bearing change with sufficient existing tests, run green pre/post) or carve-out B (behavior-free change, verified by lint + spell-check + HITL eyeball). Silent application of either carve-out is forbidden. See [gr/gr_tdd.md](gr/gr_tdd.md) TDD1–TDD11.

### 3.23 Enforce Vertical Slices

Fires: Plan=high, Implement=medium, Verify=low
Tasks must be sliced vertically (crossing UI, API, DB layers) to deliver testable, integrated behavior early. Horizontal layer-by-layer slicing is forbidden. See [gr/gr_governance.md](gr/gr_governance.md).

### 3.24 Prevent Documentation Rot (Retire PRDs)

Fires: Plan=high, Implement=low, Verify=none
Old PRDs and plans must not be kept indefinitely in the repository files where they can mislead future agents. Store journey documents and PRDs externally (e.g. GitHub Issues) and close them when done. Enforcement: paths matching `prd/**`, `**/PRD-*.md`, or `**/*_prd.md` are forbidden in the working tree (pre-commit lint); the PRD body lives in the owning issue, not in the repo. See [gr/gr_documentation.md](gr/gr_documentation.md).

### 3.25 Clear Context Over Compaction

Fires: Plan=high, Implement=high, Verify=high
The agent must start fresh sessions (clear context) instead of summarizing long histories (compacting context). If the agent cannot physically clear its own context, it must stop and ask the human (HITL) to do so to prevent entering the dumb zone. See [gr/gr_operational.md](gr/gr_operational.md).

### 3.26 Plan via Dependency Graphs (DAGs)

Fires: Plan=high, Implement=none, Verify=none
When decomposing a PRD into tasks, the agent must structure the plan as an issue DAG (Directed Acyclic Graph) of independently grabbable issues with explicit blocking edges. What is forbidden is **plan shape that bakes in forced ordering not justified by real blocking edges** ("Phase 1, Phase 2, Phase 3" lists). **Execution mode is orthogonal:** sequential execution over a DAG (single-agent `ral`) is allowed and often preferred; parallel execution (`par`) is a bonus when blocking edges permit. See [gr/gr_governance.md](gr/gr_governance.md).

### 3.27 Retire Research Artifacts

Fires: Plan=high, Implement=low, Verify=low
Sprint-scoped research files (`research/<topic>.md`) are cached external knowledge, not durable documentation. They must be **deleted** when the sprint or feature closes — stale research actively misleads future agent runs because it looks authoritative but reflects yesterday's API or codebase. Distinct from 3.24 (PRDs move to external trackers); research files live in the working tree briefly, then are removed outright. Enforcement: every `research/<topic>.md` declares a single `owner-issue: #NNN` (the PRD/feature epic) in its Res4 provenance header; pre-commit lint rejects a research file without the field. Retirement trigger = owner issue closes → the same PR that closes the feature deletes the file, verified by Q11 in `qa`. See [gr/gr_res.md](gr/gr_res.md).

### 3.28 Prototype Hard-to-Reverse Decisions

Fires: Plan=high, Implement=low, Verify=low
When grilling cannot resolve a design decision in words AND either (a) the decision is hard / expensive to reverse once code lands, OR (b) the wrong-choice cost vastly exceeds the cost of building 2–3 throwaway variants, the agent enters phase `pro`: produce 2–3 disposable variants (FE/UX, architecture, or integration — one flavor per invocation), let the human pick, record rejected variants as negative decisions, **delete the sandbox before** production impl begins. Agent does not self-judge. `pro` is HITL by construction. See [gr/gr_proto.md](gr/gr_proto.md).

### 3.29 Right-Size the Workflow (Mode Selection in `ide`)

Fires: Plan=high, Implement=low, Verify=low
The full pipeline is scale-invariant — trivial tasks **collapse** phases rather than skip them silently. Mode selection is the named entry-triage decision owned by the `ide` phase (gr_idea.md Idea8): the agent proposes one of three modes — `direct-edit` (`ide`→`ral`→`qa`), `mini` (`ide`→`aln`-collapsed→`ral`→`qa`), `full` (full pipeline) — based on the 4-axis matrix (design ambiguity, blast radius, reversibility, existing test coverage); the human confirms. **Tripwire surfaces** — public API, schema, auth, security, safety-critical, concurrency, broad architecture — force `full` regardless of axis scores. Mid-task tripwire discovery triggers 3.37 halt. Silent mode pick or silent mode change is forbidden. See [gr/gr_idea.md](gr/gr_idea.md) Idea8 + Idea11 and [gr/gr_governance.md](gr/gr_governance.md) (Gov5b).

### 3.30 Converge the QA Loop on Human Verdict

Fires: Plan=none, Implement=low, Verify=high
The plan → execute → QA loop (`iss → ral|par → qa → fix-now → iss` or pass) terminates on an explicit human verdict, not a mechanized checklist. Pass requires (a) zero fix-now findings remaining and (b) PRD intent met in the human's judgment; `pass-with-backlog` is allowed — backlog findings do not block convergence. Silent downgrading of fix-now → backlog to force a pass is forbidden. Mechanized convergence (typed AC-checklist gate) is deferred (coding_plan.md D9). See [gr/gr_qa.md](gr/gr_qa.md) (Q9).

### 3.31 Gray-Box Labor Partition

Fires: Plan=high, Implement=high, Verify=high
Deep modules are built under a default labor partition: **human owns the interface and boundary tests; agent owns the internals; source stays visible** (gray, not black — the human may step in but does not have to). Partition applies by default to AFK-eligible work (Gov5a); HITL work requires the agent to **ask** which partition variant to use — silent assumption is forbidden. QA consequence: human reads the seam (interface + boundary tests + AC), not internals line-by-line; `rev` of internals is unchanged. See [gr/gr_mod.md](gr/gr_mod.md) (M3a) and [gr/gr_qa.md](gr/gr_qa.md) (Q10).

### 3.32 Distill the Brief into 3–6 Goals (Idea Phase)

Fires: Plan=high, Implement=none, Verify=none
Before `aln` grilling begins, the agent distills the incoming brief / backlog item / stakeholder ask into **3–6 major goals** (phase `ide`). No details (no module map, no APIs, no UX specifics, no acceptance criteria). Negative goals welcome. HITL only — agent proposes, human edits. Output anchors `aln` but does not replace it. Persisted to `<artifacts>/<WI>/idea.md` with companion `<artifacts>/<WI>/status_idea.md` (`status: open|wip|done`) so downstream phases can read the anchor; retired with the rest of `<artifacts>/<WI>/` at WI close (3.33). Collapsible (3.29) when the upstream brief already names goals explicitly. See [gr/gr_idea.md](gr/gr_idea.md).

### 3.33 Retire Idea Artifacts

Fires: Plan=high, Implement=low, Verify=low
Idea goal files (`<artifacts>/<WI>/idea.md`) and their companion `<artifacts>/<WI>/status_idea.md` are WI-scoped anchor artifacts, not durable documentation. They must be **deleted** when the work-item closes — stale idea files actively mislead future agent runs because they look authoritative but reflect yesterday's understanding of the work. Distinct from 3.24 (PRDs move to external trackers) and parallel to 3.27 (research files retire on owner-issue close): idea files live in `<artifacts>/<WI>/` for the WI lifecycle, then are removed outright with the rest of `<artifacts>/<WI>/`. Enforcement: every `<artifacts>/<WI>/idea.md` is paired with `<artifacts>/<WI>/status_idea.md`; the same PR that closes the WI deletes `<artifacts>/<WI>/`, verified by Q11 in `qa`. Human-only `done` on `status_idea.md` — never auto-flip. See [gr/gr_idea.md](gr/gr_idea.md).

### 3.34 Capture Non-Obvious Decisions as ADRs

Fires: Plan=high, Implement=low, Verify=medium
Decisions that are (a) **hard to reverse**, (b) **surprising without context**, and (c) the result of a **real tradeoff** with downstream consequences are captured as Architectural Decision Records at `docs/adr/NNNN-<slug>.md`. Distinct from Aln15 negative decisions (rejected options live in the alignment transcript) and from PRDs (PRDs state *what*, ADRs explain *why* for sub-decisions). ADRs are durable, in-tree, and superseded — never silently deleted — when reversed. ADRs may be drafted during `aln` (per Aln17 in-session), surfaced during `rev` (when review finds a surprising choice with no rationale), or produced by `ica`. Routing (§5) must surface relevant ADRs when their topic matches the task; the implementer pulls them on demand (3.17). See [gr/gr_adr.md](gr/gr_adr.md).

### 3.36 Retire Alignment Transcripts

Fires: Plan=high, Implement=low, Verify=low
Alignment transcripts (`<artifacts>/<WI>/algn_transcript.md`) and their companion `<artifacts>/<WI>/status_algn_transcript.md` are WI-scoped session artifacts, not durable documentation. They must be **deleted** when the work-item closes — stale transcripts actively mislead future agent runs because they reflect yesterday's understanding of the work. Distinct from 3.24 (PRDs move to external trackers) and parallel to 3.33 (idea files retire on WI close) and 3.27 (research retires on owner-issue close): the transcript is the *source* artifact, the PRD composed by A2 is its *destination summary*. Enforcement: every `<artifacts>/<WI>/algn_transcript.md` is paired with `<artifacts>/<WI>/status_algn_transcript.md`; the same PR that closes the WI deletes `<artifacts>/<WI>/`, verified by Q11 in `qa`. Human-only `done` on `status_algn_transcript.md` — never auto-flip. See [gr/gr_algn.md](gr/gr_algn.md) Aln18.

### 3.37 Tripwire Discovery Forces Halt and Mode Re-Triage

Fires: Plan=high, Implement=high, Verify=medium
When the agent discovers a tripwire surface (3.29 list — public API, schema, auth, security, safety-critical, concurrency, broad architecture) mid-task after a non-`full` mode was selected in `ide`, the agent **halts, does not edit**, and surfaces the discovery on the GH issue body. The human picks: (i) approve narrow edit with explicit reasoning recorded on the issue, or (ii) re-enter `ide` for mode re-triage per Idea11. Either path is logged on the issue body — silent expansion of scope under a too-small mode is forbidden. Specialization of 3.7 (stop on high-risk decisions) for the scope-mode dimension. See [gr/gr_idea.md](gr/gr_idea.md) Idea11 and [gr/gr_governance.md](gr/gr_governance.md).

### 3.35 Maintain `context.md` and CLAUDE.md Pointer

Fires: Plan=high, Implement=medium, Verify=low
Each bounded context has a `context.md` at its root that defines the project's ubiquitous-language terms; a monorepo with multiple contexts forms a context map of many `context.md` files. The local `CLAUDE.md` (or equivalent agent-instruction file) carries an explicit pointer to the domain docs so agents — notably A1 `align-concept` per Aln17 — find them reliably. `context.md` is **read at session start, updated in-session under HITL accept** (Aln17), and durable (not retired like PRDs per 3.24 or research per 3.27). See [gr/gr_domain_language.md](gr/gr_domain_language.md) L8 and L9.

---

## 4. Guardrail Categories (Routing Index)

For each category: purpose, apply-when triggers, and detail document. Detailed rules live in the linked `gr/gr_*.md` files.

### 4.1 Architecture

Purpose: protect structural boundaries, dependency direction, and component ownership.
Apply when: module boundaries, layering, dependencies, public APIs, service boundaries, shared libraries, anti-corruption layers, or infrastructure/domain separation are involved.
Detail: [gr/gr_architecture.md](gr/gr_architecture.md)

### 4.2 Domain and Ubiquitous Language

Purpose: protect meaning. Keep names, terms, and concepts consistent with the domain.
Apply when: business terms, domain concepts, naming of domain objects, terminology changes, cross-team language, or user-facing concepts are involved.
Detail: [gr/gr_domain_language.md](gr/gr_domain_language.md)

### 4.3 Domain-Driven Design (Tactical)

Purpose: protect the integrity of domain models, aggregates, and invariants.
Apply when: bounded contexts, aggregates, entities, value objects, domain services, application services, domain events, or invariants are involved.
Detail: [gr/gr_ddd.md](gr/gr_ddd.md)

### 4.4 Coding Style and Conventions

Purpose: protect readability, consistency, and predictable behavior at the code level.
Apply when: any implementation task that produces or modifies code.
Detail: [gr/gr_coding_style.md](gr/gr_coding_style.md)

### 4.5 Testing and Verification

Purpose: define proof that a change is correct and safe.
Apply when: behavior change, bug fix, refactoring, legacy code change, public API change, or regression risk.
Detail: [gr/gr_testing_verification.md](gr/gr_testing_verification.md)

### 4.6 Security and Compliance

Purpose: protect against vulnerabilities, leaks, and regulatory violations.
Apply when: authentication, authorization, secrets, input validation, external interfaces, cryptography, logging of sensitive data, or compliance requirements are involved.
Detail: [gr/gr_security_compliance.md](gr/gr_security_compliance.md)

### 4.7 Brownfield Change Rules

Purpose: preserve invisible intent in existing systems.
Apply when: existing production code, legacy logic, or established behavior is touched.
Detail: [gr/gr_brownfield.md](gr/gr_brownfield.md)

### 4.8 Greenfield Design Rules

Purpose: prevent premature architecture in new code.
Apply when: a new project, service, module, or major component is created.
Detail: [gr/gr_greenfield.md](gr/gr_greenfield.md)

### 4.9 Documentation

Purpose: keep documentation concise, durable, and aligned with the code.
Apply when: documentation, comments, READMEs, or API docs are created or changed.
Detail: [gr/gr_documentation.md](gr/gr_documentation.md)

### 4.10 Governance and Authority

Purpose: define when the AI may act autonomously and when it must stop.
Apply when: any task — but especially when scope, approval, off-limits areas, or autonomy level is unclear.
Detail: [gr/gr_governance.md](gr/gr_governance.md)

### 4.11 Dependencies and Licensing

Purpose: control third-party code surface, versions, and license compatibility.
Apply when: adding, removing, or upgrading any third-party package or external service.
Detail: [gr/gr_dependencies.md](gr/gr_dependencies.md)

### 4.12 Operational and Agent Execution

Purpose: define what the agent must do during execution and what evidence it must produce.
Apply when: any implementation task — covers build/test commands to run, definition of done, and final-response format.
Detail: [gr/gr_operational.md](gr/gr_operational.md)

### 4.13 Module Depth

Purpose: protect codebase shape against shallow-module drift. Prefer deep modules with small interfaces hiding significant functionality.
Apply when: a module is created, split, merged, or restructured; a PRD proposes a module map; review surfaces tangled cross-dependencies; architecture-improvement (`ica`) is run.
Detail: [gr/gr_mod.md](gr/gr_mod.md)

### 4.14 Review

Purpose: define how a code-review pass is conducted in the smart zone, with standards pushed into context and module depth checked explicitly.
Apply when: a change is ready for review (`rev` phase); after an AFK loop produces commits; when a human asks the agent to review a diff or branch.
Detail: [gr/gr_rev.md](gr/gr_rev.md)

### 4.15 Alignment

Purpose: reach a shared design concept with the human before any planning artifact is written. Grilling produces alignment; PRD only summarizes it.
Apply when: a new feature, change, or vague backlog item enters the workflow (`aln` phase); before any PRD, issue decomposition, or implementation begins.
Detail: [gr/gr_algn.md](gr/gr_algn.md)

### 4.16 Test-Driven Development

Purpose: enforce the Red-Green-Refactor loop, false-green verification, and mock discipline that keep an autonomous implementation loop honest.
Apply when: any task in `ral` / `par` that produces or modifies executable logic; reviews (`rev`) that must verify the loop was followed; bug fixes (failing reproduction test first); legacy refactors (characterization tests first).
Detail: [gr/gr_tdd.md](gr/gr_tdd.md)

### 4.17 Research

Purpose: cache hard-to-recover external knowledge into a sprint-scoped artifact so downstream agent runs don't re-explore from a fresh context window — and retire the artifact before it rots.
Apply when: phase `res` is entered; `aln` grilling surfaces an external-dependency unknown (third-party API, uncommon SDK, unfamiliar codebase region) the agent must answer with facts; review (`rev`) of work that consumed a `research.md`.
Detail: [gr/gr_res.md](gr/gr_res.md)

### 4.19 Idea

Purpose: entry phase. Triages incoming work into one of three modes (`direct-edit` / `mini` / `full`) via the 4-axis matrix (Idea8); for `mini`/`full` modes also distills the brief into 3–6 major goals anchoring `aln` grilling; emits the GH issue and bootstraps `<artifacts>/<N>_<slug>/` for `mini`/`full` (Idea9).
Apply when: **every** task entering the workflow — `ide` always runs. Triggered by a brief, Slack note, ticket, vague backlog item, or any direct ask; before any downstream phase begins.
Detail: [gr/gr_idea.md](gr/gr_idea.md) (Idea1–Idea11)

### 4.18 Prototype

Purpose: resolve hard-to-reverse design decisions by building 2–3 throwaway variants and letting the human pick, instead of pretending grilling can settle every ambiguity.
Apply when: phase `pro` is entered; `aln` grilling stalls on a decision and the agent considers whether the Pro1 trigger (irreversibility OR cost asymmetry) holds; `res` surfaces a question only a build-to-learn spike can answer; review (`rev`) of work that consumed a prototype (verify sandbox deleted, human picked, no fabricated integration responses).
Detail: [gr/gr_proto.md](gr/gr_proto.md)

### 4.20 Architectural Decision Records (ADRs)

Purpose: capture the *why* of non-obvious, hard-to-reverse, tradeoff-heavy decisions so future agents and humans don't relitigate them.
Apply when: a decision that meets the Adr1 threshold (hard-to-reverse AND surprising AND real tradeoff) is made during `aln`, `prd`, `rev`, or `ica`; reviewing a diff whose rationale isn't obvious from code, `context.md`, or the PRD; touching code an existing ADR governs (implementer pulls the ADR per 3.17).
Detail: [gr/gr_adr.md](gr/gr_adr.md)

---

## 5. Routing Rule

Before detailed planning or implementation, the agent identifies which categories apply. Routing is a deliberation gate, not a checkbox — exclusion must be visible, because that is where misses hide.

**Required format:**

```
Relevant guardrails:
- Core rules
- Testing and Verification, because the task changes behavior
- Brownfield, because existing production code is affected

Considered but excluded:
- DDD: no domain model touched.
- Security and Compliance: no auth, secrets, input, or PII involved.
```

Rules:

- **Include + justify exclusion.** Listed categories carry a one-line reason. Categories considered and excluded are listed when their `Apply when` triggers are plausibly nearby; categories with no plausible trigger need not be mentioned.
- **Tie-breaker: include rather than exclude** when uncertain.
- **Re-route on discovery.** If mid-task a category surfaces (e.g. a touched file imports a crypto library, a renamed symbol turns out to be a domain term), the agent stops, re-declares routing, then continues.
- **Smallest reasonable set, not smallest possible set.** The agent does not load every detail document by default, but does not minimize for context-cost at the expense of safety.

**Core rules apply regardless of routing.** A misclassified task must not silently lose the core-rule floor.

---

## 6. Conflict Resolution

When guardrails conflict, use the **Priority Order Ladder** below:

1. Safety, security, and compliance
2. Correctness and behavior preservation
3. Architecture and domain integrity
4. Testability and maintainability
5. Consistency with coding style
6. Convenience or implementation speed

Speed is never a valid reason to bypass a higher-banded guardrail.

### 6.1 Process Rules and the Priority Order Ladder

The Priority Order Ladder ranks **quality dimensions of the resulting code/change**. Many guardrails are **process or governance rules** instead — they describe *how the agent operates*, not *what the resulting code looks like*. Examples: 3.1 Minimize Scope, 3.4 Make Assumptions Visible, 3.7 Stop on High-Risk Decisions, 3.15 Read Before Write, 3.16 Disagree Visibly, and the `Gov*` family. These rules do not sit in a band of the ladder.

Resolution when a process rule meets a quality rule:

- **Quality wins over process.** A process rule (e.g. minimize scope) cannot override a higher-banded quality rule (e.g. behavior preservation). The B3 ↔ Gov1 case is the canonical pattern: characterization tests required for safe refactor are scope expansion the process rule must accept.
- **Two process rules conflict?** The **more specific rule** governs. If the situation is high-risk, Gov3 (stop and ask) takes precedence over any other process rule.
- **Process rules shape *how* a band is honored, not *which* band wins.** They tell the agent how to operate inside the chosen quality priority — they do not compete with it.

---

## 7. Anti-Patterns

The agent should avoid:

- Loading every detail document when only a subset is relevant.
- Skipping core rules because routing did not select the matching category.
- Treating guardrails as optional suggestions.
- Hiding assumptions or uncertainty.
- Turning a small change into a broad redesign.
- Changing behavior as a side effect of cleanup.
- Introducing new abstractions without current need.
- Inventing rules when a detail document is empty — instead, mark the gap and ask.

---

## 8. Starter Examples

### Example 1: Bug Fix in Existing Code

Relevant: Core rules, Brownfield, Testing and Verification, Coding Style, Operational.
Reason: behavior-affecting change with regression risk.

### Example 2: New Module in a Greenfield Project

Relevant: Core rules, Greenfield, Architecture, Coding Style, Testing and Verification, Operational.
Reason: new structure with risk of premature abstraction.

### Example 3: Rename a Business Concept

Relevant: Core rules, Domain Language, DDD (if domain model), Brownfield (if existing code), Testing and Verification, Documentation.
Reason: language change may ripple through code, API, docs, tests.

### Example 4: Authentication Change

Relevant: Core rules, Security and Compliance, Testing and Verification, Architecture (if boundaries change), Governance (likely human approval), Operational.
Reason: security-sensitive, high-risk decision.

### Example 5: Upgrade a Third-Party Library

Relevant: Core rules, Dependencies, Testing and Verification, Security and Compliance, Governance, Brownfield.
Reason: external surface change with potential behavior, license, and security impact.

### Example 6: Start a Completely New Greenfield Project

Relevant: Core rules, Greenfield, Architecture, Domain Language, DDD (domain-modeling mindset only — defer tactical patterns until complexity warrants per G5/G6), Coding Style, Testing and Verification, Security and Compliance, Documentation, Dependencies, Governance, Operational.
Reason: a new project sets the long-term shape of the system. Initial decisions — architecture size, conventions, ubiquitous language, test strategy, dependency policy, repo structure — are durable and expensive to change later. The agent must resist premature architecture, record the initial ubiquitous language as it emerges, establish conventions deliberately, and produce only the smallest first vertical slice instead of a full scaffold.
Note on Security and Compliance: included from day 1. Even a CRUD prototype touches secrets (S1), input validation (S2), and dependency security (Dep5, Dep6). Retrofitting security habits is expensive; starting right is cheap.
Note on DDD: the domain-modeling mindset (model around business concepts, avoid anemic data classes, name from the domain) applies from day 1 — much of it already enforced by Domain Language (§3.13, L*) and G7. The tactical patterns (aggregates, value objects with invariants, bounded contexts, anti-corruption layers) are deferred until the domain shows enough complexity to justify them; introducing them early violates G5 (no premature abstraction) and G6 (no premature framework).
Note: Brownfield rules do not apply yet.

---

## 9. Maintenance: Editing Parallel-Stated Rules

Several core rules in §3 are also stated in a `gr/gr_*.md` detail document. Both copies exist by design — §3 keeps the rule cheap to load; the detail doc carries nuance. This creates drift risk: a rule edited in one place but not the other will diverge over time.

**Rule.** When editing any rule that appears in both §3 and a detail doc, check the parallel copy in the same change and align prose. The same applies in reverse when editing a detail-doc rule that has a §3 mirror.

**Parallels.** Each entry maps a §3 rule to its detail-doc counterpart(s):

| §3 rule                                        | Detail-doc rule(s) |
| ---------------------------------------------- | ------------------ |
| 3.1 Minimize Scope                             | Gov1               |
| 3.2 Do Not Mix Concerns                        | C10, B2            |
| 3.3 Respect Existing Behavior                  | B1                 |
| 3.4 Make Assumptions Visible                   | Gov2               |
| 3.5 Avoid Speculative Design                   | C8, A10, G5        |
| 3.6 Verify Changes                             | T1                 |
| 3.7 Stop on High-Risk Decisions                | Gov3               |
| 3.8 No Hardcoded Secrets                       | S1                 |
| 3.9 No Bypass of Existing Abstraction          | A3                 |
| 3.10 Preserve Public API Compatibility         | A6                 |
| 3.11 No Silent Dependency Changes              | Dep1               |
| 3.12 Provide Verification Evidence             | Op4                |
| 3.13 Use Domain Language Consistently          | L1                 |
| 3.14 No Fabrication                            | Op13               |
| 3.15 Read Before Write                         | Op14               |
| 3.16 Disagree Visibly                          | Gov12              |
| 3.17 Push for Reviewer, Pull for Implementer   | Op14b, Rev2        |
| 3.18 Review Runs in a Fresh Context            | Rev1               |
| 3.19 Prefer Deep Modules                       | M1, A11            |
| 3.20 Declare Autonomy: HITL vs AFK             | Gov5a              |
| 3.21 Reach Alignment Before Planning Artifacts | Aln1–Aln6          |
| 3.22 Strict Test-Driven Development (TDD)      | TDD1, TDD2, TDD11  |
| 3.23 Enforce Vertical Slices                   | Gov1a              |
| 3.24 Prevent Documentation Rot                 | Doc11, Q11         |
| 3.25 Clear Context Over Compaction             | Op15               |
| 3.26 Plan via Dependency Graphs (DAGs)         | Gov1b              |
| 3.27 Retire Research Artifacts                 | Res1, Res3, Res4, Q11 |
| 3.28 Prototype Hard-to-Reverse Decisions       | Pro1, Pro3, Pro4   |
| 3.29 Right-Size the Workflow (Mode Selection)  | Gov5b, Idea8       |
| 3.30 Converge the QA Loop on Human Verdict     | Q9                 |
| 3.31 Gray-Box Labor Partition                  | M3a, Q10           |
| 3.32 Distill the Brief into 3–6 Goals          | Idea1–Idea7        |
| 3.37 Tripwire Discovery Forces Halt + Re-Triage | Idea11             |
| 3.33 Retire Idea Artifacts                     | Idea7, Q11         |
| 3.34 Capture Non-Obvious Decisions as ADRs     | Adr1–Adr10, Aln17  |
| 3.35 Maintain `context.md` and CLAUDE.md Pointer | L8, L9, Aln17    |
| 3.36 Retire Alignment Transcripts              | Aln18, Q11         |

**Convention.** §3 entries stay short (headline + one-line rule). Longer prose, nuance, and anti-patterns live in the detail doc. Drift surface is then limited to the headline and one-liner.

**When adding a new core rule.** Place the substance in the relevant detail doc first, then add the short mirror in §3 and a new row in the table above.

**When removing or renumbering.** Update both copies and the table in the same change.
