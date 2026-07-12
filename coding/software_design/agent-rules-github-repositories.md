# Agent-Rules / Agent-Skills GitHub Repositories for Software Design

This document surveys GitHub repositories that package software design methods — books, Domain-Driven Design, Clean Architecture, refactoring — as rules or skills for coding agents (Claude Code, Cursor, GitHub Copilot, Codex, Windsurf, and others).

Repositories are grouped by category and, within each category, ordered by relevance and depth to the software design methods covered in [software_design.md](./software_design.md) and [strategic_tactical_design.md](./strategic_tactical_design.md) — not by popularity metrics such as GitHub stars, which are a noisy signal for a fast-moving, months-old ecosystem like agent skills and go stale quickly.

Terms used throughout this document are defined in [glossary.md](./glossary.md). Each repository entry below ends with a **Software design methods referenced** line naming the concepts it covers, so the two companion documents ([software_design.md](./software_design.md) and [strategic_tactical_design.md](./strategic_tactical_design.md)) can be cross-linked accordingly.

## Table of Contents

- [Book-Distilled Rule Sets](#book-distilled-rule-sets)
  1. [ciembor/agent-rules-books](#ciembor-agent-rules-books)
  2. [ZLStas/skills](#zlstas-skills)
  3. [addyosmani/agent-skills](#addyosmani-agent-skills)
- [Domain-Driven Design–Focused](#domain-driven-designfocused)
  4. [ForceInjection/domain-driven-design-skills](#forceinjection-domain-driven-design-skills)
  5. [zudochkin/go-clean-ddd-skill](#zudochkin-go-clean-ddd-skill)
- [Clean Architecture–Focused](#clean-architecturefocused)
  6. [nathankim0/clean-architecture-skills](#nathankim0-clean-architecture-skills)
  7. [codewithmukesh/dotnet-claude-kit](#codewithmukesh-dotnet-claude-kit)
- [Broad / Multi-Framework Collections](#broad--multi-framework-collections)
  8. [SebastienDegodez/copilot-instructions](#sebastiendegodez-copilot-instructions)
  9. [wondelai/skills](#wondelai-skills)
  10. [danmestas/agent-skills](#danmestas-agent-skills)
- [Refactoring-Focused](#refactoring-focused)
  11. [MuhiminOsim/code-refactoring-skill](#muhiminosim-code-refactoring-skill)
- [Process / SDLC Tooling](#process--sdlc-tooling)
  12. [arozumenko/sdlc-skills](#arozumenko-sdlc-skills)
- [Discovery Indexes](#discovery-indexes)
  13. [VoltAgent/awesome-agent-skills](#voltagent-awesome-agent-skills)
  14. [kodustech/awesome-agent-skills](#kodustech-awesome-agent-skills)
  15. [github/awesome-copilot](#github-awesome-copilot)
  16. [Source Books Referenced](#16-source-books-referenced)
- [Recommended evaluation order](#recommended-evaluation-order)
- [Suggested combined setup](#suggested-combined-setup)

---

## Book-Distilled Rule Sets

Repositories whose primary organizing principle is one rule/skill per source book, rather than a single opinionated workflow.

<a id="ciembor-agent-rules-books"></a>

### 1. `ciembor/agent-rules-books`

GitHub:
https://github.com/ciembor/agent-rules-books

MIT-licensed, tool-agnostic rule sets (for Codex, Cursor, and Claude Code) distilled from 14 classic software-engineering sources covering design, architecture, DDD, refactoring, legacy code, and reliability: *A Philosophy of Software Design*, *Clean Architecture*, *Clean Code*, *Code Complete*, *Designing Data-Intensive Applications*, *Domain-Driven Design*, *Domain-Driven Design Distilled*, *Implementing Domain-Driven Design*, *Patterns of Enterprise Application Architecture*, *Refactoring*, Refactoring.Guru, *Release It!*, *The Pragmatic Programmer*, and *Working Effectively with Legacy Code*.

Each rule set ships in three sizes — `full` (canonical reference), `mini` (recommended for everyday use), and `nano` (compact fallback for tight context budgets) — so the same source book can back either an always-on persistent rule or an on-demand skill.

Each rule set is a static, book-scoped Markdown file rather than an installable skill package with commands or agents, which is what makes it compose cleanly alongside the more operational tooling in the other repositories below.

**Software design methods referenced:** [Domain-Driven Design](./glossary.md#domain-driven-design-ddd) (strategic and tactical), [Clean/Hexagonal Architecture](./glossary.md#hexagonal--clean-architecture), object-oriented design discipline (*Clean Code*, *Code Complete*, *A Philosophy of Software Design*), [refactoring](./glossary.md#refactoring) and legacy-code techniques, distributed/data-intensive systems design, general engineering discipline (*The Pragmatic Programmer*).

---

<a id="zlstas-skills"></a>

### 2. `ZLStas/skills`

GitHub:
https://github.com/ZLStas/skills

This repository follows a very similar concept to `agent-rules-books`: practices from programming books are converted into reusable rules, commands, agents, and `SKILL.md` files. Its own tagline is "book knowledge distilled into AI agent skills." It ships 22 book-grounded skills (with `SKILL.md` + examples + evals), 8 autonomous reviewer agents, 22 slash commands, 6 always-on language standards, and a Claude Code `UserPromptSubmit` hook. Confirmed source books include *Clean Code*, *Domain-Driven Design*, and *Effective Kotlin*; open "good first issue" requests at the time of writing include *The Pragmatic Programmer*, *Clean Architecture*, *A Philosophy of Software Design*, and *Accelerate*, so the book list is still growing.

It includes book-based skills and supports tools such as:

- Claude Code
- Cursor
- GitHub Copilot
- Windsurf

It also provides installer profiles for areas such as:

- Python
- TypeScript
- Rust
- JVM
- Software architecture
- Data engineering

**Software design methods referenced:** [Clean Code](./glossary.md#code-smell)-style object-oriented design discipline, [Domain-Driven Design](./glossary.md#domain-driven-design-ddd) (strategic and tactical), language-specific idiomatic design ("Effective" style guides), general software architecture practice.

#### Comparison with `agent-rules-books`

These two are the closest pair in this category — both convert named books into per-book agent content — but they differ in shape:

| Repository                  | Main emphasis                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `ciembor/agent-rules-books` | Concise, tool-agnostic rules distilled from classic books, including full, mini, and nano variants                     |
| `ZLStas/skills`             | Operational skill package with slash commands, specialized agents, persistent rules, installers, and language profiles |

`ZLStas/skills` may be more convenient for direct daily use. `agent-rules-books` is particularly useful when you want compact, inspectable, and composable rule sets.

---

<a id="addyosmani-agent-skills"></a>

### 3. `addyosmani/agent-skills`

GitHub:
https://github.com/addyosmani/agent-skills

Twenty-four production-grade lifecycle skills (23 lifecycle skills plus one meta-skill on using agent skills), installable into 70+ agents via a skills CLI (`npx skills add addyosmani/agent-skills`). Rather than distilling one design book, it bakes in practices from *Software Engineering at Google* (Winters, Manshreck & Wright) across the full development lifecycle: when to write a spec, what to test, how to review, and when to ship.

Its premise is close to this document's framing of *The Pragmatic Programmer* rule set in `agent-rules-books` — general engineering discipline that cuts across every design method rather than mapping onto one — but implemented as an enforced, multi-skill workflow instead of a single rule set.

**Software design methods referenced:** No single design method — full-lifecycle engineering discipline (spec-writing, testing strategy, code review, security review, shipping gates) grounded in *Software Engineering at Google* rather than a specific architecture or modelling approach.

---

## Domain-Driven Design–Focused

<a id="forceinjection-domain-driven-design-skills"></a>

### 4. `ForceInjection/domain-driven-design-skills`

GitHub:
https://github.com/ForceInjection/domain-driven-design-skills

A DDD-specific repository covering an end-to-end domain-modelling workflow:

```text
Discovery
→ Strategic Design
→ Tactical Design
→ Validation
→ Specification Bridging
```

(See [Strategic DDD](./glossary.md#strategic-ddd) and [Tactical DDD](./glossary.md#tactical-ddd) in the glossary.)

Its emphasis is on modelling artifacts rather than immediately generating application code.

The project is technology-neutral, although it is still marked as work in progress.

For Domain-Driven Design work, this is one of the most relevant companions to `agent-rules-books`.

**Software design methods referenced:** [Strategic DDD](./glossary.md#strategic-ddd) (domain discovery, bounded contexts, context mapping) and [Tactical DDD](./glossary.md#tactical-ddd) (aggregates, entities, value objects), plus a validation and specification-bridging step of its own.

---

<a id="zudochkin-go-clean-ddd-skill"></a>

### 5. `zudochkin/go-clean-ddd-skill`

GitHub:
https://github.com/zudochkin/go-clean-ddd-skill

An interactive DDD modelling workflow for Claude Code.

It covers topics such as:

- [Bounded contexts](./glossary.md#bounded-context)
- [Aggregates](./glossary.md#aggregate)
- [Invariants](./glossary.md#tactical-ddd)
- [Domain events](./glossary.md#domain-event)
- Code generation

The main limitation is that its implementation guidance and templates are Go-specific.

**Software design methods referenced:** [Tactical DDD](./glossary.md#tactical-ddd) (bounded contexts, aggregates, invariants, domain events), applied through Go-specific code generation rather than a technology-neutral model.

---

## Clean Architecture–Focused

<a id="nathankim0-clean-architecture-skills"></a>

### 6. `nathankim0/clean-architecture-skills`

GitHub:
https://github.com/nathankim0/clean-architecture-skills

A focused collection for:

- [Clean Architecture](./glossary.md#hexagonal--clean-architecture) reviews
- [Dependency Rule](./glossary.md#dependency-rule) validation
- [SOLID principles](./glossary.md#solid-principles)
- Kent Beck-style simple design
- [Code smell](./glossary.md#code-smell) detection
- [Refactoring](./glossary.md#refactoring) guidance

It is primarily packaged for Claude Code, but also documents installation for Cursor, Gemini CLI, and OpenCode.

This is a good choice when you want actionable architecture and refactoring reviews rather than a broad book library.

**Software design methods referenced:** [Clean/Hexagonal Architecture](./glossary.md#hexagonal--clean-architecture), [Dependency Rule](./glossary.md#dependency-rule), [SOLID principles](./glossary.md#solid-principles), Kent Beck simple design, [code smells](./glossary.md#code-smell) and [refactoring](./glossary.md#refactoring).

---

<a id="codewithmukesh-dotnet-claude-kit"></a>

### 7. `codewithmukesh/dotnet-claude-kit`

GitHub:
https://github.com/codewithmukesh/dotnet-claude-kit

A .NET-oriented repository with separate skills for:

- [Domain-Driven Design](./glossary.md#domain-driven-design-ddd)
- [Clean Architecture](./glossary.md#hexagonal--clean-architecture)
- Architecture assessment
- Implementation guidance

It is more implementation-oriented than book-oriented.

A useful aspect is that its architecture guidance explicitly discourages applying DDD or Clean Architecture where the project complexity does not justify the overhead: a `dotnet-architect` agent runs a structured questionnaire covering domain complexity, team size, project lifetime, and compliance needs, then recommends one of four architectures — [Vertical Slice Architecture](./glossary.md#vertical-slice-architecture), [Clean Architecture](./glossary.md#hexagonal--clean-architecture), [Domain-Driven Design](./glossary.md#domain-driven-design-ddd), or Modular Monolith — with a stated evolution path between them.

**Software design methods referenced:** [Vertical Slice Architecture](./glossary.md#vertical-slice-architecture), [Clean Architecture](./glossary.md#hexagonal--clean-architecture), [Domain-Driven Design](./glossary.md#domain-driven-design-ddd), Modular Monolith — offered as a decision, not a default.

---

## Broad / Multi-Framework Collections

<a id="sebastiendegodez-copilot-instructions"></a>

### 8. `SebastienDegodez/copilot-instructions`

GitHub:
https://github.com/SebastienDegodez/copilot-instructions

A broader repository containing:

- Instructions
- Prompts
- Skills
- Agent personas
- Plugin bundles
- [DDD](./glossary.md#domain-driven-design-ddd) rules
- [Clean Architecture](./glossary.md#hexagonal--clean-architecture) rules
- [CQRS](./glossary.md#cqrs-command-query-responsibility-segregation) guidance
- Testing practices

It is particularly relevant for C#, .NET, and GitHub Copilot.

Its C# plugin combines architectural guidance, DDD, CQRS, testing, setup scripts, and architecture validation. The `clean-architecture-dotnet` skill specifically is a complete guide for Clean Architecture with DDD and CQRS (no MediatR), including project-initialization scripts and ArchUnit-style validation; a companion `application-layer-testing` skill covers sociable testing of application-layer handlers using real domain objects and mocked infrastructure. It also documents a specification pattern for expressing business rules.

**Software design methods referenced:** [Domain-Driven Design](./glossary.md#domain-driven-design-ddd), [Clean Architecture](./glossary.md#hexagonal--clean-architecture), [CQRS](./glossary.md#cqrs-command-query-responsibility-segregation), the Specification pattern, and sociable unit/integration testing practice.

---

<a id="wondelai-skills"></a>

### 9. `wondelai/skills`

GitHub:
https://github.com/wondelai/skills

A broader "business & engineering frameworks as AI agent skills" repository (agentskills.io-compatible: Claude, Claude Code, Claude Cowork, Codex, Cursor, and others) spanning roughly 50 skills, two of which map directly onto this document's territory:

- A **clean-architecture** skill that structures software around the [Dependency Rule](./glossary.md#dependency-rule) (dependencies point inward from frameworks → use cases → entities), covering component principles, boundaries, and [SOLID](./glossary.md#solid-principles).
- A **domain-driven-design** skill covering [bounded contexts](./glossary.md#bounded-context), [aggregates](./glossary.md#aggregate), [ubiquitous language](./glossary.md#strategic-ddd), entities vs. value objects, domain events, and context-mapping strategies.

Unlike the dedicated DDD and Clean Architecture repositories above, this one packages both inside a much larger, non-software-specific skill library — closer in spirit to `danmestas/agent-skills` than to `ForceInjection` or `nathankim0`, but with noticeably more detailed coverage of the two methods it does address.

**Software design methods referenced:** [Clean Architecture](./glossary.md#hexagonal--clean-architecture) ([Dependency Rule](./glossary.md#dependency-rule), [SOLID principles](./glossary.md#solid-principles), component principles), [Domain-Driven Design](./glossary.md#domain-driven-design-ddd) (bounded contexts, aggregates, ubiquitous language, context mapping) — two modules inside a much wider, non-software-specific framework pack.

---

<a id="danmestas-agent-skills"></a>

### 10. `danmestas/agent-skills`

GitHub:
https://github.com/danmestas/agent-skills

A mixed collection of AI coding-agent skills covering:

- Software design
- Testing
- DevOps
- Project management

It is less tightly grounded in named books, but structurally similar as a reusable agent-skills repository. Beyond design skills it also includes meta-skills for evaluating other skills (binary pass/fail evals on skill edits) and for auditing or reconstructing prior Claude Code sessions.

**Software design methods referenced:** No single named method — general design-principle guidance packaged alongside testing, DevOps, and project-management skills.

---

## Refactoring-Focused

<a id="muhiminosim-code-refactoring-skill"></a>

### 11. `MuhiminOsim/code-refactoring-skill`

GitHub:
https://github.com/MuhiminOsim/code-refactoring-skill

A dedicated [refactoring](./glossary.md#refactoring) skill, cross-agent (Claude Code, Cursor, Antigravity, Copilot, and others), built around a strict five-phase process: Intake (read target files, detect language and test harness) → Diagnose ([code smells](./glossary.md#code-smell), ranked) → Plan (decompose into atomic, verifiable steps) → Execute (one change at a time, tests run after each) → Wrap-up (summarize, suggest but don't apply follow-ons).

It never "fixes forward" — a change that breaks a test is reverted and re-approached rather than patched around. Architectural refactoring gets a stricter sub-protocol of its own (map the target first, confirm it, then apply an Introduce → Redirect → Remove sequence while preserving the "moving invariant," with tests passing after every sub-step).

None of the repositories above package a dedicated, cross-agent refactoring workflow of this depth — the closest equivalent in `agent-rules-books` is the static Refactoring / Refactoring.Guru / Working Effectively with Legacy Code rule sets, which this repository turns into an enforced procedure rather than a reference.

**Software design methods referenced:** [Refactoring](./glossary.md#refactoring) ([code smell](./glossary.md#code-smell) catalog, behavior-preserving steps), [characterization](./glossary.md#refactoring-and-legacy-code)-adjacent safety discipline (revert-on-red rather than fix-forward), a named [invariant](./glossary.md#invariant)-preserving technique for architectural-scale changes.

---

## Process / SDLC Tooling

<a id="arozumenko-sdlc-skills"></a>

### 12. `arozumenko/sdlc-skills`

GitHub:
https://github.com/arozumenko/sdlc-skills

SDLC agents and skills for Claude Code, Cursor, Windsurf, and Copilot, including Atlassian/Jira integration content, personal-assistant-style personas, and a shared registry cache for installing skills from other repositories. It is closer to process and tooling automation than to a specific design method — useful context for teams choosing an agent-skills stack, but included here for completeness rather than as a design-method resource.

**Software design methods referenced:** None specifically — SDLC process and tooling integration (issue trackers, agent orchestration) rather than a design or modelling method.

---

## Discovery Indexes

Larger directories for discovering more skills, rather than repositories dedicated to a specific design method themselves.

<a id="voltagent-awesome-agent-skills"></a>

### 13. `VoltAgent/awesome-agent-skills`

GitHub:
https://github.com/VoltAgent/awesome-agent-skills

A large curated index of agent skills from engineering teams and community projects (1000+ at the time of writing).

It includes skills for tools such as:

- Claude Code
- Codex
- Cursor
- GitHub Copilot
- Gemini CLI
- OpenCode
- Windsurf

This is useful for discovering additional focused repositories beyond architecture and DDD.

**Software design methods referenced:** None directly — a discovery index spanning every method covered elsewhere in this document, plus many unrelated to software design.

<a id="kodustech-awesome-agent-skills"></a>

### 14. `kodustech/awesome-agent-skills`

GitHub:
https://github.com/kodustech/awesome-agent-skills

A smaller catalogue focused primarily on reusable `SKILL.md` projects for software engineering.

**Software design methods referenced:** None directly — a smaller discovery index, same role as `VoltAgent/awesome-agent-skills` above.

<a id="github-awesome-copilot"></a>

### 15. `github/awesome-copilot`

GitHub:
https://github.com/github/awesome-copilot

GitHub's own official collection of Copilot instructions, agents, and skills. Most of it is not software-design-specific, but it includes a `refactor` skill and a `review-and-refactor` skill: the latter reads a project's own `.github/instructions/*.md` and `.github/copilot-instructions.md` files and refactors code to comply with them, without restructuring files, while keeping tests passing.

Worth checking when a team's coding standards already live in Copilot instruction files and the goal is enforcing those specific standards, rather than a named external method.

**Software design methods referenced:** [Refactoring](./glossary.md#refactoring) driven by project-local coding-standard files rather than a named book or method; otherwise a general discovery index like the two above.

---

<a id="16-source-books-referenced"></a>

## 16. Source Books Referenced

Real, purchasable books (physical or Kindle) named anywhere in this document, [software_design.md](./software_design.md), or [strategic_tactical_design.md](./strategic_tactical_design.md) — not papers, blog posts, or free-standing whitepapers/PDFs (e.g. Vernon's *Effective Aggregate Design* series or the InfoQ *DDD Quickly* minibook are excluded on that basis, as is `ciembor/agent-rules-books`' `refactoring-guru` rule set, which distills a website rather than a single named book). Sorted alphabetically by title.

The **Related repositories** column lists every repository *in this document's list of 15* that ties its content to that specific book — not only `ciembor/agent-rules-books`. Only three repositories name individual books at all ([§1 `ciembor/agent-rules-books`](#ciembor-agent-rules-books), [§2 `ZLStas/skills`](#zlstas-skills), [§3 `addyosmani/agent-skills`](#addyosmani-agent-skills)); the other twelve reference design *methods* (DDD, Clean Architecture, refactoring, …) without naming a specific book, so they never appear in this column. `(planned)` marks a book that is an open "good first issue" on `ZLStas/skills` rather than a shipped skill yet.

| Book                                              | Author(s)                                                  | Referenced in                                                   | Related repositories                                                                                   |
| ------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| *A Philosophy of Software Design* (2nd ed.)       | John Ousterhout                                            | software_design.md, strategic_tactical_design.md, this document | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books); [`ZLStas/skills`](#zlstas-skills) (planned) |
| *Accelerate*                                      | Nicole Forsgren, Jez Humble, Gene Kim                      | this document                                                   | [`ZLStas/skills`](#zlstas-skills) (planned)                                                            |
| *Building Evolutionary Architectures*             | Neal Ford, Rebecca Parsons, Patrick Kua                    | software_design.md                                              | —                                                                                                      |
| *Clean Architecture*                              | Robert C. Martin                                           | software_design.md, this document                               | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books); [`ZLStas/skills`](#zlstas-skills) (planned) |
| *Clean Code*                                      | Robert C. Martin                                           | software_design.md, strategic_tactical_design.md, this document | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books); [`ZLStas/skills`](#zlstas-skills)           |
| *Code Complete*                                   | Steve McConnell                                            | software_design.md, this document                               | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books)                                              |
| *Designing Data-Intensive Applications*           | Martin Kleppmann                                           | software_design.md, this document                               | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books)                                              |
| *Domain-Driven Design* ("Blue Book")              | Eric Evans                                                 | software_design.md, strategic_tactical_design.md, this document | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books); [`ZLStas/skills`](#zlstas-skills)           |
| *Domain-Driven Design Distilled*                  | Vaughn Vernon                                              | software_design.md, strategic_tactical_design.md, this document | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books)                                              |
| *Effective Kotlin*                                | Marcin Moskała                                             | this document                                                   | [`ZLStas/skills`](#zlstas-skills)                                                                      |
| *Fundamentals of Software Architecture*           | Mark Richards, Neal Ford                                   | strategic_tactical_design.md                                    | —                                                                                                      |
| *Implementing Domain-Driven Design* ("Red Book")  | Vaughn Vernon                                              | software_design.md, strategic_tactical_design.md, this document | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books)                                              |
| *Learning Domain-Driven Design*                   | Vlad Khononov                                              | strategic_tactical_design.md                                    | —                                                                                                      |
| *Patterns of Enterprise Application Architecture* | Martin Fowler                                              | software_design.md, strategic_tactical_design.md, this document | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books)                                              |
| *Refactoring*                                     | Martin Fowler                                              | software_design.md, this document                               | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books)                                              |
| *Release It!*                                     | Michael T. Nygard                                          | software_design.md, this document                               | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books)                                              |
| *Software Architecture: The Hard Parts*           | Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani | strategic_tactical_design.md                                    | —                                                                                                      |
| *Software Engineering at Google*                  | Titus Winters, Tom Manshreck, Hyrum Wright                 | software_design.md, this document                               | [`addyosmani/agent-skills`](#addyosmani-agent-skills)                                                  |
| *Team Topologies*                                 | Matthew Skelton, Manuel Pais                               | strategic_tactical_design.md                                    | —                                                                                                      |
| *The Pragmatic Programmer*                        | David Thomas, Andrew Hunt                                  | software_design.md, this document                               | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books); [`ZLStas/skills`](#zlstas-skills) (planned) |
| *Working Effectively with Legacy Code*            | Michael Feathers                                           | software_design.md, strategic_tactical_design.md, this document | [`ciembor/agent-rules-books`](#ciembor-agent-rules-books)                                              |

---

## Recommended evaluation order

For a Python, TypeScript, C#, and Domain-Driven Design-oriented use case:

1. `ZLStas/skills`
   Closest overall replacement or companion to `agent-rules-books`.

2. `ForceInjection/domain-driven-design-skills`
   Strongest DDD modelling workflow.

3. `ciembor/agent-rules-books`
   Best compact source of book-derived principles.

4. `SebastienDegodez/copilot-instructions`
   Especially useful for C# and .NET projects.

5. `nathankim0/clean-architecture-skills`
   Lightweight architecture and refactoring review.

6. `wondelai/skills`
   Worth a look if you want Clean Architecture and DDD skills bundled with a much wider set of business/engineering frameworks, rather than as dedicated repositories.

7. `MuhiminOsim/code-refactoring-skill`
   Add when you specifically want an enforced, cross-agent refactoring workflow rather than static refactoring rules.

## Suggested combined setup

A practical approach is:

- Use the mini rules from `agent-rules-books` as persistent project guidance.
- Add selected skills from `ZLStas/skills` for operational workflows.
- Use a dedicated DDD workflow repository for modelling sessions.
- Add language-specific instruction repositories only where needed.
- Add `MuhiminOsim/code-refactoring-skill` where an enforced refactoring procedure (not just reference rules) is wanted.

This keeps the always-on context compact while still providing deeper, task-specific guidance when required.
