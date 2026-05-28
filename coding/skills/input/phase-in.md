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

The skill does **one** thing: orchestrate phase transitions by managing `<artifacts>/<WI>/phase_status.md` and `<artifacts>/ACTIVE` via five subcommands (`enter`, `exit`, `status`, `resolve-tripwire`, `close`).

`<artifacts>` is an optional input parameter, defaulting to `plan`. The skill accepts it and passes it through to all file operations.

The skill does **not**:

- Execute any phase work (distillation, grilling, coding, review, QA, etc.).
- Create or modify planning artifacts other than `phase_status.md` and `<artifacts>/ACTIVE`.
- Decide which workflow mode to use — that's `/triage-idea`'s job; `/phase` enforces mode-phase legality after the decision is made.
- Invoke other skills — it is called *by* phase skills, not the caller of them.

Phase skills call `/phase enter <code>` before starting and `/phase exit <code>` when done. The caller owns workflow sequencing; `/phase` owns state consistency.

**Phase token exception**: Unlike regular phase skills, `/phase` legitimately references all phase codes as domain objects. Phase codes are this skill's core lookup data — they appear in subcommand arguments, legality tables, and next-phase computation. The "no phase tokens in body" constraint that applies to other skills does NOT apply here.

---

## Self-Containment Mandate

The output skill must run **without** `coding_plan.md`, `phases.md`, `guardrails.md`, or `gr/gr_idea.md` in context or on disk. Every rule the skill needs at runtime must be **inlined** — including the phase chain definitions, mode-phase legality tables, Current block schema, artifact-presence checks, and next-phase computation logic. No links to source docs. No "see X" references. The skill is a leaf artifact.

Source docs below are author-time scaffolding only — read them, distill them, embed the distilled content into the skill.

---

## Artifact Pattern (non-standard)

`/phase` is an artifact-producing skill, but its artifact (`phase_status.md`) follows a **custom B-style schema**, not the standard Idea7 `status: open|wip|done` / `updated` / `owner-issue` frontmatter pattern.

- **Artifact:** `<artifacts>/<WI>/phase_status.md` — mutable Current block + reverse-chronological History.
- **No companion `status_phase_status.md`**: the Current block's `phase_status` field IS the state machine; a separate status file would be redundant.
- **No `owner-issue` field on `phase_status.md`**: it is infrastructure, not a WI artifact subject to Q11 retirement lint. Deleted with `<artifacts>/<WI>/` at WI close (same deletion event as `idea.md`, `algn_transcript.md`), but retirement trigger is WI close, not owner-issue close.
- **`<artifacts>/ACTIVE`**: a single-line pointer file — always present, written by `/phase` on issue-emit (Idea9), cleared to `<none>` at WI close.

The standard Step 5 template rules (Idea7-style status file, `owner-issue` prompt at write-time, auto-wip/human-done flip) do **not** apply. The Current block schema in Rule 3 is the authoritative spec.

---

## Source Documents (author-time only)

| File               | Relevant sections                                                                 |
| ------------------ | --------------------------------------------------------------------------------- |
| `coding_plan.md`   | §"Phase Transition Mechanism" (lines 122–215): PTM spec, Current block schema, `<artifacts>/ACTIVE` contract, enforcement chain |
| `coding_plan.md`   | §A12 detail block: subcommand behavior summary                                    |
| `phases.md`        | §4 Phase Sequence: phase chains per mode, optional phase gates                    |
| `phases.md`        | §5 Phase–Skill Binding: transition protocol table, ide call sequence by mode      |
| `guardrails.md`    | §3.37 Tripwire Discovery Forces Halt: halt + re-triage enforcement                |
| `gr/gr_idea.md`    | Idea8 (mode definitions), Idea11 (mode transitions) — context for legality table, no rules annotated `Skills: phase` |

Note: `gr/gr_idea.md` rules are annotated for `distill-idea` and `triage-idea`, not `phase` — consumed here only to build the mode-phase legality table. `phases.md` §4.x routing entries and `guardrails.md` §3.29 collapse-mode are excluded — mode selection is `/triage-idea`'s concern. D10 (`status_idea.md` migration into `phase_status.md`) is still open — tentative decision is "fold"; the Current block schema below follows the tentative answer.

---

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. **Sole writer of `phase_status.md` and `<artifacts>/ACTIVE`.** No other skill writes these files. Phase skills call `/phase enter` and `/phase exit` — they never modify phase state directly.

2. **State file: `<artifacts>/<WI>/phase_status.md`, B-style.** Mutable `Current` block at the top + reverse-chronological `## History` section (newest entry on top). Current block = single source of truth for live phase state; history entries are immutable once appended.

3. **Current block schema.** Exactly these fields:
   - `wi` — work-item folder name (`<N>_<slug>`)
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

5. **`<artifacts>/ACTIVE` pointer.** Single-line file containing `<N>_<slug>` (active WI) or literal `<none>`. Must always exist — never absent. Worktree-scoped if a worktree exists, else repo-global. `<artifacts>` defaults to `plan`.

6. **Enter guards.** `/phase enter <code>` checks three conditions:
   - **Mode-phase legality** — phase code must be valid for current mode (inlined legality table).
   - **Previous phase exited** — `phase_status` must be `exited` (or this is the WI's first `enter`).
   - **Tripwire-halt clear** — `tripwire_halt` must be `false`.
   On pass: update Current block, append history entry.

7. **Exit guards.** `/phase exit <code>` checks:
   - **Phase-required artifacts present** — per the inlined artifact table.
   - **HITL ack recorded** — for HITL-only phases, explicit human acceptance must have been recorded.
   On pass: update Current block (`phase_status: exited`), append history entry.

8. **Status is read-only.** `/phase status` reads `<artifacts>/ACTIVE` → reads `phase_status.md` → computes `next_phase` → reports. No writes. If `<artifacts>/ACTIVE` = `<none>`, report "no active WI."

9. **Tripwire halt blocks all entry; only `resolve-tripwire` clears it.** When `tripwire_halt: true`, `/phase enter` refuses all transitions. Human must call `/phase resolve-tripwire <reason>` — supplying the explicit decision (approve narrow edit or re-triage rationale). Resolution sets `tripwire_halt: false`, appends the decision to history, and updates the GH issue body.

10. **History entries immutable.** Once appended, never modified or deleted. History is the audit trail.

11. **WI close clears `<artifacts>/ACTIVE`.** `/phase close` is the sole operation that flips `<artifacts>/ACTIVE` from `<N>_<slug>` to `<none>`. Refuses unless `phase_status` = `exited` AND `current_phase` is the terminal legal phase for `mode` AND `tripwire_halt` = `false`. Appends a `close` history entry and sets `last_actor: human`. Does NOT delete `<artifacts>/<WI>/` — folder retirement is a separate ritual owned by a different skill.

### Reference Tables (inline verbatim in output skill)

#### Mode-Phase Legality

| Mode          | Legal phases (in order)                                   |
| ------------- | --------------------------------------------------------- |
| `direct-edit` | `ide`, `ral`, `qa`                                        |
| `mini`        | `ide`, `aln`, `ral`, `qa`                                 |
| `full`        | `ide`, `aln`, `res`*, `pro`*, `prd`, `iss`, `ral`†, `qa` |

\* Optional — `res` legal only when `needs_research` flag set; `pro` legal only when `pro_gate_tripped` flag set.  
† `par` is an alternative to `ral` (mutually exclusive); `par` currently blocked (substrate TBD).

Cross-phase: `rev` and `ica` legal alongside any sequential phase in any mode.

#### Phase-Required Artifacts for Exit

| Phase | Required artifacts for exit                                                          | HITL-only? |
| ----- | ------------------------------------------------------------------------------------ | ---------- |
| `ide` | `mini`/`full`: `<artifacts>/<WI>/idea.md` exists. `direct-edit`: GH issue exists.   | yes        |
| `aln` | `context.md` touched or ADR written                                                  | yes        |
| `res` | Research file(s) written                                                             | no         |
| `pro` | Prototype variant presentation written; chosen direction recorded                     | yes        |
| `prd` | PRD artifact exists                                                                  | yes        |
| `iss` | At least one issue created from PRD                                                   | no         |
| `ral` | All assigned issues resolved or explicitly deferred                                   | no         |
| `par` | (same as `ral`)                                                                      | no         |
| `qa`  | QA notes written; human verdict recorded                                              | yes        |
| `rev` | Review output written                                                                | yes        |
| `ica` | Arch-review output written                                                           | no         |

#### Next-Phase Computation

Given `mode`, `current_phase` (with `phase_status: exited`), and flags:

1. Look up mode's legal-phase sequence.
2. Find `current_phase` in the sequence.
3. Next entry = `next_phase`.
4. If `current_phase` is last in sequence → `next_phase: done`.
5. Optional phases (`res`, `pro`) are skipped unless their gate flag is set.
6. If `current_phase` = `aln` and `needs_research` set → `next_phase: res`. If `current_phase` = `aln` or `res` and `pro_gate_tripped` set → `next_phase: pro`.

---

## Skill Behaviors

In order:

1. **Parse subcommand.** Accept: `enter <code>`, `exit <code>`, `status`, `resolve-tripwire <reason>`, `close`. Unrecognized → return `status: error, reason: unknown subcommand "<input>"`.

2. **Resolve active WI.** Read `<artifacts>/ACTIVE`.
   - If `<none>` + subcommand `status` → report "no active WI" and return `status: ok, wi: none`.
   - If `<none>` + subcommand `enter`, `exit`, or `resolve-tripwire` → return `status: error, reason: no active WI — set <artifacts>/ACTIVE first`.
   - Otherwise → read `<artifacts>/<WI>/phase_status.md`. If absent and subcommand is `enter` (first phase of WI), create with default Current block (`wi` from `<artifacts>/ACTIVE`; `mode` + `current_phase` from `enter` arguments; `phase_status: exited` initially so the enter-guard "previous exited" check passes; `tripwire_halt`, `needs_research`, `pro_gate_tripped` default `false`).

3. **Branch on subcommand.**

   **`enter <code>`:**
   - Check mode-phase legality. If illegal → `status: rejected, reason: phase <code> not valid for mode <mode>`.
   - Check previous phase exited (or first entry). If not → `status: rejected, reason: previous phase <current> not yet exited`.
   - Check `tripwire_halt` = `false`. If `true` → `status: rejected, reason: tripwire halt active — call /phase resolve-tripwire <reason> to clear`.
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

   **`resolve-tripwire <reason>`:**
   - Require non-empty `<reason>`. If empty → `status: rejected, reason: reason required — record the human's decision (approve narrow edit or re-triage rationale)`.
   - Verify `tripwire_halt` = `true`. If already `false` → `status: rejected, reason: tripwire_halt is already false`.
   - Update Current block: `tripwire_halt: false`, `last_actor: human`.
   - Append history entry: `<timestamp> | resolve-tripwire | reason: <reason>`.
   - Update GH issue body: append `Tripwire halt resolved: <reason>` via `gh issue edit --body-file` or `gh issue comment`.
   - Return `status: ok, tripwire_resolved: true`.

   **`close`:**
   - Verify `<artifacts>/ACTIVE` ≠ `<none>`. If already `<none>` → `status: rejected, reason: no active WI to close`.
   - Verify `tripwire_halt` = `false`. If `true` → `status: rejected, reason: tripwire halt active — call /phase resolve-tripwire <reason> before close`.
   - Verify `phase_status` = `exited`. If not → `status: rejected, reason: current phase <current_phase> is <phase_status>, not exited`.
   - Verify `current_phase` is the terminal legal phase for `mode` (last entry in that mode's legal-phase sequence — `qa` in all current modes). If not → `status: rejected, reason: current phase <current_phase> is not the terminal phase for mode <mode>`.
   - Append history entry: `<timestamp> | close | <mode>`.
   - Update Current block: `last_actor: human`.
   - Write `<artifacts>/<WI>/phase_status.md`.
   - Overwrite `<artifacts>/ACTIVE` with the literal string `<none>`.
   - Return `status: ok, closed: <wi>`.

4. **Write state file.** For `enter`, `exit`, `resolve-tripwire`, and `close`: rewrite Current block in-place; append history entry at top of `## History` section. For `close`, additionally overwrite `<artifacts>/ACTIVE` with `<none>`.

---

## Constraints (must appear as Hard Rules inside the skill)

- **Sole writer**: no other skill writes `phase_status.md` or `<artifacts>/ACTIVE`.
- **`<artifacts>` parameter**: accepted as optional input; defaults to `plan`; passed through to all file operations.
- **Mode-phase validation**: every `enter` checks legality table; illegal transitions rejected, never silently allowed.
- **Tripwire blocks all**: `tripwire_halt: true` blocks ALL `enter` calls; only `resolve-tripwire` clears it.
- **History immutability**: history entries are append-only.
- **`next_phase` never persisted**: always computed at read time.
- **`<artifacts>/ACTIVE` always exists**: contains `<N>_<slug>` or `<none>`, never absent.
- **HITL phases enforce ack**: exit from HITL-only phases requires recorded human acceptance.
- **No artifact production beyond state files**: `/phase` writes only `phase_status.md` and `<artifacts>/ACTIVE`.
- **WI close clears ACTIVE**: `close` is the sole operation that writes `<none>` to `<artifacts>/ACTIVE`; refuses unless terminal phase exited cleanly with tripwire clear.
- **No skill invocation**: `/phase` does not call other skills; it is called by them.

---

## Output Format (for the generated skill)

The output skill (`skills/output/phase.md`) must be a Claude Code SKILL.md — a single self-contained markdown prompt file that:

- Opens with a one-paragraph role statement: this skill orchestrates phase transitions via five subcommands (`enter`, `exit`, `status`, `resolve-tripwire`, `close`) and is the sole writer of `phase_status.md` and `<artifacts>/ACTIVE`.
- Contains an inlined **Hard Rules** block (Rules + Constraints above, brief imperative form). No "see doc §X" references.
- Has an ordered **Steps** section mapping to Behaviors above.
- Inlines the three reference tables (mode-phase legality, phase-required artifacts, next-phase computation) verbatim — core lookup data.
- Has a **Return** section specifying success/failure signal shape per subcommand. **Status signal exception**: this skill uses `status: rejected` (guard conditions not met) and `status: error` (invalid input/state) rather than `status: not_produced`, because it is an orchestration skill whose output is a state change, not an artifact. Both signal types carry a `reason:` field.
- Does **not** link to `coding_plan.md`, `phases.md`, `guardrails.md`, or `gr/gr_idea.md`.
- Phase codes appear throughout as domain objects — this is the orchestrator, not a phase-coupled skill.
- Passes the test: if the skill file were the only file in the repo, an agent reading it could still execute correctly.

---

**Resolved 2026-05-28:** `issue` field dropped from the Current block schema. Issue numbers live on GH itself — surfaced via `gh issue list --search "<WI>"` or the `owner-issue` provenance field in artifact frontmatter. Rationale: `full` mode emits its issue at `iss` (post-PRD), so a pre-`iss` issue field forced a chicken/egg dance. D10 (`status_idea.md` migration into `phase_status.md`) tentative answer "fold" still stands.
