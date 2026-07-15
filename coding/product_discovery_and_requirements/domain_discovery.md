# Domain Discovery

**Status:** Second draft

Domain discovery builds a shared understanding of the real-world concepts, language, rules, events, and organizational boundaries the software must respect. It is especially valuable when business behavior is complex or terminology differs across groups.

Terms used here are defined in the [glossary](./glossary.md). Note the distinction: the domain glossary produced by this stage records the *project's* domain language; the collection glossary defines the *method's* terms.

Domain discovery precedes and informs domain modeling. Its purpose is learning; the first diagram is not the final architecture.

## Questions to investigate

- Which events matter to the business?
- What commands, decisions, and policies cause them?
- Which rules must always hold?
- What information is needed to make each decision?
- Where do terms change meaning?
- Who owns decisions and data?
- Which processes are synchronous, delayed, manual, or uncertain?
- Where do exceptions and compensating actions occur?
- Which capabilities differentiate the product?

## Core techniques

### EventStorming

Collaboratively map domain events in time order, then add commands, actors, policies, read models, external systems, hotspots, and candidate boundaries. Start broad before focusing on one process.

### Domain storytelling

Let domain experts narrate concrete work while participants, work objects, and activities are drawn. This is useful when sequence and responsibility matter more than technical events.

### Example mapping

Explore a rule through concrete examples and questions. Rules without examples are often ambiguous; examples without rules are hard to generalize.

### Glossary and ubiquitous language

Record canonical terms, definitions, examples, forbidden synonyms, and context-specific meanings. Update prose and models when terminology changes.

### Context mapping

Identify where models and language differ, who owns each model, and how information crosses boundaries. Candidate bounded contexts are hypotheses that should reflect meaning, capability, ownership, and rate of change.

## Suggested workshop sequence

1. Choose a concrete business process or outcome.
2. Invite people who perform, support, govern, and build it.
3. Tell real recent stories before abstracting.
4. Map events and chronology.
5. Add decisions, actors, policies, external dependencies, and information needs.
6. Mark disagreements, unknowns, delays, failures, and manual interventions as hotspots.
7. Extract terms, rules, invariants, and ownership questions.
8. Propose capability and context boundaries only after the behavior is visible.
9. Validate the model against additional scenarios and exceptions.
10. Feed discoveries into use cases, requirements, quality scenarios, and design decisions.

## Outputs

- Domain event or story map
- Ubiquitous-language glossary
- Business rules and invariants
- Actor and responsibility map
- Capability map
- Candidate subdomains and bounded contexts
- Context map and integration relationships
- Hotspot and open-question list
- Representative examples and acceptance scenarios

## Rule and invariant template

```markdown
## BR-<id>: <Name>

Statement: ...
Applies in context: ...
Reason: ...
Examples: ...
Counterexamples: ...
Enforcement owner: ...
Consequences of violation: ...
Open questions: ...
```

An **invariant** must remain true within a defined consistency boundary. Not every policy is an invariant; some rules can be checked later or repaired through a compensating process.

## Common failure modes

- Inviting only engineers and guessing the domain
- Treating database nouns as the domain language
- Jumping from events directly to services or classes
- Forcing one enterprise-wide meaning on terms that legitimately differ by context
- Mistaking a workshop wall for validated truth
- Creating bounded contexts from organizational fashion rather than behavioral evidence
- Ignoring failures, delays, corrections, and manual work

## Completion checks

- Domain experts recognize their work and vocabulary in the model.
- Important disagreements and unknowns remain visible.
- Rules are supported by concrete examples and counterexamples.
- Context-specific meanings and ownership are explicit.
- Candidate boundaries explain what changes together and why.
- Discoveries trace into product behavior and requirements.

## Further material

**Examples:**

- During an EventStorming session, the event `Payment authorized` collects a hotspot sticker: finance explains that authorizations above a threshold go through a manual fraud review nobody in engineering knew existed. The review becomes an explicit policy with its own actor, instead of a surprise discovered in production.
- Example mapping of the rule "returned goods are refunded at purchase price" produces the counterexample "price changed between purchase and return during a promotion." The single rule splits into two — refund basis and promotion adjustment — each with its own owner.

**References:** [EventStorming](https://www.eventstorming.com/); [Domain-Driven Design Reference — Eric Evans](https://www.domainlanguage.com/ddd/reference/); [Domain Storytelling](https://domainstorytelling.org/).

**Agent rule sets:** [`ddd-crew/ddd-starter-modelling-process`](https://github.com/ddd-crew/ddd-starter-modelling-process) — scaffold from business model and discovery toward context boundaries and code; [`ForceInjection/domain-driven-design-skills`](https://github.com/ForceInjection/domain-driven-design-skills) — agent workflow from discovery through strategic and tactical design, validation, and specification bridging; [`lagz0ne/design-skill`](https://github.com/lagz0ne/design-skill) — a five-phase EventStorming-based design process (Requirements → Big Picture → Processes → Data/Flows → Integration) producing a navigable catalog of Mermaid diagrams.

**Books:** *Introducing EventStorming* — Alberto Brandolini; *Learning Domain-Driven Design* — Vlad Khononov; *Domain Storytelling* — Stefan Hofer, Henning Schwentner.

