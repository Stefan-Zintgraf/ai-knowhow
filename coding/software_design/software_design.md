# Software Design Overview

Software design turns needs and constraints into a structure that can be built, tested, operated, and changed. It covers more than code organization: it also addresses product fit, behavior, boundaries, interfaces, data, and quality.

No single design approach covers every concern. A project may combine several approaches, using each where its strengths match the uncertainty or risk at hand.

Where a method has been distilled into an actionable rule set for coding agents, this document links it inline as **Agent rule set**. Those come from the third-party, MIT-licensed [`agent-rules-books`](https://github.com/ciembor/agent-rules-books) project — prescriptive working agreements for code generation, review, and refactoring, not method explainers — and each link gives both the local clone and the upstream repo. One rule set, *The Pragmatic Programmer* ([local](C:/PROJ/github/agent-rules-books/the-pragmatic-programmer/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/the-pragmatic-programmer)), is general engineering discipline that cuts across every method rather than mapping to one.

## Contents

- [What software design addresses](#what-software-design-addresses)
- [Product discovery and requirements approaches](#product-discovery-and-requirements-approaches)
  - [User-centered design and Design Thinking](#user-centered-design-and-design-thinking)
  - [Jobs to Be Done](#jobs-to-be-done)
  - [Lean Startup](#lean-startup)
  - [Use-case-driven design](#use-case-driven-design)
  - [Requirements engineering](#requirements-engineering)
- [Domain and behavioral modeling](#domain-and-behavioral-modeling)
  - [Domain-Driven Design](#domain-driven-design)
  - [EventStorming](#eventstorming)
  - [Structured analysis and state modeling](#structured-analysis-and-state-modeling)
- [Architectural styles and boundaries](#architectural-styles-and-boundaries)
  - [Clean and Hexagonal Architecture](#clean-and-hexagonal-architecture)
  - [Vertical Slice Architecture](#vertical-slice-architecture)
  - [Evolutionary architecture](#evolutionary-architecture)
- [Programming and implementation paradigms](#programming-and-implementation-paradigms)
  - [Object-oriented analysis and design](#object-oriented-analysis-and-design)
  - [Functional core, imperative shell](#functional-core-imperative-shell)
  - [Data-oriented design](#data-oriented-design)
  - [Data-intensive and distributed data design](#data-intensive-and-distributed-data-design)
  - [Aspect-oriented programming](#aspect-oriented-programming)
- [API and library design](#api-and-library-design)
  - [API-first and contract-first design](#api-first-and-contract-first-design)
- [Correctness and assurance approaches](#correctness-and-assurance-approaches)
  - [Formal methods](#formal-methods)
- [Operational and resilience design](#operational-and-resilience-design)
  - [Stability and resilience patterns](#stability-and-resilience-patterns)
- [Improving and evolving existing code](#improving-and-evolving-existing-code)
- [Choosing approaches by the problem](#choosing-approaches-by-the-problem)
- [A pragmatic sequence for a new product](#a-pragmatic-sequence-for-a-new-product)
- [A pragmatic sequence for a new library](#a-pragmatic-sequence-for-a-new-library)

## What software design addresses

Software design connects several levels of decision-making:

- **Product design** determines whose problem to solve and which outcomes matter.
- **Requirements design** defines behavior, constraints, and quality expectations.
- **Domain design** models the concepts, rules, and language of the problem space.
- **Architecture design** divides the system and controls dependencies.
- **Interface design** defines how users and software consumers interact with it.
- **Implementation design** chooses code structures, data representations, and programming paradigms.
- **Operational design** accounts for deployment, observability, security, reliability, and change.

These levels influence one another. Good design keeps them aligned without forcing one method to answer every question.

## Product discovery and requirements approaches

These approaches clarify what should be built and what the system must achieve.

### User-centered design and Design Thinking

Start with users, their environment, and their workflows. Observation, interviews, prototypes, and usability tests reduce the risk of solving the wrong problem.

**Best suited to:** products whose main uncertainty is user need or usability.

**Example:** observe warehouse workers and prototype a faster mobile picking flow before committing to backend structures.

**Reference:** [Design thinking — Wikipedia](https://en.wikipedia.org/wiki/Design_thinking).

### Jobs to Be Done

Define the progress a user seeks rather than starting from a feature list. This helps shape product positioning, scope, and priorities.

**Best suited to:** product and feature decisions centered on desired outcomes.

**Example:** design invoicing around “get paid promptly without chasing clients.”

### Lean Startup

Identify risky assumptions and test them with the smallest useful experiment. Evidence from prototypes, pilots, or manual services guides further investment.

**Best suited to:** new products with uncertain demand or business viability.

**Example:** test an AI meeting-summary service with a landing page and a manually operated pilot before building the complete platform.

**Reference:** [Lean startup — Wikipedia](https://en.wikipedia.org/wiki/Lean_startup).

### Use-case-driven design

Describe the goals of actors and their interactions with the system. Use cases make behavior concrete without prematurely choosing implementation details.

**Best suited to:** applications with identifiable actors and workflows.

**Example:** design a lending system around borrowing, renewing, returning, and collecting fines.

**Reference:** [Use case — Wikipedia](https://en.wikipedia.org/wiki/Use_case).

### Requirements engineering

Specify capabilities, constraints, interfaces, and quality attributes. Requirements may include timing, availability, safety, auditability, compliance, and capacity.

**Best suited to:** enterprise, embedded, regulated, safety-related, or contract-driven systems.

**Example:** define the timing, availability, and audit requirements of a medical monitoring service before selecting its architecture.

**Reference:** [Requirements engineering — Wikipedia](https://en.wikipedia.org/wiki/Requirements_engineering).

## Domain and behavioral modeling

These approaches help explain what the system represents and how it behaves over time.

### Domain-Driven Design

DDD aligns software models with a complex, evolving business domain. It emphasizes shared language, explicit model boundaries, and close collaboration with domain experts.

Strategic DDD separates models into bounded contexts. Tactical patterns such as entities, value objects, aggregates, repositories, and domain services can express behavior within a context.

**Best suited to:** systems with subtle business rules, changing terminology, competing models, or costly conceptual errors.

**Example:** separate pricing, fulfillment, and accounting models when each uses “order” differently and applies distinct rules.

DDD is one design approach among many. Its techniques can be used selectively and need not determine the architecture of an entire system.

**Reference:** [Domain-driven design — Wikipedia](https://en.wikipedia.org/wiki/Domain-driven_design).

**Agent rule sets:** Domain-Driven Design — [local](C:/PROJ/github/agent-rules-books/domain-driven-design/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/domain-driven-design); DDD Distilled — [local](C:/PROJ/github/agent-rules-books/domain-driven-design-distilled/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/domain-driven-design-distilled); Implementing DDD — [local](C:/PROJ/github/agent-rules-books/implementing-domain-driven-design/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/implementing-domain-driven-design). For the Domain Model vs. Transaction Script choice these patterns assume, see Patterns of Enterprise Application Architecture — [local](C:/PROJ/github/agent-rules-books/patterns-of-enterprise-application-architecture/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/patterns-of-enterprise-application-architecture).

### EventStorming

Explore a domain or workflow collaboratively by mapping events, commands, policies, actors, and external systems. It exposes gaps and disagreements quickly.

**Best suited to:** discovering complex processes with domain experts.

**Example:** map `Order placed`, `Payment authorized`, and `Parcel shipped` across sales, finance, and fulfillment.

**Reference:** [EventStorming — Wikipedia](https://en.wikipedia.org/wiki/Event_storming).

### Structured analysis and state modeling

Model processes, data flows, state transitions, and functional decomposition. These views make sequencing, transformation, and protocol behavior explicit.

**Best suited to:** workflow systems, protocols, embedded software, and transformation pipelines.

**Example:** model a vending machine through payment, selection, dispensing, refund, and fault states.

## Architectural styles and boundaries

Architecture establishes the system’s major parts, responsibilities, dependencies, and evolution constraints.

### Clean and Hexagonal Architecture

Keep application policy independent of infrastructure and delivery mechanisms. Ports express needs; adapters connect databases, user interfaces, external services, and tests.

**Best suited to:** systems that need replaceable integrations and independently testable application logic.

**Example:** put payment rules behind ports so tests use in-memory adapters while production uses a provider and SQL database.

**Reference:** [Hexagonal architecture — Wikipedia](https://en.wikipedia.org/wiki/Hexagonal_architecture_%28software%29).

**Agent rule set:** Clean Architecture — [local](C:/PROJ/github/agent-rules-books/clean-architecture/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/clean-architecture).

### Vertical Slice Architecture

Organize code around end-to-end capabilities rather than broad technical layers. Each slice contains the behavior and infrastructure needed for one feature.

**Best suited to:** teams delivering relatively independent capabilities incrementally.

**Example:** keep the command, validation, persistence, and endpoint for “cancel booking” together.

### Evolutionary architecture

Allow architecture to change incrementally while protecting important properties with feedback and fitness functions.

**Best suited to:** products whose requirements, integrations, or scale will change substantially.

**Example:** begin with a modular monolith and enforce dependency, security, and deployment-time constraints as it evolves.

**Reference:** [Building Evolutionary Architectures — Martin Fowler’s foreword](https://martinfowler.com/articles/evo-arch-forward.html).

Architectural styles are not exclusive. A system can use vertical slices within a modular monolith and hexagonal boundaries around volatile integrations.

## Programming and implementation paradigms

Implementation approaches shape code, data, control flow, and the placement of side effects.

### Object-oriented analysis and design

Assign responsibilities to collaborating objects that combine behavior with state. Encapsulation and polymorphism help localize variation.

**Best suited to:** behavior-rich systems with stable concepts and meaningful collaborations.

**Example:** model a drawing editor with `Document`, `Shape`, `Selection`, and `Command` objects.

**Reference:** [Object-oriented analysis and design — Wikipedia](https://en.wikipedia.org/wiki/Object-oriented_analysis_and_design).

**Agent rule sets:** Clean Code — [local](C:/PROJ/github/agent-rules-books/clean-code/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/clean-code); Code Complete — [local](C:/PROJ/github/agent-rules-books/code-complete/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/code-complete).

### Functional core, imperative shell

Place deterministic transformations in a pure core and isolate I/O and other side effects in a thin shell. This improves testability and reasoning.

**Best suited to:** rule-heavy logic, data transformations, and systems where effects need tight control.

**Example:** calculate prices with pure functions while a shell reads orders and persists results.

### Data-oriented design

Design around data layout, access patterns, and transformations. Representation is chosen to suit how data is processed rather than to mirror conceptual objects.

**Best suited to:** games, simulations, and high-performance or data-intensive systems.

**Example:** store positions and velocities in contiguous arrays so an engine can update thousands of entities efficiently.

**Reference:** [Data-oriented design — Wikipedia](https://en.wikipedia.org/wiki/Data-oriented_design).

### Data-intensive and distributed data design

Design around how data is stored, replicated, partitioned, and kept consistent across a system rather than around in-memory layout. The dominant concerns are reliability, scalability, replication and partitioning schemes, transaction and consistency semantics, event/stream processing, and schema evolution.

This is distinct from data-oriented design above: data-oriented design optimizes CPU and memory access within a process; data-intensive design governs correctness and durability of data across processes, machines, and time.

**Best suited to:** systems where data ownership, event flows, consistency guarantees, and evolving schemas dominate the risk — databases, pipelines, distributed services, and analytics platforms.

**Example:** choose partitioning keys and a replication and consistency model for a multi-region order store before deciding which framework serves it.

**Reference:** [Designing Data-Intensive Applications — Martin Kleppmann (book site)](https://dataintensive.net/).

**Agent rule set:** Designing Data-Intensive Applications — [local](C:/PROJ/github/agent-rules-books/designing-data-intensive-applications/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/designing-data-intensive-applications).

### Aspect-oriented programming

AOP modularizes behavior that cuts across many components. An aspect applies advice at selected join points, commonly defined through pointcuts.

Typical uses include tracing, metrics, authorization, transaction management, retries, caching, and policy enforcement. AOP can reduce repetition when the same concern must be applied consistently.

**Best suited to:** well-defined cross-cutting policies supported by clear tooling and conventions.

**Example:** apply an audit aspect to annotated service operations so calls record the actor, action, outcome, and duration consistently.

AOP should be used deliberately. Broad pointcuts and invisible interception can obscure control flow, complicate debugging, and create surprising interactions between aspects.

Prefer explicit composition, middleware, decorators, or higher-order functions when they keep the behavior easy to discover. Use AOP when centralized weaving provides a clearer and more reliable policy boundary.

**Reference:** [Aspect-oriented programming — Wikipedia](https://en.wikipedia.org/wiki/Aspect-oriented_programming).

## API and library design

For libraries, SDKs, services, and platforms, the public contract is often more important than the internal architecture.

### API-first and contract-first design

Design from the consumer’s perspective. Define inputs, outputs, failure behavior, compatibility, versioning, and operational expectations before implementation details harden.

**Best suited to:** libraries, SDKs, public services, platforms, and system integrations.

**Example:** write representative client code and specify errors and compatibility rules before implementing an image-processing library.

Consumer examples, contract tests, and small coherent interfaces reveal whether an API is understandable. Internal patterns should support the contract rather than leak through it.

**Agent rule set:** A Philosophy of Software Design (deep modules, simple interfaces, information hiding) — [local](C:/PROJ/github/agent-rules-books/a-philosophy-of-software-design/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/a-philosophy-of-software-design).

## Correctness and assurance approaches

Some systems require stronger evidence than example-based tests alone can provide.

### Formal methods

Use mathematical specifications, invariants, model checking, or proofs to reason about behavior.

**Best suited to:** safety-, security-, concurrency-, or correctness-critical components.

**Example:** verify that a distributed lock protocol cannot grant exclusive ownership to two clients at once.

Property-based testing, static analysis, type systems, simulation, and fault injection offer additional assurance. The appropriate combination depends on the cost and likelihood of failure.

**Reference:** [Formal methods — Wikipedia](https://en.wikipedia.org/wiki/Formal_methods).

## Operational and resilience design

Systems fail in production in ways that are invisible at design time: dependencies time out, load spikes, connection pools exhaust, and one slow component stalls the rest. Operational design treats production survival as a first-class design concern rather than an afterthought.

### Stability and resilience patterns

Design explicit behavior for failure and overload. Timeouts bound waiting; retries with backoff and jitter avoid synchronized storms; circuit breakers stop calling a failing dependency; bulkheads isolate resource pools so one failure cannot sink the whole system; backpressure and load shedding protect a service from demand it cannot meet. Health checks, graceful degradation, and observability make failures visible and recoverable.

**Best suited to:** networked services, APIs, queues, integrations, and any critical production path with real dependencies and load.

**Example:** wrap a flaky payment provider in a timeout and circuit breaker, isolate its thread pool with a bulkhead, and degrade to "payment pending" rather than blocking the checkout flow.

Resilience is a design property, not a deployment setting. Where failures propagate is decided by the boundaries and interfaces chosen earlier, so operational concerns belong in the design conversation from the start.

**References:** [Circuit breaker pattern — Wikipedia](https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern); [Release It! — Michael Nygard (book site)](https://pragprog.com/titles/mnee2/release-it-second-edition/).

**Agent rule set:** Release It! — [local](C:/PROJ/github/agent-rules-books/release-it/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/release-it).

## Improving and evolving existing code

Most design work happens on systems that already exist. Changing them safely — under incomplete tests and unclear boundaries — is its own design discipline, distinct from designing greenfield structure.

Refactoring improves internal structure without changing observable behavior, in small behavior-preserving steps guarded by tests. A catalog of code smells and named refactorings turns "this feels wrong" into concrete, reversible moves, and keeps structural change separate from feature change.

Legacy change adds a prior step: regaining control before improving. Characterization tests capture current behavior, seams create places to intervene without editing everything, and dependency-breaking techniques make untested code testable so refactoring can proceed safely.

**Best suited to:** any change to code you did not just write — especially poorly tested or tightly coupled systems where the first goal is regaining confidence.

**Example:** before extracting a tangled billing routine, pin its current output with characterization tests, introduce a seam to inject a fake clock and gateway, then refactor in small steps.

This complements evolutionary architecture: architecture-level fitness functions protect system properties over time, while refactoring and legacy techniques keep the code itself changeable underneath them.

**Reference:** [Refactoring — Martin Fowler](https://refactoring.com/).

**Agent rule sets:** Refactoring — [local](C:/PROJ/github/agent-rules-books/refactoring/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/refactoring); Refactoring.Guru — [local](C:/PROJ/github/agent-rules-books/refactoring-guru/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/refactoring-guru); Working Effectively with Legacy Code — [local](C:/PROJ/github/agent-rules-books/working-effectively-with-legacy-code/) · [GitHub](https://github.com/ciembor/agent-rules-books/tree/main/working-effectively-with-legacy-code).

## Choosing approaches by the problem

Start from the dominant uncertainty or risk:

- **Unclear user need:** user-centered design, Design Thinking, or Jobs to Be Done.
- **Uncertain demand:** Lean Startup and small experiments.
- **Complicated workflows:** use cases, EventStorming, structured analysis, and state machines.
- **Rich business rules:** DDD and explicit domain modeling.
- **Volatile integrations:** Hexagonal Architecture and ports and adapters.
- **Incremental feature delivery:** Vertical Slice Architecture.
- **Cross-cutting policies:** AOP, middleware, decorators, or explicit composition.
- **Library usability:** API-first design and consumer-driven contracts.
- **Throughput or memory pressure:** data-oriented design.
- **Data ownership, replication, or consistency:** data-intensive and distributed data design.
- **Production reliability under failure and load:** operational and resilience design (stability patterns).
- **Existing or legacy code:** refactoring, and characterization tests plus seams before change.
- **Change over time:** evolutionary architecture and fitness functions.
- **Critical correctness:** formal methods and stronger automated assurance.

The best choice is usually a combination. Use the smallest set of approaches that makes the important decisions explicit and keeps future change affordable.

## A pragmatic sequence for a new product

1. Identify the user outcome with research or Jobs to Be Done.
2. Test the riskiest assumptions with Lean experiments.
3. Describe critical use cases and quality requirements.
4. Model complicated domains and workflows with appropriate techniques.
5. Choose boundaries around business capability, volatility, and ownership.
6. Deliver vertical slices and validate them with users and operational feedback.
7. Add specialized techniques such as DDD, AOP, or formal methods where the problem justifies them.
8. Evolve the architecture while protecting important properties with automated checks.

## A pragmatic sequence for a new library

1. Write concrete examples of how consumers should use the library.
2. Design the smallest coherent public API that supports those examples.
3. Define invariants, failures, versioning, and compatibility guarantees.
4. Keep the core deterministic and side-effect-free where practical.
5. Test the API from the consumer’s perspective.
6. Select internal structures and paradigms that preserve the contract.
7. Add observability, security, or other cross-cutting behavior explicitly or through carefully scoped aspects.
