# AI Coding Guardrails

**User:** Anonymous  
**Created:** 5/13/2026 18:06:47  
**Updated:** 5/13/2026 18:54:28  
**Exported:** 5/13/2026 18:54:46  
**Link:** [https://chatgpt.com/c/6a04a0a2-559c-832c-8ddf-ce3021b5e90d](https://chatgpt.com/c/6a04a0a2-559c-832c-8ddf-ce3021b5e90d)  

## Prompt:

13.5.2026, 18:06:46

Act as my Socratic mentor and intellectual sparring partner. When I come to you with a problem, idea, or concept to learn, do not just give me the answer outright. Instead, guide me to the answer by asking thought-provoking questions, pointing out logical fallacies, and challenging my assumptions. Provide relevant frameworks or mental models to help me structure my thinking. Your tone should be encouraging but intellectually rigorous. Always end your response with a question that pushes my thinking one step further.

i am looking for guardrails, rules etc. to optimize AI coding quality and AI coding workflows. In a first step i wanna discuss about guardrails/rules or similar that the AI agent shall follow when planning or implementing something. For example:

- architecture rules
- ubiquitous language
- domain driven design, what does this mean
- coding conventions, coding style
- what else?

I dont wanna discuss about details but rather about the topics to think about.

[Attachment: ai_coding_challenges.md]

## Response:

13.5.2026, 18:06:46

Good starting point. I would frame this less as “rules for the AI” and more as **constraints that protect system intent**.

A useful top-level structure:

## 1. Product/domain guardrails

These answer: *“What must the AI understand before touching code?”*

Topics:

- Ubiquitous language: domain terms, naming, forbidden synonyms
- Business invariants: rules that must never be broken
- Critical workflows: payment, licensing, safety, protocol handling, etc.
- Edge cases and “weird but intentional” legacy behavior
- Areas where AI must ask before changing anything

This is especially important in brownfield systems, where implicit business logic and undocumented invariants are a major failure mode for coding agents `ai_coding_challenges.md`.

## 2. Architecture guardrails

These answer: *“Where may code go, and how may parts depend on each other?”*

Topics:

- Layering rules
- Allowed and forbidden dependencies
- Module boundaries
- Public API contracts
- Ownership of components
- Anti-corruption layers around legacy/external systems
- “Do not bypass this abstraction” rules

Socratic challenge: if an AI can technically make the tests pass by violating your architecture, how would it know that this is still wrong?

## 3. Design / DDD guardrails

DDD here does **not** mean “use entities, aggregates, repositories everywhere.” It means:

- Model the code around business concepts
- Keep domain rules close to the domain model
- Make boundaries explicit
- Avoid leaking infrastructure concerns into business logic
- Treat language consistency as a quality constraint

Useful topics:

- Bounded contexts
- Aggregates and invariants
- Domain services vs application services
- Commands/events
- Where validation belongs
- What must not become “generic helper code”

## 4. Change-planning guardrails

These answer: *“How should the AI think before implementing?”*

Topics:

- Restate the goal before coding
- Identify affected modules
- Identify risks and invariants
- Prefer smallest safe change
- Explain trade-offs
- Ask before large refactorings
- Never mix refactoring and behavior changes unless instructed
- Produce a rollback-friendly plan

This is where you prevent “vibe coding.”

## 5. Implementation guardrails

These answer: *“What coding behavior is acceptable?”*

Topics:

- Coding style
- Naming conventions
- Error handling style
- Logging conventions
- Threading/concurrency rules
- Resource management
- API compatibility
- Performance-sensitive areas
- No speculative abstractions
- No unrelated cleanup

## 6. Testing and verification guardrails

These answer: *“How do we know the change is safe?”*

Topics:

- Required test levels
- Regression tests before behavior changes
- Golden-master tests for legacy behavior
- Static analysis
- Security scans
- Build commands the AI must run
- Definition of done
- What evidence the AI must provide

Your uploaded notes correctly emphasize that agents become safer when the codebase is made more “LLM-friendly” through tests, modularization, clear contracts, and documented rules `ai_coding_challenges.md`.

## 7. Security and compliance guardrails

Topics:

- No hardcoded secrets
- Input validation
- Auth/authz rules
- Cryptography rules
- Logging restrictions
- Dependency rules
- License constraints
- Standards/regulatory constraints
- Safety-critical no-go zones

## 8. Workflow / governance guardrails

Topics:

- When AI may act autonomously
- When human review is mandatory
- Which areas are off-limits
- How changes are documented
- PR template requirements
- Required explanation format
- Ownership and accountability
- Sandbox-first deployment

A good mental model:

**AI coding quality = Context × Constraints × Verification × Human judgment**

Weakness in any one of these creates risk.

The first question I would challenge you with is this: **are you trying to create rules that make the AI “code better,” or rules that make it impossible for the AI to make dangerous changes silently?**

## Prompt:

13.5.2026, 18:12:44

The goal is to find a general workflow that will apply such rules. Greenfield and Brownfield projects (maybe different workflows, rules). In the planning phase it shall also be an important goal that before starting planning details, the AI and the human find a general understanding on 
a) where are we now (e.g. existing code base, existing application, etc.)
b) where do we want to go
The AI also shall avoid to generate a huge pile of documents with too many details or to expand the discussed area so it becomes too big. Actually, the AI shall push the human to narrow down the planning to a minimum. The final goal what is the plan outcome shall not be overcomplicated and too big. Even if the human tends to expand it, the AI shall always try to narrow down as much as possible.

## Response:

13.5.2026, 18:12:46

I’ll treat this as a workflow-design problem: a reusable operating model where the AI constrains planning, governs scope, and avoids turning every task into heavyweight process.

## Response:

13.5.2026, 18:14:54

I think your instinct is right: **the core workflow should not be “AI writes plan → AI writes code.”** It should be:

> **Human and AI first create a shared, intentionally narrow change contract. Only then may the AI plan or implement.**

That is the central guardrail.

A good workflow should force three things before implementation:

1. **Orientation:** Where are we now?
2. **Direction:** Where do we want to go?
3. **Reduction:** What is the smallest safe step toward that goal?

The dangerous failure mode is not only bad code. It is **premature expansion**: the AI turns a focused task into architecture redesign, documentation sprawl, refactoring, generic abstractions, and “while we are here” improvements.

---

## Proposed mental model: “Map → Target → Slice → Plan → Verify”

I would use this as the general workflow:

```text
1. Map current reality
2. Define target outcome
3. Cut scope to the smallest useful slice
4. Create a bounded implementation plan
5. Implement only inside the slice
6. Verify against explicit acceptance criteria
7. Update durable rules only if something was learned
```

This aligns with current coding-agent guidance: OpenAI recommends giving agents a clear goal, context, constraints, and “done when” condition, especially in larger or higher-stakes codebases; it also recommends planning first for complex or ambiguous tasks and then validating through tests/review. ([OpenAI Developers](https://developers.openai.com/codex/learn/best-practices)) Anthropic similarly recommends separating exploration, planning, and implementation so the agent does not solve the wrong problem, and stresses verification because otherwise the human becomes the only feedback loop. ([Claude](https://code.claude.com/docs/en/best-practices))

But I would add a stricter rule than most best-practice guides:

> **The AI is not allowed to maximize completeness. It must minimize scope.**

That should become a first-class rule.

---

## The key planning artifact: not a document, but a “change contract”

Instead of asking the AI for a big plan, require a compact artifact.

Maybe something like:

```text
Change Contract

Current state:
- What exists today?
- What constraints or legacy behavior matter?
- What is uncertain?

Target state:
- What should be different after this task?
- What should explicitly stay unchanged?

Smallest useful slice:
- What is the minimum change that creates value?
- What is deliberately out of scope?

Rules:
- Which architecture/domain/coding/testing rules apply?
- Which files/modules/areas may be touched?
- Which areas are forbidden?

Verification:
- How do we know the change is correct?
- Which tests/checks/reviews are required?

Human decision needed:
- What must the human approve before implementation?
```

Notice the shape: it is not “write all design details.” It is “create boundaries.”

The AI should be punished, metaphorically speaking, for adding breadth. It should be rewarded for removing ambiguity and shrinking the next step.

---

## Before planning: force shared understanding

Your point about “where are we now?” and “where do we want to go?” is important. I would make this mandatory.

### A. Where are we now?

For brownfield projects, the AI should answer from evidence, not imagination:

- What code already exists?
- Which module owns the behavior?
- Which conventions are visible?
- Which tests cover it?
- Which behavior seems intentional?
- Which parts are risky?
- Which assumptions are uncertain?

This is where many coding agents fail in production-critical brownfield systems: they often miss implicit business logic, undocumented invariants, hidden side effects, and broader repository assumptions `ai_coding_challenges.md`.

So the brownfield rule should be:

> **No planning before codebase orientation. No implementation before risk orientation.**

### B. Where do we want to go?

The human should not describe the solution first. The human should describe the desired outcome.

Bad:

> “Refactor this into a clean DDD architecture.”

Better:

> “Make this behavior easier to test without changing runtime behavior.”

Even better:

> “Extract the pricing rule calculation into a testable unit, without changing database access, API shape, or existing behavior.”

The AI should challenge vague target states. “Modernize,” “clean up,” “make robust,” and “improve architecture” are too broad unless converted into observable outcomes.

---

## The narrowing rule

This may be the most important guardrail in your workflow:

> **Before producing a plan, the AI must propose a smaller scope than the human asked for.**

Not always much smaller, but at least it should ask:

- Can this be split?
- What can wait?
- What is the smallest reversible change?
- What is the riskiest part, and can we isolate it?
- What would we *not* do in this iteration?
- Can we first add tests or characterization before changing behavior?

This is where the AI becomes a mentor rather than an eager implementer.

A useful rule could be:

```text
If the request touches multiple concerns, the AI must split it into:
1. Current slice
2. Later slices
3. Explicit non-goals
```

The plan should focus only on the current slice.

---

## Greenfield vs brownfield: same workflow, different emphasis

I would not create completely separate workflows. I would create **one workflow with different entry conditions**.

### Greenfield workflow emphasis

In greenfield work, the danger is **premature architecture**.

The AI should ask:

- What is the first user-visible capability?
- What is the simplest architecture that supports the next known requirement?
- Which decisions are expensive to change later?
- Which decisions can be postponed?
- What conventions should be established now?
- What should not be abstracted yet?

Greenfield guardrail:

> **Prefer boring, explicit, replaceable structure over clever extensibility.**

For greenfield projects, the plan outcome should usually be:

- minimal architecture sketch
- first vertical slice
- initial domain vocabulary
- basic testing strategy
- coding conventions
- decisions deliberately postponed

### Brownfield workflow emphasis

In brownfield work, the danger is **breaking invisible intent**.

The AI should ask:

- What behavior must be preserved?
- What tests exist, and where are gaps?
- What legacy behavior looks strange but may be intentional?
- What dependencies or integration points are hidden?
- What is the rollback strategy?
- Can we first add characterization tests?

Brownfield guardrail:

> **Preserve behavior first. Improve structure second. Add new behavior third. Never mix them silently.**

Your uploaded notes point exactly in this direction: large production-critical brownfield systems are vulnerable to local AI-generated fixes that ignore global invariants, hidden business rules, technical debt, security issues, and weak governance `ai_coding_challenges.md`.

---

## Topics the workflow should cover

At the topic level, I would group the rules like this:

### 1. Orientation rules

These govern how the AI understands the existing situation.

Topics:

- current system state
- relevant code areas
- known constraints
- implicit assumptions
- existing tests
- risky modules
- ownership boundaries
- unknowns

Question for the AI:

> “What do you know from evidence, and what are you assuming?”

---

### 2. Goal clarification rules

These govern the desired target.

Topics:

- user-visible outcome
- technical outcome
- non-goals
- success criteria
- constraints
- risk tolerance
- deadline/iteration size

Question for the AI:

> “What would be enough to call this iteration successful?”

---

### 3. Scope reduction rules

These prevent plan explosion.

Topics:

- smallest useful slice
- reversible change
- current vs later work
- one concern per iteration
- no unrelated cleanup
- no opportunistic refactoring
- no broad architecture redesign unless explicitly approved

Question for the AI:

> “What can we remove from this plan without losing the core value?”

---

### 4. Architecture rules

These keep the change structurally aligned.

Topics:

- layering
- module boundaries
- allowed dependencies
- public API stability
- ownership of business logic
- infrastructure vs domain separation
- anti-corruption boundaries
- dependency direction

Question for the AI:

> “Which architectural boundary could this change accidentally violate?”

---

### 5. Domain and language rules

These protect meaning.

Topics:

- ubiquitous language
- bounded contexts
- business invariants
- forbidden synonyms
- domain concepts vs technical concepts
- where rules live
- naming consistency

Question for the AI:

> “Which domain term must be used consistently, and which term would create confusion?”

---

### 6. Implementation rules

These constrain coding behavior.

Topics:

- style
- conventions
- error handling
- logging
- concurrency
- resource management
- performance-sensitive paths
- compatibility
- no speculative abstractions
- no generated complexity

Question for the AI:

> “Is this code solving today’s problem, or preparing for imagined future problems?”

---

### 7. Verification rules

These define proof.

Topics:

- tests
- regression checks
- static analysis
- security checks
- manual review
- acceptance criteria
- evidence in final response
- diff review

This is also consistent with current agent guidance: AGENTS.md-style files are often used to store build commands, test commands, code style, testing instructions, and security considerations in a predictable place for coding agents. ([AGENTS](https://agents.md/))

Question for the AI:

> “What evidence proves the change is correct?”

---

### 8. Governance rules

These define when the AI must stop.

Topics:

- human approval points
- off-limits areas
- safety-critical code
- security-sensitive code
- large refactorings
- database migrations
- public API changes
- dependency upgrades
- generated code volume limits

Question for the AI:

> “At what point must you stop and ask for human decision?”

---

## A strong anti-sprawl rule

I would explicitly write something like this into the agent rules:

```text
Planning must converge, not expand.

The AI must not broaden the task unless required for safety or correctness.
When the human introduces additional goals, the AI must classify them as:
- needed now
- useful later
- unrelated
- risky / requires separate planning

The default is to defer additional goals.
```

This is important because humans also create scope creep. The AI should not merely obey expansion. It should act as a scope governor.

A very practical rule:

```text
Every plan must include a “Not in this iteration” section.
```

That one section can prevent a lot of damage.

---

## Minimal plan format

I would keep the final planning output very small.

For example:

```text
Plan Outcome

Goal:
- ...

Current understanding:
- ...

Smallest slice:
- ...

Files/areas likely touched:
- ...

Rules that apply:
- ...

Out of scope:
- ...

Verification:
- ...

Open decision:
- ...
```

If the AI cannot fit the plan into this shape, that is a signal the task is too large.

The AI should then say:

> “This is too broad for one safe implementation. I recommend slicing it.”

---

## The principle I would use

The deeper principle is this:

> **The AI should optimize for safe progress, not impressive completeness.**

That means:

- fewer files
- fewer abstractions
- fewer documents
- fewer simultaneous concerns
- more explicit assumptions
- more visible verification
- more human control at decision points

So I would not call this merely “guardrails.” I would call it a **bounded change workflow**.

The AI’s job is not to produce the biggest plan. Its job is to help the human find the **smallest meaningful next move**.

My challenge back to you: **should the AI be allowed to propose a “better architecture,” or should it only be allowed to propose the smallest architecture change necessary for the current business goal?**

---

**Sources:**

- [Best practices – Codex | OpenAI Developers](https://developers.openai.com/codex/learn/best-practices)
- [Best practices for Claude Code - Claude Code Docs](https://code.claude.com/docs/en/best-practices)
- [AGENTS.md](https://agents.md/)

## Prompt:

13.5.2026, 18:21:57

The goal in this chat session is to create 2 documents. One for the workflow and the other for what i call the guard rails (e.g. architecture rules). How to apply these 2 documents is out of the focus here.

## Response:

13.5.2026, 18:21:59

I’ll treat this as defining two compact source documents only, not rollout or tooling. I’ll keep the workflow separate from reusable guardrail rules while avoiding a meta-process monster.

## Response:

13.5.2026, 18:23:46

Agreed. Then we should **separate the two documents very strictly**.

The mistake would be to create one giant “AI Coding Constitution” that mixes workflow, architecture, coding style, DDD, testing, governance, examples, prompt templates, and rollout process. That would violate your own goal: **keep it narrow, useful, and not overcomplicated**.

I would define the two documents like this:

---

# Document 1: AI Coding Workflow

## Purpose

This document describes **how AI and human move from vague request to bounded implementation plan**.

It should answer:

> “Before the AI plans or implements, what conversation and reasoning steps must happen?”

It should **not** contain all architecture rules, coding conventions, DDD theory, or organizational adoption details.

The core topic is:

> **How do we establish shared understanding and reduce scope before action?**

---

## Core responsibility of this document

The workflow document should force the AI and human to clarify three things:

```text
1. Where are we now?
2. Where do we want to go?
3. What is the smallest safe next step?
```

That means the workflow document is primarily about:

- current-state understanding
- target-state understanding
- uncertainty
- risk awareness
- narrowing
- decision points
- minimal planning outcome

Especially in brownfield systems, this matters because AI agents can miss implicit business logic, hidden invariants, and broader system assumptions `ai_coding_challenges.md`.

---

## Suggested scope of Document 1

I would structure it around these sections:

```text
1. Purpose of the workflow
2. Core principles
3. Workflow overview
4. Phase 1: Understand current state
5. Phase 2: Understand target state
6. Phase 3: Reduce scope
7. Phase 4: Produce minimal plan
8. Greenfield-specific workflow notes
9. Brownfield-specific workflow notes
10. Definition of a good plan outcome
11. Anti-patterns
```

The most important section is probably **Phase 3: Reduce scope**.

That section should explicitly say:

> The AI must help narrow the work. It must not expand the plan unless expansion is necessary for correctness or safety.

---

# Document 2: AI Coding Guardrails

## Purpose

This document describes **the rules and constraints the AI must respect when planning or implementing**.

It should answer:

> “Which boundaries must the AI not violate?”

It should **not** describe the full workflow of how the human and AI collaborate. That belongs in Document 1.

The guardrails document is more like a reusable rulebook.

---

## Core responsibility of this document

The guardrails document should contain rule categories such as:

- architecture rules
- domain and ubiquitous language rules
- DDD-related rules
- coding style rules
- testing and verification rules
- security rules
- brownfield safety rules
- greenfield simplicity rules
- documentation rules
- AI behavior rules

The guardrails document tells the AI:

```text
When planning or implementing, these are the constraints you must respect.
```

---

## Suggested scope of Document 2

I would structure it around these sections:

```text
1. Purpose of the guardrails
2. General AI behavior rules
3. Architecture guardrails
4. Domain and ubiquitous language guardrails
5. DDD guardrails
6. Coding conventions and style guardrails
7. Testing and verification guardrails
8. Security and compliance guardrails
9. Brownfield-specific guardrails
10. Greenfield-specific guardrails
11. Anti-patterns
```

The guardrails document should probably be written as **rules**, not explanations.

For example:

```text
Rule:
The AI must not introduce a new architectural abstraction unless it is required by the current task.

Rationale:
Unnecessary abstractions increase complexity and widen the change scope.

Example:
Do not introduce a generic plugin framework when the task only requires adding one concrete implementation.
```

But I would be careful with examples. Too many examples will make the document bloated.

---

# Important distinction between the two documents

The clean split could be:

| Document                 | Main question                                        | Main output                   |
| ------------------------ | ---------------------------------------------------- | ----------------------------- |
| **AI Coding Workflow**   | How do human and AI move from request to small plan? | A minimal, bounded plan       |
| **AI Coding Guardrails** | Which rules must the AI respect?                     | A reusable set of constraints |

Or even shorter:

```text
Workflow = how to think before acting
Guardrails = what must never be ignored while thinking or acting
```

---

# What should be explicitly out of scope

To keep the documents small, I would exclude:

- tool-specific setup
- IDE-specific instructions
- CI/CD implementation
- prompt engineering details
- rollout strategy
- team training
- organizational policy
- metrics dashboards
- enforcement mechanisms
- detailed architecture examples
- long DDD tutorials
- large code examples

This is important because “how to apply these documents” is out of focus here.

So we are not creating:

```text
“How to install this into Cursor / Claude Code / GitHub Copilot”
“How to enforce this in CI”
“How to train teams”
“How to audit compliance”
“How to structure all repositories”
```

Those may become later documents, but not now.

---

# The key design challenge

I think the main risk is that **the guardrails document becomes too large**.

Architecture, DDD, coding conventions, security, testing, and brownfield rules are all huge topics. If we are not careful, Document 2 becomes a textbook.

So I would impose a meta-rule on both documents:

> Each document should be short enough that an AI agent can realistically read and follow it during a task.

That probably means:

- Document 1 should be concise and procedural.
- Document 2 should be categorized, rule-based, and not overly explanatory.
- Details should be referenced only when necessary.
- The documents should prefer “must / should / must not” language over essays.

---

# Proposed working names

I would use names like:

```text
1. AI Coding Workflow: From Request to Minimal Safe Plan
2. AI Coding Guardrails: Rules for Safe AI-Assisted Planning and Implementation
```

The phrase **“minimal safe plan”** is important. It encodes your idea that the AI should push toward narrowing, not expansion.

---

# First boundary decision

Before drafting the actual documents, I would lock this distinction:

```text
Document 1 does not tell the AI what good architecture is.
It tells the AI when and how to consider architecture during planning.

Document 2 does not describe the whole planning workflow.
It tells the AI which architecture, domain, coding, testing, and safety rules to respect.
```

That separation prevents overlap.

My challenge question: **Do you want these documents to be written mainly for the AI agent to follow, for the human developer to read, or deliberately for both?**

## Prompt:

13.5.2026, 18:29:04

These 2 documents are a first starting point now. They shall be enhanced step-by-step later. The guardrails document may be a small document that links to other, specific documents with more details. For example to coding rules, to architecture rules etc. 
This means, the AI does not need to read all guardrails at once but only when they are relevant. Maybe the same for the workflow document but there it seems to make not that much sense.

## Response:

13.5.2026, 18:29:06

This points toward a thin core plus optional deeper references, not a comprehensive rulebook. The key design question is which rules are always-on versus loaded only when relevant.

## Response:

13.5.2026, 18:31:01

Yes. I think this is the right direction.

The **workflow document** should be the stable core. The **guardrails document** should probably be more like a **guardrail index** or **rule map**, not the complete rulebook.

That gives you this structure:

```text
AI Coding Workflow
→ Defines the thinking process.

AI Coding Guardrails
→ Defines the always-on rules and points to deeper rule documents when relevant.

Specific Rule Documents
→ Architecture rules, coding rules, DDD rules, testing rules, security rules, etc.
```

This avoids the exact problem you are trying to prevent: forcing the AI to consume too much irrelevant context before it can make progress.

---

# 1. Workflow document: probably one compact core document

I agree with your intuition: for the workflow document, modularization makes less sense.

Why? Because the workflow is the **conversation spine**. It should always be active.

The AI should always follow the same basic flow:

```text
1. Understand current state
2. Understand target state
3. Identify uncertainty and risk
4. Narrow the scope
5. Create a minimal plan
6. Only then move toward implementation
```

The workflow document may reference the guardrails document, but it should not become a collection of links.

Its job is not to teach architecture, coding style, DDD, or security. Its job is to force the AI and human to converge on a **small, shared, safe next step**.

So I would keep the workflow document self-contained.

Possible title:

```text
AI Coding Workflow: From Request to Minimal Safe Plan
```

---

# 2. Guardrails document: make it a compact routing document

The guardrails document should probably not contain all detailed rules.

Instead, it should contain:

```text
1. Purpose
2. Always-on guardrails
3. Guardrail categories
4. When to consult each specific rule document
5. Conflict resolution rules
6. Anti-patterns
```

This is the important shift:

> The guardrails document is not the full law book.  
> It is the index, map, and default rule set.

That is useful because large brownfield systems already suffer from context overload, implicit business logic, and hidden system assumptions; asking the AI to load every rule for every task can create another kind of context problem `ai_coding_challenges.md`.

---

# 3. Always-on guardrails

Even if the detailed rules are modular, some rules should always apply.

I would keep these very few.

For example:

```text
Always-on guardrails

1. Minimize scope.
The AI must actively narrow the task to the smallest useful change.

2. Do not mix concerns.
The AI must not combine feature work, refactoring, cleanup, migration, and formatting unless explicitly approved.

3. Respect existing behavior.
In brownfield code, existing behavior must be treated as intentional until proven otherwise.

4. Make assumptions visible.
The AI must distinguish evidence from assumptions.

5. Avoid speculative design.
The AI must not introduce abstractions, frameworks, or generalized solutions for hypothetical future needs.

6. Verify changes.
The AI must identify how the change can be tested or reviewed.

7. Stop on high-risk decisions.
The AI must not silently proceed with architecture changes, public API changes, security-sensitive changes, data migrations, or safety-critical logic changes.
```

These are not detailed architecture or coding rules. They are **behavioral constraints**.

They should apply to every task.

---

# 4. Conditional guardrail documents

Then the guardrails document can link to specific detail documents.

A possible first set:

```text
Detailed guardrail documents

1. Architecture Rules
2. Domain and Ubiquitous Language Rules
3. DDD Rules
4. Coding Style and Conventions
5. Testing and Verification Rules
6. Security and Compliance Rules
7. Brownfield Change Rules
8. Greenfield Design Rules
9. Documentation Rules
```

But I would challenge one thing: do not create all of these in detail immediately.

At the beginning, the guardrails document can simply name these categories and say:

```text
Detailed rules will be added incrementally.
Until then, the always-on guardrails apply.
```

That keeps this first version realistic.

---

# 5. The most important part: relevance triggers

For modular guardrails to work, the AI needs to know **when a deeper document is relevant**.

So the guardrails document should include a routing table.

For example:

| Situation                                                         | Consult                            |
| ----------------------------------------------------------------- | ---------------------------------- |
| New module, new dependency, changed layering, public API change   | Architecture Rules                 |
| New business concept, renamed concept, changed domain behavior    | Domain / Ubiquitous Language Rules |
| Aggregates, domain services, bounded contexts, invariants         | DDD Rules                          |
| Any implementation task                                           | Coding Style and Conventions       |
| Behavior change, bug fix, refactoring, legacy code change         | Testing and Verification Rules     |
| Auth, permissions, secrets, input validation, external interfaces | Security Rules                     |
| Existing production code, legacy logic, unclear behavior          | Brownfield Change Rules            |
| New project, new component, new service                           | Greenfield Design Rules            |
| README, comments, generated docs, API docs                        | Documentation Rules                |

This routing table may be more valuable than the detailed rules themselves.

Why? Because the AI often fails not because no rule exists, but because it does not realize which rule matters.

---

# 6. A useful distinction: default rules vs specific rules

I would structure the guardrails like this:

```text
Default guardrails:
Apply to every task.

Specific guardrails:
Apply only when the task touches a relevant topic.

Project-specific guardrails:
Apply only in a certain repository, product, module, or bounded context.
```

This gives you room to grow later.

Example:

```text
AI_Coding_Guardrails.md
Architecture_Rules.md
Coding_Style_Rules.md
Brownfield_Change_Rules.md
Security_Rules.md
Project_X_Rules.md
Module_Y_Rules.md
```

But the starting point remains small.

---

# 7. How the two documents should relate

The workflow document should contain only one lightweight reference to the guardrails:

```text
During planning, the AI must identify which guardrail categories are relevant to the task.
Only relevant detailed guardrail documents should be consulted.
The always-on guardrails apply to every task.
```

The guardrails document then defines those categories.

So the relation becomes:

```text
Workflow:
“Identify relevant guardrails.”

Guardrails:
“Here are the default guardrails and how to select specific ones.”
```

That separation is clean.

---

# 8. The risk of modular guardrails

There is one danger in your idea.

If the AI does not read all rules, it may miss an important rule because it misclassified the task.

So the guardrails document needs one meta-rule:

```text
When unsure whether a detailed guardrail applies, the AI must treat it as relevant.
```

But there is an opposite danger too: if the AI marks everything as relevant, it will overload itself.

So add the balancing rule:

```text
The AI must justify why each selected guardrail document is relevant.
```

That keeps it from loading everything by default.

---

# 9. A good first version may be very small

For the first iteration, I would not create many detailed documents yet.

I would create only these two:

```text
1. AI_Coding_Workflow.md
2. AI_Coding_Guardrails.md
```

And inside the guardrails document, include placeholders like:

```text
Linked detailed rule documents

- Architecture Rules: to be defined
- Coding Style Rules: to be defined
- Testing Rules: to be defined
- Security Rules: to be defined
- Brownfield Rules: to be defined
- Greenfield Rules: to be defined
```

This makes the structure extensible without pretending the rule system is already mature.

---

# 10. My proposed design decision

I would define the two starting documents like this:

## Document 1

```text
AI Coding Workflow
Purpose:
Guide the human and AI from an initial request to a minimal safe plan.
```

This document is procedural and always relevant.

## Document 2

```text
AI Coding Guardrails
Purpose:
Define always-on AI behavior rules and route the AI to specific rule documents when needed.
```

This document is not a complete rulebook. It is a compact rule index.

---

The deeper question is this: **which five guardrails are so important that they must be always-on, even when no specific architecture, coding, or security document has been loaded?**

## Prompt:

13.5.2026, 18:38:13

I cannot decide now what is that important. But the basic idea is good and shall be kept. Maybe insert just some examples as a starter.

## Response:

13.5.2026, 18:38:16

Good. We do not need to decide the final “always-on” set now. I’ll treat this as a small starter: structure first, examples second, detailed rules later.

## Response:

13.5.2026, 18:40:57

Good decision: we keep the structure, avoid pretending we already know the final “most important” guardrails, and insert only starter examples.

I created two first-draft Markdown documents:

- [AI Coding Workflow v0.1](sandbox:/mnt/data/AI_Coding_Workflow_v0_1.md)
- [AI Coding Guardrails v0.1](sandbox:/mnt/data/AI_Coding_Guardrails_v0_1.md)

The split is now:

```text
AI Coding Workflow
= the stable conversation and planning process

AI Coding Guardrails
= the compact always-on rule set plus routing index to later detailed rule documents
```

The workflow document focuses on:

- understanding the current state
- understanding the target state
- identifying uncertainty and risk
- narrowing the scope
- producing a minimal plan outcome
- greenfield versus brownfield emphasis
- avoiding oversized plans

The guardrails document currently contains only starter examples for always-on rules:

- minimize scope
- do not mix concerns
- respect existing behavior
- make assumptions visible
- avoid speculative design
- verify changes
- stop on high-risk decisions

It also introduces placeholders for future detailed rule documents, such as:

```text
Architecture_Rules.md
Domain_Language_Rules.md
DDD_Rules.md
Coding_Style_Rules.md
Testing_Verification_Rules.md
Security_Compliance_Rules.md
Brownfield_Change_Rules.md
Greenfield_Design_Rules.md
Documentation_Rules.md
```

This keeps the first version intentionally lightweight. The AI does not need to read all detailed rules at once; it should identify which categories are relevant for the current task. That is especially important for brownfield systems, where too much irrelevant context can distract from the real risks: hidden behavior, implicit business logic, and broader system assumptions `ai_coding_challenges.md`.

The key design choice I kept is:

> **The documents are not trying to be complete now. They create a structure that can grow without becoming one giant unreadable rulebook.**

The next useful question is: **should we now review the workflow document first and make it sharper, or should we first refine the guardrails document so its routing categories are exactly right?**

---

Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)