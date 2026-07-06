# Output templates

The markdown skeleton for each companion file — eight core files, plus
`deferred-inputs.md` when the vision parks `BV` items, plus three meta/review files
(`_status.md`, `decisions.md`, `critic-report.md`). These are *shapes*, not
fill-in forms — adapt headings and prose to the product, but keep the columns, the
ID schemes, and the cross-links. Every derived claim cites ≥1 `S`/`V`/`UC` (or `BV`).

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
> and cite back by stable ID (`UC`, `V`, `S`, `BV`). They never replace or
> contradict it. If a derived file and the vision disagree, the vision wins — fix
> the derived file. Do **not** edit the vision to match these.

A **sibling** file, [<product-slug>-architecture-lens.md](../<product-slug>-architecture-lens.md)
(emitted by the `brainstorm-vision` skill), carries the build phase's one-way-door
axes — including the *generalization door* behind this vision's **horizon**. It is
the other half of this handoff; `vision-index.md` cites it rather than duplicating it.

## Files

| File | Concern | Load it when… |
|------|---------|---------------|
| [invariants.md](invariants.md) | Cross-cutting constraints (`INV1…`) stated once | …always. Every architecture/design decision must honour these. |
| [glossary.md](glossary.md) | Ubiquitous language — one canonical term per concept | …always. Use these terms in code, schemas, docs. |
| [actors.md](actors.md) | Actor types & personas | …reasoning about permissions, multi-tenancy, or whose POV a need is. |
| [capability-map.md](capability-map.md) | The <n> UCs clustered into capabilities (`CAP1…`) | …shaping modules/services or scoping a feature area. |
| [subdomains-and-context-map.md](subdomains-and-context-map.md) | Core/Supporting/Generic + context relationships | …deciding where to concentrate design effort and how contexts integrate. |
| [uc-index.md](uc-index.md) | Traceability spine: every UC → actor · capability · invariants · normalized intent | …you need to trace a requirement back to a UC, or forward from a UC. |
| [vision-index.md](vision-index.md) | Press-release spine: scope ladder (`S#`) + each vision point (`V#`) traced to UCs/capabilities | …checking the build still serves the promised vision, or where the scope boundary/horizon sits. |
| [deferred-inputs.md](deferred-inputs.md) *(only if the vision parked `BV` items)* | Parked `BV` items routed to the phase that consumes them | …planning architecture or scope and you need the deferred build-phase inputs. |

## Suggested load order by task

- **Whole-system architecture:** invariants → glossary → vision-index (scope boundary) → capability-map → subdomains-and-context-map → actors → deferred-inputs (if present).
- **Requirements for one capability:** invariants → glossary → that `CAP` section → its UC rows in uc-index → the cited UCs in the vision.
- **Where to invest design effort:** subdomains-and-context-map (Core first).
- **Checking the vision is served / where the boundary sits:** vision-index (unrealized-promise flags; the horizon).
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

Rules: state each once; nothing here is per-feature.

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
Sweep the `## Vision scope` and `## Vision points` sections too, not just the UC list
(the anchor often names the product's *raison d'être* most sharply). Keep the
scope-ladder structural terms — *scope item, anchor, horizon, sibling vision* — **out**
of this glossary; they belong in `vision-index.md`'s header. If the project has a
`CONTEXT.md` ubiquitous-language section, reconcile with it.

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
- **Serves:** <V list — the press-release promises this capability keeps; back-filled from vision-index.md (S9). A capability that serves no `V#` is candidate gold-plating — flag it.>
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

- **Actor** → [actors.md](actors.md) · **CAP** → [capability-map.md](capability-map.md) · **INV** → [invariants.md](invariants.md) · **Scope** → [vision-index.md](vision-index.md)
- **Src** links the UC's line in the vision. Coverage: all <n> UCs present, each with a primary capability and an actor.
- **Scope** is the UC's *native rung* — the lowest scope item (`S#`) among the vision points it realizes; `—` if it realizes none (flag such a UC in vision-index.md).

| UC | Src | Scope | Actor | Primary | Also | INV | Normalized intent |
|----|-----|-------|-------|---------|------|-----|-------------------|
| UC1 | [L<n>](../<product-slug>-foundation-vision.md#L<n>) | S<n> | <CODE> | CAP<n> | <CAP or —> | <INV list or —> | <one-line intent, invariant boilerplate factored out> |
```

Rules: one row per UC, **100% coverage**, every row has a primary CAP and an
actor. The `Src` link points at the UC's actual line in the vision. The normalized
intent is the single sanctioned compression — never restate an invariant verbatim
here; reference it by `INV` id.

---

## 8. `vision-index.md` — the press-release layer, traced (S9)

*Always present.* The **scope ladder** and the **press-release vision points**,
mapped to the derived UC/capability layer. The altitude-up sibling of `uc-index.md`:
where that traces *requirements*, this traces *promises* and marks the scope boundary.

```markdown
# Vision index — the press-release layer, traced

Derived from the `## Vision scope` and `## Vision points` sections of
[<product-slug>-foundation-vision.md](../<product-slug>-foundation-vision.md). Two
layers the flat UC list doesn't carry: the **scope ladder** (how far the product's
ambition climbs, and where it deliberately stops) and the **vision points** (the
press-release promises each cluster of UCs must keep).

> Scope terms used here — **scope item** (`S#`, a rung of ambition), **anchor** (the
> top in-scope rung), **horizon** (the next rung up, deliberately excluded),
> **sibling vision** (the fork that would live beyond the horizon) — describe the
> vision's *boundary*, not the product's domain; they are **not** glossary terms.
> The `S#` ladder is a **boundary/altitude** axis, **not** a priority or build order.

## Scope ladder

| S# | Rung (plain) | In scope? | Capabilities native here | Representative UCs |
|----|--------------|-----------|--------------------------|--------------------|
| S1 | <the concrete job> | yes | CAP<n>… | UC<n>… |
| S<n> | <the anchor rung> · **anchor** | yes | … | … |
| — | *Horizon:* <the excluded rung> | **no** | — | — |

*Horizon / sibling vision:* <one line>. The build phase treats this as a
**generalization one-way door** — see
[<product-slug>-architecture-lens.md](../<product-slug>-architecture-lens.md) (the
sibling handoff); it is **not** re-derived here.

## Vision points → realization

Each press-release point mapped to the scope item it sits under, the UCs that realize
it, its primary capability, and a coverage check.

| V# | S# | Promise | Realized by (UCs) | Primary CAP | Coverage |
|----|----|---------|-------------------|-------------|----------|
| V1 | S1 | <terse promise> | UC<n>… | CAP<n> | ok |
| V<n> | S<n> | <…> | — | — | ⚠ unrealized — flag |

## Notes / judgment calls

- **Unrealized promises** (a `V#` no UC delivers) and **unpromised capabilities** (a
  `CAP` no `V#` names) are surfaced here for the human — never silently reconciled by
  editing the vision (S6).
```

Rules: every `V#` appears with its `S#` and its realizing UCs (or a flagged coverage
gap); every `S#` rung is on the ladder with the **anchor** marked and the **horizon**
recorded; the horizon **cites** `<product-slug>-architecture-lens.md` rather than
restating it. Every claim cites `S`/`V`/`UC` IDs.

---

## 9. `deferred-inputs.md` — routed parking-lot items (S8)

*Only when the vision has a `## Beyond the vision (parking lot)` section with `BV`
items. Cross-cutting `BV` constraints (offline, on-device, scale) go to
`invariants.md` instead — they are not repeated here.*

```markdown
# Deferred inputs — parked items routed downstream

The vision deliberately kept build-phase thinking out of scope and parked it as
`BV` items. This file **preserves and routes** those items so none is lost; it does
**not** design from them or promote them into capabilities (altitude fence). Each
row is tagged with the phase that consumes it.

> Cross-cutting `BV` constraints are recorded as invariants — see
> [invariants.md](invariants.md). Everything else lives here.

| BV | Src | Item | Type | Consumed by |
|----|-----|------|------|-------------|
| BV1 | [L<n>](../<product-slug>-foundation-vision.md#L<n>) | <one-line restatement> | integration / tech-leaning / scoping / edge-case | architecture / design / scoping |
```

Rules: every `BV` item lands in exactly one home — an `INV` (cross-cutting) or one
row here. Zero parked orphans. The `Src` link points at the `BV` item's line in the
vision. Route and tag only; do not expand into design.

---

## 10. `_status.md` — build state & resume notes (meta, not part of the bundle)

A small bookkeeping file inside the folder. It tracks whether the build is paused
or finished, lets a later sitting resume cleanly, and lets a re-run detect that a
finalized set already exists (see Pause and resume / Re-running in `SKILL.md`). The
folder name never changes; this file is the marker. It persists into the finalized
bundle as a build log.

```markdown
# Build status — <Product> vision companion

- **status:** in-progress | finalized
- **vision:** [<product-slug>-foundation-vision.md](../<product-slug>-foundation-vision.md)
- **started:** <YYYY-MM-DD>
- **finalized:** <YYYY-MM-DD or —>
- **built-with-hash:** <skill fingerprint, stamped at finalize — see below>
- **next phase:** <Phase N — name, or "—" when finalized>
- **blocker:** <— | the hard blocker that halted the run (Phase 0); build stops until resolved>
- **open low-confidence decisions:** <n — count of unreviewed rows in decisions.md>

## Phases

`Draft` = artifact written · `Critic` = per-phase critic sub-agent has run and its
fixes/flags applied (n/a for phases 0, 9, 10).

| Phase | Draft | Critic | File(s) written |
|-------|-------|--------|-----------------|
| 0 Setup & blocker check | done | n/a | _status.md, decisions.md |
| 1 Invariants | done | done | invariants.md |
| 2 Glossary | done | done | glossary.md |
| 3 Actors | open | open | — |
| 4 Capability map | open | open | — |
| 5 Subdomains & context map | open | open | — |
| 6 Vision index | open | open | — |
| 7 UC index | open | open | — |
| 8 Parking lot | open / n/a | open / n/a | — |
| 9 README + mechanical gates | open | n/a | README.md |
| 10 Whole-bundle critic → review → finalize | open | n/a | critic-report.md |

## Open threads / next question

- <the thread you'd pick up first on resume>

## Run log

- <YYYY-MM-DD> started build.
- <YYYY-MM-DD> finalized.
- <YYYY-MM-DD> re-opened for <upgrade to current method | review/iterate>: <what changed>.
```

Rules: update it at the end of every phase and on pause. Flip `status` to
`finalized` only at Phase 10. On a confirmed re-run, flip back to `in-progress` and
append a run-log line stating the reason.

`built-with-hash` is a fingerprint of the skill's output-shaping files, stamped at
finalize and re-checked at Phase 0 to detect skill drift — recipe and semantics in
Re-running in `SKILL.md`.

---

## 11. `decisions.md` — the judgment log (review artifact)

The concentrated record of every *reading* the builder made, so the human reviews
the interpretation layer in one place instead of watching every phase. Seeded empty
in Phase 0; appended to whenever a phase's critic pass leaves a call unsettled. The
human reads the **low-confidence** rows at Phase 10. A mechanical fact never belongs
here — only judgment.

```markdown
# Decisions & assumptions — <Product> vision companion

Every row is a *reading* of the frozen vision, not a fact in it. `confidence`:
**low** = the human should look; **med/high** = logged for audit. All cite ≥1 stable ID.

| ID | Phase | Decision (the reading taken) | Alternative rejected | Confidence | Cites | Reviewed |
|----|-------|------------------------------|----------------------|------------|-------|----------|
| D1 | 2 | "thread" ≡ "conversation" → one term **Thread** | keep them distinct | low | UC4, UC9 | [ ] |
| D2 | 4 | UC12 primary = CAP3 | CAP5 primary | low | UC12 | [ ] |
| D3 | 1 | INV4 "offline-first" is cross-cutting | scope to CAP2 only | med | UC3, UC7, BV2 | [ ] |
| D4 | 6 | V4 has no realizing UC → flagged unrealized promise | force-fit to UC10 | high | V4 | [ ] |

## Notes

- Low-confidence rows are the Phase-10 review surface; check the box when adjudicated.
- Never resolve a low-confidence row by editing the vision (S6) — fix the derived file.
```

---

## 12. `critic-report.md` — whole-bundle critic findings (review artifact)

Written in Phase 10 by the **whole-bundle critic sub-agent** (fresh context, the
frozen vision + the entire finished set, never the builder's reasoning). It catches
*cross-phase* compounding the per-phase critics couldn't see. Iterated: clear
findings are fixed and the critic re-spawned until clean or the cap (default 3). What
remains is the human's to adjudicate alongside `decisions.md`.

```markdown
# Critic report — <Product> vision companion

- **critic passes run:** <n> (cap 3)
- **status:** clean | residual findings below
- **audited against:** [<product-slug>-foundation-vision.md](../<product-slug>-foundation-vision.md) @ <byte-identical>

## Findings

| # | Severity | Where | Finding | Cites | Disposition |
|---|----------|-------|---------|-------|-------------|
| F1 | high | uc-index.md UC7 | normalized one-liner drops the "without leaving the thread" constraint → meaning drift | UC7 | fixed pass 2 |
| F2 | med | capability-map.md CAP4 | UC15 clustered under CAP4 but its actor/intent fits CAP2 | UC15 | **open — human** |
| F3 | low | subdomains-and-context-map.md | CAP6 tagged Supporting; arguably Core given INV2 | UC9, INV2 | **open — human** |

## Cross-phase checks

- **Dropped/invented:** every UC in the vision appears once in uc-index; nothing invented. ✓/✗
- **Meaning drift:** each normalized line still means its source sentence. ✓/✗
- **Language:** no glossary term split or merged wrongly across files. ✓/✗
- **Altitude:** no tactical/tech/MVP leak in any file. ✓/✗
- **Promises:** unrealized-promise / unpromised-capability flags present, not reconciled by editing the vision. ✓/✗

## Residuals for the human

- <the F# rows marked "open — human", one line each — this is half the Phase-10 review surface>
```
