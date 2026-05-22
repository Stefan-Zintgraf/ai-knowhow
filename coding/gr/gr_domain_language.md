# Guardrail: Domain and Ubiquitous Language

Purpose: protect meaning. The same concept must have one name everywhere — in code, tests, docs, APIs, and UI.

---

## Apply When

- Business terms or domain concepts are named, renamed, or restructured.
- New domain objects, fields, events, or operations are introduced.
- User-facing concepts cross into code or APIs.
- Terminology differs between teams, modules, or documents.

---

## Rules

### L1. Use Defined Terms Exactly

Terms from the project's glossary or ubiquitous language are used verbatim. No casual variation, abbreviation, or translation.

### L2. No Forbidden Synonyms

If a term is the canonical one (e.g. "Order"), synonyms ("Purchase", "Transaction") must not appear for the same concept. Synonyms used for *different* concepts must be defined and distinguished.

### L3. Separate Domain Terms from Technical Terms

A domain concept ("Invoice") is not named after a technical artifact ("InvoiceDTO", "InvoiceRow") in the domain layer. Technical suffixes belong to technical layers only.

### L4. Naming Reflects Behavior, Not Storage

Names describe what the concept means in the domain, not how it is stored or transported.

### L5. Renaming Is a Domain Change

Renaming a domain term is not cosmetic. It must propagate consistently across code, tests, APIs, docs, UI, and messages — or not happen at all.

### L6. Introduce New Terms Explicitly

If a new domain term is needed, the agent flags it and proposes a definition rather than silently inventing one.

### L7. Match Language Across Bounded Contexts Deliberately

The same word may legitimately mean different things in different bounded contexts. The agent must not unify them by accident.

### L8. `context.md` Is the Ubiquitous-Language Artifact

The project's ubiquitous language lives in a durable in-tree file `context.md` at the root of each bounded context. One bounded context → one `context.md`. A single-domain repo has exactly one at the repo root; a monorepo with multiple bounded contexts has one per context, forming a **context map** (DDD strategic design). Each `context.md`:

- Defines every non-obvious domain term, entity, status value, and relationship in plain language.
- Connects terms to code entities / database fields / UI labels where relevant.
- Includes concrete examples and edge cases when a definition alone is ambiguous.
- Is the canonical source `aln` reads at session start and updates in-session (Aln17).

`context.md` is **not** retired (distinct from PRDs per 3.24 and research per 3.27). It is durable, like an ADR (3.34). It is **the source of truth for terms** — code, tests, APIs, and UI must match it (L1, L5).

Origin: Pocock — `/grill-with-docs` is built around a `context.md` per bounded context; transcripts `i-stopped-using-grill-me-for-coding-heres-what-i-use-instead_*.md`.

Note: this project's working directory does not (yet) have a `context.md` because it is a meta-repo (guardrails + skill authoring), not a domain product. The L8 convention applies prospectively to projects this guardrail set governs.

### L9. CLAUDE.md Points to the Domain Docs

When `context.md` (or a context map) exists in a repo, the local `CLAUDE.md` (or equivalent agent-instruction file) must contain an explicit pointer to it — path and one-line role description ("Domain glossary; read before any planning or implementation; update in-session when terms emerge or shift"). Skills that read domain language (notably A1 `align-concept` per Aln17) rely on the pointer to find the artifact reliably across repos.

Without the pointer, agents either miss `context.md` entirely (treating it as just another markdown file) or re-discover its location every session.

---

## Anti-Patterns

- Using "User", "Customer", and "Account" interchangeably.
- Inventing a name because the canonical one is "too long."
- Renaming a class without renaming the matching event, table, or API field.
- Letting database column names dictate domain field names.
- Maintaining a glossary in a wiki / ticket / Notion page instead of `context.md` in the repo. The point of L8 is co-location with the code so the agent reads it as ground truth.
- Collapsing two bounded contexts into a single `context.md` "to keep it simple" — produces overloaded terms (L7).
- Having `context.md` but no `CLAUDE.md` pointer — agent misses it (L9).
- Treating `context.md` as write-once. Stale glossary entries mislead worse than missing ones; Aln17 keeps it current.
