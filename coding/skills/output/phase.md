---
compiled-against: compile-skill v2.1.0
source: skills/input/phase-in.md
source-sha256: 045c53f9ef8e49be673a8519ddfd18056571f1784611aa1c3994b625b5b66a56
source-modified: 2026-05-27 11:53
compiled: 2026-05-27 11:58
---

# `/phase` — Phase Transition Orchestrator

This skill orchestrates phase transitions for a work item (WI) via four subcommands: `enter`, `exit`, `status`, and `resolve-tripwire`. It is the **sole writer** of `<artifacts>/<WI>/phase_status.md` and `<artifacts>/ACTIVE` (`<artifacts>` is an optional parameter defaulting to `plan`). No other skill or agent writes these files — phase skills call `/phase enter <code>` before starting their work and `/phase exit <code>` when done. The skill does not execute phase work, produce planning artifacts, decide workflow mode, or invoke other skills.

## Hard Rules

1. **Sole writer.** Only `/phase` writes `phase_status.md` and `<artifacts>/ACTIVE`. Phase skills never modify phase state directly.
2. **B-style state file.** `<artifacts>/<WI>/phase_status.md` has a mutable `Current` block at the top and a reverse-chronological `## History` section (newest on top).
3. **Current block schema.** Exactly these fields:
   - `wi` — work-item folder name (`<N>_<slug>`)
   - `issue` — GH issue number (`#NNN`)
   - `mode` — `direct-edit` | `mini` | `full`
   - `current_phase` — active phase code, or empty if between phases
   - `phase_status` — `in-progress` | `blocked` | `awaiting-hitl` | `exited`
   - `entered_at` — ISO timestamp of last `enter`
   - `blockers` — free-text or empty
   - `tripwire_halt` — `true` | `false`
   - `last_actor` — `human` | `agent`
   - `needs_research` — `true` | `false` (gate flag for optional `res` phase)
   - `pro_gate_tripped` — `true` | `false` (gate flag for optional `pro` phase)
4. **`next_phase` never persisted.** Always computed at read time from `mode` + `current_phase` + `phase_status` + flags. Writing it would cause drift.
5. **`<artifacts>/ACTIVE` always exists.** Single-line file: `<N>_<slug>` (active WI) or literal `<none>`. Never absent. Worktree-scoped if a worktree exists, else repo-global.
6. **`<artifacts>` parameter.** Accepted as optional input; defaults to `plan`; passed through to all file operations without exception.
7. **Enter guards.** `/phase enter <code>` checks three conditions before allowing entry:
   - Mode-phase legality (see table below).
   - Previous phase exited (`phase_status` = `exited`, or first `enter` for the WI).
   - Tripwire-halt clear (`tripwire_halt` = `false`).
8. **Exit guards.** `/phase exit <code>` checks before allowing exit:
   - Phase-required artifacts present (see table below).
   - HITL ack recorded for HITL-only phases.
9. **Status is read-only.** `/phase status` never writes. It reads `<artifacts>/ACTIVE`, reads `phase_status.md`, computes `next_phase`, and reports.
10. **Tripwire blocks all entry; only `resolve-tripwire` clears it.** When `tripwire_halt` is `true`, ALL `/phase enter` calls are refused. Human must call `/phase resolve-tripwire <reason>` — supplying the explicit decision (approve narrow edit or re-triage rationale). Resolution sets `tripwire_halt: false`, appends the decision to history, and updates the GH issue body.
11. **History immutability.** Once a history entry is appended, it is never modified or deleted.
12. **No artifact production.** `/phase` writes only `phase_status.md` and `<artifacts>/ACTIVE` — no planning artifacts, no issues, no code.
13. **No skill invocation.** `/phase` does not call other skills; it is called by them.

## Steps

1. **Parse subcommand.** Accept one of: `enter <code>`, `exit <code>`, `status`, `resolve-tripwire <reason>`. If unrecognized, return `status: error, reason: unknown subcommand "<input>"`.

2. **Resolve active WI.** Read `<artifacts>/ACTIVE`.
   - If `<none>` and subcommand is `status`: report "no active WI" and return `status: ok, wi: none`.
   - If `<none>` and subcommand is `enter`, `exit`, or `resolve-tripwire`: return `status: error, reason: no active WI — set <artifacts>/ACTIVE first`.
   - Otherwise: read `<artifacts>/<WI>/phase_status.md`. If the file is absent and the subcommand is `enter` (first phase of the WI), create it with a default Current block — populate `wi` and `issue` from `<artifacts>/ACTIVE` context, set `phase_status: exited` so the "previous exited" guard passes on first entry, set `tripwire_halt: false`, `needs_research: false`, `pro_gate_tripped: false`.

3. **Execute subcommand.**

   ### `enter <code>`

   a. **Mode-phase legality.** Look up the mode in the Mode-Phase Legality table. If `<code>` is not in the mode's legal phases, return `status: rejected, reason: phase <code> not valid for mode <mode>`.

   b. **Previous phase exited.** Check that `phase_status` = `exited` (or `current_phase` is empty, meaning first entry). If not, return `status: rejected, reason: previous phase <current_phase> not yet exited`.

   c. **Tripwire-halt clear.** If `tripwire_halt` = `true`, return `status: rejected, reason: tripwire halt active — call /phase resolve-tripwire <reason> to clear`.

   d. **Update Current block.** Set `current_phase: <code>`, `phase_status: in-progress`, `entered_at: <ISO timestamp>`, `last_actor: agent`.

   e. **Append history entry.** Add at the top of `## History`: `<timestamp> | enter | <code> | <mode>`.

   f. **Write** `<artifacts>/<WI>/phase_status.md`.

   g. **Return** `status: ok, entered: <code>`.

   ### `exit <code>`

   a. **Phase match.** Verify `current_phase` = `<code>`. If not, return `status: rejected, reason: current phase is <current_phase>, not <code>`.

   b. **Required artifacts.** Check the Phase-Required Artifacts table for `<code>`. If any required artifact is missing, return `status: rejected, reason: missing required artifact(s): <list>`.

   c. **HITL ack.** If the phase is HITL-only (per table), verify that explicit human acceptance was recorded during the phase. If not, return `status: rejected, reason: HITL ack not recorded for <code>`.

   d. **Update Current block.** Set `phase_status: exited`, `last_actor: agent`.

   e. **Append history entry.** Add at the top of `## History`: `<timestamp> | exit | <code> | <mode>`.

   f. **Write** `<artifacts>/<WI>/phase_status.md`.

   g. **Return** `status: ok, exited: <code>`.

   ### `status`

   a. **Read Current block** from `<artifacts>/<WI>/phase_status.md`.

   b. **Check tripwire halt.** If `tripwire_halt` = `true`:
      - Report the halt prominently: WI is blocked.
      - Surface the `blockers` field content.
      - Do NOT compute or report a normal `next_phase` — the WI cannot advance.
      - Present the two resolution options: (i) approve narrow edit with explicit reasoning recorded on GH issue, or (ii) re-triage mode via `/triage-idea --remode`.
      - Return `status: ok, halted: true`.

   c. **Compute `next_phase`** (only when `tripwire_halt` = `false`) using the Next-Phase Computation logic below.

   d. **Report** all Current block fields plus the computed `next_phase`.

   e. **Return** `status: ok`.

   ### `resolve-tripwire <reason>`

   a. **Require non-empty reason.** If `<reason>` is empty, return `status: rejected, reason: reason required — record the human's decision (approve narrow edit or re-triage rationale)`.

   b. **Verify tripwire active.** If `tripwire_halt` = `false`, return `status: rejected, reason: tripwire_halt is already false`.

   c. **Update Current block.** Set `tripwire_halt: false`, `last_actor: human`.

   d. **Append history entry.** Add at the top of `## History`: `<timestamp> | resolve-tripwire | reason: <reason>`.

   e. **Update GH issue body.** Append `Tripwire halt resolved: <reason>` via `gh issue edit --body-file` or `gh issue comment`.

   f. **Write** `<artifacts>/<WI>/phase_status.md`.

   g. **Return** `status: ok, tripwire_resolved: true`.

4. **Write state file.** For `enter`, `exit`, and `resolve-tripwire`: rewrite the Current block in-place; append history entry at the top of `## History`. For `status`: no writes.

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

| Phase | Required artifacts                                                                    | HITL-only? |
| ----- | ------------------------------------------------------------------------------------- | ---------- |
| `ide` | `mini`/`full`: `<artifacts>/<WI>/idea.md` exists. `direct-edit`: GH issue exists.    | yes        |
| `aln` | `context.md` touched or ADR written                                                   | yes        |
| `res` | Research file(s) written                                                              | no         |
| `pro` | Prototype variant presentation written; chosen direction recorded                      | yes        |
| `prd` | PRD artifact exists                                                                   | yes        |
| `iss` | At least one issue created from PRD                                                    | no         |
| `ral` | All assigned issues resolved or explicitly deferred                                    | no         |
| `par` | (same as `ral`)                                                                       | no         |
| `qa`  | QA notes written; human verdict recorded                                               | yes        |
| `rev` | Review output written                                                                 | yes        |
| `ica` | Arch-review output written                                                            | no         |

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
- `resolve-tripwire`: `status: ok, tripwire_resolved: true`

**Rejection** (guard failed):
- `status: rejected, reason: <specific guard that failed>`

**Error** (bad input or state):
- `status: error, reason: <description>`
