---
title: "The 7 phases of AI-driven development"
url: "https://www.youtube.com/watch?v=Ah9p7v7nJWg"
channel: "Matt Pocock"
published: "2026-03-03"
duration: "8:26"
processed: "2026-05-17"
status: "unvalidated"
confidence: "medium"
tags:
  - ai-coding
  - technical-video
  - workflow
  - claude-code
  - ralph-loop
  - prd
  - kanban
  - agentic-coding
  - spec-driven-development
---

# The 7 phases of AI-driven development

## Table of Contents

- [Executive Summary](#executive-summary)
- [One-Sentence Thesis](#one-sentence-thesis)
- [Core Concepts](#core-concepts)
- [Workflows and Methods](#workflows-and-methods)
- [Tools, Libraries, and Frameworks](#tools-libraries-and-frameworks)
- [Tradeoffs and Failure Modes](#tradeoffs-and-failure-modes)
- [Claims Made By Speaker](#claims-made-by-speaker)
- [Relevance To AI Coding Workflow](#relevance-to-ai-coding-workflow)
- [Detailed Timestamped Notes](#detailed-timestamped-notes)
- [Open Questions](#open-questions)
- [Experiments To Try](#experiments-to-try)
- [My Current Assessment](#my-current-assessment)
- [Transcript Information](#transcript-information)
- [References](#references)

## Executive Summary

- Matt Pocock proposes a 7-phase pipeline for serious AI-assisted coding: **Idea → Research → Prototype → PRD → Implementation Plan → Execution → QA**.
- The framing is explicitly **anti-vibe-coding**: aimed at engineers who treat AI as a force-multiplier for durable, production-grade software, not as a vending machine for throwaway demos.
- The phases are claimed to generalize across multiple AI coding methodologies: **Ralph loops**, **GSD (Get Shit Done)**, and **SpecKit**.
- **Phase 1 — Idea**: The trigger. Can be anything from a whole app to a single bug fix or refactor; scale is irrelevant; the process is the same.
- **Phase 2 — Research** (conditional): Only when external dependencies or hard-to-explore territory exist (e.g., Stripe, uncommon APIs). Output is cached into a `research.md` asset that lives in the repo for the lifetime of the sprint, then is discarded to prevent rot.
- **Phase 3 — Prototype** (conditional): Used when human taste must be imposed — UI, software architecture, or testing external services. The LLM generates multiple variants on a throwaway route; the human picks one and commits it as a reference for downstream agents.
- **Phase 4 — PRD**: A Product Requirements Document (or any document describing the end state). Created by having the agent **grill the human** down every branch of the decision tree. Matt uses a custom "writer PRD" skill for this.
- **Phase 5 — Implementation Plan**: PRD is decomposed into a **Kanban board** of tickets with blocking relationships, enabling parallel agent execution rather than a single sequential plan.
- **Phase 6 — Execution**: A coding agent (Matt: a Ralph loop) processes tickets. Most of the time sequential is sufficient; parallelization is available when tickets are non-blocking.
- **Phase 7 — QA**: Agent generates a QA plan; a **human** walks through the completed work, reads code, and feeds defects back as new tickets. The last three phases (Plan → Execute → QA) **loop** until convergence.
- Matt uses **GitHub Issues** for both PRD and Kanban board but notes GitHub lacks native blocking relationships; **Linear** is suggested as a better fit.
- A "gray box architecture" (referenced from prior videos, not defined here) may reduce the need for human code review during QA.
- **Code review is conspicuously absent** as a named phase; Matt acknowledges this and folds it tentatively under Execution or QA.
- The full setup is designed to enable **AFK (away-from-keyboard) execution** — the upfront investment in research, prototype, PRD, and Kanban is what makes unattended runs produce good results.
- The model is **iterative and recursive at the tail end** — QA produces new Kanban tickets which feed back into Execution, so phases 5–7 are a loop, not a straight line.
- Research artifacts are **deliberately ephemeral** to prevent stale context from misleading future agent runs.
- The video is short (8:26) and acts as a map/index to deeper material in Matt's newsletter rather than a deep dive into any single phase.

## One-Sentence Thesis

Serious AI-driven development should flow through seven distinct phases — idea, research, prototype, PRD, implementation plan, execution, and QA — with the last three forming a tight iterative loop, because front-loading taste, specification, and decomposition is what allows AI agents to execute long-running work unattended and still produce code that lasts.

## Core Concepts

### The 7-Phase Pipeline

- **Explanation:** A linear-then-iterative workflow for AI coding: Idea → Research (optional) → Prototype (optional) → PRD → Implementation Plan (Kanban) → Execution → QA, where phases 5–7 loop until done.
- **Why it matters:** Provides a reusable mental model that survives across specific tooling choices (Ralph, GSD, SpecKit). Treats AI coding as engineering discipline rather than improvisation.
- **Related concepts:** Spec-driven development, agentic loops, ticket-based work decomposition.
- **Prerequisites:** Familiarity with a coding agent (e.g., Claude Code), basic engineering process literacy (PRDs, Kanban boards).

### Research Caching (`research.md`)

- **Explanation:** When the work involves external APIs or hard-to-explore code, pre-explore once and cache findings into a Markdown asset the agent reads on each invocation, instead of forcing every fresh context window to re-discover.
- **Why it matters:** Each new agent run starts with a fresh context window; expensive exploration shouldn't be repeated. Caching the research makes downstream agent runs cheaper, faster, and more consistent.
- **Related concepts:** Context window management, retrieval augmentation, prompt caching, agent memory.
- **Prerequisites:** A repository the agent can read from; a convention for where research lives.
- **Caveat from Matt:** Research is sprint-scoped and disposable — it can rot and mislead the agent, so it shouldn't persist beyond the idea it serves.

### Prototype as Taste-Imposition Step

- **Explanation:** Before specifying anything, throw multiple LLM-generated variants onto a throwaway route, iterate with the agent in a human-in-the-loop fashion, pick the best, commit it as a reference artifact for later agents.
- **Why it matters:** PRDs alone are too abstract; taste decisions (UI, architecture, integration patterns) need concrete artifacts to anchor them. Pre-committing the chosen prototype gives the execution agent a known-good target.
- **Related concepts:** Design exploration, divergent/convergent thinking, reference implementations.
- **Prerequisites:** A safe throwaway location in the codebase; willingness to discard most variants.

### PRD via Adversarial Grilling

- **Explanation:** A Product Requirements Document is generated by prompting the agent to interrogate the human across every decision point, rather than letting the human write a one-sided spec.
- **Why it matters:** Forces decisions to be made explicit before code is written; surfaces ambiguity the human would otherwise leave for the agent to resolve (badly).
- **Related concepts:** Socratic prompting, requirements elicitation, spec-first development.
- **Prerequisites:** A "writer PRD" skill or equivalent prompt scaffold; tolerance for being questioned.

### Kanban-Style Implementation Plan

- **Explanation:** The PRD is decomposed into tickets with blocking relationships. Non-blocking tickets can be picked up by parallel agents; blocked ones wait. Alternative is a single sequential plan.
- **Why it matters:** Enables parallelism, makes progress legible, and gives each agent invocation a narrow, well-defined task — which empirically works better than vague large tasks.
- **Related concepts:** Task graphs, DAGs, parallel agent orchestration.
- **Prerequisites:** A board that supports blocking relationships (Linear preferred; GitHub Issues works but lacks native blocking).

### Ralph Loop (Execution Pattern)

- **Explanation:** Matt's preferred execution mechanism. Not defined in the video, but referenced as a loop in which a coding agent works through tickets, typically sequentially. Detailed writing is linked separately (see References).
- **Why it matters:** The execution phase needs *some* loop mechanism; Ralph is one named, documented option.
- **Related concepts:** Agent loops, GSD, SpecKit.
- **Prerequisites:** See linked Ralph getting-started post.

### QA Loop With Human-in-the-Loop

- **Explanation:** After execution, the agent generates a QA plan. A human walks through the deliverable, reads code, finds defects, and files them as new tickets. The cycle repeats.
- **Why it matters:** Closes the loop between agent output and validated reality. The human is the authority on "done."
- **Related concepts:** Code review, acceptance testing, gray-box architecture (referenced).
- **Prerequisites:** Human time and attention; willingness to actually read agent-produced code.

### Gray Box Architecture (referenced, not defined)

- **Explanation:** Matt mentions a "gray box architecture" from previous videos that may reduce the need for humans to read every line of agent-produced code during QA.
- **Why it matters:** Implies architectural choices can shift the QA burden; reduces the cost of unattended execution.
- **Related concepts:** Black-box testing, contract testing, observability.
- **Prerequisites:** Watching Matt's previous videos for the actual definition.

## Workflows and Methods

### The 7-Phase Workflow

- **Purpose:** End-to-end pipeline for shipping production-quality software with AI assistance.
- **When to use:** Any AI-assisted coding task — full app, feature, bug fix, or refactor. Scale-invariant per Matt.
- **Inputs:** An idea (any size), access to a coding agent (Matt uses Claude Code), a repo, optionally a Kanban tool.
- **Steps:**
  1. **Idea** — Articulate the trigger (app, feature, bug, refactor).
  2. **Research** *(optional)* — If external dependencies or hard exploration needed, cache findings into `research.md`.
  3. **Prototype** *(optional)* — If taste needs to be imposed, generate variants on a throwaway route, pick one, commit it.
  4. **PRD** — Have the agent grill you to produce a doc describing the end state.
  5. **Implementation Plan** — Decompose PRD into a Kanban of tickets with blocking relationships.
  6. **Execution** — Run a coding agent (e.g., Ralph loop) over the board; parallelize where non-blocking.
  7. **QA** — Agent produces QA plan; human validates; defects become new tickets; loop back to Execution.
- **Outputs:** A shipped, human-validated feature or codebase change; a discardable `research.md`; a committed prototype; a PRD; a Kanban history.
- **Benefits:**
  - Allows AFK / unattended execution.
  - Generalizes across Ralph, GSD, SpecKit.
  - Forces taste and spec decisions to be made *before* code is written.
  - Scales from bug fix to full app.
- **Tradeoffs:**
  - High upfront process overhead — overkill for trivial changes.
  - Requires tool support (Kanban with blocking) and custom skills (writer PRD).
  - Research assets can rot if not actively managed.
- **Failure modes:**
  - Stale `research.md` misleads later agent runs.
  - Skipping the prototype phase produces taste-blind output.
  - PRD without adversarial grilling leaves ambiguity that the agent resolves badly.
  - Skipping human QA produces unreviewed code that may pass agent self-checks but fail in production.
  - Treating phases 5–7 as linear (one-shot) rather than a loop.
- **Validation idea:** Run the workflow once on a real feature; compare time-to-ship and defect rate against an ad-hoc "just prompt and pray" baseline.

### Research Caching Sub-workflow

- **Purpose:** Avoid re-exploring expensive external dependencies on every agent invocation.
- **When to use:** Integrations with uncommon APIs, third-party services (Matt's example: Stripe), or any context the agent finds hard to recover on its own.
- **Inputs:** API docs, codebase regions, external service behavior.
- **Steps:**
  1. Run a research phase with the agent.
  2. Persist findings into `research.md` (or similar) inside the repo.
  3. Reference this asset in subsequent agent prompts.
  4. **Discard** at the end of the sprint to prevent rot.
- **Outputs:** A scoped, ephemeral Markdown research asset.
- **Benefits:** Faster, cheaper, more consistent downstream agent runs.
- **Tradeoffs:** Maintenance burden; stale-content risk.
- **Failure modes:** Forgetting to discard; treating research as canonical instead of provisional.
- **Validation idea:** Compare agent token usage and exploration time with and without a `research.md` for the same task.

### Prototype Variant Generation

- **Purpose:** Externalize taste decisions early, before they're frozen in the PRD.
- **When to use:** UI work, architectural choices, or testing external service shapes.
- **Inputs:** A rough idea of the surface area; a throwaway route or directory.
- **Steps:**
  1. Ask the LLM to generate multiple variants of the thing.
  2. Iterate with the agent in a couple of sessions.
  3. Select the preferred variant.
  4. Commit it as a reference artifact.
- **Outputs:** A committed reference prototype the execution agent can target.
- **Benefits:** Concrete grounding for downstream work; cheap exploration of design space.
- **Tradeoffs:** Time spent on variants that get thrown away.
- **Failure modes:** Over-iterating on prototypes that should have been promoted to real code; committing a prototype that drifts from the eventual PRD.

### PRD Grilling Pattern

- **Purpose:** Surface ambiguity in the human's mental model before the agent writes code.
- **When to use:** Whenever creating a spec for non-trivial work.
- **Inputs:** A rough idea, research, prototype.
- **Steps:**
  1. Invoke a writer-PRD skill or equivalent prompt.
  2. Let the agent ask hard questions across the decision tree.
  3. Answer them; capture answers in the PRD.
- **Outputs:** A PRD describing the end state.
- **Benefits:** Fewer agent-time surprises; clearer Kanban decomposition.
- **Tradeoffs:** Slower than freewriting a spec.
- **Failure modes:** Agent doesn't push back hard enough; human waves off questions.

### Plan → Execute → QA Loop

- **Purpose:** Iteratively converge on a finished product.
- **When to use:** After PRD exists; loop until QA produces no new tickets.
- **Inputs:** PRD, Kanban board, coding agent.
- **Steps:**
  1. Decompose PRD into tickets with blocking relationships.
  2. Run coding agent(s) over non-blocked tickets.
  3. On completion, generate QA plan.
  4. Human walks through QA, files defects as new tickets.
  5. Back to step 2.
- **Outputs:** A converged, QA-passed deliverable.
- **Benefits:** Progress is observable per ticket; defects re-enter the same machinery.
- **Tradeoffs:** Loop can extend indefinitely without a clear "done" definition.
- **Failure modes:** Skipping human QA; treating agent self-QA as sufficient; never converging because QA keeps generating low-priority tickets.

## Tools, Libraries, and Frameworks

| Name                 | Type                                 | Purpose                                                                   | Mentioned Context                                                     | Link                                                          |
| -------------------- | ------------------------------------ | ------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------- |
| Claude Code          | AI coding assistant                  | Matt's primary AI coding agent                                            | "in my case, Claude code usually"                                     | https://www.anthropic.com/claude-code                         |
| Ralph (Ralph loops)  | Execution loop pattern / methodology | Matt's preferred execution mechanism for phase 6                          | "doing Ralph loops like I mostly am"                                  | https://aihero.dev/getting-started-with-ralph                 |
| GSD                  | AI coding methodology                | Listed as one approach the 7 phases generalize over                       | "whether you're doing GSD"                                            | *not linked*                                                  |
| SpecKit              | AI coding methodology                | Listed as one approach the 7 phases generalize over                       | "whether you're using SpecKit"                                        | *not linked*                                                  |
| GitHub Issues        | Issue tracker / Kanban               | Used by Matt for both PRD and Kanban board                                | "I generally use GitHub issues for both the PRD and the canbon board" | https://github.com/                                           |
| Linear               | Issue tracker / Kanban               | Suggested alternative because it supports blocking relationships natively | "you might be just better off with something like linear, which does" | https://linear.app/                                           |
| Stripe               | Payment API                          | Example of an integration that warrants a research phase                  | "if you're doing like a Stripe integration"                           | https://stripe.com/                                           |
| Writer-PRD skill     | Custom agent skill (Matt's)          | Purpose-built skill for generating PRDs via grilling                      | "I have a writer PRD skill that is purpose-designed for this"         | *implied via Matt's newsletter; not directly linked in video* |
| AI Hero (newsletter) | Newsletter / content platform        | Matt's longer-form writing on AI engineering                              | "this is what I cover and elaborate on in my newsletter"              | https://aihero.dev/                                           |

## Tradeoffs and Failure Modes

- **Process overhead vs. agility:** The 7-phase pipeline is heavyweight; tiny changes may not justify it, but Matt claims the process is scale-invariant. Caution: the workflow may bottleneck on PRD/Kanban setup for small tasks.
- **Research rot:** Cached `research.md` can go stale and actively mislead future agent runs. Mitigated by scoping research to the sprint and discarding it.
- **Kanban tooling gap:** GitHub Issues lacks native blocking relationships, which undermines the parallelism benefit of the Kanban model.
- **Prototype-to-PRD drift:** A committed prototype can diverge from the PRD that follows it if the PRD-writing phase introduces new decisions.
- **QA as bottleneck:** Human QA is the only point in the loop where unautomated human attention is required. The whole AFK story collapses if the human is slow or absent.
- **Code review gap:** Matt explicitly notes there is no named "code review" phase. He hand-waves it into Execution or QA but acknowledges it's essential. Risk: review may fall through the cracks.
- **Gray-box reliance:** Matt suggests "gray-box architecture" may obviate code-reading during QA. Unverified in this video; risks if applied naively.
- **Hype-to-substance ratio:** The video is short and pitches a newsletter; depth on each phase is limited. Many claims are presented as personal experience rather than measured outcomes.

## Claims Made By Speaker

| Claim                                                                                                    | Evidence / Context                                                 | Confidence                                      | Needs Validation                                       |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------- | ------------------------------------------------------ |
| There are 7 distinct phases of AI-driven development.                                                    | Matt's own taxonomy; presented as observed across many approaches. | Low–medium (one practitioner's framing)         | Yes                                                    |
| These 7 phases generalize across Ralph loops, GSD, and SpecKit.                                          | Asserted, no comparison shown.                                     | Low                                             | Yes                                                    |
| The pipeline is scale-invariant (works for tiny bugs and full apps).                                     | Asserted in 01:23–01:34.                                           | Low                                             | Yes                                                    |
| Research artifacts should be sprint-scoped because they rot.                                             | Explained at 06:14–06:31 as preventing wrong turns.                | Medium (plausible mechanism)                    | Partial — depends on agent behavior with stale context |
| Prototyping is essential when taste must be imposed; PRD alone is too abstract.                          | Argued at 06:33–06:53.                                             | Medium                                          | Yes                                                    |
| Adversarial grilling during PRD creation produces better specs than freewriting.                         | Implied; uses a custom "writer PRD" skill.                         | Medium                                          | Yes                                                    |
| Kanban with blocking relationships enables effective parallel agent execution.                           | Asserted at 04:35–05:04.                                           | Medium                                          | Yes (depends on agent orchestration tooling)           |
| Most execution can be sequential; parallelization is a bonus, not a default.                             | Stated at 05:13–05:17.                                             | Medium                                          | Yes                                                    |
| With sufficient setup (research + prototype + Kanban + PRD), execution can be run AFK with good results. | Asserted at 07:34–07:40.                                           | Low–medium (depends heavily on task complexity) | Yes                                                    |
| Linear is a better Kanban tool than GitHub Issues because it natively models blocking relationships.     | Stated at 07:09–07:19.                                             | High (factual; verifiable)                      | Low — verifiable via tool docs                         |
| "Gray-box architecture" can reduce the need for humans to read all agent-produced code in QA.            | Referenced from prior videos; not defined here.                    | Unknown                                         | Yes                                                    |
| Code review is essential but not yet a named phase in this taxonomy.                                     | Self-acknowledged at 08:06–08:16.                                  | High (Matt's own admission)                     | N/A                                                    |

## Relevance To AI Coding Workflow

### Idea → Plan

- Phases 1–5 of Matt's model directly cover this stretch: Idea, Research, Prototype, PRD, Implementation Plan.
- Forces decisions upstream so agents have unambiguous targets downstream.
- Key takeaway: invest in PRD-via-grilling and a Kanban with blocking relationships before any code-generation loop starts.

### Plan → Code

- Phase 6 (Execution) is the code-generation step.
- Pattern: feed Kanban tickets to a coding agent (Ralph loop or similar), preferring sequential execution unless tickets are clearly parallelizable.
- Implication: the *prompt* the execution agent sees is the ticket + PRD + research + prototype context. Quality of those upstream artifacts directly determines code quality.

### Code → Test

- Not a named phase; testing is implicit in Execution and explicit in QA.
- Gap worth attention: no explicit guidance on agent-written tests, test-driven prompting, or test pyramid concerns.

### Test → Deploy

- Not addressed in the video.
- Implication: this taxonomy stops at "QA passed by human"; deployment, observability, and rollback are out of scope.

### Review / Debug

- Matt explicitly flags this as a gap: code review is not its own phase. He tentatively folds it under Execution or QA.
- Debugging-as-iteration is implicitly handled by the QA loop producing new Kanban tickets.

## Detailed Timestamped Notes

- **[00:00–00:34] Framing and scope.** Seven phases of AI-assisted development. Phases generalize across Ralph loops, GSD, SpecKit. Position: anti-vibe-coding, pro-engineering-fundamentals. Pitch for the AI Hero newsletter.
- **[00:57–01:23] Phase 1 — Idea.** Anything from a full app to a bug fix to a refactor. Scale-invariant.
- **[01:23–01:35] Foreshadowing.** The idea will be decomposed into tickets, run sequentially or in parallel by AI(s).
- **[01:35–02:40] Phase 2 — Research (optional).** Triggered by external/uncommon dependencies (example: Stripe, uncommon APIs). Cache findings in a `research.md` asset accessible to the agent, because each agent invocation runs in a fresh context window. Avoid re-exploration.
- **[02:40–03:25] Phase 3 — Prototype (optional).** When taste must be imposed (UI, architecture, external-service behavior). Use a throwaway route. Let the LLM generate variants. Iterate human-in-the-loop. Pick one. Commit to the codebase as a reference for downstream agents.
- **[03:25–04:24] Phase 4 — PRD.** Product Requirements Document. The agent grills the human across the decision tree. Matt has a custom "writer PRD" skill. Naming is incidental — the artifact is "some kind of document that describes the end state."
- **[04:24–05:05] Phase 5 — Implementation Plan.** Decompose the PRD into a Kanban board with blocking relationships. Alternative: a single sequential plan. Kanban enables parallel agent execution on non-blocked tickets.
- **[05:05–05:25] Phase 6 — Execution.** A coding agent (Ralph loop, for Matt) processes the board. Sequential is usually enough; parallelization is a bonus.
- **[05:25–06:00] Phase 7 — QA.** Agent generates a QA plan. A human walks through the deliverable, reads the code, files new tickets for defects. The last three phases (Plan → Execute → QA) **loop** until convergence. Gray-box architecture may reduce code-reading burden.
- **[06:00–06:31] Recap — Idea & Research.** Re-emphasis that research is sprint-scoped and disposable because it rots.
- **[06:31–06:53] Recap — Prototype.** Not only for UI; also for architecture and testing external services. PRD alone is too abstract — concrete feedback first.
- **[06:53–07:19] Recap — PRD & Kanban.** Matt uses GitHub Issues for both. Notes GitHub doesn't natively support blocking relationships; Linear does.
- **[07:19–07:40] Recap — Execution.** Ralph loop for Matt. Human-in-the-loop execution is possible but unnecessary if upstream phases were done well. AFK execution is viable.
- **[07:40–07:58] Recap — QA loop.** Agent QA plan → human QA → new tickets → more execution → more QA.
- **[07:58–08:24] Reflection and open ends.** Matt expects the list to grow to 8–9 phases over time. No explicit code-review phase — possibly folded into Execution or QA. Newsletter pitch and sign-off.

## Open Questions

- What exactly is a Ralph loop mechanically — what's the loop body, the termination condition, the prompt structure? (Linked separately; not defined in the video.)
- What does "gray-box architecture" mean in Matt's vocabulary, and how does it actually reduce QA load?
- Where should code review live? As a step in Execution, in QA, or as an 8th phase?
- How is "done" defined in the Plan → Execute → QA loop? What stops the loop from generating tickets forever?
- How does the workflow handle deployment, monitoring, and rollback?
- How does agent-written testing fit into the pipeline?
- How are merge conflicts handled when multiple parallel agents touch the same files?
- How is PRD-vs-prototype drift resolved when they disagree?
- What does the "writer PRD" skill actually look like as a prompt or skill definition?
- Is there empirical data (defect rate, time-to-ship) backing the claim that this pipeline beats ad-hoc prompting?

## Experiments To Try

### Experiment 1 — End-to-end on a real feature

- **Hypothesis:** Running the full 7-phase pipeline on a non-trivial feature produces fewer defects and less rework than ad-hoc agent prompting.
- **Context:** A medium-complexity feature in an existing codebase.
- **What to try:** Pick a feature. Walk through all 7 phases. Track time per phase and defects found in QA.
- **Expected benefit:** Better-quality output and a clearer estimate of process overhead.
- **Risk:** Overhead dominates on small features.
- **Measurement:** Time-per-phase, defect count at QA, rework cycles before convergence.

### Experiment 2 — Research caching A/B

- **Hypothesis:** A cached `research.md` materially reduces agent token usage and improves output consistency for external-API work.
- **Context:** An integration with an uncommon API.
- **What to try:** Same task twice — once with `research.md`, once without.
- **Expected benefit:** Reduced token usage, fewer wrong-turn errors.
- **Risk:** Stale research may degrade quality if not actively maintained.
- **Measurement:** Tokens used, number of agent self-corrections, time-to-completion.

### Experiment 3 — Prototype-first vs PRD-first

- **Hypothesis:** Building a prototype before the PRD produces a more useful PRD and reduces downstream rework.
- **Context:** A feature with significant UI or architectural decisions.
- **What to try:** Two parallel runs — one prototype-first, one PRD-first.
- **Expected benefit:** Concrete prototypes anchor PRD decisions.
- **Risk:** Prototype-first may bias the PRD toward whatever was prototyped, even if suboptimal.
- **Measurement:** Number of PRD revisions, agent confusion during Execution, QA defect count.

### Experiment 4 — GitHub Issues vs Linear

- **Hypothesis:** Linear's native blocking relationships materially improve parallel agent throughput.
- **Context:** A feature with naturally parallelizable subtasks.
- **What to try:** Run the same Kanban on both tools; measure orchestration overhead and parallel utilization.
- **Expected benefit:** Cleaner parallelism, less human bookkeeping.
- **Risk:** Tool migration cost.
- **Measurement:** Agent-hours running in parallel, human-minutes managing the board.

### Experiment 5 — Adversarial PRD grilling vs human freewriting

- **Hypothesis:** A PRD produced by adversarial agent grilling has fewer ambiguities than one freewritten by a human.
- **Context:** Same feature, two PRD-creation methods.
- **What to try:** Have a second agent read both PRDs and list ambiguities.
- **Expected benefit:** Quantified evidence that grilling reduces ambiguity.
- **Risk:** Grilling agent may invent fake ambiguities or miss real ones.
- **Measurement:** Count of ambiguities flagged; downstream Execution agent questions during runs.

### Experiment 6 — AFK execution feasibility

- **Hypothesis:** With sufficient upstream setup, an unattended execution loop produces production-grade output.
- **Context:** A well-scoped feature with a complete PRD and Kanban.
- **What to try:** Launch execution; do not intervene until QA.
- **Expected benefit:** Reclaimed developer time.
- **Risk:** Agent goes off-rails undetected; expensive token burn.
- **Measurement:** Defect count, time saved, token cost.

## My Current Assessment

- **Plausible:**
  - Front-loading research, prototype, and PRD work pays off when execution is delegated to agents.
  - Caching research in a `research.md` is a pragmatic context-management tactic.
  - Kanban with blocking relationships is a clean abstraction for agent-orchestrated parallel work.
  - Adversarial PRD grilling is a reasonable technique for surfacing ambiguity.
  - The Plan → Execute → QA loop matches how iterative engineering actually works in practice.
- **May be hype:**
  - The claim that these 7 phases generalize across Ralph, GSD, and SpecKit is asserted, not demonstrated.
  - "AFK execution with good results" is an aspirational claim and likely highly task-dependent.
  - The scale-invariance claim ("works for bug fixes and full apps alike") risks process overkill on small tasks.
- **Needs testing:**
  - Whether the full pipeline actually beats simpler workflows in measurable ways (defects, time, cost).
  - Whether research rot is a real problem at the timescales Matt suggests.
  - Whether prototype-first ordering helps or biases the PRD.
- **Useful later:**
  - The taxonomy itself is a good checklist for AI-assisted work even if individual phases are skipped.
  - The "research.md as ephemeral asset" idea is a clean, reusable pattern.
  - The naming of phases is helpful vocabulary for talking about AI coding workflows with collaborators.

## Transcript Information

- **Transcript source:** User-provided, originally extracted via `yt-dlp` with auto-generated English captions.
- **Transcript quality:** Reasonable but auto-generated; minor transcription artifacts visible (e.g., "canon board" / "canbon" / "canban" all referring to "Kanban"; "PR helping it" likely "PRD helping it"; "AFK" rendered correctly). Sufficient for distillation.
- **Caption type:** Auto-generated, not human-authored.
- **Description:** User-provided verbatim alongside the transcript.
- **Transcript file:** Embedded in user input (`the-7-phases-of-ai-driven-development.input.md`).
- **Description file:** Same input file.
- **Metadata file:** Same input file.
- **Extraction date:** 2026-05-17 (per user input).

## References

### Explicitly Mentioned References

#### GitHub Repositories

*None mentioned by name.*

#### Websites / Documentation

- **AI Hero (Matt Pocock's newsletter/site)** — https://aihero.dev/ — referenced throughout (00:42, 07:58) — Matt's longer-form writing on AI engineering and the broader context for this video.
- **Getting Started with Ralph** — https://aihero.dev/getting-started-with-ralph — referenced at ~05:23–05:25 — Matt's foundational write-up on the Ralph loop execution pattern.
- **How To Make Codebases AI Agents Love** — https://aihero.dev/s/QmBEIh — linked from the description — related material on structuring codebases for AI agents.
- **AI Hero newsletter signup** — https://aihero.dev/s/RQqb0X — linked from the description — newsletter subscription.
- **AI Hero Discord** — https://aihero.dev/s/N9eseO — linked from the description — community channel.

#### Books

*None mentioned.*

#### Papers

*None mentioned.*

#### Tutorials / Blog Posts / Courses

- **Getting Started with Ralph** — https://aihero.dev/getting-started-with-ralph — written tutorial on Ralph loops.
- **How To Make Codebases AI Agents Love** — https://aihero.dev/s/QmBEIh — related blog post.

#### Tools / Frameworks / APIs

- **Claude Code** — Matt's primary AI coding assistant (00:09) — https://www.anthropic.com/claude-code
- **Ralph (Ralph loops)** — Execution loop pattern (00:28, 05:21, 07:23) — https://aihero.dev/getting-started-with-ralph
- **GSD** — Named methodology (00:30) — *no link given in video or description*.
- **SpecKit** — Named methodology (00:31) — *no link given in video or description*.
- **GitHub Issues** — Used by Matt for both PRD and Kanban board (07:05) — https://github.com/
- **Linear** — Recommended alternative Kanban tool with native blocking relationships (07:18) — https://linear.app/
- **Stripe** — Example external integration warranting a research phase (02:06) — https://stripe.com/

#### People / Channels / Companies

- **Matt Pocock** — Speaker; the channel author — https://twitter.com/mattpocockuk (from description)
- **AI Hero** — Matt's publishing brand / newsletter — https://aihero.dev/

### Related / Inferred References

- **SpecKit (likely GitHub Spec Kit)** — https://github.com/github/spec-kit — *inferred*; GitHub's open-source toolkit for spec-driven development is the most likely referent for "SpecKit" given the context.
- **Anthropic Skills documentation** — https://docs.claude.com/ — *inferred*; Matt's "writer PRD skill" implies use of Claude Code's skill mechanism.
- **Kanban method (general)** — https://en.wikipedia.org/wiki/Kanban_(development) — *inferred*; relevant background for readers unfamiliar with the concept.
- **Spec-driven development (general)** — *inferred*; the broader category this workflow belongs to.
- **Context-window management literature** — *inferred*; relevant to the `research.md` caching idea.
