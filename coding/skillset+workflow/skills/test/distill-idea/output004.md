# Evaluation Criteria

## Requirements Tested
- Idea12: When input is a vague notion (no clear problem statement, no identifiable user, no articulated value), run concept sharpening before goal distillation
- Idea12: Sharpening produces five fields: Problem, Target user, Core value, Key assumptions, Open questions
- Idea12: Context section persisted at top of idea.md, above goals — no separate file
- Idea1: Goals section still contains 3–6 major goals
- Idea2: No implementation details in either Context or Goals sections

## Pass Criteria
- Output contains a `## Context` section with all five fields: Problem, Target user, Core value, Key assumptions, Open questions
- Output contains a `## Goals` section below Context
- Goal count is between 3 and 6
- Context fields name what/why, not how (Idea2 applies to Idea12 output)
- No implementation details in any field (no specific tools, libraries, architectures)
- Context section appears before Goals section

## Fail Criteria
- Missing `## Context` section (Idea12 skipped on sub-brief input)
- Any of the five Context fields missing
- Implementation details leak into Context or Goals (e.g., specific wiki software, tech stack)
- Goal count outside 3–6 range
- Context and Goals in wrong order (Goals before Context)
- "Smallest useful version," market research, or feature lists appear in Context fields

## Example Output

## Context

**Problem:** New hires report excessive time-to-productivity; existing onboarding wiki is disorganized and hard to navigate.
**Target user:** New engineering hires in their first two weeks.
**Core value:** Reduce ramp-up time so new hires contribute meaningfully sooner.
**Key assumptions:** The wiki content itself is mostly correct but poorly structured; the bottleneck is findability and sequencing, not missing knowledge.
**Open questions:** Is the problem uniform across teams or worse for specific roles? Are there existing onboarding checklists that partially work?

## Goals

1. Provide a structured onboarding path that guides new hires through setup and essential context in a clear sequence.
2. Reorganize or replace the onboarding wiki so critical information is findable without tribal knowledge.
3. Give new hires a way to track their own onboarding progress and know what remains.
