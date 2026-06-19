---
name: create-vision-companion
description: Convert a finalized foundation vision (a `*-foundation-vision.md` — press-release vision + flat use-case list) into an AI-friendly companion set — invariants, glossary, actors, capability map, subdomain/context map, and a use-case traceability index — that a build-phase agent uses for architecture, requirements, and planning. Use when the user has a finalized product vision / use-case list and wants to prepare it for the build phase, mentions a "vision companion", "AI-friendly spec", or "vision-to-planning", or passes a `*-foundation-vision.md` to operationalize. This is the phase *after* the brainstorm-vision skill.
---

<what-to-do>

Turn a **finalized** foundation vision into a **derived companion set** — a small bundle of structured markdown docs a build-phase agent (architecture / requirements / planning) can consume without re-deriving the vision's structure every run.

The vision is written for a *human*: narrative, emotional, one flat use-case list, plain language, no structure. That's correct for what it is — but it creates four frictions for a planning agent (cross-cutting rules restated everywhere, no clustering, no shared terminology, no traceability). This skill resolves each with one recognized practice, **without ever editing the vision down**. The strategies (S1–S7) and their rationale live in [strategies.md](strategies.md); the exact output shapes live in [templates.md](templates.md). Read both before drafting.

Run this **conversationally, phase by phase**: draft one artifact, show it, take the user's cuts/merges, write it, then move to the next. Don't draft the whole bundle in one shot.

</what-to-do>

<inputs>

- **The vision** — a finalized `*-foundation-vision.md` (produced by the `brainstorm-vision` skill): a press-release vision plus a flat, numbered use-case list (`UC1…`), optionally a `## Beyond the vision (parking lot)` of `BV…` items. If the user doesn't name one, look in `docs/brainstorming/` and confirm which file (and that it's *finalized*, not a `.wip.md`).
- **Stop if the vision isn't finalized.** A `.wip.md` means the brainstorm session is unfinished — say so and offer to finish that first. This skill consumes a frozen artifact.

</inputs>

<the-bundle>

Output goes in a tidy subfolder **parallel to the vision**: `docs/brainstorming/<product-slug>-vision-ai-spec/`. Seven files, each owning exactly one concern (S5):

| File | Concern | Strategy |
|------|---------|----------|
| `README.md` | Map + per-task load order; states the no-compression / vision-wins rule | S5/S6 |
| `invariants.md` | Cross-cutting constraints (`INV1…`) stated **once**, referenced by ID everywhere | S1 |
| `glossary.md` | Ubiquitous language — one canonical term per concept + the vision phrasings it absorbs | S3 |
| `actors.md` | Actor types (relationships to the product → tenancy/permissions) + personas (UX flavours) | S2 |
| `capability-map.md` | The flat UCs clustered into capabilities (`CAP1…`); one **primary** per UC | S2 |
| `subdomains-and-context-map.md` | Each capability tagged Core/Supporting/Generic + DDD context relationships at actor boundaries | S7 |
| `uc-index.md` | **Traceability spine**: every UC → actor · capability(+secondaries) · invariants · source line · normalized one-liner | S4 |

A worked reference bundle exists at `ai-mail/ai-mail.pocock/docs/brainstorming/ai-mail-vision-ai-spec/` (the pilot — note it predates S7, so it has no `subdomains-and-context-map.md`).

</the-bundle>

<principles>

The non-negotiables (full rationale in [strategies.md](strategies.md)):

- **Derive, never replace (S6).** The vision stays byte-identical and canonical. The bundle only *adds* files. Every derived claim cites ≥1 `UC` (no invented requirements; nothing dropped). If a derived doc and the vision disagree, the vision wins — fix the derived doc.
- **Don't compress the vision — restructure.** Token count isn't the bottleneck; structure is. The only legitimate compression is the *normalized one-liner* per UC in the index, and only by factoring repeated invariant boilerplate out to `INV` references. The rich original sentence stays in the vision.
- **The altitude fence (§2a).** Borrow only the **strategic-design** layer. No tactical DDD (Aggregates, Entities, ports/adapters, consistency models), no tech/platform, no MVP/phasing — those belong to the phase this bundle *feeds*. Pulling them in is altitude leakage.
- **Bidirectional traceability or it didn't happen.** capability→UCs, UC→capability, invariant→UCs all resolve. No orphans on either side.
- **Flag judgment calls.** The clusters, the primary/secondary assignments, the exact invariant set, and the Core/Supporting/Generic tags are *readings* of the vision, not mechanical outputs. Mark them as such so the human can overrule.

</principles>

<workflow>

Phase by phase. After each, **re-read the vision from disk** (the user may edit between turns), present the draft, take feedback, write the file, then continue.

- **Phase 0 — Setup & conventions.** Confirm the input vision and the output folder. Lock the ID schemes (`UC`/`BV` already in the vision; new `INV`, `CAP`). Confirm the vision is finalized and will stay untouched. Note coverage target: 100% of UCs land in the index.
- **Phase 1 — Invariants (S1) → `invariants.md`.** Sweep every UC; collect the cross-cutting constraints restated across many; dedupe into `INV1…` with statement, what-it-means-for-the-build, and representative asserting UCs. Invent nothing — every INV is cited by ≥1 UC.
- **Phase 2 — Glossary (S3) → `glossary.md`.** One canonical term per concept; list the vision's synonyms each absorbs. Feed the project's `CONTEXT.md` ubiquitous-language convention if one exists.
- **Phase 3 — Actors (S2) → `actors.md`.** Distinct *relationships to the product* (drive tenancy/permissions) as actor codes; personas (UX flavours, not architecture) listed separately.
- **Phase 4 — Capability map (S2) → `capability-map.md`.** Cluster the flat UCs into `CAP1…`; each UC gets **one primary** capability (note secondaries for the index). Per capability: intent, member UCs, key entities (glossary terms), leaned-on invariants. Flag UCs that resist clustering — they're a gap-check on the vision.
- **Phase 5 — Subdomains & context map (S7) → `subdomains-and-context-map.md`.** Tag each capability **Core / Supporting / Generic** with rationale (a derived attention/investment ordering — *not* MVP scoping). Name the DDD relationship at each actor/external boundary (Partnership, Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host, Published Language, Separate Ways) with who owns the language and whether translation is needed. Every row cites UC IDs. **Strategic design only — no tactical patterns.**
- **Phase 6 — UC index (S4) → `uc-index.md`.** One row per UC: id · source-line link · actor(s) · primary CAP · secondaries · INVs · normalized one-liner. This is the spine — it must reconcile every prior file.
- **Phase 7 — README + consistency/gap pass → `README.md`.** Write the map + per-task load order + the vision-wins rule. Then run the quality gates below; resolve orphans, unused invariants, synonym collisions, mis-clustered UCs.
- **Phase 8 — Human review & finalize.** Read the bundle back; invite cuts/merges/sharpening; finalize.

> **Fan-out option (opt-in only).** Per-UC tagging, per-cluster drafting, and adversarial consistency checks make this a good multi-agent Workflow candidate. Only run one if the user explicitly opts in; otherwise execute the phases inline.

</workflow>

<quality-gates>

Before finalizing (Phase 7), verify:

- **Vision unchanged** — byte-identical source; the bundle only added files.
- **Total coverage** — 100% of UCs in `uc-index.md`, each with ≥1 capability and ≥1 actor. Zero orphans.
- **Invariants factored** — no invariant restated verbatim in a normalized line or capability description; referenced by `INV` id. Every `INV` cited by ≥1 UC.
- **Single language** — every concept has exactly one canonical glossary term; known synonyms mapped to it.
- **Bidirectional links resolve** — pick any UC and trace it forward and back.
- **Independently loadable** — each doc makes sense loaded alone with glossary + invariants (the point of the split: selective context for downstream agents).
- **Altitude held** — no tactical patterns, tech, or MVP/phasing leaked into any file.

</quality-gates>

See [strategies.md](strategies.md) for the methodology and references, and [templates.md](templates.md) for the markdown skeleton of each output file.
