# Evaluation Criteria

## Requirements Tested
- Idea8: Triage must identify tripwire surface (public API) even though individual axes score low
- 3.29: Tripwire override — public API change forces `full` regardless of axis scores
- 3.37: Tripwire surface detection is the prerequisite for mid-task halt enforcement
- Idea4: HITL pick mandatory even for tripwire-forced mode

## Pass Criteria
- Output contains a 4-axis scoring table with values for all four axes
- Individual axes may score low (the brief describes a simple additive change)
- Output explicitly identifies "public API" as a tripwire surface from the 3.29 list
- Proposed mode is `full` — tripwire override noted as the reason
- Output makes clear that tripwire surface overrides what axis scores alone would suggest
- Output includes explicit prompt asking human to confirm mode

## Fail Criteria
- Mode proposed is `direct-edit` or `mini` — public API is a tripwire surface, always `full`
- Tripwire surface not identified despite "public user profile API endpoint" and versioned URL in brief
- Axis scores presented without mentioning tripwire override
- Mode auto-picked without HITL confirmation prompt

## Example Output

**Triage Assessment**

| Axis | Score | Reasoning |
|---|---|---|
| Design ambiguity | none | Field exists in DB, just needs serializer addition |
| Blast radius | local | One serializer, additive field |
| Reversibility | trivial | Additive API field, backwards compatible |
| Existing test coverage | covers it | Full contract tests exist |

**Tripwire surface detected:** public API (`GET /api/v2/users/:id` — versioned public endpoint)

**Tripwire override: axes suggest `direct-edit`, but public API surface forces `full`.**

**Proposed mode: `full`**
Chain: `ide → aln → [res?] → [pro?] → prd → iss → ral|par → qa`

Confirm this mode? [human responds]
