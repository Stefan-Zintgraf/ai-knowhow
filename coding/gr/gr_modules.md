# Guardrail: Module Depth

Purpose: protect codebase shape against drift toward shallow modules. Deep modules — small interface, significant hidden functionality — are easier for both humans and AI agents to navigate, test, and change. Shallow modules with tangled cross-dependencies push agents into the dumb zone faster and produce brittle tests.

Origin: John Ousterhout, *A Philosophy of Software Design*. Reinforced as an AI-coding concern by Matt Pocock — unaided AI tends to produce shallow-module codebases unless humans direct otherwise.

---

## Apply When

- A new module, service, or significant component is created.
- An existing module is split, merged, or restructured.
- A PRD or planning artifact proposes a module map.
- A review surfaces tangled dependencies, unclear ownership, or many small files with cross-arrows.
- An architecture-improvement pass (`ica` phase) is run.
- Tests are hard to write because the "right" boundary is unclear.

---

## Rules

### M1. Prefer Deep Modules

A module should expose a small interface and hide significant functionality behind it. Default to fewer, broader-shouldered modules over many narrow ones.

### M2. Interface Before Implementation

When designing or proposing a module, name and shape its public interface first. Internals follow. The interface is the contract the rest of the codebase — and future agents — will rely on.

### M3. Treat Modules as Gray Boxes

Callers know the module's shape, behavior, and contract. They do not know its internals. The agent must not reach past the public interface (cross-reference: A4 module boundaries, A3 no bypass).

### M4. Anti-Pattern: Shallow Modules with Tangled Dependencies

Avoid: many small files each exposing many small pieces, with dense cross-module arrows. This forces every consumer (human or agent) to trace a dependency graph to understand what one call does. It also produces unclear mocking decisions in tests.

### M5. Test at the Module Boundary

A module's tests exercise its public interface, not every internal helper. A single test boundary should cover meaningful integrated behavior. Wrapping every tiny internal function in its own test is a shallow-module symptom and is forbidden as a default (cross-reference: gr_testing_verification.md).

### M6. Plan a Module Map in PRDs and Alignment

During `aln` and `prd` phases, the agent proposes and the human approves a **module map**: which modules will be touched, which are new, and what each new module's public interface looks like. The map stays in mind through implementation. New deep modules with a testable interface are identified explicitly.

### M7. Review Phase Checks Module Depth Explicitly

Code review (cross-reference: gr_review.md) must explicitly assess:

- Did the change deepen a module, leave depth unchanged, or shallowen it?
- Were new files added that expose narrow interfaces over small internals?
- Did dependency arrows multiply across module boundaries?

A change that shallowens modules without explicit justification is flagged for revision.

### M8. Refactor Toward Depth, Not Width

When refactoring touches module structure, the default direction is consolidation behind an interface, not further splitting. Splitting requires a stated reason (e.g. independent deployment, isolated invariant, separate ownership) — not "this file is getting long."

### M9. Resist AI's Default Toward Width

The agent treats its own first instinct to "split this into smaller pieces" as suspect. Small-piece decomposition feels clean but tends to produce shallow modules. The agent prefers a single deeper module unless a concrete reason for splitting is named.

### M10. Module Depth Is a Planning Concern, Not Only a Code Concern

Decisions that affect module depth (where a new responsibility lives, whether to introduce a service, whether to split an existing one) belong in `aln`/`prd`/`iss` — not invented during `ral`/`par`. An implementer agent that discovers a missing module decision stops and routes back to planning (cross-reference: Gov3).

---

## Anti-Patterns

- A new feature that adds eight small files in seven directories with mutual imports.
- A "utils" or "helpers" module that grows by accretion with no coherent interface.
- A service whose public API exposes nearly every internal function.
- Tests that mock every collaborator because the module boundary is unclear.
- Splitting a 300-line file into five 60-line files just to "keep files small."
- An agent silently introducing a new module mid-implementation without surfacing the decision.
- A PRD or issue that proposes implementation work without naming the modules involved.

---

## Notes on Interaction with Other Guardrails

- Reinforces **A4** (preserve module boundaries) and **A3** (no bypass of abstraction).
- Constrains **A10** (no speculative extension points) — a deep module is not a speculative extension point; it is a deliberate hiding of complexity behind a contract.
- Feeds **gr_review.md** — depth is one of the review dimensions.
- Feeds **gr_alignment.md** and **gr_governance.md** — module-shape decisions are HITL planning concerns, not AFK implementation concerns.
