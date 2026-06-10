# How to Regenerate `idea.md`

This file documents how to regenerate `idea.md` (the goal-distillation
output for this work-item) using the project skill chain. It is meta-
instruction maintained by humans; the `distill-idea` skill does NOT
emit it.

## Two-axis choice

- **Axis 1:** rebuild the skill itself, or reuse the existing compiled skill?
- **Axis 2:** which anchor-doc snapshot — current `HEAD`, or a pinned commit?

For determinism testing, pin the anchor docs to a commit; for an "is the
design captured?" rerun, use `HEAD`.

---

## Path A — Lightweight rerun (regenerate `idea.md` only)

Use when: the existing `skills/output/distill-idea.md` is acceptable and
you only want to refresh `idea.md` against the latest anchor docs.

Invocation (paste at a fresh prompt):

```
/distill-idea

WI slug: coding_workflow
Anchor docs (read these in full before distilling):
  - guardrails.md (core rules §3.* + routing index §4.* + parallel table §9)
  - gr/gr_idea.md (Idea1–Idea11 — phase-entry, modes, triage matrix)
  - gr/gr_algn.md (Aln1–Aln19 — grilling, collapsed-aln spec)
  - gr/gr_tdd.md (TDD1–TDD11 — TDD loop + direct-edit exemption)
  - gr/gr_qa.md (Q1–Q12 — manual qa, mode-dependent shape)
  - gr/gr_proto.md, gr/gr_res.md, gr/gr_mod.md, gr/gr_rev.md,
    gr/gr_adr.md, gr/gr_domain_language.md, gr/gr_governance.md
  - phases.md (phase definitions and sequence)
  - coding_plan.md (work-item state — W1–W17, A1–A11, B1–B11, C1–C8, D1–D9)

Brief (verbatim):
  Define an end-to-end AI coding workflow covering greenfield and
  brownfield work. Establish guardrails that protect system intent
  without bloating always-on agent context. Operationalize the
  workflow and guardrails as enforceable agent behavior — skills,
  hooks, templates — not prose-only docs. Keep planning effort
  proportionate so the workflow reaches real code quickly. Provide
  shortcuts for small coding tasks so the full pipeline collapses
  appropriately rather than being skipped silently.
```

Expected output:

- `plan/coding_workflow/idea.md` — Goals + Starting Point.
- `plan/coding_workflow/status_idea.md` — frontmatter only.

Skip behavior: per `gr_idea.md` §"Apply When", if the brief already
names 3–6 explicit goals (it does), `ide` collapses to a one-line
confirmation — the goal list is restated verbatim, not re-distilled.

---

## Path B — Full regeneration (rebuild the skill chain first)

Use when: anchor docs have shifted enough that the prior `distill-idea`
skill may no longer reflect the design (e.g. after Idea8–Idea11 landed).
Three steps. Steps 1 and 2 hand-off via files; step 3 is Path A.

### Step 1 — `/draft-skill-input distill-idea`

Inputs (read in full):

- `coding_plan.md` — especially the W15 "Contracts settled" block and Pocock skill index.
- `phases.md` — `ide` phase §1.
- `guardrails.md` — §3.32 idea, §3.29 mode selection, §3.37 tripwire.
- `gr/gr_idea.md` — Idea1–Idea11.
- `tpl/tpl_idea.md` — C8 template, the output-shape contract.
- Reference skills (load full SKILL.md bodies):
  - `skills-plugins/matt_pocock_skills/skills/productivity/grill-me/SKILL.md`
  - `skills-plugins/matt_pocock_skills/skills/productivity/write-a-skill/SKILL.md`
  - `.claude/skills/distill-idea/skill.md` — the current compiled version, for reference only; do not copy.

Output: `skills/input/distill-idea-in.md` (tool-managed; do not hand-edit).

### Step 2 — `/compile-skill skills/input/distill-idea-in.md`

Input: the file produced by Step 1.
Output: `skills/output/distill-idea.md` (tool-managed; do not hand-edit).

Note: also update `.claude/skills/distill-idea/skill.md` symlink/copy
if the install requires it (check repo convention).

### Step 3 — Run Path A above.

---

## Reproducibility notes

- The skill produces **goals** (3–6 entries + Starting Point). It does NOT
  produce the design contracts that crystallized during alignment — those
  live in `gr/*` detail docs, not in `idea.md`.
- `idea_ref.md` (sibling file) is the gold-standard baseline. Diff a fresh
  `idea.md` against `idea_ref.md` to assess skill-chain determinism. The
  diff should be small and meaning-preserving; large divergence is a
  signal that the skill prompt needs tightening.
- Stochasticity sources: model sampling (mitigate with `temperature=0`),
  model version drift, anchor-doc drift. For a strict determinism test,
  pin all three (git checkout the anchor commit, fix model + temp=0).
- Per the project rule in `CLAUDE.md`, files matching `*_ref.md` are
  frozen baselines — do not hand-edit. `idea_ref.md` is updated only by
  re-running this regeneration and copying the cleaned output.
- This file (`idea_recreation.md`) is itself part of `plan/coding_workflow/`
  and retires with the rest of the WI directory at WI close per 3.33.
