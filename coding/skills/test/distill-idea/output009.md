# Evaluation Criteria

## Requirements Tested
- 3.33: plan/<WI>/ artifacts deleted at WI close — no files survive
- Idea7: idea.md and status_idea.md are WI-scoped, not durable; deleted with the rest of plan/<WI>/

## Pass Criteria
- `plan/999_test-slug/idea.md` no longer exists after skill execution
- `plan/999_test-slug/status_idea.md` no longer exists after skill execution
- `plan/999_test-slug/` directory itself is removed (or empty and removed)
- No idea files moved or copied elsewhere — retirement means deletion, not relocation
- Skill confirms retirement action in its output text

## Fail Criteria
- `plan/999_test-slug/idea.md` still exists
- `plan/999_test-slug/status_idea.md` still exists
- Files moved to an archive or backup location instead of deleted
- Skill refuses to retire or skips deletion

## Filesystem Assertions
- NOT_EXISTS plan/999_test-slug/idea.md
- NOT_EXISTS plan/999_test-slug/status_idea.md
- NOT_EXISTS plan/999_test-slug/

## Example Output

Retired plan artifacts for WI #999 (test-slug):
- Deleted `plan/999_test-slug/idea.md`
- Deleted `plan/999_test-slug/status_idea.md`
- Removed `plan/999_test-slug/`
