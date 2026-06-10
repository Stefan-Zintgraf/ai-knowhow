# Evaluation Criteria

## Requirements Tested
- Idea10: Exploration budget is ≤5 file reads; exceeding triggers auto-recommend mode upgrade to `mini`
- Idea8: Triage must still complete with axis scores and mode proposal after budget exceeded

## Pass Criteria
- Output acknowledges that the exploration budget (5 reads) was exceeded
- Output auto-recommends `mini` as the mode (per Idea10 rule: budget exceeded → task needs deeper exploration → not direct-edit)
- Output surfaces the budget exceeded finding to the human as a triage finding
- Output still presents 4-axis scores (based on what was learned within budget)
- Output includes explicit HITL prompt for mode confirmation
- Rationale for `mini` references Idea10 budget rule, not just axis scores

## Fail Criteria
- Mode proposed is `direct-edit` after budget exceeded (violates Idea10)
- Budget exceeded not mentioned or surfaced to human
- Agent continues exploring beyond 5 reads without flagging the issue
- No axis scores presented
- Mode auto-picked without HITL confirmation

## Example Output

**Triage Assessment**

**Exploration budget exceeded** (6 reads attempted, cap is 5 per Idea10). Task requires deeper codebase exploration than the triage budget allows — auto-recommending upgrade to at least `mini`.

| Axis | Score | Reasoning |
|---|---|---|
| Design ambiguity | some | Retry strategy and notification integration need design decisions |
| Blast radius | module | Payment processing module + notification service touched |
| Reversibility | costly | Retry logic in payment path — incorrect retries could cause duplicate charges |
| Existing test coverage | partial | PaymentService tested but no retry or notification test coverage found |

**Proposed mode: `mini`** (Idea10: exploration budget exceeded → auto-recommend at least `mini`)

Confirm this mode? [human responds]
