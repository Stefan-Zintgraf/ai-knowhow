# Product Discovery and Requirements Engineering

**Status:** Second draft

This collection covers the work that determines **what outcomes and observable behavior are worth creating** before and alongside software design. Software design then determines how to structure software that provides that behavior reliably and remains changeable.

Terms used across the collection are defined in the [glossary](./glossary.md).

There is no single universal phase name. In this collection:

- **Product discovery** reduces uncertainty about users, problems, value, and viable solutions.
- **Product definition** turns evidence and strategy into a coherent scope and set of capabilities.
- **Requirements engineering** makes required behavior, qualities, interfaces, and constraints explicit and verifiable.
- **Domain discovery** exposes the language, rules, events, and boundaries of the problem domain.
- **Validation and feedback** measures released behavior against intended outcomes and reopens earlier decisions.

These activities overlap and repeat. They are not a one-time handoff to design.

The lifecycle also does not divide work by department. Product, design, engineering, domain experts, and governance specialists participate where their evidence and authority are needed; one named person remains accountable for each consequential decision. See [Collaboration and decision ownership](./collaboration_and_decision_ownership.md).

## The lifecycle

The vision is a slow-changing anchor; a thin product strategy recorded alongside it — ordered outcomes and target segments — names the path toward it and is revised as evidence arrives. Discovery, definition, and requirements form a fast loop that runs continuously or in short cycles. Delivery consumes coherent slices from that loop, and validation feeds evidence back into every earlier stage.

```text
Product vision  (slow-changing anchor)
        │  revised only when evidence breaks it
        ▼
┌───────────────────────────────────────────────────┐
│  Discovery–definition–requirements loop (fast)    │
│                                                   │
│   Product discovery                               │
│     users, problems, outcomes, assumptions        │
│   Product definition                              │
│     scope, capabilities, journeys, priorities     │
│   Requirements and domain discovery               │
│     use cases, rules, constraints,                │
│     quality-attribute scenarios                   │
└───────────────────────────────────────────────────┘
        │  coherent slice with success and stop criteria
        ▼
Software design → implementation → release
        │
        ▼
Validation and feedback
  outcome measures, guardrails, incidents, operational evidence
        ↺  reopens vision, opportunities, scope, or requirements
```

Three clarifications the diagram cannot show:

- **Most pivots are discovery pivots.** Evidence normally changes opportunities, solutions, scope, or strategy — routine course corrections under a stable vision. A vision pivot, revising the intended future itself, is rare and requires evidence that invalidates the target need.

- **Quality attributes start early.** Qualities that could change the architecture are among the riskiest assumptions, so their discovery begins during product discovery. The requirements stage sharpens them into measurable scenarios; it does not begin them.
- **Not every topic enters at the top.** A greenfield product enters at the vision; a rework enters from validation evidence; a compliance mandate enters at requirements. See [Lifecycle tailoring](./lifecycle_tailoring.md) for entry points and how to size the lifecycle for a specific topic.

## Documents

Start with [Lifecycle tailoring](./lifecycle_tailoring.md) when applying this collection to a specific topic: it selects the entry point, stages, artifacts, cadence, and decision authority.

Stage documents, in lifecycle order:

1. [Product vision](./product_vision.md) — establish direction, target users, intended change, principles, and boundaries.
2. [Product discovery](./product_discovery.md) — investigate opportunities and test risky assumptions.
3. [Product definition](./product_definition.md) — select opportunities, shape scope and capabilities, prioritize, and cut a coherent release.
4. [Requirements engineering](./requirements_engineering.md) — elicit, analyze, specify, validate, and manage requirements.
5. [Use cases and story mapping](./use_cases_and_story_mapping.md) — describe behavior around actor goals and coherent journeys.
6. [Domain discovery](./domain_discovery.md) — uncover terminology, rules, events, invariants, and candidate boundaries.
7. [Quality attributes](./quality_attributes.md) — make security, reliability, performance, usability, and other qualities concrete.
8. [Validation and feedback](./validation_and_feedback.md) — measure released behavior against intended outcomes and decide what to reopen.

Reference documents:

- [Lifecycle tailoring](./lifecycle_tailoring.md) — derive a specific lifecycle for a specific topic.
- [Collaboration and decision ownership](./collaboration_and_decision_ownership.md) - default accountability, required participation, specialist authority, and skillset implications across the lifecycle.
- [Glossary](./glossary.md) — method terms used across the collection.
- [Resources](./resources.md) — reading order, technique index, and adoption criteria. Stage-specific examples, references, agent rule sets, and books live in each stage document's **Further material** section.

## A pragmatic workflow

The lifecycle above is the structural model — which stages exist and how evidence flows between them. A workflow is one ordered path through it. The steps below are a sensible default for a first pass; after that, the loop repeats at the cadence chosen during tailoring rather than restarting from step 1.

1. Classify the topic and tailor the lifecycle: entry point, stages, cadence, decision authority.
2. Frame a provisional vision and name the desired outcome.
3. Identify the people involved and observe their present situation.
4. Map opportunities and assumptions; test the riskiest ones cheaply.
5. Define scope: select opportunities, capabilities, and priorities for the next release.
6. Describe critical journeys and use cases, including failure paths.
7. Discover domain language, policies, events, and invariants.
8. Specify quality attributes and external constraints as measurable scenarios.
9. Cut a small, coherent release that can test the next important belief.
10. Carry requirements and evidence into design, delivery, and measurement.
11. Measure outcomes and guardrails after release; reopen earlier decisions when evidence changes.

## Minimum useful discovery package

For a small product, avoid producing documents merely for completeness. A useful minimum is:

- Lifecycle one-pager: entry point, stages in use, cadence, decision owners
- One-page product vision
- Named target users or actors and their desired outcomes
- Current journey or problem narrative based on evidence
- Opportunity/assumption map with the riskiest assumptions highlighted
- Critical use cases or a story map
- Important business rules and shared glossary
- Top quality-attribute scenarios and constraints
- Smallest release or experiment, with success and stop criteria
- Decision log linking major choices to evidence

## Readiness for software design

Design can begin incrementally when the team can answer:

Readiness is a team property, not a product-management sign-off. Use [Collaboration and decision ownership](./collaboration_and_decision_ownership.md) to ensure the answers include the necessary product, design, engineering, domain, and specialist judgment.

- Whose outcome are we improving, and how will improvement be recognized?
- Which behavior is essential now, and which is deliberately deferred?
- What rules must always hold?
- Which failures and edge cases matter?
- Which quality attributes could change the architecture?
- What evidence supports the scope, and which assumptions remain open?
- How will the outcome and its guardrails be observed after release?

Uncertainty is acceptable. Hidden uncertainty is not.
