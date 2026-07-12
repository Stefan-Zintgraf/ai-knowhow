# Product Discovery and Requirements Engineering

**Status:** First draft

This collection covers the work that determines **what outcomes and observable behavior are worth creating** before and alongside software design. Software design then determines how to structure software that provides that behavior reliably and remains changeable.

There is no single universal phase name. In this collection:

- **Product discovery** reduces uncertainty about users, problems, value, and viable solutions.
- **Product definition** turns evidence and strategy into a coherent scope and set of capabilities.
- **Requirements engineering** makes required behavior, qualities, interfaces, and constraints explicit and verifiable.
- **Domain discovery** exposes the language, rules, events, and boundaries of the problem domain.

These activities overlap and repeat. They are not a one-time handoff to design.

## The lifecycle

```text
Vision and strategy
        ↓
Product discovery
  users, problems, outcomes, assumptions
        ↓
Product definition
  scope, capabilities, journeys, priorities
        ↓
Requirements and domain discovery
  use cases, rules, constraints, quality attributes
        ↓
Software design
  boundaries, architecture, interfaces, data
        ↓
Implementation and validation
        ↺ evidence feeds back into earlier decisions
```

## Documents

1. [Product vision](./product_vision.md) — establish direction, target users, intended change, principles, and boundaries.
2. [Product discovery](./product_discovery.md) — investigate opportunities and test risky assumptions.
3. [Requirements engineering](./requirements_engineering.md) — elicit, analyze, specify, validate, and manage requirements.
4. [Use cases and story mapping](./use_cases_and_story_mapping.md) — describe behavior around actor goals and coherent journeys.
5. [Domain discovery](./domain_discovery.md) — uncover terminology, rules, events, invariants, and candidate boundaries.
6. [Quality attributes](./quality_attributes.md) — make security, reliability, performance, usability, and other qualities concrete.
7. [Resources](./resources.md) — books, standards, repositories, and practical tools.

## A pragmatic workflow

1. Frame a provisional vision and name the desired outcome.
2. Identify the people involved and observe their present situation.
3. Map opportunities and assumptions; test the riskiest ones cheaply.
4. Describe critical journeys and use cases, including failure paths.
5. Discover domain language, policies, events, and invariants.
6. Specify quality attributes and external constraints as measurable scenarios.
7. Select a small, coherent release that can test the next important belief.
8. Carry requirements and evidence into design, delivery, and measurement.
9. Revisit earlier decisions when evidence changes.

## Minimum useful discovery package

For a small product, avoid producing documents merely for completeness. A useful minimum is:

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

- Whose outcome are we improving, and how will improvement be recognized?
- Which behavior is essential now, and which is deliberately deferred?
- What rules must always hold?
- Which failures and edge cases matter?
- Which quality attributes could change the architecture?
- What evidence supports the scope, and which assumptions remain open?

Uncertainty is acceptable. Hidden uncertainty is not.
