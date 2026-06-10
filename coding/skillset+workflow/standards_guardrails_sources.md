# Open-Source Guardrails and Guidelines for AI-Agent Workflows

This document collects practical open-source sources that can be used as the basis for **implementation**, **architecture/planning**, and **review** guardrails for AI coding agents working with **Python**, **TypeScript**, and **Bash**. The recommendations below favor concrete, reusable rule sets and templates over generic advice.

## Recommended sources

### Language-specific implementation guides

| Area       | Source                                                                                                                | Why it is useful                                                                                                       |
| ---------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Python     | [PEP 8](https://peps.python.org/pep-0008/)                                                                            | Canonical baseline for formatting and general style.                                                                   |
| Python     | [NI Python Styleguide](https://ni.github.io/python-styleguide/)                                                       | More concrete and operational than PEP 8, especially for docstrings and enforceable rules.                             |
| TypeScript | [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)                                     | Strong, opinionated language-level guidance.                                                                           |
| TypeScript | [google/gts](https://github.com/google/gts)                                                                           | Practical enforcement package for style, linting, and formatting.                                                      |
| TypeScript | [microsoft/TypeScript wiki coding guidelines](https://github.com/microsoft/TypeScript/wiki/Coding-guidelines)         | Good project-oriented conventions from the TypeScript compiler team.                                                   |
| Bash       | [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)                                       | Best-known concrete Bash guide, including advice on when shell is appropriate and patterns compatible with ShellCheck. |
| Bash       | [Open-Technology-Foundation/bash-coding-standard](https://github.com/Open-Technology-Foundation/bash-coding-standard) | Newer repo focused on robust Bash engineering practices.                                                               |
| Bash       | [GitLab shell scripting guide](https://docs.gitlab.com/development/shell_scripting_guide/)                            | Practical standards tied to review, ShellCheck, and formatting.                                                        |

### Architecture and planning sources

For architecture, the best open approach is to store **Architecture Decision Records (ADRs)** in the repository and let agents check implementations against them.

- [adr/madr](https://github.com/adr/madr) — widely used Markdown ADR templates with a repeatable format and examples.
- [Architectural Decision Records](https://adr.github.io) — central ADR hub with concepts and supporting tooling.
- [opinionated-digital-center/architecture-decision-records](https://github.com/opinionated-digital-center/architecture-decision-records) — public repo with practical ADR examples.
- [The Architecture of Open Source Applications](https://aosabook.org/en/) — useful for studying real-world architecture explanations, even though it is not a rules repository.

### Review guidance sources

- [mgreiler/code-review-checklist](https://github.com/mgreiler/code-review-checklist) — concise general review checklist.
- [mgreiler/awesome-code-review-checklists](https://github.com/mgreiler/awesome-code-review-checklists) — curated directory of review checklists by language and context.
- [knonm/code-review-checklist](https://github.com/knonm/code-review-checklist) — broader checklist covering naming, return types, complexity, DRY, architecture adherence, and SOLID.
- [swomack/cpp-code-review-checklist](https://github.com/swomack/cpp-code-review-checklist) — C++-specific, but structurally useful as a template for language-specific review docs.

## Best practical combination

If the goal is to build a reusable AI-agent ruleset, this is a strong combination:

- **Python:** PEP 8 + NI Python Styleguide
- **TypeScript:** Google TypeScript Style Guide + `gts`
- **Bash:** Google Shell Style Guide + GitLab shell guide
- **Architecture:** MADR / ADR templates
- **Review:** Michaela Greiler’s review checklist repositories

## Suggested repository layout

A simple structure inspired by these sources:

- `docs/adr/` — architecture decisions, based on MADR
- `agent-rules/gr_python.md` — Python implementation rules
- `agent-rules/gr_typescript.md` — TypeScript implementation rules
- `agent-rules/gr_bash.md` — Bash implementation rules
- `agent-rules/gr_architecture.md` — architecture and boundary rules
- `agent-rules/gr_rev.md` — review behavior and checklist rules
- `.github/copilot-instructions.md` or equivalent — tells the agent which guardrails to load during implementation and review

## Recommended use by phase

### Implementation phase

Use the language-specific style guides and enforcement tools as the primary basis for implementation guardrails:

- Python: PEP 8, NI Python Styleguide
- TypeScript: Google TS Style Guide, `gts`
- Bash: Google Shell Style Guide, GitLab shell guide

### Planning / architecture phase

Use ADRs as the main source of truth for architectural rules, module boundaries, dependency direction, and accepted patterns.

### Review phase

Use a review checklist repo as the structural base, then adapt it into a `gr_rev.md` file that requires:

- loading the applicable language and architecture guardrails before reviewing
- checking tests before implementation
- checking behavior, not only style
- checking scope discipline, API changes, and architecture adherence

## Shortlist of best sources

If only a compact set is needed, these are the strongest picks:

1. [PEP 8](https://peps.python.org/pep-0008/)
2. [NI Python Styleguide](https://ni.github.io/python-styleguide/)
3. [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
4. [google/gts](https://github.com/google/gts)
5. [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
6. [GitLab shell scripting guide](https://docs.gitlab.com/development/shell_scripting_guide/)
7. [adr/madr](https://github.com/adr/madr)
8. [Architectural Decision Records](https://adr.github.io)
9. [mgreiler/code-review-checklist](https://github.com/mgreiler/code-review-checklist)
10. [mgreiler/awesome-code-review-checklists](https://github.com/mgreiler/awesome-code-review-checklists)
