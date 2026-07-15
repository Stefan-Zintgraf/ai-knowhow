# Validation and Feedback

**Status:** First draft

Validation and feedback closes the lifecycle loop: it measures released behavior against the intended outcomes and decides which earlier decisions the evidence reopens. Shipping is not evidence of value, and usage alone is not an outcome. Without this stage the lifecycle's feedback arrow is decoration.

This is distinct from requirements validation (confirming that requirements describe the right behavior before building); see the [glossary](./glossary.md) for both senses.

## What to measure

- **Outcome measures** — the behavioral change the release hypothesis predicted, defined in the [vision](./product_vision.md) and the [definition one-pager](./product_definition.md).
- **Guardrail measures** — harm that must not occur while the outcome is optimized: support load, churn, error rates, cost, trust signals.
- **Qualitative signals** — follow-up interviews about actual use, support conversations, observed changes in workarounds.
- **Operational evidence** — incidents, degraded-mode events, performance under real load, deployment and recovery experience.

Distinguish usage from outcome: a heavily used feature that leaves the target outcome unmoved is a value finding, not a success.

Instrumentation is a requirement, not an afterthought. Define during [product definition](./product_definition.md) and [requirements engineering](./requirements_engineering.md) how each outcome and guardrail will be observed in production — a release whose outcome cannot be observed cannot be validated.

## Review cadence

Schedule the first outcome review, with a named owner, **before** the release ships; otherwise it happens only after a crisis. Subsequent reviews follow the loop cadence chosen during [lifecycle tailoring](./lifecycle_tailoring.md). Guardrails are monitored continuously, not only at reviews.

## What evidence can reopen

Route each finding to the decision it challenges. Typical routes:

| Evidence | Reopens |
| --- | --- |
| Outcome unmoved although the capability is used | Opportunity selection in [product definition](./product_definition.md) |
| Capability barely used | Value assumption — back to [product discovery](./product_discovery.md) |
| Users misuse it or build workarounds around it | Usability — [use cases and journeys](./use_cases_and_story_mapping.md) |
| Guardrail breached | Release scope, [quality scenarios](./quality_attributes.md), possibly vision principles |
| Incidents, operational pain, support burden | [Quality-attribute scenarios](./quality_attributes.md) |
| Terminology confuses users or support | Domain glossary and [domain model](./domain_discovery.md) |
| Repeated audit or compliance findings | [Requirements](./requirements_engineering.md) and their traceability |
| Evidence contradicts a foundational assumption | [Product vision](./product_vision.md) itself |

## Decide and record

Apply the same discipline as discovery decisions: **persevere, adapt, pause, or retire** — with evidence strength recorded in the decision log. Reopening a decision is the feedback loop working, not a failure.

Retiring scope is a first-class outcome: it needs transition requirements (migration, communication, decommissioning) just as new scope does — see [requirements engineering](./requirements_engineering.md).

## Common failure modes

- Treating "shipped" as "done" and never reviewing outcomes
- Vanity metrics: celebrating usage while the target outcome stands still
- Guardrails defined at planning time but never monitored
- Feedback collected diligently but never routed to a decision
- No named owner and no scheduled review, so validation happens only after incidents
- Reopening nothing because of sunk cost, or reopening everything because of one anecdote
- Measuring only the happy path while operational evidence accumulates unread

## Completion checks

- Every release hypothesis has a scheduled review with a named owner, set before shipping.
- Outcome and guardrail measures are observable in production.
- Each significant finding is routed: a named decision is reopened, or perseverance is recorded with rationale.
- Decisions are logged with the evidence and its strength.
- Retired scope is handled through transition requirements.
- The loop's cadence matches the tailored lifecycle, not ad-hoc urgency.

## Further material

**Examples:**

- A self-service signup flow lifts activation by 12% — but the support-ticket guardrail doubles. The review routes the finding to release scope: the flow skipped the workspace-naming step that support now handles by hand. The outcome measure alone would have declared victory.
- An export feature shows heavy weekly usage while the renewal rate it was meant to move stays flat. The team records it as a value finding — users export data *to leave* — and reopens opportunity selection in product definition rather than iterating on the feature.

**References:** [The North Star Playbook — Amplitude](https://amplitude.com/north-star); [HEART framework — Google Research](https://research.google/pubs/pub36299/); [Experiment Guide — Kohavi, Tang, Xu](https://experimentguide.com/).

**Agent rule sets:** [`ai-analyst-lab/north-star`](https://github.com/ai-analyst-lab/north-star) — a North Star Metric coach for Claude Code (audit a metric, decompose drivers, build the input tree), grounded in and cited to Amplitude's playbook; [`phuryn/pm-skills`](https://github.com/phuryn/pm-skills) — includes metric-tree and launch skills chaining spec → risk → success metrics; [`florianbonnet14/ThePowerOfAnalytics_ClaudeSkills`](https://github.com/florianbonnet14/ThePowerOfAnalytics_ClaudeSkills) — North Star metrics, KPI trees, and analysis planning, built from the author's book.

**Books:** *Trustworthy Online Controlled Experiments* — Ron Kohavi, Diane Tang, Ya Xu; *Lean Analytics* — Alistair Croll, Benjamin Yoskovitz; *The Lean Startup* — Eric Ries.
