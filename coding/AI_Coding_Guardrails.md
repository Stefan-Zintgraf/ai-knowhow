# AI Coding Guardrails

Version: 0.1  
Purpose: Define always-on rules and route the AI agent to more specific guardrail documents when they become relevant.

---

## 1. Core Idea

This document is not intended to contain every detailed rule.

It is a compact guardrail index:

- It defines a small starter set of always-on guardrails.
- It lists guardrail categories that may later become separate detailed documents.
- It tells the AI agent when to consult more specific rules.

The AI agent does not need to load every detailed rule for every task. It should load only the rules relevant to the current task.

---

## 2. Always-On Guardrails

The following guardrails apply to every AI-assisted planning or implementation task.

These are starter examples and may be refined later.

---

### 2.1 Minimize Scope

The AI agent must actively narrow the task to the smallest useful and verifiable change.

It must not expand the task unless expansion is necessary for correctness or safety.

---

### 2.2 Do Not Mix Concerns

The AI agent must not combine unrelated work in one change.

Examples of concerns that should usually stay separate:

- feature work
- bug fixing
- refactoring
- formatting
- migration
- documentation cleanup
- dependency upgrades
- architectural redesign

---

### 2.3 Respect Existing Behavior

In brownfield systems, existing behavior must be treated as intentional until proven otherwise.

The AI agent must not remove, simplify, or rewrite strange-looking code without understanding the risk.

---

### 2.4 Make Assumptions Visible

The AI agent must clearly distinguish between:

- facts known from code, tests, documentation, or user input
- assumptions
- open questions

---

### 2.5 Avoid Speculative Design

The AI agent must not introduce abstractions, frameworks, extension points, or generic mechanisms for hypothetical future requirements.

New structure must be justified by the current task.

---

### 2.6 Verify Changes

The AI agent must identify how a change can be verified.

Verification may include:

- unit tests
- integration tests
- characterization tests
- static analysis
- build checks
- manual review
- explicit acceptance criteria

---

### 2.7 Stop on High-Risk Decisions

The AI agent must not silently proceed when the task involves a high-risk decision.

Examples:

- public API changes
- database migrations
- security-sensitive code
- authentication or authorization logic
- safety-critical behavior
- concurrency-sensitive code
- broad architecture changes
- unclear business invariants
- removal of legacy behavior

---

## 3. Guardrail Categories

The following categories may later become separate detailed documents.

At this stage, they are placeholders and routing categories.

---

### 3.1 Architecture Rules

Use when the task touches:

- module boundaries
- layering
- dependencies
- public APIs
- shared libraries
- service boundaries
- architectural patterns
- infrastructure/domain separation

Possible future document:

```text
Architecture_Rules.md
```

---

### 3.2 Domain and Ubiquitous Language Rules

Use when the task touches:

- business terms
- domain concepts
- naming of domain objects
- terminology changes
- business rules
- user-facing concepts
- cross-team language consistency

Possible future document:

```text
Domain_Language_Rules.md
```

---

### 3.3 DDD Rules

Use when the task touches:

- bounded contexts
- aggregates
- entities
- value objects
- domain services
- application services
- invariants
- domain events

Possible future document:

```text
DDD_Rules.md
```

---

### 3.4 Coding Style and Conventions

Use for implementation tasks that involve code changes.

Topics may include:

- formatting
- naming
- error handling
- logging
- comments
- file organization
- language-specific idioms
- dependency usage

Possible future document:

```text
Coding_Style_Rules.md
```

---

### 3.5 Testing and Verification Rules

Use when the task touches:

- behavior changes
- bug fixes
- refactorings
- legacy code
- public APIs
- regression risk
- acceptance criteria

Possible future document:

```text
Testing_Verification_Rules.md
```

---

### 3.6 Security and Compliance Rules

Use when the task touches:

- authentication
- authorization
- secrets
- input validation
- external interfaces
- cryptography
- permissions
- logging of sensitive data
- dependency security
- compliance requirements

Possible future document:

```text
Security_Compliance_Rules.md
```

---

### 3.7 Brownfield Change Rules

Use when the task touches an existing codebase, existing behavior, production code, or legacy logic.

Topics may include:

- behavior preservation
- characterization tests
- hidden invariants
- compatibility
- rollback
- small diffs
- avoiding opportunistic cleanup

Possible future document:

```text
Brownfield_Change_Rules.md
```

---

### 3.8 Greenfield Design Rules

Use when the task creates a new project, service, module, or major component.

Topics may include:

- simplest useful architecture
- first vertical slice
- postponed decisions
- initial conventions
- avoiding premature abstraction

Possible future document:

```text
Greenfield_Design_Rules.md
```

---

### 3.9 Documentation Rules

Use when the task creates or changes documentation.

Topics may include:

- concise documentation
- durable decisions
- examples
- API documentation
- comments
- avoiding redundant generated docs

Possible future document:

```text
Documentation_Rules.md
```

---

## 4. Routing Rule

Before detailed planning or implementation, the AI agent should identify which guardrail categories are relevant.

Recommended format:

```text
Relevant guardrails:
- Always-on guardrails
- Testing and Verification Rules, because the task changes behavior
- Brownfield Change Rules, because existing production code is affected
```

The AI agent should not load every detailed guardrail document by default.

When unsure whether a guardrail category applies, the AI agent should mention the uncertainty and choose the smallest reasonable set of relevant guardrails.

---

## 5. Conflict Resolution

If guardrails conflict, use this priority order:

1. Safety, security, and compliance
2. Correctness and behavior preservation
3. Architecture and domain integrity
4. Testability and maintainability
5. Consistency with coding style
6. Convenience or implementation speed

The AI agent must not use speed as a reason to bypass safety, correctness, or explicit boundaries.

---

## 6. Anti-Patterns

The AI agent should avoid:

- reading all detailed rules when only a small subset is relevant
- ignoring relevant rules because they were not explicitly repeated by the human
- applying architecture rules mechanically without considering the current task
- turning a small change into a broad redesign
- treating guardrails as optional suggestions
- hiding assumptions or uncertainty
- introducing new abstractions without current need
- changing behavior as a side effect of cleanup

---

## 7. First Starter Examples

### Example 1: Bug Fix in Existing Code

Relevant guardrails:

```text
- Always-on guardrails
- Brownfield Change Rules
- Testing and Verification Rules
- Coding Style and Conventions
```

Reason:

The task affects existing behavior and may introduce regression risk.

---

### Example 2: New Module in a Greenfield Project

Relevant guardrails:

```text
- Always-on guardrails
- Greenfield Design Rules
- Architecture Rules
- Coding Style and Conventions
- Testing and Verification Rules
```

Reason:

The task creates new structure and should avoid premature abstraction.

---

### Example 3: Rename a Business Concept

Relevant guardrails:

```text
- Always-on guardrails
- Domain and Ubiquitous Language Rules
- DDD Rules, if the concept is part of the domain model
- Brownfield Change Rules, if existing code is changed
- Testing and Verification Rules
```

Reason:

Renaming a business concept can affect language consistency, behavior, APIs, documentation, and tests.

---

### Example 4: Authentication Change

Relevant guardrails:

```text
- Always-on guardrails
- Security and Compliance Rules
- Testing and Verification Rules
- Architecture Rules, if boundaries or public interfaces change
```

Reason:

Authentication changes are security-sensitive and require explicit verification.
