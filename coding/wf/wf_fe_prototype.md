# Workflow: Front-End Prototype Route for Visual Decisions

Purpose: use AI for exploratory UI generation when visual/UX direction is uncertain, without pretending the agent can judge mature front-end quality.

Scope: invoked from the `aln` phase via [`gr/gr_alignment.md`](../gr/gr_alignment.md) Aln17. Decision to run this workflow is made during alignment, not deferred to implementation.

Origin: Pocock workflow W11 ("Front-End Prototype Route for Visual Decisions").

---

## When to Use

- Visual design, layout, interaction shape, or UX direction is uncertain.
- Grilling cannot resolve the decision in words — the choice only becomes concrete when seen.
- The ambiguity is genuinely visual. Backend, data, or contract decisions do **not** qualify.

---

## Inputs

- UI goal (from alignment so far).
- Existing design system, if any.
- Throwaway route or sandbox page where variants can live without polluting the production tree.

---

## Steps

1. Ask the agent to produce several prototype variants (typically 2–3).
2. Put variants behind a temporary route or switchable UI.
3. Human / domain expert clicks through variants. Agent does not self-judge.
4. Capture chosen direction and feedback.
5. Feed the chosen direction back into grilling or PRD — it becomes a normal alignment outcome (feeds Aln12 module map; Aln15 captures rejected variants as negative decisions).
6. Delete or rewrite throwaway prototype code **before** production implementation begins.

---

## Outputs

- Prototype options (throwaway).
- Human-selected direction.
- Better UI requirements fed back into `aln` / `prd`.

---

## Benefits

- Early visual feedback before committing to an implementation.
- Avoids overcommitting to AI-generated front-end code as production code.

---

## Tradeoffs

- Prototype code is likely low quality.
- Requires human attention to inspect visuals — not AFK-compatible.

---

## Failure Modes

- **Prototype leaks into production** — step 6 skipped or partial. Mitigation: throwaway route lives in a clearly marked sandbox path; deletion is a precondition for closing the `aln` phase on this decision.
- **Agent ignores design system** — existing system not supplied as input, or agent invents tokens. Mitigation: design system is a mandatory input when one exists.
- **Human picks aesthetics but misses accessibility / responsiveness** — review criteria not stated. Mitigation: variant evaluation must explicitly include a11y and responsive behavior, not only look.

---

## Validation Idea

Track whether prototype-derived PRDs reduce later UI rework compared to PRDs without a prototype step.

---

## Notes on Interaction with Other Guardrails

- Entry point: `gr_alignment.md` Aln17.
- Output feeds: Aln12 (module map), Aln15 (negative decisions for rejected variants), `prd` phase.
- Not AFK: inherits Aln1 (alignment is strictly HITL).
