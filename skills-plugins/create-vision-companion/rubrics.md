# Rubric contract

This is the shared contract for all phase rubric files. It is intentionally small: load it with the phase-specific rubric file, then use only the section for the phase being run.

Phase-specific rubrics:

- Phases 1-8: [rubrics-1-8.md](rubrics-1-8.md)
- Phases 9-12: [rubrics-9-12.md](rubrics-9-12.md)

No sub-agent loads `SKILL.md`. The orchestrator briefs sub-agents with the relevant rubric file, strategy section, template section, and artifact paths.

## Sub-agent use

For a producing phase, the builder sub-agent loads:

- the frozen vision
- this file
- the phase section in `rubrics-1-8.md` or `rubrics-9-12.md`
- the strategy section named by that phase
- the matching template section
- already-finalized prior-phase files

It drafts to disk and returns only a short summary.

For a critic phase, the critic sub-agent loads:

- the frozen vision
- this file
- the drafted artifact or finished bundle
- the prior-phase artifacts needed by the phase
- the phase's critic/checklist section in `rubrics-1-8.md` or `rubrics-9-12.md`

It never sees the builder's reasoning. It auto-fixes clear defects in place, logs unresolved residuals to `decisions.md` with a confidence tag, and returns only a short summary.

## Gate types

Mechanical gates are decidable by inspection. They run unattended. A green pass needs no human; an unambiguous failure is auto-fixed in place; a structurally unmeetable mechanical gate is a hard blocker and must halt the run.

Judgment gates are readings of the vision. A critic audits them adversarially. Residual judgment calls are logged to `decisions.md` for the single human review in Phase 11. Do not ask the human to verify a mechanical gate, and do not let a builder self-certify a judgment gate.

## Decision rows

Each unresolved judgment row in `decisions.md` uses `Confidence` of `low`, `medium`, or `high`. `confirmed` in the Confidence column is the resolved marker: the human has reviewed the row and accepted the reading as-is or as edited.

Rows are not resolved silently. If a human-directed change affects companion artifacts, a sub-agent applies it. The orchestrator does not edit artifacts itself during review.

Never resolve a decision by editing the frozen vision. If a derived file disagrees with the vision, the derived file changes.
