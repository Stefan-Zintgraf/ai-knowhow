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
- ai-agents
- claude-code
- tdd
- software-design
- workflow

---

# Full Walkthrough: Workflow for AI Coding — Matt Pocock

## Table of Contents

- [Executive Summary](#executive-summary)
- [One-Sentence Thesis](#one-sentence-thesis)
- [Core Concepts](#core-concepts)
  - [LLM Smart Zone and Dumb Zone](#llm-smart-zone-and-dumb-zone)
  - [Session Lifecycle: System Prompt, Exploration, Implementation, Testing](#session-lifecycle-system-prompt-exploration-implementation-testing)
  - [Clearing Context Versus Compacting Context](#clearing-context-versus-compacting-context)
  - [Shared Design Concept](#shared-design-concept)
  - [Specs-to-Code Versus Code-Informed Planning](#specs-to-code-versus-code-informed-planning)
  - [PRD as Destination Document](#prd-as-destination-document)
  - [Issues / Kanban as Journey Document](#issues--kanban-as-journey-document)
  - [Tracer Bullets / Vertical Slices](#tracer-bullets--vertical-slices)
  - [Human-in-the-Loop Versus AFK Work](#human-in-the-loop-versus-afk-work)
  - [TDD as an Agent Feedback Mechanism](#tdd-as-an-agent-feedback-mechanism)
  - [Fresh-Context Automated Review](#fresh-context-automated-review)
  - [Deep Modules Versus Shallow Modules](#deep-modules-versus-shallow-modules)
  - [Module Interfaces as Cognitive Handles](#module-interfaces-as-cognitive-handles)
  - [Push Versus Pull Instructions](#push-versus-pull-instructions)
  - [Documentation Rot](#documentation-rot)
  - [Parallel Agent Orchestration](#parallel-agent-orchestration)
- [Workflows and Methods](#workflows-and-methods)
  - [Workflow 1: Ambiguous Brief to Grilled Design Concept](#workflow-1-ambiguous-brief-to-grilled-design-concept)
  - [Workflow 2: Grilled Design Concept to PRD](#workflow-2-grilled-design-concept-to-prd)
  - [Workflow 3: PRD to Vertical-Slice Issue DAG](#workflow-3-prd-to-vertical-slice-issue-dag)
  - [Workflow 4: Ralph Once Loop for Human-Observed Implementation](#workflow-4-ralph-once-loop-for-human-observed-implementation)
  - [Workflow 5: AFK Implementation Loop](#workflow-5-afk-implementation-loop)
  - [Workflow 6: Agentic TDD Red-Green-Refactor](#workflow-6-agentic-tdd-red-green-refactor)
  - [Workflow 7: Fresh-Context Automated Review](#workflow-7-fresh-context-automated-review)
  - [Workflow 8: Manual QA as Taste Preservation](#workflow-8-manual-qa-as-taste-preservation)
  - [Workflow 9: Deep-Module Architecture Improvement](#workflow-9-deep-module-architecture-improvement)
  - [Workflow 10: Parallel Agents with Planner, Implementers, Reviewers, and Merger](#workflow-10-parallel-agents-with-planner-implementers-reviewers-and-merger)
  - [Workflow 11: Front-End Prototype Route for Visual Decisions](#workflow-11-front-end-prototype-route-for-visual-decisions)
  - [Workflow 12: Coding Standards with Pull for Implementers and Push for Reviewers](#workflow-12-coding-standards-with-pull-for-implementers-and-push-for-reviewers)
- [Tools, Libraries, and Frameworks](#tools-libraries-and-frameworks)
- [Tradeoffs and Failure Modes](#tradeoffs-and-failure-modes)
- [Claims Made By Speaker](#claims-made-by-speaker)
- [Relevance To AI Coding Workflow](#relevance-to-ai-coding-workflow)
  - [Idea → Plan](#idea--plan)
  - [Plan → Code](#plan--code)
  - [Code → Test](#code--test)
  - [Test → Deploy](#test--deploy)
  - [Review / Debug](#review--debug)
- [Detailed Timestamped Notes](#detailed-timestamped-notes)
- [Open Questions](#open-questions)
- [Experiments To Try](#experiments-to-try)
- [My Current Assessment](#my-current-assessment)
- [Transcript Information](#transcript-information)
- [References](#references)

## Executive Summary

- Matt Pocock’s central claim is that AI coding feels like a new paradigm, but the highest-leverage practices are still classic software-engineering fundamentals: small tasks, good feedback loops, shared understanding, testability, modularity, and code review.
- He frames LLMs as having a “smart zone” and a “dumb zone”: early in a fresh context window, attention relationships are less strained and coding quality is higher; as the context accumulates tokens, decision quality degrades. His practical current threshold is roughly around 100k tokens, even when larger context windows exist.
- The workflow is designed to keep agents inside the smart zone by decomposing large work into small, independently grabbable tasks rather than letting one long conversation accumulate sediment.
- He prefers clearing context over compacting. Compacting summarizes prior conversation into a smaller history, but he argues it introduces sediment and variance; clearing returns the agent to the same base state every time.
- The first major workflow step is a “grill me” alignment session: the AI interviews the human relentlessly, one question at a time, and includes its recommended answer for each question. The goal is not a plan; the goal is a shared design concept.
- The “grill me” step is meant to reduce silent misalignment in ambiguous product work. In the demo, a vague Slack-style brief about gamification becomes a concrete set of decisions about points, streaks, retroactivity, levels, UI location, and scope.
- Pocock explicitly argues against pure “specs-to-code” workflows where the human only edits specs and ignores code. He says the code remains the battleground; humans still need to shape the codebase.
- After alignment, the conversation is converted into a PRD. The PRD is described as a “destination document”: it captures the desired end state, user stories, implementation decisions, testing decisions, and out-of-scope items.
- He says he often does not deeply review the PRD because, after a strong grilling session, he trusts the LLM’s summarization ability. This is a speaker practice, not a universally validated recommendation; it is a risk point in team settings.
- The PRD is then converted into a Kanban-style set of issues: the “journey document.” He prefers issue DAGs with blocking relationships over sequential multi-phase plans because issue DAGs can be parallelized across agents.
- The crucial decomposition technique is “tracer bullets” / vertical slices: each issue should ideally cross enough layers to produce an integrated, testable, reviewable result. He warns that AI tends to code horizontally by layer, such as database first, then API, then frontend, which delays useful feedback.
- The implementation stage is the first stage he wants to make AFK: after humans shape the destination and journey, agents can select AFK-labelled tasks, implement them, run tests/typechecks, commit, and report status.
- His simple “Ralph” loop passes local issue files, recent commits, and an implementation prompt into Claude Code. The loop asks the agent to pick the next unblocked AFK task, work with TDD, run feedback loops, and emit a sentinel when no tasks remain.
- TDD is presented as essential for agent reliability. The agent should write a failing test first, confirm red, implement the feature, then confirm green. Pocock argues this makes it harder for agents to cheat with weak tests because the tests precede the implementation.
- Feedback loops define the ceiling for agent output. If a codebase lacks reliable tests, typechecks, migrations, linting, or other automated feedback, the agent is effectively coding blind.
- He recommends automated review, but preferably in a fresh context. If the implementing context has already drifted into the dumb zone, asking the same context to review its own work produces a weaker review.
- Manual QA remains necessary because QA is where the human imposes taste, product judgment, and domain judgment. He treats fully automated idea-to-QA pipelines as likely to produce low-taste or broken “slop.”
- Codebase architecture strongly affects agent quality. “Bad codebases make bad agents.” He uses John Ousterhout’s deep-module idea: small simple interfaces with substantial hidden functionality are easier for agents and humans to understand and test than many shallow, interdependent modules.
- His preferred mental model for maintaining codebase understanding is to design and remember module interfaces, then delegate internal implementation details. The module interface becomes a cognitive handle that preserves the human’s map of the system.
- For coding standards, he distinguishes “push” and “pull.” Implementers should be able to pull standards when needed, but reviewers should have standards pushed into context so they can compare the diff against them.
- He warns against keeping PRDs and plans inside the repo indefinitely because outdated documentation can mislead future agents. His preferred alternative is to close GitHub issues so historical context remains accessible but visually marked as done.
- For parallelization, he demonstrates a TypeScript library called Sand Castle that creates git worktrees, sandboxes them in Docker, runs agents on separate issues, reviews their commits, and merges branches with a merger agent.
- The end-to-end workflow is: idea → grill/alignment → optional research/prototype → PRD destination → issue/Kanban journey → AFK agent implementation → automated review → manual QA → more issues if needed → team review/merge.

## One-Sentence Thesis

AI-assisted development works best when autonomous coding agents are constrained by classic engineering discipline: strong human alignment, small vertical slices, fresh contexts, TDD feedback loops, deep modules, explicit review, and codebase-aware planning.

## Core Concepts

### LLM Smart Zone and Dumb Zone

- **Explanation:** Pocock describes an LLM session as beginning in a “smart zone,” where the context is relatively clean and attention relationships are less strained. As tokens accumulate, the model moves toward a “dumb zone,” where it is more likely to make poor decisions.
- **Why it matters:** Coding tasks should be sized so that the agent can complete meaningful work before the context gets polluted or too large. The decomposition strategy exists largely to preserve agent quality.
- **Related concepts:** Context windows, attention, context rot, task slicing, subagents, compaction, clearing context.
- **Prerequisites:** Basic understanding of transformer context windows and coding-agent workflows.

### Session Lifecycle: System Prompt, Exploration, Implementation, Testing

- **Explanation:** He sketches a typical coding-agent session as: persistent system prompt → exploration of the codebase → implementation → testing/feedback loops. After clearing context, the session returns to the base system prompt.
- **Why it matters:** If this lifecycle is predictable, the workflow can be optimized around it. Keep the persistent context small, let exploration happen inside fresh sessions, and run implementation/testing before degradation.
- **Related concepts:** Agent orchestration, context budgeting, tool use, status line token reporting.
- **Prerequisites:** Familiarity with Claude Code or similar terminal-based coding agents.

### Clearing Context Versus Compacting Context

- **Explanation:** Compacting summarizes a long conversation into a smaller history. Clearing drops the history and returns to the base prompt.
- **Why it matters:** Pocock prefers clearing because it is deterministic: the next run starts from the same clean state. He dislikes compacting because compressed history can carry sediment, distortions, and stale decisions.
- **Related concepts:** Summarization, memory, state reset, context hygiene, long-running agent loops.
- **Prerequisites:** Awareness of how coding agents preserve or compress conversation history.

### Shared Design Concept

- **Explanation:** Borrowing from Frederick P. Brooks, Pocock says the goal of early planning is a shared design concept between the human and the AI, not merely a generated plan.
- **Why it matters:** A plan produced too early may look plausible while encoding misalignment. A shared design concept means the human and agent have resolved key assumptions together.
- **Related concepts:** Product requirements, design trees, pair programming, domain expert interviews, alignment.
- **Prerequisites:** Ability to reason about product requirements and system behavior before implementation.

### Specs-to-Code Versus Code-Informed Planning

- **Explanation:** “Specs-to-code” is described as a workflow where the human edits specs and lets AI generate code without directly shaping or understanding the code. Pocock argues this fails because the code remains the operational reality.
- **Why it matters:** The workflow keeps the codebase in view while planning. It asks what modules will be modified, how test boundaries should be drawn, and what architecture is implied.
- **Related concepts:** Vibe coding, PRDs, code review, codebase architecture, module maps.
- **Prerequisites:** Experience reading and shaping production code.

### PRD as Destination Document

- **Explanation:** The PRD captures where the project is going: problem, solution, user stories, implementation decisions, testing decisions, definition of done, and out-of-scope decisions.
- **Why it matters:** It turns an alignment conversation into a durable artifact that future agents can use without replaying the full conversation.
- **Related concepts:** Product requirements documents, user stories, definition of done, scope control.
- **Prerequisites:** Basic product planning and requirements writing.

### Issues / Kanban as Journey Document

- **Explanation:** The issue set describes the journey from current codebase to destination. Each issue is intended to be independently grabbable, with blocking relationships.
- **Why it matters:** An issue DAG can be parallelized; a sequential multi-phase plan usually cannot. Agents can select unblocked issues and work independently.
- **Related concepts:** Kanban, DAGs, GitHub Issues, blockers, backlog curation, agent task selection.
- **Prerequisites:** Familiarity with issue trackers and dependency graphs.

### Tracer Bullets / Vertical Slices

- **Explanation:** A tracer bullet is a thin slice through the system that produces feedback across layers. In software, a vertical slice touches database/schema, service/API, and UI enough to validate an integrated path.
- **Why it matters:** Agents tend to produce horizontal layer-by-layer plans, delaying integrated feedback until late. Vertical slices create earlier testable/reviewable increments.
- **Related concepts:** The Pragmatic Programmer, walking skeletons, thin slices, integration tests, feedback loops.
- **Prerequisites:** Understanding of layered architectures and incremental delivery.

### Human-in-the-Loop Versus AFK Work

- **Explanation:** Pocock distinguishes tasks that require human participation from tasks that can run “away from keyboard” (AFK). Planning/alignment is human-in-the-loop; implementation can often be AFK once issues are shaped.
- **Why it matters:** The human’s high-leverage role is not typing code; it is clarifying goals, designing boundaries, reviewing outputs, and applying taste. Agents can run the night shift.
- **Related concepts:** Autonomous agents, pair programming, mob programming, delegation, backlog design.
- **Prerequisites:** Ability to identify which decisions require domain/product/human judgment.

### TDD as an Agent Feedback Mechanism

- **Explanation:** The agent writes a failing test first, confirms the red state, implements code, then confirms green. This is classic red-green-refactor adapted to coding agents.
- **Why it matters:** Pocock claims TDD prevents agents from cheating with after-the-fact weak tests and gives agents tight feedback during implementation.
- **Related concepts:** Red-green-refactor, test-first development, typechecking, CI, service-level tests.
- **Prerequisites:** A codebase with meaningful test infrastructure and fast-enough feedback loops.

### Fresh-Context Automated Review

- **Explanation:** After implementation, clear context and run a separate review process rather than asking the same long-running agent to review itself.
- **Why it matters:** If implementation consumed much of the smart zone, the review would happen in a degraded context. Fresh-context review uses the smart zone for evaluation.
- **Related concepts:** Code review, self-review, separate reviewer agents, context budgeting.
- **Prerequisites:** Ability to generate diffs/commits and pass them to a new agent session.

### Deep Modules Versus Shallow Modules

- **Explanation:** Citing John Ousterhout, Pocock contrasts shallow modules with many exposed details against deep modules with small interfaces and substantial internal functionality.
- **Why it matters:** Deep modules are easier to test and easier for agents to navigate. Shallow modules create tangled dependencies and unclear test boundaries.
- **Related concepts:** A Philosophy of Software Design, encapsulation, module boundaries, service interfaces, test boundaries.
- **Prerequisites:** Software architecture and modular design experience.

### Module Interfaces as Cognitive Handles

- **Explanation:** The human designs and remembers the module interface but delegates internal implementation. The module becomes a gray box: understood by behavior and contract, not necessarily every internal line.
- **Why it matters:** This preserves the human’s map of the codebase while allowing agents to implement more volume than the human could manually inspect line-by-line.
- **Related concepts:** API design, contract tests, black-box testing, encapsulation.
- **Prerequisites:** Ability to define stable interfaces and behavioral expectations.

### Push Versus Pull Instructions

- **Explanation:** “Push” means always putting instructions into the agent context. “Pull” means making instructions available for the agent to retrieve when relevant, such as via skills.
- **Why it matters:** Implementers may not need every coding standard pushed into context, but reviewers should have standards pushed so they can compare the code against them.
- **Related concepts:** Skills, CLAUDE.md, coding standards, context budget, agent memory.
- **Prerequisites:** Understanding how coding agents discover repo instructions and skills.

### Documentation Rot

- **Explanation:** PRDs and plans can become stale after code evolves. If left in the repo, future agents may treat old documentation as authoritative and make bad decisions.
- **Why it matters:** Agent-visible documentation has operational consequences. Stale docs are not passive; they actively influence generation.
- **Related concepts:** Doc rot, historical issues, closed GitHub issues, source-of-truth management.
- **Prerequisites:** Experience maintaining documentation in evolving codebases.

### Parallel Agent Orchestration

- **Explanation:** A planner chooses unblocked issues; multiple implementer agents work in separate sandboxes/worktrees; reviewer agents review commits; a merger agent integrates branches and resolves conflicts.
- **Why it matters:** Parallelism turns the issue DAG into agent throughput. It also creates new risks: conflicts, review load, inconsistent architecture, and merge complexity.
- **Related concepts:** Git worktrees, Docker sandboxing, issue DAGs, autonomous agents, CI gates.
- **Prerequisites:** Git branching, isolation, test automation, and merge-conflict management.

## Workflows and Methods

### Workflow 1: Ambiguous Brief to Grilled Design Concept

- **Purpose:** Convert vague product intent into a shared design concept between human and agent.
- **When to use:** At the beginning of a feature, especially when the brief is underspecified, ambiguous, or comes from a stakeholder who is not currently available.
- **Inputs:**
  - Client brief, Slack message, meeting transcript, or product idea.
  - Existing codebase context.
  - “Grill me” skill or equivalent interview prompt.
- **Steps:**
  1. Clear the context before starting.
  2. Invoke the “grill me” skill with the brief.
  3. Let the agent explore the codebase if needed, preferably via subagent to avoid polluting parent context.
  4. Answer one question at a time.
  5. Use the agent’s recommended answers as defaults when they seem reasonable.
  6. Resolve product, data, UI, scope, and testing assumptions.
  7. Continue until the major branches of the design tree have been walked.
- **Outputs:**
  - Conversation history containing decisions, rejected alternatives, assumptions, and recommendations.
  - A shared design concept suitable for summarization into a PRD.
- **Benefits:**
  - Surfaces hidden decisions early.
  - Keeps the human engaged in the high-leverage alignment stage.
  - Can incorporate domain experts or other developers.
- **Tradeoffs:**
  - Can be long and tiring; Pocock reports sessions with 40, 80, or even 100 questions.
  - Requires human attention and cannot be fully AFK.
- **Failure modes:**
  - Agent asks too many questions.
  - Human lazily accepts recommendations without enough judgment.
  - The prompt fails to ask about critical constraints such as security, permissions, data retention, migrations, or observability.
- **Validation idea:** Compare defects and rework from features started with grilling versus features started from a direct implementation prompt.

### Workflow 2: Grilled Design Concept to PRD

- **Purpose:** Persist the alignment session into a destination document.
- **When to use:** After enough questions have been answered that the product behavior, scope, and implementation direction are stable.
- **Inputs:**
  - Grilling conversation.
  - Codebase exploration notes.
  - Any stakeholder/domain-expert transcript.
- **Steps:**
  1. Ask the agent to write a PRD from the current conversation.
  2. Include problem statement, solution, user stories, implementation decisions, testing decisions, and out-of-scope decisions.
  3. Ask it to identify proposed modules to modify.
  4. Confirm that the module list matches the intended architecture.
  5. Store the PRD as a local issue file or GitHub issue, depending on workflow.
- **Outputs:**
  - Destination PRD.
  - Module map / likely affected areas.
  - Definition of done.
- **Benefits:**
  - Converts ephemeral conversation into a compact artifact.
  - Gives later agents a stable destination.
  - Captures negative decisions and scope boundaries.
- **Tradeoffs:**
  - Pocock often does not read the PRD deeply; this saves time but risks summarization errors.
  - The PRD can become stale if kept too long.
- **Failure modes:**
  - Summarization drops edge cases.
  - Agent invents implementation details not agreed during grilling.
  - PRD becomes treated as source of truth after code diverges.
- **Validation idea:** Sample PRDs against the original grilling transcript; measure missing decisions, hallucinated decisions, and later issue churn.

### Workflow 3: PRD to Vertical-Slice Issue DAG

- **Purpose:** Turn the destination into independently grabbable, dependency-aware implementation tasks.
- **When to use:** Before delegating coding to agents.
- **Inputs:**
  - PRD.
  - Codebase architecture.
  - Module map.
  - Vertical-slice/tracer-bullet prompt.
- **Steps:**
  1. Ask the agent to split the PRD into issues.
  2. Require each issue to be independently grabbable.
  3. Require explicit blocker relationships.
  4. Mark tasks as AFK or human-in-the-loop.
  5. Reject horizontal slices that only implement one architectural layer.
  6. Prefer early issues that create visible, integrated, reviewable behavior.
  7. Store issues as local Markdown files or GitHub issues.
- **Outputs:**
  - Kanban board / issue DAG.
  - AFK-labelled work queue.
  - Blocker graph for sequential or parallel execution.
- **Benefits:**
  - Enables agents to pick the next task without human micromanagement.
  - Enables parallelization after blockers are cleared.
  - Increases feedback by making early slices integrated.
- **Tradeoffs:**
  - Human review of issue slicing is still required.
  - Too-thin slices may create overhead; too-thick slices may push agents into the dumb zone.
- **Failure modes:**
  - Agent creates horizontal tasks despite instructions.
  - Blockers are wrong, causing agents to start tasks too early.
  - Issues are not self-contained enough for fresh-context agents.
- **Validation idea:** Track how often generated issues can be completed by a fresh agent without clarification.

### Workflow 4: Ralph Once Loop for Human-Observed Implementation

- **Purpose:** Run one implementation iteration while observing agent behavior before allowing full AFK execution.
- **When to use:** When tuning prompts, validating a new repo setup, or testing whether the issue DAG is good enough.
- **Inputs:**
  - Local issue files.
  - Recent commits.
  - Implementation prompt.
  - Coding agent CLI.
- **Steps:**
  1. Concatenate issues into a context variable.
  2. Fetch the last five commits for recent history.
  3. Pass prompt + issues + commit history into Claude Code or another agent.
  4. Instruct agent to select the next unblocked AFK issue.
  5. Watch whether it explores appropriately, chooses a sensible task, writes tests, runs feedback loops, and commits.
  6. Tune prompts based on observed mistakes.
- **Outputs:**
  - One completed commit or a reported blocker.
  - Prompt-tuning observations.
- **Benefits:**
  - Catches setup problems before unattended runs.
  - Lets the human see whether the agent interprets issues correctly.
- **Tradeoffs:**
  - Still requires attention.
  - Not a throughput-maximizing mode.
- **Failure modes:**
  - Agent picks the wrong issue.
  - Agent ignores blockers.
  - Agent fails to run tests or commits incomplete work.
- **Validation idea:** Run the once loop across several generated issues and measure task-selection accuracy and CI pass rate.

### Workflow 5: AFK Implementation Loop

- **Purpose:** Let an agent repeatedly pick, implement, test, and commit AFK tasks.
- **When to use:** After issues are reviewed, prompts are tuned, and the repo has reliable feedback loops.
- **Inputs:**
  - AFK-labelled backlog.
  - Dependency/blocker graph.
  - Agent implementation prompt.
  - Sandbox or permission model.
  - Feedback commands such as tests and typechecks.
- **Steps:**
  1. Start from a clean context.
  2. Provide backlog and recent commit context.
  3. Tell the agent to work only on AFK issues.
  4. If no tasks remain, emit a sentinel such as “no more tasks.”
  5. Pick next task by priority: critical bug fixes, development infrastructure, tracer bullets, polishing/quick wins/refactors.
  6. Explore repo.
  7. Use TDD.
  8. Run feedback loops.
  9. Commit work.
  10. Repeat until backlog is empty or blocked.
- **Outputs:**
  - One or more commits.
  - Completed issue markers.
  - Agent summaries.
- **Benefits:**
  - Converts human planning into autonomous night-shift implementation.
  - Reduces human typing burden.
- **Tradeoffs:**
  - Increases code review and QA load.
  - Requires strong sandboxing and deterministic feedback.
- **Failure modes:**
  - Agent loops on failing tests.
  - Agent makes broad unrelated changes.
  - Agent completes multiple issues in a large, hard-to-review diff.
  - Permissions or sandboxing are too loose.
- **Validation idea:** Run AFK loop on non-critical tasks and measure completion rate, rollback rate, human review time, and defect escape rate.

### Workflow 6: Agentic TDD Red-Green-Refactor

- **Purpose:** Give the agent a tight correctness loop and prevent implementation-first test cheating.
- **When to use:** For logic, service modules, data transformations, API contracts, migrations, and any behavior that can be automatically checked.
- **Inputs:**
  - Issue requirements.
  - Existing test infrastructure.
  - TDD prompt/skill.
  - Test command.
- **Steps:**
  1. Agent identifies the smallest behavior to implement.
  2. Agent writes a failing test first.
  3. Agent runs the test and confirms failure for the expected reason.
  4. Agent implements minimum code to pass.
  5. Agent reruns targeted tests.
  6. Agent runs broader feedback loops such as all tests and typechecks.
  7. Agent refactors if needed while keeping tests green.
- **Outputs:**
  - Tests that encode intended behavior.
  - Implementation satisfying those tests.
  - Test/typecheck logs.
- **Benefits:**
  - Makes tests part of the design.
  - Gives agent immediate feedback.
  - Reduces after-the-fact weak test generation.
- **Tradeoffs:**
  - Harder for visual UI work.
  - Requires fast, reliable tests.
  - Agent may still write tests that assert implementation details.
- **Failure modes:**
  - Test fails for the wrong reason.
  - Test is too shallow.
  - Agent mocks away the behavior that matters.
  - TDD becomes slow if feedback loops are too heavy.
- **Validation idea:** Compare agent-generated tests with implementation-first versus test-first workflows for mutation-test strength or bug-catching ability.

### Workflow 7: Fresh-Context Automated Review

- **Purpose:** Review agent-generated commits with a separate smart-zone context.
- **When to use:** After each implementation commit or batch, especially before manual QA or team PR.
- **Inputs:**
  - Diff or commits.
  - Issue/PRD context.
  - Coding standards.
  - Test results.
- **Steps:**
  1. Clear context.
  2. Start reviewer agent.
  3. Push relevant coding standards and requirements into context.
  4. Provide diff/commits.
  5. Ask reviewer to identify correctness, architecture, test, security, and maintainability issues.
  6. Convert findings into fix issues or ask implementer to patch.
- **Outputs:**
  - Review comments.
  - Potential follow-up issues.
  - Higher confidence before human review.
- **Benefits:**
  - Uses smart zone for review.
  - Catches bugs cheaply.
  - Can enforce standards more consistently.
- **Tradeoffs:**
  - Extra token cost.
  - Review quality depends on standards and diff size.
- **Failure modes:**
  - Reviewer rubber-stamps plausible code.
  - Reviewer lacks full runtime context.
  - Reviewer over-focuses on style.
- **Validation idea:** Track how many automated-review findings are accepted by humans and how many defects escape despite clean review.

### Workflow 8: Manual QA as Taste Preservation

- **Purpose:** Reintroduce human taste, product judgment, and real-world behavior checking after agent implementation.
- **When to use:** After a vertical slice produces something visible or behaviorally testable.
- **Inputs:**
  - Running app.
  - Implemented slice.
  - PRD/user stories.
  - Manual test persona/data.
- **Steps:**
  1. Run the app.
  2. Exercise the user path manually.
  3. Inspect UI, copy, behavior, errors, and edge cases.
  4. Notice missing migrations, broken flows, awkward product choices, and naming problems.
  5. Feed findings back into the issue Kanban as new tasks or blockers.
- **Outputs:**
  - QA notes.
  - Additional issues.
  - Human approval or rejection of the slice.
- **Benefits:**
  - Protects against low-taste automation.
  - Catches integration issues tests missed.
  - Keeps human ownership of product quality.
- **Tradeoffs:**
  - Manual QA is time-consuming.
  - Hard to scale with high agent throughput.
- **Failure modes:**
  - Human only checks the happy path.
  - QA findings are patched ad hoc rather than added to backlog.
  - Agent throughput exceeds QA capacity.
- **Validation idea:** Record QA defect categories and add automated tests for recurring categories where possible.

### Workflow 9: Deep-Module Architecture Improvement

- **Purpose:** Improve a codebase so agents and humans can test and modify it more reliably.
- **When to use:** When agents struggle, tests are brittle, code is fragmented, or module boundaries are unclear.
- **Inputs:**
  - Existing codebase.
  - “Improve codebase architecture” skill or equivalent prompt.
  - Test coverage and dependency information.
- **Steps:**
  1. Ask agent to scan architecture.
  2. Identify clusters of tightly coupled shallow modules.
  3. Identify missing tests around meaningful logic.
  4. Propose deeper modules with smaller public interfaces.
  5. Define test boundaries around deep modules.
  6. Refactor incrementally with TDD and review.
- **Outputs:**
  - Architecture improvement candidates.
  - Proposed deep modules.
  - Testing plan.
- **Benefits:**
  - Raises the ceiling for future agent work.
  - Makes code easier to reason about.
  - Improves test leverage.
- **Tradeoffs:**
  - Requires architectural judgment.
  - Refactors can conflict with active feature work.
- **Failure modes:**
  - Agent creates abstraction for its own sake.
  - Refactor changes behavior.
  - Deep module interface is poorly chosen and becomes a bottleneck.
- **Validation idea:** Before/after measure: agent task success rate, test runtime, review time, number of files touched per feature, and defect rate.

### Workflow 10: Parallel Agents with Planner, Implementers, Reviewers, and Merger

- **Purpose:** Execute independent issues concurrently while keeping review and merge steps structured.
- **When to use:** After the backlog is represented as a dependency graph with clear blockers.
- **Inputs:**
  - Issue DAG.
  - Git worktree/sandbox infrastructure.
  - Planner prompt.
  - Implementer prompt.
  - Reviewer prompt.
  - Merger prompt.
- **Steps:**
  1. Planner inspects backlog and selects issues that can run in parallel.
  2. For each selected issue, create an isolated git worktree/branch and Docker sandbox.
  3. Run an implementer agent in each sandbox.
  4. If commits were produced, run reviewer agents.
  5. Pass branches and issue context to a merger agent.
  6. Merger integrates branches, resolves conflicts, and reruns tests/typechecks.
- **Outputs:**
  - Multiple feature branches.
  - Reviews.
  - Merged branch or integration failure report.
- **Benefits:**
  - Exploits independent tasks.
  - Separates planning, implementation, review, and merge responsibilities.
- **Tradeoffs:**
  - More infrastructure complexity.
  - More merge conflicts and review volume.
- **Failure modes:**
  - Planner selects tasks with hidden coupling.
  - Implementers make inconsistent architectural choices.
  - Merger masks semantic conflicts.
  - Review cannot keep up.
- **Validation idea:** Compare parallel throughput against sequential AFK loop on a controlled backlog, measuring total lead time and post-merge defects.

### Workflow 11: Front-End Prototype Route for Visual Decisions

- **Purpose:** Use AI for exploratory UI generation without pretending it can fully judge mature frontend quality.
- **When to use:** When visual design, layout, interaction, or UX direction is uncertain.
- **Inputs:**
  - UI goal.
  - Existing design system if any.
  - Throwaway route or sandbox page.
- **Steps:**
  1. Ask the agent to produce several prototype variants.
  2. Put them behind a temporary route or switchable UI.
  3. Human/domain expert clicks through variants.
  4. Capture chosen direction and feedback.
  5. Feed that feedback back into grilling or PRD.
  6. Delete or rewrite throwaway prototype code before production implementation.
- **Outputs:**
  - Prototype options.
  - Human-selected direction.
  - Better UI requirements.
- **Benefits:**
  - Gets early visual feedback.
  - Avoids overcommitting to AI-generated frontend code.
- **Tradeoffs:**
  - Prototype code may be low quality.
  - Requires humans to inspect visuals.
- **Failure modes:**
  - Prototype leaks into production.
  - Agent ignores design system.
  - Human picks aesthetics but misses accessibility or responsiveness.
- **Validation idea:** Track whether prototype-derived PRDs reduce later UI rework.

### Workflow 12: Coding Standards with Pull for Implementers and Push for Reviewers

- **Purpose:** Enforce repo conventions without wasting implementer context budget.
- **When to use:** In codebases with documented architecture, style, testing, security, or API conventions.
- **Inputs:**
  - Coding standards.
  - Skills or docs discoverable by agents.
  - Reviewer prompt.
- **Steps:**
  1. Store standards where implementer can pull them when relevant.
  2. Avoid pushing all standards into every implementation context unless necessary.
  3. For automated review, push the standards directly into context.
  4. Ask reviewer to compare diff against standards.
  5. Convert violations into fixes or feedback.
- **Outputs:**
  - Lower implementer context load.
  - More standards-aware review.
- **Benefits:**
  - Balances context budget and enforcement.
  - Makes review stricter than implementation.
- **Tradeoffs:**
  - Implementer may not pull needed standards.
  - Reviewer prompt can become large.
- **Failure modes:**
  - Standards are stale.
  - Skills are poorly described and not retrieved.
  - Reviewer misses conventions not pushed.
- **Validation idea:** Measure standards violations found by human review before and after push/pull setup.

## Tools, Libraries, and Frameworks

| Name                                                | Type                                           | Purpose                                                                                    | Mentioned context                                                            | Link if available |
| --------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------:| ---------------------------------------------------------------------------- | ----------------- |
| Claude Code                                         | Coding agent / CLI                             | Terminal-based agent used for planning, skills, implementation, permissions, and AFK loops | Main demo environment; speaker says method is not Claude-specific            | See References    |
| Claude                                              | LLM / assistant                                | Underlying model family used by Claude Code                                                | Used throughout; “Claude” sometimes mistranscribed as “claw”                 | See References    |
| Claude Opus                                         | LLM model                                      | Higher-capability model used by subagents/review in examples                               | Subagent spent ~93.7k tokens on Opus; speaker uses Opus for review           | See References    |
| Claude Sonnet                                       | LLM model                                      | Implementation model in Sand Castle setup                                                  | Speaker says he uses Sonnet for implementation                               | See References    |
| Claude subagents                                    | Agent pattern / Claude feature                 | Delegate exploration to isolated context and return summary                                | Used during “grill me” exploration to avoid polluting parent context         | See References    |
| Claude skills / slash commands                      | Agent extension mechanism                      | Invoke reusable prompts such as “grill me,” “write a PRD,” and architecture improvement    | Speaker invokes skills with slash command syntax                             | See References    |
| “Grill me” skill                                    | Prompt / skill                                 | Relentlessly interview human one question at a time until shared understanding             | First workflow step after ambiguous client brief                             | Not provided      |
| “Write a PRD” skill                                 | Prompt / skill                                 | Convert discussion/design concept into a PRD                                               | Produces destination document with user stories and decisions                | Not provided      |
| “PRD to issues” skill                               | Prompt / skill                                 | Convert PRD into independently grabbable vertical-slice issues                             | Produces local Markdown issue files or GitHub issues                         | Not provided      |
| “Improve codebase architecture” skill               | Prompt / skill                                 | Scan repo for architecture improvements and deep-module opportunities                      | Used near end to identify shallow/tightly coupled module clusters            | Not provided      |
| Ralph / Ralph loop                                  | Agent loop pattern                             | Repeatedly pick small tasks that move toward destination                                   | Named after “Ralph Wiggum” practice; used for AFK issue implementation       | Not provided      |
| `once.sh`                                           | Bash script                                    | Run one agent iteration with issues, commits, and implementation prompt                    | Concatenates local issues and recent commits, then runs Claude Code          | Not provided      |
| `afk.sh` / AFK loop                                 | Bash/scripted agent loop                       | Repeated unattended implementation in sandbox                                              | Mentioned as more complicated Docker-sandbox version                         | Not provided      |
| Sand Castle                                         | TypeScript library / orchestration tool        | Create worktrees, sandbox agents in Docker, run parallel implement/review/merge loops      | Speaker-built tool for AFK parallel agent orchestration                      | Not provided      |
| GitHub Issues                                       | Issue tracker                                  | Store PRDs and implementation issues, close old items to reduce doc rot                    | Speaker prefers GitHub Issues in his normal workflow                         | See References    |
| Local Markdown issue files                          | File convention                                | Store issue backlog locally for workshop simplicity                                        | Used instead of GitHub Issues in exercise repo                               | Not applicable    |
| Git                                                 | Version control                                | Commits, branches, worktrees, recent history, merge                                        | Used by Ralph loop and Sand Castle                                           | See References    |
| Git worktrees                                       | Git feature                                    | Isolate parallel branches / agent workspaces                                               | Sand Castle creates worktrees                                                | See References    |
| Docker                                              | Containerization                               | Sandbox agent runs and isolate filesystem/execution                                        | AFK loop and Sand Castle use Docker sandboxing                               | See References    |
| Docker sandbox                                      | Execution isolation pattern                    | Reduce risk from unattended agents                                                         | Used for AFK runs; not required in workshop due conference Wi-Fi constraints | See References    |
| TypeScript                                          | Programming language                           | Main language in demo app and Sand Castle                                                  | Speaker jokes AI knows TypeScript; app uses TypeScript services              | See References    |
| npm                                                 | Package manager / script runner                | Run tests, typechecks, DB commands                                                         | Agent runs `npm run test`, `npm run typecheck`, DB migration commands        | See References    |
| Vitest                                              | Test runner                                    | Run tests in the TypeScript codebase                                                       | Transcript likely says `npx vitest` while auto-caption reads “npxv text”     | See References    |
| SQLite                                              | Database                                       | Demo app storage and test database                                                         | Migration/table issue appears during manual QA                               | See References    |
| Cucumber                                            | BDD language/tool                              | Possible language for user stories                                                         | Mentioned as a way developers may have seen user stories written             | See References    |
| Playwright MCP                                      | Browser automation / MCP integration           | Give agents browser tools for frontend inspection                                          | Speaker says AI is not yet good enough at mature frontend visual judgment    | See References    |
| Agent Browser                                       | Browser automation tool/category               | Let agents inspect frontend through browser/images                                         | Mentioned with Playwright MCP as not yet sufficient for mature frontend      | Not provided      |
| MCP                                                 | Model Context Protocol / tool interface        | Connect agents to browser-like tools                                                       | Mentioned in “Playwright MCP” context                                        | See References    |
| Gemini Meetings                                     | Meeting/transcript tool                        | Capture meeting transcript to feed into grilling                                           | Speaker suggests feeding domain-expert meeting transcript into grilling      | See References    |
| TLDraw / tldraw                                     | Infinite canvas / drawing tool                 | Speaker uses an infinite canvas instead of slides                                          | Used for diagrams of context, workflow, and modules                          | See References    |
| Slack                                               | Messaging platform                             | Source format for ambiguous client brief                                                   | Demo brief is a Slack message from “Sarah Chen”                              | See References    |
| Slido                                               | Q&A tool                                       | Audience questions and voting                                                              | Used to democratize Q&A during workshop                                      | See References    |
| GitHub repository `mattpocock/course-video-manager` | Repository / app                               | Speaker’s work repo and real workflow example                                              | Used to show hundreds of closed issues from PRD/implementation workflow      | See References    |
| Course Video Manager                                | Application                                    | Speaker’s app for recording/managing course videos                                         | Used as real-world app and Sand Castle example                               | See References    |
| Cadence                                             | Demo course platform                           | Workshop application where gamification is implemented                                     | Course-management CMS for instructors/students                               | Not provided      |
| Spec Kit / Specit                                   | Planning framework, transcript uncertain       | Possible alternative to the grill-me skill                                                 | Audience asks about “specit open spec or taskmaster”; transcript unclear     | Not provided      |
| OpenSpec / Open spec                                | Planning/spec framework, transcript uncertain  | Possible structured alternative to custom planning stack                                   | Mentioned in audience question; exact product uncertain                      | Not provided      |
| Taskmaster                                          | Agent task/planning tool, transcript uncertain | Possible structured alternative to custom planning stack                                   | Mentioned in audience question                                               | Not provided      |
| Beads framework                                     | Task/issue framework, transcript uncertain     | Manage Kanban/issues                                                                       | Audience asks for thoughts; speaker has not tested it                        | Not provided      |
| Windows                                             | Operating system                               | Speaker’s laptop environment                                                               | Mentioned jokingly as source of friction                                     | See References    |

## Tradeoffs and Failure Modes

| Area                         | Tradeoff / failure mode                                                                  | Speaker context                                                            | Mitigation or validation idea                                                                |
| ---------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Context length               | Larger context windows may encourage agents to keep working into lower-quality territory | Smart zone/dumb zone discussion around 0:03:02–0:05:44 and 0:37:24–0:38:30 | Track token usage; cap task size; clear context between phases                               |
| Compaction                   | Summaries preserve history but can accumulate sediment and distortions                   | 0:08:48–0:10:53                                                            | Prefer clear context for repeatable agent starts; test compaction quality on real tasks      |
| Persistent system prompt     | Large always-on prompts push agent toward dumb zone before work begins                   | 0:07:52–0:08:17                                                            | Keep system/context instructions small; move detailed docs to pull-based skills              |
| Grilling                     | Strong alignment but high human time cost                                                | 0:16:15–0:21:43                                                            | Tune skill for stop points; involve domain experts only for questions needing them           |
| Accepting AI recommendations | Agent recommendations are useful but can induce lazy human agreement                     | 0:18:36–0:20:31                                                            | Require explicit rationale for high-impact decisions; mark assumptions                       |
| Specs-to-code                | Ignoring code can produce code humans do not understand or cannot maintain               | 0:12:34–0:13:39                                                            | Keep proposed modules and test boundaries in planning artifacts                              |
| PRD summarization            | Speaker often skips PRD review, relying on LLM summarization                             | 0:35:09–0:36:00                                                            | At least sample high-risk sections; compare against decisions and out-of-scope list          |
| Horizontal slicing           | AI tends to plan by layers: schema, API, frontend                                        | 0:42:53–0:45:57                                                            | Force tracer-bullet vertical slices; human-review issue split                                |
| Too-large slices             | Vertical slices can still be too broad and exceed smart-zone capacity                    | Implied by task-sizing thesis                                              | Split by user-visible behavior and feedback-loop duration                                    |
| Sequential plans             | Multi-phase plans serialize work and prevent parallel agents                             | 0:05:44–0:06:39 and 0:49:40–0:51:38                                        | Use issue DAG with blockers instead of numbered phases                                       |
| Parallel agents              | Throughput increases but conflicts/review burden increase                                | 0:50:05–0:51:14 and 1:30:51–1:32:19                                        | Use worktrees/sandboxes; constrain tasks; run merger agent and CI                            |
| AFK implementation           | Reduces typing but can create more code than humans can review                           | 0:58:55–1:00:14                                                            | Limit batch size; keep PRs small; prioritize review capacity metrics                         |
| Frontend work                | Agents have weak visual judgment in mature codebases                                     | 1:02:32–1:03:47                                                            | Use throwaway prototypes for direction; human chooses; productionize separately              |
| Agent self-review            | Same context reviews in dumb zone after implementation                                   | 1:05:24–1:06:27                                                            | Clear context and run separate reviewer                                                      |
| TDD                          | Powerful when feasible; less straightforward for UI/visual work                          | 1:06:41–1:08:34                                                            | Use service-level tests where possible; supplement frontend with manual QA and browser tests |
| Weak tests                   | Agents may write tests that cheat or assert implementation details                       | 1:07:47–1:08:21                                                            | Enforce red-first tests; review tests before implementation                                  |
| Missing migrations           | Manual QA exposed missing SQLite table after agent commit                                | 1:11:47–1:12:19                                                            | Include migration checks in feedback loop; run app from fresh DB state                       |
| Shallow modules              | Many tiny interdependent modules make testing and navigation hard                        | 1:13:39–1:17:58                                                            | Refactor toward deep modules and stable interfaces                                           |
| Deep modules                 | Interface choice becomes high leverage and high risk                                     | 1:17:02–1:20:57                                                            | Human designs interface; add contract tests; refactor incrementally                          |
| Documentation rot            | Old PRDs can mislead future agents                                                       | 1:23:34–1:25:03                                                            | Close issues rather than keeping stale docs in repo; mark historical docs clearly            |
| Coding standards             | Pushing too much wastes context; pulling too little misses standards                     | 1:27:40–1:29:42                                                            | Pull for implementer, push for reviewer                                                      |
| Sandbox permissions          | Unattended agents can modify too much or run unsafe commands                             | 0:54:21–0:55:37 and 1:29:54–1:30:24                                        | Use Docker sandbox, restricted permissions, worktrees, and review gates                      |
| Team integration             | The clean pipeline is messier in real teams                                              | 1:00:27–1:02:15                                                            | Treat early artifacts as RFC-like shared assets; bounce between phases as needed             |

## Claims Made By Speaker

| Claim                                                                                         | Evidence or context from the video  | Confidence                                                 | Needs validation         |
| --------------------------------------------------------------------------------------------- | ----------------------------------- | ----------------------------------------------------------:| ------------------------ |
| AI is a new paradigm, but software engineering fundamentals still work well with AI           | Opening thesis at 0:00:52–0:01:38   | High that speaker said it; medium as universal claim       | Yes                      |
| LLMs have a smart zone and a dumb zone                                                        | 0:03:02–0:04:34                     | High that speaker said it; medium technical generalization | Yes                      |
| Around 100k tokens is his current marker for smart-zone boundary                              | 0:04:05–0:04:17                     | High that speaker said it; low/medium as general threshold | Yes                      |
| Larger context windows are better for retrieval than coding                                   | 0:37:24–0:38:30                     | High that speaker said it; medium technical claim          | Yes                      |
| Tasks should be sized to fit in the smart zone                                                | 0:04:34–0:05:44                     | High                                                       | Yes                      |
| Compacting is worse than clearing for his workflow                                            | 0:08:48–0:10:53                     | High as preference; medium as general advice               | Yes                      |
| “Grill me” is how he starts virtually every AI work item                                      | 0:15:45–0:16:04                     | High                                                       | No, unless adopting      |
| The goal of early AI planning is shared understanding, not an asset or plan                   | 0:16:42–0:17:31                     | High                                                       | Partly                   |
| AI recommendations during grilling are often good                                             | 0:18:36–0:19:16                     | High as experience claim                                   | Yes                      |
| Planning/alignment must be human-in-the-loop                                                  | 0:26:30–0:27:06                     | High                                                       | Yes                      |
| Implementation can be converted into an AFK task                                              | 0:26:42–0:27:00 and 0:52:23–0:53:14 | High                                                       | Yes                      |
| Pure specs-to-code does not work well because code must still be shaped                       | 0:12:34–0:13:39                     | High                                                       | Yes                      |
| PRD is the destination document; issues/Kanban are the journey document                       | 0:28:38–0:31:56 and 0:39:32–0:40:19 | High                                                       | No as conceptual framing |
| He often does not review generated PRDs                                                       | 0:35:09–0:36:00                     | High                                                       | Yes before copying       |
| AI tends to code horizontally by layer                                                        | 0:42:53–0:43:18                     | High as speaker observation                                | Yes                      |
| Vertical slices produce earlier integrated feedback                                           | 0:43:18–0:45:11                     | High                                                       | Yes                      |
| Kanban issue DAGs are more parallelizable than sequential plans                               | 0:49:40–0:51:38                     | High                                                       | No, mostly logical       |
| TDD is essential for getting the most out of agents                                           | 1:06:41–1:08:34                     | High as speaker view                                       | Yes                      |
| Feedback-loop quality is the ceiling for agent output                                         | 1:09:45–1:10:27                     | High                                                       | Yes                      |
| Automated review should happen in a fresh context                                             | 1:05:24–1:06:27                     | High                                                       | Yes                      |
| Manual QA is necessary to impose human taste                                                  | 1:12:38–1:13:33                     | High                                                       | Yes                      |
| Bad codebases make bad agents                                                                 | 0:36:48–0:37:06 and 1:13:39–1:17:58 | High                                                       | Yes                      |
| Deep modules improve agent ability by improving testability and navigability                  | 1:13:39–1:22:59                     | High                                                       | Yes                      |
| Designing module interfaces while delegating internals preserves human codebase understanding | 1:19:17–1:20:57                     | High                                                       | Yes                      |
| Old PRDs kept in the repo can mislead agents due documentation rot                            | 1:23:34–1:25:03                     | High                                                       | Yes                      |
| Implementers should pull coding standards, reviewers should have them pushed                  | 1:27:40–1:29:42                     | High                                                       | Yes                      |
| Sand Castle parallel workflow works “super super well” for his projects                       | 1:29:47–1:32:39                     | High as speaker experience claim                           | Yes                      |

## Relevance To AI Coding Workflow

### Idea → Plan

- Use AI first as an interviewer, not as an implementer.
- Start from a clean context to preserve the smart zone.
- Feed in the smallest useful brief: client message, meeting transcript, or rough idea.
- Have the agent ask one question at a time and include a recommended answer.
- Treat unresolved questions as signals to involve the right human: product owner, domain expert, security reviewer, fellow developer, or designer.
- Capture both positive decisions and negative decisions; negative decisions become out-of-scope boundaries.
- Use optional research and prototype loops before PRD if the destination is still uncertain.
- Do not expect the first AI-generated plan to be trustworthy; alignment comes from interrogation and iteration.

### Plan → Code

- Convert the alignment session into a PRD only after shared understanding exists.
- Use the PRD as a destination, not as a substitute for code awareness.
- Ask for proposed modules to modify and review those modules as an architecture decision.
- Convert PRD into a Kanban/DAG of independently grabbable issues.
- Reject horizontal layer-only tasks when they delay integrated feedback.
- Prefer tracer-bullet issues that produce a visible or testable end-to-end behavior.
- Mark issues as AFK only when they do not require product/domain judgment.
- Keep issue size small enough for one fresh context to complete.

### Code → Test

- Use TDD as the default agent implementation discipline when the behavior is testable.
- Require “red” before implementation and “green” after implementation.
- Review tests first during code review; tests reveal what the agent thought the task meant.
- Improve codebase architecture to make meaningful test boundaries possible.
- Deep modules make tests more valuable because one test boundary covers substantial behavior behind a small interface.
- Typechecks, migrations, linters, and integration tests are all feedback loops that raise agent reliability.

### Test → Deploy

- Run automated feedback loops before manual QA.
- Run automated review in a fresh context.
- Use sandboxed worktrees or containers for unattended agent work.
- Keep PRs/diffs small enough to review; this is an unresolved challenge as agent throughput rises.
- Merge parallel branches only after conflict resolution and full feedback-loop execution.
- Treat deployment readiness as a human-reviewed state, not merely “agent says tests pass.”

### Review / Debug

- Manual QA is the place where human taste and product judgment re-enter the workflow.
- QA findings should become new issues in the same Kanban/backlog, not ad hoc side conversations.
- When debugging agent mistakes, inspect whether the failure came from unclear requirements, bad issue slicing, weak feedback loops, poor architecture, stale docs, or context overload.
- Use old PRDs carefully; stale plans can be harmful when agents treat them as current facts.
- Push standards into reviewer context; leave standards pullable for implementers to conserve context.

## Detailed Timestamped Notes

### 0:00:07–0:02:55 — Opening, thesis, and workshop setup

- The session begins at capacity, with Matt Pocock introducing himself as a teacher who now teaches AI.
- He points attendees to a link containing workshop exercises and says the workshop will run roughly two hours.
- Central opening thesis: AI is a new paradigm, but software-engineering fundamentals that work well with humans also work well with AI.
- He polls the audience:
  - Most have coded with AI.
  - Many code with AI daily.
  - Many have been frustrated with AI.
- Q&A is handled through Slido to make questions more democratic than open mic.

### 0:03:02–0:05:44 — LLM constraints: smart zone, dumb zone, and task sizing

- Pocock introduces an idea attributed to a person from HumanLayer: LLMs have a smart zone and a dumb zone.
- Early in a fresh conversation, the LLM tends to do its best work.
- He explains the intuition through attention relationships: as more tokens are added, the number of relationships the model must manage grows sharply.
- He gives a practical current marker: around 100k tokens is where he expects degradation, even with larger context windows.
- The engineering implication: size tasks so agents stay in the smart zone.
- He connects this to older advice from Martin Fowler and The Pragmatic Programmer: do not bite off more than you can chew; keep tasks small.

### 0:05:01–0:07:18 — From multi-phase plans to loops and Ralph-style progress

- The problem: large tasks must be broken into smaller tasks.
- One naive approach is to keep one conversation going, compact repeatedly, and continue. Pocock argues this does not work well because sediment accumulates.
- He describes his older approach: multi-phase plans that break work into smaller sections.
- Then he notes that any developer sees a numbered phase list as a loop: phase one, phase two, phase three becomes phase N.
- He mentions “Ralph Wiggum” as a software practice: specify an end destination and repeatedly ask AI to make a small change that gets closer.
- He says Ralph-style looping works, but he prefers more structure.

### 0:07:18–0:11:06 — LLMs as Memento-like: forgetful sessions, compaction, and clearing

- Pocock compares LLMs to the protagonist of *Memento*: they continually forget and reset to base state.
- He draws a session lifecycle:
  - System prompt / always-present context.
  - Exploration phase.
  - Implementation phase.
  - Testing / feedback phase.
- He warns to keep the always-present context small. Huge persistent prompts push the agent straight toward the dumb zone.
- He demonstrates Claude Code and a token status line showing exact token usage.
- He strongly recommends having token usage visible in every coding session.
- He demonstrates clearing versus compacting:
  - Clear: return to no conversation history.
  - Compact: squeeze conversation into a summary.
- He says developers love compacting, but he hates it for his workflow because he prefers the repeatable base state of clearing.
- The two key LLM constraints established:
  1. Smart zone versus dumb zone.
  2. Memento-like reset/forgetfulness.

### 0:11:24–0:13:45 — Demo app and rejection of pure specs-to-code

- The workshop repo is a course-management platform / CMS for instructors and students.
- The workshop will implement a feature from idea to PRD to implementation.
- The first skill introduced is “grill me.”
- Pocock names misalignment as a main issue when working with AI.
- He argues against the “specs-to-code” movement:
  - Write specs.
  - Let AI turn specs into code.
  - If code is wrong, edit specs rather than code.
- He says this is essentially vibe coding by another name and that, in his experience, it “sucks.”
- Key rationale: the code is the battleground. Humans need to understand and shape it.

### 0:13:45–0:21:43 — “Grill me” skill on the gamification brief

- The input brief is a Slack-style message from “Sarah Chen” saying retention is poor and requesting gamification.
- Pocock clears context and invokes the “grill me” skill with the client brief.
- The skill prompt instructs the agent to:
  - Interview relentlessly.
  - Walk down each branch of the design tree.
  - Resolve dependencies one by one.
  - Provide a recommended answer for each question.
  - Ask one question at a time.
- Pocock says plan mode often produces a plan too eagerly.
- He cites Frederick P. Brooks and the “design concept”: the shared idea among people building something together.
- He wanted a shared understanding with Claude, not just a generated artifact.
- The agent explores the codebase using a subagent. The subagent has an isolated context and reports summary back to the parent/orchestrator agent.
- First grilling question: what actions earn points and how much?
- The agent recommends keeping point sources simple and avoiding noisy/gameable events like video watch events.
- Another key question: should points be retroactive for existing lesson progress records?
- Pocock notes that this is exactly the kind of decision stakeholders might not have specified but implementation requires.
- He proceeds through questions about level progression, streaks, and where UI should live.
- He explains that grilling can last 40, 80, or 100 questions, producing a conversation history that becomes an asset.
- He suggests a domain-expert meeting transcript can be fed into a grilling session to validate assumptions.

### 0:23:24–0:28:12 — Q&A: owning the planning stack and human-in-loop planning

- Audience asks about alternatives like Spec Kit/OpenSpec/Taskmaster.
- Pocock says that when there is no clear winner and tools change rapidly, engineers should own as much of their planning stack as possible.
- Rationale: if you overuse an opaque stack and it fails, you lack observability and do not know how to fix it.
- Audience asks whether grilling questions are more appropriate for product owners than developers.
- Pocock recommends pair or mob sessions with AI:
  - For domain questions: developer + domain expert + AI.
  - For implementation questions: developer + fellow developer + AI.
- He distinguishes two task types:
  - Human-in-the-loop tasks, where a human must be present.
  - AFK tasks, where the human can leave.
- Planning/alignment is human-in-the-loop and cannot be Ralph-looped safely.

### 0:28:38–0:36:00 — PRD as destination document

- After the grilling session, Pocock says they have used about 25k tokens, much of it valuable.
- The goal is to summarize the conversation into a destination document.
- He invokes the “write a PRD” skill.
- The PRD skill can ask for a long problem description, explore the repo, interview the user, and then fill a PRD template.
- The PRD template includes:
  - Problem statement.
  - User problem.
  - Solution.
  - User stories.
  - Implementation decisions.
  - Testing decisions.
- The agent proposes modules to modify. Pocock emphasizes this because code remains central; this is not specs-to-code.
- The PRD is written locally in the workshop, but Pocock’s normal workflow uses GitHub Issues.
- He shows his `mattpocock/course-video-manager` repository with hundreds of closed issues, representing PRDs and implementation issues from his workflow.
- He says he does not usually read the generated PRD deeply.
- His reasoning: after the grilling session, the human and LLM share the design concept, and the PRD mostly tests the LLM’s summarization ability.
- This is a controversial/risky practice: useful for speed, but it assumes the grilling session was complete and summarization is faithful.

### 0:36:00–0:38:49 — Q&A: code expertise and large context windows

- Pocock says bad codebases make bad agents: garbage codebase in, garbage agent output out.
- He argues developers still benefit from deep TypeScript/code understanding because they need to shape the codebase and get more from AI.
- On 1M-token context windows:
  - He recorded his Claude Code course using a 200k context window.
  - Claude announced 1M context on launch day.
  - His view: 1M mostly ships “more dumb zone.”
  - Good for retrieval over large material.
  - Less good for coding.
- He expects the smart zone to improve over time.

### 0:38:49–0:47:13 — PRD to Kanban and tracer bullets / vertical slices

- With a destination PRD, the next step is the journey: how to reach that destination without pushing work into the dumb zone.
- Instead of asking for a sequential multi-phase plan, Pocock prefers creating a Kanban board.
- The agent proposes five tasks:
  - Schema and gamification service.
  - Streak tracking.
  - Wire points/streaks into lessons and quizzes.
  - Retroactive backfill.
  - UI polish / final integration.
- Pocock introduces tracer bullets / vertical slices from The Pragmatic Programmer.
- Systems have layers:
  - Database.
  - API.
  - Frontend.
  - Internal services.
- AI tends to code horizontally by layer.
- The problem with horizontal coding: integrated feedback only arrives after later phases.
- Vertical slices cross layers and create testable/reviewable integrated behavior earlier.
- Pocock reviews the generated issues and criticizes the first task as too horizontal.
- He asks the AI to improve the slice.
- The agent responds with a better vertical slice: award points for lesson completion and make it visible on the dashboard.
- Pocock approves this as a good slice because it produces visible behavior at the end.

### 0:47:13–0:51:38 — Issue generation, blocking relationships, and parallelization

- Pocock answers that grilling length can be tuned in the skill if it asks too many questions.
- He says he has dropped the older prompt “sacrifice grammar for concision” because he no longer wants to read plans; he wants alignment.
- Issues are designed to be independently grabbable.
- He draws a dependency graph:
  - Some tasks must happen before others.
  - After a root task completes, multiple tasks can be grabbed by independent agents.
- This turns the implementation plan into a directed acyclic graph.
- He contrasts this with sequential phase plans, which only one agent can work through.

### 0:51:44–0:58:14 — From planning to AFK implementation; Ralph loop internals

- The agent initially tries to create GitHub issues, but Pocock redirects it to create local Markdown files for the workshop.
- He summarizes the flow so far:
  - Idea.
  - Grilling.
  - PRD destination.
  - Kanban journey.
  - All human-reviewed.
- Now, at implementation, the human leaves the loop.
- He describes this as day shift and night shift:
  - Human day shift prepares high-quality work.
  - AI night shift executes AFK tasks.
- The “Running your AFK agent” exercise uses a Ralph-style prompt.
- `once.sh`:
  - Reads all local issue Markdown files.
  - Reads the last five commits.
  - Runs Claude Code with permission mode accepting edits.
  - Passes all information into an implementation prompt.
- The full AFK version is more complicated and uses a Docker sandbox.
- The workshop avoids making everyone run Docker to avoid overloading conference Wi-Fi.
- The implementation prompt:
  - Works only on AFK issues.
  - Emits a sentinel when no AFK tasks remain.
  - Picks the next task.
  - Prioritizes critical bugs, dev infrastructure, tracer bullets, then polish/refactors.
  - Explores repo.
  - Uses TDD.
  - Runs feedback loops.

### 0:58:14–1:05:43 — Q&A: negative decisions, review load, teams, prototypes, and AI QA

- Negative decisions are retained in the PRD’s out-of-scope section.
- Audience asks how to deal with agents producing more code than humans can review.
- Pocock says this is a real unresolved issue: if implementation is delegated, developers may do more code review.
- He does not present a clean solution; he expects teams to be ready for more review.
- Audience asks how the workflow works in real teams where work is messy.
- Pocock says the idea-to-destination stages are team artifacts:
  - Grilling questions can require team members.
  - Prototypes and research may feed back into the idea.
  - PRDs and journey documents can be argued over like RFCs.
- Audience asks about prototypes.
- Pocock says frontend is sensitive to human eyes and AI does not yet have strong visual judgment.
- For frontend, he recommends asking AI for several throwaway prototypes on a route, letting humans click between them, and feeding the chosen direction back into planning.
- Audience asks why not get AI to QA/test its own code.
- Pocock says automated review should absolutely happen, but ideally after clearing context.
- If the same long implementation context reviews itself, it reviews in the dumb zone.
- Fresh-context review is smarter.

### 1:05:50–1:08:53 — TDD for agents

- Pocock introduces TDD as essential for getting the most out of agents.
- TDD is red-green-refactor:
  - Write failing test.
  - Make it pass.
  - Refactor while green.
- In the demo, the agent writes a test for a gamification service before the module exists.
- It confirms the test fails because the module does not exist.
- Then it implements code and runs tests.
- Pocock says AI often writes bad tests and tries to cheat when it implements first and tests later.
- Test-first makes cheating harder because the test instruments the code before the code is written.
- He says TDD is so good that he warps his technique around making TDD work better.

### 1:08:53–1:13:39 — First implementation result and manual QA

- The Ralph loop completes issue number two and produces a summary.
- The implementation added dashboard-related gamification behavior and ran tests/typechecks.
- The agent ran `npm run test` and `npm run typecheck`.
- It hit a type error and fixed it with TypeScript.
- The repo now has 284 tests in the demo state.
- Pocock explains his code-review sequence:
  1. Review tests first.
  2. Then review code.
- He manually QA’s by logging in as a student and completing a lesson.
- Manual QA reveals an error: missing SQLite table `point_events`.
- He notes that watching QA is boring, but QA is crucial.
- QA is where he imposes opinions and taste back onto the codebase.
- He warns that teams trying to automate the entire process from idea to QA often produce apps that lack taste or do not work.

### 1:13:39–1:20:57 — Bad codebases, shallow modules, deep modules

- Pocock introduces John Ousterhout’s module model from *A Philosophy of Software Design*.
- A bad codebase is drawn as many small files with tangled dependency arrows.
- These shallow modules export many small pieces and require agents to trace complex dependency graphs.
- This is hard for agents to navigate and hard to test.
- Bad tests often wrap every tiny function in its own test boundary.
- That creates unclear mocking decisions and misses integrated behavior.
- Good codebases use deep modules:
  - Small, simple interfaces.
  - Significant hidden functionality inside.
- Deep modules are easier to test because a single test boundary can cover meaningful behavior.
- The caller has a simpler interface.
- Pocock says unaided AI tends to create shallow-module codebases, so humans must direct it.
- In the PRD, he includes proposed modules and identifies a gamification service as a new deep module with a testable interface.
- This module map stays in mind through planning and implementation.
- He asks who feels they work harder with AI and who feels they know their codebase less well; many raise hands.
- He says delegating more can cause humans to lose a sense of the codebase.
- His solution: design module interfaces and delegate internals.
- Treat modules as gray boxes: know their shape, behavior, and contract, not necessarily every implementation detail.

### 1:21:08–1:23:04 — Architecture-improvement skill

- Pocock runs an “improve codebase architecture” skill.
- The skill scans the codebase to find places where modules can be deepened.
- He gives an example from his Course Video Manager app:
  - A browser-based video editor.
  - He wanted to wrap frontend-to-backend flow in a single large testable module.
  - A discriminated union helped connect frontend/backend types.
  - This made AI much better at working on the video editor.
- He says if viewers take one thing away, try running this architecture-improvement skill on their repo.

### 1:23:04–1:25:15 — Documentation rot and whether to keep PRDs

- Audience asks whether he keeps Markdown plans and issues for later.
- Pocock asks who wants to keep PRDs in the repo versus delete them.
- He is worried about documentation rot:
  - A PRD for gamification may be accurate today.
  - A month later, code names, file structure, and requirements may have changed.
  - Claude might find the old PRD and treat it as current documentation.
- He tends not to keep PRDs around in the repo.
- Because he uses GitHub Issues, he can close the issue. It remains fetchable if needed but visually marked as done.
- This is his preferred way to preserve history without making stale docs look authoritative.

### 1:25:15–1:29:42 — Planning optimization and coding standards

- Audience asks whether early plans should be optimized repeatedly.
- Pocock says there is not much value in optimizing the PRD endlessly.
- The journey document is a hint; the important work is alignment up front and QA later.
- Audience asks how to get AI to code the way the team wants.
- Pocock introduces push versus pull:
  - Push: always send instructions, e.g. `CLAUDE.md` instructions like “talk like a pirate.”
  - Pull: make instructions available for the agent to retrieve when needed, such as skills.
- Current thinking:
  - Implementer should have coding standards available via pull.
  - Reviewer should have coding standards pushed into context.
- Reason: reviewer compares the written code against the standards, so it needs standards present.

### 1:29:47–1:32:39 — Sand Castle: parallel AFK agent orchestration

- Pocock introduces Sand Castle, a TypeScript library he built because he was unhappy with existing AFK agent-running options.
- Sand Castle:
  - Creates a git worktree.
  - Sandboxes it in Docker.
  - Runs prompts inside the worktree.
  - Lets branches be merged later.
- He walks through a `main.ts` file:
  - A planner reads backlog and chooses several issues to work on in parallel.
  - For each issue, it creates a sandbox.
  - It runs an implementer prompt with issue number, title, and branch.
  - If commits are created, a reviewer reviews them.
  - A merger agent receives branches and issues and merges them.
  - If merge produces type/test issues, the merger solves them.
- He says this has been his flow for most projects for a while and works very well.
- He uses Sonnet for implementation and Opus for reviewing because review needs more intelligence.

### 1:32:44–1:33:37 — Architecture scan result

- The architecture-improvement skill returns candidates.
- It identifies a quiz scoring service cluster and reordering logic extraction.
- It gives coupling arguments and dependency categories.
- It notes that the quiz scoring service currently has zero tests and calls that the biggest gap.
- This demonstrates what architecture-improvement output looks like: clusters, rationale, and testability opportunities.

### 1:33:37–1:36:04 — Final synthesis

- Pocock recaps the flow:
  - Bear the shape of the codebase in mind throughout.
  - Do not treat AI as a specs-to-code compiler.
  - Use grilling to hammer out the idea and alignment.
  - Do not overindex on the PRD.
  - Turn the destination into parallelizable issues.
  - Implement with agents.
  - QA and code-review heavily.
  - Feed QA findings back into the Kanban as more issues.
  - Share with team for full review when happy.
- He says the workflow is customizable and not meant as a one true way.
- He recommends reading older software-engineering books because pre-AI writing contains many principles that translate well into AI-assisted development.

## Open Questions

- What is the exact exercise repository URL shown on screen? The transcript references a link, but the prompt does not include it.
- What is the exact spelling/identity of the person from HumanLayer credited with the smart-zone/dumb-zone framing? The transcript appears to say “Dex Hy,” likely an auto-caption error.
- What is the exact origin and definition of “Ralph Wiggum” as a software practice? The talk assumes some audience familiarity.
- Is the claimed ~100k smart-zone threshold empirically measured, model-specific, or a personal heuristic?
- How much does compaction actually degrade coding quality compared with clearing across current models and tools?
- How safe is the practice of not reviewing generated PRDs in team or regulated environments?
- What is the best review strategy when agents produce more code than humans can review?
- How should teams balance small PRs with high-throughput AFK agent loops?
- What sandbox permissions are minimally sufficient for useful AFK coding while limiting blast radius?
- How should database migrations be handled in this workflow, especially when multiple agents generate migrations in parallel?
- How often do agent-generated vertical slices still hide horizontal coupling?
- Can the “improve codebase architecture” skill reliably distinguish useful deep modules from over-abstraction?
- Is Sand Castle public, private, or experimental? The transcript does not provide a URL.
- How should stale PRDs be archived so future agents can use historical intent without mistaking it for current truth?
- How should frontend visual QA evolve as multimodal browser agents improve?
- What metrics should teams track to know whether AI-assisted development is improving delivery rather than just increasing code volume?
- How should security, privacy, compliance, and API-contract constraints be added to the grilling and review workflows?
- How should agent prompts be adapted for non-TypeScript stacks, monorepos, mobile apps, data pipelines, or infrastructure-as-code?

## Experiments To Try

### Experiment 1: Token-status-line awareness

- **Hypothesis:** Showing exact token usage during coding sessions improves context hygiene and task sizing.
- **Context:** The speaker says token visibility is essential to know proximity to the dumb zone.
- **What to try:** Add a token/status line to the coding agent environment and record token levels at task success/failure.
- **Expected benefit:** Earlier context clearing and smaller tasks.
- **Risk:** Team over-focuses on token count rather than task quality.
- **Measurement:** Correlate token count with rework, test failures, review comments, and task completion.

### Experiment 2: Grill-me on a real ambiguous ticket

- **Hypothesis:** A grilling session reduces rework caused by hidden assumptions.
- **Context:** Demo gamification brief surfaces retroactivity, point sources, streaks, and UI location.
- **What to try:** Take one vague backlog item and run a one-question-at-a-time grilling prompt before implementation.
- **Expected benefit:** Better scope clarity and fewer mid-implementation interruptions.
- **Risk:** Session becomes too long or humans accept weak recommendations.
- **Measurement:** Count assumptions surfaced, follow-up questions avoided, and post-implementation scope changes.

### Experiment 3: PRD summarization fidelity check

- **Hypothesis:** LLM-generated PRDs preserve most important decisions from a grilling session but may drop edge cases.
- **Context:** Speaker often skips PRD review.
- **What to try:** Generate a PRD, then have a different agent or human compare it against the grilling transcript.
- **Expected benefit:** Identify whether skipping PRD review is safe for your team.
- **Risk:** Extra review undermines speed gains.
- **Measurement:** Missing decisions, hallucinated decisions, incorrect out-of-scope items.

### Experiment 4: Horizontal versus vertical issue slicing

- **Hypothesis:** Vertical tracer-bullet issues produce earlier useful feedback than horizontal layer issues.
- **Context:** Speaker rejects a schema/service-only first task as too horizontal.
- **What to try:** Split a small feature both ways and implement with agents in separate branches.
- **Expected benefit:** Faster integrated QA and less late rework.
- **Risk:** Vertical slices may be too broad for one context.
- **Measurement:** Time to first reviewable behavior, number of integration bugs, review effort.

### Experiment 5: Ralph once loop prompt tuning

- **Hypothesis:** Running one observed agent iteration reveals prompt/setup problems before AFK runs.
- **Context:** `once.sh` is the human-in-the-loop precursor to full AFK.
- **What to try:** Implement one issue with a once loop and document where the agent hesitates or makes poor decisions.
- **Expected benefit:** Better implementation prompt and issue format.
- **Risk:** Observed run looks fine but AFK loop fails later.
- **Measurement:** Task-selection accuracy, test pass rate, number of human interventions.

### Experiment 6: Agentic TDD versus implementation-first

- **Hypothesis:** Red-first TDD produces stronger tests and fewer bugs than implementation-first agent coding.
- **Context:** Speaker says AI cheats less when tests are written first.
- **What to try:** Assign similar issues to two agent workflows: one red-first, one implementation-first.
- **Expected benefit:** More reliable behavior and better regression tests.
- **Risk:** Agent writes superficial red tests or spends too long on test setup.
- **Measurement:** Mutation testing, bug-seeding detection, human review score for tests.

### Experiment 7: Fresh-context review

- **Hypothesis:** A fresh reviewer agent catches more issues than same-context self-review.
- **Context:** Speaker argues same-context review happens in the dumb zone.
- **What to try:** For several commits, run both same-session self-review and fresh-context review.
- **Expected benefit:** Higher-quality automated review.
- **Risk:** Fresh reviewer lacks implicit implementation context.
- **Measurement:** Accepted findings, duplicate/noise rate, defects found by later human review.

### Experiment 8: Manual QA feedback-to-Kanban loop

- **Hypothesis:** Converting QA findings into issues improves agent correction compared with ad hoc prompts.
- **Context:** Speaker says QA should add more issues to the Kanban.
- **What to try:** During QA, write each issue as a backlog item with blockers and AFK/HITL label.
- **Expected benefit:** Cleaner rework loop and better prioritization.
- **Risk:** Overhead for small fixes.
- **Measurement:** Reopened defects, fix cycle time, clarity of QA-to-implementation handoff.

### Experiment 9: Deep-module audit

- **Hypothesis:** Refactoring shallow clusters into deep modules improves agent success rate.
- **Context:** Speaker recommends trying the architecture-improvement skill on a repo.
- **What to try:** Run an architecture audit, pick one cluster, define a deeper interface, add tests, and refactor.
- **Expected benefit:** Easier future changes and better test boundaries.
- **Risk:** Misdesigned abstraction or risky refactor.
- **Measurement:** Future task file count touched, review complexity, test coverage, agent failure rate.

### Experiment 10: Interface-first delegation

- **Hypothesis:** Humans can preserve codebase understanding by designing module interfaces and delegating internals.
- **Context:** Speaker proposes gray-box modules as a way to retain sanity.
- **What to try:** For a new service, human writes the public interface and behavioral tests; agent writes internals.
- **Expected benefit:** Better architecture control with less manual coding.
- **Risk:** Interface underspecifies important behavior.
- **Measurement:** Human confidence in module, number of internal review comments, consumer-code simplicity.

### Experiment 11: Pull versus push standards

- **Hypothesis:** Pull-based standards for implementers plus pushed standards for reviewers balances context cost and enforcement.
- **Context:** Speaker recommends pull for implementer, push for reviewer.
- **What to try:** Store standards as retrievable skills/docs; push the same standards into review prompt only.
- **Expected benefit:** Cleaner implementation contexts and stricter reviews.
- **Risk:** Implementer may miss standards until review, causing rework.
- **Measurement:** Standards violations per PR, rework from review, token usage.

### Experiment 12: Frontend throwaway prototype route

- **Hypothesis:** AI-generated prototypes improve frontend requirements without contaminating production code.
- **Context:** Speaker recommends multiple clickable frontend prototypes for human selection.
- **What to try:** Ask agent for three UI variants behind a temporary route, then run a design/product review.
- **Expected benefit:** Faster visual exploration and clearer PRD.
- **Risk:** Prototype code gets reused uncritically.
- **Measurement:** UI rework after implementation, stakeholder preference clarity, accessibility issues found.

### Experiment 13: Closed-issue archive versus repo Markdown docs

- **Hypothesis:** Closed issues preserve historical context with lower doc-rot risk than old Markdown PRDs in the repo.
- **Context:** Speaker prefers closing GitHub issues instead of keeping stale PRDs visible in repo.
- **What to try:** For one project, store planning artifacts as issues and remove local plan files after merge.
- **Expected benefit:** Less stale context retrieved by agents.
- **Risk:** Agents may not fetch historical issues when useful.
- **Measurement:** Incidents where stale docs mislead agents, ease of reconstructing intent later.

## My Current Assessment

### What seems plausible

- The workflow’s strongest parts are grounded in durable engineering ideas: small tasks, tight feedback loops, test-first development, vertical slicing, modularity, and review.
- Treating early AI interaction as alignment rather than plan generation is a useful reframing.
- Vertical slices are likely better than horizontal slices for agent work because they generate earlier integration feedback.
- Fresh-context review is logically sound if context degradation is real.
- Deep modules and clear test boundaries are likely to improve both human and agent productivity.
- Manual QA as a taste-preserving step is important, especially for frontend/product work.

### What may be hype or overgeneralized

- The ~100k smart-zone boundary is presented as a personal heuristic, not a measured universal limit.
- “I do not review PRDs” may work for the speaker but could be risky in teams, regulated environments, or high-stakes domains.
- TDD is likely valuable, but “essential” may be too strong for all task types.
- AFK agents can ship code, but review burden and hidden defects may offset throughput gains.
- Deep-module refactoring can help, but agent-generated architecture advice can also over-abstract.

### What needs testing

- Quantitative relationship between token count and coding quality for the specific models/tools a team uses.
- Whether grilling reduces rework enough to justify its time cost.
- Whether generated PRDs faithfully preserve decisions.
- Whether vertical-slice issue DAGs improve parallel throughput without increasing merge conflicts.
- Whether automated reviewer agents catch enough meaningful issues to justify extra complexity.
- Whether Sand Castle-style parallel orchestration improves net delivery speed after review and QA are included.

### What might be useful later

- The “destination document” versus “journey document” distinction is a compact retrieval handle for the workflow.
- The “pull for implementer, push for reviewer” distinction is useful for managing coding standards.
- “Bad codebases make bad agents” is a useful diagnostic: when agents fail, inspect architecture and feedback loops before blaming only the model.
- “Design interfaces, delegate internals” is a practical way to preserve human ownership while using agents for volume.
- The issue DAG / Kanban framing is useful for any future parallel-agent system.

## Transcript Information

- **Transcript source:** User-provided transcript in prompt, apparently from YouTube captions or an extracted transcript.
- **Transcript quality:** Medium. It is mostly coherent and timestamped, but appears auto-transcribed and contains likely errors:
  - “claw” / “clawed” for Claude.
  - “Momento” for *Memento*.
  - “John Alistster/Asterhout” for John Ousterhout.
  - “npxv text” likely for `npx vitest`.
  - “canban/camon/came on” for Kanban.
  - “Ralph Wigum/Wiggum” variants.
  - Tool/framework names in audience questions are uncertain.
- **Transcript file if known:** Not provided.
- **Description file if known:** Not provided.
- **Metadata file if known:** Not provided.
- **Extraction date if known:** Not provided. Processed from prompt on 2026-05-09.
- **Chapters:** Not available. The prompt says no chapter markers in description and no video progress bar segments.
- **Video metadata provided:** URL, title, channel, published date, duration, description, transcript.

## References

### Explicitly Mentioned References

#### GitHub Repositories

- **Name:** `mattpocock/course-video-manager`
  
  - **URL if available:** https://github.com/mattpocock/course-video-manager
  - **Timestamp if available:** ~0:34:04
  - **Why it matters:** Speaker’s real work repo used to demonstrate his issue-based workflow, with hundreds of closed issues representing PRDs and implementation tasks.

- **Name:** Workshop exercise repository
  
  - **URL if available:** Not provided in prompt; shown on screen during workshop.
  - **Timestamp if available:** ~0:00:35, ~0:11:32
  - **Why it matters:** Contains the demo app, skills, scripts, and exercises used in the walkthrough.

- **Name:** Cadence demo course-platform repository
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:11:45
  - **Why it matters:** The course-management CMS where the gamification feature is implemented.

#### Websites / Documentation

- **Name:** YouTube video page
  
  - **URL if available:** https://www.youtube.com/watch?v=-QFHIoCo-Ko
  - **Timestamp if available:** Whole video.
  - **Why it matters:** Source video for this distillation.

- **Name:** Matt Pocock X profile
  
  - **URL if available:** https://x.com/mattpocockuk
  - **Timestamp if available:** Video description.
  - **Why it matters:** Speaker information provided in the video description.

- **Name:** AI Hero article on Claude Code status line
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:09:45
  - **Why it matters:** Speaker says the article explains how to copy his token status-line setup.

- **Name:** HumanLayer
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:03:14
  - **Why it matters:** Company associated with the smart-zone/dumb-zone framing attributed by the speaker.

- **Name:** Anthropic Claude / Claude Code documentation
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** Multiple mentions throughout.
  - **Why it matters:** Claude Code is the main agent environment used in the demo.

- **Name:** GitHub Issues documentation
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:33:51–0:34:39, ~1:23:34–1:25:03
  - **Why it matters:** Speaker’s preferred storage for PRDs/issues and mitigation for doc rot.

- **Name:** Docker documentation
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:54:21–0:55:37, ~1:29:54–1:30:24
  - **Why it matters:** Docker sandboxing is used for AFK agent execution.

- **Name:** tldraw / TLDraw
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:07:38
  - **Why it matters:** Speaker uses an infinite canvas instead of slides for diagrams.

#### Books

- **Name:** *Refactoring*
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:04:39
  - **Why it matters:** Cited as old software-engineering advice that aligns with keeping tasks small and avoiding excessive complexity.

- **Name:** *The Pragmatic Programmer*
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:04:46, ~0:41:57
  - **Why it matters:** Cited for classic advice and tracer bullets / vertical slices.

- **Name:** *The Design of Design*
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:16:55
  - **Why it matters:** Frederick P. Brooks source for the “design concept” / shared understanding framing.

- **Name:** *A Philosophy of Software Design*
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~1:13:39
  - **Why it matters:** John Ousterhout source for deep versus shallow modules.

- **Name:** *War and Peace*
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:38:03
  - **Why it matters:** Used only as an example of large-context retrieval, not as a technical source.

#### Papers

- **Name:** No papers explicitly identified in the transcript.
  - **URL if available:** Not applicable.
  - **Timestamp if available:** Not applicable.
  - **Why it matters:** The talk relies on books, tools, workflows, and speaker experience rather than named papers.

#### Tutorials / Blog Posts / Courses

- **Name:** Matt Pocock’s Claude Code course
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:37:41
  - **Why it matters:** Speaker says he recorded the course with a 200k context window and references it as part of his experience.

- **Name:** AI Hero token status-line article
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:09:45
  - **Why it matters:** Practical setup for seeing token usage during coding sessions.

- **Name:** Workshop exercises
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:00:35, ~0:11:32
  - **Why it matters:** Hands-on materials containing the repo, skills, and scripts.

#### Tools / Frameworks / APIs

- **Name:** Claude Code
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:09:19 and throughout.
  - **Why it matters:** Main coding-agent environment used for skills, planning, implementation, and permissions.

- **Name:** Claude Opus
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:17:38, ~1:32:33
  - **Why it matters:** Used by subagent/reviewer; speaker prefers Opus for review.

- **Name:** Claude Sonnet
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~1:32:33
  - **Why it matters:** Speaker uses Sonnet for implementation in his setup.

- **Name:** Claude subagents
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:17:38–0:18:30
  - **Why it matters:** Isolated context delegation pattern for exploration.

- **Name:** “Grill me” skill
  
  - **URL if available:** Not provided; in workshop repo.
  - **Timestamp if available:** ~0:12:15–0:17:31
  - **Why it matters:** Core alignment mechanism.

- **Name:** “Write a PRD” skill
  
  - **URL if available:** Not provided; in workshop repo.
  - **Timestamp if available:** ~0:30:30–0:32:26
  - **Why it matters:** Converts alignment conversation into destination document.

- **Name:** “PRD to issues” skill
  
  - **URL if available:** Not provided; in workshop repo.
  - **Timestamp if available:** ~0:44:07–0:45:17
  - **Why it matters:** Converts PRD into vertical-slice issues.

- **Name:** “Improve codebase architecture” skill
  
  - **URL if available:** Not provided; in workshop repo.
  - **Timestamp if available:** ~1:21:25–1:23:04
  - **Why it matters:** Scans codebase for opportunities to deepen modules and improve testability.

- **Name:** Sand Castle
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~1:29:47–1:32:39
  - **Why it matters:** Speaker’s TypeScript library for sandboxed parallel AFK agent orchestration.

- **Name:** GitHub Issues
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:33:51–0:34:39
  - **Why it matters:** Preferred place for PRDs and implementation issues in speaker’s workflow.

- **Name:** Git worktrees
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~1:30:12–1:30:24
  - **Why it matters:** Isolation mechanism for parallel agent branches.

- **Name:** Docker
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:54:21–0:55:37, ~1:30:12
  - **Why it matters:** Sandboxing mechanism for AFK/parallel agents.

- **Name:** TypeScript
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:36:36, ~1:10:39
  - **Why it matters:** Main language context; typechecking is part of feedback loop.

- **Name:** npm
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~1:10:33
  - **Why it matters:** Runs tests, typechecks, and database commands.

- **Name:** Vitest
  
  - **URL if available:** Not provided in transcript; transcript likely mistranscribes `npx vitest`.
  - **Timestamp if available:** ~1:08:06
  - **Why it matters:** Test runner used in demo.

- **Name:** SQLite
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~1:12:00
  - **Why it matters:** Demo database; missing table appears during QA.

- **Name:** Cucumber
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:32:12
  - **Why it matters:** Mentioned as a language/tool for writing user stories.

- **Name:** Playwright MCP
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~1:02:57
  - **Why it matters:** Example of giving agents browser/frontend inspection tools.

- **Name:** Agent Browser
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~1:02:57
  - **Why it matters:** Tool/category for AI frontend inspection; speaker says results are not yet good enough for mature frontend quality.

- **Name:** Gemini Meetings
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:21:27
  - **Why it matters:** Example meeting transcript source for grilling.

- **Name:** TLDraw / tldraw
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:07:38
  - **Why it matters:** Diagramming surface used instead of slides.

- **Name:** Slack
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:14:05
  - **Why it matters:** Source format for the sample client brief.

- **Name:** Slido
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:22:35
  - **Why it matters:** Audience Q&A and voting.

- **Name:** Spec Kit / “specit” (transcript uncertain)
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:23:24
  - **Why it matters:** Mentioned by an audience question as an alternative planning/spec framework.

- **Name:** OpenSpec / “open spec” (transcript uncertain)
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:23:24
  - **Why it matters:** Mentioned by an audience question as an alternative structured planning framework.

- **Name:** Taskmaster
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:23:24
  - **Why it matters:** Mentioned by an audience question as an alternative planning/task framework.

- **Name:** Beads framework
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~1:25:03
  - **Why it matters:** Audience asks about it as another way to manage Kanban/issues; speaker has not tested it.

- **Name:** Windows
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:19:27, ~0:32:32
  - **Why it matters:** Speaker’s laptop OS; mentioned jokingly as source of friction.

#### People / Channels / Companies

- **Name:** Matt Pocock
  
  - **URL if available:** https://x.com/mattpocockuk
  - **Timestamp if available:** Whole video; speaker info in description.
  - **Why it matters:** Speaker, teacher, and creator of the demonstrated workflow.

- **Name:** Matt Pocock channel / `@mattpocockuk`
  
  - **URL if available:** Not provided beyond YouTube URL and X profile.
  - **Timestamp if available:** Metadata.
  - **Why it matters:** Publishing channel for the video.

- **Name:** HumanLayer
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:03:14
  - **Why it matters:** Company associated with the smart-zone/dumb-zone framing.

- **Name:** Dex Horthy / “Dex Hy” (transcript uncertain)
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:03:14
  - **Why it matters:** Person credited with smart-zone/dumb-zone framing; exact name uncertain from transcript.

- **Name:** Martin Fowler
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:04:39
  - **Why it matters:** Cited for classic refactoring/small-task engineering advice.

- **Name:** Frederick P. Brooks
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:16:55
  - **Why it matters:** Cited for the “design concept” framing from *The Design of Design*.

- **Name:** John Ousterhout
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~1:13:39
  - **Why it matters:** Cited for deep modules versus shallow modules.

- **Name:** Steve (identity uncertain)
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:07:38 and/or ~1:25:03
  - **Why it matters:** Mentioned in relation to TLDraw and/or Beads; transcript does not provide enough context to identify confidently.

- **Name:** Sarah Chen
  
  - **URL if available:** Not applicable; appears to be demo persona.
  - **Timestamp if available:** ~0:14:05
  - **Why it matters:** Fictional/stub client in the sample brief requesting gamification.

- **Name:** Emma Wilson
  
  - **URL if available:** Not applicable; appears to be demo persona.
  - **Timestamp if available:** ~1:11:41
  - **Why it matters:** Demo student account used during QA.

- **Name:** Anthropic
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** Implied through Claude/Claude Code references.
  - **Why it matters:** Company behind Claude and Claude Code.

- **Name:** GitHub
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:33:51–0:34:39
  - **Why it matters:** Repository and issue platform central to the workflow.

- **Name:** Google / Gemini
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:21:27
  - **Why it matters:** Gemini Meetings is mentioned as an example transcript source.

- **Name:** Microsoft / Windows
  
  - **URL if available:** Not provided in transcript.
  - **Timestamp if available:** ~0:19:27, ~0:32:32
  - **Why it matters:** Windows laptop context; not technically central to the workflow.

- **Name:** Mike and Mark
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:00:42, ~0:22:15
  - **Why it matters:** Logistical/event names mentioned during room setup; no technical relevance.

- **Name:** Ralph Wiggum
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:06:39
  - **Why it matters:** Namesake for the “Ralph” loop/practice of repeatedly making small changes toward a destination.

- **Name:** *Memento* / protagonist comparison
  
  - **URL if available:** Not provided.
  - **Timestamp if available:** ~0:07:25
  - **Why it matters:** Analogy for LLM sessions continually resetting/forgetting.

### Related / Inferred References

These are not explicitly cited as references in the transcript, but they are useful context for reconstructing or validating the technical ideas.

- **Name:** Walking skeleton
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Related to ~0:41:57–0:45:11.
  - **Why it matters:** Closely related to tracer bullets and vertical slices: build a minimal end-to-end path early.

- **Name:** Continuous Integration (CI)
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Related to test/typecheck feedback loops around ~1:09:45–1:10:57.
  - **Why it matters:** The workflow depends on reliable automated feedback that CI commonly provides.

- **Name:** Contract testing
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Related to deep modules and interfaces around ~1:17:02–1:20:57.
  - **Why it matters:** Useful technique for testing module interfaces while delegating internals.

- **Name:** Mutation testing
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Related to TDD/test quality around ~1:06:41–1:08:34.
  - **Why it matters:** Possible way to validate whether agent-written tests are meaningful or superficial.

- **Name:** Architectural Decision Records (ADRs)
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Related to PRDs, negative decisions, and doc rot around ~0:28:38–0:36:00 and ~1:23:34–1:25:03.
  - **Why it matters:** ADRs may preserve decisions while reducing ambiguity, but would need doc-rot controls.

- **Name:** RFC-style design review
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Related to team feedback around ~1:00:27–1:02:15.
  - **Why it matters:** Team setting for arguing over destination/journey artifacts before AFK implementation.

- **Name:** Playwright end-to-end tests
  
  - **URL if available:** Inferred from Playwright MCP mention; no URL.
  - **Timestamp if available:** Related to frontend QA around ~1:02:32–1:03:47.
  - **Why it matters:** Could supplement manual frontend QA, though speaker says AI visual judgment remains weak.

- **Name:** OpenTelemetry / observability
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Not directly mentioned.
  - **Why it matters:** For production features, feedback loops should extend beyond tests into runtime observability; this is a likely next layer not covered in the talk.

- **Name:** Security review checklists
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Related to audience question at ~1:03:53–1:04:25.
  - **Why it matters:** Security constraints should be pushed into reviewer context or asked during grilling.

- **Name:** Dependency graph scheduling / topological sort
  
  - **URL if available:** Inferred; no URL.
  - **Timestamp if available:** Related to issue DAG around ~0:49:40–0:51:14 and Sand Castle planner around ~1:30:51–1:31:16.
  - **Why it matters:** Formal way to choose unblocked tasks for sequential or parallel agent execution.
