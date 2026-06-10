# Guardrail: Domain-Driven Design (Tactical)

Purpose: protect the integrity of domain models, aggregates, and business invariants. DDD here means modeling code around business concepts — not applying patterns mechanically.

---

## Apply When

- Bounded contexts, aggregates, entities, value objects are involved.
- Domain services, application services, or domain events are introduced or modified.
- Business invariants or domain rules are enforced.
- Cross-context boundaries are crossed.

---

## Rules

### D1. Keep Domain Rules Inside the Domain
Business invariants belong in domain types (entity, aggregate, value object) or domain services — not in controllers, repositories, or generic helpers.

### D2. Respect Aggregate Boundaries
A change that touches multiple aggregates must go through the aggregate root or a domain service. No direct reach-in across aggregate boundaries.

### D3. Enforce Invariants at Construction
An entity or value object cannot exist in an invalid state. Validation happens in the constructor or factory, not later.

### D4. Distinguish Domain Services from Application Services
Domain service = business logic that does not naturally fit one entity.
Application service = orchestration, transactions, external calls.
Do not mix.

### D5. Value Objects Are Immutable
Value objects must be immutable and compared by value. No identity, no setters.

### D6. Domain Events Describe Facts
Domain events are named in past tense and describe something that happened in the domain. They do not carry transport or infrastructure concerns.

### D7. Respect Bounded Context Boundaries
Crossing bounded contexts requires an explicit translation (adapter, anti-corruption layer, contract). No direct sharing of internal types.

### D8. No Generic "Helper" Code for Domain Logic
Domain rules are not extracted into `Util`, `Helper`, or `Manager` classes. They belong to a named domain concept.

### D9. Validation Lives Where the Invariant Lives
Input validation happens at the boundary (application layer). Domain invariants are enforced inside the domain. Do not duplicate or skip either.

---

## Anti-Patterns

- Anemic domain model: data classes with logic spread across services.
- "Smart" repositories that contain business rules.
- Mutable value objects with setters.
- Sharing an entity type directly across bounded contexts.
- A `DomainHelper` class holding business rules.
