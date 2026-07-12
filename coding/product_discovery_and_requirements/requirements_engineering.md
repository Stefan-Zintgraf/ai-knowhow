# Requirements Engineering

**Status:** First draft

Requirements engineering is the disciplined work of eliciting, analyzing, specifying, validating, and managing what a system must achieve and the conditions under which it must operate. ISO/IEC/IEEE 29148 is the principal international standard.

Requirements should preserve intent while leaving design freedom where no constraint is justified.

## Requirement types

- **Stakeholder needs:** outcomes or capabilities needed by people and organizations.
- **Functional requirements:** observable behavior the system must provide.
- **Quality requirements:** measurable properties such as latency, availability, safety, or usability.
- **Interface requirements:** interactions with people, devices, software, and organizations.
- **Data requirements:** meaning, quality, ownership, retention, residency, and lifecycle.
- **Constraints:** mandated technologies, standards, laws, budgets, dates, or operating conditions.
- **Transition requirements:** migration, rollout, training, coexistence, and decommissioning needs.

## Core process

### 1. Establish scope and sources

Identify system boundaries, stakeholders, governing documents, existing systems, and decision authority.

### 2. Elicit

Use interviews, observation, workshops, document analysis, prototypes, use cases, event analysis, and operational evidence. Elicitation discovers disagreements and tacit rules; it is not transcription.

### 3. Analyze

Resolve conflicts, define terms, model behavior, find omissions, test feasibility, prioritize, and separate needs from proposed solutions.

### 4. Specify

Write requirements at a level appropriate to risk and audience. Combine prose with examples, diagrams, state models, tables, or formal notation where these communicate more precisely.

### 5. Validate

Review requirements with stakeholders and test them against realistic examples. Confirm that they describe the right system behavior, not merely well-formed sentences.

### 6. Manage

Version requirements, record rationale, assess changes, and maintain traceability through design, implementation, verification, and outcomes.

## Writing an individual requirement

A useful requirement is necessary, clear, singular, feasible, verifiable, and traceable. Prefer an actor and observable result.

```text
When <trigger/condition>, the <system or component> shall <observable response>
within/while <measurable constraint>, so that <rationale, recorded separately if preferred>.
```

Example:

> When an authorized user revokes a sharing link, the service shall reject subsequent uses of that link within 60 seconds across all regions.

Avoid vague terms such as “fast,” “user-friendly,” “secure,” “normally,” or “as appropriate” unless they are defined by measurable criteria.

## Traceability model

Use only as much traceability as the risk warrants:

```text
Evidence → stakeholder need → requirement/use case → design decision
         → implementation → verification → observed outcome
```

Trace rationale as well as identifiers. Otherwise teams know that two items are connected but not why.

## Prioritization

Consider:

- Contribution to desired outcomes
- Risk reduction and learning value
- Legal, safety, security, or contractual necessity
- Dependency and sequencing
- Cost of delay
- Implementation cost and reversibility

MoSCoW can communicate release scope, but every “must” needs a consequence explaining why it is mandatory.

## Change policy

Changing a requirement is not failure; unmanaged change is. For consequential changes, record:

- Trigger and new evidence
- Affected stakeholders and requirements
- Design, data, operational, and test impact
- Decision owner and date
- Migration or compatibility consequences

## Completion checks

- Requirements trace to real needs, constraints, or risks.
- Terms have one agreed meaning within the relevant context.
- Critical normal, alternative, and failure behavior is represented.
- Quality requirements are measurable scenarios.
- Conflicts and assumptions are visible.
- Each important requirement has a viable verification method.
- The set is understandable to product, domain, design, engineering, and test participants.

