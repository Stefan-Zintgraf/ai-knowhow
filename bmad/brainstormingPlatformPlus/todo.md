
# TODO

check rethinking folder (the current plan may be over-engineered)

How to continue later:
Start a new chat and run the same command: /bmad-bmm-create-prd
The workflow's step 1 will detect the existing PRD file at _bmad-output/planning-artifacts/prd.md, read its frontmatter, see that steps are completed but step-11-complete is not yet in the list, and automatically trigger the Continuation Protocol — picking up right where you left off (Step 3: Success Criteria).



# Strategy: tick-md Integration for Post-MVP Phases (enhance brainstorming session)

**Document Intent:** To define the architectural integration of `tick-md` as the core orchestration and concurrency engine for Phase V1 (Autonomous Pipeline) and Phase V2 (Multi-Agent Brainstorming), replacing custom-built routing mechanisms.

---

## 1. Phase Alignment: Why `tick-md` is Excluded from POC/MVP

Introducing `tick-md` during the POC or MVP phases would violate the "Filesystem-as-Truth Principle" established in your SCAMPER session (Lens 3, A-5 & Lens 6, E-1). 

**Rationale for Exclusion:**
* **MVP Goal:** Establish a rock-solid, single-agent REPL loop driven by a deterministic Python Spec Runner. 
* **MVP Complexity:** The MVP must validate the core `topic.md` and `session.md` data structures and the BMad hybrid integration (Strategy C). Adding `tick-md` introduces Git-dependency and file-locking overhead before the core brainstorming data contracts are proven.
* **Verdict:** The Python Spec Runner handles the DAG resolution for MVP. `tick-md` is strictly reserved for when multiple independent agents require asynchronous coordination (V1 and V2).

---

## 2. V1 Strategy: The Autonomous Build & Test Pipeline (Ideas #71–92, #123–130)

In Phase V1, the platform transitions from a single human-triggered Python script to a multi-role AI pipeline. `tick-md` replaces the custom dependency DAG resolver of your MVP Spec Runner.

### 2.1 Mapping Ideas to `tick-md`
* **Idea #78 (Role Separation):** The Architect, Builder, and Tester agents operate as independent workers monitoring the same workspace via the MCP server.
* **Idea #126 (Autonomous Build Loop):** Instead of a Python script forcing the loop, `tick-md` handles the state transitions. 
    * Architect agent creates a `[ ]` task in `TICK.md` pointing to `specs/SPEC-040.md`.
    * Builder agent claims it `[>]`.
    * Builder completes it `[x]`, which automatically unblocks the Tester agent's task.
* **Idea #125 (Spec-Driven Development):** Spec files remain the single source of truth, but `TICK.md` becomes the execution ledger.

### 2.2 Execution Flow
1. **Initiation:** The human user adds a high-level feature request to `TICK.md`.
2. **Architecture:** The Architect agent reads it, generates the necessary `SPEC-XXX.md` files, and writes dependent sub-tasks into `TICK.md`.
3. **Build & Test:** Builders and Testers lock files via Git, complete the specs, and log results to `verification-log.md`.
4. **Phase Gate (#127):** `tick-md` triggers a blocked "Human Review" task when all sub-tasks pass Layer 1 and Layer 2 tests.

---

## 3. V2 Strategy: Multi-Agent Brainstorming (Ideas #109–118)

Phase V2 introduces the most complex feature: multiple AI personas brainstorming concurrently. `tick-md` eliminates the need for custom filesystem routing.

### 3.1 Retiring POC/MVP Concepts
* **Retire Idea #110 (Agent Mailbox Protocol):** Custom `inbox/` and `private/` folders are unnecessary. Agents use `tick-md` task assignments and Git commits to pass context.
* **Retire Idea #116 (Orchestrator Script):** No master bash/Python script is needed to dictate turn order. Turn order is enforced by `tick-md` dependency chains (e.g., Task B cannot start until Task A is marked `[x]`).

### 3.2 The Multi-Agent Workflow
* **The Leader Agent (#112):** Acts as the project manager. It analyzes the `topic.md`, selects a BMad technique, and writes the required steps into `TICK.md`.
* **Concurrent Ideation:** If the technique calls for "Generate 10 SCAMPER variations," the Leader assigns tasks to the "Critic" persona and "Enthusiast" persona simultaneously.
* 
* **Collision Prevention:** Because `tick-md` requires agents to "claim" tasks and uses Git to sync, the Critic and Enthusiast can write to the `session.md` file (or temporary round files) without overwriting each other's tokens.
* **Compaction (#114):** Once all assigned ideation tasks are checked off, the dependency chain unblocks the Leader's "Compaction and Synthesis" task.

---

## 4. Example `TICK.md` State for a V2 Brainstorming Session

Here is how the platform's orchestration layer will look during a live multi-agent SCAMPER session:

```markdown
# Topic: Multi-Topic Dashboard Redesign
**Phase:** V2 Brainstorming - SCAMPER Step 1

- [x] @leader: Analyze topic.md and initialize BMad technique (SCAMPER)
- [x] @leader: Draft baseline PRD template in session.md
- [>] @enthusiast: GENERATE - Apply "Substitute" lens to UI constraints (Working...)
- [ ] @critic: CHALLENGE - Apply "Eliminate" lens to current feature set
  - Depends on: @leader baseline completion
- [ ] @logical: SYNTHESIZE - Merge Enthusiast and Critic outputs into session.md
  - Depends on: @enthusiast GENERATE
  - Depends on: @critic CHALLENGE
- [ ] @leader: Run Diminishing Returns Detector (#118) and determine next round
  - Depends on: @logical SYNTHESIZE


## 5. Migration Path (MVP → V1)

1. **Retain the Spec Runner:** Keep the MVP Python Spec Runner strictly for Layer 1 mechanical tests. 
2. **Install `tick-md`:** Add the `TICK.md` file to the platform root.
3. **Connect MCP:** Spin up the `tick-md` MCP server so the CLI agents (Claude/Gemini) can natively read/write task states.
4. **Delegate Orchestration:** Strip the DAG resolution logic out of your Python script and allow the agents to self-orchestrate using the `TICK.md` ledger.