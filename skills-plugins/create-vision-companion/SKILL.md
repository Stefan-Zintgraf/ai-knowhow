---
name: create-vision-companion
description: Convert a finalized `*-foundation-vision.md` into the derived companion bundle (invariants, glossary, actors, capability map, context map, UC/vision indexes) that a build-phase agent consumes for architecture, requirements, and planning. Runs after the `brainstorm-vision` skill.
disable-model-invocation: true
---

<what-to-do>

Turn a **finalized** foundation vision into a **derived companion set** — a bundle of structured markdown docs a build-phase agent (architecture / requirements / planning) can consume without re-deriving the vision's structure every run.

The vision is written for a human — narrative, one flat use-case list, no structure — which creates frictions for a planning agent, each resolved by one practice **without editing the vision down**. The strategies (S1–S9) and method live in [strategies.md](strategies.md); the output shapes in [templates.md](templates.md). Each builder sub-agent reads strategies.md before drafting and pulls its phase's template section; the orchestrator briefs it with the pointers, not the content.

This is an **AFK run**: autonomous, single batch, no human in the inner loop. **The main session is only the orchestrator — it does none of the derivation itself.** Every phase runs twice, and *both* passes run in their own fresh sub-agent: a **builder sub-agent** drafts the phase's artifact to disk, then an **adversarial critic sub-agent** re-reads the vision from disk and audits the draft against it. The critic auto-fixes clear defects and logs residual judgment calls, each with a confidence tag, to `decisions.md`. After all phases, a **whole-bundle critic** (another fresh sub-agent) audits the finished set against the frozen vision into `critic-report.md`, iterating until clean or a cap. The human enters twice: mid-run only for a **hard blocker** (Phase 0), and at the end (Phase 10) to review `decisions.md` and `critic-report.md` and gate the finalize.

**Stepping mode.** If the user asks to run with debugging/stepping, or the bundle's `_status.md` carries `debug: on`, read [debug.md](debug.md) — it suspends the AFK rule with a per-phase halt.

</what-to-do>

<inputs>

- **The vision** — a finalized `*-foundation-vision.md` (produced by the `brainstorm-vision` skill): a `## Vision scope` ladder (**scope items** `S1…`), press-release **vision points** (`V1…`) grouped under the scope items, and a flat, numbered use-case list (`UC1…`), optionally a `## Beyond the vision (parking lot)` of `BV…` items. A **sibling** `*-architecture-lens.md` may sit alongside it (the brainstorm skill's one-way-door handoff) — the companion cites it, never duplicates it. If the user doesn't name one, look in `docs/brainstorming/` and confirm which file (and that it's *finalized*, not a `.wip.md`).
- **Stop if the vision isn't finalized.** A `.wip.md` means the brainstorm session is unfinished — say so and offer to finish that first. This skill consumes a frozen artifact.

</inputs>

<the-bundle>

Output goes in a subfolder **parallel to the vision**, with a **fixed name** that never changes across sittings or re-runs: `docs/brainstorming/<product-slug>-vision-ai-spec/`. A `_status.md` file inside the folder carries the build state (`in-progress` vs `finalized`) and resume notes (see Pause and resume). Eight core files, each owning one concern (S5), plus `deferred-inputs.md` when the vision parks `BV` items (S8), plus two **review artifacts** (`decisions.md`, `critic-report.md`) the human reads at the end:

| File                                                         | Concern                                                                                                                                      | Strategy |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `README.md`                                                  | Map + per-task load order; states the no-compression / vision-wins rule                                                                      | S5/S6    |
| `invariants.md`                                              | Cross-cutting constraints (`INV1…`) stated **once**, referenced by ID everywhere                                                             | S1       |
| `glossary.md`                                                | Ubiquitous language — one canonical term per concept + the vision phrasings it absorbs                                                       | S3       |
| `actors.md`                                                  | Actor types (relationships to the product → tenancy/permissions) + personas (UX flavours)                                                    | S2       |
| `capability-map.md`                                          | The flat UCs clustered into capabilities (`CAP1…`); one **primary** per UC                                                                   | S2       |
| `subdomains-and-context-map.md`                              | Each capability tagged Core/Supporting/Generic + DDD context relationships at actor boundaries                                               | S7       |
| `uc-index.md`                                                | **Traceability spine**: every UC → actor · capability(+secondaries) · invariants · source line · normalized one-liner                        | S4       |
| `vision-index.md`                                            | **Press-release spine**: the scope ladder (`S#`) + each vision point (`V#`) → scope · realizing UCs · capability · coverage flag             | S9       |
| `deferred-inputs.md` *(only if the vision parks `BV` items)* | Non-cross-cutting parked items (`BV…`) routed to the phase that consumes them; **not** promoted into capabilities                            | S8       |
| `decisions.md` *(review artifact)*                           | The judgment log: every reading the builder made, alternative rejected, **confidence** tag, cites; the human reviews the low-confidence rows | —        |
| `critic-report.md` *(review artifact)*                       | Findings from the whole-bundle critic sub-agent audited against the frozen vision; the human adjudicates residuals                           | —        |

</the-bundle>

<principles>

The non-negotiables (full rationale in [strategies.md](strategies.md)):

- **Derive, never replace (S6).** The vision stays byte-identical and canonical. The bundle only *adds* files. Every derived claim cites ≥1 stable ID (`UC`/`V`/`S`/`BV`) (no invented requirements; nothing dropped). If a derived doc and the vision disagree, the vision wins — fix the derived doc.
- **Don't compress the vision — restructure.** Token count isn't the bottleneck; structure is. The only legitimate compression is the *normalized one-liner* per UC in the index, and only by factoring repeated invariant boilerplate out to `INV` references. The rich original sentence stays in the vision.
- **The altitude fence (§2a).** Borrow only the **strategic-design** layer. No tactical DDD (Aggregates, Entities, ports/adapters, consistency models), no tech/platform, no MVP/phasing — those belong to the phase this bundle *feeds*. Pulling them in is altitude leakage.
- **Bidirectional traceability.** capability→UCs, UC→capability, invariant→UCs, vision-point→UCs, UC→scope all resolve. No orphans on either side.
- **Flag judgment calls.** The clusters, primary/secondary assignments, the invariant set, and the Core/Supporting/Generic tags are *readings* of the vision, not mechanical outputs. Every such reading is logged to `decisions.md` with a **confidence** tag; the human adjudicates the low-confidence ones at the end. Nothing is silently collapsed.
- **The main session only orchestrates.** All real work — every draft and every audit — happens in a fresh sub-agent that reads its inputs from disk and writes its output to disk. The orchestrator never reads the vision or a full artifact into its own context; it sequences the sub-agents, receives their short summaries, and updates `_status.md`. Stepping mode (debug.md) suspends only the *autonomy*, adding a per-phase halt — it does not move any work back into the orchestrator.
- **The critic is independent.** Each critic pass runs in a **separate sub-agent** with a fresh context, distinct from the builder sub-agent that drafted the artifact: it re-reads the vision from disk and sees the *artifact*, never the builder's reasoning. A same-context self-review inherits the misreading it's meant to catch.

</principles>

<workflow>

An AFK run to the end; the human enters only at Phase 10 (or on a hard blocker). The main session orchestrates and never drafts or audits in its own context. **Every phase 1–8 runs the same two-sub-agent loop:**

1. **Draft (builder sub-agent).** Spawn a fresh sub-agent whose brief is: read the frozen vision from disk · strategies.md · its phase's template section · the already-finalized prior-phase files — draft the phase's artifact per its strategy, **write it to disk**, and return only a short summary. The orchestrator does not draft.
2. **Critic (separate sub-agent, fresh context).** Spawn a *different* sub-agent whose brief is: read the frozen vision (from disk) · the drafted artifact · the already-finalized prior-phase artifacts · this phase's rubric (its S-strategy + the gates it must meet) — and audit adversarially for dropped/invented items, meaning drift, broken traceability to prior phases, altitude leaks (§2a), and synonym collisions. It does **not** receive the builder's reasoning. It **auto-fixes clear defects in place**, writes low-confidence residuals to `decisions.md` (never silently resolving them), and returns a short summary of confirmed defects + residual judgment calls with confidence tags.
3. **Orchestrate.** From the two summaries alone — without pulling the vision or the full artifact into the main context — update the `_status.md` checklist (phase done, critic-pass state, file written, open-decisions count). Nothing else.

Checkpoint pauses between *sittings* still work (see Pause and resume); they are not review gates.

- **Phase 0 — Setup & blocker check.** The orchestrator's own steps (no vision read): look in the output directory for an existing `<product-slug>-vision-ai-spec/` and branch on its `_status.md` (see Pause and resume for `in-progress`, and Re-running for `finalized`); ask before continuing either way. For a new build: confirm the input vision and the output folder with the user, then create the folder and seed `_status.md` (status `in-progress`, empty phase checklist) and an empty `decisions.md`. **Then spawn a setup sub-agent** to do the vision-reading work and report a short summary back: confirm the vision is finalized (not `.wip.md`), inventory the ID schemes (`S`/`V`/`UC`/`BV` already in the vision; reserve new `INV`, `CAP`), record coverage targets (100% of UCs in the index, every `V#` traced or its gap flagged, every `S#` on the ladder with anchor and horizon), and run the hard-blocker check below — writing the inventory, targets, and any blocker into `_status.md`.
  - **Hard-blocker check — the setup sub-agent halts the run and surfaces immediately if any hold** (the *only* mid-run human interrupts): (a) the vision isn't finalized — a `.wip.md` (already a stop, per Inputs); (b) the vision **self-contradicts irreconcilably** and a reading can't be chosen without inventing intent; (c) a **mechanical gate is structurally unmeetable** (e.g. a UC no actor or capability can own → 100% coverage impossible). Record the blocker in `_status.md` and stop. Anything short of a blocker is logged to `decisions.md` and carried to the end, not surfaced now.
- **Phase 1 — Invariants (S1) → `invariants.md`.** Sweep every UC; collect the cross-cutting constraints restated across many; dedupe into `INV1…` with statement, what-it-means-for-the-build, and representative asserting UCs. If the vision parks `BV` items, also fold any cross-cutting `BV` constraints (e.g. must-work-offline, data-stays-on-device, scale) into `INV…`, cited by `BV` ID (S8).
- **Phase 2 — Glossary (S3) → `glossary.md`.** One canonical term per concept; list the vision's synonyms each absorbs. Feed the project's `CONTEXT.md` ubiquitous-language convention if one exists.
- **Phase 3 — Actors (S2) → `actors.md`.** Distinct *relationships to the product* (drive tenancy/permissions) as actor codes; personas (UX flavours, not architecture) listed separately.
- **Phase 4 — Capability map (S2) → `capability-map.md`.** Cluster the flat UCs into `CAP1…`; each UC gets **one primary** capability (note secondaries for the index). Per capability: intent, member UCs, key entities (glossary terms), leaned-on invariants. Flag UCs that resist clustering — they're a gap-check on the vision. (The per-capability **`Serves: V#`** line — which press-release promises the cluster keeps — is back-filled in Phase 6, once the vision-point→UC mapping exists.)
- **Phase 5 — Subdomains & context map (S7) → `subdomains-and-context-map.md`.** Tag each capability **Core / Supporting / Generic** with rationale (a derived attention/investment ordering — *not* MVP scoping). Name the DDD relationship at each actor/external boundary (Partnership, Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host, Published Language, Separate Ways) with who owns the language and whether translation is needed. Every row cites UC IDs. **Strategic design only — no tactical patterns.**
- **Phase 6 — Vision index (S9) → `vision-index.md`.** Record the **scope ladder** (`S1…Sn`, anchor marked, the **horizon**/sibling-vision noted as a generalization one-way door that *cross-references* `<slug>-architecture-lens.md` rather than re-deriving it) and map every **vision point** (`V#`) → its scope item · realizing UCs · primary capability · coverage flag. Then **back-fill** the `Serves: V#` line into `capability-map.md`. Flag **unrealized promises** (a `V#` no UC delivers) and **unpromised capabilities** (a `CAP` no `V#` names) for the human — never edit the vision to reconcile (S6). This phase also fixes each UC's **native rung** (`S#`), which Phase 7 carries into the index.
- **Phase 7 — UC index (S4) → `uc-index.md`.** One row per UC: id · source-line link · **scope (`S#`, from Phase 6)** · actor(s) · primary CAP · secondaries · INVs · normalized one-liner. This is the spine — it must reconcile every prior file.
- **Phase 8 — Parking lot (S8) → `deferred-inputs.md`.** *Skip if the vision parks no `BV` items.* Cross-cutting `BV` constraints already went to `invariants.md` in Phase 1; route every remaining `BV` item here, tagged with the phase that consumes it (architecture / design / scoping). Preserve and route — do **not** design from them or promote them into the capability map (altitude fence).
- **Phase 9 — README + mechanical gate pass → `README.md`.** Spawn a builder sub-agent to write the map + per-task load order + the vision-wins rule (acknowledging the `<slug>-architecture-lens.md` sibling), then run the **mechanical** quality gates below **unattended**: coverage, bidirectional links, INV-cited, zero orphans, parked-items routed. A green pass needs no human. A red gate is auto-fixed by the sub-agent if the fix is unambiguous; if a gate is *structurally* unmeetable it is a hard blocker (Phase 0) — halt and surface. The sub-agent returns a short pass/fail summary; the orchestrator only updates `_status.md`.
- **Phase 10 — Whole-bundle critic → human review → finalize.** Spawn the **whole-bundle critic** (a fresh sub-agent over the frozen vision and the entire finished set) — it writes `critic-report.md` **and applies its own clear fixes in place**. It catches *cross-phase* compounding the per-phase critics couldn't see (a glossary term collapsed in Phase 2 that mis-clusters in Phase 4, etc.). **Iterate**: re-spawn the critic sub-agent until the report comes back clean or a cap (default 3 passes) is hit; unresolved items stay in `critic-report.md`. The orchestrator only sequences the spawns from each pass's summary. **Only now does the human enter** — reviewing `decisions.md` (low-confidence calls) and `critic-report.md` (residuals). Their cuts/merges are applied by a final sub-agent, then **finalize**: set `_status.md` to `finalized`, record the date (and, if a re-run, what this pass changed), and stamp `built-with-hash` with the skill fingerprint (recipe in Re-running). The folder name does not change.

> **Every pass is a sub-agent** (see Principles) — the builder pass and the critic pass alike; the main session only orchestrates. A builder sub-agent *may* additionally fan out per-UC tagging or per-cluster drafting into further sub-agents; that stays optional.

</workflow>

<pause-and-resume>

A companion build can span multiple sittings, and **each phase is a clean checkpoint** — one self-contained artifact derived from the frozen vision. State lives in **`_status.md` inside the bundle folder** (the folder name never changes): a bundle whose `_status.md` reads `in-progress` *is* a paused, resumable build — even if a previous sitting ended abruptly. At finalize the same file flips to `finalized` (Phase 10); the resume notes become a historical record.

`_status.md` holds: the `status` line; a **phase checklist** (each phase → done/open, its critic-pass state, and the file it wrote); a running count of open low-confidence entries in `decisions.md`; any recorded hard blocker; open threads; and the next phase to run.

The run can be safely interrupted (context limit, Ralph-loop boundary, machine stopping) and resumed with almost no loss; keep `_status.md` current after every phase.

**Resuming (at session start — part of Phase 0).** Before setting up a new build, look in the output directory (default `docs/brainstorming/`) for the bundle folder and read its `_status.md`. If `status` is `in-progress`, **always ask** — never auto-continue. Name the folder and its product, then offer the choice:

- **Resume it** — the orchestrator reads only `_status.md` (the small state file), plays back in two or three sentences which phases are done and what's still open from its checklist, then continues from the first unfinished phase by spawning that phase's builder sub-agent (which re-reads the vision and prior files from disk itself). Don't redo settled phases, and don't pull the vision or written artifacts into the orchestrator's context to do the playback.
- **Start fresh** — confirm first (this overwrites the in-progress work), then reset `_status.md` and rebuild from Phase 0.

(If `status` is `finalized`, this is a re-run — see Re-running on a finalized vision.)

**Pausing (on request — "pause", "stop for now", "let's continue later" — or when the run is interrupted).**

1. Make sure the current phase's file is written *and its critic pass has run* — don't pause mid-artifact; finish or discard the in-flight draft first.
2. Update `_status.md` (phase checklist + critic state, open-decisions count, any blocker, next phase).
3. Tell the user the folder path and that re-invoking the skill resumes from it. Then stop.

</pause-and-resume>

<re-running-on-a-finalized-vision>

The skill is meant to be **run again on the same vision** — to upgrade a bundle after the skill itself improved, or to review/iterate the bundle with a stronger model (e.g. Ralph-looping). The vision stays frozen and canonical throughout (S6); a re-run revises only the *derived* files.

**Detecting skill drift (the hash check).** A finalized bundle records `built-with-hash` in `_status.md` — a fingerprint of the skill's output-shaping files at build time. At Phase 0, recompute it **from the skill's own directory** and compare. The recipe (reproducible because `git hash-object` normalizes and follows symlinks to real content):

```
git hash-object SKILL.md strategies.md templates.md | git hash-object --stdin
```

- **Matches** → the skill is unchanged since this bundle was built; no upgrade is warranted (a re-run would only be a Review/iterate pass).
- **Differs, or no `built-with-hash` recorded** (bundles built before this mechanism) → the skill content changed since the build; **recommend an Upgrade re-run**. The hash only says *that* something changed — fall back to the structural diff (file set, ID schemes, template shapes vs. the current `templates.md`) to decide *which* phases to re-run.

(A pure whitespace/line-ending-only change can flip the hash harmlessly — the structural diff then finds nothing to do.)

**Confirm before re-opening.** When Phase 0 finds a bundle whose `_status.md` is `finalized`, do **not** silently start editing. State that a finalized companion set already exists, report the hash-check result (in sync / drifted), and ask the user to confirm a re-open. Only on confirmation: flip `_status.md` back to `in-progress`, record that a re-run started (date + reason), and proceed. If the user declines, stop.

Once confirmed, ask which kind of re-run this is:

- **Upgrade to current method** (the skill changed). Diff what's on disk against the bundle the *current* skill produces: missing files (a bundle built by an earlier skill version can lack files a later strategy introduced), missing IDs (an absent ID layer, column, or cross-reference line the current templates expect), stale templates. Re-run only the affected phases (each through its builder + critic sub-agents, as in the normal loop) to fill the gaps; leave still-correct artifacts as they are. Re-run the Phase 9 mechanical-gate pass and the Phase 10 whole-bundle critic at the end so the whole set reconciles.
- **Review / iterate** (stronger model, looping). Hold the structure and re-examine the existing artifacts for quality — sharper clusters, tighter invariants, cleaner glossary, missed traceability — phase by phase, each phase's builder + critic sub-agents re-drafting and re-auditing against the vision. Each pass still ends with the Phase 9 mechanical gates, the Phase 10 whole-bundle critic, and a `finalized` flip; resume notes in `_status.md` carry what changed so successive loops compound rather than thrash.

Either way the Principles and quality gates still bind. Finalize as in Phase 10 (flip `_status.md` back to `finalized`, recording what this pass changed).

</re-running-on-a-finalized-vision>

<quality-gates>

The gates split into two kinds. **Mechanical gates** are decidable by inspection and the Phase 9 builder sub-agent runs them **unattended** — a green pass needs no human; an unambiguous failure is auto-fixed; a structurally unmeetable one is a hard blocker (Phase 0). **Judgment gates** are *readings* — a critic sub-agent audits them (per-phase in 1–8, bundle-wide in 10) and residual doubts go to `decisions.md`/`critic-report.md` for the human's single end review. Every gate runs inside a sub-agent, never the orchestrator's context. Don't ask the human to verify a mechanical gate, and don't let a builder sub-agent self-certify a judgment gate.

**Mechanical (builder sub-agent, unattended):**

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
