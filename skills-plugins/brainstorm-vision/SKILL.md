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
   - Read [`scope-steering.md`](scope-steering.md), turn scope steering **ON**, and run its A/B/C verification checks (it covers what to do on a failed check).
   - Before starting anything new, check for prior work to resume — see Pause and resume.
   - Settle the topic: if the user passed a brief/foundation file (or one is open), read it, treat its topic and goal as already chosen, confirm in one line, and begin — don't re-elicit what the brief settled. Otherwise ask once what product or problem we're opening up.
   - Once the topic is settled, write the `## Vision scope` section with a single **scope item** `S1` — the product's job in one plain line. This is the starting **anchor**. Draft, mention, or hint at **no** further **ladder** — the next **rung** is discovered later, by the **scope lens**, one at a time.

2. **Diverge.** Read [`brainstorming.md`](brainstorming.md) and run the interview. Stay here — this *is* the session. Keep generating until **saturation** (defined there).

3. **Wrap up — only at saturation.** The session ends when the user signals it ("done", "that's enough", "wrap up") **or** when you judge breadth has reached **saturation**. When you sense saturation, **offer** to wrap up once, gently — never force it; a divergent session shouldn't be cut short while ideas are still flowing. Once wrap-up is agreed, the next phase is the **scope lens** ([`scope-lens.md`](scope-lens.md)) — **not** finalize. **Hand off to a fresh session — do not read [`scope-lens.md`](scope-lens.md) or [`finalizing.md`](finalizing.md) inline.** Reading the climb/finalize machinery here would anchor the diverge phase; and the scope-lens pass runs entirely from the on-disk `.wip.md`, so a clean context drops the whole divergence transcript at no cost:
   - make the `.wip.md` current (**vision points** + **use-cases** written, per [`brainstorming.md`](brainstorming.md));
   - add a `## Resume notes` section marking **divergence saturated, wrap-up agreed, ladder open — resume runs the scope lens ([`scope-lens.md`](scope-lens.md))**;
   - turn **scope steering** OFF (see [`scope-steering.md`](scope-steering.md)) — this handoff is a session-end;
   - tell the user the file path and to `/clear` (or open a new session) and re-invoke the skill to run the scope lens with a fresh context, then **stop**.

   The scope lens then proposes one **rung** and the human **climbs** or **closes**; only a **closed** **ladder** proceeds to the finalize gate. A **climb** re-enters a focused **divergence** at the new rung (back to step 2) — the loop.

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

  Distinguish the third from the fourth carefully: **wrap-up agreed, ladder open** goes to the scope lens (which may still **climb**); only a **ladder closed** goes to finalize. Turn scope steering back ON on resume (its steer carries the current **anchor**).
- **Extend a finished vision** (`*-foundation-vision.md`) — re-open it: rename it back to `<name>.wip.md`, turn scope steering ON, and continue appending **use-cases** from where it stands (continuous numbering — never renumber existing items). A re-open goes back through the finalize gate afterwards.
- **Start fresh** — leave existing files untouched and begin a new `.wip.md` for the new topic.

If there are several candidates, list them and ask which (if any) to resume or extend.

**Pausing (on request — "pause", "stop for now", "let's continue later").**

1. Make sure the `.wip.md` is current (`## Vision scope` + **vision points** + **use-cases** written, per the file format in [`brainstorming.md`](brainstorming.md)).
2. Add or refresh a **`## Resume notes`** section at the end, capturing just enough session state to pick up cleanly — and marking which of the **four** states above the session is in (see the table). Capture: which **breadth axes** are well covered vs. thin, threads left open, the next question you would have asked, whether the **provisional vision** still feels right, and — on a mid-climb pause — that scope widened to `S<n>`. If you've reached the wrap-up gate, note how far the sweep got (which axes in the `<slug>-architecture-lens.md` artifact are covered vs. open — the artifact holds the axes; don't duplicate them here) and whether the ladder is **open** (scope lens still pending) or **closed** and **ready to finalize**.
3. Turn scope steering OFF — a pause is a mini session-end (see [`scope-steering.md`](scope-steering.md)).
4. Tell the user the file path and that re-invoking the skill will resume from it. Then stop.

</pause-and-resume>
