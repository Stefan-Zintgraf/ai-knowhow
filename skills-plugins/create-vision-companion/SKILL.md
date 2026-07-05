---
name: create-vision-companion
description: Convert a finalized `*-foundation-vision.md` into the derived companion bundle (invariants, glossary, actors, capability map, context map, UC/vision indexes) that a build-phase agent consumes for architecture, requirements, and planning. Runs after the `brainstorm-vision` skill.
disable-model-invocation: true
---

<what-to-do>

Turn a **finalized** foundation vision into a **derived companion set** — a small bundle of structured markdown docs a build-phase agent (architecture / requirements / planning) can consume without re-deriving the vision's structure every run.

The vision is written for a *human*: narrative, emotional, one flat use-case list, plain language, no structure. That's correct for what it is — but it creates frictions for a planning agent, each resolved with one recognized practice, **without ever editing the vision down**. The diagnosis, the strategies (S1–S9), and the method live in [strategies.md](strategies.md); the exact output shapes live in [templates.md](templates.md). Read strategies.md before drafting; pull each phase's template section as you draft it.

This is an **AFK run**: autonomous, single batch, no human in the inner loop. Work phase by phase, but each phase is **run twice**: a *draft* pass by the builder, then an **adversarial critic pass in a separate sub-agent** that re-reads the vision from disk and audits the drafted artifact against it (see the workflow). The critic auto-fixes clear defects and logs residual judgment calls, each with a confidence tag, to `decisions.md`. After all phases, a **whole-bundle critic** (another fresh sub-agent) audits the finished set against the frozen vision into `critic-report.md`, iterating until clean or a cap. The human enters exactly twice: mid-run only for a **hard blocker** (see Phase 0 — the run halts and surfaces it rather than producing a doomed bundle), and at the very end (Phase 10) to review `decisions.md` (the low-confidence calls) and `critic-report.md`, then gate the finalize.

**Stepping mode.** If the user asks to run with debugging/stepping, or the bundle's `_status.md` carries `debug: on`, read [debug.md](debug.md) — it suspends the AFK rule with a per-phase halt.

</what-to-do>

<inputs>

- **The vision** — a finalized `*-foundation-vision.md` (produced by the `brainstorm-vision` skill): a `## Vision scope` ladder (**scope items** `S1…`), press-release **vision points** (`V1…`) grouped under the scope items, and a flat, numbered use-case list (`UC1…`), optionally a `## Beyond the vision (parking lot)` of `BV…` items. A **sibling** `*-architecture-lens.md` may sit alongside it (the brainstorm skill's one-way-door handoff) — the companion cites it, never duplicates it. If the user doesn't name one, look in `docs/brainstorming/` and confirm which file (and that it's *finalized*, not a `.wip.md`).
- **Stop if the vision isn't finalized.** A `.wip.md` means the brainstorm session is unfinished — say so and offer to finish that first. This skill consumes a frozen artifact.

</inputs>

<the-bundle>

Output goes in a tidy subfolder **parallel to the vision**, with a **fixed name** that never changes across sittings or re-runs: `docs/brainstorming/<product-slug>-vision-ai-spec/`. A small `_status.md` file inside the folder carries the build state (`in-progress` vs `finalized`) and the resume notes — it is the marker that distinguishes a paused build from a finished one (see Pause and resume) and survives into the finalized bundle. Eight core files, each owning exactly one concern (S5), plus `deferred-inputs.md` when the vision parks `BV` items (S8), plus two **review artifacts** (`decisions.md`, `critic-report.md`) the human reads at the end:

| File | Concern | Strategy |
|------|---------|----------|
| `README.md` | Map + per-task load order; states the no-compression / vision-wins rule | S5/S6 |
| `invariants.md` | Cross-cutting constraints (`INV1…`) stated **once**, referenced by ID everywhere | S1 |
| `glossary.md` | Ubiquitous language — one canonical term per concept + the vision phrasings it absorbs | S3 |
| `actors.md` | Actor types (relationships to the product → tenancy/permissions) + personas (UX flavours) | S2 |
| `capability-map.md` | The flat UCs clustered into capabilities (`CAP1…`); one **primary** per UC | S2 |
| `subdomains-and-context-map.md` | Each capability tagged Core/Supporting/Generic + DDD context relationships at actor boundaries | S7 |
| `uc-index.md` | **Traceability spine**: every UC → actor · capability(+secondaries) · invariants · source line · normalized one-liner | S4 |
| `vision-index.md` | **Press-release spine**: the scope ladder (`S#`) + each vision point (`V#`) → scope · realizing UCs · capability · coverage flag | S9 |
| `deferred-inputs.md` *(only if the vision parks `BV` items)* | Non-cross-cutting parked items (`BV…`) routed to the phase that consumes them; **not** promoted into capabilities | S8 |
| `decisions.md` *(review artifact)* | The judgment log: every reading the builder made, alternative rejected, **confidence** tag, cites; the human reviews the low-confidence rows | — |
| `critic-report.md` *(review artifact)* | Findings from the whole-bundle critic sub-agent audited against the frozen vision; the human adjudicates residuals | — |

A worked reference bundle exists at `ai-mail/ai-mail.pocock/docs/brainstorming/ai-mail-vision-ai-spec/` (the pilot — an early build predating S8–S9, so it has no `deferred-inputs.md` or `vision-index.md` yet; its upgrade re-run adds them).

</the-bundle>

<principles>

The non-negotiables (full rationale in [strategies.md](strategies.md)):

- **Derive, never replace (S6).** The vision stays byte-identical and canonical. The bundle only *adds* files. Every derived claim cites ≥1 stable ID (`UC`/`V`/`S`/`BV`) (no invented requirements; nothing dropped). If a derived doc and the vision disagree, the vision wins — fix the derived doc.
- **Don't compress the vision — restructure.** Token count isn't the bottleneck; structure is. The only legitimate compression is the *normalized one-liner* per UC in the index, and only by factoring repeated invariant boilerplate out to `INV` references. The rich original sentence stays in the vision.
- **The altitude fence (§2a).** Borrow only the **strategic-design** layer. No tactical DDD (Aggregates, Entities, ports/adapters, consistency models), no tech/platform, no MVP/phasing — those belong to the phase this bundle *feeds*. Pulling them in is altitude leakage.
- **Bidirectional traceability or it didn't happen.** capability→UCs, UC→capability, invariant→UCs, vision-point→UCs, UC→scope all resolve. No orphans on either side.
- **Flag judgment calls.** The clusters, the primary/secondary assignments, the exact invariant set, and the Core/Supporting/Generic tags are *readings* of the vision, not mechanical outputs. Because no human watches the inner loop, every such reading is logged to `decisions.md` with a **confidence** tag; the low-confidence ones are what the human adjudicates at the end. Nothing is silently collapsed.
- **The critic is independent or it's theatre.** Each critic pass runs in a **separate sub-agent** with a fresh context: it re-reads the vision from disk and sees the *artifact*, never the builder's reasoning. A same-context self-review inherits the misreading it's meant to catch — don't do it.

</principles>

<workflow>

An AFK run to the end; the human enters only at Phase 10 (or on a hard blocker). **Every phase 1–8 runs the same two-pass loop:**

1. **Draft.** Re-read the vision from disk, draft the phase's artifact per its strategy.
2. **Critic (separate sub-agent, fresh context).** Spawn a sub-agent whose brief is: read the frozen vision (from disk) · the drafted artifact · the already-finalized prior-phase artifacts · this phase's rubric (its S-strategy + the gates it must meet) — and audit adversarially for dropped/invented items, meaning drift, broken traceability to prior phases, altitude leaks (§2a), and synonym collisions. It does **not** receive the builder's reasoning. It returns confirmed defects + residual judgment calls with confidence tags.
3. **Apply & log.** Fix the clear defects; write low-confidence residuals to `decisions.md` (never silently resolve them). Then write the corrected file and update `_status.md`.

Checkpoint pauses between *sittings* still work (see Pause and resume); they are not review gates.

- **Phase 0 — Setup & blocker check.** First look in the output directory for an existing `<product-slug>-vision-ai-spec/` and branch on its `_status.md` (see Pause and resume for `in-progress`, and Re-running for `finalized`); ask before continuing either way. For a new build: confirm the input vision and the output folder, then create the folder and seed `_status.md` (status `in-progress`, empty phase checklist) and an empty `decisions.md`. Lock the ID schemes (`S`/`V`/`UC`/`BV` already in the vision; new `INV`, `CAP`). Note coverage targets: 100% of UCs in the index, every `V#` traced (or its gap flagged), every `S#` on the ladder with the anchor and horizon recorded.
  - **Hard-blocker check — halt and surface immediately if any hold** (these are the *only* mid-run human interrupts; don't spend ~9 sub-agent spawns on a doomed bundle): (a) the vision isn't finalized — a `.wip.md` (already a stop, per Inputs); (b) the vision **self-contradicts irreconcilably** and a reading can't be chosen without inventing intent; (c) a **mechanical gate is structurally unmeetable** (e.g. a UC no actor or capability can own → 100% coverage impossible). Record the blocker in `_status.md` and stop. Anything short of a blocker is logged to `decisions.md` and carried to the end, not surfaced now.
- **Phase 1 — Invariants (S1) → `invariants.md`.** Sweep every UC; collect the cross-cutting constraints restated across many; dedupe into `INV1…` with statement, what-it-means-for-the-build, and representative asserting UCs. If the vision parks `BV` items, also fold any cross-cutting `BV` constraints (e.g. must-work-offline, data-stays-on-device, scale) into `INV…`, cited by `BV` ID (S8).
- **Phase 2 — Glossary (S3) → `glossary.md`.** One canonical term per concept; list the vision's synonyms each absorbs. Feed the project's `CONTEXT.md` ubiquitous-language convention if one exists.
- **Phase 3 — Actors (S2) → `actors.md`.** Distinct *relationships to the product* (drive tenancy/permissions) as actor codes; personas (UX flavours, not architecture) listed separately.
- **Phase 4 — Capability map (S2) → `capability-map.md`.** Cluster the flat UCs into `CAP1…`; each UC gets **one primary** capability (note secondaries for the index). Per capability: intent, member UCs, key entities (glossary terms), leaned-on invariants. Flag UCs that resist clustering — they're a gap-check on the vision. (The per-capability **`Serves: V#`** line — which press-release promises the cluster keeps — is back-filled in Phase 6, once the vision-point→UC mapping exists.)
- **Phase 5 — Subdomains & context map (S7) → `subdomains-and-context-map.md`.** Tag each capability **Core / Supporting / Generic** with rationale (a derived attention/investment ordering — *not* MVP scoping). Name the DDD relationship at each actor/external boundary (Partnership, Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host, Published Language, Separate Ways) with who owns the language and whether translation is needed. Every row cites UC IDs. **Strategic design only — no tactical patterns.**
- **Phase 6 — Vision index (S9) → `vision-index.md`.** Record the **scope ladder** (`S1…Sn`, anchor marked, the **horizon**/sibling-vision noted as a generalization one-way door that *cross-references* `<slug>-architecture-lens.md` rather than re-deriving it) and map every **vision point** (`V#`) → its scope item · realizing UCs · primary capability · coverage flag. Then **back-fill** the `Serves: V#` line into `capability-map.md`. Flag **unrealized promises** (a `V#` no UC delivers) and **unpromised capabilities** (a `CAP` no `V#` names) for the human — never edit the vision to reconcile (S6). This phase also fixes each UC's **native rung** (`S#`), which Phase 7 carries into the index.
- **Phase 7 — UC index (S4) → `uc-index.md`.** One row per UC: id · source-line link · **scope (`S#`, from Phase 6)** · actor(s) · primary CAP · secondaries · INVs · normalized one-liner. This is the spine — it must reconcile every prior file.
- **Phase 8 — Parking lot (S8) → `deferred-inputs.md`.** *Skip if the vision parks no `BV` items.* Cross-cutting `BV` constraints already went to `invariants.md` in Phase 1; route every remaining `BV` item here, tagged with the phase that consumes it (architecture / design / scoping). Preserve and route — do **not** design from them or promote them into the capability map (altitude fence).
- **Phase 9 — README + mechanical gate pass → `README.md`.** Write the map + per-task load order + the vision-wins rule; acknowledge the `<slug>-architecture-lens.md` sibling. Then run the **mechanical** quality gates below **unattended**: coverage, bidirectional links, INV-cited, zero orphans, parked-items routed. A green pass needs no human. A red gate is auto-fixed if the fix is unambiguous; if a gate is *structurally* unmeetable it is a hard blocker (Phase 0) — halt and surface.
- **Phase 10 — Whole-bundle critic → human review → finalize.** Spawn the **whole-bundle critic** (a fresh sub-agent over the frozen vision and the entire finished set) → write `critic-report.md`. It catches *cross-phase* compounding the per-phase critics couldn't see (a glossary term collapsed in Phase 2 that mis-clusters in Phase 4, etc.). **Iterate**: apply clear fixes and re-spawn until the report comes back clean or a cap (default 3 passes) is hit; unresolved items stay in `critic-report.md`. **Only now does the human enter** — reviewing exactly `decisions.md` (low-confidence calls) and `critic-report.md` (residuals). Apply their cuts/merges, then **finalize**: set `_status.md` to `finalized`, record the date (and, if a re-run, what this pass changed), and stamp `built-with-hash` with the skill fingerprint (recipe in Re-running). The folder name does not change. *(With zero open low-confidence decisions and a clean critic report, this review is a rubber-stamp — but the human still gates the finalize.)*

> **Critic fan-out is required** (see Principles). The builder additionally *may* fan out per-UC tagging or per-cluster drafting; that part stays optional.

</workflow>

<pause-and-resume>

A companion build can span multiple sittings, and **each phase is a clean checkpoint** — one self-contained artifact derived from the frozen vision. State lives in **`_status.md` inside the bundle folder** (the folder name never changes): a bundle whose `_status.md` reads `in-progress` *is* a paused, resumable build — even if a previous sitting ended abruptly. At finalize the same file flips to `finalized` (Phase 10); the resume notes become a historical record.

`_status.md` holds: the `status` line; a **phase checklist** (each phase → done/open, its critic-pass state, and the file it wrote); a running count of open low-confidence entries in `decisions.md`; any recorded hard blocker; open threads; and the next phase to run.

Checkpointing is about *sittings*, not review — this is an AFK run. Because each phase is a self-contained artifact off the frozen vision, the run can be safely interrupted (context limit, a Ralph-loop boundary, the machine stopping) and resumed later with almost no loss; keep `_status.md` current after every phase.

**Resuming (at session start — part of Phase 0).** Before setting up a new build, look in the output directory (default `docs/brainstorming/`) for the bundle folder and read its `_status.md`. If `status` is `in-progress`, **always ask** — never auto-continue. Name the folder and its product, then offer the choice:

- **Resume it** — read `_status.md` and the files already written, re-read the vision from disk, play back in two or three sentences which phases are done and what's still open, then continue from the first unfinished phase. Don't redo settled phases.
- **Start fresh** — confirm first (this overwrites the in-progress work), then reset `_status.md` and rebuild from Phase 0.

(If `status` is `finalized`, this is a re-run — see Re-running on a finalized vision.)

**Pausing (on request — "pause", "stop for now", "let's continue later" — or when the run is interrupted).**

1. Make sure the current phase's file is written *and its critic pass has run* — don't pause mid-artifact; finish or discard the in-flight draft first.
2. Update `_status.md` (phase checklist + critic state, open-decisions count, any blocker, next phase).
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

- **Upgrade to current method** (the skill changed). Diff what's on disk against the bundle the *current* skill produces: missing files (e.g. an old bundle predating S7–S9 has no `subdomains-and-context-map.md`, `deferred-inputs.md`, or `vision-index.md`), missing IDs (no `S#`/`V#` layer, no `Scope` column, no `Serves` line), stale templates. Re-run only the affected phases (each with its critic sub-agent) to fill the gaps; leave still-correct artifacts as they are. Re-run the Phase 9 mechanical-gate pass and the Phase 10 whole-bundle critic at the end so the whole set reconciles.
- **Review / iterate** (stronger model, looping). Hold the structure and re-examine the existing artifacts for quality — sharper clusters, tighter invariants, cleaner glossary, missed traceability — phase by phase, each phase's critic sub-agent re-auditing against the vision. Each pass still ends with the Phase 9 mechanical gates, the Phase 10 whole-bundle critic, and a `finalized` flip; resume notes in `_status.md` carry what changed so successive loops compound rather than thrash.

Either way the Principles and quality gates still bind. Finalize as in Phase 10 (flip `_status.md` back to `finalized`, recording what this pass changed).

</re-running-on-a-finalized-vision>

<quality-gates>

The gates split into two kinds. **Mechanical gates** are decidable by inspection and the builder runs them **unattended** in Phase 9 — a green pass needs no human; an unambiguous failure is auto-fixed; a structurally unmeetable one is a hard blocker (Phase 0). **Judgment gates** are *readings* — a critic sub-agent audits them (per-phase in 1–8, bundle-wide in 10) and residual doubts go to `decisions.md`/`critic-report.md` for the human's single end review. Don't ask the human to verify a mechanical gate, and don't let the builder self-certify a judgment gate.

**Mechanical (builder, unattended):**

- **Vision unchanged** — byte-identical source; the bundle only added files.
- **Total coverage** — 100% of UCs in `uc-index.md`, each with ≥1 capability and ≥1 actor. Zero orphans.
- **Parked items routed** — every `BV` item lands in exactly one home: an `INV` (cross-cutting) or a `deferred-inputs.md` entry tagged with its consuming phase. Zero parked orphans.
- **Every `V#` and `S#` present** — every `V#` maps to its `S#` and ≥1 realizing UC *or* a flagged coverage gap; every `S#` rung is on the ladder with the anchor marked and the horizon recorded; the horizon cites `<slug>-architecture-lens.md` (not re-derived).
- **Invariants cited** — every `INV` cited by ≥1 UC; no invariant restated verbatim in a normalized line or capability description (referenced by `INV` id instead).
- **Bidirectional links resolve** — pick any UC and trace it forward and back.

**Judgment (critic sub-agent → `decisions.md` / `critic-report.md`):**

- **Right readings** — clusters, primary/secondary assignments, the invariant *set*, Core/Supporting/Generic tags, and context-map relationships are defensible against the vision; low-confidence ones are logged, not silently settled.
- **No meaning drift** — each normalized one-liner still means what its source UC sentence means.
- **Single language** — every concept has exactly one canonical glossary term; known synonyms mapped to it, none wrongly split or merged.
- **Promises reconciled, not edited** — unrealized-promise / unpromised-capability flags are surfaced, never reconciled by touching the vision.
- **Independently loadable** — each doc makes sense loaded alone with glossary + invariants.
- **Altitude held** — no tactical patterns, tech, or MVP/phasing leaked into any file.

</quality-gates>

See [strategies.md](strategies.md) for the methodology and references, and [templates.md](templates.md) for the markdown skeleton of each output file.
