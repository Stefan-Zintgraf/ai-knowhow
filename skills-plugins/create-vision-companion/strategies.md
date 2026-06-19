# Vision → Planning: Conversion Strategies

**What this is.** The methodology for converting a finalized
`*-foundation-vision.md` (a human, divergent, plain-language press-release, a flat
use-case list, and an optional parking-lot of out-of-scope items) into the
**planning-phase companion bundle** an AI agent uses to produce architecture,
requirements, and an implementation plan.

There is no single official, named methodology for this. The approach is a
**synthesis of recognized building blocks, driven by a structural diagnosis** of
what makes a vision document hard for a build-phase agent to consume. The chain:

1. **Diagnose the structural gaps** between "good for a human reader" and "good
   for a planning agent."
2. **Pick one recognized practice per gap** — each derived document answers
   exactly one diagnosed problem.
3. **Bind it all with a traceability spine** so nothing is invented and nothing
   is lost, and the original vision stays the single source of truth.

The output is principled but bespoke. It does not yet conform to a formally
citable standard (see §5 for candidates), and it deliberately borrows only the
**strategic-design layer** of the source disciplines — see the altitude fence in
§2a.

---

## 1. The diagnosis (what's wrong with a vision for an agent)

The vision is deliberately optimized for a **human**: narrative, emotional, one
flat list, plain language, no structure. For a planning agent that creates four
specific frictions — and the friction is **structural, not length**:

| # | Gap in the vision | Consequence for the agent |
|---|-------------------|---------------------------|
| D1 | Cross-cutting constraints restated in nearly every use-case | Noise + risk of inconsistent re-derivation; the load-bearing rules are buried in repetition |
| D2 | No clustering — a long flat list of use-cases | Agent must re-cluster every run, possibly differently each time |
| D3 | No consistent terminology — same concept named many ways | No ubiquitous language to carry into code/schemas; ambiguity |
| D4 | No traceability — stable IDs exist but map to nothing | Can't trace a requirement back to intent, or forward from a use-case |

**Key principle that falls out of the diagnosis:** *don't compress the vision.*
Token count isn't the bottleneck; structure is. The emotional framing is cheap
insurance against locally-clever, globally-wrong design choices. So the strategy
is **derive a companion bundle, never edit the vision down.**

**Companion principle — total coverage.** The companion set, not the vision, is
the working input to the next phase, so *every* item in the vision must resolve to
at least one place in the bundle: each press-release claim, each use-case (`UC#`),
and each parked item (`BV#`). Nothing in the vision may be left without a home —
an item with no companion location would silently vanish from the build phase. The
vision stays canonical for arbitration (S6); the bundle stays complete enough to
stand on its own.

This is Ousterhout's thesis in *A Philosophy of Software Design* — *complexity is
structural, not size*; the cost that matters is **cognitive load** (how many facts
a reader must hold at once), not line count. The four gaps are the document forms
of his named complexity symptoms: D1 ≈ *change amplification / repeated
reasoning*, D2/D3 ≈ *high cognitive load*, D4 ≈ *hidden dependencies*. "Don't
compress, restructure" is the Separation-of-Design principle applied to a
document. (Ref: APOSD, §5.)

---

## 2. The strategies (one per gap) and the practice each rests on

Each strategy is a recognized practice. They are **assembled**, not lifted from
one combined standard.

### S1 — Factor cross-cutting constraints into an invariants doc  *(answers D1)*
Pull the rules that touch every capability (e.g. approval gate, non-destructive,
transparency, audit, ownership, progressive autonomy, boundaries, acts-in-real-name)
into a single document, stated once, referenced by ID everywhere else.
- **Rests on:** *Cross-cutting concerns* — the scattering/tangling problem that
  aspect-oriented design names and solves by extracting the concern. Reinforced by
  *Clean Architecture* (Martin): the invariants are **business policy**, and policy
  must be stated independently of detail — "do not let details become the
  architecture." An invariants doc is the planning-phase form of policy-independence:
  the load-bearing rules live in one place, free of any framework, storage, or
  transport commitment, exactly as the vision keeps tech out.
- **Refs:** [Wikipedia: Cross-cutting concern](https://en.wikipedia.org/wiki/Cross-cutting_concern) ·
  Clean Architecture (Martin), §5

### S2 — Cluster use-cases into a capability map  *(answers D2)*
Group the flat list into capabilities; assign each use-case **one primary**
capability (+ noted secondaries); list actors separately.
- **Rests on:** *Use-case / actor modelling* (UML/RUP lineage); the actor split
  also echoes DDD *bounded contexts* (each actor relationship is a candidate
  context boundary, e.g. single-user vs. team/manager).
- **Sharpened by S7:** the clustering is otherwise a free *reading* of the list.
  S7 makes it more repeatable — classify each cluster's subdomain (Core / Supporting
  / Generic) and name the relationship at each actor boundary using DDD's context-map
  vocabulary. S2 produces the clusters; S7 classifies and connects them.
- **Refs:** [Wikipedia: Use case](https://en.wikipedia.org/wiki/Use_case) ·
  [Wikipedia: DDD](https://en.wikipedia.org/wiki/Domain-driven_design)

### S3 — Establish a glossary / ubiquitous language  *(answers D3)*
One canonical term per concept; each term absorbs the vision's many synonyms.
Use these terms in all downstream code, schemas, and docs.
- **Rests on:** *Ubiquitous Language* from Domain-Driven Design (Eric Evans),
  reinforced by *DDD Distilled* (Vernon). Two rules from Distilled tighten this:
  (a) **one concept gets one term, and one term does not carry two meanings inside a
  context** — so the glossary is per-context, not global; (b) the *same word in
  different contexts is potentially a different concept* — translate at the boundary
  rather than forcing one shared definition. For a single-context vision this collapses
  to one glossary, but the rule is what scales it when team/manager contexts split off.
- **Refs:** [DDD Reference PDF (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) ·
  DDD Distilled (Vernon), §5

### S4 — Build a traceability index (the spine)  *(answers D4)*
One row per use-case → actor · capability · invariants · normalized one-liner ·
link back to the source line. Plus a reverse index (capability → use-cases).
- **Rests on:** *Requirements Traceability Matrix (RTM)* — maps each requirement
  to its source and dependent artifacts, giving audit-ready forward/back paths.
- **Refs:** [Perforce: RTM](https://www.perforce.com/resources/alm/requirements-traceability-matrix) ·
  [Jama: Requirements traceability](https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/what-is-traceability-12/)

### S5 — Split by pipeline role, one concern per file  *(structural strategy)*
The bundle is many small docs, each owning one concern, plus a README entry
point. Split by *role in the downstream pipeline* (so an agent loads only the
slice a task needs), **not** by feature.
- **Rests on:** *Separation of Concerns / Single-Responsibility Principle*,
  applied to documents rather than code. Sharpened by APOSD's *deep module* test:
  a split is only worth it if the new boundary **hides more complexity than it adds**.
  So the rule isn't "many small files" — it's "each file is a deep doc with a
  semantic name and a self-contained concern." Reject pass-through docs and tiny
  split-outs that add a filename without reducing what a task must load. The README
  is the *interface*; each doc hides its internals behind a one-line purpose.
- **Refs:** [Wikipedia: Separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) ·
  [Wikipedia: SRP](https://en.wikipedia.org/wiki/Single-responsibility_principle) ·
  APOSD (Ousterhout), §5

### S6 — Derive, never replace; cite back by stable ID  *(integrity strategy)*
The vision stays canonical and untouched. Every derived claim traces to ≥1
use-case ID; if a derived doc and the vision disagree, the vision wins.
- **Rests on:** the general *single-source-of-truth* discipline; the specific
  layering here is bespoke.

### S7 — Classify subdomains and map context relationships  *(deepens D2; partly answers the phasing gap)*
On top of the S2 capability map, add two pieces of **strategic-design** structure
from DDD — the layer that lives at the planning altitude, *not* tactical DDD:

1. **Subdomain classification.** Tag each capability/cluster as **Core**,
   **Supporting**, or **Generic**.
   - *Core* = the differentiating reason the product exists; concentrate modeling
     and design effort here.
   - *Supporting* = needed but not differentiating; keep simple.
   - *Generic* = solved problems (auth, storage); prefer buy/adopt over modelling.
   This converts the flat, priority-free map into an **investment/attention
   ordering** without smuggling MVP-scoping or tech into the vision (the vision
   stays priority-free; the *classification* is a derived, citable judgment).

2. **Context-map relationships.** Where S2 noted that each actor relationship is a
   *candidate* context boundary, S7 names the relationship with DDD's vocabulary —
   **Partnership, Shared Kernel, Customer/Supplier, Conformist, Anticorruption
   Layer (ACL), Open Host Service, Published Language, Separate Ways**. Each choice
   carries explicit ownership and translation duties downstream (e.g. single-user
   vs. team/manager, or the boundary with an external mail provider → likely
   Conformist or ACL).

- **Output:** a short `subdomains-and-context-map.md` — a table (capability →
  subdomain class → rationale → use-case IDs) plus a context-relationship list
  (boundary → relationship type → who owns the language → translation needed?).
  Every row cites use-case IDs per S6.
- **Rests on:** *Strategic Design* in DDD — subdomains and context mapping (Evans,
  strategic half; Vernon, *DDD Distilled*). **Explicitly excludes** tactical
  patterns (Aggregates, Entities, Value Objects, Domain Events, Application
  Services) — those are downstream of planning and would violate the
  no-architecture-in-the-vision discipline. See the fence in §2a.
- **Refs:** [Wikipedia: DDD](https://en.wikipedia.org/wiki/Domain-driven_design) ·
  DDD Distilled (Vernon), §5 ·
  [DDD Reference PDF (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)

### S8 — Route every parked item to its downstream phase; drop nothing  *(coverage strategy)*
The vision may carry a parking lot of out-of-scope items (`BV1…`) — integrations
and other-tool interop, hard constraints (offline, privacy, scale), tech/platform
leanings, MVP/scoping calls, remembered edge cases. These are precisely the
build-phase thinking the vision deliberately kept out, captured so it isn't lost.
Many visions park nothing and have no `BV` items at all; when they exist, the
companion set is now the main input to the phase that consumes them, so none may
be dropped. Route each `BV` item by type, **citing it by `BV` ID**:

- **Cross-cutting constraints the build must honor** (e.g. must-work-offline,
  data-stays-on-device, scale) → fold into the **invariants doc (S1)** as
  first-class invariants, cited by `BV` ID alongside any asserting `UC` IDs.
- **Everything else** (integrations, tech/platform leanings, scoping calls, edge
  cases) → a dedicated holding doc (`parking-lot.md` / `deferred-inputs.md`), each
  item tagged with the downstream phase that consumes it (architecture / design /
  scoping). The bundle **preserves and routes** these; per the altitude fence
  (§2a) it does **not** design from them or promote them into the capability map.

Every `BV` item must land in exactly one of these homes — the same no-orphans rule
S4 applies to use-cases, extended to the parking lot.
- **Rests on:** the RTM coverage discipline (S4) extended to parked items, bounded
  by the altitude fence (§2a).

---

## 2a. The altitude fence (what to leave out)

The method pulls only the **strategic-design** layer from DDD and the *principles*
(not the rules) from APOSD and Clean Architecture. Everything below operates at
the code-construction or runtime altitude and would contradict the vision's
no-tech/no-architecture discipline if pulled into the bundle — defer it to the
phase the bundle *feeds*:

| Deferred to | Source | Why not in the bundle |
|-------------|--------|-----------------------|
| Architecture phase | Tactical DDD (Aggregates, Entities, Value Objects, Domain Events, Application Services — *Implementing DDD*) | Implementation shape; downstream of the capability/subdomain map. |
| Architecture phase | Clean Architecture *rules* (dependency rule, ports/adapters, composition root) | Only the *policy-independence principle* is at-altitude (see S1); the mechanics are downstream. |
| Architecture phase | Designing Data-Intensive Applications (ownership, consistency, event flow, schema evolution) | Feeds the *architecture docs the bundle produces*, not the conversion method. |
| Build / review phase | Clean Code, Code Complete, PEAA, Refactoring, Release It!, Working Effectively with Legacy Code | Code-construction or production-operations altitude; no code or running system exists yet. |

**Standing rule: borrow only the strategic-design layer.** When tempted to pull a
tactical pattern (an Aggregate boundary, a port, a consistency model) into the
planning bundle, that is altitude leakage — it belongs to the phase the bundle
*feeds*, not the conversion. Parked (`BV#`) tech/architecture leanings are subject
to the same fence: the bundle **carries them forward** to the phase that consumes
them (S8), it does not act on them.

---

## 3. Where judgment is required (not standard)

These parts are discretion, not rule — flag them as judgment calls in the output:

- **The specific clusters, the primary/secondary assignments, and the exact set
  of invariants** are a *reading* of the source use-cases, not an output of any
  method. S7's subdomain classification and context-map vocabulary make the
  clustering *more* repeatable (a fixed taxonomy and a Core/Supporting/Generic
  test) but not deterministic — what counts as the Core Domain is still a judgment
  call.
- **Refusing to compress the emotional vision** is a deliberate call; the opposite
  (terse specs) is arguably more conventional. APOSD's cognitive-load argument is
  the principled defense.
- **The exact bundle shape** (which files, the README load-order) is assembled
  judgment, not a named template.

---

## 4. Considerations when scaling beyond a single vision

- **Clustering heuristics (S2).** S7 fixes a taxonomy (subdomain class +
  context-map relationship) that makes clustering more repeatable. Drawing the
  initial cluster lines is still a free reading; explicit heuristics for that step
  could tighten it further.
- **A machine-readable layer.** The bundle is markdown-first. When a real
  programmatic consumer appears, mirror the traceability index as YAML/JSON.
- **Priority / phasing.** The vision stays priority-free; S7's
  Core/Supporting/Generic classification is itself a derived *attention/investment*
  ordering — a soft prioritization that doesn't touch the vision. A harder
  *phasing/roadmap* artifact (sequence, MVP cut) belongs in the planning phase
  *after* this pipeline, not in the bundle.
- **Formal standards.** Whether to conform the output to a formally citable
  standard is a trade-off of rigor vs. rigidity. Candidates: **ISO/IEC/IEEE 29148**
  (requirements engineering — formalizes the requirements/traceability side),
  **arc42** (architecture documentation template — formalizes the downstream
  architecture docs the bundle feeds), **C4 model** (architecture diagrams, later).

---

## 5. Reference summary

- DDD / Ubiquitous Language / Strategic Design: [DDD Reference (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) · [Wikipedia: DDD](https://en.wikipedia.org/wiki/Domain-driven_design) · DDD Distilled (Vernon) — subdomains (Core/Supporting/Generic) & context mapping
- Cognitive load / structural complexity / deep modules: *A Philosophy of Software Design* (Ousterhout) — anchors §1 ("don't compress") and S5 (deep docs)
- Policy independent of detail: *Clean Architecture* (Martin) — anchors S1 (invariants = tech-free business policy)
- Cross-cutting concerns: [Wikipedia](https://en.wikipedia.org/wiki/Cross-cutting_concern)
- Requirements Traceability Matrix: [Perforce](https://www.perforce.com/resources/alm/requirements-traceability-matrix) · [Jama](https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/what-is-traceability-12/)
- Separation of Concerns / SRP: [SoC](https://en.wikipedia.org/wiki/Separation_of_concerns) · [SRP](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- Use-case modelling: [Wikipedia: Use case](https://en.wikipedia.org/wiki/Use_case)
- Candidate formal standards: ISO/IEC/IEEE 29148 (requirements), arc42 (architecture docs), C4 model (diagrams)
