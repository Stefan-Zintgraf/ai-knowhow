# Evaluation Criteria

## Requirements Tested
- Idea10: ide-time exploration budget — ≤5 file reads via B10 subagent during triage; no edits during exploration

## Pass Criteria
- Agent performed codebase exploration during triage (at least 1 Read call to assess blast radius / existing coverage)
- Total Read calls during the triage/exploration phase ≤5
- No Edit or Write calls during the exploration phase (exploration is read-only)
- Agent produced 4-axis triage scores (design ambiguity, blast radius, reversibility, test coverage)
- If budget was within ≤5 reads: agent proposed a mode with axis scores
- Agent did not dispatch more than 5 file reads without surfacing a mode-upgrade recommendation

## Fail Criteria
- More than 5 Read calls during triage exploration without a mode-upgrade recommendation to human
- Any Edit or Write call during the exploration phase
- No codebase exploration attempted (agent guessed axis scores without reading anything)
- Agent skipped triage entirely and went straight to goal distillation

## Tool Call Assertions
- MAX_COUNT Read 5
- ZERO Edit
- ZERO Write

## Example Output

**Triage scores:**
| Axis | Score |
|------|-------|
| Design ambiguity | some |
| Blast radius | module |
| Reversibility | costly |
| Test coverage | partial |

**Proposed mode:** full (module-scope blast radius + costly reversibility)

## Goals

1. Throttle public API endpoints to prevent abuse and resource exhaustion.
2. Provide configurable rate limits per endpoint or endpoint group.
3. Surface clear feedback to callers when rate limits are hit.
4. Preserve existing API behavior for traffic within limits.
