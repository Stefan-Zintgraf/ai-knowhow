---
title: "Full Walkthrough: Workflow for AI Coding — Matt Pocock"
url: "https://www.youtube.com/watch?v=-QFHIoCo-Ko"
channel: "Matt Pocock (@mattpocockuk)"
published: "2026-04-24"
duration: "1:36:29"
processed: "2026-05-09"
status: "unvalidated"
confidence: "medium"
tags:

- ai-coding
- technical-video
- agentic-coding
- tdd
- software-architecture
- prd
- kanban
- claude-code
- workflow

---

# Full Walkthrough: Workflow for AI Coding — Matt Pocock

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

- Software-engineering fundamentals (small tasks, deep modules, TDD, vertical slices, alignment) are *more* valuable in the AI age, not less; they’re the load-bearing primitives of an agent workflow.
- LLMs have a "smart zone" and a "dumb zone." The smart zone is roughly the first ~100K tokens of any context window, regardless of the advertised maximum (200K vs. 1M). Beyond that, decisions degrade.
- LLMs behave like the protagonist of *Memento*: every cleared session resets to the same starting state. Pocock prefers `/clear` over `/compact`; compaction creates "sediment" that drifts further from a clean baseline on each cycle.
- The system prompt + always-loaded context (CLAUDE.md, etc.) should be kept tiny. Stuffing 250K of standing instructions starts the agent in the dumb zone before it does any work.
- Reject "specs-to-code" as a paradigm. Code is the battleground; you must keep your hands on it. Spec → AI → code → never look at code → loop is just vibe coding.
- The right early goal is *alignment / shared design concept* (Brooks, *The Design of Design*), not a written plan. Pocock’s `grill-me` skill interrogates the user one question at a time until alignment is reached.
- Two task categories: **human-in-the-loop** (idea, grilling, PRD, kanban planning, QA) and **AFK** (implementation). Planning must stay human-in-the-loop; implementation can be delegated.
- Workflow stages: idea → grill-me → PRD (destination doc) → kanban of vertical-slice issues (journey doc) → AFK Ralph-style loop → QA → code review → team review.
- "Tracer bullet" / vertical-slice issues (Hunt & Thomas, *The Pragmatic Programmer*) beat horizontal layered phases because the agent gets near-instant end-to-end feedback during phase 1 instead of waiting until phase 3.
- A kanban with explicit blocking edges enables parallelization across agents (DAG of tickets). Sequential multi-phase plans bottleneck onto a single agent.
- "Ralph Wiggum loop" (after Dex Horthy / Human Layer): a simple loop that repeatedly tells an agent to make one small change toward a PRD-defined destination. Pocock prefers a slightly more structured kanban variant.
- TDD (red → green → refactor) is essential for AFK runs. Agents tend to cheat at tests written *after* implementation; instrumenting the test first makes cheating much harder and produces better tests.
- Feedback loops (typecheck, tests, lint) are the *ceiling* of AI quality in your codebase. Bad feedback loops → bad AI output, full stop.
- Codebase architecture matters more, not less. Ousterhout’s *A Philosophy of Software Design* deep-vs-shallow modules: agents thrive in deep modules with small interfaces and rich internals because they enable big, meaningful test boundaries.
- Push vs. pull for coding standards: implementer should *pull* (skills/docs available on demand); reviewer should *push* (standards forcibly injected so review compares code against them).
- Documentation rot: keep PRDs/issues out of the live repo after completion (Pocock closes GitHub issues rather than letting old PRDs misdirect future agents).
- Use a separate review pass in a *fresh* context so review happens in the smart zone, not in the implementation’s already-degraded dumb zone.
- Pocock’s tool: **Sandcastle**, a TypeScript library for spawning sandboxed (Docker + git worktree) parallel agent runs with planner/implementer/reviewer/merger roles.
- Heuristic role split that worked for him: Sonnet for implementation, Opus for review.
- The hardest unsolved problem in this workflow is code-review volume: AFK agents produce more diff than humans can comfortably review; PR-size discipline conflicts with multi-issue Ralph loops.

## One-Sentence Thesis

Effective AI-assisted software engineering is mostly classical software engineering — alignment, small tasks, vertical slices, deep modules, TDD, and tight feedback loops — applied with explicit awareness that LLMs have a finite smart zone and a *Memento*-like memory.

## Core Concepts

### Smart zone vs. dumb zone

- **Explanation:** Within an LLM’s context window, decision quality is high in roughly the first ~100K tokens and degrades thereafter, because attention relationships scale quadratically with token count.
- **Why it matters:** Sets a hard upper bound on per-task complexity and forces task-sizing discipline.
- **Related concepts:** Context-window management, compaction, `/clear`, system-prompt minimalism.
- **Prerequisites:** Awareness of the agent’s current token usage (status line).

### LLM as Memento protagonist

- **Explanation:** Every cleared session restarts from the same blank base state. The agent has no persistent memory across sessions unless you give it one.
- **Why it matters:** Encourages designing workflows that can be safely *reset* rather than ones that hoard accumulated context.
- **Related concepts:** Stateless agents, durable artifacts (PRDs, issues), `/clear` over `/compact`.

### `/clear` vs. `/compact`

- **Explanation:** `/clear` returns to the system prompt baseline; `/compact` summarizes the prior session into the new context, leaving "sediment."
- **Why it matters:** Compaction drifts further from clean state each cycle; clear preserves a known-good starting point.

### Specs-to-code (and why Pocock rejects it)

- **Explanation:** A workflow where humans only edit specs, AI generates code, and code is never directly inspected.
- **Why it matters:** Pocock argues code is the battleground; without inspecting it you cannot shape architecture or catch drift. He calls it "vibe coding by another name."

### Alignment / shared design concept

- **Explanation:** Borrowed from Brooks: when collaborators converge on a shared mental model of what they’re building. Pocock claims this — not a written plan — is the real prerequisite to good agent work.
- **Why it matters:** Once aligned, you don’t need to read the agent’s plans/PRDs to trust them, because you’re on the same wavelength.
- **Related concepts:** Grill-me skill, PRD-as-summary, "I don’t read the PRD."

### Human-in-the-loop vs. AFK tasks

- **Explanation:** Some work (alignment, planning, QA) requires a human present each step; some (implementation against well-specified issues) can run unattended.
- **Why it matters:** Determines where to spend human time and what to delegate to long-running loops.

### Tracer bullets / vertical slices

- **Explanation:** From Hunt & Thomas: a thin end-to-end slice through all layers (DB → service → API → UI) that produces visible, testable behavior.
- **Why it matters:** Forces early integration feedback. Horizontal layer-by-layer plans only become testable in the final phase.
- **Related concepts:** Kanban tickets, vertical slice rules.

### Deep vs. shallow modules

- **Explanation:** From Ousterhout: deep modules expose small interfaces but contain rich functionality; shallow modules are many tiny files with sprawling cross-dependencies.
- **Why it matters:** Deep modules give big, meaningful test boundaries — exactly what agents need for tight feedback loops. Shallow codebases produce shallow tests and shallow agent output.

### Push vs. pull context delivery

- **Explanation:** Push = always-injected tokens (CLAUDE.md, system prompt). Pull = available on demand (skills, docs the agent fetches if needed).
- **Why it matters:** Implementers benefit from pull (cheap context, fetched only when relevant); reviewers benefit from push (standards forcibly present so review compares against them).

### Documentation rot

- **Explanation:** Old PRDs and plans left in the repo drift from current code and mislead future agents.
- **Why it matters:** Pocock prefers external (closed GitHub issues) or deleted artifacts post-completion.

### The kanban-DAG of issues

- **Explanation:** Replace sequential multi-phase plans with independently grabbable issues that declare blocking relationships, forming a DAG.
- **Why it matters:** Enables parallel agents; sequential plans can only run one agent at a time.

## Workflows and Methods

### `grill-me` skill

- **Purpose:** Reach alignment / shared design concept between human and agent before any planning artifact exists.
- **When to use:** At the start of any non-trivial feature, especially when the input is a vague client/Slack brief.
- **Inputs:** A short brief (e.g., a Slack message), the codebase as exploration target.
- **Steps:** Agent explores codebase via sub-agent → asks one question at a time, each with a recommended answer → continues until shared understanding (can be 20–100 questions).
- **Outputs:** A long Q&A history living in the conversation that captures alignment.
- **Benefits:** Surfaces decisions the human/client never considered (e.g., retroactive backfill); produces a high-fidelity design concept cheaply.
- **Tradeoffs:** Slow; requires sustained human attention. Cannot be looped.
- **Failure modes:** Agent over-grills (40–100 questions); skill can be tuned to stop earlier.
- **Validation idea:** Compare downstream rework on features built with vs. without grilling.

### `write-a-PRD` skill

- **Purpose:** Summarize the alignment into a destination document — problem, solution, user stories, implementation decisions, testing decisions, **out-of-scope** items, proposed module map.
- **When to use:** After grilling.
- **Inputs:** Grill-me conversation history + repo context.
- **Steps:** Re-explore repo → second short interview round → fill PRD template → propose modules to modify.
- **Outputs:** A markdown PRD (Pocock keeps issues local; production setup uses GitHub issues).
- **Benefits:** Single durable artifact capturing destination + scope.
- **Tradeoffs:** Pocock explicitly does *not* read the PRD — he trusts the alignment. Counter-intuitive and requires confidence in the grill-me step.
- **Failure modes:** Without prior alignment, the PRD becomes the only artifact and inherits any misunderstanding.

### `prd-to-issues` skill (vertical-slice kanban)

- **Purpose:** Decompose the PRD into independently grabbable issues with explicit blocking edges and AFK/human-in-loop tags.
- **When to use:** After PRD is written.
- **Inputs:** PRD, repo, vertical-slice rules.
- **Steps:** Locate PRD → re-explore → draft vertical slices → user quiz → emit one markdown file per issue.
- **Outputs:** A set of issue files forming a DAG (kanban board).
- **Benefits:** Each ticket produces something visible; parallelizable; matches agent attention budget.
- **Tradeoffs:** Agents default to *horizontal* slices; you must push back ("first slice is too horizontal") to force vertical.
- **Failure modes:** Tickets too coarse → exceeds smart zone; too fine → integration overhead dominates.

### Ralph loop (sequential AFK implementation)

- **Purpose:** Run a single agent that picks the next available issue, implements it via TDD, runs feedback loops, and commits.
- **When to use:** Once a backlog of well-specified issues exists.
- **Inputs:** All issue files (catted into a bash variable), last 5 commits, the Ralph prompt.
- **Steps:** Exit if no AFK tasks remain → prioritize (critical bug fixes → infra → tracer bullets → polish/refactors) → explore repo → TDD red/green → run feedback loops (typecheck, tests) → commit.
- **Outputs:** Commits on a branch, one issue closed per loop iteration.
- **Benefits:** Genuinely AFK; produces a written summary on completion.
- **Tradeoffs:** Sequential — only one issue in flight.
- **Failure modes:** Bad feedback loops cap output quality; without TDD, agent cheats at post-hoc tests.

### Sandcastle parallel loop

- **Purpose:** Parallelize implementation across multiple sandboxed agents.
- **When to use:** Mature backlog with many independent tickets.
- **Inputs:** Backlog of issues, planner prompt, implementer prompt, reviewer prompt, merger prompt.
- **Steps:** Planner picks N parallelizable issues → for each: spawn Docker sandbox + git worktree → implement → review (fresh context, Opus) → merger agent merges branches and resolves typecheck/test conflicts.
- **Outputs:** Merged branch with all parallel work integrated.
- **Benefits:** Parallel throughput; reviewer runs in smart zone.
- **Tradeoffs:** Operational complexity (Docker, worktrees); merge conflicts on shared modules.

### `improve-codebase-architecture` skill

- **Purpose:** Scan the repo for opportunities to deepen modules / consolidate test boundaries.
- **When to use:** Before any new feature work, or whenever AI output quality is poor in a given area.
- **Inputs:** The repo.
- **Steps:** Architectural scan → cluster related modules → propose deepening candidates with coupling rationale and dependency category.
- **Outputs:** A list of refactor proposals, ranked by impact (e.g., "biggest test gap").
- **Benefits:** Pocock’s strongest single recommendation: "if you take one thing away, run this on your repo."
- **Tradeoffs:** Refactors are risky; need their own grilling/PRD/issue treatment.

### Automated review in a fresh context

- **Purpose:** Have an agent review code in the smart zone, not the dumb zone.
- **When to use:** After every implementation, before human QA.
- **Steps:** `/clear` → push coding standards into reviewer context → review the diff.
- **Benefits:** Catches bugs cheaply (tokens are cheap, AI is good at review); separates review smarts from implementation smarts.

## Tools, Libraries, and Frameworks

| Name                             | Type                                             | Purpose                                                                                           | Mentioned context                                                                                                      | Link                                                                     |
| -------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Claude Code                      | CLI coding agent                                 | Primary agent used in workshop                                                                    | Pocock’s default ("worst apart from all the others"); demonstrated `/clear`, `/compact`, plan mode, skills, sub-agents | https://claude.com/product/claude-code                                   |
| Cadence                          | Demo app                                         | Course management/CMS used as the workshop codebase                                               | Built by Pocock; has services for quiz/team/user/coupon/course                                                         | (workshop repo)                                                          |
| Course Video Manager             | Production app                                   | Pocock’s real workflow repo                                                                       | Real-world example of the issue-driven workflow (744 closed issues)                                                    | https://github.com/mattpocock/course-video-manager (path stated in talk) |
| Sandcastle                       | TypeScript library                               | Run parallel agents in Docker + git worktree sandboxes; planner/implementer/reviewer/merger roles | Pocock built it after dissatisfaction with existing AFK runners                                                        | (mentioned by name; URL not stated)                                      |
| AI Hero                          | Pocock’s site / course                           | Source of supporting articles (e.g., status line tokens)                                          | Referenced for token-display tip                                                                                       | https://aihero.dev (inferred from "AI Hero on my website")               |
| TLDraw                           | Whiteboard tool                                  | Pocock’s "slide deck" — infinite canvas for diagramming live                                      | Used throughout the talk                                                                                               | https://www.tldraw.com                                                   |
| GitHub Issues                    | Issue tracker                                    | Production target for prd-to-issues                                                               | Pocock’s real setup uses GitHub issues; demo uses local markdown files                                                 | https://github.com/features/issues                                       |
| Slido                            | Audience Q&A                                     | Live Q&A during workshop                                                                          | Used to crowdsource and vote on questions                                                                              | https://www.slido.com                                                    |
| Docker                           | Sandboxing                                       | Isolation for parallel agent runs in Sandcastle                                                   | Required for Sandcastle                                                                                                | https://www.docker.com                                                   |
| git worktree                     | Git feature                                      | Branch-per-agent isolation                                                                        | Used inside Sandcastle                                                                                                 | (built into git)                                                         |
| Opus / Sonnet                    | Anthropic models                                 | Implementation vs. review role split                                                              | "Sonnet for implementation, Opus for reviewing"                                                                        | https://www.anthropic.com/claude                                         |
| `npx tsx`                        | TypeScript runner                                | Ad-hoc TS execution permitted to the agent                                                        | Used in Cadence for tests                                                                                              | https://github.com/privatenumber/tsx                                     |
| Playwright MCP / Agent Browser   | Browser automation MCP                           | Giving agents eyes on the front end                                                               | Pocock: tried it, "not very good at that yet"                                                                          | https://github.com/microsoft/playwright                                  |
| Beads                            | Issue/kanban framework (Steve Yegge / community) | Alternative to Pocock’s prd-to-issues approach                                                    | Asked about; Pocock hadn’t tested it                                                                                   | (mentioned by name)                                                      |
| Spec Kit / OpenSpec / Taskmaster | Spec-driven planning frameworks                  | Alternatives to grill-me                                                                          | Pocock prefers owning the stack over adopting these                                                                    | (mentioned by name)                                                      |
| CLAUDE.md                        | Per-repo agent config                            | Standing instructions to Claude Code                                                              | Demoed adding "sacrifice grammar for concision" — later dropped                                                        | https://docs.claude.com/en/docs/claude-code/memory                       |
| Plan Mode (Claude Code)          | Agent mode                                       | Read-only planning before execution                                                               | Pocock finds it overeager; prefers grill-me                                                                            | https://docs.claude.com/en/docs/claude-code                              |

## Tradeoffs and Failure Modes

- **Smart-zone exhaustion:** Long sessions, oversized system prompts, or aggressive `/compact` push the agent into the dumb zone with no warning beyond degraded decisions.
- **Compaction sediment:** Each compaction cycle drifts further from a clean baseline; the only deterministic state is `/clear`.
- **Specs-to-code drift:** Ignoring the code in favor of editing specs hides architectural decay.
- **Horizontal slicing:** Default agent behavior; produces no end-to-end feedback until the last phase. Must be actively corrected.
- **Sequential plans:** Numbered phases can only be picked up by a single agent — kills parallelism.
- **Doc rot:** PRDs persisted in-repo can mislead future agents months later as code drifts from spec.
- **Over-grilling:** Skill may ask 40–100 questions; needs tuning when fatigue dominates.
- **Tests written after implementation:** Agent can cheat by tailoring tests to the code it just wrote; TDD red-first prevents this.
- **Bad feedback loops cap AI quality:** No amount of prompting fixes a codebase whose tests/typecheck don’t reliably catch regressions.
- **Shallow-module sprawl:** Unsupervised agents tend to produce many tiny modules that are individually mocked and untested as a system.
- **PR review volume:** AFK loops produce more diff than humans can review well; conflicts with "small PRs" discipline. Pocock acknowledges no clean answer.
- **Front-end QA:** Agents lack reliable visual perception; current MCP browser tools "not good enough yet" for mature UIs.
- **Pre-cooked planning frameworks:** Adopting Spec Kit / OpenSpec / Taskmaster wholesale removes observability over your own stack; when it breaks you can’t fix it.
- **1M-token context windows:** Per Pocock, the smart zone didn’t grow proportionally — they "shipped a lot more dumb zone." Useful for retrieval, not for coding.
- **Autonomy-induced codebase amnesia:** Devs delegating heavily lose mental model of the codebase; Pocock’s deep-modules-with-delegated-internals is his proposed mitigation.

## Claims Made By Speaker

| Claim                                                                                                                                              | Evidence / context                                                                  | Confidence                      | Needs validation?                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------------ |
| Smart zone is roughly 100K tokens regardless of advertised window                                                                                  | Personal experience; presented as rule of thumb                                     | Speaker high; objectively low   | Yes — empirical eval needed                      |
| 1M-token Claude Code release was "more dumb zone, not more smart zone"                                                                             | Anecdote from launching his Claude Code course the same day                         | Speaker high; objectively low   | Yes — coding-task benchmark across context sizes |
| Compaction degrades quality; clearing is preferable                                                                                                | Architectural reasoning + experience                                                | Speaker medium-high             | Yes — A/B compare task completion                |
| Grilling produces alignment such that PRD review is unnecessary                                                                                    | Pocock’s personal practice                                                          | Speaker high; idiosyncratic     | Yes — others may not skip PRD review safely      |
| Vertical slices outperform horizontal phases for AI work                                                                                           | Pragmatic Programmer principle, applied to agents                                   | Speaker high                    | Plausible; partial validation needed             |
| Deep modules dramatically improve agent output quality                                                                                             | Anecdote: video editor became tractable after wrapping FE+BE in one testable module | Speaker high                    | Yes — measure defect/throughput delta            |
| TDD makes agents cheat less on tests                                                                                                               | Direct observation across many runs                                                 | Speaker high                    | Plausible; easy to test                          |
| Reviewer in fresh context catches more bugs than same-session review                                                                               | Smart-zone reasoning                                                                | Speaker high                    | Easy to test                                     |
| Sonnet-implements + Opus-reviews is a good role split                                                                                              | Pocock’s current setup                                                              | Speaker medium                  | Yes — depends on cost/quality tradeoff           |
| AFK agents produce more code than humans can review                                                                                                | Stated directly; "I don’t honestly know what the answer is"                         | Speaker high; openly unresolved | Yes — open problem                               |
| MCP browser tools insufficient for mature front-end QA                                                                                             | Personal experience                                                                 | Speaker medium                  | Yes — capability is moving fast                  |
| Pre-AI software engineering books (Pragmatic Programmer, Mythical Man-Month, Philosophy of Software Design, Design of Design) are gold for prompts | Repeatedly cited; closing recommendation                                            | Speaker high                    | Anecdotal but plausible                          |
| Owning your planning stack beats adopting Spec Kit / OpenSpec / Taskmaster wholesale                                                               | Argued via observability of failure modes                                           | Speaker high; opinionated       | Reasonable but contested                         |
| Pair / mob programming with AI as the third participant works well                                                                                 | Stated as recommendation                                                            | Speaker medium                  | Plausible                                        |

## Relevance To AI Coding Workflow

### Idea → Plan

- Use grill-me to convert a vague brief into a shared design concept.
- Loop in domain experts and teammates while still human-in-the-loop.
- Build throwaway prototypes for ambiguous front-end or third-party-integration questions before committing to a PRD.

### Plan → Code

- Convert PRD into a kanban-DAG of vertical-slice issues; tag each as AFK or human-in-loop.
- Reject the first horizontal-slice proposal explicitly.
- Pre-declare the module map (deep modules) inside the PRD/issues so the agent doesn’t fragment the codebase.

### Code → Test

- TDD red-first via Ralph loop; agent writes failing test → confirms red → implements → confirms green.
- Wrap each issue in a single deep-module test boundary, not per-function unit tests.
- Run typecheck and full test suite as feedback loops in every iteration.

### Test → Deploy

- Each tracer-bullet issue produces something deployable/observable end-to-end.
- Use Sandcastle (or equivalent) for parallel branches; merger agent handles integration conflicts.

### Review / Debug

- Always run automated review in a fresh context (push standards to reviewer; pull from implementer).
- Use a stronger model (Opus) for review than for implementation (Sonnet).
- Manual QA is non-negotiable — it’s how the human reasserts taste and surfaces new tickets back into the kanban.

## Detailed Timestamped Notes

- **0:07–0:52** Intro. ~2-hour workshop. Live link to exercises repo. Live-streamed to Gilgud room.
- **0:52–1:38** Thesis: AI is a new paradigm, but classical SWE fundamentals matter *more*, not less.
- **1:38–2:30** Audience polls (coded with AI; coded daily; been frustrated). Q&A via Slido (Pocock dislikes mic Q&A as undemocratic).
- **2:30–4:17** **Smart zone vs. dumb zone.** Credit to Dex Horthy (Human Layer). Quadratic scaling of attention. ~100K is the practical smart-zone marker regardless of total window.
- **4:17–5:00** Task sizing analogy back to Fowler (*Refactoring*) and *Pragmatic Programmer*: don’t bite off more than you can chew.
- **5:00–6:13** Naive solution: keep going + compact. Pocock dislikes due to sediment. Multi-phase plans introduced.
- **6:13–7:24** **Ralph Wiggum loop**: PRD as destination + tight loop of small changes. Pocock prefers more structure than raw Ralph.
- **7:24–8:48** **LLMs are like the *Memento* protagonist.** Diagram of session phases: system prompt (gray, keep small) → exploratory (blue) → implementation → testing. `/clear` resets to system prompt baseline.
- **8:48–10:53** Live demo of compaction in Claude Code. Status line shows token count — Pocock: "absolutely essential." Article on AI Hero.
- **10:53–11:12** Recap of the two LLM constraints: smart/dumb zone + Memento memory.
- **11:12–14:00** **Exercise 1**: workshop repo Cadence. `clientbrief.md` is a Slack message from Sarah Chen asking for gamification to fix retention.
- **14:00–14:46** Argument against the "specs-to-code" movement: ignoring the code is just vibe coding under a new name.
- **14:46–17:30** **`grill-me` skill** introduced. Skill body: "Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies one by one. For each question, provide your recommended answer. Ask the questions one at a time."
- **17:30–18:30** Brooks’ *Design of Design*: shared design concept. Pocock’s realization: he didn’t need a plan, he needed alignment.
- **18:30–20:30** Live grilling: points economy (lessons vs. quizzes vs. videos), retroactive backfill (room vote, Pocock takes the recommendation). Sub-agent burned 93.7K tokens but only added a small delta to main context — sub-agents are isolated context windows that summarize back.
- **20:30–22:00** Grilling can run 40–100 questions; can also be fed meeting transcripts for domain validation.
- **22:00–28:30** Q&A: alternatives to grill-me (Spec Kit / OpenSpec / Taskmaster) — Pocock prefers owning the stack. Pair/mob programming with AI as third participant. The `ask_user_question` tool UI is "broken in a ton of ways."
- **28:30–31:00** Two-document model: **destination** (PRD) and **journey** (kanban). Both needed.
- **31:00–34:00** **`write-a-PRD` skill**. Template includes problem, solution, user stories, implementation decisions, testing decisions, **out-of-scope**, proposed module map. Production setup uses GitHub issues; demo uses local markdown. Pocock’s real repo (course-video-manager) has 744 closed issues.
- **34:00–36:00** **Pocock does not read the PRD.** Rationale: alignment was achieved in grilling; LLMs are good at summarization; reading is not a meaningful failure-mode test at this point.
- **36:00–38:30** Q&A: "If you don’t like Claude Code, what?" — Churchill quote about democracy. Bad codebases produce bad agents. 1M-token release: "they shipped you a lot more dumb zone." Smart zone ~100K still.
- **38:30–39:35** Five-minute break.
- **39:35–42:00** **Kanban over multi-phase plans.** Live: PRD-to-issues produced 5 tickets with blocking edges and AFK tags. DAG enables parallelization; numbered phases do not.
- **42:00–45:00** **Tracer bullets / vertical slices.** History from *Pragmatic Programmer*. Agents default to horizontal slicing; must be corrected. Vertical slice rules in `prd-to-issues` skill.
- **45:00–47:00** Live correction: "first slice is too horizontal." Agent revises to "Award points for lesson completion visible on dashboard."
- **47:00–50:00** Q&A: parallelization (covered later via Sandcastle). Code review volume problem — openly unresolved. Front-end multimodal limits — agents lack good vision tools.
- **50:00–52:30** DAG → phased parallel execution: phase 1 unblocks phase 2 (parallel) which unblocks phase 3.
- **52:30–55:30** **AFK Ralph loop** demoed. `once.sh`: `cat issues/*.md` into a variable, `git log -5`, run `claude` with `--permission-mode=acceptEdits`. AFK version is more complex, runs in Docker.
- **55:30–57:30** Ralph prompt structure: exit if no AFK tasks; pick next by priority (critical bugs → infra → tracer bullets → polish/refactors); explore → TDD → feedback loops.
- **57:30–58:50** Q&A: out-of-scope retention is in the PRD’s "out of scope" section. Front-end workflow deferred.
- **58:50–60:30** Code-review-volume question. Pocock: "we just need to be ready to be doing more code review… that’s not a fun thing to say."
- **60:30–63:00** Team workflow question. Idea → research → prototype → grilling → PRD is *team* work; implementation is the AFK shift.
- **63:00–64:00** Front-end prototypes: ask the agent for 3 throwaway variants, choose, feed back into grilling.
- **64:00–65:30** Architecture/security constraints question — answered later via deep modules + push/pull.
- **65:30–67:00** **Reviewer in fresh context.** Diagram: implementer in smart zone uses up budget → reviewing same context happens in dumb zone. `/clear` first, then review, gets you back to smart zone.
- **67:00–68:30** **TDD red/green/refactor** skill. Agents tend to cheat at post-hoc tests; TDD instruments first.
- **68:30–69:35** Break.
- **69:35–71:30** Implementation results: 284 tests, single typecheck error fixed by agent.
- **71:30–73:30** Live QA: agent created a `point_events` table the schema didn’t have; runs migrations. Pocock: human QA is where you reassert taste; full automation produces slop.
- **73:30–75:30** **Bad codebases produce bad agents.** Question: how to fix?
- **75:30–78:00** **Ousterhout deep vs. shallow modules.** Shallow = many small files, ambiguous test boundaries. Deep = small interface, rich internals, one big meaningful test boundary.
- **78:00–80:00** PRD module map: explicit deep-module declarations for new and modified services.
- **80:00–81:30** Mental trick: design the *interface*, delegate the *implementation*. Modules become gray boxes — preserves human mental model while delegating volume.
- **81:30–84:00** **`improve-codebase-architecture` skill.** Live run on Cadence; finds quiz scoring service has zero tests. Anecdote: video editor in his real app — wrapping FE+BE in one big testable module via discriminated union was "night and day."
- **84:00–86:30** Q&A: docrot — Pocock closes GitHub issues rather than persist PRDs in-repo. Beads framework mentioned but untested.
- **86:30–88:00** Database migrations question — Pocock declines to answer cleanly.
- **88:00–89:30** PRD optimization question. Pocock: don’t over-optimize the PRD; the value is alignment, not the artifact.
- **89:30–93:00** **Push vs. pull.** Implementer pulls (skills); reviewer pushes (standards). Diagram.
- **93:00–95:30** **Sandcastle** walkthrough: TypeScript library; planner picks N parallelizable issues; implementer per sandbox (Docker + git worktree); reviewer (fresh context, Opus); merger resolves conflicts. Sonnet for implement, Opus for review.
- **95:30–96:29** Wrap-up: workflow summary diagram. Closing recommendation: buy old SWE books on Amazon.

## Open Questions

- Empirically, where does the smart zone actually end across current models? Is 100K a stable rule or already obsolete?
- How do we reconcile small-PR discipline with multi-issue Ralph loops? Pocock has no clean answer.
- How should team review work when a single dev’s AFK agent can produce a week’s worth of diff overnight?
- What’s the right policy on persisting PRDs/issues — repo-resident vs. external tracker vs. delete-on-close?
- How well do Sandcastle-style merger agents actually handle non-trivial semantic merge conflicts?
- Does the "don’t read the PRD" stance generalize beyond solo / domain-expert authors? What’s the failure rate for newer engineers?
- Best practices for front-end / multimodal QA — is browser MCP catching up, or is human-in-the-loop still required?
- How to teach the "vertical slice" reflex to agents reliably without per-task correction?
- Where exactly should standards live: CLAUDE.md (push), skills (pull), reviewer prompt (push)? Pocock gives a heuristic but no taxonomy.
- Can grill-me be partially looped without losing the alignment property?

## Experiments To Try

### Run `improve-codebase-architecture` on your worst repo

- **Hypothesis:** Deepening 1–2 modules will measurably improve agent output quality in that area.
- **Context:** Any codebase where AI assistance feels poor.
- **What to try:** Run the skill, pick the top recommendation, refactor under TDD, then re-attempt a previously-failed agent task.
- **Expected benefit:** Higher first-pass success rate on AFK loops.
- **Risk:** Refactor introduces regressions.
- **Measurement:** AFK loop success rate before/after on N similar tickets.

### A/B `/clear` vs. `/compact`

- **Hypothesis:** Cleared sessions produce better decisions than compacted ones at equal "effective" context.
- **What to try:** Same task, two sessions; one uses compaction at 80% window, one clears + reloads issue file.
- **Measurement:** Independent rubric on output quality, count of regressions.

### TDD-first vs. implementation-first

- **Hypothesis:** TDD-first runs produce tests that catch real regressions; post-hoc runs produce tests that mirror the code.
- **What to try:** Mutation testing on the resulting test suites.
- **Measurement:** Mutation score.

### Sonnet-implements + Opus-reviews vs. single-model

- **Hypothesis:** Two-model split improves bug catch rate per dollar.
- **Measurement:** Bugs found per $ of token spend; comparable PR-pass rates.

### Vertical-slice-only kanban

- **Hypothesis:** Banning horizontal slices shortens cycle time to first deployable change.
- **Measurement:** Time from issue creation to a green merge containing visible end-to-end behavior.

### Grill-me without reading the PRD

- **Hypothesis:** Skipping PRD review does not increase rework, *if* grilling reached alignment.
- **What to try:** For a small feature, grill thoroughly, then ship without reading the PRD; track rework.
- **Risk:** If alignment was incomplete, downstream rework spikes.

### Push-pull standards split

- **Hypothesis:** Coding-standards adherence is highest when standards are pushed to the reviewer and pulled by the implementer.
- **What to try:** Three configs (push-both, pull-both, split). Same prompt, same task.
- **Measurement:** Lint/style compliance + reviewer catch rate.

### Sandcastle on a real backlog

- **Hypothesis:** 3-way parallelization produces >2× throughput vs. sequential Ralph.
- **Measurement:** Tickets closed per hour, conflict rate, manual fixup time.

## My Current Assessment

### Plausible

- Smart-zone-as-finite-budget framing.
- Grilling > free-form planning for alignment.
- Vertical slices > horizontal phases for agent feedback.
- Deep modules > shallow modules for testability and agent traction.
- TDD reduces test-cheating.
- Reviewer-in-fresh-context catches more.
- Bad feedback loops cap AI quality.

### Possibly hype

- The exact 100K smart-zone number — likely model- and task-dependent; presented as universal.
- "Don’t read the PRD" — works for Pocock, may not generalize.
- Sandcastle-style merging at scale — operational complexity may eat the wins.
- "Old books are gold" — true in spirit; risks over-romanticizing.

### Needs testing

- Push-vs-pull taxonomy.
- Multi-model role split economics (Sonnet/Opus).
- Whether deep-module refactoring actually moves the needle on AI output, or whether it just produces a tidier codebase that’s easier for humans.

### Useful later

- The grill-me / PRD / kanban / Ralph / review pipeline as a *defaultable workflow* for any non-trivial feature.
- The "design interface, delegate implementation" mental trick to fight codebase amnesia.
- The kanban-as-DAG framing for scaling beyond a single agent.

## Transcript Information

- **Transcript source:** Provided alongside the prompt; YouTube auto-style transcript with timestamps every few seconds.
- **Transcript quality:** Good for content; minor noise (filler words, "snorts", music markers, occasional ASR errors — e.g., "John Alistster" for *John Ousterhout*, "John Asterhout"). Light editorial cleanup applied in notes.
- **Transcript file:** Inline in the prompt.
- **Description file:** Inline in the prompt.
- **Metadata file:** Inline in the prompt.
- **Extraction date:** 2026-05-09.
- **Chapters:** None provided; section breaks in detailed notes are inferred from the transcript content.

## References

### Explicitly Mentioned References

#### GitHub Repositories

- **mattpocock/course-video-manager** — Pocock’s real workflow repo, cited as having 744 closed issues; reference example for the issue-driven setup. Timestamp ~33:30. URL stated in talk: `github.com/mattpocock/course-video-manager`.
- **Workshop exercises repo (Cadence demo + skills)** — The repo cloned by attendees containing `clientbrief.md`, `grill-me`, `write-a-PRD`, `prd-to-issues`, `improve-codebase-architecture` skills, and `once.sh`. Timestamp 11:12. URL not stated; available via the workshop exercises link shown on stage.

#### Websites / Documentation

- **AI Hero (Pocock’s site)** — Source of the article on the Claude Code token status line. Timestamp ~9:45. URL: `aihero.dev` (inferred from "AI Hero on my website").
- **Slido** — Used for live audience Q&A. Timestamp throughout. URL: https://www.slido.com.
- **TLDraw** — Used as the live diagramming surface. Timestamp 7:38. URL: https://www.tldraw.com.
- **Claude Code documentation** — Implicit; commands `/clear`, `/compact`, plan mode, sub-agents, skills referenced throughout. URL: https://docs.claude.com/en/docs/claude-code.

#### Books

- *The Pragmatic Programmer* — Hunt & Thomas. Source of "tracer bullets" and small-task discipline. Timestamp ~42:00.
- *Refactoring* — Martin Fowler. "Don’t bite off more than you can chew." Timestamp ~4:46.
- *The Design of Design* — Frederick P. Brooks. Source of "shared design concept." Timestamp ~17:00.
- *A Philosophy of Software Design* — John Ousterhout (transcribed as "John Alistster"/"Asterhout"). Source of deep vs. shallow modules. Timestamp ~75:30.
- *The Mythical Man-Month* — Brooks. Mentioned implicitly as part of the "old books" recommendation set; closing remarks ~95:30.

#### Papers

- None explicitly cited.

#### Tutorials / Blog Posts / Courses

- **Pocock’s Claude Code course** — Mentioned as the context for his 200K-window experience and the 1M-window release. Timestamp ~37:46. (Hosted on AI Hero.)
- **Pocock’s AI Hero article on token status line** — Timestamp ~9:50.

#### Tools / Frameworks / APIs

- **Claude Code** (Anthropic) — Primary agent CLI. https://claude.com/product/claude-code.
- **Sandcastle** (Pocock) — TypeScript library for parallel sandboxed agent runs. Timestamp ~93:30.
- **Spec Kit** — Spec-driven planning framework. Timestamp ~23:30.
- **OpenSpec** — Spec-driven planning framework. Timestamp ~23:30.
- **Taskmaster** — Task-management framework for AI workflows. Timestamp ~23:30.
- **Beads** — Issue/kanban framework attributed to Steve (likely Steve Yegge). Timestamp ~85:00.
- **Playwright MCP / Agent Browser** — Browser automation MCPs Pocock tested for front-end QA. Timestamp ~63:00.
- **Docker** — Sandboxing for Sandcastle. Timestamp ~55:00.
- **git worktree** — Branch-per-agent isolation in Sandcastle. Timestamp ~93:30.
- **Opus / Sonnet** — Anthropic models, role split. Timestamp ~94:00.
- **`npx tsx`** — Used inside Cadence test runs. Timestamp ~68:00.
- **CLAUDE.md** — Per-repo Claude Code configuration. Timestamp ~48:00.

#### People / Channels / Companies

- **Matt Pocock** (@mattpocockuk) — Speaker. https://x.com/mattpocockuk.
- **Dex Horthy** — Founder of Human Layer; credited with smart-zone / dumb-zone framing. Timestamp 3:14.
- **Human Layer** — Dex Horthy’s company. Timestamp 3:14.
- **Frederick P. Brooks** — Author of *The Design of Design*, *The Mythical Man-Month*. Timestamp 17:00.
- **Martin Fowler** — Author of *Refactoring*. Timestamp 4:46.
- **Andy Hunt & Dave Thomas** — Authors of *The Pragmatic Programmer*. Timestamp 42:00.
- **John Ousterhout** — Author of *A Philosophy of Software Design*. Timestamp 75:30.
- **Sarah Chen** — Fictional client in the workshop brief. Timestamp 14:00.
- **Steve (Yegge, inferred)** — Attributed creator of the Beads framework; also acknowledged in-room ("Thank you, Steve" at 7:38). Timestamp ~85:00.
- **Anthropic** — Vendor of Claude Code, Opus, Sonnet. Throughout.
- **Mike** — Workshop organizer in the room. Timestamp throughout.

### Related / Inferred References

- **Steve Yegge** *(inferred)* — Most prominent "Steve" associated with a Beads-like AI-agent framework circulating in 2026; identity not explicitly confirmed in the talk.
- **Anthropic Skills documentation** *(inferred)* — Mechanism behind `grill-me`, `write-a-PRD`, `prd-to-issues`, `improve-codebase-architecture`. URL: https://docs.claude.com/en/docs/claude-code/skills.
- **`claude --permission-mode=acceptEdits`** *(inferred from `once.sh` walkthrough)* — Claude Code flag enabling AFK runs.
- **Discriminated unions in TypeScript** *(inferred)* — The technique Pocock cites for unifying FE+BE in one testable module; standard TS feature.
- **Mutation testing tools (e.g., Stryker)** *(inferred)* — Natural way to validate the TDD-cheating claim experimentally.
- **Claude sub-agents documentation** *(inferred)* — Mechanism behind the "explore sub-agent" that burned 93.7K tokens in isolation. URL: https://docs.claude.com/en/docs/claude-code/sub-agents.
- **Git worktree documentation** *(inferred)* — Underpins Sandcastle’s parallel branch isolation. URL: https://git-scm.com/docs/git-worktree.
