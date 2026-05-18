# Workflow: Prototype Route for Hard-to-Reverse Decisions

Purpose: use AI for exploratory variant generation when grilling cannot resolve a decision in words, without pretending the agent has calibrated taste over the outcome.

Scope: invoked from phase `pro` (see [`phases.md`](../phases.md) and [`gr/gr_prototype.md`](../gr/gr_prototype.md)). Entry from `aln` (design ambiguity) or `res` (build-to-learn spike). Decision to prototype is made before `pro` enters, per Pro1 trigger gate.

Origin: Pocock 7-phases doc, phase 3 (Prototype). Replaces and broadens the earlier FE-only `wf_fe_prototype.md`.

---

## When to Use

Run `pro` when Pro1 holds:

- **Irreversibility** — decision is hard / expensive to reverse once code lands (persistence shape, public API shape, queue vs. sync, framework choice, primary UX paradigm).
- **Cost asymmetry** — wrong-choice cost >> 2–3 throwaway variants.

If neither holds, do not prototype. Resolve in `aln` and move on.

Three flavors (Pro2). Pick one per `pro` invocation — do not mix:

| Flavor          | Question shape                                                | Variant artifact                                                       |
| --------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **FE / UX**     | Visual, layout, interaction shape, information density.       | Disposable routes / switchable UI behind a sandbox path.               |
| **Architecture**| Module shape, sync vs. async, queue vs. direct, storage shape.| Throwaway skeleton impls exercising the shape, not the full feature.   |
| **Integration**| External-service shape (real payload, webhook order, limits). | Spike scripts hitting the real or vendor-sandbox service; captures.    |

---

## Inputs

- The unresolved decision, stated as a single question (one flavor).
- Constraints already established in `aln` (module map so far, hidden-constraint coverage).
- For FE: existing design system tokens / components, if any.
- For Architecture: existing architecture sketch (current module map) and the boundary the decision sits at.
- For Integration: vendor docs, sandbox credentials, and any captured traffic so far.
- A clearly-marked sandbox location (route, branch, folder) where variants live.

---

## Steps

1. Restate the decision in one sentence. Verify Pro1 (irreversibility or cost asymmetry). If neither holds, exit `pro` and resolve in `aln`.
2. Pick the flavor (FE / Architecture / Integration). One only.
3. Generate **2–3 variants** (Pro4). Each variant is independently runnable in the sandbox. No variant is marked "preferred" by the agent.
4. Run the hidden-constraint check (Pro7) per variant — security, perms, retention, migrations, observability, API compat, concurrency. Flag or replace any variant that quietly violates a class.
5. Present variants to the human / domain expert. For each variant, supply observable facts only (LOC, dependency delta, latency measured, captured response). No agent recommendation.
6. Human picks. Capture chosen direction **and** rejected variants (rejected variants become Aln15 negative decisions).
7. Feed the chosen direction back:
   - to `aln` (Aln12 module map updated, Aln15 negative decisions recorded), or
   - to `res` (if `pro` was invoked from research — record the chosen shape as fact), or
   - directly to `prd` (PRD implementation-decisions section cites the prototype outcome).
8. **Delete the sandbox** (Pro3). Deletion is a precondition for exiting `pro`. No prototype code survives into production impl.

---

## Outputs

- Chosen direction (single).
- Set of rejected variants with reasons (Aln15 negative decisions).
- Updated module map / research facts / PRD implementation-decisions entry.
- A clean working tree — sandbox deleted.

---

## Benefits

- Surfaces irreversibility before code lands.
- Forces variant comparison instead of first-idea lock-in.
- Keeps taste-judgments with the human, who has the calibrated taste.
- Shared discipline across FE, architecture, and integration — one phase, one rulebook.

---

## Tradeoffs

- Costs hours-to-days of agent + human time. Reserved for Pro1 cases.
- Prototype code is low quality by design — temptation to keep it is real (Pro3 anti-pattern).
- HITL only (Pro6). Not AFK-compatible.

---

## Failure Modes

- **Prototype leaks into production** — Pro3 skipped. Mitigation: sandbox path is clearly marked; deletion is a hard precondition for exiting `pro`. Reviewer (`rev`) verifies the deletion.
- **Agent picks the winner** — Pro4 violated. Mitigation: agent supplies observable facts only; explicit "no recommendation" in the variant report.
- **Single variant produced** — defeats the comparison logic. Mitigation: 2–3 is mandatory; one-variant output fails the phase.
- **Wrong flavor mixed** — e.g., FE variant smuggling an architecture decision. Mitigation: one flavor per invocation; mixed-flavor decisions split into separate `pro` runs.
- **Fabricated integration responses** — Pro8 violated. Mitigation: spike hits the real or vendor-sandbox service; any "synthetic" payload is flagged as such, never presented as observed.
- **FE variant ignores design system / a11y / responsive** — variant evaluation criteria not stated. Mitigation: criteria stated up front; design system tokens supplied as input when one exists.
- **Pro1 gate ignored** — `pro` invoked for reversible, low-cost decisions, becoming the default escape from grilling. Mitigation: step 1 restates Pro1 explicitly; agent declines `pro` when neither condition holds.

---

## Validation Idea

Track whether prototype-derived PRDs reduce later rework (architecture churn, UX U-turns, integration surprises) compared to PRDs without a prototype step. Separate the three flavors when measuring.

---

## Notes on Interaction with Other Guardrails

- Entry: `gr_prototype.md` Pro1 (trigger), Pro2 (flavor selection).
- Output feeds: Aln12 (module map), Aln15 (negative decisions for rejected variants), `prd` phase, `res` (when invoked from research).
- Not AFK: inherits Pro6 (HITL by construction).
- Retirement parallels: Pro3 mirrors Res3 / 3.27 (research retirement) and Doc11 / 3.24 (PRD retirement). Same anti-rot logic, different artifact shape.
- Distinct from research: `res` captures facts; `pro` explores design by building. The two compose — `res` may invoke `pro` to produce a fact; `pro` may produce facts as a side effect that then live in `res`, not in the prototype sandbox.
