# Guardrail: Alignment

Purpose: define how the agent reaches shared understanding with the human **before any planning artifact is written**. The goal of alignment is a shared **design concept** (Frederick P. Brooks) — not a document. The PRD that follows is a summary; the alignment itself is the asset.

Scope: applies to the `aln` phase (see [phases.md](../phases.md)).

Origin: Pocock — "misalignment is the main issue when working with AI." Grilling produces alignment; PRD only summarizes it. Plan mode tends to produce plans too eagerly, before alignment exists.

---

## Apply When

- A new feature, change, or initiative is being scoped.
- A vague backlog item is being prepared for implementation.
- A bug report is ambiguous about expected behavior.
- A stakeholder request lacks concrete acceptance criteria.
- Before any PRD, issue decomposition, or implementation begins.

---

## Rules

### Aln1. Alignment Is Strictly Human-in-the-Loop

The `aln` phase is never AFK. The human must be present and engaged. Ralph loops, parallel agents, and unattended runs are forbidden during alignment. This is the hard floor on alignment autonomy (cross-reference: gr_governance.md Gov5, autonomy tiers).

### Aln2. One Question at a Time

The grilling agent asks one question per turn. Multi-question batches force the human to context-switch and produce shallow answers. The discipline is patience: each branch of the design tree is walked, not jumped over.

### Aln3. Walk Every Branch of the Design Tree

Grilling is exhaustive over decisions, not over topics. Every branch with a real decision must be walked. Branches that look obvious are still explicitly checked because "obvious" is where misalignment hides.

### Aln4. Recommend an Answer per Question

For every question, the agent offers a recommended answer with reasoning. This is not optional. A question without a recommendation is a quiz; a question with a recommendation is a design conversation. The human accepts, modifies, or rejects.

### Aln5. Resolve Dependencies One by One

When question B depends on question A, A is resolved before B is asked. The agent does not ask speculative questions whose framing assumes an unresolved earlier decision.

### Aln6. Hidden-Constraint Checklist

Before grilling closes, the agent explicitly raises constraints commonly missed by stakeholders. For each, the human must answer "covered" or "not applicable":

- **Security** — auth, secrets, input validation, PII handling.
- **Permissions / authorization** — who can do this, who cannot.
- **Data retention** — how long, where, deletion rules.
- **Migrations** — schema or data changes needed.
- **Observability** — logs, metrics, traces required for this feature.
- **Public API compatibility** — does this break a contract.
- **Concurrency** — multiple agents, users, or processes touching the same state.
- **Out-of-scope** — what is deliberately not in this iteration.

Silent omission of a class is forbidden.

### Aln7. Subagent for Codebase Exploration

When the grilling needs facts about the existing codebase, the agent uses a subagent with an isolated context that explores and reports a summary back. The grilling agent's main context is not polluted with raw exploration output. This keeps the alignment conversation in the smart zone.

### Aln8. Treat Stakeholder Brief as Input, Not Truth

The original brief (Slack message, ticket, email) is the prompt for alignment — not the alignment itself. The agent does not implement directly from a brief. Grilling is mandatory before any planning artifact is written.

### Aln9. Length of Grilling Is Open-Ended

A grilling session may run dozens or even ~100 questions. The agent does not shortcut the session to "be helpful." The transcript is the asset. If the human signals fatigue, the agent offers to pause and resume, not to skip remaining branches.

### Aln10. Pair with the Right Human

The agent flags which kind of human is needed for which question type:

- Domain / product questions → domain expert (with or without developer).
- Implementation / technical questions → developer (with or without peer).
- Cross-cutting → both.

When the wrong human is in the loop, the agent says so rather than pushing through.

### Aln11. Domain Transcripts May Be Fed In

When a domain-expert meeting transcript or written source-of-truth exists, the agent may feed it into the grilling session to validate or generate questions against it. This is an input to grilling, not a replacement.

### Aln12. Module Map Is an Alignment Output

By the end of alignment, the agent and human agree on a proposed **module map** (cross-reference: gr_modules.md M6): which modules will be touched, which are new, what each new module's public interface looks like. Module-shape decisions belong here, not in implementation. The proposed map must be explicitly reviewed for depth (ensuring narrow interfaces) during the alignment/PRD review phase before implementation begins.

### Aln13. PRD Summarizes Alignment, Does Not Replace It

The PRD that follows alignment is a destination document — a summary. It is not the source of truth for the design concept. Skipping deep PRD review is acceptable only when the grilling session is genuinely complete; this is a judgment call, not a default (cross-reference: open question in workflow doc on PRD review safety).

### Aln14. Stop and Re-Align on Discovery

If during PRD writing, issue decomposition, or implementation, a contradiction or missed branch surfaces, the agent stops and routes back to `aln`. Alignment debt is paid at discovery time, not at QA time.

### Aln15. Negative Decisions Are Captured

Decisions to *not* do something are recorded explicitly in the alignment artifacts and carried forward into the PRD's out-of-scope section. Negative decisions are how scope is defended later.

### Aln16. Visualize the Decision Tree

During the grilling session, the agent maintains and displays a visual map of the decision tree (e.g., a Mermaid `graph TD`). The graph shows the root goal, walked branches (decisions made), and pending branches (unresolved questions). This keeps the human oriented and exposes missed constraints.

### Aln17. Throwaway Front-End Prototypes for Visual Ambiguity

When alignment hits a visual or UX decision that cannot be resolved in words (layout, interaction shape, information density), the agent proposes generating 2–3 disposable front-end prototypes as alignment input. The **decision to prototype is made during `aln`**, not deferred to implementation.

Procedure, inputs, outputs, and failure modes are defined in [`wf/wf_fe_prototype.md`](../wf/wf_fe_prototype.md). Key bindings to alignment:

- Prototype output feeds back into grilling — chosen direction becomes a normal alignment outcome (Aln12 module map; Aln15 negative decisions for rejected variants).
- Prototype code is throwaway. Deletion before production impl is mandatory.
- Human / domain expert drives variant selection — agent does not self-judge mature FE quality.

Applies only when the ambiguity is genuinely visual. Backend, data, or contract decisions are resolved by grilling, not by prototypes.

---

## Anti-Patterns

- Jumping into plan mode before grilling is complete.
- Asking three questions in one turn to "save time."
- Implementing directly from a Slack brief.
- A grilling session that ends after five questions because the agent "thinks it has enough."
- Asking questions without offering a recommendation.
- Losing track of pending decisions because no visual tree is maintained.
- A PRD that contradicts the grilling transcript.
- Silently dropping hidden-constraint classes (security, retention, observability) because the brief did not mention them.
- Running grilling AFK or via Ralph loop.
- Treating the PRD as the design concept rather than its summary.
- Discovering a module-shape decision during implementation and silently making it.

---

## Notes on Interaction with Other Guardrails

- Aln1 specializes gr_governance.md Gov5 — `aln` is the canonical HITL phase.
- Aln6 feeds gr_review.md Rev7 — what was checked during grilling becomes the review checklist.
- Aln12 feeds gr_modules.md M6 — module map is owned by alignment.
- Aln13 pairs with Core rule 3.4 (make assumptions visible) — alignment is where assumptions are surfaced and resolved.
- Aln14 specializes Core rule 3.7 (stop on high-risk decisions) for the planning side.
