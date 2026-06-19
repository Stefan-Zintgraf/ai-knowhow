# Output templates

The markdown skeleton for each of the seven companion files. These are *shapes*,
not fill-in forms — adapt headings and prose to the product, but keep the columns,
the ID schemes, and the cross-links. Every derived claim cites ≥1 `UC`. The
ai-mail pilot (`ai-mail.pocock/docs/brainstorming/ai-mail-vision-ai-spec/`) is the
worked reference for files 1–6; file 7 (subdomains/context-map) is new with S7.

Replace `<product>` / `<product-slug>` and the bracketed placeholders throughout.

---

## 1. `README.md` — map + load order

```markdown
# <Product> Vision — AI-Friendly Companion Set

This folder is a **derived, machine-navigable view** of
[<product-slug>-foundation-vision.md](../<product-slug>-foundation-vision.md). It
exists so a build-phase agent (architecture, requirements, planning) can consume
the vision without re-deriving its structure each run.

> **The vision is the single source of truth.** These files are derived from it
> and cite back by UC ID (`UC1…UC<n>`). They never replace or contradict it. If a
> derived file and the vision disagree, the vision wins — fix the derived file.
> Do **not** edit the vision to match these.

## Files

| File | Concern | Load it when… |
|------|---------|---------------|
| [invariants.md](invariants.md) | Cross-cutting constraints (`INV1…`) stated once | …always. Every architecture/design decision must honour these. |
| [glossary.md](glossary.md) | Ubiquitous language — one canonical term per concept | …always. Use these terms in code, schemas, docs. |
| [actors.md](actors.md) | Actor types & personas | …reasoning about permissions, multi-tenancy, or whose POV a need is. |
| [capability-map.md](capability-map.md) | The <n> UCs clustered into capabilities (`CAP1…`) | …shaping modules/services or scoping a feature area. |
| [subdomains-and-context-map.md](subdomains-and-context-map.md) | Core/Supporting/Generic + context relationships | …deciding where to concentrate design effort and how contexts integrate. |
| [uc-index.md](uc-index.md) | Traceability spine: every UC → actor · capability · invariants · normalized intent | …you need to trace a requirement back to a UC, or forward from a UC. |

## Suggested load order by task

- **Whole-system architecture:** invariants → glossary → capability-map → subdomains-and-context-map → actors.
- **Requirements for one capability:** invariants → glossary → that `CAP` section → its UC rows in uc-index → the cited UCs in the vision.
- **Where to invest design effort:** subdomains-and-context-map (Core first).
- **Reviewing coverage / traceability:** uc-index (it links everything).

## How this was built & its limits

- **Derived, not authored.** Every claim traces to ≥1 UC. No new requirements
  invented; nothing dropped — all <n> UCs appear in uc-index.md with a primary
  capability and actor.
- **Compression is bounded.** The only shortening is the *normalized intent*
  one-liner per UC in the index, which factors repeated invariant boilerplate out
  to `INV` references. The rich original sentence stays in the vision.
- **A UC can touch several capabilities.** Filed under one *primary*; notable
  secondaries noted. Cross-cutting needs are invariants, not capabilities.
- **Out of scope:** priority/phasing (vision omits it by design; subdomain class
  is the only soft ordering) and a machine-readable (YAML/JSON) layer — add only
  when a real consumer needs them.

Method and rationale: see the bundled `strategies.md` in the
`create-vision-companion` skill.
```

---

## 2. `invariants.md` — cross-cutting constraints (S1)

```markdown
# Invariants — global constraints

These are the load-bearing constraints the vision re-asserts across many
use-cases. They are stated **once** here; capability and UC descriptions
reference them by ID instead of repeating them. **Every** architecture, design,
and data-model decision must honour all of these.

> Each invariant lists *representative* asserting UCs, not an exhaustive list.
> See [uc-index.md](uc-index.md) for the per-UC mapping.

| ID | Invariant | What it means for the build | Asserting UCs (representative) |
|----|-----------|-----------------------------|-------------------------------|
| **INV1** | **<short name>.** | <concrete consequence for architecture/design> | <UC list> |
| **INV2** | … | … | … |

## Notes for downstream design

- <how invariants combine, e.g. "INV1 + INV2 together imply a propose→review→apply pipeline">
```

Rules: every `INV` is cited by ≥1 UC (no invented constraints). State each once;
nothing here is per-feature.

---

## 3. `glossary.md` — ubiquitous language (S3)

```markdown
# Glossary — ubiquitous language

One canonical term per concept, so code, schemas, and docs speak the same
language. The **Vision phrasings** column lists the various ways the (deliberately
non-technical) vision names the same thing — treat those as synonyms of the
canonical term, not distinct concepts.

| Canonical term | Definition | Vision phrasings it absorbs |
|----------------|------------|-----------------------------|
| **<Term>** | <one-sentence definition; cite an INV if the term encodes one> | "<synonym>", "<synonym>", … |
```

Rules: exactly one canonical term per concept; every known synonym mapped to one.
If the project has a `CONTEXT.md` ubiquitous-language section, reconcile with it.

---

## 4. `actors.md` — actor types & personas (S2)

```markdown
# Actors & personas

Whose point of view each use-case is told from. Codes appear in the **Actor**
column of [uc-index.md](uc-index.md). **Actors** are distinct *relationships to
the product* (they drive permissions, isolation, tenancy); **personas** are
flavours of an actor (they drive UX and tone, not architecture).

## Actor types

| Code | Actor | Description | Representative UCs |
|------|-------|-------------|--------------------|
| **<CODE>** | <Actor> | <relationship to the product> | <UC list> |

## Personas (flavours of <default actor>)

- **<persona>** — <what they feel / need; shapes UX not architecture>. (<UCs>)

## Notes for downstream design

- <the primary tenancy fault line, delegated-access cases, oversight-vs-privacy constraints, …>
```

---

## 5. `capability-map.md` — UC clusters (S2)

```markdown
# Capability map

The <n> use-cases clustered into <m> capabilities. Each UC has **one primary**
capability (here); notable secondary touches are in [uc-index.md](uc-index.md).
Cross-cutting needs are **invariants**, not capabilities — see
[invariants.md](invariants.md).

> Coverage: all <n> UCs are assigned a primary capability below. Terms in
> *italics* are defined in [glossary.md](glossary.md).

---

### CAP1 — <name>
<one-paragraph intent, using glossary terms in italics>
- **UCs:** <UC list>
- **Key entities:** <glossary terms>
- **Leans on:** <INV list>

### CAP2 — <name>
…

---

## Capability dependency notes

- <foundational capabilities, the multi-user cluster, which CAPs pass the INV1 gate, …>
```

Rules: every UC has exactly one primary CAP here (secondaries live in the index).
Flag UCs that resist clustering — they're a gap-check on the vision.

---

## 6. `subdomains-and-context-map.md` — strategic design (S7)

```markdown
# Subdomains & context map

Two pieces of **strategic-design** structure layered on the capability map. This
is the *strategic* layer only — **no tactical patterns** (Aggregates, Entities,
ports, consistency models); those belong to the architecture phase this bundle
feeds.

## Subdomain classification

Each capability tagged **Core** (the differentiating reason the product exists —
concentrate design effort), **Supporting** (needed, not differentiating — keep
simple), or **Generic** (a solved problem — prefer buy/adopt). This is a derived
*attention/investment* ordering, **not** MVP scoping; the vision stays
priority-free.

| Capability | Class | Rationale | UCs |
|------------|-------|-----------|-----|
| CAP1 — <name> | Core / Supporting / Generic | <why> | <UC list> |

## Context-map relationships

Each actor/external boundary named with DDD's vocabulary — **Partnership, Shared
Kernel, Customer/Supplier, Conformist, Anticorruption Layer (ACL), Open Host
Service, Published Language, Separate Ways** — with who owns the language and
whether translation is needed.

| Boundary | Relationship | Who owns the language | Translation needed? | UCs |
|----------|--------------|-----------------------|---------------------|-----|
| <e.g. single-user ↔ team/manager> | <type> | <which side> | <yes/no + what> | <UC list> |
| <e.g. product ↔ external mail provider> | Conformist / ACL | <side> | <…> | <UCs> |

## Notes

- <which subdomain is *the* Core; where ACLs protect the model; …> (flag as judgment calls)
```

---

## 7. `uc-index.md` — traceability spine (S4)

```markdown
# UC index — traceability spine

Every use-case from
[<product-slug>-foundation-vision.md](../<product-slug>-foundation-vision.md),
mapped to its actor, primary capability (+ notable secondaries), the invariants it
leans on, and a **normalized intent** one-liner. The one-liner is the *only* place
text is compressed — repeated invariant boilerplate is factored out to `INV`
references; read the cited source line for the full original.

- **Actor** → [actors.md](actors.md) · **CAP** → [capability-map.md](capability-map.md) · **INV** → [invariants.md](invariants.md)
- **Src** links the UC's line in the vision. Coverage: all <n> UCs present, each with a primary capability and an actor.

| UC | Src | Actor | Primary | Also | INV | Normalized intent |
|----|-----|-------|---------|------|-----|-------------------|
| UC1 | [L<n>](../<product-slug>-foundation-vision.md#L<n>) | <CODE> | CAP<n> | <CAP or —> | <INV list or —> | <one-line intent, invariant boilerplate factored out> |
```

Rules: one row per UC, **100% coverage**, every row has a primary CAP and an
actor. The `Src` link points at the UC's actual line in the vision. The normalized
intent is the single sanctioned compression — never restate an invariant verbatim
here; reference it by `INV` id.
