# Re-running on a finalized vision

Read this from **Phase 0** only when the bundle's `_status.md` reads `finalized` — a re-run.
On a fresh build or a resume of an `in-progress` bundle, skip it (cold weight otherwise).

The skill is meant to be **run again on the same vision** — to upgrade a bundle after the skill
itself improved, or to review/iterate the bundle with a stronger model (e.g. Ralph-looping). The
vision stays frozen and canonical throughout (S6); a re-run revises only the *derived* files.

**Detecting skill drift (the hash check).** A finalized bundle records `built-with-hash` in
`_status.md` — a fingerprint of the skill's output-shaping files at build time. At Phase 0,
recompute it **from the skill's own directory** and compare. The recipe (reproducible because
`git hash-object` normalizes and follows symlinks to real content):

```
git hash-object SKILL.md strategies.md templates.md rubrics.md | git hash-object --stdin
```

- **Matches** → the skill is unchanged since this bundle was built; no upgrade is warranted (a
  re-run would only be a Review/iterate pass).
- **Differs, or no `built-with-hash` recorded** (bundles built before this mechanism) → the skill
  content changed since the build; **recommend an Upgrade re-run**. The hash only says *that*
  something changed — fall back to the structural diff (file set, ID schemes, template shapes vs.
  the current `templates.md`) to decide *which* phases to re-run.

(A pure whitespace/line-ending-only change can flip the hash harmlessly — the structural diff then
finds nothing to do.)

**Confirm before re-opening.** When Phase 0 finds a bundle whose `_status.md` is `finalized`, do
**not** silently start editing. State that a finalized companion set already exists, report the
hash-check result (in sync / drifted), and ask the user to confirm a re-open. Only on
confirmation: flip `_status.md` back to `in-progress`, record that a re-run started (date +
reason), and proceed. If the user declines, stop.

Once confirmed, ask which kind of re-run this is:

- **Upgrade to current method** (the skill changed). Diff what's on disk against the bundle the
  *current* skill produces: missing files (a bundle built by an earlier skill version can lack
  files a later strategy introduced), missing IDs (an absent ID layer, column, or cross-reference
  line the current templates expect), stale templates. Re-run only the affected phases (each
  through its builder + critic sub-agents, as in the normal loop) to fill the gaps; leave
  still-correct artifacts as they are. Re-run the Phase 9 mechanical-gate pass and the Phase 10
  whole-bundle critic at the end so the whole set reconciles.
- **Review / iterate** (stronger model, looping). Hold the structure and re-examine the existing
  artifacts for quality — sharper clusters, tighter invariants, cleaner glossary, missed
  traceability — phase by phase, each phase's builder + critic sub-agents re-drafting and
  re-auditing against the vision. Each pass still ends with the Phase 9 mechanical gates, the
  Phase 10 whole-bundle critic, and a `finalized` flip; resume notes in `_status.md` carry what
  changed so successive loops compound rather than thrash.

Either way the Principles and quality gates still bind. Finalize as in Phase 10 (flip `_status.md`
back to `finalized`, recording what this pass changed).
