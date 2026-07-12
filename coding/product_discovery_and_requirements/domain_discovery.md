# Domain Discovery

**Status:** First draft

Domain discovery builds a shared understanding of the real-world concepts, language, rules, events, and organizational boundaries the software must respect. It is especially valuable when business behavior is complex or terminology differs across groups.

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

