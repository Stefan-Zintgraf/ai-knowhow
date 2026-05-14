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

---

## Anti-Patterns

- Using "User", "Customer", and "Account" interchangeably.
- Inventing a name because the canonical one is "too long."
- Renaming a class without renaming the matching event, table, or API field.
- Letting database column names dictate domain field names.
