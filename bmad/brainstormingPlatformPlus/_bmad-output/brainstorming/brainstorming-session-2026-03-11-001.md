---
stepsCompleted: [1, 2, 3]
inputDocuments: []
session_topic: 'Designing a BMad-powered brainstorming platform for Claude Desktop and other AI tools'
session_goals: 'Platform architecture, UX/interaction design, multi-topic folder management, BMad workflow integration with MD file storage, AI-agent testability, portability across AI tools'
selected_approach: 'ai-recommended'
techniques_used: ['First Principles Thinking', 'SCAMPER Method (POC-scoped)']
techniques_remaining: ['Solution Matrix']
ideas_generated: 134
scamper_decisions: 30
new_ideas_from_scamper: 4
design_principles_established: 5
technique_execution_complete: false
facilitation_notes: 'Session 1: Deep First Principles (104 ideas). Session 2: User added 30 ideas across 4 new categories. Session 3: POC scope defined, roadmap framed (POC/MVP/V1/V2), SCAMPER applied to 26 POC ideas — 30 decisions across 7 lenses, 5 new design principles established, significant simplification achieved (5 files eliminated/merged, TDD build order adopted, convention-over-configuration principle, AI-generative brainstorming mode added). Session 4: POC roadmap detailed — 5 build phases with spec dependency DAG, dual-mode execution model (script-first), hybrid BMad integration (strategy C), sophisticated Python spec runner, AI Test User Agent (single-invocation), spec files from day one (dogfooding).'
session_state: 'poc_roadmap_detailed_solution_matrix_next'
next_action: 'Solution Matrix for MVP/V1/V2 idea allocation, then finalize spec file format (SPEC-000) and begin Phase 1 spec writing'
session_continued: true
continuation_date: '2026-03-11'
context_file: ''
write_status: complete
---

# Brainstorming Session Results

**Facilitator:** Stefan
**Date:** 2026-03-11

## Session Overview

**Topic:** Designing a BMad-powered brainstorming platform for Claude Desktop and other AI tools
**Goals:** Platform architecture, UX/interaction design, multi-topic folder management, BMad workflow integration with MD file storage, AI-agent testability, portability across AI tools

### Session Setup

The user wants to create a brainstorming platform that:
- Uses the BMad brainstorming method in Claude Desktop (Cowork or Code mode)
- Stores all results as Markdown files
- Supports multiple independent brainstorming topics, each in its own folder
- Each topic optionally accepts one or multiple input knowledge base folders
- Results serve as starting points for new or brownfield coding projects
- The primary consumer of output is AI (Claude, etc.), not just humans
- Must be portable across AI tools (ChatGPT, Gemini, OpenClaw)
- Must be testable by AI agents using synthetic brainstorming topics
- The platform itself should be buildable by AI agents

## Technique Selection

**Approach:** AI-Recommended Techniques
**Analysis Context:** Platform design challenge requiring foundational clarity, wide divergent ideation, then structured convergence

**Recommended Techniques:**

1. **First Principles Thinking** — Strip assumptions, rebuild from bedrock truths (COMPLETED — 104 ideas)
2. **SCAMPER Method** — Systematically challenge and transform ideas through 7 lenses (NEXT SESSION)
3. **Solution Matrix** — Map intersecting platform dimensions to find optimal combinations (PENDING)

---

## Technique Execution Results

### First Principles Thinking (104 Ideas)

**Interactive Focus:** Rebuilt the platform concept from bedrock truths across 10+ domains
**Key Breakthrough:** The platform is not a brainstorming tool — it's a persistent AI workspace where brainstorming is one activity. The knowledge graph, lifecycle states, and cross-references are infrastructure for long-lived AI-assisted thinking.
**User Creative Strengths:** Strong architectural instinct, repeated pattern of introducing pivotal constraints (portability, testability) that expanded the design space significantly
**Energy Level:** Sustained high energy across 100+ ideas

---

### Category 1: Core Design Principles (Ideas #1–12)

**[#1]: The Output-as-Prompt Principle**
_Concept:_ Every brainstorming MD file is a pre-structured prompt artifact. Format, headings, and idea density are optimized for how AI ingests context, not how humans scan notes.
_Novelty:_ Most tools optimize output for human review. This inverts it — the human produces, the AI consumes.

**[#2]: The Self-Orienting Knowledge Base**
_Concept:_ Each topic folder contains a `knowledge_base_overview.md` as Claude's entry point. If missing, Claude traverses all files/subfolders and synthesizes it. A manual "rebuild overview" command triggers regeneration after adding new documents.
_Novelty:_ The knowledge base documents itself — the AI maintains the index, not the human.

**[#3]: The Accumulating Memory Pattern**
_Concept:_ Completed brainstorming sessions are offered for inclusion in the knowledge base after each session. Over time, the topic folder becomes a layered archive of every ideation cycle.
_Novelty:_ Turns ephemeral brainstorming into persistent project intelligence. The "why" behind decisions survives.

**[#4]: Human-Claude Co-Authorship Model**
_Concept:_ All AI-generated files carry `source: ai-generated` frontmatter and are treated as "draft" until confirmed by the user. A `status: confirmed` flag promotes them to trusted knowledge.
_Novelty:_ Epistemic hygiene layer — the system always knows what it knows with certainty vs. what it inferred.

**[#5]: Zero-Friction Entry**
_Concept:_ A topic can be born with nothing but a name. Empty knowledge base is a valid starting state, not an error condition.
_Novelty:_ Thinking comes first, knowledge base grows around it.

**[#6]: The Knowledge Gap Advisor**
_Concept:_ After the user states their topic, Claude proactively suggests what types of knowledge would enrich the session. User can pause to add these or proceed with what they have.
_Novelty:_ AI acts as a preparation coach before ideation — it knows what it doesn't know and tells you.

**[#7]: The Staged Knowledge Handshake**
_Concept:_ An explicit "knowledge enrichment gate" between topic setup and brainstorming start. Claude presents a checklist of suggested knowledge types, user marks which they have/will add/skip. Gaps are tracked in frontmatter and visible during ideation.
_Novelty:_ Makes knowledge gaps explicit objects. Claude can flag ideas that depend on missing knowledge.

**[#8]: The Topic Lifecycle State Machine**
_Concept:_ Each topic has an explicit lifecycle: `exploring` → `converging` → `actionable` → `archived`. Claude adapts facilitation style based on state. User can manually override.
_Novelty:_ Prevents brainstorming from never ending — shared understanding of "done enough."

**[#9]: Topic Type Classification Gate**
_Concept:_ Before brainstorming, Claude asks "What kind of challenge is this?" — Project / Problem / Decision / Domain / Exploration. The answer shapes facilitation, knowledge suggestions, lifecycle expectations, and folder template.
_Novelty:_ Topic type is a first-class design parameter. Same engine, radically different behavior per type.

**[#10]: The Topic Knowledge Graph**
_Concept:_ Each topic folder has optional `topic_references.md` linking to sibling topics. Claude traverses references and pulls relevant context. References are directional and typed (informs / depends-on / contradicts / extends).
_Novelty:_ Topics become nodes in a living knowledge graph, not isolated silos.

**[#11]: The Cross-Topic Insight Broker**
_Concept:_ During brainstorming, when an idea belongs in another topic's knowledge base, Claude flags it in real-time for cross-reference. User approves or dismisses. The graph grows organically through brainstorming.
_Novelty:_ Brainstorming actively maintains the knowledge graph.

**[#12]: The Shared Knowledge Base Layer**
_Concept:_ A top-level `_shared/` folder holds documents that apply across multiple topics. Any topic references it automatically. Claude checks it during every session.
_Novelty:_ Eliminates knowledge duplication across topics. One truth, many consumers.

---

### Category 2: Brownfield & Code Integration (Ideas #13–16, #23–25)

**[#13]: The Brownfield Ingestion Protocol**
_Concept:_ A structured "knowledge extraction" workflow for brownfield projects. Claude walks the project and produces synthesized MD summaries — architecture overview, key dependencies, existing patterns, pain points. Raw code stays in place; extracted intelligence enters the KB.
_Novelty:_ Source code is a data source to be processed, not a document to be read directly.

**[#14]: The Living Codebase Mirror**
_Concept:_ Optional sync mechanism re-scans the project folder and updates KB summaries when significant changes detected. `knowledge_base_overview.md` carries `last_synced` timestamp.
_Novelty:_ The knowledge base tracks drift — Claude knows how stale the picture is.

**[#15]: The Contradiction Detection Engine**
_Concept:_ When a topic's conclusions are updated, Claude checks all referencing topics and flags contradictions. A `knowledge_conflicts.md` surfaces tensions explicitly.
_Novelty:_ Contradictions become visible objects to be resolved, not silently accumulating.

**[#16]: The Assumption Registry**
_Concept:_ Every topic maintains `assumptions.md` — things the brainstorming took as given. Claude flags unregistered assumptions during ideation. Assumptions marked `verified`, `unverified`, or `challenged`.
_Novelty:_ Makes invisible scaffolding of brainstorming into an explicit, auditable artifact.

**[#23]: The GitHub Bootstrap Workflow**
_Concept:_ "Import from repo" command accepts a local path or GitHub URL. Claude performs structured repo analysis and outputs a pre-populated knowledge base.
_Novelty:_ Developer goes from raw repo to brainstorming context in one command.

**[#24]: The Selective Repo Lens**
_Concept:_ User specifies a focus area — "authentication", "data layer", "API contracts" — and Claude extracts only relevant knowledge. Same repo, different knowledge bases for different topics.
_Novelty:_ One repo, many perspectives. KB reflects the question being asked.

**[#25]: The Code-to-Insight Extractor**
_Concept:_ Claude translates code observations into architectural insights rather than storing code snippets. "The auth layer couples session management with user persistence" instead of raw class definitions.
_Novelty:_ Bridges "what the code does" and "what that means for future decisions."

---

### Category 3: Session Continuity & Recovery (Ideas #17–19, #26–28, #31, #45)

**[#17]: The Session Re-Entry Briefing**
_Concept:_ When opening an existing topic, Claude generates a 5-bullet synthesis: (1) what topic is about, (2) where last session left off, (3) decided vs. open, (4) KB changes since last session, (5) suggested next steps.
_Novelty:_ Solves the cold start problem — user orients in 10 seconds, not 20 minutes.

**[#18]: The Decision Log**
_Concept:_ `decisions.md` is a running ledger of conclusions — what, when, why, which session. Claude auto-appends after convergence moments. Humans can add manually.
_Novelty:_ Preserves both the journey and the destination.

**[#19]: The Claude Desktop Mode Split**
_Concept:_ In Cowork mode: conversational guidance. In Code mode: direct file read/write, folder traversal without asking. Same workflow adapts interaction pattern.
_Novelty:_ Two distinct UX modes matched to how the user is working.

**[#26]: The Intra-Topic Contradiction Surfacer**
_Concept:_ Claude scans session archives for conflicting conclusions and surfaces them in the re-entry brief. Contradictions are first-class agenda items.
_Novelty:_ Most recent idea doesn't silently win — evolution of thinking is visible and intentional.

**[#27]: The Idea Versioning Model**
_Concept:_ Ideas that evolve across sessions are linked with `PREV:` frontmatter. Claude traverses version chains to explain how thinking evolved.
_Novelty:_ Preserves reasoning behind position changes, not just final position.

**[#28]: The Devil's Advocate Pass**
_Concept:_ Optional pre-session step where Claude argues against current direction, surfaces weakest assumptions, identifies untested ideas.
_Novelty:_ Institutionalizes intellectual challenge as recurring practice.

**[#31]: The Stateless Resume Protocol**
_Concept:_ `session_state.md` — machine-readable file updated at session end: last action, current workflow stage, open threads, next step. Always the first file read.
_Novelty:_ File system becomes the memory layer that conversation history can't be.

**[#45]: The Session Crash Checkpoint**
_Concept:_ Claude periodically writes checkpoints to `session_state.md` during long sessions. Interrupted sessions can resume from last checkpoint.
_Novelty:_ Software engineering's checkpointing pattern applied to conversational workflows.

---

### Category 4: Context Window Management (Ideas #20–22)

**[#20]: The Tiered Context Loading Model**
_Concept:_ Knowledge loaded in concentric rings. Ring 1 (always): overview, decisions, assumptions. Ring 2 (on demand): specific session files. Ring 3 (never auto-loaded): raw sources, full archives. Each ring has a size budget.
_Novelty:_ Context management is an explicit, visible design principle, not a hidden constraint.

**[#21]: The Compact Summary Discipline**
_Concept:_ Every AI-generated file has a full version and a `_summary` frontmatter block (max 200 words). Orientation layer built exclusively from summaries.
_Novelty:_ Forces distillation at write time, not read time. Claude summarizes while it has full context.

**[#22]: The Knowledge Pruning Prompt**
_Concept:_ When a topic exceeds a content threshold, Claude offers a "pruning" session — reviews all content, proposes archiving superseded or irrelevant files. `_archive/` subfolder holds pruned content.
_Novelty:_ Actively manages knowledge debt. Accumulation is a liability as well as an asset.

---

### Category 5: Navigation & Topic Management (Ideas #29–36)

**[#29]: The Platform Invocation Pattern**
_Concept:_ Single trigger (`/brainstorm`) → Claude lists topics → user picks or creates new. Zero-UI design. Folder structure is the interface, conversation is the UX.
_Novelty:_ No app, no web interface. The folder structure is the UI.

**[#30]: The Topic Creation Ceremony**
_Concept:_ 4-beat sequence: (1) Name it, (2) Type it, (3) Seed it (existing knowledge or fresh?), (4) Brief it (3-sentence charter). Charter becomes first `decisions.md` entry.
_Novelty:_ Fast (2 min) but intentional. Creates shared contract between user and AI.

**[#32]: The Platform Root Index**
_Concept:_ Top-level `_index.md` lists all topics: name, type, state, last session date, summary, open thread count. Auto-maintained by Claude at session close.
_Novelty:_ A Markdown dashboard. Ambient awareness of the entire thinking portfolio.

**[#33]: The Open Threads System**
_Concept:_ Interesting tangents captured as one-line stubs in `open_threads.md`. At session close, Claude reviews: promote, archive, or dismiss.
_Novelty:_ Built-in capture for "interesting but not now" moments.

**[#34]: The Cross-Topic Navigation Command**
_Concept:_ Mid-session pivot: "this connects to topic X." Claude offers cross-reference, context pull, or insight transfer — without ending the current session.
_Novelty:_ In-session graph navigation. Thinking flows across topics fluidly.

**[#35]: The Asynchronous Collaboration Model**
_Concept:_ Multiple users contribute via files. Git is the collaboration layer. No accounts, no sharing settings. Pull requests review knowledge base changes.
_Novelty:_ Collaboration is file-based, not platform-based.

**[#36]: The Attribution Model**
_Concept:_ Optional `author:` frontmatter for provenance. Claude surfaces attribution when relevant in re-entry briefs.
_Novelty:_ Lightweight provenance without user management systems.

---

### Category 6: Handoff & BMad Integration (Ideas #37–38, #48–49)

**[#37]: The Handoff Synthesis Command**
_Concept:_ `/synthesize` triggers output generation: Claude reads entire topic and produces a structured handoff — PRD for Projects, ADR for Decisions, domain model for Domains.
_Novelty:_ Closes the loop between brainstorming and action.

**[#38]: The BMad Workflow Bridge**
_Concept:_ Handoff output is explicitly formatted for BMad downstream workflows (Create PRD, Create Architecture, Implement Story). Brainstorming becomes the upstream thinking layer of the full BMad lifecycle.
_Novelty:_ Ideation and implementation become a continuous pipeline.

**[#48]: The BMad-Native Installation**
_Concept:_ Platform installs as a BMad core workflow. Installer handles setup: creates directories, generates config from existing BMad config, registers commands. Zero manual setup.
_Novelty:_ First-class BMad citizen inheriting identity, language, output conventions.

**[#49]: The Workflow Upgrade Path**
_Concept:_ Version in `config.yaml`. On mismatch, platform offers migration. Upgrades non-destructive — workflow files change, user data never touched.
_Novelty:_ Platform code and platform data separated cleanly enough for safe automatic upgrades.

---

### Category 7: Folder Structure & Configuration (Ideas #39–47)

**[#39]: The Canonical Topic Folder Structure**
_Concept:_ Predictable, Claude-readable layout:
```
_brainstorm/
├── _index.md
├── _shared/
├── config.yaml
├── tools/
│   ├── claude-desktop.md
│   ├── chatgpt.md
│   ├── gemini.md
│   └── openclaw.md
└── topics/
    └── [topic-slug]/
        ├── topic.yaml
        ├── session_state.md
        ├── decisions.md
        ├── assumptions.md
        ├── open_threads.md
        ├── knowledge_conflicts.md
        ├── knowledge_base/
        │   ├── knowledge_base_overview.md
        │   ├── topic_references.md
        │   └── [input documents]
        ├── sessions/
        │   └── session-YYYY-MM-DD-NNN.md
        └── _archive/
```
_Novelty:_ File location tells Claude what it is and how to use it. Self-documenting structure.

**[#40]: The `topic.yaml` as Platform Nerve Center**
_Concept:_ Small YAML: name, type, state, created, last_session, author, open_thread_count, session_count, kb_last_synced, references. Always read first.
_Novelty:_ Machine-readable metadata separated from human-readable content.

**[#41]: The Naming Convention as Protocol**
_Concept:_ Sessions: `session-YYYY-MM-DD-NNN.md`. Archives prefix `archived-YYYY-MM-DD-`. Kebab-case for knowledge files. No spaces, no version suffixes.
_Novelty:_ Naming conventions become a communication protocol between file system and AI.

**[#42]: The Partial Write Recovery**
_Concept:_ Every write begins with `write_status: in_progress`, updated to `complete` on success. Crash detection on next open with recovery offer.
_Novelty:_ Files carry their own integrity signal.

**[#43]: The Knowledge Base Integrity Check**
_Concept:_ `/check` command triggers full health scan: missing files, orphaned references, stale overviews, old open threads. Triage report with fixes and flags.
_Novelty:_ The platform can audit itself proactively.

**[#44]: The Graceful Misread Protocol**
_Concept:_ Unparseable files are never silently skipped. Claude narrates the issue, degrades gracefully, and suggests fixes. Session continues with honest context.
_Novelty:_ Failure is always visible, never silent.

**[#46]: The Platform `config.yaml`**
_Concept:_ Root-level config: default_topic_type, context_ring1_max_tokens, kb_sync_interval_days, session_checkpoint_interval, contradiction_check_on_open, pruning_threshold_sessions, handoff_format, bmad_integration_enabled. Optional with sensible defaults.
_Novelty:_ Self-configuring by default, fully customizable without code.

**[#47]: The Per-Topic Config Override**
_Concept:_ Each `topic.yaml` can override platform-wide config. Platform → Topic → Session inheritance with selective overrides.
_Novelty:_ Environment override pattern from software engineering applied to knowledge management.

---

### Category 8: Portability & Tool Adapters (Ideas #50–59, #62–64, #70)

**[#50]: The AI-Agnostic Platform Principle**
_Concept:_ Core rule: never encode capability only one AI tool can execute. All state in files, all instructions in Markdown. The AI is a replaceable runtime.
_Novelty:_ The platform outlives any specific AI tool. Thinking is never locked in.

**[#51]: The Tool Capability Profile**
_Concept:_ `tools/` folder with one adapter file per AI tool documenting capabilities: file access method, context window size, multi-file handling, tool use availability. Claude reads its own adapter to calibrate behavior.
_Novelty:_ Same workflow, tool-aware execution. Adding a new AI = writing one adapter file.

**[#52]: The File Access Abstraction Layer**
_Concept:_ Two modes: Direct (AI reads/writes files natively) and Assisted (AI outputs content for user to save manually). Workflow identical; write mechanism differs.
_Novelty:_ Portability without lowest-common-denominator design.

**[#53]: The Universal Invocation Protocol**
_Concept:_ Paste contents of `WORKFLOW.md` into any new conversation. One file, universal entry point. No plugins, no extensions required.
_Novelty:_ Platform "install" on any AI tool = copy one file's contents.

**[#54]: The Context Window Normalization**
_Concept:_ Ring 1 budget configured as percentage of available context. Tool adapter declares `context_window_tokens`. Platform scales automatically per host AI.
_Novelty:_ Context loading adapts to host AI capacity.

**[#55]: The Workflow Instruction Format Contract**
_Concept:_ All workflow files use plain Markdown, no tool-specific syntax, unambiguous imperatives, explicit decision trees. Documented in `WORKFLOW_FORMAT.md`.
_Novelty:_ Workflow instructions as a portable programming language for LLMs.

**[#56]: The Tool-Specific Enhancement Layer**
_Concept:_ Optional enhancements activate when native capabilities exist — extended thinking, massive context windows, specific tool-use patterns. Progressive enhancement borrowed from web dev.
_Novelty:_ Degrades gracefully on simpler tools, accelerates on powerful ones. Same codebase.

**[#57]: The Human-as-Filesystem Fallback**
_Concept:_ For zero-file-access tools: AI outputs every write explicitly, maintains session clipboard, outputs file update checklist at session end. Human becomes the file system.
_Novelty:_ No AI tool is excluded. Tedious but functional. Overhead disappears as tools gain file access.

**[#58]: The Portability Test Suite**
_Concept:_ `tests/` folder with synthetic scenarios and correct behavior checklists. Pass/fail per tool documented in `tools/compatibility-matrix.md`.
_Novelty:_ "Does this work on Gemini?" has a concrete, reproducible answer.

**[#59]: The Separation of Concerns Trinity**
_Concept:_ Three layers: (1) Knowledge Layer — files, YAML, fully AI-agnostic. (2) Workflow Layer — Markdown instructions, portable with adapters. (3) Runtime Layer — the AI tool, replaceable. Changes to one don't require changes to others.
_Novelty:_ Explicitly enforced separation prevents lock-in.

**[#62]: The Tool Switching Invariant**
_Concept:_ Any AI tool can pick up any topic, cold, from files alone. Tool switching is zero-cost by design.
_Novelty:_ Switching AI tools is as simple as switching text editors.

**[#63]: The Tool Switch Handoff Note**
_Concept:_ Optional `tool_handoff.md` captures conversational context not yet in files. Ephemeral — overwritten each session close.
_Novelty:_ Bridges the gap between conversational context (doesn't transfer) and file context (does).

**[#64]: The Tool Fidelity Downgrade Path**
_Concept:_ When a less-capable tool opens a topic built with a more capable one, the platform narrates the difference explicitly. No features break silently.
_Novelty:_ Capability differences are visible, not mysterious.

**[#70]: The Cross-Platform Session Continuity Signal**
_Concept:_ Re-entry brief explicitly acknowledges tool changes: "Last session on Claude Desktop (5 days ago), you were mid-SCAMPER." Continuity is a file property, not tool property.
_Novelty:_ User feels like they never left, even on a different AI tool.

---

### Category 9: AI Agent Build & Test Pipeline (Ideas #71–82, #83–92)

**[#71]: The AI-Executable Specification**
_Concept:_ Requirements written in BDD Given/When/Then format — readable as human requirements AND executable as AI tests. Specification is the test suite.
_Novelty:_ No separate test document to maintain.

**[#72]: The Synthetic Topic Test Harness**
_Concept:_ `tests/` folder with scenario folders: empty-topic, rich-topic, conflicted-topic, brownfield-topic, cross-referenced-topic. AI agent runs each and checks against spec.
_Novelty:_ Tests are first-class platform artifacts, runnable by any AI agent.

**[#73]: The Automated Build Spec**
_Concept:_ `BUILD.md` contains complete ordered instructions for an AI agent to build the platform from scratch. AI reads and executes step by step.
_Novelty:_ Platform bootstraps via AI. BUILD.md is infrastructure-as-code for AI agents.

**[#74]: The Test Oracle Pattern**
_Concept:_ Each test includes expected behavior oracle precise enough for AI self-evaluation. Removes human judgment from test evaluation.
_Novelty:_ AI can evaluate its own or another AI's execution objectively.

**[#75]: The Regression Test Trigger**
_Concept:_ Workflow file modifications flag affected tests for re-run. `CHANGELOG.md` tracks impact. Targeted testing, not full suite.
_Novelty:_ CI/CD thinking for AI workflow development.

**[#76]: The Dogfooding Bootstrap**
_Concept:_ Platform built using itself. First topic: "Build the Brainstorming Platform." This brainstorming session's output directly feeds BUILD.md and specs.
_Novelty:_ Building the platform is the ultimate integration test.

**[#77]: The Acceptance Criteria Library**
_Concept:_ `specs/` folder with one file per capability. 5-10 Given/When/Then criteria each. Runnable individually or as full suite. Specs written before implementation.
_Novelty:_ Spec-first, AI-executable development.

**[#78]: The AI Agent Build Role Separation**
_Concept:_ Three roles: Architect Agent (brainstorming → specs + BUILD.md), Builder Agent (BUILD.md → platform files), Tester Agent (specs → test runs → verification). Roles separable across agents.
_Novelty:_ Multi-agent pipeline where builder doesn't test their own work.

**[#79]: The Continuous Verification Loop**
_Concept:_ Change → Tester runs affected specs → results to `verification-log.md` → failures to `tests/failures/`. Platform health always visible.
_Novelty:_ Automated QA for AI-powered platform.

**[#80]: The Example Topic Library**
_Concept:_ `examples/` folder with fully-worked brainstorming sessions — demonstration, training, and regression benchmarks in one.
_Novelty:_ Examples are executable specifications in disguise.

**[#81]: The Self-Healing Build**
_Concept:_ Builder Agent validates each file against its spec immediately after creating it. Self-corrects up to 3 attempts before flagging for human review.
_Novelty:_ Test-driven development at the file level during construction.

**[#82]: The Platform Spec as Living Document**
_Concept:_ `specs/` never done. Bug reports add criteria. New tools expand portability specs. New capabilities get specs first. Spec grows with platform.
_Novelty:_ Specification is a product, not a phase.

**[#83]: The Primordial Build Prompt**
_Concept:_ Entire build starts with one prompt to an AI agent: "Read brainstorming session and BUILD.md. You are the Architect Agent. Extract ideas, group into clusters, write specs/ and BUILD.md."
_Novelty:_ Brainstorming session is the requirements document. No translation step.

**[#84]: The Capability Cluster Map**
_Concept:_ Architect Agent groups ideas into 10 clusters, each becoming one spec file and build phase:
1. Core Folder Structure & File Conventions
2. Topic Lifecycle & State Management
3. Knowledge Base Management
4. Session Continuity & Recovery
5. Context Loading & Window Management
6. Contradiction & Conflict Detection
7. Cross-Topic Knowledge Graph
8. Portability & Tool Adapters
9. AI Agent Build & Test Pipeline
10. Handoff & BMad Integration
_Novelty:_ Ideas self-organize into a build plan.

**[#85]: The Behavioral Assertion Model**
_Concept:_ Tests check observable behaviors (presence, count, absence, file system checks), never exact phrases. Same test passes regardless of AI verbosity.
_Novelty:_ Decouples test validity from AI non-determinism.

**[#86]: The Deterministic File System Oracle**
_Concept:_ Most reliable assertions check file system state: which files exist, what frontmatter values are set. File state is deterministic.
_Novelty:_ Platform correctness measured through artifacts, not conversation.

**[#87]: The Semantic Similarity Threshold**
_Concept:_ Text assertions check concept coverage — required concepts must be present regardless of wording. Concept list replaces string matching.
_Novelty:_ Semantic testing for semantic outputs.

**[#88]: The Test Scenario Replay Log**
_Concept:_ Every test run produces timestamped folder: input state, conversation transcript, file system diff, oracle results. History of behavior across tools and model versions.
_Novelty:_ Forensically auditable test history.

**[#89]: The Canary Topic**
_Concept:_ One maximally complex test topic exercising the most fragile behaviors. First test after any change. Fast, comprehensive, decisive.
_Novelty:_ Concentrates highest-risk scenarios for fast regression detection.

**[#90]: The Build Agent Prompt Sequence**
_Concept:_ Full build as 5-prompt sequence, each self-contained and resumable. Fails at a specific prompt, retryable without losing prior work.
_Novelty:_ Atomic, resumable, independently verifiable build steps.

**[#91]: The Platform Health Dashboard**
_Concept:_ `verification-log.md` as human+AI readable dashboard: overall pass rate, per-cluster results, last run tool/date, open failures.
_Novelty:_ Platform knows its own health quantitatively.

**[#92]: The Spec-to-Story Bridge**
_Concept:_ Spec files auto-convert to BMad user stories for implementation. Acceptance criteria map directly from Given/When/Then assertions.
_Novelty:_ Full loop: brainstorming → specs → stories → implementation → verification.

---

### Category 10: Failure Modes & Recovery (Ideas #42, #44–45, #95–98, #102)

**[#95]: The Context Poisoning Attack**
_Concept:_ Subtly wrong knowledge base documents cause Claude to build brainstorming on false foundations. Mitigation: `source:` and `status:` frontmatter, age-based warnings in re-entry brief.
_Novelty:_ Platform's strength (trusting files) is also its vulnerability. Make quality visible.

**[#96]: The Runaway Knowledge Base**
_Concept:_ Too many documents overflow Ring 1. Mitigation: hard size limits on Ring 1 files, maximum overview length contract, pruning triggers.
_Novelty:_ Too much knowledge is as bad as too little. Size discipline is a feature.

**[#97]: The Orphaned Topic Graveyard**
_Concept:_ Abandoned topics clutter the index. Mitigation: auto-flag `dormant` after 60 days with < 2 sessions. Re-entry brief offers archive/revive/merge.
_Novelty:_ Lifecycle management includes graceful abandonment.

**[#98]: The Instruction Drift Problem**
_Concept:_ Updated workflow files break old topic data structures. Mitigation: `platform_version` in topic.yaml, migration steps in WORKFLOW.md boot sequence.
_Novelty:_ Semantic versioning for knowledge artifacts. Data migrations are first-class features.

**[#102]: The Failure Recovery Pipeline**
_Concept:_ Tester finds failure → writes failure report → Builder attempts fix → Tester re-runs → if not fixed in 2 attempts, escalates to human. Autonomous bug fix pipeline.
_Novelty:_ Platform debugs itself before escalating.

---

### Category 11: Human Psychology & UX (Ideas #60–61, #67–70, #99–100)

**[#60]: The WORKFLOW.md Boot Sequence**
_Concept:_ Four sections any LLM reads in order: Identity, Orientation, Decision Tree, Capability Declaration. Universal entry point for any AI tool.
_Novelty:_ Self-contained onboarding for any AI. Zero training required.

**[#61]: The Self-Describing Platform**
_Concept:_ WORKFLOW.md includes a "What I Am" preamble that any LLM reads aloud to new users. Platform explains itself in the first message.
_Novelty:_ No README required. The AI is the onboarding experience.

**[#65]: The Explicit Uncertainty Declaration**
_Concept:_ AI states uncertainty explicitly before any knowledge base write or workflow state advance. Mandatory confirmation for uncertain interpretations.
_Novelty:_ Epistemic humility as a structural requirement.

**[#66]: The Undo Primitive**
_Concept:_ Session-scoped `_writes.log` — append-only list of file operations. One-level undo always available.
_Novelty:_ Undo in a file-based system without Git.

**[#67]: The Zero-Setup Quick Start**
_Concept:_ For non-technical users, folder structure is invisible. Claude manages files in background. Topics referenced by name only. Power users can unlock file view.
_Novelty:_ Accessible without sacrificing file-based architecture.

**[#68]: The Plain Language Workflow Contract**
_Concept:_ Every workflow step begins with one plain-language sentence. No jargon, no file paths in user-facing messages. Implementation language and user language fully separated.
_Novelty:_ Same platform speaks developer language and non-developer language.

**[#69]: The Platform as Learning System**
_Concept:_ After each session, append technique insight to `_learnings.md`. Over time, builds personal meta-knowledge about how this user brainstorms best.
_Novelty:_ Platform learns your creative patterns. Gets better at facilitating you specifically.

**[#99]: The Blank Page Terror**
_Concept:_ Fresh empty topic UX must be energizing, not clinical. "This is a blank canvas — tell me what's been living in your head, even if it's fragments." Meet anxiety with curiosity.
_Novelty:_ Emotional design of blank state. First impressions become entire reputation.

**[#100]: The Momentum Preservation Principle**
_Concept:_ Re-entry must feel like picking up mid-sentence — "oh yes, we were just here" within 10 seconds. Every file written at session close serves the user's future emotional state, not just information needs.
_Novelty:_ Momentum is a design requirement. Every close-of-session file write serves future feeling, not just future facts.

---

### Category 12: Versioning & Long-Term Evolution (Ideas #101, #103–104)

**[#101]: The Versioning Strategy**
_Concept:_ MAJOR.MINOR.PATCH. Patch: instruction fixes, zero migration. Minor: new capabilities, existing topics unchanged. Major: structure changes, auto-migration. Documented in CHANGELOG.md.
_Novelty:_ Semantic versioning for AI workflow platform. Upgrades have predictable blast radius.

**[#103]: The Brainstorming Archaeology Feature**
_Concept:_ `/archaeology` command: "What were we thinking about X three months ago?" Claude searches session archives, traces thinking evolution, presents timeline.
_Novelty:_ Session archive becomes navigable intellectual history with a time dimension.

**[#104]: The Insight Half-Life Tracker**
_Concept:_ Ideas tagged with confidence level. Over time, Claude tracks which speculative ideas got validated, challenged, or abandoned. Quarterly "insight audit" quantifies intuition quality.
_Novelty:_ Ideas treated as hypotheses with measurable outcomes.

---

### Category 13: Language & AI Persona (Ideas #105–108)

**[#105]: The Bilingual Session Model**
_Concept:_ Brainstorming sessions support German and English. Input language (how the user speaks) and output document language (how results are written) are independently configurable per session. A user can brainstorm in German and have the session document produced in English, or vice versa.
_Novelty:_ Separates thinking language from documentation language. Users think in their strongest language, output targets its audience.

**[#106]: The Language Pair Configuration**
_Concept:_ Session config carries `brainstorm_input_language` and `brainstorm_output_language` as independent fields. Platform-level defaults come from `config.yaml`, overridable per topic and per session. The AI adapts mid-conversation if the user switches language.
_Novelty:_ Language is a per-session parameter, not a platform-wide constant. Flexible enough for multilingual teams.

**[#107]: The AI Facilitator Persona ("Soul")**
_Concept:_ Optional per-session setting that gives the AI a distinct behavioral personality -- independent of the brainstorming technique. Curated set: Enthusiastic (celebrates, amplifies), Critic (challenges, stress-tests), Spiritual (connects to meaning, values, purpose), Logical (structures, categorizes, demands evidence), Provocateur (deliberately contrarian), Empathetic (user-centered, emotional lens). Persona shapes tone, priorities, and what the AI gravitates toward.
_Novelty:_ Technique determines *what* you do. Persona determines *how* the AI shows up. Same SCAMPER session feels radically different with a Critic vs. an Enthusiast. Orthogonal creative axis.

**[#108]: The Extensible Persona Architecture**
_Concept:_ Personas defined as small Markdown files in a `personas/` folder. Each file: name, description, behavioral guidelines, example phrases, what to amplify, what to challenge. Curated set ships with platform; users add custom personas by dropping a new file. `topic.yaml` or session config references persona by filename.
_Novelty:_ Persona library is open and file-based, matching the platform's architecture. Community can share persona files. Power users craft domain-specific facilitator styles.

### Category 14: Multi-Agent Brainstorming (Ideas #109–118)

**[#109]: The Multi-Agent Brainstorming Architecture**
_Concept:_ Two or more AI agents brainstorm together on the same topic. Each agent maintains its own private workspace (personal notes, working ideas) alongside a shared exchange infrastructure. A designated leader agent produces the "golden" consolidated output. Agents can be different AI tools (Claude Code CLI + Gemini CLI) — no API integrations required, only filesystem access.
_Novelty:_ Brainstorming becomes a multi-perspective, multi-model activity. Different AI architectures produce genuinely different creative outputs. The filesystem is the only integration layer.

**[#110]: The Agent Mailbox Protocol**
_Concept:_ Each agent has an `inbox/` and a `private/` folder. Shared folders (`_shared/input/` and `_shared/output/`) provide common context and consolidated results. When Agent A wants to address Agent B, it writes to B's inbox. When addressing everyone, it writes to `_shared/`. An `_archive/` folder holds compacted old exchanges.
_Novelty:_ Mailbox pattern from distributed systems applied to AI brainstorming. Scales to N agents without every agent reading everything. Routing is filesystem-native.

**[#111]: The File Naming as Routing Protocol**
_Concept:_ Exchange filenames follow `{round}-{from}-to-{to}-{slug}.md` — e.g., `003-critic-to-enthusiast-challenge-on-mvp.md` or `003-critic-to-all-summary.md`. When `to` is `all`, every agent reads it. When `to` is a specific name, only that agent picks it up. Files are sortable by round, filterable by sender/receiver, and parseable by any AI.
_Novelty:_ Filename is the routing header. No metadata parsing required — `ls` is the message queue inspector.

**[#112]: The Discussion Leader Agent**
_Concept:_ For 3+ agent sessions, a designated leader agent coordinates: assigns turn order, curates after each round (signal vs. noise), writes round summaries to `_shared/output/`, archives raw exchanges, and tracks session progress. The leader doesn't brainstorm — it facilitates, exactly like a human moderator.
_Novelty:_ Separation of facilitation and ideation at the agent level. Leader ensures quality control and prevents circular repetition.

**[#113]: The Strict Alternation Protocol (2-Agent, No Leader)**
_Concept:_ In 2-agent sessions without a leader, agents alternate strictly: A writes, B reads and responds, A reads and responds. Turn order enforced by the orchestrator script. Each agent self-compacts every N rounds (configurable). Simple, predictable, no coordination overhead.
_Novelty:_ Simplest viable multi-agent mode. Two CLI invocations in a loop — the orchestrator is maybe 20 lines of bash.

**[#114]: The Compaction Round Mechanism**
_Concept:_ Every N rounds (configurable, default 5), a compaction step fires. The leader (or each agent in leaderless mode) writes a `compaction-summary-round-{N}.md` distilling the last N exchanges into key insights, agreements, disagreements, and open threads. Raw exchange files move to `_archive/`. Agents read only from the latest compaction summary forward. Keeps active file count bounded.
_Novelty:_ Log compaction from distributed databases applied to brainstorming. Full history preserved in archive, working set stays small.

**[#115]: The Leader-as-Curator Model**
_Concept:_ After each round, the leader actively curates: decides what's signal vs. noise, writes a tight round summary to `_shared/output/`, and archives raw exchanges. Agents read the leader's curated feed, not the raw firehose. Combined with compaction rounds, this provides two layers of overflow prevention.
_Novelty:_ The leader is an editorial function, not just a coordinator. Quality gate between raw ideation and the golden record.

**[#116]: The Orchestrator Script**
_Concept:_ A lightweight script (bash or Python, no dependencies) drives the multi-agent loop: invokes each agent's CLI in turn order, passes the inbox/shared folder paths, waits for output, triggers compaction when due, and stops when the leader declares convergence or a round limit is reached. No API, no server — just sequential CLI calls with file paths.
_Novelty:_ The entire multi-agent infrastructure is one script + folder conventions. Runs anywhere CLI tools run.

**[#117]: The Agent Identity & Persona Binding**
_Concept:_ Each agent in a multi-agent session is assigned a name and optionally a persona (from idea #107). The agent's persona file is placed in its workspace and loaded at each invocation. E.g., Agent "critic" runs Claude Code CLI with the Critic persona; Agent "visionary" runs Gemini CLI with the Enthusiastic persona. Different AI models + different personas = maximum perspective diversity.
_Novelty:_ Persona system (#107) and multi-agent system compose naturally. The same persona library serves both single-agent and multi-agent modes.

**[#118]: The Diminishing Returns Detector**
_Concept:_ The leader (or orchestrator in leaderless mode) tracks idea novelty per round. When new genuinely original ideas per round drop below a configurable threshold (default: < 2 per round for 3 consecutive rounds), the system proposes convergence, technique switch, or session end. Prevents circular repetition and runaway sessions.
_Novelty:_ Automatic stopping criterion for generative processes. The session knows when it's done being productive.

### Category 15: Autonomous Development & Testing Requirements (Ideas #123–130)

**[#123]: The Two-Layer Test Architecture**
_Concept:_ All platform requirements split into two testable layers. Layer 1 — Mechanical Tests (deterministic): file existence, folder structure, frontmatter values, naming conventions, compaction triggers, round counts. Pure file system assertions, zero AI judgment needed. Layer 2 — Behavioral Tests (non-deterministic): workflow adherence, facilitation quality, idea generation, persona consistency. Requires an AI "test user" agent running scripted scenarios with semantic assertions.
_Novelty:_ Explicitly separates what can be tested with `ls` and `grep` from what needs AI evaluation. Layer 1 is cheap, fast, and reliable. Layer 2 is the harder problem, isolated and budget-controlled.

**[#124]: The AI Test User Agent**
_Concept:_ A dedicated AI agent role that simulates a human brainstormer. Given a test scenario file (topic, goals, scripted responses, decision points), the test user interacts with the platform exactly as a human would. The test harness captures all file system changes and conversational outputs for assertion. Multiple test user personas (verbose user, terse user, indecisive user) stress-test different interaction patterns.
_Novelty:_ The platform's user is simulated by AI, enabling fully automated end-to-end testing without human involvement. Test user personas catch edge cases real users would hit.

**[#125]: The Spec-Driven Development Contract**
_Concept:_ Every feature is defined as a spec file in `specs/` with Given/When/Then assertions before any implementation begins. The spec is precise enough that an AI agent can implement from it without human clarification. Ambiguity in a spec is a bug — if the builder agent asks a question, the spec is deficient and must be improved first.
_Novelty:_ "No clarification needed" is the quality bar for specs. Eliminates the human bottleneck during autonomous development. Spec quality is directly measurable: did the builder agent need to ask anything?

**[#126]: The Autonomous Build Loop**
_Concept:_ The builder agent follows a strict cycle: (1) Read spec, (2) Implement, (3) Run Layer 1 tests, (4) Self-fix failures (up to 3 attempts), (5) Run Layer 2 tests, (6) Self-fix failures (up to 3 attempts), (7) If still failing, log issue and move to next spec. No human intervention within a phase. All build activity logged to `build-log.md`.
_Novelty:_ The agent knows its own retry budget and escalation path. Prevents infinite loops and runaway autonomous sessions. Build log provides full forensic trail.

**[#127]: The Phase Gate Model**
_Concept:_ Development is organized into explicit phases (POC, MVP, V1, V2, ...). Each phase has a `phase-definition.md`: scope (which specs), success criteria (which tests must pass), and a "done" checklist. The builder agent stops at the end of each phase, runs the full phase test suite, writes a `phase-report.md` (what was built, what passed, what failed, what was deferred), and halts for human review. The next phase does not start until the user gives explicit go-ahead.
_Novelty:_ Human oversight without human busywork. The user reviews finished work, not work-in-progress. Phase boundaries are the control surface for human judgment.

**[#128]: The Phase Report as Decision Document**
_Concept:_ `phase-report.md` is structured for human decision-making: (1) What was planned, (2) What was delivered, (3) Test results (pass/fail counts + details), (4) Known issues, (5) Recommended next steps, (6) User action required (approve / fix issues / re-scope). The user reads one document and decides whether to proceed.
_Novelty:_ The build agent's final output per phase is optimized for human review efficiency. One document, one decision.

**[#129]: The Test Coverage Requirement**
_Concept:_ Every requirement in the brainstorming output that is technically testable MUST have at least one spec assertion. A `coverage-matrix.md` maps requirements → spec files → test results. Gaps are visible. The architect agent is responsible for 100% coverage before the builder agent starts. Untestable requirements (e.g., "feels natural") are explicitly marked as human-evaluation-only.
_Novelty:_ Coverage is a first-class artifact, not an afterthought. The gap between "what we want" and "what we verify" is always visible and intentional.

**[#130]: The Human-Evaluation Checklist**
_Concept:_ Requirements that cannot be automatically tested (UX quality, facilitation feel, creative output quality) are collected into a `human-evaluation-checklist.md` per phase. At phase gate, the user evaluates these manually alongside the automated test report. Keeps the human focused on what only humans can judge.
_Novelty:_ Explicit separation of "machine can verify" and "human must judge." Neither is forgotten. The checklist evolves as the platform matures and more aspects become automatable.

---

### Category 16: Voice Interface (Ideas #131–134)

**[#131]: The Voice I/O Mode**
_Concept:_ Human input and AI output each independently configurable as voice or text. Four possible combinations per session: text-in/text-out (default), voice-in/text-out, text-in/voice-out, voice-in/voice-out. Configured in session setup or mid-session switchable. Agent-to-agent communication is always text (file-based exchange is the protocol contract).
_Novelty:_ Voice lowers the friction for generative brainstorming — speaking is faster and more fluid than typing for many people. Independent configuration means the user picks what feels natural without forcing the AI's output format.

**[#132]: The Voice-to-Text Transcript Layer**
_Concept:_ When voice input is active, the platform captures or expects a text transcript alongside the audio. All session documents remain Markdown text — voice is an input/output modality, never the storage format. The transcript is what gets written to the session file. If the AI tool provides native speech-to-text (e.g., Claude voice mode), the platform uses it; otherwise, an external STT step feeds text into the standard pipeline.
_Novelty:_ Voice is a UX layer, not an architecture layer. The file-based, portable, AI-agnostic core is never compromised. Any tool that can't do voice simply falls back to text with zero feature loss.

**[#133]: The Voice Persona Expression**
_Concept:_ When AI voice output is active, the persona (#107) influences not just content but vocal style guidance — the Enthusiastic persona suggests an energetic, upbeat delivery; the Critic suggests a measured, questioning tone. Persona files gain an optional `voice_style:` field with guidance for text-to-speech rendering or AI voice mode behavior.
_Novelty:_ Persona becomes multi-modal. The "soul" of the facilitator comes through in voice, not just words. Same persona file, richer expression when voice is available.

**[#134]: The Hands-Free Brainstorming Mode**
_Concept:_ Full voice-in/voice-out mode enables brainstorming while walking, exercising, or doing manual work. The AI manages session state, captures ideas, and provides verbal summaries. At session end, the full text transcript is written to the session file. User can review and edit the written output later.
_Novelty:_ Brainstorming escapes the desk. The best ideas often come during movement — the platform meets the user where creativity actually happens.

---

## Session Summary

### Creative Facilitation Narrative

This session used First Principles Thinking across 104 ideas, then added 30 ideas from user-driven session continuation input: language flexibility and AI persona (#105-108), multi-agent brainstorming architecture (#109-118), autonomous development and testing requirements (#123-130), and voice interface (#131-134). Stefan drove multiple pivotal expansions — the portability requirement transformed a Claude-specific tool into an AI-agnostic platform; the testability requirement produced a complete self-building, self-testing agent pipeline. The breakthrough meta-insight: this isn't a brainstorming tool, it's a persistent AI workspace where brainstorming is one activity, and the entire build/test/deploy cycle is AI-executable.

### Session Highlights

**User Creative Strengths:** Architectural intuition, ability to introduce constraints that expand rather than limit the design space (portability, testability), consistent push toward concrete structural decisions
**AI Facilitation Approach:** Session 1: Deep First Principles exploration with organic domain pivots. Session 2: User-driven input expansion — 4 new categories added before SCAMPER.
**Breakthrough Moments:** #1 Output-as-Prompt, #10 Topic Knowledge Graph, #59 Separation of Concerns Trinity, #76 Dogfooding Bootstrap, #109 Multi-Agent Architecture (file system as message bus between CLI agents), #125 Spec-Driven Development Contract ("no clarification needed" as spec quality bar)
**Energy Flow:** Sustained high energy across both sessions. Session 2 added substantial new design dimensions (multi-agent, voice, personas, autonomous dev pipeline).

### Idea Categories (134 total)

| # | Category | Ideas | Range |
|---|----------|-------|-------|
| 1 | Core Design Principles | 12 | #1–12 |
| 2 | Brownfield & Code Integration | 7 | #13–16, #23–25 |
| 3 | Session Continuity & Recovery | 8 | #17–19, #26–28, #31, #45 |
| 4 | Context Window Management | 3 | #20–22 |
| 5 | Navigation & Topic Management | 8 | #29–36 |
| 6 | Handoff & BMad Integration | 4 | #37–38, #48–49 |
| 7 | Folder Structure & Configuration | 9 | #39–47 |
| 8 | Portability & Tool Adapters | 14 | #50–59, #62–64, #70 |
| 9 | AI Agent Build & Test Pipeline | 22 | #71–92 |
| 10 | Failure Modes & Recovery | 7 | #42, #44–45, #95–98, #102 |
| 11 | Human Psychology & UX | 10 | #60–61, #65–70, #99–100 |
| 12 | Versioning & Long-Term Evolution | 3 | #101, #103–104 |
| 13 | Language & AI Persona | 4 | #105–108 |
| 14 | Multi-Agent Brainstorming | 10 | #109–118 |
| 15 | Autonomous Development & Testing | 8 | #123–130 |
| 16 | Voice Interface | 4 | #131–134 |

### Open Threads for Next Session

1. ~~**SCAMPER pass**~~ — COMPLETED (Session 3). Applied all 7 lenses to 26 POC-scoped ideas.
2. **Solution Matrix** — Map intersecting axes (complexity × value, phase × capability, etc.) to find optimal groupings
3. **Roadmap synthesis** — Define concrete phases (POC → MVP → V1 → V2) using Solution Matrix output and phase gate model (#127)
4. **MVP detailed design** — Flesh out ideas #93-94 into a buildable plan
5. **Persona interaction with techniques** — How persona and technique combine creatively
6. **Multi-agent orchestrator script design** — Concrete bash/Python implementation
7. **Multi-agent + BMad integration** — How multi-agent sessions feed into downstream workflows
8. **Agent trust model** — When agents disagree, how is it resolved?
9. **AI model degradation over time** — How the platform handles model version changes

### Next Action

Build refined POC roadmap integrating all SCAMPER results. Then proceed to Solution Matrix for MVP+ phasing.

---

## Session 3: SCAMPER on POC Scope (2026-03-11)

### Pre-SCAMPER: POC Scope Definition & Roadmap Framing

Before applying SCAMPER, the session established a phased roadmap framework and defined POC scope. Key decisions:

- **POC must be a strict superset of native BMad brainstorming** — all 60+ techniques, all facilitation quality, plus multi-topic workspace, plus PRD-compatible output
- **Autonomous build/test pipeline is a POC must-have**, not deferred
- **Knowledge base loading deferred** to MVP
- **Portability deferred** to MVP
- **Multi-topic support required** in POC (single differentiator over native BMad)

**Roadmap Phases Defined:**
- **POC** — Persistent multi-topic brainstorming workspace with autonomous build/test pipeline and PRD-compatible output
- **MVP** — Topic lifecycle, knowledge base management, context window tiering, portability, platform config, BMad-native installation
- **V1** — Cross-topic knowledge graph, brownfield ingestion, contradiction detection, handoff synthesis, full AI agent test pipeline
- **V2** — Multi-agent brainstorming, voice interface, AI personas, archaeology, self-healing systems

### SCAMPER Method Results (7 Lenses × 26 POC Ideas)

#### Lens 1: SUBSTITUTE — What can we replace with something simpler?

| ID | Proposal | Decision | Impact |
|----|----------|----------|--------|
| S-1 | Substitute folder hierarchy with flat structure | **REJECT** | Keep separate folders per topic |
| S-2 | Substitute topic.yaml + session_state.md with single topic.md | **ACCEPT** | Two files merged into one. Agent reads one file for all topic metadata and state |
| S-3 | Substitute maintained _index.md with dynamic generation | **ACCEPT** | No stored index. Workspace overview generated fresh at each invocation by scanning topic.md files |
| S-4 | Substitute BUILD.md with brainstorming session itself | **ACCEPT** | Session document IS the build spec. No separate translation step |
| S-5 | Substitute write_status with Git | **REJECT** | Platform must work without Git. Keep #42 write_status mechanism |

#### Lens 2: COMBINE — What can we merge to reduce moving parts?

| ID | Proposal | Decision | Impact |
|----|----------|----------|--------|
| C-1 | Combine Zero-Friction Entry (#5) + Topic Creation Ceremony (#30) | **ACCEPT** | Progressive enrichment: name-only creation, ceremony questions at first session start |
| C-2 | Combine Re-Entry Briefing (#17) + Platform Invocation (#29) | **ACCEPT** | Two-level briefing: workspace overview at invocation, topic deep-dive at selection |
| C-3 | Combine Naming Conventions (#41) + Graceful Misread (#44) | **ACCEPT** | Convention-aware file discovery with visible warnings for violations |
| C-4 | Combine BDD Specs (#71) + Synthetic Test Harness (#72) + Spec-Driven Dev (#125) | **ACCEPT** | Single spec file per capability: build instruction + test fixture + BDD scenarios |
| C-5 | Combine Phase Gate (#127) + Phase Report (#128) | **ACCEPT** | Phase gate IS the phase report. Build-test loop with configurable max retries. Agent loops (implement → test → self-fix) until all pass or retries exhausted. Only then writes failure report for human review |

#### Lens 3: ADAPT — What patterns can we borrow from other domains?

| ID | Proposal | Decision | Impact |
|----|----------|----------|--------|
| A-1 | Adapt Makefile dependency pattern for spec build order | **ACCEPT** | Spec files declare dependencies. Build agent follows topological order (DAG). Upstream failures block downstream builds |
| A-2 | Adapt microservices health check pattern | **ACCEPT** | Quick structural health check per topic at scan time. Health status computed, never stored |
| A-3 | Adapt database migration pattern for platform upgrades | **ACCEPT** | Stamp `platform_version` in topic.md from day one. **#98 (Instruction Drift) pulled into POC scope** |
| A-4 | Adapt REPL pattern for platform interaction | **ACCEPT** | Explicit REPL loop: Invoke → Scan → Present → Select → Load → Brief → Act → Save → Return. Each step is a testable spec |
| A-5 | Adapt "convention over configuration" from Rails | **ACCEPT** | **New foundational design principle: "The Filesystem-as-Truth Principle" — never store what can be derived from filesystem state** |

#### Lens 4: MODIFY — What can we magnify or minimize?

| ID | Proposal | Decision | Impact |
|----|----------|----------|--------|
| M-1 | Minimize topic.md to non-derivable data only | **ACCEPT** | topic.md contains: name, type, platform_version, created, state (archived only), AI-generative mode flag, markdown body. Excludes session_count, last_session, open_thread_count (all derivable) |
| M-2 | Minimize config.yaml to 4 fields | **ACCEPT** | (Later eliminated entirely in E-3) |
| M-3 | Magnify spec files into "capability contracts" | **ACCEPT** | Specs declare: REPL step coverage, platform_version introduced, phase tag (poc/mvp/v1/v2). `specs/` folder IS the living roadmap |
| M-4 | Modify session file granularity | **ACCEPT (modified)** | One living session.md per topic containing complete information. Old sessions archived to `_archive/` subfolder (debug only, agent never reads) |
| M-5 | Magnify health checks into self-repair | **ACCEPT** | Platform offers to fix simple structural problems at scan time (missing fields, naming violations, orphaned files) |

#### Lens 5: PUT TO OTHER USES — What can serve additional purposes?

| ID | Proposal | Decision | Impact |
|----|----------|----------|--------|
| P-1 | Spec files as living documentation | **ACCEPT** | Specs = tests = docs = build instructions. One artifact, four purposes. No separate documentation |
| P-2 | Archived sessions as regression baselines | **ACCEPT** | Real brainstorming sessions, once archived, become test fixtures automatically |
| P-3 | REPL pattern reusable beyond brainstorming | **ACCEPT** | REPL kept generic. Brainstorming plugs into "Act" step. Other BMad workflows could reuse the shell later |
| P-4 | Shared structural validator for health checks AND tests | **ACCEPT** | One validator, two triggers (invocation health check + Layer 1 test assertions) |
| P-5 | Brainstorming output as PRD-compatible input | **ACCEPT** | Session synthesis structured with PRD-like headings. **Major scope clarification: POC must be strict superset of native BMad brainstorming, with output that flows directly into downstream BMad workflows** |

#### Lens 6: ELIMINATE — What can we remove or defer?

| ID | Proposal | Decision | Impact |
|----|----------|----------|--------|
| E-1 | Eliminate stored _index.md entirely | **ACCEPT** | Hard rule: platform has zero stored derived state. Dynamic scan only |
| E-2 | Eliminate session archive for POC | **REJECT** | Archive stays in POC |
| E-3 | Eliminate config.yaml for POC | **ACCEPT** | No config.yaml. max_build_retries is a constant in spec runner instructions. Language settings in topic.md |
| E-4 | Eliminate Topic Creation Ceremony | **REJECT** | Ceremony stays (combined with progressive enrichment per C-1) |
| E-5 | Eliminate platform/brainstorming distinction | **REJECT** | Keep two layers: thin REPL platform shell + brainstorming plugin. Clean separation for build pipeline and future extensibility |

#### Lens 7: REVERSE — What if we flip order, roles, or assumptions?

| ID | Proposal | Decision | Impact |
|----|----------|----------|--------|
| R-1 | Reverse build order: test infrastructure first | **ACCEPT** | TDD approach: spec runner + structural validator + synthetic fixtures built FIRST. Platform grows inside pre-existing test harness |
| R-2 | Reverse brainstorming driver: AI-generative mode | **ACCEPT** | Opt-in AI-generative mode configured in Topic Creation Ceremony, stored in topic.md, changeable at any time. AI generates idea bursts, human curates |
| R-3 | Reverse session document direction: synthesis first | **ACCEPT** | session.md starts with living synthesis at top, raw session history appended below (most recent first) |
| R-4 | Reverse PRD relationship: synthesis IS PRD draft | **ACCEPT** | Living synthesis structured as PRD draft: Problem Statement, Goals, Feature Concepts, Technical Considerations, Open Questions, Roadmap Suggestion |
| R-5 | Reverse archive trigger: automatic archiving | **ACCEPT** | New session start automatically snapshots previous session.md to `_archive/`. Default is clean, current state |

### New Design Principles Established During SCAMPER

1. **The Filesystem-as-Truth Principle (A-5):** Never store what can be derived from filesystem state. Zero stored derived state.
2. **BMad Brainstorming Superset Requirement (P-5):** The platform must include all native BMad brainstorming capabilities plus multi-topic management, plus PRD-compatible output.
3. **Test-First Build Philosophy (R-1):** Test infrastructure is the first deliverable. The platform grows inside a pre-existing test harness.
4. **One Artifact, Many Purposes (P-1):** Spec files serve as tests, documentation, build instructions, and roadmap items simultaneously.
5. **Convention Over Configuration (A-5 + E-3):** Filesystem structure and naming conventions replace configuration files wherever possible.

### SCAMPER Impact Summary

**Files eliminated:** _index.md, BUILD.md, config.yaml, topic.yaml (separate file), session_state.md (separate file)
**Files merged:** topic.yaml + session_state.md → topic.md
**Files restructured:** session.md now synthesis-first with append-only history below
**Ideas pulled into POC:** #98 (platform versioning/migration)
**Ideas added:** AI-generative brainstorming mode (R-2), spec dependency DAG (A-1), health check with self-repair (A-2 + M-5), structural validator shared between health checks and tests (P-4)
**Architecture patterns adopted:** REPL (A-4), TDD build order (R-1), Makefile-style dependency DAG (A-1), microservice health checks (A-2), database migrations (A-3), convention over configuration (A-5)

### Refined POC Scope After SCAMPER

**Per-Topic Files (minimal):**
- `topic.md` — name, type, platform_version, created, state, ai_generative_mode, markdown body
- `session.md` — living synthesis (PRD-structured) at top + append-only session history below
- `_archive/` — automatic session snapshots (debug only)

**Platform Files:**
- `WORKFLOW.md` — platform REPL shell (invoke, scan, present, select, load, brief, act, save, return)
- `brainstorming/` — brainstorming plugin (all 60+ BMad techniques, facilitation, AI-generative mode)
- `specs/` — capability contracts (build + test + docs + roadmap in one file per capability, with dependency DAG and phase tags)
- Structural validator (shared by health checks and Layer 1 tests)
- Spec runner (build-test-fix loop with max retries constant)

**No stored derived state. No config.yaml. No separate docs. Filesystem is truth.**

### Updated Open Threads (Post-Session 3)

1. ~~**SCAMPER pass**~~ — COMPLETED
2. **Solution Matrix** — Apply to MVP/V1/V2 idea allocation
3. ~~**POC Roadmap detailing**~~ — COMPLETED (Session 4)
4. **Spec file format design** — Finalize the unified spec format (SPEC-000 bootstrap)
5. **REPL step definition** — Define exact REPL steps and their spec coverage
6. **Session.md format design** — Finalize PRD-structured synthesis + append-only history format
7. **Structural validator design** — Shared assertions for health checks and Layer 1 tests
8. **AI-generative mode design** — How AI burst generation + human curation works in practice

---

## Session 4: POC Roadmap Detailing (2026-03-11)

### Architectural Decisions Made

Seven key architectural decisions were debated and resolved during this session:

#### Decision 1: Layer Ordering — Test Infrastructure Before Platform Shell

**Decision:** Layer 1 (test infrastructure) is built before Layer 2 (platform shell).

**Reasoning:** TDD approach. Specs are contracts that describe what the system SHOULD look like. The structural validator checks filesystem state against conventions. Neither requires a working REPL — they need Layer 0's definitions (schemas, naming, folder layout). The platform then grows inside the pre-existing test harness.

**Dependency chain:**
- Layer 0: Define conventions (schemas, naming, folder layout)
- Layer 1: Build tooling that verifies conventions + spec contracts for everything
- Layer 2: Build the REPL (which Layer 1's specs already describe)
- Layer 3: Brainstorming plugin (which Layer 1's specs already describe)

#### Decision 2: Dual-Mode Execution — Script Mode First

**Decision:** Two execution modes: Script Mode (Python orchestrator, invokes AI CLIs) and Conversational Mode (AI reads workflow files directly). Script mode is built first.

**Reasoning:** Script mode enables automated testing — the foundation the TDD approach demands. It forces specs to be precise enough for automated execution, which also makes conversational mode more reliable when built later. Without script mode, the autonomous build-test loop can't close.

**Key properties:**
- The spec file is identical in both modes — only the execution mechanism differs
- Script mode: Python script invokes AI CLI, captures filesystem output, runs validator, reports results
- Conversational mode: AI reads workflow/spec files and follows instructions directly
- Execution mode is implicit from the runtime environment, not configured per-topic
- Script mode invocation: `python spec-runner.py --spec specs/SPEC-020.md --ai claude`
- Conversational mode invocation: "Read specs/SPEC-020.md and follow the build instructions"

#### Decision 3: POC Is Not a Monolith

**Decision:** Clean platform/plugin separation from day one. The REPL shell is one layer, brainstorming plugs into it through a defined interface contract.

**Plugin interface contract (thin):** A plugin is a folder containing a `workflow.md`. The REPL loads it, passes `{topic_path}` and `{session_path}`, and expects the plugin to manage files within the topic folder. WORKFLOW.md content must be clear enough for any AI agent to follow reliably.

#### Decision 4: Hybrid BMad Integration (Strategy C)

**Decision:** Platform handles inter-session concerns (which topic, which session, re-entry brief). BMad handles intra-session concerns (technique selection, facilitation, idea generation). Frontmatter serves both — platform fields and BMad fields coexist.

**The orchestrator model — Platform wraps BMad, doesn't replace it:**

1. **Platform pre-processes** → Reads `topic.md`, resolves paths, generates re-entry brief from `session.md` frontmatter, presents topic context
2. **Platform configures BMad** → Sets `output_folder` to topic's path, points to platform's PRD-structured template, passes `user_name` and language settings
3. **BMad takes over** → Runs its own continuation detection from `session.md` frontmatter, executes techniques, manages ideas — all existing logic, unchanged
4. **BMad finishes** → Session document written/updated
5. **Platform post-processes** → Archives previous session if needed (R-5), updates platform fields in `topic.md`, returns to REPL

**BMad files are never modified.** When BMad updates, the platform benefits automatically.

**Frontmatter ownership split:**

Platform-owned fields (in `topic.md`):
- `name`, `type`, `platform_version`, `created`, `state`, `ai_generative_mode`

BMad-owned fields (in `session.md`):
- `stepsCompleted`, `techniques_used`, `techniques_remaining`, `ideas_generated`, `selected_approach`, `facilitation_notes`, `write_status`

#### Decision 5: Spec Files from Day One (Dogfooding)

**Decision:** Phase 1 produces actual spec files in the `specs/` folder using the platform's own spec format (Option A). No intermediate design documents.

**Reasoning:** Embodies P-1 (One Artifact, Many Purposes). Phase 2's spec runner has real inputs to parse from its first test. The spec format is validated by being used. Bootstrapping is natural: SPEC-000 (Spec File Format) is self-describing and is the first file written.

#### Decision 6: AI Test User Agent — Single Invocation Approach

**Decision:** The test user agent is a prompt prepended to the platform agent's context, not a separate agent. One AI CLI invocation simulates both the platform workflow and the user responses.

**How it works:**
1. Test scenario file defines: topic name, goals, scripted responses at each decision point (technique selection, facilitation responses, completion triggers)
2. Scenario-to-prompt compiler prepends test user behavior to the agent's context
3. Single AI CLI invocation runs: the agent follows the workflow AND provides scripted user responses
4. Python spec runner validates filesystem state matches spec assertions

**Reasoning:** Avoids the complexity of orchestrating two AI agents in conversation. One invocation, deterministic inputs, filesystem-verifiable outputs. The test user is a prompt, not a separate agent.

**POC scope confirmed:** Without the test user agent, Phase 4 (brainstorming integration) can't be tested autonomously.

#### Decision 7: Sophisticated Python Spec Runner

**Decision:** The spec runner is a full-featured Python application with test reporting, retry logic, dependency DAG resolution, and the complete build-test-fix loop.

**Capabilities:**
- Spec file parser (reads SPEC-000 format)
- Dependency DAG resolver (topological sort, upstream failures block downstream)
- AI CLI invoker (configurable: claude, gemini, etc.)
- Build-test-fix loop with configurable max retries
- Structural validator integration
- Test reporter (pass/fail per spec, summary, build log)
- Fully autonomous operation (no human interaction within a phase)

**This is the heaviest engineering in the POC and the most critical component.** Phases 3-5 go faster because the pipeline does the heavy lifting.

---

### POC Build Phases with Spec Dependency Ordering

#### Phase 1: Conventions, Contracts & Spec Files

**Output:** Real spec files in `specs/` — the foundation everything validates against. No code, pure definition work.

| Spec | Name | Depends On |
|------|------|------------|
| SPEC-000 | Spec File Format (self-describing bootstrap) | — |
| SPEC-001 | Folder Structure Conventions | SPEC-000 |
| SPEC-002 | topic.md Schema | SPEC-000, SPEC-001 |
| SPEC-003 | session.md Format (PRD-structured synthesis + history) | SPEC-000, SPEC-001 |
| SPEC-004 | Plugin Interface Contract | SPEC-000 |
| SPEC-005 | Frontmatter Ownership Map (platform vs. BMad fields) | SPEC-002, SPEC-003 |
| SPEC-006 | Platform Versioning Scheme | SPEC-002 |

#### Phase 2: Test Infrastructure

**Output:** Working autonomous test pipeline. The harness everything else grows inside.

| Component | Description |
|-----------|-------------|
| Structural Validator | Python module. Takes a folder path, checks against SPEC-001/002/003. Returns structured pass/fail with details. Shared by health checks and Layer 1 tests (P-4). |
| Spec Runner | Python. Parses spec files, resolves dependency DAG (topological sort), invokes AI CLI, runs build-test-fix loop with retries, generates test reports and build logs. Fully autonomous. |
| Synthetic Test Fixtures | Pre-built folder structures: empty workspace, single-topic, multi-topic, malformed-topic. |
| Test User Agent Infrastructure | Test scenario format + scenario-to-prompt compiler. Single AI invocation simulates both platform workflow and user responses. |
| Meta-test | Spec runner validates its own fixtures pass SPEC-001/002/003. |

#### Phase 3: Platform Shell

**Output:** Working REPL that creates and manages topics, validated by Phase 2's pipeline.

| Spec | Name | Depends On |
|------|------|------------|
| SPEC-020 | WORKFLOW.md REPL Loop (invoke → scan → present → select → load → brief → act → save → return) | SPEC-001, SPEC-004 |
| SPEC-021 | Topic Creation Ceremony (progressive enrichment) | SPEC-002, SPEC-020 |
| SPEC-022 | Dynamic Workspace Scanning (no stored index) | SPEC-001, SPEC-002, SPEC-020 |
| SPEC-023 | Health Check & Self-Repair | SPEC-001, SPEC-002, SPEC-020 |

After Phase 3: working platform shell that scans workspaces, lists topics, creates new topics, hands off to plugins. No brainstorming yet.

#### Phase 4: Brainstorming Plugin & BMad Integration

**Output:** End-to-end brainstorming through the platform, using the real BMad engine. Validated by test user agent.

| Spec | Name | Depends On |
|------|------|------------|
| SPEC-030 | BMad Config Injection (pre-processor) | SPEC-004, SPEC-002 |
| SPEC-031 | PRD-Structured Session Template | SPEC-003 |
| SPEC-032 | BMad Workflow Passthrough | SPEC-030, SPEC-004 |
| SPEC-033 | Platform State Post-Processing | SPEC-032, SPEC-002, SPEC-003 |
| SPEC-034 | AI-Generative Mode | SPEC-002, SPEC-032 |
| SPEC-035 | Session Archive Management (R-5 automatic archiving) | SPEC-003, SPEC-001 |

End-to-end test: spec runner invokes platform with test scenario → test user drives through create topic → brainstorm → complete session → structural validator checks all outputs.

#### Phase 5: Integration, Hardening & Phase Report

**Output:** POC complete, ready for human evaluation.

| Component | Description |
|-----------|-------------|
| Platform versioning & migration stubs | SPEC-006 implementation — platform_version in topic.md, migration detection |
| Full regression suite | All specs pass, end-to-end scenarios green |
| Conversational mode spec runner | Instructions-based execution for Claude Desktop / non-CLI environments |
| Phase report | What was built, what passes, what was deferred to MVP, human evaluation checklist |

### Spec Dependency DAG

```
SPEC-000 (Spec Format)
  ├── SPEC-001 (Folders)
  │     ├── SPEC-002 (topic.md)
  │     │     ├── SPEC-005 (Frontmatter Map)
  │     │     ├── SPEC-006 (Versioning)
  │     │     ├── SPEC-021 (Topic Creation)
  │     │     ├── SPEC-022 (Workspace Scan)
  │     │     ├── SPEC-030 (Config Injection)
  │     │     └── SPEC-034 (AI-Generative)
  │     ├── SPEC-003 (session.md)
  │     │     ├── SPEC-005 (Frontmatter Map)
  │     │     ├── SPEC-031 (PRD Template)
  │     │     ├── SPEC-033 (Post-Processing)
  │     │     └── SPEC-035 (Archive Mgmt)
  │     ├── SPEC-020 (REPL Loop)
  │     │     ├── SPEC-021, SPEC-022, SPEC-023
  │     │     └── SPEC-032 (BMad Passthrough)
  │     └── SPEC-023 (Health Check)
  └── SPEC-004 (Plugin Contract)
        ├── SPEC-020 (REPL Loop)
        ├── SPEC-030 (Config Injection)
        └── SPEC-032 (BMad Passthrough)
```

### Updated Open Threads (Post-Session 4)

1. ~~**SCAMPER pass**~~ — COMPLETED (Session 3)
2. **Solution Matrix** — Apply to MVP/V1/V2 idea allocation (remaining technique)
3. ~~**POC Roadmap detailing**~~ — COMPLETED (Session 4)
4. **SPEC-000 design** — Finalize the unified spec file format (bootstrap spec, first deliverable)
5. **REPL step definition** — Define exact REPL steps (invoke → scan → present → select → load → brief → act → save → return) and their behavioral contracts
6. **Session.md format design** — Finalize PRD-structured synthesis + append-only history format
7. **Structural validator assertion library** — Define the shared assertions for health checks and Layer 1 tests
8. **AI-generative mode design** — How AI burst generation + human curation works in practice
9. **Test scenario format design** — Define the scripted scenario format for the test user agent
10. **Spec runner CLI interface** — Define the Python spec runner's command-line interface and configuration
