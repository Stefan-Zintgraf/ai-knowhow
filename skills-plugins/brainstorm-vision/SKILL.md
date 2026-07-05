---
name: brainstorm-vision
description: Coach a divergent product-vision brainstorm, captured as press-release vision points plus user-POV use-cases — with a scope lens that climbs the abstraction ladder to widen the vision one rung at a time.
disable-model-invocation: true
---

<what-this-is>

Run a relentless, one-question-at-a-time brainstorming session that opens up the **widest possible high-level vision** of a product, captured in a single living markdown file with a `## Vision scope` section (**scope items** `S1…Sn`) plus two capture parts: **vision points** (`V1`, `V2`, …) grouped under scope items, and a flat list of **use-cases** ("as someone …, I can finally …"). See [`GLOSSARY.md`](GLOSSARY.md) for every bolded term.

The session is **divergent** (**divergence**): push past the obvious first answers. Works for any product, software preferred.

Its rhythm is a loop, not a funnel: **diverge** → **scope lens** → (climb ↺ diverge) → finalize. It runs in phases — **Diverge** ([`brainstorming.md`](brainstorming.md)), then the **Scope lens** ([`scope-lens.md`](scope-lens.md)) at each **saturation**, then **Finalize** ([`finalizing.md`](finalizing.md)) once the **ladder** is **closed** — sequenced below.

</what-this-is>

<sequencing>

1. **Start the session.**
   - First, check for prior work to resume — see Pause and resume. Only a "start fresh" choice (or no prior work) begins a new session.
   - Read [`scope-steering.md`](scope-steering.md), turn scope steering **ON**, and run its A/B/C verification checks (it covers what to do on a failed check).
   - Read [`config.md`](config.md) for the session limits (`max_new_use_cases`, `warn_before`) — the **use-case cap**, hard-enforced by the `usecase-cap.sh` hook. If a cap is set, read [`usecase-cap.md`](usecase-cap.md), run its A/B verification checks, and — once the `.wip.md` path is settled — write the `brainstorm_usecase_cap.state` file (`WIP=` + `BASELINE=` current `UC` count, 0 for a brand-new file). A missing file or blank/`off` value means no cap; skip the state file. The counter is per *sitting* — re-do this baseline reset on every resume (see Pause and resume).
   - Settle the topic: if the user passed a brief/foundation file (or one is open), read it, treat its topic and goal as already chosen, confirm in one line, and begin — don't re-elicit what the brief settled. Otherwise ask once what product or problem we're opening up.
   - Once the topic is settled, write the `## Vision scope` section with a single **scope item** `S1` — the product's job in one plain line. This is the starting **anchor**. Draft, mention, or hint at **no** further **ladder** — the next **rung** is discovered later, by the **scope lens**, one at a time.

2. **Diverge.** Read [`brainstorming.md`](brainstorming.md) and run the interview. Stay here — this *is* the session. Keep generating until **saturation** (defined there).

3. **Wrap up — only at saturation.** The session ends when the user signals it ("done", "that's enough", "wrap up") **or** when you judge breadth has reached **saturation**. When you sense saturation, **offer** to wrap up once, gently — never force it; a divergent session shouldn't be cut short while ideas are still flowing. Once wrap-up is agreed, the next phase is the **scope lens** ([`scope-lens.md`](scope-lens.md)) — **not** finalize. **Hand off to a fresh session — do not read [`scope-lens.md`](scope-lens.md) or [`finalizing.md`](finalizing.md) inline.** Reading the climb/finalize machinery here would anchor the diverge phase; and the scope-lens pass runs entirely from the on-disk `.wip.md`, so a clean context drops the whole divergence transcript at no cost:
   - make the `.wip.md` current (**vision points** + **use-cases** written, per [`brainstorming.md`](brainstorming.md));
   - **replace** the `## Resume notes` section (see Pause and resume for the snapshot rule) with a single block marking **divergence saturated, wrap-up agreed, ladder open — resume runs the scope lens ([`scope-lens.md`](scope-lens.md))**;
   - do the **fresh-context handoff** (defined just below).

   The scope lens then proposes one **rung** and the human **climbs** or **closes**; only a **closed** **ladder** proceeds to the finalize gate. A **climb** re-enters a focused **divergence** at the new rung (back to step 2) — the loop.

**Fresh-context handoff.** The handoff shape used at wrap-up (step 3 above) and at a scope-lens **climb** ([`scope-lens.md`](scope-lens.md)) — a real context boundary that drops the divergence transcript at no cost, since the `.wip.md` + `## Resume notes` carry all resumable state: turn **scope steering** OFF (see [`scope-steering.md`](scope-steering.md)) — a session-end; tell the user the file path and to `/clear` (or open a new session) and re-invoke the skill, then **stop**. The branch-specific `## Resume notes` marker is written *before* the handoff, where the branch is described.

A session can also be **paused** mid-flight and resumed in a later sitting — including at the "ready to finalize" milestone. See Pause and resume.

</sequencing>

<pause-and-resume>

A vision session can span multiple sittings. The working file keeps a **`.wip.md`** suffix for as long as the session is unfinished, so an on-disk `*.wip.md` in the output directory *is* a paused, resumable session — even if the previous sitting ended abruptly without a clean pause.

**Resuming or extending (at session start).** Before proposing a new path, look in the output directory (default `docs/brainstorming/`) for prior work — both `*.wip.md` (a paused session) **and** finalized `*-foundation-vision.md` (a completed vision that can be re-opened to add use-cases). If any exist, **always ask the user** what to do — never auto-continue. Name the file(s) and topic(s), then offer the choice:

- **Resume a paused session** (`*.wip.md`) — read the whole file (`## Vision scope`, **vision points**, **use-cases**, and the **`## Resume notes`** if present), play back in two or three sentences where you left off and what's still open, then continue. Don't re-elicit settled ground. The `## Resume notes` marks which of **four** states the session is in — that decides where you re-enter:

  | `## Resume notes` marker | Re-enter at |
  |---|---|
  | *checkpoint / break, divergence not saturated* | **diverge**, same **anchor** (step 2) |
  | *scope widened to `S<n>`, divergence NOT saturated at the new scope* | **diverge**, focused on the new **rung** (step 2, walking the **breadth axes** afresh for the delta only) |
  | *divergence saturated, wrap-up agreed, ladder open* | the **scope lens** ([`scope-lens.md`](scope-lens.md)) |
  | *ready to finalize, sweep done, ladder closed* | finalize step 2 of [`finalizing.md`](finalizing.md) — unless use-cases changed since the sweep, which warrants a quick re-sweep of the affected axes first |

  Distinguish the third from the fourth carefully: **wrap-up agreed, ladder open** goes to the scope lens (which may still **climb**); only a **ladder closed** goes to finalize. Turn scope steering back ON on resume (its steer carries the current **anchor**). **If a use-case cap is configured, reset the cap baseline first thing** — rewrite `brainstorm_usecase_cap.state` with `BASELINE=` the current `UC` count in the `.wip.md`, giving this new sitting a fresh budget (see [`usecase-cap.md`](usecase-cap.md)). The hook allows exactly one prompt for this reset before it starts counting again.
- **Extend a finished vision** (`*-foundation-vision.md`) — re-open it: rename it back to `<name>.wip.md`, turn scope steering ON, and continue appending **use-cases** from where it stands (continuous numbering — never renumber existing items). A re-open goes back through the finalize gate afterwards.
- **Start fresh** — leave existing files untouched and begin a new `.wip.md` for the new topic.

If there are several candidates, list them and ask which (if any) to resume or extend.

**Pausing (on request — "pause", "stop for now", "let's continue later").**

1. Make sure the `.wip.md` is current (`## Vision scope` + **vision points** + **use-cases** written, per the file format in [`brainstorming.md`](brainstorming.md)).
2. **Replace** the **`## Resume notes`** section at the end with a single current-state snapshot — not a running log. Resume notes describe where to pick up *now*; the vision points and use-cases are the durable record, so don't keep a per-sitting changelog here. Carry forward only what's still true and **drop any superseded content** — old derived ladders, "next climb" pointers already climbed, prior-sitting progress blocks now folded into the current summary, and any re-open retrofit block (this rule owns it too). Capture just enough state to pick up cleanly, marking which of the **four** states above the session is in (see the table): which **breadth axes** are well covered vs. thin, threads left open, the next question you would have asked, whether the **provisional vision** still feels right, and — on a mid-climb pause — that scope widened to `S<n>`. If you've reached the wrap-up gate, note how far the sweep got (which axes in the `<slug>-architecture-lens.md` artifact are covered vs. open — the artifact holds the axes; don't duplicate them here) and whether the ladder is **open** (scope lens still pending) or **closed** and **ready to finalize**.

   **Safety — when to prune.** Only ever delete resume-note content *here*, at the pause/wrap-up write, where the block you delete is superseded in the same step by the one you write. Never prune at resume-*start* (read time): until this new snapshot is written, the old note is the only crash breadcrumb, so read it and re-establish context first, then let the next pause/wrap-up write replace it.
3. Turn scope steering OFF — a pause is a mini session-end (see [`scope-steering.md`](scope-steering.md)).
4. Tell the user the file path and that re-invoking the skill will resume from it. Then stop.

</pause-and-resume>
