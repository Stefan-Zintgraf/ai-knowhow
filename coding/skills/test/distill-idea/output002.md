# Evaluation Criteria

## Requirements Tested
- 3.29: When upstream artifact already names goals explicitly, collapse to one-line confirmation instead of full distillation pass
- Idea1: Confirmed goals must still be 3–6 major goals
- Idea2: Confirmed goals must still be detail-free

## Pass Criteria
- Skill detects input is already goal-shaped and collapses (does not re-distill from scratch)
- Output confirms the goals with minimal or no transformation
- Goal count remains between 3 and 6
- No implementation details present in confirmed goals
- Output preserves the substance of all input goals

## Fail Criteria
- Skill runs full distillation on already-shaped goals (ignores 3.29 collapse)
- Skill rejects the input or asks for a "raw brief"
- Goals are substantially altered beyond minor phrasing adjustments
- Goal count changes to outside 3–6 range
- Implementation details are introduced that weren't in the input

## Example Output

# Goals

1. Replace the current session-token storage approach with one that meets the new compliance requirements.
2. Keep existing user sessions valid across the cutover so no one gets force-logged-out.
3. Make the new storage layer observable enough that we can detect token-handling regressions before users do.
4. Leave room for a future second auth factor without committing to a specific mechanism now.
