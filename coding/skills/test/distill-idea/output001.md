# Evaluation Criteria

## Requirements Tested
- Idea1: Output must contain between 3 and 6 major goals
- Idea2: Implementation details (component names, endpoints, DB tables, timelines) must be stripped from goals and noted as deferred
- Idea3: Negative goals (explicit non-goals) are first-class and count toward the 3–6 budget

## Pass Criteria
- Output contains a `## Goals` section
- Goal count is between 3 and 6 (inclusive)
- At least one goal is a negative goal / non-goal (mobile push notifications out of scope)
- No implementation details appear in goals: no `<NotificationDrawer>`, no `/api/v2/events`, no `user_notification_state`, no "two sprints"
- Stripped details are listed separately (deferred to aln/prd)
- Goals cover: reliable event surfacing, triage/prioritization, durable handled-state, and the mobile-push non-goal

## Fail Criteria
- Implementation details (component names, endpoints, table names, timelines) leak into goal text
- Non-goal is omitted or not recognized as a goal
- Stripped details are silently dropped without noting them
- Goal count outside 3–6 range

## Example Output

# Goals

1. Surface account-critical events reliably so users notice them in time to act.
2. Enable at-a-glance triage so users can distinguish noise from events needing response.
3. Persist per-user handled-state durably so resolved notifications do not re-nag across devices.
4. Non-goal: Deliver mobile push notifications — owned by the mobile team on a separate track.

Stripped detail: base on existing React <NotificationDrawer> component — deferred to aln/prd
Stripped detail: wire to /api/v2/events endpoint — deferred to aln/prd
Stripped detail: persist read-state in Postgres user_notification_state table — deferred to aln/prd
Stripped detail: ship in roughly two sprints — deferred to aln/prd
