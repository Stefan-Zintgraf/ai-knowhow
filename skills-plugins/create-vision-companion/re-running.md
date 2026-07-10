# Re-running on a finalized vision

Read this from **Phase 0** only when the bundle's `_status.md` reads `finalized` - a re-run.
On a fresh build or a resume of an `in-progress` bundle, skip it (cold weight otherwise).

The skill is meant to be **run again** - to upgrade a bundle after the skill itself improved, to
review/iterate the bundle with a stronger model (e.g. Ralph-looping), or because **a few items in
the vision changed** and the derived files must catch up. There are two independent change axes:
the **skill** may have drifted (the hash check below) and the **vision** may have drifted (the
manifest check below). Whichever changed, the vision stays frozen and canonical for the duration of
the run (S6) - a re-run revises only the *derived* files.

**Detecting skill drift (the hash check).** A finalized bundle records `built-with-hash` in
`_status.md` - a fingerprint of the skill's output-shaping files at build time. At Phase 0,
recompute it **from the skill's own directory** and compare. The recipe (reproducible because
`git hash-object` normalizes and follows symlinks to real content):

```
git hash-object SKILL.md strategies.md templates.md rubrics.md rubrics-1-8.md rubrics-9-12.md | git hash-object --stdin
```

- **Matches** -> the skill is unchanged since this bundle was built; no upgrade is warranted (a
  re-run would only be a Review/iterate pass).
- **Differs, or no `built-with-hash` recorded** (bundles built before this mechanism) -> the skill
  content changed since the build. **Do not assume which mode to take** - the drift may be a small
  method tweak (a targeted review re-run suffices) or a wholesale change (regenerating everything is
  cleaner). Present both and let the human choose (see the fork below). The hash only says *that*
  something changed - fall back to the structural diff (file set, ID schemes, template shapes vs.
  the current `templates.md`) to inform the recommendation and, for a review re-run, *which* phases
  to re-run.

(A pure whitespace/line-ending-only change can flip the hash harmlessly - the structural diff then
finds nothing to do.)

**Detecting vision drift (the manifest check).** A whole-file hash of the vision would only say
*that* it changed, not *which* items - useless for scoping. So a finalized bundle also carries a
**`vision-manifest.md`**: a per-ID fingerprint of the frozen vision at build time, one line per
stable ID (`UC#`/`V#`/`S#`/`BV#`) mapping the ID to a content hash of its source block:

```
UC17: a3f9...    V4: 7c21...    S2: 91be...    BV3: 0d4c...
```

Each block is hashed the same way at build (Phase 12) and at diff (Phase 0) so the two are
comparable: extract the ID's source text - the lines from its anchor up to the next stable ID - and
`git hash-object --stdin` over exactly those lines. (Because the hash is over source lines, a
re-numbering shifts every downstream block and reads as a wholesale change - correctly routing to a
rebuild, per below.)

At Phase 0, **spawn a sub-agent** (the orchestrator never reads the vision) to recompute the same
per-ID hashes from the current vision and diff them against the recorded manifest, returning a short
**changeset**: which IDs are `modified` (hash differs), `added` (new ID), or `removed` (ID gone),
per ID class. Read the outcome:

- **Empty changeset** -> the vision is byte-identical to the build; only the *skill* axis is live, so
  this is at most an Upgrade / Review-iterate pass (below), never a Vision-diff one.
- **A few IDs changed** -> a **Vision-diff (scoped)** re-run is the economical path (sub-mode below):
  re-derive only the changed IDs' closure, not all of them.
- **Many IDs changed, or IDs were renumbered** (the manifest can't line up old to new by ID) ->
  scoping buys little and the readings-of-the-whole shift wholesale; recommend **(B) rebuild from
  scratch**. The vision's IDs are meant to be stable (S6); renumbering *is* a substantial change.

(Bundles finalized before this mechanism carry no `vision-manifest.md`. Then the vision axis can't
be diffed - treat any suspected vision change as "many changed" and offer (B), or, if the human
confirms only a handful moved, let them name the changed IDs to seed the changeset manually. Either
way the re-run writes a fresh manifest at Phase 12 so the *next* re-run can diff.)

**Confirm before re-opening.** When Phase 0 finds a bundle whose `_status.md` is `finalized`, do
**not** silently start editing. State that a finalized companion set already exists, report the
hash-check result (in sync / drifted), and ask the user to confirm a re-open. Only on
confirmation: record that a re-run started (date + reason) and proceed to the fork below. If the
user declines, stop.

**Once confirmed, ask the top-level fork - a review re-run, or a from-scratch rebuild.** This is a
required question whenever the hash **drifted or is absent** (and offered on request even when it
matches); do not pick for the user:

- **(A) Review re-run** - keep the existing derived artifacts and *revise them in place*; the
  vision stays frozen and only the derived files change. Flip `_status.md` back to `in-progress`.
  Then pick the sub-mode:
  - **Upgrade to current method** (the skill changed). Diff what's on disk against the bundle the
    *current* skill produces: missing files (a bundle built by an earlier skill version can lack
    files a later strategy introduced), missing IDs (an absent ID layer, column, or cross-reference
    line the current templates expect), stale templates. Re-run only the affected phases (each
    through its builder + critic sub-agents, as in the normal loop) to fill the gaps; leave
    still-correct artifacts as they are.
  - **Review / iterate** (stronger model, looping). Hold the structure and re-examine the existing
    artifacts for quality - sharper clusters, tighter invariants, cleaner glossary, missed
    traceability - phase by phase, each phase's builder + critic sub-agents re-drafting and
    re-auditing against the vision. Resume notes in `_status.md` carry what changed so successive
    loops compound rather than thrash.
  - **Vision-diff (scoped)** (a handful of vision items changed). Driven by the manifest changeset,
    **not** a full-bundle re-draft. Re-derive only the changed IDs' **closure under the traceability
    spine**, because the readings (clusters, primary/secondary, invariant set, Core/Supporting tags)
    are readings of the *whole* (S5/section Flag-judgment-calls) - a purely local patch is unsafe. Resolve
    the closure from the existing `uc-index.md`, then brief each affected phase's builder + critic
    sub-agents with *only* that scope, leaving untouched artifacts as they are:
    - a **modified/added `UC`** -> its `uc-index.md` row, the `capability-map.md` cluster it sits in
      (re-open the cluster's siblings, since one UC can re-shape a boundary), the `V#` coverage flag
      it realizes (or its `Unpromised UCs` row) in `vision-index.md`, and - only if it introduces or drops one - an actor
      (`actors.md`), term (`glossary.md`), or cross-cutting constraint (`invariants.md`);
    - a **removed `UC`** -> drop its row and re-check its old cluster/`V#` and any
      `Unpromised UCs` row for a new orphan or gap;
    - a **changed `V#`/`S#`** -> the `vision-index.md` spine rows it anchors and any UC whose native
      rung moves; a **changed `BV`** -> `deferred-inputs.md` (or `invariants.md` if cross-cutting).

    The builder work is scoped; **verification stays global** - always run the Phase 9 mechanical
    gate and the Phase 10 whole-bundle critic over the *entire* set, so cross-phase compounding a
    scoped draft can't see (a new UC that should re-cluster an untouched capability) is still caught.
    The critic is a read/audit, not a re-draft, so a global pass stays cheap.

  All three sub-modes preserve the human confirmations already in `decisions.md` - re-run only the
  Phase 9 mechanical-gate pass, then Phases 10 -> 11 -> 12, so the whole set reconciles and any rows
  the re-run touched are re-confirmed by the human before finalize. Under **Vision-diff**, only rows
  whose *readings* the changeset actually moved re-open for Phase 11; confirmations on untouched IDs
  stand.
- **(B) Rebuild from scratch** - discard the derived artifacts entirely and regenerate every phase
  as a fresh build (this is what to choose when the vision itself changed substantially, or the
  method drifted enough that patching is riskier than rebuilding). **Confirm once more** that this
  overwrites the existing bundle - including the human confirmations in `decisions.md`, which will
  be re-derived at low/med confidence and must be re-reviewed in Phase 11. On confirmation, reset
  `_status.md` (status `in-progress`, empty phase checklist), re-seed an empty `decisions.md`, and
  run from **Phase 0** through **Phase 12** exactly as a new build. If prior human confirmations
  are worth preserving, prefer (A), or capture them before the reset so Phase 11 can re-apply them.

Either way the Principles and quality gates still bind, and the run finalizes only at **Phase 12**
(flip `_status.md` back to `finalized`, recording what this pass changed).
