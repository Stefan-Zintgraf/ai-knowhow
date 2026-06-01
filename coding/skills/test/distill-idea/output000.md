# Evaluation Criteria

## Requirements Tested
- Idea1: Output must contain between 3 and 6 major goals
- Idea2: Goals must not contain module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or estimates
- Idea5: Brief is distilled into a goal list — not echoed verbatim
- Idea6: Output is a goal list that feeds `aln` grilling — not a PRD, not a design, not a substitute for alignment
- Idea7: Output structure matches `idea.md` template shape (## Goals section; no extraneous sections for a formed brief)
- 3.32: Brief distilled into 3–6 goals per the core rule mirror of Idea1–Idea7

## Pass Criteria
- Output contains a `## Goals` section (no `## Context` section — input is a formed brief, not sub-brief)
- Goal count is between 3 and 6 (inclusive)
- Each goal names an intent the work must serve, not an implementation approach
- Goals collectively cover: workflow definition, guardrails, enforcement/operationalization, proportionality, and collapse/shortcut for small tasks
- No module names, file paths, API shapes, UX specifics, or tech choices appear in goals
- Output is goal-level only — no user stories, acceptance criteria, module maps, or implementation decisions (Idea6)
- Output structure is compatible with `idea.md` template: `## Goals` section with numbered list (Idea7)

## Fail Criteria
- Fewer than 3 or more than 6 goals
- Any goal contains implementation detail (component names, endpoints, libraries, timelines)
- Output echoes the brief verbatim instead of distilling it
- Output contains a `## Context` section (Idea12 sharpening should be skipped for a well-formed brief)
- Goals are too vague to anchor an `aln` grilling session
- Output contains PRD-level content: user stories, acceptance criteria, module maps, implementation decisions (Idea6 violation)
- Output structure incompatible with `idea.md` template (missing `## Goals` heading, unnumbered list, extraneous sections)

## Example Output

# Goals

1. Define end-to-end AI coding workflow covering greenfield and brownfield work.
2. Establish guardrails protecting system intent without bloating always-on agent context.
3. Operationalize workflow and guardrails as enforceable agent behavior, not prose-only docs.
4. Keep planning effort proportionate so workflow reaches real code quickly.
5. Provide shortcuts for small coding tasks so full pipeline collapses appropriately rather than being skipped silently.
