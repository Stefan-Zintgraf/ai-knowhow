---
name: brainstorm-vision
description: Coach a divergent product-vision brainstorm, captured as a press-release vision plus user-POV use-cases.
disable-model-invocation: true
---

<what-this-is>

Run a relentless, one-question-at-a-time brainstorming session that opens up the **widest possible high-level vision** of a product, captured in a single living markdown file with two parts: a **press-release vision** and a growing list of **user-POV use-cases** ("as someone …, I can finally …").

The session is **divergent**: push past the obvious first answers. Works for any product, software preferred.

It runs in two phases, split across files so each carries only its own weight — **Diverge** ([`brainstorming.md`](brainstorming.md)), then **Finalize** ([`finalizing.md`](finalizing.md)) — sequenced below.

</what-this-is>

<sequencing>

1. **Start the session.**
   - Read [`scope-steering.md`](scope-steering.md), turn scope steering **ON**, then **verify the hook actually fires** — don't assume renaming the flag was enough (run its A/B/C checks). If verification fails, tell the user what's broken and ask whether to continue anyway before proceeding.
   - Before starting anything new, look in the output directory (default `docs/brainstorming/`) for prior work — see Pause and resume.
   - Settle the topic: if the user passed a brief/foundation file (or one is open), read it, treat its topic and goal as already chosen, confirm in one line, and begin — don't re-elicit what the brief settled. Otherwise ask once what product or problem we're opening up.

2. **Diverge.** Read [`brainstorming.md`](brainstorming.md) and run the interview. Stay here — this *is* the session. Keep generating until **saturation** (defined there).

3. **Wrap up — only at saturation.** The session ends when the user signals it ("done", "that's enough", "wrap up") **or** when you judge breadth has reached saturation. When you sense saturation, **offer** to wrap up once, gently — never force it; a divergent session shouldn't be cut short while ideas are still flowing. Once wrap-up is agreed, **hand off to a fresh session — do not read [`finalizing.md`](finalizing.md) inline.** The finalize gate runs entirely from the on-disk `.wip.md`, so a clean context here drops the whole divergence transcript at no cost:
   - make the `.wip.md` current (vision + use-cases written, per [`brainstorming.md`](brainstorming.md));
   - add a `## Resume notes` section marking **divergence saturated, wrap-up agreed — resume runs the finalize gate ([`finalizing.md`](finalizing.md)) from step 1**;
   - turn scope steering OFF (see [`scope-steering.md`](scope-steering.md)) — this handoff is a session-end;
   - tell the user the file path and to `/clear` (or open a new session) and re-invoke the skill to finalize with a fresh context, then **stop**.

A session can also be **paused** mid-flight and resumed in a later sitting — including at the "ready to finalize" milestone. See Pause and resume.

</sequencing>

<pause-and-resume>

A vision session can span multiple sittings. The working file keeps a `.wip.md` suffix for as long as the session is unfinished, so an on-disk `*.wip.md` in the output directory *is* a paused, resumable session — even if the previous sitting ended abruptly without a clean pause.

**Resuming or extending (at session start).** Before proposing a new path, look in the output directory (default `docs/brainstorming/`) for prior work — both `*.wip.md` (a paused session) **and** finalized `*-foundation-vision.md` (a completed vision that can be re-opened to add use-cases). If any exist, **always ask the user** what to do — never auto-continue. Name the file(s) and topic(s), then offer the choice:

- **Resume a paused session** (`*.wip.md`) — read the whole file (vision, use-cases, and the `## Resume notes` if present), play back in two or three sentences where you left off and what's still open, then continue from there. Don't re-elicit settled ground. If the notes say **wrap-up is agreed** (divergence saturated), don't re-open divergence — read [`finalizing.md`](finalizing.md) and run the two-step gate from step 1 (the architecture sweep). If instead the notes say the session is **ready to finalize** (the step-1 sweep is already done), go straight to step 2 of [`finalizing.md`](finalizing.md) — unless use-cases changed since the sweep, which warrants a quick re-sweep of the affected axes first.
- **Extend a finished vision** (`*-foundation-vision.md`) — re-open it: rename it back to `<name>.wip.md`, turn scope steering ON, and continue appending use-cases from where it stands (continuous numbering — never renumber existing items). At the next wrap-up its `<slug>-architecture-lens.md` is reconciled if present, or generated from scratch if absent.
- **Start fresh** — leave existing files untouched and begin a new `.wip.md` for the new topic.

If there are several candidates, list them and ask which (if any) to resume or extend.

**Pausing (on request — "pause", "stop for now", "let's continue later").**

1. Make sure the `.wip.md` is current (vision + use-cases written, per the file format in [`brainstorming.md`](brainstorming.md)).
2. Add or refresh a `## Resume notes` section at the end, capturing just enough session state to pick up cleanly: which breadth axes (emotion / kinds of user / lifecycle) are well covered vs. thin, threads left open, the next question you would have asked, and whether the provisional vision still feels right. If you've reached the wrap-up gate, note how far the step-1 sweep got — which axes in the `<slug>-architecture-lens.md` artifact are covered vs. open (the artifact itself holds the axes; don't duplicate them here) — and, if it's complete, that the session is **ready to finalize** (so resuming can skip straight to step 2).
3. Turn scope steering OFF — a pause is a mini session-end (see [`scope-steering.md`](scope-steering.md)).
4. Tell the user the file path and that re-invoking the skill will resume from it. Then stop.

</pause-and-resume>
