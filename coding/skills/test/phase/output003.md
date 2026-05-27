# Evaluation Criteria

## Requirements Tested
- PTM4 (coding_plan.md §PTM): next_phase computed at read time from mode + current_phase + flags — not a stored field
- PTM9 (coding_plan.md §PTM / phases.md §5): status is read-only
- PH4.2 (phases.md §4): needs_research=true triggers optional res phase next
- PH4.3 (phases.md §4): pro_gate_tripped=false means pro not next

## Pass Criteria
- Skill computes and reports `next_phase = res`
- Reports `current_phase: aln`, `phase_status: exited`
- `pro` NOT listed as next phase
- No file written

## Fail Criteria
- Skill computes `next_phase = prd` (ignoring needs_research=true)
- Skill reads a persisted `next_phase` field from file rather than computing it
- Any file written

## Example Output

WI: 12_payment-gateway (mode: full)
Current phase: aln (exited)
next_phase: res  ← needs_research=true
pro_gate_tripped: false — pro not in chain

Run `/phase enter res` to proceed.
