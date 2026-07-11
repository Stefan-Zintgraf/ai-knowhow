# Vision -> Planning Conversion Strategies - Source Map

**What this is.** A source-of-record for [strategies.md](strategies.md): for every
diagnosis (`D#`), strategy (`S#`), the altitude fence (section 2a), and the candidate-standards
list (section 4/section 5), this file points at the **specific parts of the local rule-set documents**
in the `agent-rules-books` repo that the strategy rests on (or, for the fence, defers to),
plus the external/web sources already cited in `strategies.md`.

`strategies.md` and `SKILL.md` are kept **provenance-free by design** - they carry only what
changes what the agent *produces*. This file is therefore the **single home** for all
sources. Method-level gaps that genuinely change the output have been folded into the skill
(the single-source-of-truth basis of S6; operationalizing S8's parked-item routing into the
bundle); reference-only items (Wikipedia / Fowler / AOP links, the orthogonality and
Domain-Vision-Statement provenance) stay here on purpose; section A/section B mark each one where it
occurs, and section C lists the web sources.

> **Reading the "cites" notes below.** Earlier drafts of `strategies.md` carried inline
> `Rests on` / `Refs` lines and a section 5 reference summary. Those were consolidated here so the
> skill files stay outcome-focused. Where section A/section B say *"`strategies.md` cites ..."* or
> *"currently cited as ..."*, that describes the **pre-refactor** inline citation now housed in
> this file - not a live link in `strategies.md`. Nothing was lost, only relocated.

---

## How to read this file

- **Local repo root:** `C:/PROJ/github/agent-rules-books/` (a separate git repo  - 
  the README calls these "AI agent rules / skills distilled from programming books").
  Each book ships three tool-agnostic variants: `....md` (**full**, canonical),
  `....mini.md` (**recommended working version**), `....nano.md` (compact). Citations below
  point at the variant whose line numbers were verified, and name the section heading so
  the anchor survives renumbering.
- **Line ranges** are given where verified against the cited variant. Headings are the
  durable anchor; line numbers are a convenience.
- **`missing in strategies.md`** = the source is deliberately *not* inlined into
  `strategies.md`; it lives here instead. After the outcome-focused refactor this is a
  statement of *where the source lives*, not an outstanding to-do.

---

## A. Local source inventory (`agent-rules-books`)

| Book | Author | Local files | Role in `strategies.md` |
|------|--------|-------------|-------------------------|
| A Philosophy of Software Design (APOSD) | Ousterhout | `a-philosophy-of-software-design/a-philosophy-of-software-design{.md,.mini.md,.nano.md}` | **Rests-on** - section 1 diagnosis ("don't compress"), S5 (deep docs) |
| Clean Architecture | Martin | `clean-architecture/clean-architecture{.md,.mini.md,.nano.md}` | **Rests-on** - S1 (policy independent of detail); **deferred** (the *rules*) by section 2a |
| Domain-Driven Design (the "blue book") | Evans | `domain-driven-design/domain-driven-design{.md,.mini.md,.nano.md}` | **Rests-on** - S2, S3, S7 (strategic half); **deferred** (tactical half) by section 2a |
| Domain-Driven Design Distilled | Vernon | `domain-driven-design-distilled/domain-driven-design-distilled{.md,.mini.md,.nano.md}` | **Rests-on** - S3, S7 (subdomains + full context-map vocabulary incl. *Partnership*) |
| Implementing Domain-Driven Design | Vernon | `implementing-domain-driven-design/...` | **Deferred** by section 2a (tactical DDD) |
| Designing Data-Intensive Applications | Kleppmann | `designing-data-intensive-applications/...` | **Deferred** by section 2a (ownership/consistency/schema-evolution -> architecture phase) |
| The Pragmatic Programmer | Hunt & Thomas | `the-pragmatic-programmer/the-pragmatic-programmer{.md,.mini.md,.nano.md}` | **Source for S6** (DRY = single-source-of-truth, now stated as method in S6); reinforces S5 (orthogonality - provenance only) |
| Clean Code | Martin | `clean-code/...` | **Deferred** by section 2a (build/review altitude) |
| Code Complete | McConnell | `code-complete/...` | **Deferred** by section 2a (construction altitude) |
| Patterns of Enterprise Application Architecture (PEAA) | Fowler | `patterns-of-enterprise-application-architecture/...` | **Deferred** by section 2a |
| Refactoring | Fowler | `refactoring/...` | **Deferred** by section 2a |
| Refactoring.Guru | Refactoring.Guru | `refactoring-guru/...` | **Deferred** by section 2a (same altitude as Refactoring; the fence is now category-based, so individual books aren't listed in it) |
| Release It! | Nygard | `release-it/...` | **Deferred** by section 2a (production-operations altitude) |
| Working Effectively with Legacy Code | Feathers | `working-effectively-with-legacy-code/...` | **Deferred** by section 2a (no running system yet) |

> All 14 rule sets in the repo are accounted for here: four the strategies rest on, plus
> ten the altitude fence defers (the eight named in earlier drafts of `strategies.md` plus
> The Pragmatic Programmer and Refactoring.Guru). The Pragmatic Programmer is the exception  - 
> it is a *positive* source (S6/S5), not a deferred one.

---

## B. Per-element source map

### Diagnosis D1-D4 and the section 1 "don't compress" principle

`strategies.md` section 1 anchors the diagnosis in Ousterhout: *complexity is structural, not
size*; the cost is **cognitive load**; the four gaps are document-forms of his named
complexity symptoms (D1 ~= change amplification, D2/D3 ~= cognitive load, D4 ~= hidden
dependencies). Currently cited as "APOSD, section 5" (the book's chapter numbering).

**Local source - APOSD** (`a-philosophy-of-software-design/a-philosophy-of-software-design.md`):
- **"Primary Directive"** (lines 21-33) - *"Complexity is anything that makes software hard
  to understand or hard to change... Do not optimize for shorter files, fewer lines, or
  clever compactness if complexity rises."* -> direct anchor for **"don't compress; restructure."**
- **"Core Complexity Rules -> Symptoms of Complexity"** (lines 38-45) - the named symptom
  list: *change amplification, cognitive load, unknown unknowns, hidden dependencies,
  information spread across many places, temporal coupling.* -> the literal mapping for
  **D1 (change amplification), D2/D3 (cognitive load), D4 (hidden dependencies).**
- **"Combine or Separate Code"** (lines 231-243) and **"Module Depth Rules"** (lines 57-78)
  - the deep-vs-shallow test reused by S5.

> Note: the local file has no "section 5" numbering; the strategies.md citation "APOSD section 5" refers
> to the book's chapters, not the rule file. The rule-file anchors above are the local
> equivalents.

---

### S1 - Factor cross-cutting constraints into an invariants doc *(answers D1)*

`strategies.md` cites: [Wikipedia: Cross-cutting concern] - "Clean Architecture (Martin), section 5".

**Local source - Clean Architecture** (`clean-architecture/clean-architecture.md`):
- **Rule 2 "Keep Business Rules Pure"** (lines 26-30) and **Rule 3 "Treat Frameworks as
  Details"** (31-35) - business policy stated independently of framework/transport/storage.
  -> the exact basis for *"invariants = tech-free business policy, stated once."*
- **Rule 9 "Entities Must Guard Invariants"** (61-64) - invariants are first-class,
  centrally owned rules, not scattered into handlers.
- **"Architecture Economics and Priority"** (257-264) - *"Preserve options... until evidence
  justifies commitment"* -> supports keeping the invariants tech-free at planning altitude.

**External (already cited):** [Wikipedia: Cross-cutting concern](https://en.wikipedia.org/wiki/Cross-cutting_concern).

- **Gap:** no `agent-rules-books` document covers *cross-cutting concerns / AOP* directly  - 
  that leg of S1 is external-only. The original named source is Kiczales et al. on
  Aspect-Oriented Programming (see section C). **`missing in strategies.md`** (optional enrichment).

---

### S2 - Cluster use-cases into a capability map *(answers D2)*

`strategies.md` cites: [Wikipedia: Use case] - [Wikipedia: DDD]. The actor split "echoes DDD
bounded contexts."

**Local source - DDD Distilled** (`domain-driven-design-distilled/domain-driven-design-distilled.md`):
- **"Strategic Rules -> Define Bounded Contexts Early"** (lines 61-66) - each actor
  relationship as a candidate context boundary.
- **"Strategic Rules -> Start with Subdomains"** (50-60) - the cluster-then-classify move S2
  sets up and S7 completes.

**Local source - DDD / Evans** (`domain-driven-design/domain-driven-design.md`):
- **"Bounded Contexts"** (lines 223-242) - a model is valid only inside its context;
  single-user vs. team/manager is a boundary, not one shared model.
- **"Associations and Modules"** (443-466) - *"Organize modules around model meaning, not
  only technical layers"* -> cluster by capability, not by feature/tech.

**External (already cited):** [Wikipedia: Use case](https://en.wikipedia.org/wiki/Use_case)  - 
[Wikipedia: Domain-driven design](https://en.wikipedia.org/wiki/Domain-driven_design).

- **Gap:** *use-case / actor modelling (UML/RUP lineage)* has no local rule-set source - it
  is external-only and remains so (no book in the repo covers UML/RUP). Noted for completeness.

---

### S3 - Establish a glossary / ubiquitous language *(answers D3)*

`strategies.md` cites: [DDD Reference PDF (Evans)] - "DDD Distilled (Vernon), section 5", and quotes
two rules from Distilled: (a) one concept -> one term, one term not two meanings *within a
context*; (b) same word in different contexts is potentially a different concept.

**Local source - DDD Distilled** (`domain-driven-design-distilled/domain-driven-design-distilled.md`):
- **"Ubiquitous Language Rules"** (lines 112-124) - rule 2 *"One concept gets one term"* and
  rule 3 *"One term must not carry multiple meanings inside one context"* -> strategies.md
  rule (a), verbatim source.
- **"Strategic Rules -> Define Bounded Contexts Early"** (line 64) - *"The same term may mean
  different things in different contexts"* -> strategies.md rule (b), verbatim source.

**Local source - DDD / Evans** (`domain-driven-design/domain-driven-design.md`):
- **"Ubiquitous Language"** (lines 144-164) - rules 2-3: one name per concept, one name not
  two concepts, inside a bounded context. The canonical statement behind the glossary.
- **"Communication Artifacts"** (167-184) - glossary-like explanations kept close to the
  context they describe; documents must not drift from the code's vocabulary.

**External (already cited):** [DDD Reference PDF (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf).

---

### S4 - Build a traceability index (the spine) *(answers D4)*

`strategies.md` cites: [Perforce: RTM] - [Jama: Requirements traceability].

- **Local source: none.** No `agent-rules-books` document covers the Requirements
  Traceability Matrix - S4 is **external-only**, by nature (the repo is design/coding books,
  not requirements-engineering). This is expected, not a gap.
- **Adjacent local support:** DDD/Evans **"Model-Driven Design"** (lines 81-99) - the design
  must reflect the model used in discussion; documents that use different names than the code
  are an anti-pattern. This reinforces the spine's "cite back, don't drift" intent but is not
  the RTM source.
- **External (already cited):** [Perforce RTM](https://www.perforce.com/resources/alm/requirements-traceability-matrix)  - 
  [Jama: traceability](https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/what-is-traceability-12/).
- **External candidate:** **ISO/IEC/IEEE 29148** (named in section 4/section 5) formalizes the
  requirements/traceability side and would be the standards-grade citation for S4.

---

### S5 - Split by pipeline role, one concern per file *(structural strategy)*

`strategies.md` cites: [Wikipedia: Separation of concerns] - [Wikipedia: SRP] - "APOSD section 5"
(deep-module test).

**Local source - APOSD** (`a-philosophy-of-software-design/a-philosophy-of-software-design.md`):
- **"Module Depth Rules"** (lines 57-78) - deep vs. shallow; *"A module that only forwards
  work is usually too shallow."* -> the *"deep doc, not many tiny files"* test in S5.
- **"Information Hiding Rules"** (81-93) - each doc hides its internals behind a one-line
  purpose (the README as interface).
- **"Combine or Separate Code"** (231-243) - *"Separate code only when the separation reduces
  complexity... Combine code when split pieces force readers to jump between shallow fragments."*
  -> the rule that rejects pass-through docs.
- **Forbidden: "Shallow Decomposition"** (299-301) - splitting into tiny units that don't
  reduce understanding cost.

**Local source - Clean Architecture** (`clean-architecture/clean-architecture.md`):
- **"Paradigm and Component Rules", item 4** (line 273) - *"Apply SRP by separating code that
  changes for different actors or reasons."* -> the SRP leg, locally.
- **"Organize by Use Case"** (51-54) - split by role/use-case, not generic technical buckets
  -> reinforces "split by role in the pipeline, not by feature."

**Local source - The Pragmatic Programmer** (`the-pragmatic-programmer/the-pragmatic-programmer.md`):
- **"Orthogonality Rules"** (lines 83-93) - *"Keep components independent so one change does
  not force unrelated changes elsewhere... Separate policy from mechanism, data from
  presentation."* -> a named, reinforcing source for "one concern per file" alongside SoC/SRP.
  **`missing in strategies.md`** (S5 does not cite The Pragmatic Programmer / orthogonality).

**External (already cited):** [Wikipedia: Separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns)  - 
[Wikipedia: SRP](https://en.wikipedia.org/wiki/Single-responsibility_principle).

---

### S6 - Derive, never replace; cite back by stable ID *(integrity strategy)*

`strategies.md` says: *"Rests on the general single-source-of-truth discipline; the specific
layering here is bespoke."* - **with no named reference at all.**

**Local source - The Pragmatic Programmer** (`the-pragmatic-programmer/the-pragmatic-programmer.md`):
- **"DRY Rules"** (lines 64-79) - *"DRY means do not duplicate knowledge, not merely do not
  duplicate text. A business rule should have one authoritative representation."* -> this is
  the **canonical named source for single-source-of-truth**, which S6 currently leaves
  unattributed. The vision-as-canonical / derive-and-cite-back design *is* DRY-at-the-
  knowledge-level applied to documents. **`missing in strategies.md`** (high priority).

**Local source - DDD / Evans** (`domain-driven-design/domain-driven-design.md`):
- **"Model-Driven Design"** (lines 81-99) and **"Communication Artifacts"** (167-184)  - 
  derived documents must not drift from / contradict the canonical model; an anti-pattern is
  *"A design document that uses different names than the code."* -> reinforces "vision wins;
  fix the derived doc."

**External candidates (not in strategies.md):** [Wikipedia: Single source of truth](https://en.wikipedia.org/wiki/Single_source_of_truth)  - 
[Wikipedia: Don't repeat yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).
**`missing in strategies.md`**

---

### S7 - Classify subdomains and map context relationships *(deepens D2)*

`strategies.md` cites: [Wikipedia: DDD] - "DDD Distilled (Vernon), section 5" - [DDD Reference PDF
(Evans)]. Two pieces: (1) subdomain class Core/Supporting/Generic; (2) context-map vocabulary
**Partnership, Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host Service, Published
Language, Separate Ways**.

**Local source - DDD Distilled** (`domain-driven-design-distilled/domain-driven-design-distilled.md`):
- **"Strategic Rules -> Start with Subdomains"** (lines 50-60) - *core / supporting / generic*
  classification + "invest the most design effort in the core domain." -> S7 part 1, verbatim.
- **"Context Relationship Rules"** (lines 80-98) - the **complete** vocabulary: Partnership,
  Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host Service,
  Published Language, Separate Ways (+ Big Ball of Mud). -> S7 part 2, exact match.
  - **Important:** *Partnership* appears **only** in DDD Distilled (Vernon), **not** in
    Evans' blue book. So Distilled is the *required* local source for S7's full list - Evans
    alone is insufficient. (Verified: "Partnership" occurs only in the Distilled files.)

**Local source - DDD / Evans** (`domain-driven-design/domain-driven-design.md`):
- **"Strategic Design -> Core Domain / Supporting and Generic Subdomains / Context Mapping"**
  (lines 245-266).
- **"Model Integrity Patterns -> Context Relationships"** (276-302) - Shared Kernel,
  Customer/Supplier, Conformist, ACL, Separate Ways, Open Host Service, Published Language
  (the Evans subset; no Partnership).
- **"Distillation"** (305-330) - Core Domain, **Generic Subdomain**, and the distillation
  patterns: **`Domain Vision Statement`** (line 314), **Highlighted Core**, **Segregated
  Core**, **Abstract Core**.
  - **Connection worth naming:** a foundation vision *is* Evans' **Domain Vision Statement**
    ("a short statement of the core model's purpose"), and S7's Core/Supporting/Generic tag is
    Evans' **Highlighted/Segregated Core** applied to the capability map. `strategies.md` never
    names these constructs, though they are the precise DDD lineage for the whole skill.
    **`missing in strategies.md`** (enrichment).

**External (already cited):** [Wikipedia: DDD](https://en.wikipedia.org/wiki/Domain-driven_design)  - 
[DDD Reference PDF (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf).

---

### S8 - Route every parked item to its downstream phase *(coverage strategy)*

`strategies.md` says S8 *"rests on the RTM coverage discipline (S4) extended to parked items,
bounded by the altitude fence (section 2a)."*

- **Local source:** none new - inherits S4 (no-orphans / RTM) and the section 2a fence. Same
  external RTM citations as S4 apply.
- The "fold cross-cutting BV items into invariants" half inherits S1's Clean Architecture
  anchors (policy stated once).

---

### section 2a - The altitude fence (deferred sources)

The fence borrows only the **strategic-design** layer and defers everything at
code-construction or runtime altitude. `strategies.md` section 2a now states the fence as the
*categories* to exclude; this table is the book-level backing for each category. Each
deferred source has a local copy:

| Deferred to | Source (book) | Local file & relevant parts |
|-------------|---------------|------------------------------|
| Architecture phase | **Tactical DDD** | `implementing-domain-driven-design/implementing-domain-driven-design.mini.md` - Aggregates (decision rules 18-19), Entities (20), Value Objects (21), Domain Events (24), Event Sourcing (25), Application Services (26). Also Evans tactical half: `domain-driven-design/domain-driven-design.md` "Entities" (386-411), "Value Objects" (414-441), "Aggregates" (470-493), "Domain Services" (496-518), "Repositories" (542-569), "Factories" (572-592), "Application Layer" (593-615). |
| Architecture phase | **Clean Architecture *rules*** | `clean-architecture/clean-architecture.md` - "Non-Negotiable Rules -> Follow the Dependency Rule" (21-25), "Use Explicit Boundaries" / ports (46-50), "Create Ports for Volatile Dependencies" (182-193), "Keep Wiring in the Main Component" = composition root (195-199). Only the *policy-independence principle* is at-altitude (S1); these mechanics are downstream. |
| Architecture phase | **Designing Data-Intensive Applications** | `designing-data-intensive-applications/designing-data-intensive-applications.mini.md` - source-of-truth & ownership (decision rule 13-16), derived-data propagation (18), write/consistency semantics (19), schema/contract evolution (23), replication & partitioning (24-25). Feeds the architecture docs the bundle *produces*. |
| Build / review phase | **Clean Code** | `clean-code/clean-code.mini.md` - names/functions/comments, local reasoning (decision rules 14-25). Code altitude; no code exists yet. |
| Build / review phase | **Code Complete** | `code-complete/code-complete.mini.md` - construction discipline, routines, data, control flow (decision rules 13-32). |
| Build / review phase | **PEAA** | `patterns-of-enterprise-application-architecture/...mini.md` - layering, Domain Model vs Transaction Script, Repository/Data Mapper/Unit of Work (decision rules 13-31). |
| Build / review phase | **Refactoring** | `refactoring/refactoring.mini.md` - behavior-preserving transforms, smells (decision rules 13-27). |
| Build / review phase | **Release It!** | `release-it/release-it.mini.md` - timeouts, circuit breakers, bulkheads, back-pressure, observability (decision rules 13-28). Production-operations altitude. |
| Build / review phase | **Working Effectively with Legacy Code** | `working-effectively-with-legacy-code/...mini.md` - seams, characterization tests, dependency breaking (decision rules 13-28). Presupposes a running system. |
| Build / review phase | **Refactoring.Guru** | `refactoring-guru/refactoring-guru.mini.md` - smell catalog + treatment selection (decision rules 13-37). Same altitude as Refactoring; covered by the fence's *Code & operations* category. |

---

### Candidate formal standards (noted in earlier `strategies.md` section 4/section 5; no local source)

**ISO/IEC/IEEE 29148** (requirements), **arc42** (architecture-doc template), **C4 model**
(diagrams). None are in `agent-rules-books`; they are external standards, listed as *candidates*
for a future formalization rather than dependencies of the current method. URLs:
- ISO/IEC/IEEE 29148:2018 - ISO catalogue (paywalled): https://www.iso.org/standard/72089.html
- arc42 - https://arc42.org/
- C4 model - https://c4model.com/

---

## C. External (web) sources behind the strategies

Consolidated here so the skill files stay outcome-focused. The first group was cited inline in
earlier `strategies.md`; the second is additional canonical provenance, deliberately **not**
inlined (doing so would reintroduce no-benefit citations). Verify URLs before reuse.

**Cited in earlier `strategies.md`:**

- DDD Reference (Evans): https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
- Wikipedia: Domain-driven design - https://en.wikipedia.org/wiki/Domain-driven_design
- Wikipedia: Cross-cutting concern - https://en.wikipedia.org/wiki/Cross-cutting_concern
- Wikipedia: Use case - https://en.wikipedia.org/wiki/Use_case
- Wikipedia: Separation of concerns - https://en.wikipedia.org/wiki/Separation_of_concerns
- Wikipedia: Single-responsibility principle - https://en.wikipedia.org/wiki/Single-responsibility_principle
- Perforce: Requirements Traceability Matrix - https://www.perforce.com/resources/alm/requirements-traceability-matrix
- Jama: Requirements traceability - https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/what-is-traceability-12/

**Additional canonical (provenance only - section A/section B note which strategy each backs):**

- Single source of truth - https://en.wikipedia.org/wiki/Single_source_of_truth
- Don't repeat yourself - https://en.wikipedia.org/wiki/Don%27t_repeat_yourself
- Aspect-oriented programming (Kiczales et al.; origin of "cross-cutting concern") - https://en.wikipedia.org/wiki/Aspect-oriented_programming
- Fowler bliki: [BoundedContext](https://martinfowler.com/bliki/BoundedContext.html) - [UbiquitousLanguage](https://martinfowler.com/bliki/UbiquitousLanguage.html)
- Amazon "Working Backwards" / PR-FAQ (Bryar & Carr, *Working Backwards*; Werner Vogels) - origin of the press-release vision format; an input to the upstream `brainstorm-vision` skill, noted as context.
