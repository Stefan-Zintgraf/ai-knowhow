# AI Coding Workflow

Version: 0.1  
Purpose: Guide the human and the AI agent from an initial request to a minimal, safe, shared plan before implementation starts.

---

## 1. Core Idea

The workflow exists to prevent premature implementation, oversized plans, and uncontrolled scope expansion.

Before the AI agent creates a detailed plan or changes code, the human and the AI agent must establish a shared understanding of:

1. Where are we now?
2. Where do we want to go?
3. What is the smallest safe next step?

The AI agent should not optimize for the largest or most complete solution. It should help the human narrow the work to the smallest useful and verifiable change.

---

## 2. Guiding Principles

### 2.1 Minimal Safe Progress

The AI agent must prefer a small, reversible, verifiable step over a broad or ambitious plan.

### 2.2 Shared Understanding Before Planning

The AI agent must not jump directly from request to implementation. It must first clarify the current state and the desired target state.

### 2.3 Scope Reduction Is Part of the AI's Job

The AI agent must actively help reduce scope. If the human adds more goals, the AI agent should classify them as:

- needed now
- useful later
- unrelated
- risky and requiring separate planning

The default is to defer additional goals unless they are necessary for correctness or safety.

### 2.4 Evidence Before Assumptions

The AI agent must distinguish between what is known from evidence and what is assumed.

### 2.5 No Silent Expansion

The AI agent must not expand the task into refactoring, redesign, documentation, migration, or cleanup unless explicitly approved.

---

## 3. Workflow Overview

The workflow has five phases:

1. Understand the current state
2. Understand the target state
3. Identify risks and uncertainties
4. Reduce the scope to the smallest useful slice
5. Produce a minimal plan outcome

Implementation may only start after a minimal plan outcome exists.

---

## 4. Phase 1: Understand the Current State

The AI agent should first establish where the project currently stands.

Questions to answer:

- Is this a greenfield or brownfield situation?
- What already exists?
- Which code, modules, interfaces, or workflows are likely involved?
- Which tests, documentation, or examples already exist?
- Which behavior must probably be preserved?
- What is unclear?

For brownfield work, existing behavior must be treated as intentional until proven otherwise.

The AI agent should not assume that strange code is wrong. It may encode legacy behavior, business rules, integration requirements, or operational workarounds.

---

## 5. Phase 2: Understand the Target State

The AI agent should clarify the desired outcome before discussing implementation details.

Questions to answer:

- What should be different after the change?
- What should explicitly stay unchanged?
- What user-visible or developer-visible value should be created?
- What is the minimum result that would be considered successful?
- Are there constraints such as compatibility, performance, safety, or release timing?

The AI agent should challenge vague goals such as:

- make it better
- clean this up
- modernize it
- improve the architecture
- make it robust

Such goals must be translated into observable outcomes.

---

## 6. Phase 3: Identify Risks and Uncertainties

Before creating a plan, the AI agent should identify risks and open questions.

Examples:

- unclear business rules
- missing tests
- public API changes
- database or persistence changes
- security-sensitive logic
- concurrency-sensitive code
- performance-sensitive code
- safety-critical behavior
- legacy behavior that may be intentional
- broad architectural impact

The AI agent should not continue silently when a high-risk decision is required.

---

## 7. Phase 4: Reduce Scope

The AI agent must try to reduce the task to the smallest useful slice.

Questions to ask:

- What can be removed from this plan without losing the core value?
- Can this be split into smaller steps?
- Can we first add tests or characterization before changing behavior?
- Can we avoid touching unrelated modules?
- Can we avoid introducing new abstractions?
- Can we keep behavior unchanged in this iteration?
- What is explicitly out of scope?

Every plan should include a section called `Out of scope`.

---

## 8. Phase 5: Produce a Minimal Plan Outcome

The plan should be short and bounded. It should not become a large design document.

Recommended format:

```text
Goal:
- ...

Current understanding:
- ...

Smallest useful slice:
- ...

Relevant guardrails:
- ...

Files / areas likely touched:
- ...

Out of scope:
- ...

Verification:
- ...

Open decisions:
- ...
```

If the plan cannot fit into this structure, the task is probably too large and should be sliced further.

---

## 9. Greenfield Notes

In greenfield projects, the main risk is premature architecture.

The AI agent should prefer:

- simple structure
- clear names
- explicit boundaries
- easy replacement
- testability
- minimal abstraction

The AI agent should avoid:

- speculative frameworks
- generic plugin systems
- premature DDD complexity
- architecture for imagined future requirements
- excessive documentation before the first useful slice exists

Starter question:

> What is the smallest vertical slice that creates real value and teaches us something about the design?

---

## 10. Brownfield Notes

In brownfield projects, the main risk is breaking hidden intent.

The AI agent should prefer:

- understanding before changing
- behavior preservation
- small diffs
- characterization tests
- compatibility
- rollback-friendly changes

The AI agent should avoid:

- large refactorings mixed with behavior changes
- removing strange-looking code without understanding it
- broad formatting changes
- changing public APIs without approval
- assuming missing documentation means missing intent

Starter question:

> What behavior must remain unchanged, and how can we prove that it remains unchanged?

---

## 11. Anti-Patterns

The AI agent should avoid:

- jumping directly into implementation
- creating a large plan before understanding the current state
- expanding a small request into a redesign
- mixing refactoring and feature work
- introducing abstractions for hypothetical future needs
- producing long documents when a short change contract is enough
- hiding uncertainty
- treating brownfield code as accidental by default

---

## 12. First Starter Examples

### Example 1: Vague Brownfield Request

Request:

> Clean up the order calculation logic.

The AI agent should not immediately refactor. It should first narrow the goal:

```text
Possible smaller slice:
Add characterization tests for the current order calculation behavior before changing the implementation.
```

### Example 2: Vague Greenfield Request

Request:

> Build a flexible architecture for the new reporting module.

The AI agent should challenge the scope:

```text
Possible smaller slice:
Implement one report end-to-end with simple boundaries, then decide which abstractions are actually needed.
```

### Example 3: Expanding Human Request

Request:

> While doing this bug fix, also refactor the module and rename the domain objects.

The AI agent should split the concerns:

```text
Current slice:
Fix and verify the bug.

Later slices:
Refactor module structure.
Rename domain objects after agreeing on terminology.
```
