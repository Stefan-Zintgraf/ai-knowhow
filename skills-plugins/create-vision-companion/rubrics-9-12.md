# Phase rubrics 9-12 - end review and finalize

Read [rubrics.md](rubrics.md) first. Load this file only after Phase 8 completes, or when resuming an in-progress bundle whose next phase is 9, 10, 11, or 12.

The orchestrator still does no derivation itself. Every artifact write or audit in Phases 9, 10, and 12 happens in a fresh sub-agent. During Phase 11, the orchestrator conducts the human review one `decisions.md` row at a time, and any artifact edits requested by the human are applied by a sub-agent.

---
## Phase 9 - `README.md` + full mechanical gate sweep

**Builder reads:** templates section 1 - the whole finished set.
**Derive:** write `README.md` - the map + per-task load order + the vision-wins rule,
acknowledging the `<slug>-architecture-lens.md` sibling. Then run the **full mechanical
checklist below, unattended**. A green pass needs no human. An unambiguous failure is auto-fixed
in place. A *structurally* unmeetable gate is a hard blocker -> halt and surface (Phase 0). Return
a short pass/fail summary; the orchestrator only updates `_status.md`.

**Mechanical gates (complete set - run every one):**
- **Vision unchanged** - byte-identical source; the bundle only added files.
- **Total coverage** - 100% of UCs in `uc-index.md`, each with >=1 capability and >=1 actor. Zero
  orphans.
- **Parked items routed** - every `BV` item lands in exactly one home: an `INV` (cross-cutting)
  or a `deferred-inputs.md` entry tagged with its consuming phase. Zero parked orphans.
- **Every `V#` and `S#` present** - every `V#` maps to its `S#` and >=1 realizing UC *or* a
  flagged coverage gap; every `S#` rung is on the ladder with the anchor marked and the horizon
  recorded; the horizon cites `<slug>-architecture-lens.md` (not re-derived).
- **Promise coverage** - every `UC#` is in exactly one state: either it realizes >=1 `V#`, is
  absent from `Unpromised UCs`, and has a non-`-` scope; or it realizes no `V#`, appears exactly
  once under `Unpromised UCs`, and has `Scope = -`. Every unpromised-UC entry has a filled
  `Reason no V# fits`; the Core-gate always requires a `decisions.md` row when its primary CAP
  is Core, while a Supporting/Generic entry may have one when the Phase 6 critic escalated a
  doubtful reason. No `Unpromised UCs` row cites a nonexistent UC or CAP.
- **Invariants cited** - every `INV` cited by >=1 UC; no invariant restated verbatim in a
  normalized line or capability description (referenced by `INV` id instead).
- **Bidirectional links resolve** - pick any UC and trace it forward and back.

**Critic check (judgment -> `decisions.md`):**
- **Independently loadable** - each doc makes sense loaded alone with the glossary + invariants.

---

## Phase 10 - whole-bundle critic (cross-phase)

**Reads:** the frozen vision - the entire finished set. Writes `critic-report.md` and applies
its own clear fixes in place. Iterate (default cap 3 passes) until clean; unresolved items stay
in `critic-report.md`. Catches *cross-phase* compounding the per-phase critics could not see.
**Every residual human-judgment finding is also appended to `decisions.md`** (unconfirmed, with a
confidence tag and cites), so Phase 11 reviews one unified surface. **Does not finalize.**

**Bundle-wide judgment checks:**
- **Cross-phase compounding** - a reading settled in one phase that mis-propagates into a later
  one (e.g. a glossary term collapsed in Phase 2 that mis-clusters capabilities in Phase 4).
- **Single language across the whole bundle** - the glossary's canonical terms are used
  consistently in every file; no synonym re-introduced downstream.
- **Altitude held everywhere** - no tactical pattern, tech/platform choice, or MVP/phasing
  leaked into *any* file.
- **Promises reconciled, not edited** - the three coverage signals (S9) are surfaced across
  the set, never reconciled by touching the vision.
- **Independently loadable** - each doc still stands alone with glossary + invariants.

---

## Phase 11 - item-by-item `decisions.md` review (human gate)

*The single human-in-the-loop gate; not a sub-agent pass - the orchestrator runs it directly with
the human.* Every earlier phase's residual readings (per-phase critics **and** the Phase 10
whole-bundle critic) are now collected as rows in `decisions.md`. Walk them **one row at a time**.

**For each row, present:** the reading taken - the alternative rejected - confidence - cites
(`UC`/`V`/`S`/`INV`/`BV`), then take the human's adjudication. Do **not** batch rows.
There is exactly one active row and exactly one adjudication prompt at a time.
Review unresolved rows in confidence order: all `low` rows first, then `medium`, then `high`.
Within each confidence band, preserve the row order already present in `decisions.md`.

- If the human **accepts** the reading as-is -> set the row's **Confidence** to **`confirmed`**.
- If the human **changes** it (a cut, merge, reword, re-cluster, re-tag) -> **spawn an edit
  sub-agent** to apply the change to the affected companion artifact(s); the orchestrator does not
  edit artifacts itself. Update the row to record the reading actually taken, then set its
  **Confidence** to **`confirmed`**.
- If the human asks a **counter-question**, asks for more context, challenges the framing, or gives
  a partial answer -> answer the question, then re-present the **same row** for adjudication. Do not
  mark the row confirmed, spawn edits, ask about another row, or treat the counter-question as an
  adjudication.
- Never resolve a row by editing the **vision** (S6) - fix the derived file.

**Exit gate (mechanical):** **every row in `decisions.md` has `Confidence = confirmed`** - zero rows left
with `low` / `medium` / `high` confidence. Update `_status.md` after each adjudication (the open-decisions count and the next
unreviewed row) so the review resumes cleanly across sittings.

---

## Phase 12 - critic reconcile -> finalize

**Reads:** the frozen vision - the entire set as left by Phase 11 (all decisions `confirmed`).
Re-spawn the **whole-bundle critic** (fresh sub-agent) to **update `critic-report.md`** so it
reflects the Phase 11 changes - the confirmed `decisions.md` rows and any artifact edits they
triggered - and to reconcile any companion files those edits touched. It applies its own clear
fixes in place.

**Checks:**
- **`critic-report.md` reflects the confirmed state** - each prior finding shows its disposition
  (fixed / accepted-by-human / superseded); no finding still points at a since-edited artifact.
- **No new unconfirmed reading is left dangling** - if this pass surfaces a *new* human-judgment
  residual, append it to `decisions.md` (unconfirmed) and **loop back to Phase 11** for that row
  before finalizing; do not confirm it on the human's behalf.
- **Mechanical gates still green** (Phase 9 set) after the Phase 11 edits - coverage, promise
  coverage, bidirectional links, INV-cited, parked-items routed, every `V#`/`S#` present, vision
  byte-unchanged. (Re-running the Core-gate here catches the flip case: a capability re-tagged
  Supporting -> Core in Phase 11 makes its unpromised UCs fail the gate, gain their rows, and
  loop back to Phase 11 via the no-dangling-reading check.)

**Finalize (only here):** flip `_status.md` to `finalized`, record the date (and, if a re-run,
what this pass changed), stamp `built-with-hash`, and **(re)write `vision-manifest.md`** - the
per-ID fingerprint of the frozen vision that lets the next re-run diff which items changed and scope
itself (both recipes in [re-running.md](re-running.md); manifest shape in [templates.md](templates.md) section 13). The
folder name does not change. **The bundle is finished only when this phase completes.**
