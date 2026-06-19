# Vision → Planning: Conversion Strategies

> **Status: working draft, to be refined in a later session.**
>
> **What this is.** A catalogue of the strategies for converting a finalized
> `*-foundation-vision.md` (a human, divergent, plain-language press-release +
> flat use-case list) into the **planning-phase document bundle** an AI agent
> uses to produce architecture, requirements, and an implementation plan.
>
> This is the *methodology* behind the concrete plan in
> [ai-friendly-vision-plan.md](ai-friendly-vision-plan.md) and the pilot bundle it
> produced (`ai-mail.pocock/docs/brainstorming/ai-mail-vision-ai-spec/`). The plan
> says *what to build for ai-mail*; this file says *why those strategies, and what
> recognized practice each rests on*.
>
> Created: 2026-06-19.

---

## 0. How the conversion was decided (the meta-strategy)

There is **no single official, named methodology** for this. The approach is a
**synthesis of recognized building blocks, driven by a structural diagnosis** of
what makes a vision document hard for a build-phase agent to consume. The chain:

1. **Diagnose the structural gaps** between "good for a human reader" and "good
   for a planning agent."
2. **Pick one recognized practice per gap** — each derived document answers
   exactly one diagnosed problem.
3. **Bind it all with a traceability spine** so nothing is invented and nothing
   is lost, and the original vision stays the single source of truth.

> **To refine later:** decide whether to additionally conform the output to a
> *formally citable* standard (see §4). Right now the bundle is principled but
> bespoke.
>
> **Refinement 2026-06-19:** reviewed against the `agent-rules-books` rule-sets
> (`pocock/agent-rules-books/`). Only the **strategic-design layer** was folded in
> — DDD subdomains + context mapping (new S7), with APOSD and Clean Architecture
> cited as anchors for principles S1/S5/§1 already applied implicitly. Tactical
> DDD, Clean Architecture mechanics, data-intensive design, and all
> code-construction/operations rule-sets were deliberately **deferred** — see the
> altitude fence in §2a.

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

> **Anchor (added in refinement):** this is exactly Ousterhout's thesis in *A
> Philosophy of Software Design* — *complexity is structural, not size*; the cost
> that matters is **cognitive load** (how many facts a reader must hold at once),
> not line count. The four gaps above are the document forms of his named
> complexity symptoms: D1 ≈ *change amplification / repeated reasoning*, D2/D3 ≈
> *high cognitive load*, D4 ≈ *hidden dependencies*. So "don't compress, restructure"
> is the SoD principle applied to a document. (Ref: APOSD, §5.)

---

## 2. The strategies (one per gap) and the practice each rests on

Each strategy is a recognized practice. They were **assembled**, not lifted from
one combined standard.

### S1 — Factor cross-cutting constraints into an invariants doc  *(answers D1)*
Pull the rules that touch every capability (approval gate, non-destructive,
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
- **Now sharpened by S7:** the clustering used to be a free *reading* of the list.
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
  rather than forcing one shared definition. For a single-context pilot this collapses
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

### S7 — Classify subdomains and map context relationships  *(answers D2 depth; partly answers the phasing gap)*
On top of the S2 capability map, add two pieces of **strategic-design** structure
from DDD — the layer that lives at the planning altitude, *not* tactical DDD:

1. **Subdomain classification.** Tag each capability/cluster as **Core**,
   **Supporting**, or **Generic**.
   - *Core* = the differentiating reason the product exists; concentrate modeling
     and design effort here.
   - *Supporting* = needed but not differentiating; keep simple.
   - *Generic* = solved problems (auth, storage); prefer buy/adopt over modelling.
   This is the single most useful thing the books add: it converts the flat,
   priority-free map into an **investment/attention ordering** without smuggling
   MVP-scoping or tech into the vision (the vision stays priority-free; the
   *classification* is a derived, citable judgment).

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
  no-architecture-in-the-vision discipline. See the fence in §3a.
- **Refs:** [Wikipedia: DDD](https://en.wikipedia.org/wiki/Domain-driven_design) ·
  DDD Distilled (Vernon), §5 ·
  [DDD Reference PDF (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)

---

## 2a. The altitude fence (what was deliberately left out)

The enhancement pulls only the **strategic-design** layer from the DDD books and
the *principles* (not the rules) from APOSD and Clean Architecture. Everything
below was evaluated and **deliberately deferred to a later phase**, because it
operates at the code-construction or runtime altitude and would contradict the
vision's no-tech/no-architecture discipline if pulled in now:

| Deferred to | Source | Why not now |
|-------------|--------|-------------|
| Architecture phase | Tactical DDD (Aggregates, Entities, Value Objects, Domain Events, Application Services — *Implementing DDD*) | Implementation shape; downstream of the capability/subdomain map. |
| Architecture phase | Clean Architecture *rules* (dependency rule, ports/adapters, composition root) | Only the *policy-independence principle* is at-altitude (see S1); the mechanics are downstream. |
| Architecture phase | Designing Data-Intensive Applications (ownership, consistency, event flow, schema evolution) | Genuinely relevant to ai-mail's invariants, but feeds the *architecture docs the bundle produces*, not the conversion method. |
| Build / review phase | Clean Code, Code Complete, PEAA, Refactoring, Refactoring.Guru, Release It!, Working Effectively with Legacy Code | Code-construction or production-operations altitude; no code or running system exists yet. |

---

## 3. What is bespoke judgment, not standard

Be honest about where discretion replaced rule — these are the parts most worth
refining later:

- **The specific clusters, the primary/secondary assignments, and the exact set
  of invariants** are a *reading* of the source use-cases, not an output of any
  method. S7's subdomain classification and context-map vocabulary make the
  clustering *more* repeatable (two readers now share a fixed taxonomy and a
  Core/Supporting/Generic test) but do **not** make it deterministic — what counts
  as the Core Domain is still a judgment call.
- **Refusing to compress the emotional vision** is a deliberate call, not a
  documented practice — the opposite (terse specs) is arguably more conventional.
  (APOSD's cognitive-load argument is the principled defense, but the call predates
  the citation.)
- **The exact bundle shape** (which files, the README load-order) is assembled
  judgment, not a named template.

### 3a. The altitude fence as a standing rule

Beyond the per-doc judgment above, the enhancement adds one *integrity* rule worth
stating explicitly: **borrow only the strategic-design layer.** When a later session
is tempted to pull a tactical pattern (an Aggregate boundary, a port, a consistency
model) into the planning bundle, that is altitude leakage — it belongs to the phase
the bundle *feeds*, not the conversion. The §2a fence is the record of what was
consciously left out and where it goes next.

---

## 4. Open questions to resolve when refining

1. **Adopt a formal, citable standard on top?** Candidates to evaluate:
   - **ISO/IEC/IEEE 29148** — requirements engineering (would formalize the
     requirements/traceability side).
   - **arc42** — architecture documentation template (would formalize the
     downstream architecture docs the bundle feeds).
   - **C4 model** — for the architecture-diagram layer later.
   Decide whether conforming buys enough to be worth the rigidity.
2. **How prescriptive should the clustering method be?** *(partly resolved by S7.)*
   S7 adds a fixed taxonomy — subdomain class (Core/Supporting/Generic) + context-map
   relationship — that makes clustering more repeatable across runs and visions.
   Remaining open: whether to add explicit *heuristics* for drawing the initial
   cluster lines (S2), which is still a free reading.
3. **A machine-readable layer?** The pilot is markdown-first. When a real
   programmatic consumer appears, mirror the index as YAML/JSON.
4. **Priority / phasing.** *(partly resolved by S7.)* The vision stays
   priority-free, but S7's Core/Supporting/Generic classification is itself a derived
   *attention/investment* ordering — a soft prioritization that doesn't touch the
   vision. Remaining open: whether a separate, harder *phasing/roadmap* artifact
   (sequence, MVP cut) belongs in this pipeline or in the planning phase after it.
5. **Generalize into a companion skill?** If these strategies hold up across more
   than the ai-mail pilot, fold them into a `vision-to-spec` skill so every
   foundation vision gets the same treatment.

---

## 5. Reference summary

- DDD / Ubiquitous Language / Strategic Design: [DDD Reference (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) · [Wikipedia: DDD](https://en.wikipedia.org/wiki/Domain-driven_design) · DDD Distilled (Vernon) — subdomains (Core/Supporting/Generic) & context mapping
- Cognitive load / structural complexity / deep modules: *A Philosophy of Software Design* (Ousterhout) — anchors §1 ("don't compress") and S5 (deep docs)
- Policy independent of detail: *Clean Architecture* (Martin) — anchors S1 (invariants = tech-free business policy)
- Cross-cutting concerns: [Wikipedia](https://en.wikipedia.org/wiki/Cross-cutting_concern)
- Requirements Traceability Matrix: [Perforce](https://www.perforce.com/resources/alm/requirements-traceability-matrix) · [Jama](https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/what-is-traceability-12/)
- Separation of Concerns / SRP: [SoC](https://en.wikipedia.org/wiki/Separation_of_concerns) · [SRP](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- Use-case modelling: [Wikipedia: Use case](https://en.wikipedia.org/wiki/Use_case)
- Book rule-sets used (strategic-design layer only): `pocock/agent-rules-books/` — `domain-driven-design-distilled`, `domain-driven-design`, `a-philosophy-of-software-design`, `clean-architecture`. See §2a for what was deferred and why.
- Candidate formal standards (to evaluate): ISO/IEC/IEEE 29148 (requirements), arc42 (architecture docs), C4 model (diagrams)
