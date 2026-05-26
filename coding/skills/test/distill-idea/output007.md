# Evaluation Criteria

## Requirements Tested
- Idea4: HITL only — agent proposes, human edits/accepts/rejects; no auto-acceptance, no AFK/Ralph loop

## Pass Criteria
- Agent proposed an initial goal list before accepting any HITL input
- Goal 2 in the final output matches the edited text ("Automate CI/CD pipeline wiring so developers never configure pipelines manually") — not the agent's original wording
- The original goal 4 (from the agent's first proposal) is absent from the final output
- Final goal count is between 3 and 6 (Idea1 still applies after edits)
- Agent did not auto-accept its own goals at any point — every goal in the final output was explicitly accepted via the HITL sequence
- No AFK/Ralph loop behavior visible in the output (Idea4)
- Agent presented the updated list after each edit/rejection before asking for the next decision

## Fail Criteria
- Agent produced a final goal list without proposing first and waiting for HITL input
- Goal 2 still has the agent's original wording (edit was ignored)
- Original goal 4 still present (rejection was ignored)
- Agent auto-accepted any goal without human confirmation
- Output shows signs of AFK/Ralph loop (batch processing without pausing for human)
- Agent skipped a round — e.g., went straight from initial proposal to final output without showing the intermediate edited list

## Example Output

## Goals

1. Scaffold standard directory structure for new microservices in the monorepo.
2. Automate CI/CD pipeline wiring so developers never configure pipelines manually.
3. Register new services in the internal service catalog at creation time.
4. Enforce naming conventions and prevent collisions with existing services.
