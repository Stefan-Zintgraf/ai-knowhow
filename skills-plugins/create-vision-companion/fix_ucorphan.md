# Plan: honor orphaned UCs as coverage signals

## Purpose

Make `create-vision-companion` explicitly honor a `UC#` that realizes no `V#` as a
coverage signal, not as an invisible success and not as an automatic blocker.

This artifact uses "orphaned UC" narrowly:

- It is a use-case present in the frozen foundation vision.
- It has a valid actor and a primary capability.
- It does not realize any press-release vision point (`V#`), so it has no native
  scope rung inherited from a `V#`.

That is different from a true mechanical orphan, such as a UC with no actor, no
primary capability, or no row in `uc-index.md`. Those remain mechanical failures.

## Target behavior

Every `UC#` must end in exactly one of these states:

1. **Promised UC**: realizes at least one `V#`.
   - `vision-index.md` lists it under the relevant `V#`.
   - `uc-index.md` carries the lowest realizing `S#` as its `Scope`.

2. **Unpromised UC coverage signal**: realizes no `V#`.
   - `uc-index.md` keeps the UC row, with actor, primary capability, and
     normalized intent.
   - `uc-index.md` sets `Scope` to `-`.
   - `vision-index.md` lists it in a dedicated coverage section, e.g.
     `## Unpromised UCs`.
   - `decisions.md` gets a Phase 6 judgment row unless the fit is obvious and
     already confirmed by the artifact's local rules.
   - The vision is not edited. The human resolves the reading in Phase 11.

3. **Out-of-scope item**: the item should not have been a UC at all.
   - The companion cannot silently convert it into `BV#`, because the vision is
     frozen and canonical.
   - It is still represented as a UC in the derived files.
   - `decisions.md` records the human-facing finding: "UCn appears out of scope;
     candidate move to parking lot in a future vision revision."

## Non-goals

- Do not require every UC to realize a V#.
- Do not force-fit a UC to a weak V#.
- Do not edit the foundation vision.
- Do not treat a no-V# UC as a Phase 0 hard blocker if actor and capability
  coverage remain possible.
- Do not demote the UC to `BV#` in derived artifacts. `BV#` IDs must come from
  the frozen vision.

## Skill changes to make

### 1. `strategies.md`

Edit S9 so vision-point traceability is explicitly bidirectional:

- A `V#` with no realizing UCs is an **unrealized promise**.
- A `UC#` with no realizing `V#` is an **unpromised use-case**.
- A `CAP#` with no serving `V#` is candidate **gold-plating**.

Add the rule that all three are coverage signals surfaced for human review, never
silently fixed by editing the vision. Clarify that `uc-index.md` uses `Scope = -`
for unpromised UCs.

Also update the "Where judgment is required" list to include:

- `UC# -> V#` absence: whether the UC is a missing promise, supporting/generic
  work, or a candidate future vision revision is a reading that must be surfaced.

### 2. `SKILL.md`

In Phase 0 setup coverage targets, change:

> every `V#` traced or its gap flagged

to include:

> every `UC#` either traced to at least one `V#` or flagged as an unpromised UC.

In the principles section, refine "No orphans on either side" so it does not
confuse no-V# UCs with mechanical orphan failures:

- Mechanical coverage: every UC has a row, actor, and primary capability.
- Promise coverage: every UC either realizes a V# or is explicitly flagged as an
  unpromised UC.

### 3. `templates.md`

Update `uc-index.md` template:

- Keep the existing `Scope = -` convention.
- Strengthen the line to say `Scope = -` is valid only when the same UC appears
  in `vision-index.md` under `Unpromised UCs`.
- Add a `Promise` or `V#` column only if the table remains readable. Preferred
  minimal change: keep the current columns and make `Scope = -` the cross-link to
  `vision-index.md`.

Update `vision-index.md` template:

- Add a section after `Vision points -> realization`:

```markdown
## Unpromised UCs

Use-cases that realize no press-release vision point. These are preserved, not
force-fit. Each remains in `uc-index.md` with `Scope = -`; the human decides
whether it implies a missing `V#`, supporting/generic work, or a future vision
revision.

| UC | Primary CAP | Reason no V# fits | Coverage signal |
|----|-------------|-------------------|-----------------|
| UC<n> | CAP<n> | <short reading> | WARNING unpromised UC - review |
```

- Update `Notes / judgment calls` to name three signals:
  - unrealized promises (`V#` no UC delivers),
  - unpromised UCs (`UC#` no V# names),
  - unpromised capabilities (`CAP#` no V# names).

Update `decisions.md` example rows with one unpromised UC example:

```markdown
| D5 | 6 | UC17 realizes no V# -> flagged unpromised UC | force-fit to V3 | low | UC17 |
```

Update `critic-report.md` cross-phase checks:

- Change "Promises" to include unpromised UC flags, not only unrealized promise
  and unpromised capability flags.

### 4. `rubrics-1-8.md`

Update Phase 6 builder brief:

- After mapping every `V#`, compute the reverse relation: every `UC#` in the
  capability map that appears in no `V#` realization set.
- Write those UCs to `vision-index.md` under `Unpromised UCs`.
- Set their native rung to `-` for Phase 7.
- Back-fill `Serves: V#` as before. A capability can serve some V# while still
  containing individual unpromised UCs; those UCs must still be flagged.

Update Phase 6 critic checks:

- Add: flag every **unpromised UC** (`UC#` no `V#` realizes it); never force-fit
  it to a weak `V#`; log unresolved readings to `decisions.md`.
- Keep existing unrealized promise and unpromised capability checks.

Update Phase 6 pre-check:

- Every `V#` maps to its `S#`.
- Every `S#` is on the ladder.
- Every `UC#` either appears under at least one `V#` realization or appears in
  the `Unpromised UCs` section.

Update Phase 7 builder brief:

- Carry `Scope = -` for UCs marked unpromised by Phase 6.
- Do not invent a scope rung for them.

Update Phase 7 pre-check:

- `Scope = -` is allowed only if the UC is listed as unpromised in
  `vision-index.md`.

### 5. `rubrics-9-12.md`

Update Phase 9 mechanical gates:

- Keep total UC coverage as row/actor/capability coverage.
- Add promise coverage:
  - every `UC#` either realizes at least one `V#` or is listed in
    `vision-index.md` as an unpromised UC;
  - every `uc-index.md` row with `Scope = -` has a matching `Unpromised UCs`
    entry;
  - no `Unpromised UCs` row points at a nonexistent UC or capability.

Update Phase 10 whole-bundle critic:

- Extend "Promises reconciled, not edited" to check unrealized promises,
  unpromised UCs, and unpromised capabilities.
- Residual interpretation of an unpromised UC goes to `decisions.md`.

Update Phase 12 final checks:

- Mechanical gates still green must include promise coverage, including the
  unpromised UC cross-links.

### 6. `rubrics.md` if needed

If the shared rubric contract names coverage globally, add the same distinction:

- mechanical coverage means every source ID is represented;
- promise coverage means missing `V# <-> UC#` relationships are surfaced as
  reviewable signals.

Do not duplicate detailed phase rules here unless `rubrics.md` already owns a
global definition.

### 7. `re-running.md`

Update the vision-diff closure rules if they mention changed UCs:

- A changed or added UC must re-open the `vision-index.md` promise coverage row
  for that UC, not only the `uc-index.md` and capability cluster.
- A removed UC must re-check any `V#` realization and any `Unpromised UCs` row
  that referenced it.

## Acceptance checks

Use a fixture vision with:

- `V1` realized by `UC1`.
- `V2` realized by no UC.
- `UC2` with actor and capability but no matching `V#`.
- `CAP1` containing both `UC1` and `UC2`.

Expected derived output:

- `vision-index.md` lists `V2` as an unrealized promise.
- `vision-index.md` lists `UC2` under `Unpromised UCs`.
- `capability-map.md` can still say `CAP1` serves `V1`.
- `uc-index.md` includes `UC2` with `Scope = -`.
- Phase 9 passes only if `UC2` has actor and primary capability and the
  `Scope = -` row cross-links to `vision-index.md`.
- Phase 10/11 surface the interpretation as a human-reviewable judgment if it is
  not obviously confirmed.

## Implementation order

1. Update `strategies.md` so the method is explicit.
2. Update `templates.md` so generated artifacts have a home for unpromised UCs.
3. Update `rubrics-1-8.md` Phase 6 and Phase 7 so builders and critics create
   and carry the signal.
4. Update `rubrics-9-12.md` so final gates enforce the signal.
5. Update `SKILL.md` setup/principles language to reflect the refined coverage
   model.
6. Update `rubrics.md` and `re-running.md` only where they already define global
   coverage or changed-ID closure.

## Done definition

The skill honors orphaned UCs when a downstream run cannot finish with a
UC-without-V# hidden inside a capability. The UC must either be traced to a `V#`
or visibly carried as an unpromised UC coverage signal through:

- `vision-index.md`,
- `uc-index.md`,
- Phase 9 mechanical gates,
- Phase 10 critic checks,
- and Phase 11 human decisions when interpretation is required.
