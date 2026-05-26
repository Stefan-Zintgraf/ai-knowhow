# Evaluation Criteria

## Requirements Tested
- Idea7: Confirmed goal list persisted to `plan/<N>_<slug>/idea.md` with correct structure; companion `status_idea.md` written with correct frontmatter

## Pass Criteria
- Skill produces a goal list (3–6 goals per Idea1 — but this test focuses on persistence, not goal quality)
- `plan/999_test-slug/idea.md` exists after skill execution
- `plan/999_test-slug/idea.md` contains a `## Goals` section
- `plan/999_test-slug/status_idea.md` exists after skill execution
- `status_idea.md` frontmatter contains `status: wip`
- `status_idea.md` frontmatter contains `updated:` with today's date
- `status_idea.md` frontmatter contains `owner-issue: #999`
- No idea files written outside `plan/999_test-slug/`

## Fail Criteria
- `plan/999_test-slug/idea.md` missing after skill execution
- `plan/999_test-slug/status_idea.md` missing after skill execution
- `status_idea.md` has `status: done` (auto-flip forbidden — Idea7)
- `status_idea.md` missing `owner-issue` field
- Idea files written to any path other than `plan/999_test-slug/`
- `idea.md` missing `## Goals` section

## Filesystem Assertions
- EXISTS plan/999_test-slug/idea.md
- EXISTS plan/999_test-slug/status_idea.md
- CONTAINS plan/999_test-slug/idea.md ## Goals
- FRONTMATTER plan/999_test-slug/status_idea.md status wip
- FRONTMATTER plan/999_test-slug/status_idea.md updated <today>
- FRONTMATTER plan/999_test-slug/status_idea.md owner-issue #999
- NOT_EXISTS plan/idea.md

## Example Output

## Goals

1. Give teams real-time visibility into which AI agents are active and what they're working on.
2. Prevent duplicated agent work by surfacing current task assignments.
3. Surface cost data per session to catch runaway spending early.
4. Keep operational overhead low — polling over streaming, minimal maintenance.
