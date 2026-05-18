# Guardrail: Prototype

Purpose: resolve ambiguity that resists grilling by building 2–3 throwaway variants and letting the human pick by feel. Distinct from research (`res` captures facts) and from implementation (`ral`/`par` produces production code).

Source: Pocock 7-phases workflow, phase 3 (Prototype). See [the-7-phases-of-ai-driven-development.md](../the-7-phases-of-ai-driven-development.md) §"Prototype as Taste-Imposition Step" and §"Prototype Variant Generation".

---

## Apply When

Phase `pro` is entered. Entry comes from one of:

- `aln` — grilling cannot resolve a design decision in words.
- `res` — research surfaces a question that only a build-to-learn spike can answer (e.g., actual webhook payload shape, real latency under load).

Trigger gate (Pro1) must hold. Without it, the decision belongs in `aln` (grilling) or `res` (facts).

Skip when: ambiguity is purely about facts (use `res`), purely about scope (resolve in `aln`), or the decision is reversible at low cost (just pick one in `aln` and move on).

---

## Rules

### Pro1. Trigger Gate — Irreversibility or Cost Asymmetry

`pro` fires only when **at least one** holds:

- **Irreversibility.** The decision is hard or expensive to reverse once code lands (e.g., persistence shape, public API shape, queue vs. sync architecture, framework choice).
- **Cost asymmetry.** Cost of the wrong choice >> cost of building 2–3 throwaway variants. Choosing wrong burns weeks; prototyping burns hours.

If neither holds, prototype is over-engineering. Resolve in `aln` and pick.

**Why:** the old Aln17 used "genuinely visual" as the gatekeeper. Widening prototype scope to architecture and integration removes that bright line — a replacement gate is needed or the phase swallows every fuzzy decision.

### Pro2. Three Flavors, One Phase

Prototype variants fall into one of three flavors. Same phase, same discipline, different artifact:

- **Front-end / UX** — layout, interaction, information density. Variants live behind a temporary route or switchable UI. See [`wf/wf_prototype.md`](../wf/wf_prototype.md) §"FE Variant".
- **Architecture** — module shape, sync vs. async, queue vs. direct call, storage shape. Variants are throwaway skeleton impls that exercise the shape, not the full feature.
- **Integration** — external-service shape (third-party API actual payload, webhook firing order, rate-limit behavior). Variants are spike scripts hitting the real (or sandbox) service.

A single `pro` invocation handles one flavor. Mixing flavors in one prototype = back to grilling.

### Pro3. Throwaway by Construction

Variants are **disposable**. Code lives in a clearly-marked sandbox (route, branch, folder) and is **deleted before** `prd`/`iss` writes production code from the chosen direction. Prototype code never silently becomes the production impl — that path produces low-quality production code and erases the throwaway discipline.

Deletion is a precondition for exiting `pro`. Tracked the same way `res` artifacts are retired (3.27, Res3).

**Ordering with caller capture (Pro5).** The C6 variant artifact lives inside the sandbox (`<sandbox_path>/variants.md`). The caller must read and persist its facts (Pro5) **before** sandbox deletion — otherwise `decision_outcome.rejected` and `rationale_by_human` are lost. Deletion sequence: (1) human fills `decision_outcome`; (2) caller reads C6 and writes its own artifacts (Aln15 / `research/<topic>.md` / PRD section); (3) caller signals capture complete; (4) `pro` deletes sandbox. Step 2 failing closed blocks step 4.

### Pro4. 2–3 Variants, No Self-Judging

The agent produces 2–3 variants. The human (or domain expert) picks. Agent does **not** declare a winner. Reason: prototype variants are taste-impositions — agent has no calibrated taste over arch tradeoffs, UX, or integration ergonomics in this codebase. Self-judging defeats the phase.

Agent may flag observable facts about each variant (LOC, dependency added, latency measured) but stops short of "I recommend B".

Artifact shape: [`tpl/tpl_variant_presentation.md`](../tpl/tpl_variant_presentation.md) (C6). Schema omits `recommendation`/`preferred`/`best`/`score` fields; body vocabulary blocks subjective terms. Pro4 is enforced by template, not by reviewer convention alone.

### Pro5. Output Feeds Aln / Res / Prd — Caller Persists

The chosen direction is the output. **`pro` emits exactly one artifact: the C6 variant doc ([`tpl/tpl_variant_presentation.md`](../tpl/tpl_variant_presentation.md)) with the chosen variant marked and `captured_responses` populated where applicable.** `pro` does not edit any other phase's files. The caller reads C6 on return and updates its own artifacts:

- **`aln` caller** — reads C6, updates Aln12 module map with the chosen shape, appends rejected variants to Aln15 as negative decisions.
- **`res` caller** — reads C6, appends the chosen variant's facts (e.g., `captured_responses`) to `research/<topic>.md` under its existing `owner-issue` (Res4) header.
- **`prd` caller** — reads C6, cites the prototype outcome in the PRD's implementation-decisions section; appends rejected variants to PRD's rejected-alternatives section if present, else to Aln15.

Why caller-persists is symmetric across all three callers: `pro` stays caller-agnostic (no conditional write-mode per caller); each phase keeps ownership of its file conventions (module-map format, Res4 header, PRD section structure) instead of `pro` having to know all three; one handoff surface (C6) instead of three.

Rejected variants are recorded as negative decisions so a future agent does not re-propose them. The caller — not `pro` — performs that recording.

### Pro6. Not AFK

`pro` is HITL by construction — Pro4 requires a human picker. AFK promotion is forbidden (Gov5a). Same constraint as `aln`.

### Pro7. Hidden-Constraint Review on Variant Set

Before showing variants to the human, the agent checks each variant against the hidden-constraint classes (security, permissions, retention, migrations, observability, API compat, concurrency — same checklist as Aln6 / Rev7). A variant that quietly violates a hidden constraint must be flagged or replaced before selection, otherwise the human picks aesthetics over correctness.

### Pro8. No Fabrication in Integration Spikes

Op13 applies in full. An integration prototype that invents API responses, mocks endpoints the real service does not expose, or fakes payloads it did not actually capture launders fabrication into "verified shape." Spikes hit the real (or vendor-sandbox) service and capture observed responses, or they are not integration prototypes.

---

## Anti-Patterns

- Prototype code promoted to production because "it already works" (Pro3 skipped).
- Agent picks the winner (Pro4 violated). Result: agent imposes taste it does not have.
- One prototype variant ("look, here is the answer"). Defeats the variant-comparison logic.
- Prototype invoked for reversible, low-cost decisions (Pro1 gate ignored). Phase becomes the default escape from grilling.
- Prototype invoked when the real question is facts (use `res`) or scope (use `aln`).
- Integration spike with fabricated API responses (Pro8 violated).
- FE prototype that ignores the existing design system — invents tokens, breaks a11y, ignores responsive behavior.
- `pro` exits without deletion of the sandbox code (Pro3 violated). Stale prototype code rots in the tree.
- AFK Ralph loop spins up a prototype (Pro6 violated).

---

## Pulling This Document

Pulled when:

1. Phase `pro` is entered (from `aln` or `res`).
2. `aln` grilling stalls on a decision and the agent considers whether Pro1 trigger holds.
3. Review (`rev`) of work that consumed a prototype — reviewer verifies Pro3 (sandbox deleted), Pro4 (human picked, not agent), Pro8 (no fabricated spike data).

Not pulled for: implementation work where the prototype phase already closed and only the chosen direction remains.

---

## Notes on Interaction with Other Guardrails

- Replaces the deleted Aln17 (FE-only prototype rule). Aln1 (HITL) still applies because `pro` is HITL by construction (Pro6).
- Distinct from `res` (gr_research.md): research = capture facts; prototype = explore design by building. `res` may invoke `pro` when only a spike can produce the fact. `pro` may produce facts as a side effect, which then live in research, not in the prototype sandbox.
- Pro3 mirrors 3.27 / Res3 (retire ephemeral artifacts) and Doc11 / 3.24 (retire PRDs). Same anti-rot logic, different artifact shape.
- Pro6 specializes Gov5a (HITL declaration) — `pro` is one of the canonical HITL phases alongside `aln` and `prd`.
- Output paths (Pro5) parallel Aln12 (module map) and Aln15 (negative decisions) — prototype outcomes are alignment outcomes, just produced by building instead of grilling.
