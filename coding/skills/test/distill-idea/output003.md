# Evaluation Criteria

## Requirements Tested
- Idea1: Fewer than 3 goals means the brief is too narrow for goal-shaped framing — skill should refuse to produce a goal list

## Pass Criteria
- Output indicates the brief is too narrow for goal-shaped framing
- Status is `not_produced` or equivalent refusal
- Reason references the under-budget threshold (fewer than 3 distinct major goals)
- Skill does NOT produce a goal list from this input

## Fail Criteria
- Skill produces a goal list (even with 1–2 goals)
- Skill pads the output to reach 3 goals by inventing goals not present in the brief
- No explanation of why goals were not produced
- Skill treats the brief as valid input and runs full distillation

## Example Output

status: not_produced
reason: too narrow for goal-shaped framing — fewer than 3 distinct major goals identified
