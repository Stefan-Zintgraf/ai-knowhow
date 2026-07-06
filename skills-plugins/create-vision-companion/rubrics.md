# Phase rubrics — builder brief + critic checklist

The per-phase brief the orchestrator points sub-agents at, so no sub-agent ever
loads `SKILL.md`. Each phase (1–8) is the same two-sub-agent loop; this file gives
each pass its own targeted checklist instead of a flat, whole-skill gate list.

**How to use.**

- **Builder sub-agent** for Phase *N* loads: the frozen vision · this file's **§ Phase N**
  · the strategy it names in [strategies.md](strategies.md) · its template section in
  [templates.md](templates.md) · the already-finalized prior-phase files. It drafts to disk
  and returns a short summary.
- **Critic sub-agent** for Phase *N* loads: the frozen vision · the drafted artifact · the
  prior-phase artifacts · this file's **§ Phase N critic checks**. It never sees the builder's
  reasoning. It auto-fixes clear defects in place, logs low-confidence residuals to
  `decisions.md` with a confidence tag, and returns a short summary.

Gates are of two kinds (unchanged from the skill's contract): **mechanical** gates are
decidable by inspection — the Phase 9 builder runs the full set unattended, and each producing
phase pre-checks the ones it can; **judgment** gates are *readings* a critic audits, residuals
to `decisions.md` / `critic-report.md` for the human's single end review. Don't ask the human to
verify a mechanical gate; don't let a builder self-certify a judgment gate.

---

## Phase 1 — `invariants.md` (S1)

**Builder reads:** strategies §S1 · templates §2 · vision (incl. any `BV`). No prior files.
**Derive:** sweep every UC; collect the cross-cutting constraints restated across many; dedupe
into `INV1…` with statement, what-it-means-for-the-build, and representative asserting UCs. Fold
any cross-cutting `BV` constraint (offline, data-on-device, scale) into `INV…` cited by `BV` ID
(S8). State each as tech-free business policy.

**Critic checks (judgment → `decisions.md`):**
- The invariant *set* is defensible against the vision — each `INV` is genuinely cross-cutting
  (touches many UCs), not a single-UC rule promoted by mistake.
- Each `INV` is stated tech-free — no framework/storage/transport commitment (altitude).

**Pre-check (mechanical, re-run in Phase 9):** every `INV` will be citable by ≥1 UC; no `INV`
restated verbatim in a later normalized line or capability description (reference by `INV` id).

## Phase 2 — `glossary.md` (S3)

**Builder reads:** strategies §S3 · templates §3 · vision · the project's `CONTEXT.md`
ubiquitous-language convention if one exists · `invariants.md`.
**Derive:** one canonical term per concept; list the vision synonyms each absorbs. Sweep the
*whole* vision — including `## Vision scope` and `## Vision points`, which often name the
product's reason-for-being most sharply.

**Critic checks (judgment → `decisions.md`):**
- **Single language** — every concept has exactly one canonical term; known synonyms mapped to
  it; none wrongly split (one concept forced into two terms) or merged (two concepts collapsed).
- The vision's scope-ladder structural terms — *scope item, anchor, horizon, sibling vision* —
  are kept **out** of the product glossary (they describe the vision's boundary, not the domain;
  they live in `vision-index.md`'s header).

## Phase 3 — `actors.md` (S2)

**Builder reads:** strategies §S2 · templates §4 · vision.
**Derive:** distinct *relationships to the product* (which drive tenancy/permissions) as actor
codes; personas (UX flavours) listed separately.

**Critic checks (judgment → `decisions.md`):**
- Actor types are genuine relationship/permission boundaries, not personas in disguise.
- Personas are UX flavours only — no architecture or permission logic smuggled in (altitude).

## Phase 4 — `capability-map.md` (S2)

**Builder reads:** strategies §S2 · templates §5 · vision · `glossary.md` · `actors.md` ·
`invariants.md`.
**Derive:** cluster the flat UCs into `CAP1…`; each UC gets **one primary** capability (note
secondaries for the index). Per capability: intent, member UCs, key entities (glossary terms),
leaned-on invariants. Flag UCs that resist clustering — a gap-check on the vision.
**Cross-phase:** the per-capability `Serves: V#` line is **back-filled in Phase 6**; leave a
placeholder.

**Critic checks (judgment → `decisions.md`):**
- **Right readings** — the clusters and the primary/secondary assignments are defensible against
  the vision; low-confidence ones logged, not silently settled.
- Every UC has exactly one primary capability; unclusterable UCs are flagged (not force-fit).
- No tactical patterns / tech in capability intent (altitude).

## Phase 5 — `subdomains-and-context-map.md` (S7)

**Builder reads:** strategies §S7 · templates §6 · vision · `capability-map.md`.
**Derive:** tag each capability **Core / Supporting / Generic** with rationale (a derived
attention/investment ordering — *not* MVP scoping). Name the DDD relationship at each
actor/external boundary from the fixed vocabulary — Partnership, Shared Kernel,
Customer/Supplier, Conformist, ACL, Open Host, Published Language, Separate Ways — with who owns
the language and whether translation is needed. Every row cites UC IDs.

**Critic checks (judgment → `decisions.md`):**
- **Right readings** — the Core/Supporting/Generic tags and the context-map relationships are
  defensible against the vision.
- **Altitude held (sharpest here)** — strategic design only; **no** tactical patterns
  (Aggregates, Entities, ports/adapters, consistency models), no tech/platform.
- Rationale reads as attention/investment ordering, never an MVP cut or phasing.

**Pre-check (mechanical):** every row cites ≥1 UC.

## Phase 6 — `vision-index.md` (S9)

**Builder reads:** strategies §S9 · templates §8 · vision · `capability-map.md`.
**Derive:** record the scope ladder (`S1…Sn`, anchor marked; the **horizon** noted as a
generalization one-way door that *cross-references* `<slug>-architecture-lens.md`, not
re-derived); map every `V#` → scope · realizing UCs · primary capability · coverage flag. Then
**back-fill** the `Serves: V#` line into `capability-map.md`. Fix each UC's **native rung** `S#`
(the lowest `S#` among the vision points it realizes) — Phase 7 carries it into the index.

**Critic checks (judgment → `decisions.md`):**
- **Promises reconciled, not edited** — flag every **unrealized promise** (`V#` no UC delivers)
  and every **unpromised capability** (`CAP` no `V#` names); the fix is always the human's, never
  a silent edit of the vision (S6).
- The horizon **cites** the `<slug>-architecture-lens.md` sibling and does not re-derive its
  axes (altitude).
- The scope ladder is read as a **boundary/altitude** axis — never a priority or phasing order.

**Pre-check (mechanical):** the `Serves: V#` back-fill is actually written into
`capability-map.md`; every `V#` maps to its `S#`; every `S#` is on the ladder.

## Phase 7 — `uc-index.md` (S4)

**Builder reads:** strategies §S4 · templates §7 · vision · **all** prior artifacts.
**Derive:** one row per UC: id · source-line link · scope (`S#`, from Phase 6) · actor(s) ·
primary CAP · secondaries · INVs · normalized one-liner. This is the spine — it must reconcile
every prior file. The *only* legitimate compression is the normalized one-liner, and only by
factoring repeated invariant boilerplate out to `INV` references.

**Critic checks (judgment → `decisions.md`):**
- **No meaning drift** — each normalized one-liner still means what its source UC sentence means.

**Pre-check (mechanical, re-run in Phase 9):** 100% of UCs present, each with ≥1 capability and
≥1 actor, zero orphans; pick any UC and trace it forward and back (bidirectional links resolve).

## Phase 8 — `deferred-inputs.md` (S8)

**Builder reads:** strategies §S8 · templates §9 · vision (`BV` items) · `invariants.md`.
**Skip entirely if the vision parks no `BV` items.**
**Derive:** cross-cutting `BV` constraints already went to `invariants.md` in Phase 1; route
every remaining `BV` item here, tagged with the phase that consumes it (architecture / design /
scoping). Preserve and route — do **not** design from them or promote them into the capability
map.

**Critic checks (judgment → `decisions.md`):**
- No `BV` item is promoted into a capability or designed from (altitude fence).

**Pre-check (mechanical):** every `BV` item lands in exactly one home — an `INV` or one
`deferred-inputs.md` entry tagged with its consuming phase. Zero parked orphans, nothing dropped.

---

## Phase 9 — `README.md` + full mechanical gate sweep

**Builder reads:** templates §1 · the whole finished set.
**Derive:** write `README.md` — the map + per-task load order + the vision-wins rule,
acknowledging the `<slug>-architecture-lens.md` sibling. Then run the **full mechanical
checklist below, unattended**. A green pass needs no human. An unambiguous failure is auto-fixed
in place. A *structurally* unmeetable gate is a hard blocker → halt and surface (Phase 0). Return
a short pass/fail summary; the orchestrator only updates `_status.md`.

**Mechanical gates (complete set — run every one):**
- **Vision unchanged** — byte-identical source; the bundle only added files.
- **Total coverage** — 100% of UCs in `uc-index.md`, each with ≥1 capability and ≥1 actor. Zero
  orphans.
- **Parked items routed** — every `BV` item lands in exactly one home: an `INV` (cross-cutting)
  or a `deferred-inputs.md` entry tagged with its consuming phase. Zero parked orphans.
- **Every `V#` and `S#` present** — every `V#` maps to its `S#` and ≥1 realizing UC *or* a
  flagged coverage gap; every `S#` rung is on the ladder with the anchor marked and the horizon
  recorded; the horizon cites `<slug>-architecture-lens.md` (not re-derived).
- **Invariants cited** — every `INV` cited by ≥1 UC; no invariant restated verbatim in a
  normalized line or capability description (referenced by `INV` id instead).
- **Bidirectional links resolve** — pick any UC and trace it forward and back.

**Critic check (judgment → `decisions.md`):**
- **Independently loadable** — each doc makes sense loaded alone with the glossary + invariants.

---

## Phase 10 — whole-bundle critic (cross-phase)

**Reads:** the frozen vision · the entire finished set. Writes `critic-report.md` and applies
its own clear fixes in place. Iterate (default cap 3 passes) until clean; unresolved items stay
in `critic-report.md`. Catches *cross-phase* compounding the per-phase critics could not see.

**Bundle-wide judgment checks:**
- **Cross-phase compounding** — a reading settled in one phase that mis-propagates into a later
  one (e.g. a glossary term collapsed in Phase 2 that mis-clusters capabilities in Phase 4).
- **Single language across the whole bundle** — the glossary's canonical terms are used
  consistently in every file; no synonym re-introduced downstream.
- **Altitude held everywhere** — no tactical pattern, tech/platform choice, or MVP/phasing
  leaked into *any* file.
- **Promises reconciled, not edited** — unrealized-promise / unpromised-capability flags are
  surfaced across the set, never reconciled by touching the vision.
- **Independently loadable** — each doc still stands alone with glossary + invariants.
