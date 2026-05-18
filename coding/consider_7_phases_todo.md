# Consider 7-Phases TODO

Purpose: self-contained brief for working through the remaining recommendations from the 7-phases gap analysis in **fresh sessions**. Each item below carries enough context that a new chat can pick it up without reading prior conversation history.

---

## Background

Source video doc: [the-7-phases-of-ai-driven-development.md](the-7-phases-of-ai-driven-development.md) — Matt Pocock's 7-phase pipeline (Idea → Research → Prototype → PRD → Implementation Plan → Execution → QA), with phases 5–7 forming an iterative loop.

A gap-and-contradiction analysis was performed between that doc and the local guardrail/workflow system. The local system is anchored in:

- [guardrails.md](guardrails.md) — core rules (§3) + routing index (§4) + parallel-table (§9).
- [phases.md](phases.md) — phase definitions + bucket mapping + sequence diagram.
- [todo.md](todo.md) — workflow operationalization (W1–W13) + open decisions (D1–D8).
- [gr/](gr/) — detail docs per category (one `gr_*.md` per category in §4).
- [wf/](wf/) — workflow detail docs (currently just `wf_fe_prototype.md`).

## Detected gaps & contradictions (full list)

From the analysis. Items marked **DONE** were addressed by adding the `res` phase (see below). Items marked **OPEN** are the work for this brief.

### Gaps (Pocock has, local missing)

1. **DONE** — Research phase / `research.md` cache. Added as phase `res`, core rule 3.27, routing §4.17, detail doc [gr/gr_research.md](gr/gr_research.md), todo entry W13.
2. **OPEN** — Prototype scope narrower locally. Aln17 + [wf/wf_fe_prototype.md](wf/wf_fe_prototype.md) = visual/UX only. Pocock = UI + **architecture + external-service shape**. Local rules silent on arch/integration prototyping.
3. *(Minor, deferred)* — Idea as named phase. Pocock makes it explicit. Local flow starts at `aln`. Probably intentional; not in scope here unless the fresh session disagrees.
4. **OPEN (new)** — Loop convergence criterion. Pocock open-question; local also silent. `qa` triages to fix-now/backlog but no "when does loop terminate" rule.
5. *(Already resolved locally)* — Code review placement gap acknowledged by Pocock; locally resolved via `rev` cross-phase. Stronger than Pocock. No action.

### Contradictions / tensions

1. **(Internal, not vs Pocock)** — PRD retention D3 in todo.md is marked "open" but guardrail 3.24 already mandates the answer. Inconsistency inside [todo.md](todo.md), not vs the 7-phases doc.
2. **OPEN** — Sequentiality of execution. Pocock: "most of the time sequential is sufficient; parallelization is bonus." Local 3.26 (DAG mandatory, "sequential multi-phase plans **forbidden**"). Local rule conflates *plan structure* (DAG) with *execution mode* (sequential vs parallel) — DAG-planned work can still execute sequentially. Needs a clarifying note.
3. **OPEN** — Scale-invariance. Pocock claims pipeline works bug→app. Local guardrails 3.1 (minimize scope) + governance imply lightweight path for small changes, but no explicit "when to skip phases for trivial work" rule.
4. *(Already stricter locally, intentional)* — AFK readiness. Pocock optimistic; local Gov5a + B4 + D4 demand sandbox + checklist. No action; documented difference.
5. *(Out of scope)* — Gray-box architecture (Pocock-referenced, undefined). Possible separate research task; flagged for the fresh session to decide.

## Workflow framing additions (Pocock has)

- **Loop semantics phases 5–7** — explicit in Pocock; local sequence diagram in [phases.md](phases.md) §4 shows it implicitly. Aligned but the loop-terminator gap above is the open piece.
- **Adversarial grilling as PRD mechanism** — local Aln1–Aln6 + planned grill-me skill cover this well. Aligned.
- **Ephemeral artifacts** — local covers PRDs (3.24) **and now research** (3.27). Aligned.

---

## Items to Work (Fresh Sessions)

Each item is independent. Pick any order. Each section is self-contained — point a fresh session at one section and it can act without other context.

---

### Item 2 — Broaden Prototype Scope Beyond FE — **DONE (2026-05-17)**

**Resolution:** prototype promoted from `aln`-technique (old Aln17) to first-class phase `pro`. Scope broadened from FE-only to three flavors: FE/UX, architecture, integration. Trigger gate moved from "genuinely visual" to **irreversibility OR cost asymmetry** (Pro1) — concrete, harder to game.

**Artifacts added/changed:**

- New: [gr/gr_prototype.md](gr/gr_prototype.md) — Pro1–Pro8 (trigger gate, 3 flavors, throwaway discipline, 2–3 variants + no self-judging, output feeds aln/res/prd, HITL only, hidden-constraint check, no fabrication in integration spikes).
- Renamed: `wf/wf_fe_prototype.md` → [wf/wf_prototype.md](wf/wf_prototype.md). Broadened to cover all three flavors.
- Added: phase `pro` in [phases.md](phases.md) (definition, bucket = Plan, sequence diagram updated with `aln → [res?] → [pro?] → prd`).
- Added: core rule 3.28 in [guardrails.md](guardrails.md); routing §4.18; parallel-table row (Pro1, Pro3, Pro4); phase-list header now includes `pro`.
- Deleted: Aln17 in [gr/gr_alignment.md](gr/gr_alignment.md).
- Added: Res10 cross-ref in [gr/gr_research.md](gr/gr_research.md) — `res` may invoke `pro` for build-to-learn facts.
- Updated: W11 in [todo.md](todo.md) marked superseded; W14 added with remaining open items (skill, retirement enforcement, variant template, `res`-pro fact-flow decision).

**Decisions resolved:**

- D8-bis (phase vs. technique) → **phase**. Pocock-aligned.
- One workflow doc vs. three → **one doc** covering all three flavors (Pro2 enforces one-flavor-per-invocation).
- Aln17 fate → **deleted** (single source: gr_prototype.md).
- Replacement gatekeeper for "genuinely visual" → **irreversibility OR cost asymmetry** (Pro1).

**Follow-ups (tracked in todo.md W14, not here):** prototype skill build; sandbox retirement enforcement mechanism (parallels W13 research-retirement open question); variant-presentation template; whether `pro` invoked from `res` writes facts directly into `research/<topic>.md` or returns them for `res` to persist.

---

### Item 2 (archived gap text)

**Gap (original):** Aln17 + `wf/wf_fe_prototype.md` restrict prototyping to visual/UX ambiguity. Pocock explicitly extends prototyping to **architecture choices** and **external-service shape testing** (the-7-phases-doc §"Prototype as Taste-Imposition Step" and §"Prototype Variant Generation").

**Why it matters:** Architectural prototyping (e.g., "should this be a queue or a sync call?") and integration spike prototyping (e.g., "how does Stripe's webhook actually fire?") have the same taste-imposition logic as UI prototyping but are currently invisible in the local rules. A team facing an arch decision has no sanctioned workflow to throw away two variants and pick one.

**Likely changes:**

- Rename `wf/wf_fe_prototype.md` → `wf/wf_prototype.md` (or keep FE doc and add `wf/wf_arch_prototype.md` + `wf/wf_integration_prototype.md`). Decide first.
- Update Aln17 in [gr/gr_alignment.md](gr/gr_alignment.md) to widen the trigger from "visual/UX ambiguity" to "ambiguity that resists resolution by discussion alone — visual, architectural, or integration-shape." Keep the throwaway 2–3 variants discipline.
- Verify [gr/gr_research.md](gr/gr_research.md) Res5 (facts vs. speculation) does not collide with arch prototyping — research captures facts; prototyping explores design. Two distinct tools; document the boundary.
- Update [todo.md](todo.md) — W11 entry is currently "done"; either reopen with the broadened scope or add W11.1 / W14.
- Possibly add a `pro` (prototype) phase if prototyping deserves first-class status, or keep it as a technique inside `aln`. Pocock treats it as a phase (phase 3, optional). Decision needed.

**Decision points for the fresh session:**

- D8-bis: prototype as phase (`pro`) vs. technique inside `aln`? Pocock = phase. Local Aln17 = technique. Widening scope may justify promotion.
- One workflow doc covering all three flavors, or three separate `wf_*_prototype.md` files?
- Does arch/integration prototyping need its own rule like Aln17, or is widening Aln17 sufficient?

**Risk:** Promoting prototype to a phase ripples through [phases.md](phases.md), bucket mapping, sequence diagram, and the `aln → res? → prd` chain. Touch with care.

---

### Item 3 — Clarify 3.26 (DAG ≠ Mandatory Parallel Execution) — **DONE (2026-05-17)**

**Resolution:** reworded 3.26 + Gov1b to separate **plan shape** (DAG, mandatory) from **execution mode** (sequential `ral` or parallel `par`, both allowed). Forbidden thing narrowed to "forced ordering not justified by a real blocking edge." Added anti-pattern in `gr_governance.md` against conflating the two. todo.md W3/W4/W5/W10 audited — no parallel-mandatory drift; A3's "Output: a DAG, not a sequential list" is plan-shape, correct as-is.

**Files changed:** [guardrails.md](guardrails.md) §3.26; [gr/gr_governance.md](gr/gr_governance.md) Gov1b + anti-patterns list.

---

### Item 3 (archived gap text)

**Tension:** [guardrails.md](guardrails.md) §3.26:

> When decomposing a PRD into tasks, the agent must create an issue DAG (Directed Acyclic Graph) with explicit blocking relationships. **Sequential multi-phase plans are forbidden because they serialize work.** Each issue must be independently grabbable.

vs. Pocock (the-7-phases-doc §"Phase 6 — Execution"):

> Most of the time sequential is sufficient; parallelization is available when tickets are non-blocking.

The local rule's "forbidden because they serialize work" reads as if **execution must be parallel**. Pocock's intent (and the local intent in [phases.md](phases.md), where `ral` is sequential single-agent and `par` is the parallel variant) is that **plan shape = DAG, execution mode = either**. Without clarification, future agents may read 3.26 as banning the `ral` phase.

**Likely changes:**

- Reword 3.26 headline + body to separate the two concepts. Suggested phrasing: "Plans are structured as a DAG of independently grabbable issues. Sequential **execution** (`ral`) over a DAG is allowed and often preferred; what is forbidden is **plans that bake in a forced ordering not justified by real blocking edges**."
- Verify parallel detail doc rule **Gov1b** in [gr/gr_governance.md](gr/gr_governance.md) matches the new phrasing.
- Cross-check todo.md entries (W3 Issue DAG, W4 Ralph Once Loop, W5 AFK Loop, W10 Parallel Agents) — none should read as if parallel execution is mandatory.

**Risk:** Low. This is a clarification, not a semantic change. The intent has always been "DAG plan, flexible execution."

---

### Item 4 — Close todo.md D3 (PRD Retention Decision) — **DONE (2026-05-17)**

**Resolution:** D3 in [todo.md](todo.md) reworded to "Resolved (2026-05-17)" pointing at guardrail 3.24 (PRDs external, closed when done) and noting 3.27 extends the same shape to research files. Enforcement gap (no hook/CI verifies retirement) deferred — already tracked here as Item 8 for research; PRD retirement enforcement folded into the same item rather than spawning a new one (same mechanism likely fits both).

**Files changed:** [todo.md](todo.md) §D D3 line.

---

### Item 4 (archived gap text)

**State:** [todo.md](todo.md) §D lists D3 as an open decision:

> D3. PRD retention — keep in repo (risk: doc rot) vs. close in issue tracker. Default position: do not keep PRDs in working tree; archive via closed issues.

But [guardrails.md](guardrails.md) §3.24 has already mandated the answer:

> Store journey documents and PRDs externally (e.g. GitHub Issues) and close them when done.

D3 is decided in the guardrail but still flagged as open in todo. Inconsistency.

**Likely changes:**

- Update D3 in [todo.md](todo.md) to status "resolved" with a reference to 3.24 (and now 3.27 for research), matching how D8 is annotated ("Resolved (2026-05-15) — added as Aln17…").
- Decide whether the resolution note should mention any operational gap that *is* still open — e.g., enforcement of the retire rule (is there a hook/CI check that fails when PRDs survive in-repo?). If no such enforcement exists, file a follow-up todo (candidate: B-series cross-cutting hook). Mirror this for 3.27 (research retirement enforcement is also missing — already flagged in W13's "Missing" list).

**Risk:** Trivial. Bookkeeping.

---

### Item 5 — Scale-Invariance / "When to Skip Phases" Rule — **DONE (2026-05-17)**

**Resolution:** Option C (governance triage) — but reframed around Pocock's scale-invariance claim. The full pipeline does not get skipped by default; trivial work **collapses** each phase to seconds. Skipping requires an explicit mode coupled to the HITL/AFK label:

- **AFK → (c) agent-decides skips** — already gated by Gov5a eligibility checklist (resolved decisions, no high-risk surface, sandbox, automatable verification). Eligibility floor doubles as the triviality gate; no separate "trivial" definition needed.
- **HITL → agent asks** at task entry: (a) full / (b) human-skips / (c) agent-skips.
- **Unlabeled task** defaults to HITL-ask.
- **Hard tripwires (MUST-flag)** when (b) or (c) would skip a phase gating: public API, schema migration, auth, security-sensitive change, safety-critical logic, concurrency, broad architecture. Reuses Gov3 high-risk list.

**Files changed:**

- [guardrails.md](guardrails.md) — new core rule 3.29 + parallel-table row.
- [gr/gr_governance.md](gr/gr_governance.md) — new Gov5b (right after Gov5a) + two anti-pattern entries.

**Decisions resolved:**

- A/B/C/hybrid → **Option C** (governance rule), reframed as mode-selector rather than skip-list.
- "Trivial" definition → **not needed**; Gov5a AFK eligibility serves as the floor, and HITL defers to human.
- Mode vs label coupling → **coupled**: AFK forces (c), HITL forces ask.
- Tripwire flagging strength → **hard rule** (MUST flag), not soft.

**Loophole containment:** the "everything looks trivial" risk is closed by (1) full pipeline being the default frame (collapse, not skip), (2) (c) requiring AFK eligibility, (3) tripwires being mandatory regardless of mode.

---

### Item 5 (archived gap text)

**Gap:** Pocock claims the 7-phase pipeline is scale-invariant (works bug→app). Local guardrails imply pragmatism (3.1 Minimize Scope) but never spell out **which phases are skippable for trivial work**. Result: an agent fixing a one-line typo could technically be expected to walk through `aln → prd → iss → ral → qa → rev` or could equally skip everything — no rule says which.

**Likely changes (one of several shapes):**

- **Option A — Lightweight-path rule.** Add a core rule (3.28?) "Right-Size the Workflow" or extend Gov1 to specify: "For changes below threshold X, phases Y/Z may be skipped, but core rules still apply." Define X (LoC? files? risk class?).
- **Option B — Per-phase skip criteria in [phases.md](phases.md).** Each phase grows a "skippable when:" note. Less centralized but more accurate per phase.
- **Option C — Triage rule in [gr/gr_governance.md](gr/gr_governance.md).** A short rule that says: every task starts with a 30-second triage classifying it as `trivial | small | feature | epic`, with a phase-set per class. Mirrors how Aln17 prototyping is conditional.

**Decision points for the fresh session:**

- Pick A / B / C / hybrid.
- Define "trivial" concretely enough that agents don't game it. Candidate dimensions: LoC delta, behavior-change vs. cosmetic, public-API touched (no → maybe trivial; yes → never trivial), security touched (no → maybe trivial; yes → never trivial), files crossed.
- Verify against 3.20 (HITL/AFK declaration) — does a trivial task still need an explicit HITL/AFK label? Probably yes, but the label may be implicit-AFK for cosmetic-only changes.

**Risk:** Medium. A loose rule here becomes a loophole that swallows the whole workflow ("everything looks trivial in the moment"). The triage must be hard to game.

---

## Additional Reasonable TODOs (Surfaced by the Analysis)

### Item 6 — Loop Convergence Criterion — **DONE (2026-05-17)**

**Resolution:** human-verdict convergence (Pocock-aligned). Pass requires (a) zero fix-now findings remain + (b) PRD intent met in the human's judgment; `pass-with-backlog` allowed. Silent fix-now → backlog downgrade forbidden. Mechanized (typed AC-checklist gate) explicitly deferred — tracked as D9 in [todo.md](todo.md), revisit once PRD template C1 lands and a few QA sessions are observed.

**Files changed:**

- [gr/gr_qa.md](gr/gr_qa.md) — new Q9 (Loop Convergence Is a Human Verdict).
- [guardrails.md](guardrails.md) — new core rule 3.30 + parallel-table row (3.30 → Q9). Filed in §3 for reliability (visible without pulling detail doc).
- [todo.md](todo.md) — new D9 (postponed mechanization decision).

**Decisions resolved:**

- Strictness → **human judgment**, not mechanized.
- Home → **both** §3 core rule (visibility) + Q9 detail (locality). Mirrors existing parallel pattern.
- Timing of mechanized option → **postponed** to D9, contingent on C1 PRD template existing.

---

### Item 6 (archived gap text)

### Item 7 — Gray-Box Architecture — **DONE (2026-05-18)**

**Resolution:** Pocock's "gray-box architecture" clarified as a **labor partition** on top of deep modules, distinct from existing M3 (which is coding discipline). Definition imported from Pocock: human owns interface + boundary tests; agent owns internals; source remains visible (gray, not black). Imported as M3a in gr_modules.md (extension of M3, not a new M12 — metaphor stays adjacent). QA-load lever made explicit via Q10 in gr_qa.md.

**Files changed:**

- [gr/gr_modules.md](gr/gr_modules.md) — new M3a "Gray-Box Labor Partition" after M3. Coupled to autonomy label: AFK → partition default; HITL → agent must ask which variant (full / co-author iface+tests / joint).
- [gr/gr_qa.md](gr/gr_qa.md) — new Q10 "Read the Seam, Not the Internals (Gray-Box QA)". Human QA reads interface + boundary tests + AC; internals read only on finding or M11-flagged suspicion. Explicitly does not weaken `rev`.
- [guardrails.md](guardrails.md) — new core rule 3.31 + parallel-table row (3.31 → M3a, Q10).

**Decisions resolved:**

- A / B / C (expand M3 / new M12 / new gr_graybox.md) → **B, slotted as M3a** (extension of M3, not separate rule number — keeps metaphor adjacent).
- Scope of partition rule → **coupled to AFK eligibility**: AFK default-applies; HITL requires agent to ask.
- QA consequence → **new Q10**, mandatory seam read, conditional internals read. Without Q10 the metaphor imports without the lever.
- `rev` interaction → unchanged. Gray-box reduces human QA read only; agent review of internals stays full.

### Item 8 — Research + PRD Retirement Enforcement — **DONE (2026-05-18)**

**Resolution:** two separate mechanisms, both lint + `qa`, no GitHub Action / webhook / CI infrastructure required. The brief's "same shape covers both" claim was rejected on inspection: 3.24 retires an *external* artifact (issue close in GitHub) and 3.27 retires a *tree* artifact (file deletion in repo). The verbs differ, so the enforcement differs — but both gates fire at the same merge point (`qa` Q11), so the operational surface is unified.

**Research (3.27 / Res3 / Res4):**

- Provenance field: every `research/<topic>.md` MUST declare `owner-issue: #NNN` in its Res4 header, naming the **PRD/feature epic issue** (1:1, owner = epic, not decomposed tickets — epic closes naturally last).
- Pre-PRD exploratory research forbidden: no file on disk without an owner issue. Create the epic stub first.
- Retirement trigger: owner-issue close. The PR that closes the epic MUST delete the research file in the same diff (Res3).
- Cross-feature reuse: copy facts into a new file under a new `owner-issue`. No multi-owner, no symlinks, no resurrection (new Res10a).
- Lint: pre-commit rejects research files missing `owner-issue`.
- Merge gate: `qa` Q11 verifies "owner-issue closing → file deleted" before pass.

**PRD (3.24 / Doc11):**

- PRD body lives in the owning GitHub issue, period. There is no in-tree artifact to retire because there should never be one.
- Lint: pre-commit rejects paths matching `prd/**`, `**/PRD-*.md`, `**/*_prd.md`.
- Merge gate: `qa` Q11 verifies the same condition as belt-and-braces.

**Why simple/easy/safe:**

- Two lints (one regex each) + one `qa` checklist line. No CI Actions, no webhooks, no sprint-close ritual.
- `qa` is already a mandatory pre-merge phase (gr_qa.md scope), so Q11 attaches to an existing gate rather than introducing a new one.
- Failure mode = PR blocked at `qa`, not silent rot. Survives AFK because the lint is mechanical and Q11 is agent-runnable.
- Substrate-neutral except for the word "issue" — every tracker has issues.

**Files changed:**

- [guardrails.md](guardrails.md) §3.24 (lint-paths enforcement sentence), §3.27 (owner-issue + Q11 trigger sentence), §9 parallel table rows for both (3.24 → Doc11, Q11; 3.27 → Res1, Res3, Res4, Q11).
- [gr/gr_research.md](gr/gr_research.md) Res3 (trigger mechanic explicit), Res4 (rewritten to mandate `owner-issue` field, forbid pre-PRD orphans), new Res10a (cross-feature copy-facts), four new anti-patterns.
- [gr/gr_qa.md](gr/gr_qa.md) new Q11 "Retire Orphaned Ephemeral Artifacts Before Merge" — two mechanical checks, lands on Q6 output line, mandatory even under gray-box (Q10).
- [gr/gr_documentation.md](gr/gr_documentation.md) Doc11 (lint-paths enforcement sentence, distinction-from-Res3 note).
- [todo.md](todo.md) W13 "Missing"/"Next" (retirement removed from missing, lint implementation deferred to D1 substrate decision), W14 "Missing"/"Next" (sandbox retirement now references Item 8's pattern for the future port to directories), D3 footnote (enforcement marked closed 2026-05-18).

**Decisions resolved:**

- Same mechanism for PRD + research? → **No, different mechanisms, same gate.** PRD = "prevent authoring in-tree"; research = "delete on owner-close." Unified at `qa` Q11.
- Trigger event for research retirement → **owner-issue close** (1:1 with PRD/feature epic).
- 1:1 vs N:1 ownership of research files → **1:1 forced**, with cross-feature reuse via Res10a copy-facts rule. Mechanism stays trivial; the discipline cost is paid by Res10a writers, not by the enforcement substrate.
- Failure mode → **hard block at `qa`**, not soft nag. Lint + Q11 both gate the merge.
- Substrate → **lint + `qa` checklist only.** No GitHub Action, no webhook. Defer richer mechanisms until lint+checklist proves insufficient.
- Pre-PRD research → **forbidden** (must create epic stub first). Cheap discipline beats `owner: TBD` second-check complexity.

**Follow-ups (not blocking):**

- Pre-commit lint implementation is mechanical; deferred to whenever skill substrate D1 is settled (no point writing hooks before the hook-host is chosen).
- W14 prototype sandbox retirement: same `owner-issue` + Q11 pattern, but adapted to directories (sandbox is a dir, research is a single file). Tracked in todo.md W14, not here.

### Item 9 — Idea Phase — **DONE (2026-05-18)**

**Resolution:** added lightweight `ide` phase, not the "document omission" path. Reframed per user direction: `ide` produces **3–6 major goals, no details**, as starter for `aln` grilling. Pocock-aligned (Idea = phase 1). Ephemeral (folded into PRD Goals section; no in-tree artifact, so no lint or Q11 gate needed). Collapsible per 3.29 when upstream brief already names goals.

**Files changed:**

- New: [gr/gr_idea.md](gr/gr_idea.md) — Idea1–Idea7 (3–6 goal cap, no details, negative goals welcome, HITL only, brief-as-input, feeds-not-replaces-aln, ephemeral).
- [phases.md](phases.md) — `ide` added as first sequential phase; bucket = Plan; sequence diagram updated to `ide → aln → [res?] → [pro?] → prd → …`.
- [guardrails.md](guardrails.md) — new core rule 3.32; routing §4.19; parallel-table row (3.32 → Idea1–Idea7); phase-list header includes `ide`.
- [gr/gr_alignment.md](gr/gr_alignment.md) — Aln8 reworded to point at `ide` distillation upstream; new cross-ref note at end.

**Decisions resolved:**

- Document omission vs. add phase → **add phase** (per user direction).
- Goal-count budget → **3–6** (hard floor + soft ceiling; fewer = go straight to `aln`, more = decompose/merge).
- Detail policy → **none** (no module map, no APIs, no UX, no AC).
- Persistence → **ephemeral**, folded into PRD Goals section.
- Negative goals → **first-class**, counted in the 3–6 budget when materially shape-defining.
- Collapsibility → **yes** via 3.29 (one-line confirmation when brief already lists goals).

**Follow-ups (not blocking):**

- Idea skill (parallels alignment / research / prototype skill build) — track in [todo.md](todo.md) if/when skill substrate D1 settles.
- PRD template should grow an explicit "Goals (from `ide`)" section so Idea7 has a deterministic landing site. Folded into PRD-template work, not a new item.

---

## How to Use This Document

For each fresh session:

1. Open this file. Read the relevant item section (each is self-contained).
2. Read the source files the item references (`guardrails.md`, `phases.md`, `todo.md`, the relevant `gr/*.md` and `wf/*.md`).
3. **Do not** assume the analysis is complete — verify the current state of the linked rules before editing; they may have moved.
4. Update this file when an item is resolved: mark status, point to the change.
5. Stop the session.

## Status

| Item | Title                                   | Status |
| ---- | --------------------------------------- | ------ |
| 1    | Research phase (`res`)                  | DONE   |
| 2    | Broaden prototype scope beyond FE       | DONE   |
| 3    | Clarify 3.26 (DAG ≠ mandatory parallel) | DONE   |
| 4    | Close todo D3 (PRD retention)           | DONE   |
| 5    | Scale-invariance / skip-phases rule     | DONE   |
| 6    | Loop convergence criterion              | DONE   |
| 7    | Gray-box architecture                   | DONE   |
| 8    | Research + PRD retirement enforcement   | DONE   |
| 9    | Idea phase (decide omission vs. add)    | DONE   |
