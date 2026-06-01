# Evaluation Criteria

## Requirements Tested
- Idea1: More than 6 means goals are not yet major — must decompose or merge. Input has 8+ concerns; output must consolidate to ≤6
- Idea2: No implementation details in goals
- Idea5: Brief with many concerns distilled into coherent major goals, not echoed as a list

## Pass Criteria
- Goal count is between 3 and 6 (inclusive) — must consolidate the 8+ input concerns
- Each goal is a major intent, not a line-item from the brief
- Related concerns are merged into coherent goals (e.g., catalog + ownership → single goal; search + discoverability → single goal)
- No implementation details in goals
- Goals collectively cover the major themes: service catalog/ownership, API doc consolidation, runbook discoverability, dependency visibility, access controls, portal reliability

## Fail Criteria
- More than 6 goals (failed to consolidate)
- Goals are just the brief's bullet points rephrased 1:1 without merging
- Any goal contains implementation specifics (specific tech, architecture, CI details)
- Major theme from the brief entirely missing from goals (e.g., access controls dropped)
- Fewer than 3 goals (over-consolidated to meaninglessness)

## Example Output

# Goals

1. Establish a single trusted service catalog with clear ownership records per service.
2. Consolidate API documentation into one discoverable system with working search.
3. Make incident runbooks discoverable from the portal rather than scattered across repos.
4. Surface accurate service dependency information so teams understand cross-service impact.
5. Harden portal access controls so sensitive credentials are not visible to unauthorized roles.
6. Improve portal reliability so the application loads fast and its CI pipeline stays green.
