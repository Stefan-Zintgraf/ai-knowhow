# Evaluation Criteria

## Requirements Tested
- Idea8: 4-axis triage must score at least one axis high (system blast radius, hard reversibility, no test coverage for auth middleware) and propose `full` mode
- Idea4: Agent must present axis scores and proposed mode to human for confirmation
- 3.29: High-complexity task uses full pipeline; auth is a tripwire surface forcing `full` regardless

## Pass Criteria
- Output contains a 4-axis scoring table with values for all four axes
- At least one axis scored at highest level (lots of ambiguity, system blast, hard reversibility, or no coverage)
- Proposed mode is `full`
- Output identifies auth/security as a tripwire surface (from the 3.29 list)
- Output includes explicit prompt asking human to confirm mode
- Chain described is the full pipeline: `ide → aln → [res?] → [pro?] → prd → iss → ral|par → qa`

## Fail Criteria
- Mode proposed is `direct-edit` or `mini` for an auth system replacement
- Tripwire surface (auth/security) not identified
- Fewer than 4 axes scored
- Mode auto-picked without HITL confirmation prompt

## Example Output

**Triage Assessment**

| Axis | Score | Reasoning |
|---|---|---|
| Design ambiguity | lots | JWT architecture, refresh rotation strategy, revocation model all need design |
| Blast radius | system | 40 endpoints, auth middleware, database schema change |
| Reversibility | hard | Auth migration affects all authenticated requests; rollback requires dual-mode support |
| Existing test coverage | none | Auth middleware is mocked in all endpoint tests |

**Tripwire surfaces detected:** auth, security, schema, broad architecture

**Proposed mode: `full`**
Chain: `ide → aln → [res?] → [pro?] → prd → iss → ral|par → qa`

Confirm this mode? [human responds]
