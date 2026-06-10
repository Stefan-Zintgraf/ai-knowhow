# Guardrail: Greenfield Design Rules

Purpose: prevent premature architecture and over-engineering in new code. In greenfield work, the danger is building for imagined needs.

---

## Apply When

- A new project, service, module, or major component is created.
- A first version of a system is being designed.
- Initial conventions, structure, or patterns are being set.

---

## Rules

### G1. Boring, Explicit, Replaceable First
Prefer the simplest, most explicit structure that solves the current need. Avoid clever, generalized, or "future-proof" designs.

### G2. First Vertical Slice Before Layers
Build a working end-to-end slice (one concrete use case, end-to-end) before adding layers, abstractions, or frameworks.

### G3. Defer Expensive Decisions
Decisions that are cheap to make later (advanced patterns, plugin systems, multi-tenancy, internationalization) are postponed until a concrete requirement exists.

### G4. Establish Conventions Once, Then Follow Them
Naming, file layout, error handling, and logging conventions are decided early and applied consistently. Changing them later is more expensive than picking them deliberately.

### G5. No Premature Abstraction
Concrete code first. Extract an abstraction only when at least two concrete cases demand it.

### G6. No Premature Framework
Don't introduce a framework, ORM, message bus, or plugin system unless the current scope requires it.

### G7. Initial Domain Vocabulary Is Recorded
Even in greenfield, the agent records the initial ubiquitous language as it emerges, to prevent drift. See `gr_domain_language.md`.

### G8. Initial Testing Strategy Is Explicit
The greenfield project decides early what test levels it values (unit, integration, end-to-end) and applies them from the start.

### G9. Record Postponed Decisions
Decisions deliberately postponed are written down (one line each) so they are not forgotten or silently re-decided.

### G10. Smallest Architecture That Supports the Next Known Requirement
Architecture is sized for the next concrete requirement, not for a five-year roadmap.

---

## Anti-Patterns

- Starting with hexagonal architecture, CQRS, event sourcing, and microservices for a CRUD prototype.
- Adding a plugin system "to be flexible."
- Writing a generic `Repository<T>` before a second entity exists.
- Designing a config system before the first config option exists.
- Long architecture documents written before any code runs.
