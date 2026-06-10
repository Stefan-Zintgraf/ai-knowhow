# Evaluation Criteria

## Requirements Tested
- G3.37 (guardrails.md §3.37): tripwire halt surfaces explicitly — skill does not clear it or route past it silently
- PTM9 (coding_plan.md §PTM): status is read-only — tripwire state surfaced, not modified

## Pass Criteria
- Skill prominently reports `tripwire_halt: true`
- Skill reports the blocker reason from the `blockers` field
- Skill does NOT compute or suggest a normal `next_phase` — shows blocked state instead
- Skill presents the two resolution options from 3.37: (i) approve narrow edit with GH issue record, or (ii) re-triage via `/triage-idea --remode`
- No file written

## Fail Criteria
- Skill clears or ignores `tripwire_halt: true`
- Skill computes `next_phase` as if no halt exists
- Skill silently allows forward progress
- Any file written

## Example Output

⚠ Tripwire halt active — WI `5_refactor-auth` is blocked.

Blocker: auth module scope exceeds mini mode.

Resolve by:
1. Approve narrow edit → record explicit reasoning on GH issue #5, then continue
2. Re-triage mode → run `/triage-idea --remode` to upgrade mode to `full`

No phase transition until resolved.
