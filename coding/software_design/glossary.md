# Glossary

Definitions for terms used across [software_design.md](./software_design.md) and [strategic_tactical_design.md](./strategic_tactical_design.md). Terms are grouped by the vocabulary they come from; several terms (e.g. bounded context) are used in more than one place in those documents.

## Contents

- [General design terms](#general-design-terms)
- [A Philosophy of Software Design (Ousterhout)](#a-philosophy-of-software-design-ousterhout)
- [Domain-Driven Design (DDD)](#domain-driven-design-ddd)
  - [Strategic DDD](#strategic-ddd)
  - [Tactical DDD](#tactical-ddd)
- [Architecture and boundaries](#architecture-and-boundaries)
- [Operational and resilience design](#operational-and-resilience-design)
- [Refactoring and legacy code](#refactoring-and-legacy-code)

## General design terms

- **Module** — a unit of code with a boundary; what it hides and what it exposes determine its design quality.
- **Interface** — the part of a module visible to its callers: signatures, contracts, and behavior guarantees.
- **Capability** — a unit of business-meaningful functionality a system provides, described independently of how it is implemented; often used to draw team or architectural boundaries.
- **Use case** — a description of how an actor interacts with a system to reach a goal, capturing behavior without prescribing implementation.
- **Information hiding** — concealing volatile design decisions inside a module so changes do not spread through the system. Originates with Parnas (1972).
- **Coupling** — how much one module depends on the internal details of another; the target for reduction through good boundaries.
- **Cohesion** — how strongly the responsibilities inside a single module belong together; the target for maximization within a boundary.
- **Invariant** — a condition that must hold true for a system, object, or module at every point it can be observed, regardless of which operations were performed on it. *(see also [Tactical DDD](#tactical-ddd), where it is scoped to an aggregate's transaction boundary)*
- **Idempotency** — the property that performing an operation more than once has the same effect as performing it once; what makes retries safe.
- **Complexity** — anything about a system's structure that makes it harder to understand or change. The central variable most design approaches try to reduce.
- **Essential vs. accidental complexity** — Fred Brooks' distinction between complexity inherent to the problem (essential) and complexity introduced by tools, process, or poor design (accidental, and the only kind design can remove).
- **Technical debt** — the gap between the current state of code and the state it would be in if it had been designed carefully, incurred deliberately or inadvertently and repaid with interest over time.
- **YAGNI ("You Aren't Gonna Need It")** — the counterweight to over-investment in design: don't build for speculative future requirements.
- **Fitness function** — an automated check that protects an architectural property (e.g. a dependency rule or a performance budget) as a system evolves.
- **Bounded context** *(see also [DDD](#strategic-ddd))* — a boundary within which a model and its language are consistent.

## A Philosophy of Software Design (Ousterhout)

Terms from John Ousterhout's *A Philosophy of Software Design*, describing two mindsets for approaching a design task.

- **Tactical programming** — short-term mindset: get the feature working, defer design.
- **Strategic programming** — investment mindset: working code is not enough; invest continually in structure.
- **Tactical tornado** — a highly productive developer who ships quickly while leaving complexity for teammates to absorb.
- **Deep module** — a module with a simple interface hiding substantial implementation complexity. The goal of strategic design.
- **Shallow module** — a module whose interface is nearly as complex as its implementation, offering little abstraction leverage.
- **Classitis** — the mistaken belief that more, smaller classes is always better design.
- **Change amplification** — a symptom of complexity where one conceptual change requires edits in many places.
- **Cognitive load** — how much a developer must know to make a change safely.
- **Unknown unknowns** — the worst symptom of complexity: it isn't even clear which code must change for a given modification.
- **Design it twice** — produce at least two candidate designs before committing to one.
- **Define errors out of existence** — simplify semantics so fewer exceptional conditions can arise in the first place.

## Domain-Driven Design (DDD)

DDD aligns software models with a complex, evolving business domain. It splits into a strategic layer (boundaries and language) and a tactical layer (model building blocks inside one boundary).

### Strategic DDD

Answers "what?" and "why?": what problem is being solved, and where must models and languages remain separate.

- **Domain** — a sphere of knowledge, influence, or activity; the problem space being modeled.
- **Subdomain** — a slice of the domain: core (differentiating), supporting, or generic.
- **Bounded Context** — a boundary within which a model and its language are consistent.
- **Ubiquitous Language** — the shared, precise vocabulary used inside one bounded context, by domain experts and developers alike.
- **Context Map** — the relationships between bounded contexts and the teams that own them.
- **Anti-Corruption Layer (ACL)** — a translation layer that protects a model from a foreign one it must integrate with.
- **Shared Kernel** — a small, explicitly shared subset of the model between two bounded contexts.
- **Conformist** — a context that adapts entirely to an upstream context's model rather than translating it.
- **Open Host Service** — a context that exposes a well-defined protocol for other contexts to integrate against.
- **Published Language** — a well-documented shared language (e.g. a schema) used for integration between contexts.

### Tactical DDD

Answers "how?": how behavior inside one bounded context is modeled and implemented.

- **Entity** — an object whose identity persists while its state changes; mutable.
- **Value Object** — an object that is immutable and compared by structural value, not identity.
- **Aggregate** — a consistency and transaction boundary with a single external entry point; enforces invariants.
- **Aggregate Root** — the only object within an aggregate that outside references may point to.
- **Invariant** — a rule an aggregate guarantees to hold at every transaction boundary.
- **Corrective Policy** — the compensating logic needed when an invariant is relaxed (e.g. eventual rather than immediate consistency).
- **Repository** — collection-like access for retrieving and persisting existing aggregates.
- **Factory** — creates new aggregates, ensuring they start valid.
- **Domain Event** — a fact meaningful to the domain, named in the past tense (e.g. `OrderPlaced`).
- **Domain Service** — domain logic that belongs to no single entity or value object.
- **Application Service** — orchestrates a use case while keeping domain rules inside the model, not itself.
- **Transaction Script** — procedural business logic; a legitimate, simpler alternative to a domain model for low-complexity subdomains.

## Architecture and boundaries

- **SOLID principles** — five object-oriented design guidelines (Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion) for keeping modules cohesive and independently changeable.
- **Hexagonal / Clean Architecture** — keeps application policy independent of infrastructure; ports express what the application needs, adapters connect concrete infrastructure.
- **Dependency Rule** — in Clean Architecture, the constraint that source-code dependencies point only inward, toward higher-level policy, never outward toward infrastructure detail.
- **Port** — an interface through which application logic expresses a need (e.g. "persist an order"), independent of any concrete implementation.
- **Adapter** — a concrete implementation of a port that connects to real infrastructure (a database, an external API, a UI, or a test double).
- **CQRS (Command Query Responsibility Segregation)** — separates operations that change state (commands) from operations that read state (queries), often using different models for each.
- **Vertical Slice Architecture** — organizes code around end-to-end capabilities (one feature's command, validation, persistence, and endpoint together) rather than broad technical layers.
- **Evolutionary architecture** — an architecture designed to change incrementally, with fitness functions protecting important properties as it does.
- **Aspect-oriented programming (AOP)** — modularizes cross-cutting behavior (logging, auth, retries) by applying advice at selected join points via pointcuts, instead of repeating it in every module.

## Operational and resilience design

Patterns for surviving production failure and overload, distinct from correctness at design time.

- **Timeout** — bounds how long a caller will wait for a dependency before giving up.
- **Retry with backoff and jitter** — re-attempts a failed call after a randomized, increasing delay, to avoid synchronized retry storms.
- **Circuit breaker** — stops calling a dependency that is failing, to give it room to recover and to fail fast for callers.
- **Bulkhead** — isolates resource pools (threads, connections) per dependency so one failing dependency cannot exhaust resources needed by the rest of the system.
- **Backpressure / load shedding** — a service's mechanism for refusing or deferring work it cannot currently handle, rather than degrading for everyone.
- **Graceful degradation** — continuing to serve a reduced but useful experience when a dependency is unavailable, instead of failing entirely.

## Refactoring and legacy code

- **Refactoring** — improving a system's internal structure without changing its observable behavior, in small, behavior-preserving steps guarded by tests.
- **Code smell** — an observable symptom in code (e.g. long method, feature envy) that suggests an underlying design problem worth refactoring.
- **Characterization test** — a test that pins down a system's current (not necessarily correct) behavior before changing it, so a change to structure can be verified not to change behavior.
- **Seam** — a place in code where behavior can be altered without editing the code in that place, typically used to inject a test double into legacy code.
- **Strangler fig pattern** — incrementally replaces a legacy system by routing new functionality through a facade to a new implementation while the old system keeps running, until nothing routes to it and it can be removed.
