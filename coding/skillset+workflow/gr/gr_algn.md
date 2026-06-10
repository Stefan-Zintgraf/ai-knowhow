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
Skills: align-concept

The `aln` phase is never AFK. The human must be present and engaged. Ralph loops, parallel agents, and unattended runs are forbidden during alignment. This is the hard floor on alignment autonomy (cross-reference: gr_governance.md Gov5, autonomy tiers).

### Aln2. One Question at a Time
Skills: align-concept

The grilling agent asks one question per turn. Multi-question batches force the human to context-switch and produce shallow answers. The discipline is patience: each branch of the design tree is walked, not jumped over.

### Aln3. Walk Every Branch of the Design Tree
Skills: align-concept

Grilling is exhaustive over decisions, not over topics. Every branch with a real decision must be walked. Branches that look obvious are still explicitly checked because "obvious" is where misalignment hides.

### Aln4. Recommend an Answer per Question
Skills: align-concept

For every question, the agent offers a recommended answer with reasoning. This is not optional. A question without a recommendation is a quiz; a question with a recommendation is a design conversation. The human accepts, modifies, or rejects.

### Aln5. Resolve Dependencies One by One
Skills: align-concept

When question B depends on question A, A is resolved before B is asked. The agent does not ask speculative questions whose framing assumes an unresolved earlier decision.

### Aln6. Hidden-Constraint Checklist
Skills: align-concept, hidden-constraint-checklist

Before grilling closes, the agent explicitly raises constraints commonly missed by stakeholders. The sweep fires **always at close**, regardless of whether the topic plausibly engaged a class — the checklist's value is defeating agent judgment about which classes apply. For each class, the human must answer one of three outcomes:

- `covered` — addressed in grilling, with a pointer to the relevant transcript entry or `context.md` term.
- `not-applicable` — explicitly declared inapplicable, with a human-spoken reason recorded in the transcript.
- `missing` — gap identified; **blocks alignment close**. The branch must either be grilled now, or the class downgraded to `not-applicable` with reason. No silent passes, no "documented gap" closes that defer to `rev`.

Classes:

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
Skills: align-concept, subagent-for-exploration

When the grilling needs facts about the existing codebase, the agent uses a subagent with an isolated context that explores and reports a summary back. The grilling agent's main context is not polluted with raw exploration output. This keeps the alignment conversation in the smart zone.

**Dispatch pattern is hybrid: proactive narrow + reactive on demand.**

1. **Proactive narrow brief, at session start.** Before the first grilling question, dispatch one B10 sub-agent with a fixed, shallow brief: list modules touched (per `idea.md` goals), list test files for those modules, list `context.md` term occurrences in them. No deep reads. Returned summary grounds the opening question. **Skip the proactive dispatch when `idea.md` already names modules and tests explicitly** (the orientation work is already done).
2. **Reactive on demand, during grilling.** When a specific question requires a codebase fact the agent does not have, dispatch a focused B10 with a specific brief (e.g. "does this caller handle nulls?"), await, resume.

Speculative deep-scans at start are forbidden — the proactive brief is narrow on purpose. Threads grilling will pull are not yet known; over-fetching defeats context minimization.

### Aln8. Treat Stakeholder Brief as Input, Not Truth
Skills: align-concept

The original brief (Slack message, ticket, email) is the prompt for alignment — not the alignment itself. The agent does not implement directly from a brief. Grilling is mandatory before any planning artifact is written. The brief is normally distilled into 3–6 major goals during the upstream `ide` phase (cross-reference: gr_idea.md Idea1) — `aln` grills against those goals, not against the raw brief.

**Goal-anchor contract.** A1 consumes `<artifacts>/<WI>/idea.md` (C8) at session start with three obligations:

1. **Verbatim anchor.** A1 presents the 3–6 goals to the human verbatim before the first grilling question and asks for confirmation. Goals are the tree-roots; negative goals (gr_idea.md Idea3) become guardrails grilling will not cross.
2. **Per-branch goal-tag.** Every grilling branch opened during the session is tagged with the goal-id it serves, recorded in the alignment transcript (Aln18). Branches that map to no goal are a signal grilling has drifted — A1 surfaces this to the human, who either reframes the branch to a goal or downgrades it.
3. **Close-time coverage report.** At session close (before Aln6 sweep), A1 emits a coverage report: each goal-id → which branches covered it; uncovered goals are listed explicitly. Any uncovered goal blocks close until the human accepts a "skip, with reason" downgrade.

### Aln9. Length of Grilling Is Open-Ended
Skills: align-concept

A grilling session may run dozens or even ~100 questions. The agent does not shortcut the session to "be helpful." The transcript is the asset. If the human signals fatigue, the agent offers to pause and resume, not to skip remaining branches.

### Aln10. Pair with the Right Human
Skills: align-concept

The agent flags which kind of human is needed for which question type:

- Domain / product questions → domain expert (with or without developer).
- Implementation / technical questions → developer (with or without peer).
- Cross-cutting → both.

When the wrong human is in the loop, the agent says so rather than pushing through.

### Aln11. Domain Transcripts May Be Fed In
Skills: align-concept

When a domain-expert meeting transcript or written source-of-truth exists, the agent may feed it into the grilling session to validate or generate questions against it. This is an input to grilling, not a replacement.

### Aln12. Module Map Is an Alignment Output
Skills: align-concept

By the end of alignment, the agent and human agree on a proposed **module map** (cross-reference: gr_mod.md M6): which modules will be touched, which are new, what each new module's public interface looks like. Module-shape decisions belong here, not in implementation. The proposed map must be explicitly reviewed for depth (ensuring narrow interfaces) during the alignment/PRD review phase before implementation begins.

### Aln13. PRD Summarizes Alignment, Does Not Replace It
Skills: align-concept, compose-prd

The PRD that follows alignment is a destination document — a summary. It is not the source of truth for the design concept. Skipping deep PRD review is acceptable only when the grilling session is genuinely complete; this is a judgment call, not a default (cross-reference: open question in workflow doc on PRD review safety).

### Aln14. Stop and Re-Align on Discovery
Skills: align-concept

If during PRD writing, issue decomposition, or implementation, a contradiction or missed branch surfaces, the agent stops and routes back to `aln`. Alignment debt is paid at discovery time, not at QA time.

### Aln15. Negative Decisions Are Captured
Skills: align-concept

Decisions to *not* do something are recorded explicitly in the alignment artifacts and carried forward into the PRD's out-of-scope section. Negative decisions are how scope is defended later.

**Sources of negative decisions:**

1. **In-session rejections** — answers the human gave during grilling that ruled an option out.
2. **Rejected prototype variants** — when `aln` invoked `pro` and the human picked a winner, the rejected variants (from C6 `decision_outcome.rejected` + `rationale_by_human`) become negative decisions here.

**Intake from `pro` (caller-persists per Pro5).** On `aln` resume after `pro` exit, the alignment agent (A1 `align-concept` when built):

1. Reads the C6 variant artifact ([`tpl/tpl_var_pres.md`](../tpl/tpl_var_pres.md)) at `<sandbox_path>/variants.md` **before sandbox deletion**. This must happen before Pro3 deletes the sandbox; A1 fails closed if C6 is unreadable or `decision_outcome.chosen` is null.
2. For each id in `decision_outcome.rejected`: appends an Aln15 entry citing the variant `summary`, the observable facts that made it lose, and `rationale_by_human` if present.
3. Updates Aln12 module map per the chosen variant's shape.
4. Signals to `pro` that capture is complete, which unblocks Pro3 sandbox deletion.

**Replay on later `aln` sessions.** Existing Aln15 entries are loaded as grilling context. A1 does not re-propose options already recorded as negative decisions — it cites the prior rejection (with rationale) if the human reopens the branch, rather than walking it fresh.

### Aln16. Visualize the Decision Tree
Skills: align-concept

During the grilling session, the agent maintains and displays a visual map of the decision tree (e.g., a Mermaid `graph TD`). The graph shows the root goal, walked branches (decisions made), and pending branches (unresolved questions). This keeps the human oriented and exposes missed constraints.

### Aln17. Grill With Docs — Maintain `context.md` and Draft ADRs In-Session
Skills: align-concept, subagent-for-artifact-drafting

Grilling is **document-anchored**, not purely conversational. The alignment agent reads and updates the durable domain docs during the session — Pocock's `/grill-with-docs` pattern.

**At session start.**

1. Locate `context.md` for the relevant bounded context (gr_domain_language.md L8) via the `CLAUDE.md` pointer (L9). If neither exists in a repo that should have them, flag the gap and offer to create `context.md` as the first session output.
2. Load every defined term into the grilling context as ground truth. Aln5 dependency ordering treats `context.md` definitions as resolved.
3. Load any existing ADRs under `docs/adr/` whose topics plausibly touch the grilling root goal (per gr_adr.md routing). Cite them when their decisions constrain the current question.

**During grilling.**

4. **Always challenge on near-match.** Before adding any new term to `context.md`, the agent checks for lexical *and* semantic neighbors (substring, plural, case-fold, common synonym set, domain-cluster overlap — e.g. "User" near "Customer", "Cancellation" near "Refund"). On any candidate match, halt and ask: "same as existing X, refinement of X, or genuinely new?" Silent additions are forbidden. The dangerous overlaps are semantic, not lexical — agent leverage is at the moment of first introduction (cross-reference: Core rule 3.13).
5. **Stream-write `context.md`, HITL accept per change.** New terms, refined definitions, new relationships, and new status values are written into `context.md` *as each one is agreed* — one diff per change, explicit HITL accept on each. No batching to session close. The update happens before the next branch is walked, so later questions see the new term.
6. **Detect ADR-worthy decisions; ask before drafting.** Apply the gr_adr.md Adr1 threshold (hard-to-reverse AND surprising AND real tradeoff) continuously. When a decision plausibly crosses it, halt grilling and ask the human "ADR-worthy?" — naming the three criteria. On `yes`, dispatch a **B11 sub-agent** for the draft (see Aln17 sub-agent dispatch below); on `no`, record as in-transcript Aln15 entry or plain `context.md` term update and resume. Silent self-judgment is forbidden (Core rule 3.16; Adr8 HITL accept).
7. **B11 sub-agent dispatch for ADR drafts.** Grilling does not draft ADRs in its own context — drafts go to a B11 sub-agent with a self-contained brief. **Brief contract:** decision statement; the three Adr1 facts (why hard-to-reverse, why surprising, what tradeoff); human's verbatim rationale (paraphrase forbidden — rationale-as-spoken is the artifact's value); relevant `context.md` neighborhood (only terms involved); any Aln15 rejected options already captured. **Synchronous wait:** grilling pauses until the draft returns; human accepts/edits inline; `proposed` ADR lands at `docs/adr/NNNN-<slug>.md`; status flips to `accepted` per Adr8 only with explicit human acceptance. Async drafting is forbidden (a draft hanging over later questions reintroduces the batching failure mode).
8. **Bounded-context discipline.** In a monorepo, identify which bounded context the question lives in before updating any `context.md` (gr_domain_language.md L7). Same word with different meaning across contexts is **not** unified.

**At session close.**

9. The alignment transcript (Aln18, `<artifacts>/<WI>/algn_transcript.md`) records: (a) which `context.md` entries were added or changed (with diffs or links), (b) which ADRs were drafted/accepted with their NNNN ids, (c) which existing ADRs constrained decisions in the session.
10. `context.md` diffs and new ADRs are committed alongside the alignment transcript, not as a separate later cleanup pass. Documentation rot starts the moment maintenance is deferred.

**Distinct from Aln15.** Aln15 captures rejected options (the road not taken). Aln17 maintains the chosen-language and chosen-rationale layers. A single decision can produce all three artifacts: an Aln15 negative-decision entry, a `context.md` term update, and an ADR.

**When to skip.** Aln17 does not apply when there is no codebase yet (per Pocock's rule of thumb: codebase → grill-with-docs, no codebase → plain grill). For a brand-new repo, the very first `aln` session bootstraps `context.md` as an output rather than reading it as input — even early-stage projects benefit because that is precisely when shared language is established. The bootstrap output also includes the `CLAUDE.md` pointer (L9).

### Aln18. Alignment Transcript Artifact (C4)
Skills: align-concept

Every `aln` session produces a paired artifact under `<artifacts>/<WI>/`, mirroring the C8 idea-file shape (gr_idea.md Idea7):

- `<artifacts>/<WI>/algn_transcript.md` — markdown body. Sections: chronological Q&A log (one question + recommendation + human answer per entry, tagged with goal-id per Aln8); resolved decisions block; Aln15 rejected options; B5/Aln6 hidden-constraint sweep result (per-class outcome); B10/Aln7 sub-agent returns referenced inline; Aln17 in-session `context.md` and ADR-draft references (with NNNN ids).
- `<artifacts>/<WI>/status_algn_transcript.md` — frontmatter only: `status: wip|done`, `updated`, `owner-issue`. `done` is human-only — never auto-flip.

**Lifecycle.** WI-scoped, not durable. The transcript is the *source* artifact; the PRD (composed by A2 per Aln13) is its *destination summary*. Retired with the rest of `<artifacts>/<WI>/` at WI close (Core rule 3.36, parallel to 3.33 idea retirement and 3.27 research retirement). Same PR that closes the WI deletes `<artifacts>/<WI>/`, verified by `qa` Q11.

**Consumers.** A2 (`compose-prd`) reads the transcript to summarize into the destination PRD; A6 (`review`) reads it to verify Rev7 hidden-constraint coverage and Adr10 ADR coverage; A8 / Q11 lint reads `status_algn_transcript.md` frontmatter.

**Distinct from `context.md` and ADRs.** `context.md` and ADRs are durable, in-tree, survive WI close. The transcript records *the session that produced them*; it retires with the WI.

### Aln19. Collapsed `aln` for `mini` Mode
Skills: align-concept

When `ide` selects `mini` mode (gr_idea.md Idea8), `aln` runs in a collapsed profile that preserves irreversibility-protection rules and reduces ceremony rules. The collapse is not a skip — it is a documented shorter shape. Silent skipping of any Aln rule outside this collapse is forbidden (3.16, Idea11).

**Kept (unchanged from full `aln`):**

- **Aln6 / B5 hidden-constraint sweep** — always at close, three outcomes (covered / not-applicable / missing), `missing` blocks close. Identical to full mode.
- **Aln17 `context.md` discipline** — stream-write one diff per change, near-match challenge (lexical + semantic) before any add, HITL accept per change. Identical to full mode.
- **Aln17 ADR gating** — if Adr1 threshold (hard-to-reverse AND surprising AND real tradeoff) hits, ask "ADR-worthy?" first, draft on yes via B11. Identical to full mode.
- **Aln14** stop-and-re-align on discovery.

**Reduced:**

- **Aln2–Aln5 grilling loop** — collapsed to **1–3 sharpest questions**, not exhaustive branch-walking. Each still one-question-per-turn, with a recommended answer (Aln4).
- **Aln7 / B10 sub-agent exploration** — **reactive on demand only**. Proactive narrow brief at session start is skipped (the smaller scope of `mini` doesn't justify it, and Idea10 already ran shallow exploration in `ide`).
- **Aln8 idea anchor** — single goal anchor (the mini-mode brief verbatim) rather than per-branch goal-tag.
- **Aln12 module map** — produced only if the change touches more than one file; single-file edits skip the map.
- **Aln15 negative decisions** — recorded only when an option was actively rejected during the 1–3 question loop; otherwise no entry.

**Skipped (with explicit substitute):**

- **Aln18 transcript artifact** — no separate `<artifacts>/<slug>/algn_transcript.md` file. The 1–3 questions, recommendations, answers, and Aln6 sweep result are written **inline in the GH issue body** under a `## Alignment` heading. The issue is the transcript for `mini` mode. `status_algn_transcript.md` is not created.

**Auto-upgrade triggers.** During collapsed `aln`, if any of the following surfaces, the agent stops and proposes upgrade to `full` mode per Idea11:

- Adr1 ADR-worthy decision (the ADR itself proceeds in either mode, but the surrounding scope is `full`-shaped).
- More than 3 unresolved questions after the first round.
- Pro1 prototype gate (irreversibility OR cost asymmetry — see gr_proto.md).
- Aln6 hidden-constraint sweep marks any class `missing` that requires deep grilling to resolve.

The human approves the upgrade per Idea11. If approved, the work already done in collapsed `aln` is preserved — the inline issue-body transcript is migrated into a freshly created `<artifacts>/<slug>/algn_transcript.md` (Aln18) and grilling resumes in full shape.

**Forbidden:**

- Skipping Aln6 sweep in `mini` mode. The sweep is the safety floor.
- Treating "collapsed" as license to skip Aln17 `context.md` updates or ADR gating — those are the irreversibility protections.
- Writing the inline issue-body transcript without a `## Alignment` heading (downstream consumers parse on it).
- Letting `mini` mode grilling expand past 3 questions without proposing an upgrade.

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
- Aln6 feeds gr_rev.md Rev7 — what was checked during grilling becomes the review checklist.
- Aln12 feeds gr_mod.md M6 — module map is owned by alignment.
- Aln13 pairs with Core rule 3.4 (make assumptions visible) — alignment is where assumptions are surfaced and resolved.
- Aln14 specializes Core rule 3.7 (stop on high-risk decisions) for the planning side.
- Aln8 receives the upstream output of `ide` (gr_idea.md Idea6): grilling targets the 3–6 goals, not the raw brief.
- Aln17 wires gr_domain_language.md (L8 `context.md`, L9 `CLAUDE.md` pointer) and gr_adr.md (3.34 / Adr1 threshold, Adr5 format, Adr8 HITL accept) into the grilling session. It is the project-side embodiment of Pocock's `/grill-with-docs`.
- Aln17 #7 wires B11 (subagent for artifact drafting) — ADR drafts are produced by a sub-agent, not in A1's grilling context. B11 is also consumed by A2 (PRD section expansion) and A6 (review-summary drafting).
- Aln18 parallels gr_idea.md Idea7 (paired body + status frontmatter, `owner-issue` provenance, WI-lifetime retirement). Retirement enforced by Core rule 3.36 + `qa` Q11.
