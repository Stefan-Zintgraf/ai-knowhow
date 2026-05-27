---
compiled-against: compile-skill v2.1.0
source: skills/input/phase-in.md
source-sha256: 109b0a1678fe12c05747c47494a4f962cb298660e4545f537914104c4dea6379
source-modified: 2026-05-26 21:00
compiled: 2026-05-26 21:00
---

# `/phase` — Phase Transition Orchestrator

This skill orchestrates phase transitions for a work item (WI) via three subcommands: `enter`, `exit`, and `status`. It is the **sole writer** of `plan/<WI>/phase_status.md` and `plan/ACTIVE`. No other skill or agent writes these files — phase skills call `/phase enter <code>` before starting their work and `/phase exit <code>` when done. The skill does not execute phase work, produce planning artifacts, decide workflow mode, or invoke other skills.

## Hard Rules

1. **Sole writer.** Only `/phase` writes `phase_status.md` and `plan/ACTIVE`. Phase skills never modify phase state directly.
2. **B-style state file.** `plan/<WI>/phase_status.md` has a mutable `Current` block at the top and a reverse-chronological `## History` section (newest on top).
3. **Current block schema.** Exactly these fields (YAML frontmatter in the `Current` block):
   - `wi` — work-item folder name (`<N>_<slug>`)
   - `issue` — GH issue number (`#NNN`)
   - `mode` — `direct-edit` | `mini` | `full`
   - `current_phase` — active phase code, or empty if between phases
   - `phase_status` — `in-progress` | `blocked` | `awaiting-hitl` | `exited`
   - `entered_at` — ISO timestamp of last `enter`
   - `blockers` — free-text or empty
   - `tripwire_halt` — `true` | `false`
   - `last_actor` — `human` | `agent`
   - `needs_research` — `true` | `false` (gate flag for optional `res`)
   - `pro_gate_tripped` — `true` | `false` (gate flag for optional `pro`)
4. **`next_phase` never persisted.** Always computed at read time from `mode` + `current_phase` + `phase_status` + flags. Writing it would cause drift.
5. **`plan/ACTIVE` always exists.** Single-line file: `<N>_<slug>` (active WI) or `<none>`. Never absent. Worktree-scoped if a worktree exists, else repo-global.
6. **Enter guards.** `/phase enter <code>` checks three conditions before allowing entry:
   - Mode-phase legality (see table below).
   - Previous phase exited (`phase_status` = `exited`, or first `enter` for the WI).
   - Tripwire-halt clear (`tripwire_halt` = `false`).
7. **Exit guards.** `/phase exit <code>` checks before allowing exit:
   - Phase-required artifacts present (see table below).
   - HITL ack recorded for HITL-only phases.
8. **Status is read-only.** `/phase status` never writes. It reads `plan/ACTIVE`, reads `phase_status.md`, computes `next_phase`, and reports.
9. **Tripwire blocks all entry.** When `tripwire_halt` is `true`, ALL `/phase enter` calls are refused. Human must resolve (approve narrow edit or re-triage). Resolution clears `tripwire_halt` and records the decision in history.
10. **History immutability.** Once a history entry is appended, it is never modified or deleted.
11. **No artifact production.** `/phase` writes only `phase_status.md` and `plan/ACTIVE` — no planning artifacts, no issues, no code.
12. **No skill invocation.** `/phase` does not call other skills; it is called by them.

## Steps

1. **Parse subcommand.** Accept one of: `enter <code>`, `exit <code>`, `status`. If unrecognized, return `status: error, reason: unknown subcommand "<input>"`.

2. **Resolve active WI.** Read `plan/ACTIVE`.
   - If `<none>` and subcommand is `status`: report "no active WI" and return `status: ok, wi: none`.
   - If `<none>` and subcommand is `enter` or `exit`: return `status: error, reason: no active WI — set plan/ACTIVE first`.
   - Otherwise: read `plan/<WI>/phase_status.md`. If the file is absent and the subcommand is `enter` (first phase of the WI), create it with a default Current block — populate `wi` and `issue` from `plan/ACTIVE` context, set `phase_status: exited` so the "previous exited" guard passes on first entry, set `tripwire_halt: false`, `needs_research: false`, `pro_gate_tripped: false`.

3. **Execute subcommand.**

   ### `enter <code>`

   a. **Mode-phase legality.** Look up the mode in the Mode-Phase Legality table. If `<code>` is not in the mode's legal phases, return `status: rejected, reason: phase <code> not valid for mode <mode>`.

   b. **Previous phase exited.** Check that `phase_status` = `exited` (or `current_phase` is empty, meaning first entry). If not, return `status: rejected, reason: previous phase <current_phase> not yet exited`.

   c. **Tripwire-halt clear.** If `tripwire_halt` = `true`, return `status: rejected, reason: tripwire halt active — resolve before entering any phase`.

   d. **Update Current block.** Set `current_phase: <code>`, `phase_status: in-progress`, `entered_at: <ISO timestamp>`, `last_actor: agent`.

   e. **Append history entry.** Add at the top of `## History`: `<timestamp> | enter | <code> | <mode>`.

   f. **Write** `phase_status.md`.

   g. **Return** `status: ok, entered: <code>`.

   ### `exit <code>`

   a. **Phase match.** Verify `current_phase` = `<code>`. If not, return `status: rejected, reason: current phase is <current_phase>, not <code>`.

   b. **Required artifacts.** Check the Phase-Required Artifacts table for `<code>`. If any required artifact is missing, return `status: rejected, reason: missing required artifact(s): <list>`.

   c. **HITL ack.** If the phase is HITL-only (per table), verify that explicit human acceptance was recorded during the phase. If not, return `status: rejected, reason: HITL ack not recorded for <code>`.

   d. **Update Current block.** Set `phase_status: exited`, `last_actor: agent`.

   e. **Append history entry.** Add at the top of `## History`: `<timestamp> | exit | <code> | <mode>`.

   f. **Write** `phase_status.md`.

   g. **Return** `status: ok, exited: <code>`.

   ### `status`

   a. **Read Current block** from `phase_status.md`.

   b. **Check tripwire halt.** If `tripwire_halt` = `true`:
      - Report the halt prominently: WI is blocked.
      - Surface the `blockers` field content.
      - Do NOT compute or report a normal `next_phase` — the WI cannot advance.
      - Present the two resolution options: (i) approve narrow edit with explicit reasoning recorded on GH issue, or (ii) re-triage mode via `/triage-idea --remode`.
      - Return `status: ok, halted: true`.

   c. **Compute `next_phase`** (only when `tripwire_halt` = `false`) using the Next-Phase Computation logic below.

   d. **Report** all Current block fields plus the computed `next_phase`.

   e. **Return** `status: ok`.

## Mode-Phase Legality

| Mode          | Legal phases (in order)                                     |
| ------------- | ----------------------------------------------------------- |
| `direct-edit` | `ide`, `ral`, `qa`                                          |
| `mini`        | `ide`, `aln`, `ral`, `qa`                                   |
| `full`        | `ide`, `aln`, `res`\*, `pro`\*, `prd`, `iss`, `ral`†, `qa` |

\* Optional — `res` is legal only when `needs_research` = `true`; `pro` is legal only when `pro_gate_tripped` = `true`.

† `par` is an alternative to `ral` (mutually exclusive); `par` is currently blocked (substrate TBD).

Cross-phase: `rev` and `ica` are legal alongside any sequential phase in any mode. They do not appear in the ordered sequence — they can be entered and exited independently.

## Phase-Required Artifacts for Exit

| Phase | Required artifacts                                                           | HITL-only? |
| ----- | ---------------------------------------------------------------------------- | ---------- |
| `ide` | `mini`/`full`: `plan/<WI>/idea.md` exists. `direct-edit`: GH issue exists.   | yes        |
| `aln` | `context.md` touched or ADR written                                          | yes        |
| `res` | Research file(s) written                                                     | no         |
| `pro` | Prototype variant presentation written; chosen direction recorded             | yes        |
| `prd` | PRD artifact exists                                                          | yes        |
| `iss` | At least one issue created from PRD                                           | no         |
| `ral` | All assigned issues resolved or explicitly deferred                           | no         |
| `par` | (same as `ral`)                                                              | no         |
| `qa`  | QA notes written; human verdict recorded                                      | yes        |
| `rev` | Review output written                                                        | yes        |
| `ica` | Arch-review output written                                                   | no         |

## Next-Phase Computation

Given `mode`, `current_phase` (with `phase_status: exited`), and the gate flags:

1. Look up the mode's legal-phase sequence from the Mode-Phase Legality table.
2. Find `current_phase` in the sequence.
3. The next entry in the sequence is `next_phase`.
4. If `current_phase` is the last in the sequence, `next_phase` = `done`.
5. Optional phases (`res`, `pro`) are skipped in the sequence unless their gate flag is `true`.
6. Special cases for `full` mode:
   - If `current_phase` = `aln` and `needs_research` = `true` → `next_phase` = `res`.
   - If `current_phase` = `aln` and `needs_research` = `false` and `pro_gate_tripped` = `true` → `next_phase` = `pro`.
   - If `current_phase` = `res` and `pro_gate_tripped` = `true` → `next_phase` = `pro`.
   - Otherwise follow the sequence order, skipping optional phases whose flags are `false`.

For cross-phase skills (`rev`, `ica`): they do not affect the sequential `next_phase` computation. They run alongside and have independent enter/exit cycles.

## Return

Each subcommand returns a structured signal:

**Success:**
- `enter`: `status: ok, entered: <code>`
- `exit`: `status: ok, exited: <code>`
- `status` (normal): `status: ok` + full Current block fields + computed `next_phase`
- `status` (tripwire active): `status: ok, halted: true` + blockers + resolution options (no `next_phase`)

**Rejection** (guard failed):
- `status: rejected, reason: <specific guard that failed>`

**Error** (bad input):
- `status: error, reason: <description>`
