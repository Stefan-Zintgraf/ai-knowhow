# Authoring Prompt: `phase` Skill (A12)

## Metadata

```yaml
skill_id: A12
skill_name: phase
phase: none
status: todo
workflow_ref: W15a
depends_on: []
feeds_into: [A1-align-concept, A2-compose-prd, A3-prd-to-dag, A4-afk-loop, A5-parallel-loop, A6-review, A7-arch-review, A8-qa, A9-prototype, A10-do-research, A11-distill-idea, A13-triage-idea]
```

---

## Scope

The skill does **one** thing: orchestrate phase transitions by managing `phase_status.md` and `plan/ACTIVE` via three subcommands (`enter`, `exit`, `status`).

The skill does **not**:

- Execute any phase work (distillation, grilling, coding, review, QA, etc.).
- Create or modify planning artifacts other than `phase_status.md` and `plan/ACTIVE`.
- Decide which workflow mode to use — that's `/triage-idea`'s job; `/phase` enforces mode-phase legality after the decision is made.
- Invoke other skills — it is called *by* phase skills, not the caller of them.

Phase skills call `/phase enter <code>` before starting and `/phase exit <code>` when done. The caller owns workflow sequencing; `/phase` owns state consistency.

**Phase token exception**: Unlike regular phase skills, `/phase` legitimately references all phase codes as domain objects. Phase codes are this skill's core lookup data — they appear in subcommand arguments, legality tables, and next-phase computation. The "no phase tokens in body" constraint that applies to other skills does NOT apply here.

---

## Self-Containment Mandate

The output skill must run **without** `coding_plan.md`, `phases.md`, `guardrails.md`, or `gr/gr_idea.md` in context or on disk. Every rule the skill needs at runtime must be **inlined** — including the phase chain definitions, mode-phase legality tables, Current block schema, artifact-presence checks, and next-phase computation logic. No links to source docs. No "see X" references. The skill is a leaf artifact.

Source docs below are author-time scaffolding only — read them, distill them, embed the distilled content into the skill.

---

## Source Documents (author-time only)

| File               | Relevant sections                                                                 |
| ------------------ | --------------------------------------------------------------------------------- |
| `coding_plan.md`   | §"Phase Transition Mechanism" (lines 122–215): PTM spec, Current block schema, plan/ACTIVE contract, enforcement chain |
| `coding_plan.md`   | §A12 detail block (lines 666–672): subcommand behavior summary                   |
| `phases.md`        | §4 Phase Sequence: phase chains per mode, optional phase gates                    |
| `phases.md`        | §5 Phase–Skill Binding: transition protocol table, ide call sequence by mode      |
| `guardrails.md`    | §3.37 Tripwire Discovery Forces Halt: halt + re-triage enforcement                |
| `gr/gr_idea.md`    | Idea8 (mode definitions), Idea11 (mode transitions) — context for legality table, no rules annotated `Skills: phase` |

Note: `gr/gr_idea.md` rules are annotated for `distill-idea` and `triage-idea`, not `phase` — consumed here only to build the mode-phase legality table. `phases.md` §4.x routing entries and `guardrails.md` §3.29 collapse-mode are excluded — mode selection is `/triage-idea`'s concern. D10 (status_idea.md migration into phase_status.md) is still open — tentative decision is "fold"; the Current block schema below follows the tentative answer.

---

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. **Sole writer of `phase_status.md` and `plan/ACTIVE`.** No other skill writes these files. Phase skills call `/phase enter` and `/phase exit` — they never modify phase state directly.

2. **State file: `plan/<WI>/phase_status.md`, B-style.** Mutable `Current` block at the top + reverse-chronological `## History` section (newest entry on top). Current block = single source of truth for live phase state; history entries are immutable once appended.

3. **Current block schema.** Exactly these fields:
   - `wi` — work-item folder name (`<N>_<slug>`)
   - `issue` — GH issue number (`#NNN`)
   - `mode` — `direct-edit` | `mini` | `full`
   - `current_phase` — phase code currently active (or empty if between phases)
   - `phase_status` — `in-progress` | `blocked` | `awaiting-hitl` | `exited`
   - `entered_at` — ISO timestamp of last `enter`
   - `blockers` — free-text or empty
   - `tripwire_halt` — `true` | `false`
   - `last_actor` — `human` | `agent`
   - `needs_research` — `true` | `false` (gate flag for optional `res` phase)
   - `pro_gate_tripped` — `true` | `false` (gate flag for optional `pro` phase)

4. **`next_phase` is computed, never stored.** Derived at read time by `/phase status` from `mode` + `current_phase` + `phase_status` + flags against the inlined phase chain definitions. Writing it would cause drift.

5. **`plan/ACTIVE` pointer.** Single-line file containing `<N>_<slug>` (active WI) or literal `<none>`. Must always exist — never absent. Worktree-scoped if a worktree exists, else repo-global.

6. **Enter guards.** `/phase enter <code>` checks three conditions:
   - **Mode-phase legality** — phase code must be valid for current mode (inlined legality table).
   - **Previous phase exited** — `phase_status` must be `exited` (or this is the WI's first `enter`).
   - **Tripwire-halt clear** — `tripwire_halt` must be `false`.
   On pass: update Current block, append history entry.

7. **Exit guards.** `/phase exit <code>` checks:
   - **Phase-required artifacts present** — per the inlined artifact table.
   - **HITL ack recorded** — for HITL-only phases, explicit human acceptance must have been recorded.
   On pass: update Current block (`phase_status: exited`), append history entry.

8. **Status is read-only.** `/phase status` reads `plan/ACTIVE` → reads `phase_status.md` → computes `next_phase` → reports. No writes. If `plan/ACTIVE` = `<none>`, report "no active WI."

9. **Tripwire halt blocks all entry.** When `tripwire_halt: true`, `/phase enter` refuses all transitions. Human must resolve (approve narrow edit or re-triage). Resolution clears `tripwire_halt` and records the decision in history.

10. **History entries immutable.** Once appended, never modified or deleted. History is the audit trail.

---

## Skill Behaviors

In order:

1. **Parse subcommand.** Accept: `enter <code>`, `exit <code>`, `status`. Unrecognized → return `status: error, reason: unknown subcommand "<input>"`.

2. **Resolve active WI.** Read `plan/ACTIVE`.
   - If `<none>` + subcommand `status` → report "no active WI" and return `status: ok, wi: none`.
   - If `<none>` + subcommand `enter` or `exit` → return `status: error, reason: no active WI — set plan/ACTIVE first`.
   - Otherwise → read `plan/<WI>/phase_status.md`. If absent and subcommand is `enter` (first phase of WI), create with default Current block (fields populated from `plan/ACTIVE` + the `enter` arguments; `phase_status: exited` initially so the enter-guard "previous exited" check passes).

3. **Branch on subcommand.**

   **`enter <code>`:**
   - Check mode-phase legality. If illegal → `status: rejected, reason: phase <code> not valid for mode <mode>`.
   - Check previous phase exited (or first entry). If not → `status: rejected, reason: previous phase <current> not yet exited`.
   - Check `tripwire_halt` = `false`. If `true` → `status: rejected, reason: tripwire halt active — resolve before entering any phase`.
   - Update Current block: `current_phase: <code>`, `phase_status: in-progress`, `entered_at: <now>`, `last_actor: agent`.
   - Append history entry: `<timestamp> | enter | <code> | <mode>`.
   - Return `status: ok, entered: <code>`.

   **`exit <code>`:**
   - Verify `current_phase` matches `<code>`. If not → `status: rejected, reason: current phase is <current>, not <code>`.
   - Check phase-required artifacts (inlined table). If missing → `status: rejected, reason: missing required artifact(s): <list>`.
   - Check HITL ack for HITL-only phases. If not recorded → `status: rejected, reason: HITL ack not recorded for <code>`.
   - Update Current block: `phase_status: exited`, `last_actor: agent`.
   - Append history entry: `<timestamp> | exit | <code> | <mode>`.
   - Return `status: ok, exited: <code>`.

   **`status`:**
   - Read Current block.
   - Compute `next_phase` from mode + current_phase + phase_status + flags.
   - Report all Current block fields plus computed `next_phase`.
   - Return `status: ok`.

4. **Write state file.** For `enter` and `exit`: rewrite Current block in-place; append history entry at top of `## History` section.

---

## Inlined Reference Tables (must appear in output skill)

### Mode-Phase Legality

| Mode          | Legal phases (in order)                                     |
| ------------- | ----------------------------------------------------------- |
| `direct-edit` | `ide`, `ral`, `qa`                                          |
| `mini`        | `ide`, `aln`, `ral`, `qa`                                   |
| `full`        | `ide`, `aln`, `res`*, `pro`*, `prd`, `iss`, `ral`†, `qa`   |

* Optional — `res` legal only when `needs_research` flag set; `pro` legal only when `pro_gate_tripped` flag set.
† `par` is an alternative to `ral` (mutually exclusive); `par` currently blocked (substrate TBD).

Cross-phase: `rev` and `ica` legal alongside any sequential phase in any mode.

### Phase-Required Artifacts for Exit

| Phase | Required artifacts for exit                                                  | HITL-only? |
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

### Next-Phase Computation

Given `mode`, `current_phase` (with `phase_status: exited`), and flags:

1. Look up mode's legal-phase sequence.
2. Find `current_phase` in the sequence.
3. Next entry = `next_phase`.
4. If `current_phase` is last in sequence → `next_phase: done`.
5. Optional phases (`res`, `pro`) are skipped unless their gate flag is set.
6. If `current_phase` = `aln` and `needs_research` set → `next_phase: res`. If `current_phase` = `aln` or `res`, and `pro_gate_tripped` set → `next_phase: pro`.

---

## Constraints (must appear as Hard Rules inside the skill)

- **Sole writer**: no other skill writes `phase_status.md` or `plan/ACTIVE`.
- **Mode-phase validation**: every `enter` checks legality table; illegal transitions rejected, never silently allowed.
- **Tripwire blocks all**: `tripwire_halt: true` blocks ALL `enter` calls.
- **History immutability**: history entries are append-only.
- **next_phase never persisted**: always computed at read time.
- **plan/ACTIVE always exists**: contains `<N>_<slug>` or `<none>`, never absent.
- **HITL phases enforce ack**: exit from HITL-only phases requires recorded human acceptance.
- **No artifact production**: `/phase` writes only `phase_status.md` and `plan/ACTIVE`.
- **No skill invocation**: `/phase` does not call other skills; it is called by them.

---

## Output Format (for the generated skill)

The output skill (`skills/output/phase.md`) must be a Claude Code SKILL.md — a single self-contained markdown prompt file that:

- Opens with a one-paragraph role statement: this skill orchestrates phase transitions via three subcommands (`enter`, `exit`, `status`) and is the sole writer of `phase_status.md` and `plan/ACTIVE`.
- Contains an inlined **Hard Rules** block (Rules + Constraints above, brief imperative form). No "see doc §X" references.
- Has an ordered **Steps** section mapping to Behaviors above.
- Inlines the three reference tables (mode-phase legality, phase-required artifacts, next-phase computation) verbatim — core lookup data.
- Has a **Return** section specifying success/failure signal shape per subcommand.
- Does **not** link to `coding_plan.md`, `phases.md`, `guardrails.md`, or `gr/gr_idea.md`.
- Phase codes appear throughout as domain objects — this is the orchestrator, not a phase-coupled skill.
- Passes the test: if the skill file were the only file in the repo, an agent reading it could still execute correctly.

---

**Open question (D10):** `status_idea.md` migration. Tentative: fold into `phase_status.md` Current block. If resolved differently, the Current block schema (Rule 3) needs revision. Current draft follows the tentative "fold" answer.
