---
name: create-vision-companion
description: Convert a finalized `*-foundation-vision.md` into the derived companion bundle (invariants, glossary, actors, capability map, context map, UC/vision indexes) that a build-phase agent consumes for architecture, requirements, and planning. Runs after the `brainstorm-vision` skill.
disable-model-invocation: true
---

<what-to-do>

Turn a **finalized** foundation vision into a **derived companion set** - a bundle of structured markdown docs a build-phase agent (architecture / requirements / planning) can consume without re-deriving the vision's structure every run.

The vision is written for a human - narrative, one flat use-case list, no structure - which creates frictions for a planning agent, each resolved by one practice **without editing the vision down**. The strategies (S1-S9) and method live in [strategies.md](strategies.md); the output shapes in [templates.md](templates.md); the shared rubric contract lives in [rubrics.md](rubrics.md); phase-specific rubrics live in [rubrics-1-8.md](rubrics-1-8.md) and [rubrics-9-12.md](rubrics-9-12.md). The orchestrator briefs each sub-agent with the pointers (strategy section , template section , rubric section ), not the content - no sub-agent ever loads this file.

This is an **AFK run**: autonomous, single batch, no human in the inner loop. **The main session is only the orchestrator - it does none of the derivation itself.** Every phase runs twice, and *both* passes run in their own fresh sub-agent: a **builder sub-agent** drafts the phase's artifact to disk, then an **adversarial critic sub-agent** re-reads the vision from disk and audits the draft against it. The critic auto-fixes clear defects and logs residual judgment calls, each with a confidence tag, to `decisions.md`. After all phases, a **whole-bundle critic** (another fresh sub-agent) audits the finished set against the frozen vision into `critic-report.md`, iterating until clean or a cap, and routes its residual judgment calls into `decisions.md` so the human has a single review surface. The human enters twice: mid-run only for a **hard blocker** (Phase 0), and at the end for the **item-by-item `decisions.md` review** (Phase 11) - confirming each reading - which then gates the **Phase 12** critic-reconcile-and-finalize.

**Stepping mode.** If the user asks to run with debugging/stepping, or the bundle's `_status.md` carries `debug: on`, read [debug.md](debug.md) - it suspends the AFK rule with a per-phase halt.

</what-to-do>

<inputs>

- **The vision** - a finalized `*-foundation-vision.md` (produced by the `brainstorm-vision` skill): a `## Vision scope` ladder (**scope items** `S1...`), press-release **vision points** (`V1...`) grouped under the scope items, and a flat, numbered use-case list (`UC1...`), optionally a `## Beyond the vision (parking lot)` of `BV...` items. A **sibling** `*-architecture-lens.md` may sit alongside it (the brainstorm skill's one-way-door handoff) - the companion cites it, never duplicates it. If the user doesn't name one, look in `docs/brainstorming/` and confirm which file (and that it's *finalized*, not a `.wip.md`).
- **Optional term-sightings sidecar** - a sibling `<product-slug>-term-sightings.md` may sit alongside the vision. It is a non-canonical brainstorm scratchpad: hints about live term ambiguity, never the ubiquitous language and never source of truth. Phase 2 may use it to focus glossary review, but every canonical term still must be re-derived from the frozen vision and unresolved readings still go to `decisions.md`.
- **Stop if the vision isn't finalized.** A `.wip.md` means the brainstorm session is unfinished - say so and offer to finish that first. This skill consumes a frozen artifact.

</inputs>

<the-bundle>

Output goes in a subfolder **parallel to the vision**, with a **fixed name** that never changes across sittings or re-runs: `docs/brainstorming/<product-slug>-vision-ai-spec/`. A `_status.md` file inside the folder carries the build state (`in-progress` vs `finalized`) and resume notes (see Pause and resume). Eight core files, each owning one concern (S5), plus `deferred-inputs.md` when the vision parks `BV` items (S8), plus two **review artifacts** (`decisions.md`, `critic-report.md`) the human reads at the end:

| File                                                         | Concern                                                                                                                                      | Strategy |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `README.md`                                                  | Map + per-task load order; states the no-compression / vision-wins rule                                                                      | S5/S6    |
| `invariants.md`                                              | Cross-cutting constraints (`INV1...`) stated **once**, referenced by ID everywhere                                                             | S1       |
| `glossary.md`                                                | Ubiquitous language - one canonical term per concept + the vision phrasings it absorbs                                                       | S3       |
| `actors.md`                                                  | Actor types (relationships to the product -> tenancy/permissions) + personas (UX flavours)                                                    | S2       |
| `capability-map.md`                                          | The flat UCs clustered into capabilities (`CAP1...`); one **primary** per UC                                                                   | S2       |
| `subdomains-and-context-map.md`                              | Each capability tagged Core/Supporting/Generic + DDD context relationships at actor boundaries                                               | S7       |
| `uc-index.md`                                                | **Traceability spine**: every UC -> actor - capability(+secondaries) - invariants - source line - normalized one-liner                        | S4       |
| `vision-index.md`                                            | **Press-release spine**: the scope ladder (`S#`) + each vision point (`V#`) -> scope - realizing UCs - capability - coverage flag             | S9       |
| `deferred-inputs.md` *(only if the vision parks `BV` items)* | Non-cross-cutting parked items (`BV...`) routed to the phase that consumes them; **not** promoted into capabilities                            | S8       |
| `decisions.md` *(review artifact)*                           | The judgment log: every reading the builder made, alternative rejected, **confidence** tag, cites; the human resolves rows by setting `Confidence` to `confirmed` | -        |
| `critic-report.md` *(review artifact)*                       | Findings from the whole-bundle critic sub-agent audited against the frozen vision; the human adjudicates residuals                           | -        |
| `vision-manifest.md` *(written at finalize)*                 | Per-ID fingerprint of the frozen vision (`UC`/`V`/`S`/`BV` -> content hash); lets the next re-run diff which items changed and scope itself     | -        |

</the-bundle>

<principles>

The non-negotiables (full rationale in [strategies.md](strategies.md)):

- **Derive, never replace (S6).** The vision stays byte-identical and canonical. The bundle only *adds* files. Every derived claim cites >=1 stable ID (`UC`/`V`/`S`/`BV`) (no invented requirements; nothing dropped). If a derived doc and the vision disagree, the vision wins - fix the derived doc. A term-sightings sidecar is only a review hint; it never overrides, amends, or completes the vision.
- **Don't compress the vision - restructure.** Token count isn't the bottleneck; structure is. The only legitimate compression is the *normalized one-liner* per UC in the index, and only by factoring repeated invariant boilerplate out to `INV` references. The rich original sentence stays in the vision.
- **The altitude fence (section 2a).** Borrow only the **strategic-design** layer. No tactical DDD (Aggregates, Entities, ports/adapters, consistency models), no tech/platform, no MVP/phasing - those belong to the phase this bundle *feeds*. Pulling them in is altitude leakage.
- **Bidirectional traceability.** capability->UCs, UC->capability, invariant->UCs, vision-point->UCs, UC->scope all resolve. No orphans on either side. An *orphan* is mechanical (a UC with no row, actor, or capability); a UC realizing no `V#` is not an orphan but an **unpromised UC** - a coverage signal (S9).
- **Flag judgment calls.** The clusters, primary/secondary assignments, the invariant set, and the Core/Supporting/Generic tags are *readings* of the vision, not mechanical outputs. Every such reading is logged to `decisions.md` with a **confidence** tag; the human adjudicates every row whose `Confidence` is not `confirmed` at the end. Nothing is silently collapsed.
- **The main session only orchestrates.** All real work - every draft and every audit - happens in a fresh sub-agent that reads its inputs from disk and writes its output to disk. The orchestrator never reads the vision or a full artifact into its own context; it sequences the sub-agents, receives their short summaries, and updates `_status.md`. Stepping mode (debug.md) suspends only the *autonomy*, adding a per-phase halt - it does not move any work back into the orchestrator.
- **The critic is independent.** Each critic pass runs in a **separate sub-agent** with a fresh context, distinct from the builder sub-agent that drafted the artifact: it re-reads the vision from disk and sees the *artifact*, never the builder's reasoning. A same-context self-review inherits the misreading it's meant to catch.

</principles>

<workflow>

An AFK run to the end; the human enters only at Phase 11 (or on a hard blocker). The main session orchestrates and never drafts or audits in its own context. **Every phase 1-8 runs the same two-sub-agent loop:**

1. **Draft (builder sub-agent).** Spawn a fresh sub-agent whose brief is: read the frozen vision from disk - [rubrics.md](rubrics.md) - its phase's brief in [rubrics-1-8.md](rubrics-1-8.md) section Phase N (which points at the phase's strategy in strategies.md and its template section) - the already-finalized prior-phase files - draft the phase's artifact per its strategy, **write it to disk**, and return only a short summary. The orchestrator does not draft.
2. **Critic (separate sub-agent, fresh context).** Spawn a *different* sub-agent whose brief is: read the frozen vision (from disk) - [rubrics.md](rubrics.md) - the drafted artifact - the already-finalized prior-phase artifacts - this phase's critic checklist in [rubrics-1-8.md](rubrics-1-8.md) section Phase N (its S-strategy + the gates it must meet) - and audit adversarially for dropped/invented items, meaning drift, broken traceability to prior phases, altitude leaks (section 2a), and synonym collisions. It does **not** receive the builder's reasoning. It **auto-fixes clear defects in place**, writes unresolved residuals to `decisions.md` (never silently resolving them), and returns a short summary of confirmed defects + residual judgment calls with confidence tags.
3. **Orchestrate.** From the two summaries alone - without pulling the vision or the full artifact into the main context - update the `_status.md` checklist (phase done, critic-pass state, file written, open-decisions count). Nothing else.

Checkpoint pauses between *sittings* still work (see Pause and resume); they are not review gates.

- **Phase 0 - Setup & blocker check.** The orchestrator's own steps (no vision read): look in the output directory for an existing `<product-slug>-vision-ai-spec/` and branch on its `_status.md` (see Pause and resume for `in-progress`, and Re-running for `finalized`); ask before continuing either way. For a new build: confirm the input vision, note whether a sibling `<product-slug>-term-sightings.md` hint file exists, and confirm the output folder with the user, then create the folder and seed `_status.md` (status `in-progress`, empty phase checklist) and an empty `decisions.md`. **Then spawn a setup sub-agent** to do the vision-reading work and report a short summary back: confirm the vision is finalized (not `.wip.md`), inventory the ID schemes (`S`/`V`/`UC`/`BV` already in the vision; reserve new `INV`, `CAP`), record coverage targets (100% of UCs in the index, every `V#` traced or its gap flagged, every `S#` on the ladder with anchor and horizon, every `UC#` traced to >=1 `V#` or flagged unpromised), record the term-sightings sidecar path if present (hint only), and run the hard-blocker check below - writing the inventory, targets, term-sightings presence, and any blocker into `_status.md`.
  - **Hard-blocker check - the setup sub-agent halts the run and surfaces immediately if any hold** (the *only* mid-run human interrupts): (a) the vision isn't finalized - a `.wip.md` (already a stop, per Inputs); (b) the vision **self-contradicts irreconcilably** and a reading can't be chosen without inventing intent; (c) a **mechanical gate is structurally unmeetable** (e.g. a UC no actor or capability can own -> 100% coverage impossible). Record the blocker in `_status.md` and stop. Anything short of a blocker is logged to `decisions.md` and carried to the end, not surfaced now.
- **Phases 1-8 - the derivation loop.** Each is one builder+critic loop over the artifact below; the orchestrator spawns them in order and passes only the pointers. The shared contract lives in [rubrics.md](rubrics.md); the **full derivation recipe and the critic's per-phase checklist live in [rubrics-1-8.md](rubrics-1-8.md) section Phase N** (which in turn point at the phase's strategy and template section) - the orchestrator does not hold them. What the orchestrator *does* track is the sequence and its cross-phase dependencies:

  | Phase | Artifact | Strategy | Cross-phase dependency the orchestrator must honor |
  | ----- | -------- | -------- | -------------------------------------------------- |
  | 1 | `invariants.md` | S1 | Folds cross-cutting `BV` constraints in (Phase 8 routes the rest). |
  | 2 | `glossary.md` | S3 | - |
  | 3 | `actors.md` | S2 | - |
  | 4 | `capability-map.md` | S2 | Leaves the `Serves: V#` line as a placeholder - **back-filled in Phase 6**. |
  | 5 | `subdomains-and-context-map.md` | S7 | Reads Phase 4. |
  | 6 | `vision-index.md` | S9 | **Back-fills `Serves: V#` into `capability-map.md`** and fixes each UC's native rung `S#` for Phase 7. |
  | 7 | `uc-index.md` | S4 | The spine - reconciles every prior file; carries `S#` from Phase 6. |
  | 8 | `deferred-inputs.md` | S8 | **Skip if the vision parks no `BV` items.** |
- **Phases 9-12 - end review and finalize.** When Phase 8 is complete, or when resuming an in-progress bundle whose next phase is 9, 10, 11, or 12, read [rubrics.md](rubrics.md) and [rubrics-9-12.md](rubrics-9-12.md). `rubrics-9-12.md` owns the detailed orchestration and gates for Phase 9 (`README.md` + mechanical gate pass), Phase 10 (whole-bundle critic), Phase 11 (item-by-item human `decisions.md` review), and Phase 12 (critic reconcile + finalize). Keep only resume routing here so earlier phases do not load the review/finalize details.

> **Every pass is a sub-agent** (see Principles) - the builder pass and the critic pass alike; the main session only orchestrates. A builder sub-agent *may* additionally fan out per-UC tagging or per-cluster drafting into further sub-agents; that stays optional.

</workflow>

<pause-and-resume>

A companion build can span multiple sittings, and **each phase is a clean checkpoint** - one self-contained artifact derived from the frozen vision. State lives in **`_status.md` inside the bundle folder** (the folder name never changes): a bundle whose `_status.md` reads `in-progress` *is* a paused, resumable build - even if a previous sitting ended abruptly. At finalize the same file flips to `finalized` (Phase 12); the resume notes become a historical record.

`_status.md` holds: the `status` line; a **phase checklist** (each phase -> done/open, its critic-pass state, and the file it wrote); a running count of rows in `decisions.md` whose `Confidence` is not `confirmed`; any recorded hard blocker; open threads; and the next phase to run.

The run can be safely interrupted (context limit, Ralph-loop boundary, machine stopping) and resumed with almost no loss; keep `_status.md` current after every phase.

**Resuming (at session start - part of Phase 0).** Before setting up a new build, look in the output directory (default `docs/brainstorming/`) for the bundle folder and read its `_status.md`. If `status` is `in-progress`, **always ask** - never auto-continue. Name the folder and its product, then offer the choice:

- **Resume it** - the orchestrator reads only `_status.md` (the small state file), plays back in two or three sentences which phases are done and what's still open from its checklist, then continues from the first unfinished phase by spawning that phase's builder sub-agent (which re-reads the vision and prior files from disk itself). Don't redo settled phases, and don't pull the vision or written artifacts into the orchestrator's context to do the playback.
- **Start fresh** - confirm first (this overwrites the in-progress work), then reset `_status.md` and rebuild from Phase 0.

(If `status` is `finalized`, this is a re-run - see Re-running on a finalized vision.)

**Pausing (on request - "pause", "stop for now", "let's continue later" - or when the run is interrupted).**

1. Make sure the current phase's file is written *and its critic pass has run* - don't pause mid-artifact; finish or discard the in-flight draft first.
2. Update `_status.md` (phase checklist + critic state, open-decisions count, any blocker, next phase).
3. Tell the user the folder path and that re-invoking the skill resumes from it. Then stop.

</pause-and-resume>

<re-running-on-a-finalized-vision>

The skill is meant to be **run again on the same vision** - to upgrade a bundle after the skill improved, or to review/iterate it with a stronger model (Ralph-looping). The vision stays frozen and canonical (S6); a re-run revises only the *derived* files. At **Phase 0**, when `_status.md` reads `finalized`, the process - the `built-with-hash` skill-drift check, the `vision-manifest.md` per-ID vision-drift check (which scopes the re-run when only a few items changed), the confirm-before-re-opening rule, and the **review-re-run vs. rebuild-from-scratch** fork (with Upgrade / Review-iterate / Vision-diff as the review-re-run sub-modes) - lives in **[re-running.md](re-running.md)**. Read it only then; on a fresh build or an `in-progress` resume it is cold weight.

</re-running-on-a-finalized-vision>

<quality-gates>

The gates are of two kinds. **Mechanical gates** are decidable by inspection - the Phase 9 builder sub-agent runs the full set **unattended** (green needs no human; unambiguous failures auto-fixed; a structurally unmeetable one is a hard blocker -> Phase 0). **Judgment gates** are *readings* - a critic sub-agent audits them (per-phase in 1-8, bundle-wide in 10) and residual doubts go to `decisions.md`/`critic-report.md` for the human's single end review. Every gate runs inside a sub-agent, never the orchestrator's context: don't ask the human to verify a mechanical gate, and don't let a builder self-certify a judgment gate.

The shared rubric contract lives in [rubrics.md](rubrics.md). The **checklists themselves live in [rubrics-1-8.md](rubrics-1-8.md) and [rubrics-9-12.md](rubrics-9-12.md)** - the judgment gates distributed to each phase's critic (section Phase 1-8), the complete mechanical set in section Phase 9, the cross-phase set in section Phase 10, and the human-review + reconcile-and-finalize gates in section Phase 11-12 - so each sub-agent loads a sharp, phase-targeted list rather than a flat whole-skill one. The orchestrator does not hold them.

</quality-gates>

See [strategies.md](strategies.md) for the methodology and references, [templates.md](templates.md) for the markdown skeleton of each output file, [rubrics.md](rubrics.md) for the shared rubric contract, [rubrics-1-8.md](rubrics-1-8.md) for derivation-phase builder briefs + critic checklists, and [rubrics-9-12.md](rubrics-9-12.md) for Phases 9-12 end-review/finalize orchestration and gates.
