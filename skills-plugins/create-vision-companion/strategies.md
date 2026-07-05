# Vision → Planning: Conversion Strategies

**What this is.** The method for converting a finalized `*-foundation-vision.md`
(a human, plain-language press-release vision — **scope items** `S#` and **vision
points** `V#` — a flat use-case list, and an optional parking-lot of out-of-scope
`BV` items) into the **planning-phase companion bundle** a build-phase agent uses to
produce architecture, requirements, and an implementation plan.

Three principles govern every decision below:

- **Don't compress the vision — restructure.** The bottleneck for an agent is *structure*,
  not token count. The emotional, narrative framing is cheap insurance against
  locally-clever, globally-wrong design — keep it. Produce a companion bundle; never edit
  the vision down.
- **Derive, never replace.** The vision stays byte-identical and canonical — the single
  source of truth. The bundle only *adds* derived docs that cite back by stable ID. If a
  derived doc and the vision disagree, the vision wins; fix the derived doc.
- **Total coverage — drop nothing.** The bundle, not the vision, is the working input to
  the next phase, so *every* item in the vision must resolve to at least one place in the
  bundle: each use-case (`UC#`), each vision point (`V#`, mapped to its realizing UCs or a
  flagged coverage gap), each scope item (`S#`, placed on the ladder), and each parked item
  (`BV#`). An item with no home would silently vanish from the build.

The provenance — the recognized practices and the book/web sources each strategy draws on,
plus open gaps — lives in [strategies_sources.md](strategies_sources.md). This file carries
only what changes what the agent *produces*.

---

## 1. The diagnosis — what makes a vision hard for a planning agent

The vision is optimized for a **human**: narrative, one flat list, plain language, no
structure. For a planning agent that creates four frictions — all **structural, not
length**. The cost that matters is **cognitive load** (how many facts a reader must hold at
once), not line count, which is why the response to every gap is *restructure*, never
*compress*.

| # | Gap in the vision | Consequence for the agent | Resolved by |
|---|-------------------|---------------------------|-------------|
| D1 | Cross-cutting constraints restated in nearly every use-case | Load-bearing rules buried in repetition; risk of inconsistent re-derivation | S1 |
| D2 | No clustering — a long flat list of use-cases | Agent must re-cluster every run, possibly differently each time | S2, S7 |
| D3 | No consistent terminology — one concept named many ways | No ubiquitous language to carry into code/schemas; ambiguity | S3 |
| D4 | No traceability — stable IDs exist but map to nothing | Can't trace a requirement back to intent, or forward from a use-case | S4 |
| D5 | The press-release layer — scope ladder (`S#`) and vision points (`V#`) — is dropped entirely | Agent can't tell which promise a capability serves, or where the scope boundary/horizon sits | S9 |

---

## 2. The strategies (one per gap)

### S1 — Factor cross-cutting constraints into an invariants doc  *(D1)*
Pull the rules that touch many capabilities (e.g. approval gate, non-destructive,
transparency, audit, ownership, progressive autonomy, acts-in-real-name) into one document,
stated **once**, referenced by `INV` ID everywhere else. State them as **tech-free business
policy** — no framework, storage, or transport commitment — exactly as the vision keeps tech
out. Every `INV` is cited by ≥1 `UC`; invent nothing.

### S2 — Cluster use-cases into a capability map  *(D2)*
Group the flat list into capabilities; assign each use-case **one primary** capability (note
secondaries); list actors separately, since each actor relationship (e.g. single-user vs.
team/manager) is a candidate context boundary. S2 produces the clusters; **S7 classifies and
connects them** — without S7 the clustering is only a free reading of the list.

### S3 — Establish a glossary / ubiquitous language  *(D3)*
One canonical term per concept; each term absorbs the vision's many synonyms. Use these terms
in all downstream code, schemas, and docs. Two rules keep it sharp: **one concept gets one
term, and one term carries one meaning within a context**; the *same word in a different
context may be a different concept*, so the glossary is per-context. A single-context vision
collapses to one glossary — the per-context rule is what scales it when team/manager contexts
split off.

Sweep the **whole** vision for concepts, not just the use-case list: the `## Vision scope`
and `## Vision points` sections often name the product's *raison d'être* more sharply than any
single use-case (e.g. the anchor's "obligation that asks something of you though no message
ever arrived"). But keep the vision's **scope-ladder structural terms** — *scope item, anchor,
horizon, sibling vision* — **out** of the product glossary: they describe the vision's
*boundary*, not the product's domain, and are defined in `vision-index.md`'s header (S9).

### S4 — Build a traceability index — the spine  *(D4)*
One row per use-case → actor · capability · invariants · normalized one-liner · link back to
the source line. Plus a reverse index (capability → use-cases). This gives audit-ready
forward/back paths and is the artifact that reconciles every other file.

### S5 — Split by pipeline role, one concern per file  *(structural)*
The bundle is many small docs, each owning one concern, plus a README entry point. Split by
*role in the downstream pipeline* (so an agent loads only the slice a task needs), **not** by
feature. A split is worth it only if the new boundary **hides more complexity than it adds** —
so the rule is not "many small files" but "each file is a self-contained doc with a semantic
name." Reject pass-through docs and tiny split-outs that add a filename without reducing what
a task must load. The README is the interface; each doc hides its internals behind a one-line
purpose.

### S6 — Derive, never replace; cite back by stable ID  *(integrity)*
The vision is the one authoritative representation. Every derived claim traces to ≥1 `UC` (or
`BV`) ID; nothing is invented, nothing is dropped, and the vision is never edited to match a
derived doc — if they disagree, fix the derived doc.

### S7 — Classify subdomains and map context relationships  *(deepens D2)*
On top of the S2 capability map, add two pieces of **strategic-design** structure — strategic
altitude only, *not* tactical patterns (see the fence in §2a):

1. **Subdomain classification.** Tag each capability **Core** (the differentiating reason the
   product exists — concentrate design effort), **Supporting** (needed, not differentiating —
   keep simple), or **Generic** (a solved problem like auth/storage — prefer buy/adopt). This
   turns the flat, priority-free map into an **attention/investment ordering** without
   smuggling MVP-scoping or tech into the vision: the classification is a derived, citable
   judgment; the vision stays priority-free.
2. **Context-map relationships.** Name the relationship at each actor/external boundary with
   the standard vocabulary — **Partnership, Shared Kernel, Customer/Supplier, Conformist,
   Anticorruption Layer (ACL), Open Host Service, Published Language, Separate Ways**. Each
   choice carries explicit ownership and translation duties downstream (e.g. the boundary
   with an external mail provider → likely Conformist or ACL).

Output: a short `subdomains-and-context-map.md` — a table (capability → subdomain class →
rationale → `UC` IDs) plus a context-relationship list (boundary → relationship → who owns
the language → translation needed?). Every row cites `UC` IDs.

### S8 — Route every parked item to its downstream phase; drop nothing  *(coverage)*
The vision may carry a parking lot of out-of-scope `BV` items — integrations, hard
constraints (offline, privacy, scale), tech/platform leanings, MVP/scoping calls, edge
cases: precisely the build-phase thinking the vision deliberately kept out. Many visions park
nothing; when `BV` items exist, none may be dropped. Route each by type, **citing it by `BV`
ID**:

- **Cross-cutting constraints the build must honor** (must-work-offline, data-stays-on-device,
  scale) → fold into the **invariants doc (S1)** as first-class invariants, cited by `BV` ID
  alongside any asserting `UC` IDs.
- **Everything else** (integrations, tech/platform leanings, scoping calls, edge cases) → a
  dedicated `deferred-inputs.md`, each item tagged with the phase that consumes it
  (architecture / design / scoping). The bundle **preserves and routes** these; per the
  altitude fence it does **not** design from them or promote them into the capability map.

Every `BV` item lands in exactly one home — the no-orphans rule of S4, extended to the
parking lot.

### S9 — Trace the press-release layer: scope ladder + vision points  *(D5)*
The vision opens with two ID'd layers above the flat UC list: **scope items** (`S1…Sn`, the
abstraction ladder from the concrete job up to the **anchor**, plus a recorded **horizon** —
the deliberately-excluded **sibling vision**) and **vision points** (`V1…Vn`, the press-release
promises, grouped under scope items but numbered in *arrival* order, so "which V's are under
S2" is not obvious from the source). Both are strategic-altitude and both are otherwise
discarded. Preserve them as one derived spine — the altitude-up sibling of the UC index (S4) —
in a single `vision-index.md`:

1. **Scope ladder.** Record each rung `S#` with the capabilities/UCs native to it, mark the
   **anchor**, and record the **horizon** as a **generalization one-way door**. Do *not*
   re-derive its architectural consequences: cross-reference the `<slug>-architecture-lens.md`
   sibling artifact (see the lens note below). The ladder is a **boundary/altitude** axis,
   **never** a priority or phasing order (§2a).
2. **Vision-point traceability.** Map each `V#` → its scope item · the UCs that realize it ·
   its primary capability · a coverage flag. A vision point that maps to **no** UC is an
   **unrealized promise**; a capability that serves **no** vision point is candidate
   **gold-plating** — both are free consistency checks on the vision, flagged for the human,
   never silently "fixed" by editing the vision (S6).

Cross-wire the rest of the bundle so the layer isn't siloed: the UC index (S4) carries the
`S#` native rung each UC inherits (the lowest `S#` among the vision points it realizes); the
capability map (S2) names, per capability, the `V#` it **serves**. Every claim cites `S`/`V`/
`UC` IDs; invent nothing.

**The architecture-lens is a sibling, not part of this bundle.** `brainstorm-vision` emits
`<slug>-architecture-lens.md` — the one-way-door axes for the build phase, whose *generalization
door* is exactly this horizon rung. It is the other half of the same handoff. **Acknowledge and
cite it** (in the README, and in the horizon row of `vision-index.md`); do **not** duplicate its
axes into the bundle.

---

## 2a. The altitude fence — strategic-design only

The bundle borrows only the **strategic-design** layer. Everything at code-construction or
runtime altitude would contradict the vision's no-tech/no-architecture discipline — defer it
to the phase the bundle *feeds*:

| Leave out of the bundle | Belongs to |
|-------------------------|------------|
| Tactical patterns — Aggregates, Entities, Value Objects, Domain Events, ports/adapters, application services | Architecture phase |
| Mechanics — dependency rules, composition root, consistency / ownership / event-flow / schema-evolution models | Architecture phase |
| Code & operations — class/function design, refactoring, error handling, resilience, legacy seams | Build / review phase |
| Tech & platform choices, MVP cut, phasing / roadmap | The phase that consumes the bundle (carried forward, not acted on — S8) |

**Standing rule:** when tempted to pull a tactical pattern (an Aggregate boundary, a port, a
consistency model) into the bundle, that is altitude leakage — it belongs to the phase the
bundle *feeds*. The only soft *priority* ordering allowed in the bundle is S7's
Core/Supporting/Generic classification (the S9 scope ladder is a **boundary/altitude** axis,
not a priority order); a hard phasing/roadmap belongs to the planning phase *after* this
pipeline.

**Scope rungs are not a roadmap.** The `S#` ladder in `vision-index.md` (S9) records the
vision's outer *boundary* and its generalization door — how far the ambition climbs and where
it deliberately stops — an altitude ordering, not a build order. Reading `S1 → S<n>` as phases
is the same altitude leak as smuggling in an MVP cut.

---

## 3. Where judgment is required

Flag these as judgment calls in the output so the human can overrule:

- **The specific clusters, the primary/secondary assignments, the exact set of invariants,
  and the Core/Supporting/Generic tags** are a *reading* of the use-cases, not a mechanical
  output. S7 makes the clustering more repeatable (a fixed taxonomy and a Core/Supporting/
  Generic test) but not deterministic — what counts as the Core Domain is still a call.
- **Refusing to compress the emotional vision** is deliberate; terser specs are more
  conventional but lose the global-context insurance.
- **The exact bundle shape** (which files, the README load-order) is assembled judgment.
- **Vision-point → UC mappings and the coverage flags** (an *unrealized promise*, a
  *gold-plated capability*) are a reading of the vision; surface them for the human — the fix
  is always the human's call, never a silent bundle edit (S6, S9).

---

## 4. Scaling beyond a single vision

- **Clustering (S2).** S7 fixes a taxonomy that makes clustering more repeatable; drawing the
  initial cluster lines is still a free reading.
- **A machine-readable layer.** The bundle is markdown-first. When a real programmatic
  consumer appears, mirror the traceability index as YAML/JSON.
- **Priority / phasing.** The vision stays priority-free; S7's Core/Supporting/Generic is the
  only soft *priority* ordering (S9's scope ladder records *boundary*, not priority). A hard
  phasing/roadmap belongs in the planning phase *after* this pipeline, not in the bundle.
