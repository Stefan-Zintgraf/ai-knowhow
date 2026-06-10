# Guardrail: Architecture

Purpose: protect structural boundaries, dependency direction, and component ownership so the system remains understandable and changeable.

---

## Apply When

- Module or package boundaries are touched.
- Layering (e.g. presentation / application / domain / infrastructure) is involved.
- Dependencies between components are added, removed, or redirected.
- Public APIs, shared libraries, or service boundaries change.
- Anti-corruption layers around legacy or external systems are involved.
- Infrastructure concerns (DB, network, files) meet domain logic.

---

## Rules

### A1. Respect Layering

Code must live in the layer that matches its concern. Domain logic does not import infrastructure. Presentation does not call infrastructure directly.

### A2. Respect Dependency Direction

Dependencies point inward (toward the domain), not outward. No upward or sideways dependencies that violate the declared direction.

### A3. No Bypass of Existing Abstraction

If an abstraction exists for a concern (repository, adapter, port, facade), the agent uses it. Direct calls that skip the abstraction require explicit approval.

### A4. Preserve Module Boundaries

Cross-module access goes through the module's public interface. Reaching into another module's internals is forbidden.

### A5. Anti-Corruption Layer at Legacy and External Boundaries

Code that integrates with legacy systems or external services is isolated behind an adapter. The domain never speaks the foreign model directly.

### A6. Preserve Public API Compatibility

Public API shape, semantics, and error contract remain compatible unless a breaking change is explicitly authorized. Deprecate before removing.

### A7. Honor Component Ownership

If a component has a declared owner (team, file marker, CODEOWNERS, AI-rules file), changes must follow that owner's conventions and approval expectations.

### A8. No New Architectural Pattern Without Approval

Introducing a new framework, pattern (e.g. CQRS, event sourcing, plugin system), or cross-cutting mechanism requires explicit human decision.

### A9. Keep Infrastructure Out of Domain

Persistence, transport, framework types, and environment access must not leak into domain types or domain logic.

### A10. No Speculative Extension Points

No interfaces, plugin hooks, or generalized base classes added "in case" — only when the current task requires them.

### A11. Prefer Deep Modules

Module depth is a first-class architecture concern: prefer small interfaces hiding significant functionality over many narrow modules with tangled cross-dependencies. Module-shape decisions belong in alignment/PRD, not in implementation. See [gr_mod.md](gr_mod.md) for the full rule set; the review phase checks depth explicitly (see [gr_rev.md](gr_rev.md) Rev6).

---

## Anti-Patterns

- "Quick" direct DB or HTTP call from a domain function.
- Importing an infrastructure type into a domain entity.
- Adding a generic `BaseService` or `Manager` because "we might need it."
- Breaking a public API signature without versioning or migration note.
- Reaching into another module's private files because the public interface is "inconvenient."
- Adding many small files with mutual imports instead of a single deeper module (see [gr_mod.md](gr_mod.md) M4).
