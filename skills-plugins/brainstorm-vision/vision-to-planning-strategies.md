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

---

## 2. The strategies (one per gap) and the practice each rests on

Each strategy is a recognized practice. They were **assembled**, not lifted from
one combined standard.

### S1 — Factor cross-cutting constraints into an invariants doc  *(answers D1)*
Pull the rules that touch every capability (approval gate, non-destructive,
transparency, audit, ownership, progressive autonomy, boundaries, acts-in-real-name)
into a single document, stated once, referenced by ID everywhere else.
- **Rests on:** *Cross-cutting concerns* — the scattering/tangling problem that
  aspect-oriented design names and solves by extracting the concern.
- **Refs:** [Wikipedia: Cross-cutting concern](https://en.wikipedia.org/wiki/Cross-cutting_concern)

### S2 — Cluster use-cases into a capability map  *(answers D2)*
Group the flat list into capabilities; assign each use-case **one primary**
capability (+ noted secondaries); list actors separately.
- **Rests on:** *Use-case / actor modelling* (UML/RUP lineage); the actor split
  also echoes DDD *bounded contexts* (each actor relationship is a candidate
  context boundary, e.g. single-user vs. team/manager).
- **Refs:** [Wikipedia: Use case](https://en.wikipedia.org/wiki/Use_case) ·
  [Wikipedia: DDD](https://en.wikipedia.org/wiki/Domain-driven_design)

### S3 — Establish a glossary / ubiquitous language  *(answers D3)*
One canonical term per concept; each term absorbs the vision's many synonyms.
Use these terms in all downstream code, schemas, and docs.
- **Rests on:** *Ubiquitous Language* from Domain-Driven Design (Eric Evans).
- **Refs:** [DDD Reference PDF (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)

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
  applied to documents rather than code.
- **Refs:** [Wikipedia: Separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) ·
  [Wikipedia: SRP](https://en.wikipedia.org/wiki/Single-responsibility_principle)

### S6 — Derive, never replace; cite back by stable ID  *(integrity strategy)*
The vision stays canonical and untouched. Every derived claim traces to ≥1
use-case ID; if a derived doc and the vision disagree, the vision wins.
- **Rests on:** the general *single-source-of-truth* discipline; the specific
  layering here is bespoke.

---

## 3. What is bespoke judgment, not standard

Be honest about where discretion replaced rule — these are the parts most worth
refining later:

- **The specific clusters, the primary/secondary assignments, and the exact set
  of invariants** are a *reading* of the source use-cases, not an output of any
  method. Two people applying RTM + DDD would still cluster differently.
- **Refusing to compress the emotional vision** is a deliberate call, not a
  documented practice — the opposite (terse specs) is arguably more conventional.
- **The exact bundle shape** (which files, the README load-order) is assembled
  judgment, not a named template.

---

## 4. Open questions to resolve when refining

1. **Adopt a formal, citable standard on top?** Candidates to evaluate:
   - **ISO/IEC/IEEE 29148** — requirements engineering (would formalize the
     requirements/traceability side).
   - **arc42** — architecture documentation template (would formalize the
     downstream architecture docs the bundle feeds).
   - **C4 model** — for the architecture-diagram layer later.
   Decide whether conforming buys enough to be worth the rigidity.
2. **How prescriptive should the clustering method be?** Right now it's
   judgment. Could add explicit clustering heuristics/rules to make it
   repeatable across visions and across runs.
3. **A machine-readable layer?** The pilot is markdown-first. When a real
   programmatic consumer appears, mirror the index as YAML/JSON.
4. **Priority / phasing.** Deliberately omitted (the vision omits it too).
   Decide whether a separate prioritization artifact belongs in this pipeline.
5. **Generalize into a companion skill?** If these strategies hold up across more
   than the ai-mail pilot, fold them into a `vision-to-spec` skill so every
   foundation vision gets the same treatment.

---

## 5. Reference summary

- DDD / Ubiquitous Language: [DDD Reference (Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) · [Wikipedia: DDD](https://en.wikipedia.org/wiki/Domain-driven_design)
- Cross-cutting concerns: [Wikipedia](https://en.wikipedia.org/wiki/Cross-cutting_concern)
- Requirements Traceability Matrix: [Perforce](https://www.perforce.com/resources/alm/requirements-traceability-matrix) · [Jama](https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/what-is-traceability-12/)
- Separation of Concerns / SRP: [SoC](https://en.wikipedia.org/wiki/Separation_of_concerns) · [SRP](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- Use-case modelling: [Wikipedia: Use case](https://en.wikipedia.org/wiki/Use_case)
- Candidate formal standards (to evaluate): ISO/IEC/IEEE 29148 (requirements), arc42 (architecture docs), C4 model (diagrams)
