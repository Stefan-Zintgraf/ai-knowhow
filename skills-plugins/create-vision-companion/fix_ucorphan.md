# Plan: honor unpromised UCs as coverage signals

## Purpose

Make `create-vision-companion` explicitly honor a `UC#` that realizes no `V#` —
today the flag is half-specified: `templates.md` (uc-index rules) already says
"`Scope = -` if it realizes none (flag such a UC in vision-index.md)", but the
vision-index template gives that flag no home, S9 doesn't name the signal, and no
critic check or mechanical gate enforces it. The result is an invisible success
path: a UC can pass every gate while its missing promise is never surfaced.

## Terminology — the leading word

**Unpromised UC** completes the existing pair into a triad of **coverage
signals**, all bidirectional readings of the `V# <-> UC#/CAP#` relation:

- **unrealized promise** — a `V#` no UC realizes (exists today),
- **unpromised capability** — a `CAP#` no `V#` names (exists today, as
  "gold-plating"),
- **unpromised UC** — a `UC#` that realizes no `V#` (new).

The triad is **defined once, in S9** (single source of truth). Every other site
edits down to a reference — "the three coverage signals (S9)" — never a
restatement. Output templates (vision-index, critic-report) may spell the three
names, since they shape human-facing artifacts, not skill prose.

Naming rule: **orphan** stays reserved for mechanical failures (a UC with no
row, actor, or primary capability). A no-V# UC is never called an orphan; it is
an unpromised UC. This kills the collision with "No orphans on either side" and
"zero orphans" in the existing gates.

## Target behavior

Every `UC#` ends in exactly one of two states:

1. **Promised**: realizes >=1 `V#`. `vision-index.md` lists it under the
   relevant `V#`; `uc-index.md` carries the lowest realizing `S#` as its
   `Scope`. (Unchanged.)

2. **Unpromised**: realizes no `V#`.
   - `uc-index.md` keeps the row (actor, primary capability, normalized intent)
     with `Scope = -`.
   - `vision-index.md` lists it in a dedicated `## Unpromised UCs` section.
   - The **Core-gate** always requires a Phase 6 `decisions.md` judgment row when
     the primary capability is tagged Core in `subdomains-and-context-map.md`
     (Phase 5). Supporting/Generic work is definitionally not expected to
     carry press-release promises, so an unpromised UC there is the expected
     case: its reading is recorded in the `Reason no V# fits` column and goes
     no further. An unpromised UC in a **Core** capability is anomalous — the
     differentiating work should keep a promise — and always gets a row. The
     Phase 6 critic may still escalate a Supporting/Generic one to a row when
     it doubts the recorded reason. The gate stays checkable without flooding
     Phase 11 with the obvious cases.
   - The vision is not edited. When the Core-gate or critic escalation sends the
     reading to Phase 11, the possible resolutions are: missing promise
     (candidate `V#` in a future vision revision), supporting/generic work (fine
     as-is), or out-of-scope (candidate parking-lot move in a future vision
     revision). These are Phase 11 outcomes recorded in the decisions row — not
     distinct derived states, and never a silent conversion to `BV#` (frozen
     vision owns `BV` IDs).

## Non-goals

- Do not require every UC to realize a `V#`, and never force-fit one to a weak
  `V#`.
- Do not edit the foundation vision.
- Do not treat a no-V# UC as a Phase 0 hard blocker (actor/capability coverage
  is still possible; blocker (c) stays about mechanical unownability).
- Do not add a `V#` column to `uc-index.md` — `Scope = -` *is* the cross-link,
  and a V# column would duplicate vision-index's realization table.

## Skill changes

### 1. `strategies.md` — S9 (the single source of truth)

- Extend S9 point 2 into the triad: name all three **coverage signals** (the
  definitions above), state that all three are surfaced for human review and
  never silently fixed by editing the vision, and that an unpromised UC carries
  `Scope = -` in the uc-index and a row in vision-index's `Unpromised UCs`
  section. The Core-gate always requires a `decisions.md` row when its primary
  capability is Core; the Phase 6 critic may escalate doubtful Supporting/Generic
  reasons to a row.
- In "Where judgment is required" (section 3), extend the existing
  coverage-flags bullet to the triad and its Phase 11 resolutions; don't add a
  separate bullet.

### 2. `templates.md`

- **uc-index (section 7) rules line**: sharpen the existing sentence to
  "`-` if it realizes none — valid only when the same UC appears under
  `Unpromised UCs` in vision-index.md."
- **vision-index (section 8)**: add after `Vision points -> realization`:

  ```markdown
  ## Unpromised UCs

  Use-cases realizing no press-release vision point — preserved, not force-fit.
  Each keeps `Scope = -` in [uc-index.md](uc-index.md). Those in a **Core**
  capability always carry a `decisions.md` row for the Phase 11 review. For
  Supporting/Generic ones the `Reason no V# fits` column is normally the whole
  record; the Phase 6 critic escalates doubtful reasons to `decisions.md`.

  | UC | Primary CAP | Reason no V# fits |
  |----|-------------|-------------------|
  | UC<n> | CAP<n> | <short reading> |
  ```

  (No constant "Coverage signal" warning column — the section heading already
  is the signal.)
- **vision-index Notes / judgment calls**: reword the existing bullet to name
  the three coverage signals (S9).
- **decisions.md (section 11)**: add one example row mirroring D4, teaching the
  Core-gate:

  ```markdown
  | D5 | 6 | UC17 (in Core CAP4) realizes no V# -> unpromised UC | force-fit to V3 | low | UC17, CAP4 |
  ```

- **critic-report.md (section 12) cross-phase "Promises" check**: extend to
  "unrealized-promise / unpromised-UC / unpromised-capability flags present,
  not reconciled by editing the vision."

### 3. `rubrics-1-8.md`

- **Phase 6 builder** (add `subdomains-and-context-map.md` to its reads): after
  mapping every `V#`, compute the reverse relation — every `UC#` in the
  capability map appearing in no `V#` realization set — write those to
  `Unpromised UCs` with the `Reason no V# fits` column filled, set their native
  rung to `-` for Phase 7. The Core-gate always requires a `decisions.md` row
  when the primary CAP is tagged **Core**; the critic may escalate doubtful
  Supporting/Generic reasons. A capability can serve some `V#`
  while containing individual unpromised UCs; flag the UCs anyway.
- **Phase 6 critic**: extend "Promises reconciled, not edited" to the three
  coverage signals (S9); check no unpromised UC was force-fit to a weak `V#`,
  every Core-CAP one has its `decisions.md` row, and every Supporting/Generic
  one has a credible reason recorded — escalating it to a row when the reason
  is doubtful.
- **Phase 6 pre-check**: add "every `UC#` appears under >=1 `V#` realization
  *or* in `Unpromised UCs`."
- **Phase 7 builder**: carry `Scope = -` from Phase 6; do not invent a rung.
- **Phase 7 pre-check**: `Scope = -` only if the UC is listed in
  `Unpromised UCs`.

### 4. `rubrics-9-12.md`

- **Phase 9 mechanical gates** — add a **promise coverage** gate beside the
  existing (mechanical) total-coverage gate:
  - every `UC#` is in exactly one state: either it realizes >=1 `V#`, is absent
    from `Unpromised UCs`, and has a non-`-` scope; or it realizes no `V#`,
    appears exactly once in `Unpromised UCs`, and has `Scope = -`;
  - every `Unpromised UCs` entry has a filled `Reason no V# fits`; the Core-gate
    always requires a `decisions.md` row when its primary CAP is Core, while a
    Supporting/Generic entry may have one when the Phase 6 critic escalated a
    doubtful reason;
  - no `Unpromised UCs` row cites a nonexistent UC or CAP.
- **Phase 10** "Promises reconciled, not edited": extend to the three coverage
  signals (S9).
- **Phase 12** "Mechanical gates still green": append "promise coverage" to the
  illustrative gate list (it already defers to the Phase 9 set). Re-running the
  Core-gate here also closes the flip case: if the human re-tags a capability
  Supporting -> Core in Phase 11, its unpromised UCs now fail the gate, get
  their rows, and loop back to Phase 11 via the existing "no new unconfirmed
  reading left dangling" check.

### 5. `SKILL.md` (minimal — no sub-agent loads it)

- **Phase 0 coverage targets**: extend the parenthetical with "every `UC#`
  traced to >=1 `V#` or flagged unpromised".
- **Principles, "Bidirectional traceability"**: one clause resolving the
  terminology collision — *orphan* is mechanical (no row/actor/capability); a
  UC realizing no `V#` is an **unpromised UC**, a coverage signal (S9), not an
  orphan. Do not restate the triad here.

### 6. `re-running.md` (two micro-edits to the Vision-diff closure)

- modified/added `UC`: "...the `V#` coverage flag it realizes **(or its
  `Unpromised UCs` row)** in `vision-index.md`..."
- removed `UC`: "...re-check its old cluster/`V#` **and any `Unpromised UCs`
  row** for a new orphan or gap."

(`rubrics.md` is untouched — verified it defines gate *types*, not coverage, so
there is no global definition to extend; adding one would be duplication.)

## Acceptance checks

Fixture vision: `V1` realized by `UC1`; `V2` realized by no UC; `UC2` and `UC3`
with actors and capabilities but no matching `V#`; `CAP1` (**Core**) containing
`UC1` and `UC2`; `CAP2` (**Supporting**) containing `UC3`.

Expected derived output:

- `vision-index.md` lists `V2` as an unrealized promise, and `UC2` and `UC3`
  under `Unpromised UCs`, each with a filled `Reason no V# fits`.
- `capability-map.md` still says `CAP1` serves `V1`.
- `uc-index.md` has `UC2` and `UC3` with `Scope = -`.
- `decisions.md` has a Phase 6 row for `UC2` (Core-gate) and none for `UC3`.
- Phase 9 goes green only with the `Scope = -` <-> `Unpromised UCs`
  cross-links resolving and the Core-gate satisfied.
- Phase 11 presents the `UC2` row; the human never sees a `UC3` prompt.

## Implementation order

1. `strategies.md` — S9 owns the triad definition.
2. `templates.md` — the artifacts get their home for the signal.
3. `rubrics-1-8.md` — Phases 6-7 create and carry it.
4. `rubrics-9-12.md` — Phases 9/10/12 enforce it.
5. `SKILL.md` — Phase 0 target + the orphan/unpromised naming clause.
6. `re-running.md` — the two closure micro-edits.

After landing, `built-with-hash` flips for every finalized bundle — expected;
the re-run "Upgrade to current method" sub-mode is the designed path to
back-fill `Unpromised UCs` sections into existing bundles.

## Done definition

A run cannot finish with a no-V# UC hidden inside a capability: it is either
traced to a `V#`, or visibly carried as an unpromised UC through
`vision-index.md`, `uc-index.md` (`Scope = -`), the Phase 9 promise-coverage
gate, and the Phase 10 critic — reaching the human in Phase 11 only when its
primary capability is Core (or the critic escalates a doubtful reason).
