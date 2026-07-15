# Glossary

**Status:** First draft

Method terms used across this collection, with one agreed meaning each. A project's own **domain glossary** (its ubiquitous language) is a separate artifact produced during [domain discovery](./domain_discovery.md); this file defines the vocabulary of the method itself.

Software-design and DDD terminology is defined in [`../software_design/glossary.md`](../software_design/glossary.md).

---

**Acceptance example** — A concrete Given/When/Then example that clarifies a requirement or business rule. Examples sharpen requirements; they do not replace the broader purpose and variations of a use case.

**Actor** — A role interacting with the system (a person or an external system), not necessarily one named individual. Different goals mean different actors; do not collapse them into a generic "user."

**Assumption** — Something that must be true for a solution to succeed, classified by the four discovery risks (value, usability, feasibility, viability) and ranked by importance and lack of evidence.

**Assumption map** — Assumptions arranged by importance and evidence strength, used to decide what to test first.

**Bounded context (candidate)** — A hypothesis about a boundary within which a model and its language stay consistent. During discovery it is a proposal reflecting meaning, capability, ownership, and rate of change — not yet an architecture decision.

**Business rule** — A policy the business requires the system to respect. Not every rule is an invariant; some can be checked later or repaired by a compensating process.

**Cadence** — How often the discovery–definition–requirements loop runs and produces decisions: continuous, timeboxed cycles, or gated milestones. Chosen during [lifecycle tailoring](./lifecycle_tailoring.md).

**Capability** — Something the product enables an actor to do, expressed in solution-neutral language ("share a document with revocable access"), not as a feature or UI element.

**Constraint** — An externally mandated condition: technology, standard, law, budget, date, or operating environment. Constraints are recorded, not designed away.

**Decision log** — The running record of consequential decisions: what was decided, on what evidence, by whom, and when. It links major choices to evidence across the whole lifecycle.

**Domain discovery** — Building shared understanding of the real-world concepts, language, rules, events, and boundaries the software must respect.

**Entry point** — The lifecycle stage where work on a specific topic starts: greenfield product, new capability, rework of existing behavior, compliance mandate, fast-follow on strong evidence, or platform initiative. See [lifecycle tailoring](./lifecycle_tailoring.md).

**Evidence** — Observed behavior, data, or documented fact, deliberately distinguished from opinion, preference, and hypothetical enthusiasm. Evidence strength is recorded alongside decisions.

**Experiment card** — A one-page plan for a test: the decision it informs, the assumption, the method, the support/refute/inconclusive criteria, and the result.

**Extension** — An alternative or failure path of a use case, numbered against the step of the main success scenario where it branches.

**Functional requirement** — Observable behavior the system must provide.

**Greenfield** — An entry point where no product, prior evidence, or existing artifact exists; the lifecycle is entered at the vision stage and runs in full, at the smallest ceremony the risk allows.

**Guardrail measure** — A measure of harm that must not occur while an outcome is being optimized (e.g., support load, churn, error rate). Every outcome measure should have guardrails.

**Hotspot** — A marked disagreement, unknown, delay, or risk on a domain map, kept visible instead of resolved prematurely.

**Invariant** — A rule that must remain true at all times within a defined consistency boundary. Stricter than a business rule.

**Jobs to Be Done (JTBD)** — Framing of the stable progress a person seeks, expressed independently of any particular solution.

**Journey** — The end-to-end path an actor takes toward a goal, across features, channels, and manual steps.

**Lifecycle** — The structural model of stages and their relationships: which activities exist (vision, discovery, definition, requirements, design, delivery, validation), how they feed each other, and where evidence loops back. A lifecycle is not a schedule and not an ordered procedure — stages overlap and repeat. Contrast with **workflow**.

**Lifecycle tailoring** — Deriving a specific lifecycle for a specific topic: entry point, stages, artifacts, cadence, and decision authority. Recorded as a lifecycle one-pager.

**Minimal guarantee** — What remains true for stakeholders even when a use case fails (e.g., no partial charge, an audit record exists).

**Minimum useful discovery package** — The smallest artifact set worth producing for a small product; defined in the [overview](./overview.md).

**Opportunity** — A user need, pain point, desire, or obstacle that could be addressed. Kept deliberately separate from proposed solutions.

**Opportunity Solution Tree** — A structure connecting a desired outcome to opportunities, candidate solutions, and experiments.

**Outcome** — A measurable or observable change in user or business behavior. Outcomes, not shipped features, are the unit of value throughout this collection.

**Product definition** — Committing evidence and strategy into a coherent scope: selected opportunities, capabilities, journeys, and priorities for the next release.

**Product discovery** — Reducing uncertainty about whether a problem is worth solving, for whom, and which solution direction is desirable, usable, viable, and feasible.

**Product principle** — A durable decision rule that resolves recurring trade-offs (e.g., "the user remains in control of consequential actions").

**Quality attribute** — How well the system must behave under meaningful conditions: availability, latency, security, usability, and similar properties.

**Quality-attribute scenario** — A six-part measurable statement of a quality: source, stimulus, environment, artifact, response, response measure.

**Release slice** — A coherent subset of a story map that provides or tests value end-to-end. Coherent matters more than small.

**Requirement** — A verifiable statement of needed behavior, quality, interface, data, constraint, or transition. Types are defined in [requirements engineering](./requirements_engineering.md).

**Scenario** — One path through a use case.

**Signal** — A qualitative or leading indication that an outcome is moving. Weaker than an outcome measure; useful earlier.

**Stakeholder** — Anyone affected by or with authority over the product, including operators, regulators, and affected non-users — not only end users.

**Stop criteria** — Pre-agreed conditions under which an investment is paused or abandoned. Defined before the investment starts, alongside success criteria.

**Story** — A small, negotiable slice prepared for a delivery conversation. A flat list of stories is not a behavioral model.

**Story map** — Activities and tasks arranged in narrative order with candidate stories beneath, showing the end-to-end journey and release boundaries.

**Success criteria** — Pre-agreed conditions showing that a release or experiment achieved its purpose.

**Traceability** — Recorded links, with rationale, from evidence through stakeholder need, requirement, design, implementation, verification, and observed outcome. Used only as much as risk warrants.

**Transition requirement** — Migration, rollout, training, coexistence, and decommissioning needs — including when scope is retired.

**Ubiquitous language** — The canonical, context-specific domain terms shared by domain experts and the team, recorded in the project's domain glossary.

**Use case** — An actor goal plus its relevant scenarios: main success path, alternatives, and failures.

**Utility tree** — A ranked tree of quality-attribute scenarios beneath the product's value or mission, used to find high-importance, high-risk scenarios.

**Validation (of requirements)** — Confirming with stakeholders that requirements describe the right system behavior, not merely well-formed sentences. Distinct from the next entry.

**Validation and feedback (post-release)** — Measuring released behavior against intended outcomes and guardrails, and deciding which earlier decisions the evidence reopens. See [validation and feedback](./validation_and_feedback.md).

**Value / Usability / Feasibility / Viability** — The four recurring discovery risks: will people benefit, can they use it, can it be delivered, and does it work for the business and its legal, ethical, and operational environment.

**Vision** — The future change the product is intended to create: actors, desired change, value, principles, boundaries, and success signals. A slow-changing anchor, revised only when its underlying evidence breaks.

**Workflow** — A concrete, ordered sequence of steps for walking the lifecycle in practice. The [pragmatic workflow](./overview.md#a-pragmatic-workflow) in the overview is a default first pass; many workflows can implement the same lifecycle, and the cadence chosen during [lifecycle tailoring](./lifecycle_tailoring.md) determines how a workflow repeats. Contrast with **lifecycle**: the lifecycle says which stages exist and how they relate; a workflow says what to do next.
