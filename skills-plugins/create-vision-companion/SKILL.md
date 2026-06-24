---
name: create-vision-companion
description: Convert a finalized foundation vision (a `*-foundation-vision.md` — press-release vision + flat use-case list) into an AI-friendly companion set — invariants, glossary, actors, capability map, subdomain/context map, and a use-case traceability index — that a build-phase agent uses for architecture, requirements, and planning. Use when the user has a finalized product vision / use-case list and wants to prepare it for the build phase, mentions a "vision companion", "AI-friendly spec", or "vision-to-planning", or passes a `*-foundation-vision.md` to operationalize. This is the phase *after* the brainstorm-vision skill.
disable-model-invocation: true
---

<what-to-do>

Turn a **finalized** foundation vision into a **derived companion set** — a small bundle of structured markdown docs a build-phase agent (architecture / requirements / planning) can consume without re-deriving the vision's structure every run.

The vision is written for a *human*: narrative, emotional, one flat use-case list, plain language, no structure. That's correct for what it is — but it creates four frictions for a planning agent (cross-cutting rules restated everywhere, no clustering, no shared terminology, no traceability). This skill resolves each with one recognized practice, **without ever editing the vision down**. The strategies (S1–S8) and the method live in [strategies.md](strategies.md); the exact output shapes live in [templates.md](templates.md). Read both before drafting.

Run this **conversationally, phase by phase**: draft one artifact, show it, take the user's cuts/merges, write it, then move to the next. Don't draft the whole bundle in one shot.

</what-to-do>

<inputs>

- **The vision** — a finalized `*-foundation-vision.md` (produced by the `brainstorm-vision` skill): a press-release vision plus a flat, numbered use-case list (`UC1…`), optionally a `## Beyond the vision (parking lot)` of `BV…` items. If the user doesn't name one, look in `docs/brainstorming/` and confirm which file (and that it's *finalized*, not a `.wip.md`).
- **Stop if the vision isn't finalized.** A `.wip.md` means the brainstorm session is unfinished — say so and offer to finish that first. This skill consumes a frozen artifact.

</inputs>

<the-bundle>

Output goes in a tidy subfolder **parallel to the vision**, with a **fixed name** that never changes across sittings or re-runs: `docs/brainstorming/<product-slug>-vision-ai-spec/`. A small `_status.md` file inside the folder carries the build state (`in-progress` vs `finalized`) and the resume notes — it is the marker that distinguishes a paused build from a finished one (see Pause and resume) and survives into the finalized bundle. Seven core files, each owning exactly one concern (S5), plus `deferred-inputs.md` when the vision parks `BV` items (S8):

| File | Concern | Strategy |
|------|---------|----------|
| `README.md` | Map + per-task load order; states the no-compression / vision-wins rule | S5/S6 |
| `invariants.md` | Cross-cutting constraints (`INV1…`) stated **once**, referenced by ID everywhere | S1 |
| `glossary.md` | Ubiquitous language — one canonical term per concept + the vision phrasings it absorbs | S3 |
| `actors.md` | Actor types (relationships to the product → tenancy/permissions) + personas (UX flavours) | S2 |
| `capability-map.md` | The flat UCs clustered into capabilities (`CAP1…`); one **primary** per UC | S2 |
| `subdomains-and-context-map.md` | Each capability tagged Core/Supporting/Generic + DDD context relationships at actor boundaries | S7 |
| `uc-index.md` | **Traceability spine**: every UC → actor · capability(+secondaries) · invariants · source line · normalized one-liner | S4 |
| `deferred-inputs.md` *(only if the vision parks `BV` items)* | Non-cross-cutting parked items (`BV…`) routed to the phase that consumes them; **not** promoted into capabilities | S8 |

A worked reference bundle exists at `ai-mail/ai-mail.pocock/docs/brainstorming/ai-mail-vision-ai-spec/` (the pilot — note it predates S7 and S8, so it has no `subdomains-and-context-map.md` or `deferred-inputs.md`).

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

Phase by phase. After each, **re-read the vision from disk** (the user may edit between turns), present the draft, take feedback, write the file, update `_status.md`, then **offer a checkpoint pause** (pause and continue fresh next sitting) before moving on — see Pause and resume.

- **Phase 0 — Setup & conventions.** First look in the output directory for an existing `<product-slug>-vision-ai-spec/` and branch on its `_status.md` (see Pause and resume for `in-progress`, and Re-running for `finalized`); ask before continuing either way. For a new build: confirm the input vision and the output folder, then create the folder and seed `_status.md` (status `in-progress`, empty phase checklist). Lock the ID schemes (`UC`/`BV` already in the vision; new `INV`, `CAP`). Confirm the vision is finalized and will stay untouched. Note coverage target: 100% of UCs land in the index.
- **Phase 1 — Invariants (S1) → `invariants.md`.** Sweep every UC; collect the cross-cutting constraints restated across many; dedupe into `INV1…` with statement, what-it-means-for-the-build, and representative asserting UCs. Invent nothing — every INV is cited by ≥1 UC. If the vision parks `BV` items, also fold any cross-cutting `BV` constraints (e.g. must-work-offline, data-stays-on-device, scale) into `INV…`, cited by `BV` ID (S8).
- **Phase 2 — Glossary (S3) → `glossary.md`.** One canonical term per concept; list the vision's synonyms each absorbs. Feed the project's `CONTEXT.md` ubiquitous-language convention if one exists.
- **Phase 3 — Actors (S2) → `actors.md`.** Distinct *relationships to the product* (drive tenancy/permissions) as actor codes; personas (UX flavours, not architecture) listed separately.
- **Phase 4 — Capability map (S2) → `capability-map.md`.** Cluster the flat UCs into `CAP1…`; each UC gets **one primary** capability (note secondaries for the index). Per capability: intent, member UCs, key entities (glossary terms), leaned-on invariants. Flag UCs that resist clustering — they're a gap-check on the vision.
- **Phase 5 — Subdomains & context map (S7) → `subdomains-and-context-map.md`.** Tag each capability **Core / Supporting / Generic** with rationale (a derived attention/investment ordering — *not* MVP scoping). Name the DDD relationship at each actor/external boundary (Partnership, Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host, Published Language, Separate Ways) with who owns the language and whether translation is needed. Every row cites UC IDs. **Strategic design only — no tactical patterns.**
- **Phase 6 — UC index (S4) → `uc-index.md`.** One row per UC: id · source-line link · actor(s) · primary CAP · secondaries · INVs · normalized one-liner. This is the spine — it must reconcile every prior file.
- **Phase 7 — Parking lot (S8) → `deferred-inputs.md`.** *Skip if the vision parks no `BV` items.* Cross-cutting `BV` constraints already went to `invariants.md` in Phase 1; route every remaining `BV` item here, tagged with the phase that consumes it (architecture / design / scoping). Preserve and route — do **not** design from them or promote them into the capability map (altitude fence).
- **Phase 8 — README + consistency/gap pass → `README.md`.** Write the map + per-task load order + the vision-wins rule. Then run the quality gates below; resolve orphans, unused invariants, synonym collisions, mis-clustered UCs, unrouted `BV` items.
- **Phase 9 — Human review & finalize.** Read the bundle back; invite cuts/merges/sharpening; then **finalize** — set `_status.md` to `finalized`, record the date (and, if a re-run, what this pass changed), and stamp `built-with-hash` with the skill fingerprint (recipe in Re-running). The folder name does not change.

> **Fan-out option (opt-in only).** Per-UC tagging, per-cluster drafting, and adversarial consistency checks make this a good multi-agent Workflow candidate. Only run one if the user explicitly opts in; otherwise execute the phases inline.

</workflow>

<pause-and-resume>

A companion build can span multiple sittings, and **each phase is a clean checkpoint** — one self-contained artifact derived from the frozen vision. State lives in **`_status.md` inside the bundle folder** (the folder name never changes). While the build is unfinished its `status` is `in-progress` and it carries the resume notes, so a bundle whose `_status.md` reads `in-progress` *is* a paused, resumable build — even if a previous sitting ended abruptly. At finalize the same file flips to `finalized` (Phase 9); the resume notes become a historical record.

`_status.md` holds: the `status` line; a **phase checklist** (each phase → done/open + the file it wrote); any flagged judgment calls awaiting the user (clusterings, primary/secondary assignments, Core/Supporting/Generic tags); open threads; and the next phase to run.

**Offer a checkpoint pause after every phase (whenever reasonable).** Because the next phase re-reads the vision from disk anyway, continuing in a **fresh context loses almost nothing** and avoids the quality drift of a long session. After writing each phase's file and updating `_status.md`, offer — once, gently — to pause and continue fresh in a new sitting, then stop or continue per the user's call. Don't nag: skip the offer on trivial phases (e.g. an empty Phase 7) or when the user clearly wants momentum.

**Resuming (at session start — part of Phase 0).** Before setting up a new build, look in the output directory (default `docs/brainstorming/`) for the bundle folder and read its `_status.md`. If `status` is `in-progress`, **always ask** — never auto-continue. Name the folder and its product, then offer the choice:

- **Resume it** — read `_status.md` and the files already written, re-read the vision from disk, play back in two or three sentences which phases are done and what's still open, then continue from the first unfinished phase. Don't redo settled phases.
- **Start fresh** — confirm first (this overwrites the in-progress work), then reset `_status.md` and rebuild from Phase 0.

(If `status` is `finalized`, this is a re-run — see Re-running on a finalized vision.)

**Pausing (on request — "pause", "stop for now", "let's continue later" — or when a per-phase offer is accepted).**

1. Make sure the current phase's file is written — don't pause mid-artifact; finish or discard the in-flight draft first.
2. Update `_status.md` (phase checklist, open judgment calls, open threads, next phase).
3. Tell the user the folder path and that re-invoking the skill resumes from it. Then stop.

</pause-and-resume>

<re-running-on-a-finalized-vision>

The skill is meant to be **run again on the same vision** — to upgrade a bundle after the skill itself improved, or to review/iterate the bundle with a stronger model (e.g. Ralph-looping). The vision stays frozen and canonical throughout (S6); a re-run only ever revises the *derived* files.

**Detecting skill drift (the hash check).** A finalized bundle records `built-with-hash` in `_status.md` — a fingerprint of the skill's output-shaping files at build time. At Phase 0, recompute it **from the skill's own directory** and compare. The recipe (reproducible because `git hash-object` normalizes and follows symlinks to real content):

```
git hash-object SKILL.md strategies.md templates.md | git hash-object --stdin
```

- **Matches** → the skill is unchanged since this bundle was built; no upgrade is warranted (a re-run would only be a Review/iterate pass).
- **Differs, or no `built-with-hash` recorded** (bundles built before this mechanism) → the skill content changed since the build; **recommend an Upgrade re-run**. The hash only says *that* something changed — fall back to the structural diff (file set, ID schemes, template shapes vs. the current `templates.md`) to decide *which* phases to re-run.

(The recipe hashes the three files that determine output. It assumes they're byte-stable as installed; a pure whitespace/line-ending-only change can flip the hash, which is harmless — the structural diff then finds nothing to do.)

**Confirm before re-opening.** When Phase 0 finds a bundle whose `_status.md` is `finalized`, do **not** silently start editing. State that a finalized companion set already exists, report the hash-check result (in sync / drifted), and ask the user to confirm a re-open. Only on confirmation: flip `_status.md` back to `in-progress`, record that a re-run started (date + reason), and proceed. If the user declines, stop.

Once confirmed, ask which kind of re-run this is:

- **Upgrade to current method** (the skill changed). Diff what's on disk against the bundle the *current* skill produces: missing files (e.g. an old bundle predating S7/S8 has no `subdomains-and-context-map.md` or `deferred-inputs.md`), missing IDs, stale templates. Re-run only the affected phases to fill the gaps; leave still-correct artifacts as they are. Re-run the Phase 8 consistency/gap pass at the end so the whole set reconciles.
- **Review / iterate** (stronger model, looping). Hold the structure and re-examine the existing artifacts for quality — sharper clusters, tighter invariants, cleaner glossary, missed traceability — phase by phase. Each pass still ends with the Phase 8 gates and a `finalized` flip; resume notes in `_status.md` carry what changed so successive loops compound rather than thrash.

Either way the rules still bind: derive-never-replace, 100% UC coverage, bidirectional traceability, the altitude fence, and flagged judgment calls. Finalize as in Phase 9 (flip `_status.md` back to `finalized`, recording what this pass changed).

</re-running-on-a-finalized-vision>

<quality-gates>

Before finalizing (Phase 8), verify:

- **Vision unchanged** — byte-identical source; the bundle only added files.
- **Total coverage** — 100% of UCs in `uc-index.md`, each with ≥1 capability and ≥1 actor. Zero orphans.
- **Parked items routed** — every `BV` item lands in exactly one home: an `INV` (cross-cutting) or a `deferred-inputs.md` entry tagged with its consuming phase. Zero parked orphans.
- **Invariants factored** — no invariant restated verbatim in a normalized line or capability description; referenced by `INV` id. Every `INV` cited by ≥1 UC.
- **Single language** — every concept has exactly one canonical glossary term; known synonyms mapped to it.
- **Bidirectional links resolve** — pick any UC and trace it forward and back.
- **Independently loadable** — each doc makes sense loaded alone with glossary + invariants (the point of the split: selective context for downstream agents).
- **Altitude held** — no tactical patterns, tech, or MVP/phasing leaked into any file.

</quality-gates>

See [strategies.md](strategies.md) for the methodology and references, and [templates.md](templates.md) for the markdown skeleton of each output file.
