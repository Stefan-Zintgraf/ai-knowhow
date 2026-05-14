# AI Coding Guardrails

Purpose: Compact overview of always-on rules and routing index to detailed guardrail documents.

---

## 1. Core Idea

Guardrails are **constraints that protect system intent** — not a coding style guide.

This document is intentionally small. It contains:

- A short framing (mental model).
- A small set of **always-on** rules that apply to every task.
- A **routing index** of guardrail categories with pointers to detail documents (`gr/gr_*.md`).

The AI agent does not read every detail document by default. It identifies which categories apply to the current task and loads only those.

Applies to both greenfield and brownfield work. Context-specific emphasis lives in [gr/gr_brownfield.md](gr/gr_brownfield.md) and [gr/gr_greenfield.md](gr/gr_greenfield.md).

---

## 2. Mental Model

```
AI coding quality = Context × Constraints × Verification × Human judgment
```

Weakness in any factor creates risk. The guardrails address **Constraints**; the workflow document addresses **Context** and **Human judgment**; verification rules address **Verification**.

---

## 3. Always-On Guardrails

Apply to every AI-assisted planning or implementation task. Each entry is a headline plus a one-line rule. Detail and nuance live in the referenced category document.

### 3.1 Minimize Scope

The agent must actively narrow the task to the smallest useful, verifiable change. See [gr/gr_governance.md](gr/gr_governance.md).

### 3.2 Do Not Mix Concerns

Feature work, bug fixes, refactoring, formatting, migrations, dependency upgrades, and architectural changes must not be combined in one change. See [gr/gr_coding_style.md](gr/gr_coding_style.md).

### 3.3 Respect Existing Behavior

Existing behavior is treated as intentional until proven otherwise. See [gr/gr_brownfield.md](gr/gr_brownfield.md).

### 3.4 Make Assumptions Visible

Distinguish facts (from code, tests, docs, user input) from assumptions and open questions. See [gr/gr_governance.md](gr/gr_governance.md).

### 3.5 Avoid Speculative Design

No abstractions, frameworks, extension points, or generic mechanisms for hypothetical future needs. See [gr/gr_coding_style.md](gr/gr_coding_style.md).

### 3.6 Verify Changes

Every change must state how it is verified (tests, static analysis, build, manual review, acceptance criteria). See [gr/gr_testing_verification.md](gr/gr_testing_verification.md).

### 3.7 Stop on High-Risk Decisions

The agent must pause and ask before public API changes, data migrations, security-sensitive changes, safety-critical logic changes, concurrency changes, or broad architecture changes. See [gr/gr_governance.md](gr/gr_governance.md).

### 3.8 No Hardcoded Secrets

Secrets, tokens, keys, credentials must never appear in source, tests, fixtures, logs, or commit history. See [gr/gr_security_compliance.md](gr/gr_security_compliance.md).

### 3.9 No Bypass of Existing Abstraction

The agent must not circumvent an existing abstraction, layer, or anti-corruption boundary without explicit approval. See [gr/gr_architecture.md](gr/gr_architecture.md).

### 3.10 Preserve Public API Compatibility

Public API shape and behavior must remain compatible unless the task explicitly authorizes a breaking change. See [gr/gr_architecture.md](gr/gr_architecture.md).

### 3.11 No Silent Dependency Changes

Adding, removing, or upgrading third-party dependencies requires explicit approval. See [gr/gr_dependencies.md](gr/gr_dependencies.md).

### 3.12 Provide Verification Evidence

The final response must contain a concise diff summary plus the verification result (commands run, tests passed, checks performed). See [gr/gr_operational.md](gr/gr_operational.md).

### 3.13 Use Domain Language Consistently

Terms from the project's ubiquitous language must be used as defined; forbidden synonyms must not be introduced. See [gr/gr_domain_language.md](gr/gr_domain_language.md).

---

## 4. Guardrail Categories (Routing Index)

For each category: purpose, apply-when triggers, and detail document. Detailed rules live in the linked `gr/gr_*.md` files.

### 4.1 Architecture

Purpose: protect structural boundaries, dependency direction, and component ownership.
Apply when: module boundaries, layering, dependencies, public APIs, service boundaries, shared libraries, anti-corruption layers, or infrastructure/domain separation are involved.
Detail: [gr/gr_architecture.md](gr/gr_architecture.md)

### 4.2 Domain and Ubiquitous Language

Purpose: protect meaning. Keep names, terms, and concepts consistent with the domain.
Apply when: business terms, domain concepts, naming of domain objects, terminology changes, cross-team language, or user-facing concepts are involved.
Detail: [gr/gr_domain_language.md](gr/gr_domain_language.md)

### 4.3 Domain-Driven Design (Tactical)

Purpose: protect the integrity of domain models, aggregates, and invariants.
Apply when: bounded contexts, aggregates, entities, value objects, domain services, application services, domain events, or invariants are involved.
Detail: [gr/gr_ddd.md](gr/gr_ddd.md)

### 4.4 Coding Style and Conventions

Purpose: protect readability, consistency, and predictable behavior at the code level.
Apply when: any implementation task that produces or modifies code.
Detail: [gr/gr_coding_style.md](gr/gr_coding_style.md)

### 4.5 Testing and Verification

Purpose: define proof that a change is correct and safe.
Apply when: behavior change, bug fix, refactoring, legacy code change, public API change, or regression risk.
Detail: [gr/gr_testing_verification.md](gr/gr_testing_verification.md)

### 4.6 Security and Compliance

Purpose: protect against vulnerabilities, leaks, and regulatory violations.
Apply when: authentication, authorization, secrets, input validation, external interfaces, cryptography, logging of sensitive data, or compliance requirements are involved.
Detail: [gr/gr_security_compliance.md](gr/gr_security_compliance.md)

### 4.7 Brownfield Change Rules

Purpose: preserve invisible intent in existing systems.
Apply when: existing production code, legacy logic, or established behavior is touched.
Detail: [gr/gr_brownfield.md](gr/gr_brownfield.md)

### 4.8 Greenfield Design Rules

Purpose: prevent premature architecture in new code.
Apply when: a new project, service, module, or major component is created.
Detail: [gr/gr_greenfield.md](gr/gr_greenfield.md)

### 4.9 Documentation

Purpose: keep documentation concise, durable, and aligned with the code.
Apply when: documentation, comments, READMEs, or API docs are created or changed.
Detail: [gr/gr_documentation.md](gr/gr_documentation.md)

### 4.10 Governance and Authority

Purpose: define when the AI may act autonomously and when it must stop.
Apply when: any task — but especially when scope, approval, off-limits areas, or autonomy level is unclear.
Detail: [gr/gr_governance.md](gr/gr_governance.md)

### 4.11 Dependencies and Licensing

Purpose: control third-party code surface, versions, and license compatibility.
Apply when: adding, removing, or upgrading any third-party package or external service.
Detail: [gr/gr_dependencies.md](gr/gr_dependencies.md)

### 4.12 Operational and Agent Execution

Purpose: define what the agent must do during execution and what evidence it must produce.
Apply when: any implementation task — covers build/test commands to run, definition of done, and final-response format.
Detail: [gr/gr_operational.md](gr/gr_operational.md)

---

## 5. Routing Rule

Before detailed planning or implementation, the agent identifies which categories apply.

Recommended format:

```
Relevant guardrails:
- Always-on guardrails
- Testing and Verification, because the task changes behavior
- Brownfield, because existing production code is affected
```

The agent does not load every detail document by default. When unsure whether a category applies, the agent must mention the uncertainty and pick the smallest reasonable set.

**Always-on rules apply regardless of routing.** A misclassified task must not silently lose the always-on floor.

---

## 6. Conflict Resolution

When guardrails conflict, use this priority order:

1. Safety, security, and compliance
2. Correctness and behavior preservation
3. Architecture and domain integrity
4. Testability and maintainability
5. Consistency with coding style
6. Convenience or implementation speed

Speed is never a valid reason to bypass a higher-priority guardrail.

---

## 7. Anti-Patterns

The agent should avoid:

- Loading every detail document when only a subset is relevant.
- Skipping always-on rules because routing did not select the matching category.
- Treating guardrails as optional suggestions.
- Hiding assumptions or uncertainty.
- Turning a small change into a broad redesign.
- Changing behavior as a side effect of cleanup.
- Introducing new abstractions without current need.
- Inventing rules when a detail document is empty — instead, mark the gap and ask.

---

## 8. Starter Examples

### Example 1: Bug Fix in Existing Code

Relevant: Always-on, Brownfield, Testing and Verification, Coding Style, Operational.
Reason: behavior-affecting change with regression risk.

### Example 2: New Module in a Greenfield Project

Relevant: Always-on, Greenfield, Architecture, Coding Style, Testing and Verification, Operational.
Reason: new structure with risk of premature abstraction.

### Example 3: Rename a Business Concept

Relevant: Always-on, Domain Language, DDD (if domain model), Brownfield (if existing code), Testing and Verification, Documentation.
Reason: language change may ripple through code, API, docs, tests.

### Example 4: Authentication Change

Relevant: Always-on, Security and Compliance, Testing and Verification, Architecture (if boundaries change), Governance (likely human approval), Operational.
Reason: security-sensitive, high-risk decision.

### Example 5: Upgrade a Third-Party Library

Relevant: Always-on, Dependencies, Testing and Verification, Security and Compliance, Governance, Brownfield.
Reason: external surface change with potential behavior, license, and security impact.

### Example 6: Start a Completely New Greenfield Project

Relevant: Always-on, Greenfield, Architecture, Domain Language, Coding Style, Testing and Verification, Documentation, Dependencies, Governance, Operational.
Reason: a new project sets the long-term shape of the system. Initial decisions — architecture size, conventions, ubiquitous language, test strategy, dependency policy, repo structure — are durable and expensive to change later. The agent must resist premature architecture, record the initial ubiquitous language as it emerges, establish conventions deliberately, and produce only the smallest first vertical slice instead of a full scaffold.
Note: Security and Compliance and DDD are added on demand once the project's domain and risk profile become concrete. Brownfield rules do not apply yet.
