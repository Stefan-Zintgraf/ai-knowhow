# Phase rubrics 1-8 - builder brief + critic checklist

Read [rubrics.md](rubrics.md) first. This file contains only the derivation-loop rubrics for Phases 1-8, so early phases do not load the end-review/finalize rules.

Each phase is the same two-sub-agent loop: a builder drafts the phase artifact to disk, then an independent critic audits it and auto-fixes clear defects. Unresolved judgment calls go to `decisions.md` with a confidence tag.

---
## Phase 1 - `invariants.md` (S1)

**Builder reads:** strategies section S1 - templates section 2 - vision (incl. any `BV`). No prior files.
**Derive:** sweep every UC; collect the cross-cutting constraints restated across many; dedupe
into `INV1...` with statement, what-it-means-for-the-build, and representative asserting UCs. Fold
any cross-cutting `BV` constraint (offline, data-on-device, scale) into `INV...` cited by `BV` ID
(S8). State each as tech-free business policy.

**Critic checks (judgment -> `decisions.md`):**
- The invariant *set* is defensible against the vision - each `INV` is genuinely cross-cutting
  (touches many UCs), not a single-UC rule promoted by mistake.
- Each `INV` is stated tech-free - no framework/storage/transport commitment (altitude).

**Pre-check (mechanical, re-run in Phase 9):** every `INV` will be citable by >=1 UC; no `INV`
restated verbatim in a later normalized line or capability description (reference by `INV` id).

## Phase 2 - `glossary.md` (S3)

**Builder reads:** strategies section S3 - templates section 3 - vision - optional sibling
`<product-slug>-term-sightings.md` if present (**hint only, not source of truth**)  - 
the project's `CONTEXT.md` ubiquitous-language convention if one exists - `invariants.md`.
**Derive:** one canonical term per concept; list the vision synonyms each absorbs. Sweep the
*whole* vision - including `## Vision scope` and `## Vision points`, which often name the
product's reason-for-being most sharply. Use term sightings only to focus review on likely
splits/merges; accept a sighting only if the frozen vision itself supports it.

**Critic checks (judgment -> `decisions.md`):**
- **Single language** - every concept has exactly one canonical term; known synonyms mapped to
  it; none wrongly split (one concept forced into two terms) or merged (two concepts collapsed).
- Any term-sightings sidecar was treated as a hint, not evidence: no canonical term, synonym, or
  definition rests on the sidecar alone.
- The vision's scope-ladder structural terms - *scope item, anchor, horizon, sibling vision*  - 
  are kept **out** of the product glossary (they describe the vision's boundary, not the domain;
  they live in `vision-index.md`'s header).

## Phase 3 - `actors.md` (S2)

**Builder reads:** strategies section S2 - templates section 4 - vision.
**Derive:** distinct *relationships to the product* (which drive tenancy/permissions) as actor
codes; personas (UX flavours) listed separately.

**Critic checks (judgment -> `decisions.md`):**
- Actor types are genuine relationship/permission boundaries, not personas in disguise.
- Personas are UX flavours only - no architecture or permission logic smuggled in (altitude).

## Phase 4 - `capability-map.md` (S2)

**Builder reads:** strategies section S2 - templates section 5 - vision - `glossary.md` - `actors.md`  - 
`invariants.md`.
**Derive:** cluster the flat UCs into `CAP1...`; each UC gets **one primary** capability (note
secondaries for the index). Per capability: intent, member UCs, key entities (glossary terms),
leaned-on invariants. Flag UCs that resist clustering - a gap-check on the vision.
**Cross-phase:** the per-capability `Serves: V#` line is **back-filled in Phase 6**; leave a
placeholder.

**Critic checks (judgment -> `decisions.md`):**
- **Right readings** - the clusters and the primary/secondary assignments are defensible against
  the vision; unresolved ones logged, not silently settled.
- Every UC has exactly one primary capability; unclusterable UCs are flagged (not force-fit).
- No tactical patterns / tech in capability intent (altitude).

## Phase 5 - `subdomains-and-context-map.md` (S7)

**Builder reads:** strategies section S7 - templates section 6 - vision - `capability-map.md`.
**Derive:** tag each capability **Core / Supporting / Generic** with rationale (a derived
attention/investment ordering - *not* MVP scoping). Name the DDD relationship at each
actor/external boundary from the fixed vocabulary - Partnership, Shared Kernel,
Customer/Supplier, Conformist, ACL, Open Host, Published Language, Separate Ways - with who owns
the language and whether translation is needed. Every row cites UC IDs.

**Critic checks (judgment -> `decisions.md`):**
- **Right readings** - the Core/Supporting/Generic tags and the context-map relationships are
  defensible against the vision.
- **Altitude held (sharpest here)** - strategic design only; **no** tactical patterns
  (Aggregates, Entities, ports/adapters, consistency models), no tech/platform.
- Rationale reads as attention/investment ordering, never an MVP cut or phasing.

**Pre-check (mechanical):** every row cites >=1 UC; every `Relationship` cell is exactly one
enum value (no `/`, `+`, or free-form text - see S7); no row pairs `Conformist` with
`Translation needed? = yes` (translation implies ACL, per S7); the legend covers every pattern
used. When a hybrid is resolved, the `decisions.md` row must cite **every** affected boundary,
not a subset.

## Phase 6 - `vision-index.md` (S9)

**Builder reads:** strategies section S9 - templates section 8 - vision - `capability-map.md` -
`subdomains-and-context-map.md`.
**Derive:** record the scope ladder (`S1...Sn`, anchor marked; the **horizon** noted as a
generalization one-way door that *cross-references* `<slug>-architecture-lens.md`, not
re-derived); map every `V#` -> scope - realizing UCs - primary capability - coverage flag. Then
compute the reverse relation - every `UC#` in the capability map appearing in **no** `V#`
realization set - and write those to `Unpromised UCs` with the `Reason no V# fits` column
filled, set their native rung to `-` for Phase 7, and log a `decisions.md` row for each whose
primary CAP is tagged **Core** (the Core-gate); a capability can serve some `V#` while
containing individual unpromised UCs - flag the UCs anyway. Then **back-fill** the `Serves: V#`
line into `capability-map.md`. Fix each UC's **native rung** `S#` (the lowest `S#` among the
vision points it realizes) - Phase 7 carries it into the index.

**Critic checks (judgment -> `decisions.md`):**
- **Promises reconciled, not edited** - all three coverage signals (S9) are flagged; the fix
  is always the human's, never a silent edit of the vision (S6). No unpromised UC was
  force-fit to a weak `V#`; every
  Core-CAP one has its `decisions.md` row (the Core-gate); every Supporting/Generic one has a
  credible `Reason no V# fits` recorded - escalate to a `decisions.md` row when the reason is
  doubtful.
- The horizon **cites** the `<slug>-architecture-lens.md` sibling and does not re-derive its
  axes (altitude).
- The scope ladder is read as a **boundary/altitude** axis - never a priority or phasing order.

**Pre-check (mechanical):** the `Serves: V#` back-fill is actually written into
`capability-map.md`; every `V#` maps to its `S#`; every `S#` is on the ladder; every `UC#`
appears under >=1 `V#` realization *or* in `Unpromised UCs`.

## Phase 7 - `uc-index.md` (S4)

**Builder reads:** strategies section S4 - templates section 7 - vision - **all** prior artifacts.
**Derive:** one row per UC: id - source-line link - scope (`S#`, from Phase 6; carry `Scope = -`
for an unpromised UC as-is - do not invent a rung) - actor(s) -
primary CAP - secondaries - INVs - normalized one-liner. This is the spine - it must reconcile
every prior file. The *only* legitimate compression is the normalized one-liner, and only by
factoring repeated invariant boilerplate out to `INV` references.

**Critic checks (judgment -> `decisions.md`):**
- **No meaning drift** - each normalized one-liner still means what its source UC sentence means.

**Pre-check (mechanical, re-run in Phase 9):** 100% of UCs present, each with >=1 capability and
>=1 actor, zero orphans; pick any UC and trace it forward and back (bidirectional links resolve);
`Scope = -` only if the UC is listed under `Unpromised UCs` in `vision-index.md`.

## Phase 8 - `deferred-inputs.md` (S8)

**Builder reads:** strategies section S8 - templates section 9 - vision (`BV` items) - `invariants.md`.
**Skip entirely if the vision parks no `BV` items.**
**Derive:** cross-cutting `BV` constraints already went to `invariants.md` in Phase 1; route
every remaining `BV` item here, tagged with the phase that consumes it (architecture / design /
scoping). Preserve and route - do **not** design from them or promote them into the capability
map.

**Critic checks (judgment -> `decisions.md`):**
- No `BV` item is promoted into a capability or designed from (altitude fence).

**Pre-check (mechanical):** every `BV` item lands in exactly one home - an `INV` or one
`deferred-inputs.md` entry tagged with its consuming phase. Zero parked orphans, nothing dropped.

---
