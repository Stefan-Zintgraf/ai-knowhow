# 0001. Phase Bootstrap Sequence and `/phase` Scope

## Status

proposed

## Date

2026-05-28

## Context

`phases.md` §5 and `coding_plan.md` §"Phase Transition Mechanism" specified the `ide` entry sequence as:

```
direct-edit:  /phase enter ide → /triage-idea →                  /phase exit ide
mini / full:  /phase enter ide → /triage-idea → /distill-idea →  /phase exit ide
```

Three problems surfaced while preparing to build A12 (`/phase`) and A13 (`/triage-idea`):

1. **Chicken/egg on `/phase enter ide`.** The `enter` subcommand was specified to guard "mode legal for this phase," but mode is unknown until `/triage-idea` runs *inside* `ide`. The guard guards nothing on entry.
2. **Empty phase for `direct-edit`.** `direct-edit` mode requires no distillation. The pattern `enter ide → triage → exit ide` produced a phase entry/exit pair around what is essentially a gateway decision, not a phase of work.
3. **Re-triage carve-out.** `/triage-idea --remode` was specified to run standalone (no `/phase` enter/exit) yet still mutate `phase_status.md`'s `mode` field. This broke the "`/phase` is sole writer" invariant.

A second, related question: should `/phase` print "next step" as a verb (`/phase next`) instead of requiring the human to know which phase code to type (`/phase enter aln`)?

## Decision

Replace the prior sequence with a default-verb bootstrap that separates **state transitions** (owned by `/phase`) from **artifact creation** (owned by phase skills). Triage becomes a near-pure function that mints the slug folder and writes a pending payload; `/phase` consumes the payload and persists `ACTIVE` + `phase_status.md`.

### Locked contracts

1. **`/phase next` is the default verb.** With no args, `/phase` reads `ACTIVE` and `phase_status.md`, computes `next_phase` against `phases.md` §4 chains, and prints a paste-ready command for the next step. `/phase enter <code>` survives as a recovery / jump escape hatch (e.g., re-entering `aln` after a tripwire halt), not the everyday verb.
2. **Two-command bootstrap.** When `ACTIVE = <none>`, `/phase` prints `"no active WI. run: /triage-idea"` and stops. `/phase` does not invoke other skills (no dispatcher pattern).
3. **`/phase` is the sole writer of `phase_status.md` + `<artifacts>/ACTIVE`.** Phase skills never touch these files. They write their own artifacts (`idea.md`, ADRs, PRD sections, `research/*.md`, etc.).
4. **`/triage-idea` is a near-pure function with one side effect: it mints the `<slug>/` folder.** It runs the 4-axis matrix with HITL, derives slug from the brief (kebab-case, stopwords stripped, ≤40 chars, collision suffix), creates `<artifacts>/<slug>/`, and writes:
   - `<artifacts>/<slug>/.pending-triage.json` — the structured result (`mode`, `slug`, `owner_issue`, axis scores, rationale).
   - `<artifacts>/.pending-bootstrap` — one-line pointer file containing the slug.
   It prints `"now run: /phase"`.
5. **`/phase` consumes the pending payload on next invocation.** Reads `.pending-bootstrap` → reads `<slug>/.pending-triage.json` → writes `ACTIVE` + `phase_status.md` → renames pending to `triage-decision.json` (audit trail) → deletes the bootstrap pointer → prints the full next command (e.g., `"run: /distill-idea my-cool-slug"` for mini/full, or `"run: /phase next"` for direct-edit which jumps straight to `ral`).
6. **`/phase next` prints the full paste-ready command line, slug included.** This requires `/phase` to hold an internal skill-signature registry (name + arg shape per phase skill). The registry is small (one row per A-table skill) and grows linearly.
7. **Phase artifacts vs phase state are separately owned.** State (`phase_status.md`, `ACTIVE`) = `/phase` only. Artifacts (`idea.md`, ADRs, PRD, `research/*.md`, variant docs) = the phase skill that produces them. Phase skills receive their slug as an explicit argument (`/distill-idea <slug>`) — they do not peek at `phase_status.md` to discover it.
8. **C6 relaxed: `direct-edit` also gets a `<slug>/` folder.** The folder contains only `triage-decision.json` (audit). The "issue body is the record" intent of C6 is preserved for *work artifacts* (no `idea.md`, no `aln` transcript, no PRD) but the audit footprint is symmetric across all three modes. Symmetry buys code-path simplicity in `/triage-idea`; the one-file folder cost is negligible.
9. **Re-triage routes through `/phase`.** `/triage-idea --remode <slug>` writes `<slug>/.pending-retriage.json`; the next `/phase` invocation consumes it and renames to `retriage-decision-<ts>.json`. The `--remode` flag stays on `/triage-idea` (not `/phase remode`) because the work — running the 4-axis matrix again with HITL — is triage's, not `/phase`'s.
10. **B1 hook reinterpretation.** B1 (`routing-step-enforcer`) treats "pending scratch file exists" as a deferred-commit state, not a violation. It only warns when a phase skill ran AND no pending file was left AND no `/phase` call followed.

### Resulting sequences

```
Bootstrap (any mode):
  1. /phase                          → "no active WI. run: /triage-idea"
  2. /triage-idea                    → HITL 4-axis pass; mints <slug>/; writes pending + pointer;
                                       prints: "now run: /phase"
  3. /phase                          → consumes pending; persists ACTIVE + phase_status;
                                       moves pending → <slug>/triage-decision.json;
                                       prints next paste-ready command:
                                         direct-edit  → "run: /phase next"   (advances to ral)
                                         mini / full  → "run: /distill-idea <slug>"

  4. (mini/full only) /distill-idea <slug>  → writes <slug>/idea.md;
                                              prints: "now run: /phase next"
  5. /phase next                            → ide → aln transition (or onward per mode chain)

Re-triage (mid-WI, Idea11):
  /phase                       → "run: /triage-idea --remode <slug>"
  /triage-idea --remode <slug> → writes <slug>/.pending-retriage.json
  /phase                       → consumes; moves to retriage-decision-<ts>.json
```

## Consequences

**Easier:**

- `/phase enter ide` guard chicken/egg removed — there is no `enter ide` call. The guard checks that previously plagued the design simply don't apply.
- One verb (`/phase next`) covers the common path. Humans never look up phase codes.
- Triage's pure-ish shape (one well-defined side effect — slug folder creation) is testable in isolation. Input = brief. Output = pending JSON + folder + pointer. No transcript-coupled state writes to mock.
- Audit trail symmetric across modes — every WI has `<slug>/triage-decision.json`, simplifying audit tooling.
- Adding a new phase skill = registering its signature in `/phase`'s registry + writing the skill. No new orchestration verb per skill.

**Harder:**

- `/phase` now owns a skill-signature registry. When a phase skill's call signature changes, `/phase` must be updated in lockstep. Mitigation: registry is one row per A-table skill, kept in the same source doc that defines the skill.
- Two scratch-file locations (`<artifacts>/.pending-bootstrap` root pointer + `<slug>/.pending-triage.json` payload) introduce a small consistency invariant: pointer must match an existing pending payload. `/phase` must handle "pointer present, payload missing" and "payload present, pointer missing" as defined failure modes, not crashes.
- `direct-edit` is no longer literally featherweight (one folder + one file per WI). The C6 "issue body is the record" intent must be re-explained to refer to *work artifacts only*, not audit.

**Impossible (intentionally):**

- `/phase` invoking other skills internally. Two-command bootstrap forecloses the "`/phase` is a dispatcher" evolution. Skills stay independently runnable; `/phase` stays a state machine.
- Phase skills writing `phase_status.md` or `ACTIVE`. Hard invariant — enables single-point audit of all phase-state mutations.

## Alternatives Considered

- **Keep `/phase enter ide → /triage-idea → /phase exit ide`.** Rejected: chicken/egg on the entry guard; empty-phase ceremony for `direct-edit`; re-triage carve-out breaks sole-writer invariant.
- **`/phase` as dispatcher (invokes triage and distill internally).** Rejected: tightly couples `/phase` to every phase skill's import path; loses the "skills are independently runnable" property; one-command-start convenience didn't justify the architectural cost.
- **Handoff via conversation context (no scratch file).** Rejected: fragile across sessions; not durable for audit; breaks if compaction drops the triage result.
- **Handoff via human-pasted blob (`/phase commit <json>`).** Rejected: error-prone (humans pasting JSON), and drops the elegance of the default verb.
- **Triage skips folder creation for `direct-edit` (keep C6 strict).** Rejected: introduces a parallel code path in triage (`if mode == direct-edit: write to <artifacts>/triage-decisions/<slug>-<ts>.json else: mint folder`). Symmetric write target was cheaper.
- **Distill peeks at `phase_status.md` for slug.** Rejected: violates "phase skills do not read phase state"; couples distill to `/phase`'s file format. Explicit arg is cleaner.
- **`/phase remode` subcommand for re-triage.** Rejected: the work (4-axis pass with HITL) belongs to triage, not `/phase`. Keeping `--remode` on triage preserves separation of concerns.

## Related ADRs

(none yet — this is the first)

## Related Aln15 entries

(none — pre-`aln` design decision)

## References

- `coding_plan.md` §"Phase Transition Mechanism" (settled-decisions block, 2026-05-22 + 2026-05-28)
- `coding_plan.md` line 229 (the open question this ADR resolves) and line 235 ("strange to start with triage instead of distill")
- `phases.md` §4 (mode chains) and §5 (skill bindings + prior `ide` call sequence)
- `gr/gr_idea.md` Idea8–Idea11 (triage matrix, tripwires, re-triage)
- `gr/gr_algn.md` Aln19 (collapsed `aln` for `mini` mode)
- Pocock 7-phases doc — phase 1 idea triage origin
