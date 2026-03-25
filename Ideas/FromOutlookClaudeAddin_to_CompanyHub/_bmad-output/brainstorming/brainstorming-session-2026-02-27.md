---
stepsCompleted: [1, 2]
inputDocuments:
  - 'brainstorming/brainstorming_startingpoint.md'
  - 'brainstorming/AI_Agent_Architecture_Guide_chatgpt.md'
  - 'brainstorming/AI_Agent_Architecture_Guide_perplexity.md'
  - 'brainstorming/AI_Agent_Architecture_Guide_gemini.md'
  - 'brainstorming/AI_Agent_Architecture_Guide_opus.md'
  - 'brainstorming/open_source_code_review_tools_chatgpt.md'
  - 'brainstorming/open_source_code_review_tools_gemini.md'
  - 'brainstorming/open-source-code-review-tools_perplexity.md'
session_topic: 'Future evolution of the Outlook Claude Plugin — product vision, architecture strategy, and build strategy with no hard constraints'
session_goals: 'Open exploration of features, architecture, rewrite-vs-enhance, roadmap — everything on the table'
selected_approach: 'progressive-flow'
techniques_used: ['what-if-scenarios']
ideas_generated: 136
current_phase: 'Phase 1 - Expansive Exploration (What If Scenarios) — IN PROGRESS'
next_phase: 'Phase 2 - Pattern Recognition (Morphological Analysis) — NOT STARTED'
context_file: 'brainstorming/brainstorming_startingpoint.md'
session_continued: true
continuation_date: '2026-02-27'
continuation_from: 'brainstorming-session-2026-02-26.md'
environment:
  mail_server: 'Kerio Connect with KoffBackend (Kerio Outlook Connector Offline Edition)'
  mail_client: 'Outlook Desktop (German UI)'
  internal_chat: 'Google Chat'
  ticketing: 'Zammad (self-hosted)'
  crm: 'Pipedrive'
  project_mgmt: 'Asana (marketing)'
  erp: 'easyWinArt (https://www.netsoftec.de/easywinart)'
  file_storage: 'Server with organized folder structure (proposals, contracts, docs, specs)'
  proprietary: 'Custom tools for customer deliveries and maintenance tracking'
  calendar: 'Outlook Calendar'
session_notes: |
  Continuation of 2026-02-26 session (91 ideas).
  2026-02-27: Expanded with 45 new ideas (#92-#136) based on todo.md Section 1 topics
  and 7 additional reference documents (4 AI Architecture Guides + 3 Code Review Tool surveys).
  Phase 1 remains OPEN — user wants room to rethink and potentially expand further.
  Key new topic areas: broader product identity, mail indexing infrastructure,
  cross-platform, deterministic workflows, architecture middleware, coding conventions,
  code review tooling, TDD, language choices, and step-by-step approach.
  OpenClaw evaluation parked for later.
  Code review tool selection flagged as pre-coding gate (must decide before real coding starts).
---

# Brainstorming Session Results (Continuation)

**Facilitator:** S.zintgraf
**Date:** 2026-02-27
**Continues:** brainstorming-session-2026-02-26.md (91 ideas from Phase 1)

## Session Overview

**Phase 1 Expansion:** Folding in new topics from todo.md Section 1 and 7 additional reference documents into the What If Scenarios ideation. All new ideas numbered #92-#136 and organized by topic area.

**Additional Input Documents:**
- 4x AI Agent Architecture Guides (ChatGPT, Perplexity, Gemini, Opus) — middleware, architecture patterns, coding conventions
- 3x Open Source Code Review Tool surveys (ChatGPT, Gemini, Perplexity) — review tooling landscape

---

## Phase 1 Expansion: New Ideas (#92–#136)

_Note: Idea numbers are discussion-order labels only. They do NOT represent implementation sequence. Ideas may be merged, split, reprioritized, or removed during later phases._

---

### Broader Product Identity (not just email)

**[#92]**: Product as "Company Intelligence Hub"
_Concept_: The product isn't an email tool — it's an AI-powered company intelligence layer. Email is channel #1, but the architecture treats it as one adapter among many (chat, tickets, CRM, files, ERP). The name, UI, and mental model reflect this.
_Connects to_: #9 (Platform-Agnostic Intelligence Layer), #23 ("One Question" Promise), #19 (Full Tool Ecosystem Map)
_Impact_: This reframes the entire project. The Outlook plugin becomes a "view" into the intelligence hub, not the product itself.

**[#93]**: Name Must Be Domain-Neutral
_Concept_: Product name cannot reference "mail," "inbox," or "outlook." It should suggest intelligence, assistance, or connectivity. Working candidates from #89-91 need filtering — kill MailMind, InboxPilot, MailFlow, ContextMail. Keep exploring: Cortex, Nexus, Hermes, Werkpost (if the German flavor works).
_Supersedes_: #89 (functional mail-names are now off the table)

**[#94]**: Channel-First Architecture
_Concept_: Every data source is a "channel": email channel, chat channel, ticket channel, CRM channel, file channel. The intelligence engine is channel-agnostic. Adding a new channel means writing one adapter, not touching any core logic.
_Connects to_: #20 (Connector Architecture), #43 (Connector Categories)
_Novelty_: Elevates "connector" from "optional integration" to core architectural primitive.

---

### Mail Indexing & Search Infrastructure

**[#95]**: Dedicated Indexing Agent (Background Worker)
_Concept_: Mail indexing runs as a separate, independent agent/service — never blocks the main UI or AI agent. Processes thousands of emails in background batches. Reports progress. Can be paused, resumed, or scheduled.
_Rationale_: Some mailboxes have 10,000+ emails. Indexing must not degrade the user experience.

**[#96]**: Central Vector DB (Team-Shared Knowledge)
_Concept_: Company-wide shared vector database containing indexed emails, documents, and knowledge. All users search the same corpus. Access-controlled per role/team.
_Connects to_: #7 (Shared Knowledge), #33 (Vector DB Agnostic Layer)
_Consideration_: Requires auth layer and data partitioning from day one.

**[#97]**: Private Vector DB (Per-User)
_Concept_: Each user can also have a personal vector DB for private mailbox content, personal notes, or draft ideas. Never shared. Stored locally or in user-scoped cloud storage.
_Novelty_: Dual-DB architecture — search queries fan out to both central and private, results merged with access control.

**[#98]**: Configurable Index Scope
_Concept_: Admin and users configure exactly what gets indexed: which mailboxes, which folders, which date ranges, which attachment types. Continuous vs. one-time indexing per scope. "Index Sales/2026 continuously, index Archive/2024 once."
_Novelty_: Granular control prevents over-indexing (cost, storage) and respects privacy boundaries.

**[#99]**: Lookeen Replacement — Full-Text + Semantic Search
_Concept_: Replace Lookeen (desktop email search tool) with hybrid search: traditional full-text (fast, exact) plus semantic/vector search (meaning-based). Users get both "find exact phrase" and "find emails about the ABB pricing dispute" from one search box.
_Connects to_: #50 (Unified Natural Language Search)
_Novelty_: Not just AI search — also a better traditional search. Replaces a paid tool.

**[#100]**: Incremental Index with Change Detection
_Concept_: After initial bulk index, monitor for new/changed/deleted emails and update incrementally. Use IMAP IDLE, Kerio change notifications, or Outlook event hooks. Never re-index what hasn't changed.
_Connects to_: #84 (Incremental Indexing)

---

### Cross-Platform (Linux/macOS)

**[#101]**: Platform-Independent Backend
_Concept_: The intelligence engine, API gateway, indexing agent, and vector DB all run on Linux, macOS, or Windows. Only the Outlook VSTO plugin is Windows-bound. Everything else is cross-platform from day one.
_Connects to_: #9 (Platform-Agnostic Layer), #14 (Hybrid Plugin + Backend)
_Impact_: Technology choices must be cross-platform: .NET 8+ (not .NET Framework), Python, or TypeScript for backend.

**[#102]**: Containerized Deployment
_Concept_: Backend services packaged as Docker containers. Run on any OS. Compose file for local dev, Kubernetes for team deployment. The Outlook plugin talks to the backend via HTTP/gRPC — doesn't care where it runs.
_Novelty_: Eliminates "it works on my machine" and enables Linux server deployment for the heavy lifting.

**[#103]**: Web UI as Cross-Platform Fallback
_Concept_: The web app (#14) isn't just "secondary" — for macOS/Linux users, it's the primary interface. Must be feature-complete, not a watered-down version.
_Connects to_: #14 (Hybrid Plugin + Backend), #25 (Independent Window)

---

### Deterministic Workflows with AI Guardrails

**[#104]**: Three-Tier Action Classification
_Concept_: Every action classified into tiers: **Safe** (read-only: search, summarize, view — always auto-execute), **Cautious** (filing, categorizing — default: auto with undo), **Critical** (move, delete, send — default: always-ask). Each tier's behavior is user-configurable.
_Connects to_: #59 (Confidence Scores), #60 (Never Auto-Send), #61 (Granular Permissions)
_Novelty_: Formalizes the existing safety ideas into a single, coherent framework.

**[#105]**: "Always Ask" vs "YOLO Mode" Toggle
_Concept_: Per-action-type toggle. Default: always-ask for critical actions. Power users can switch specific actions to "YOLO mode" (auto-execute with undo available). Admin can lock certain actions to always-ask company-wide.
_Example_: Moving emails to customer folders → YOLO mode after trust is earned. Deleting emails → always-ask, always.

**[#106]**: Deterministic Workflows Run First, AI Optional
_Concept_: Hard-coded business rules and deterministic workflows execute before any AI is invoked. AI is a fallback for cases rules can't handle, not the default. Toggle per workflow: "Use AI for this workflow: Yes/No/Only when rules fail."
_Connects to_: #16 (Rules-First), #17 (Progressive Intelligence Stack)
_Novelty_: Makes the rules-first philosophy configurable and visible to users.

**[#107]**: Workflow Audit Trail with Decision Source
_Concept_: Every action logged with its decision source: "Rule: sender-domain-match," "Heuristic: 87% confidence," or "AI: Claude Sonnet, prompt-hash-abc123." Users see exactly why each action happened and which layer decided.
_Connects to_: #34 (Audit Logging), #35 (Data Flow Transparency)

---

### Architecture & Middleware

**[#108]**: Semantic Kernel as Core Orchestration
_Concept_: Use Microsoft Semantic Kernel as the agent orchestration layer. Native C# + Python support. Plugin model maps naturally to the tool/connector architecture. Handles prompt management, function calling, and model routing.
_Source_: All four AI architecture guides recommend it for this exact scenario.
_Risk_: Microsoft dependency. Mitigated by clean interfaces — could swap to LangGraph later.

**[#109]**: MCP (Model Context Protocol) for Tool Integration
_Concept_: Adopt MCP as the standard interface between the AI engine and all tools/connectors. Each connector is an MCP server. The AI engine is an MCP client. Clean separation, language-agnostic, standardized schemas.
_Source_: Recommended by 3/4 architecture guides. Growing ecosystem. SDKs for C#, Python, TypeScript.
_Connects to_: #20 (Connector Architecture), #41 (Language-Agnostic Backend via API)

**[#110]**: OpenClaw Evaluation — Messaging Gateway Layer (PARKED)
_Concept_: OpenClaw is a WhatsApp/Telegram/Discord/iMessage gateway for AI agents. It could serve as the messaging/notification delivery layer — sending AI-generated alerts, summaries, or approvals via WhatsApp or Telegram instead of (or alongside) email.
_Role in Step 1_: None — OpenClaw is irrelevant for the Outlook plugin MVP. It becomes relevant when the product expands to multi-channel notifications (Phase 2-3).
_Risk_: OpenClaw is Node.js-based, adds another runtime dependency. Evaluate whether a simpler notification adapter is sufficient.
_Verdict_: Parked. Revisit when multi-channel messaging becomes a priority.

**[#111]**: Clean/Hexagonal Architecture from Day One
_Concept_: Domain layer (pure business rules, no AI) → Application layer (use cases) → Agent layer (planning, tool selection, prompts) → Infrastructure layer (Outlook APIs, CRM, DB). Strict dependency rule: inner layers never depend on outer layers.
_Source_: Recommended by all architecture guides.
_Connects to_: #36 (Evolutionary Layered Architecture), #37 (Critical v0.1 Interfaces)

**[#112]**: Architecture Decision Records (ADRs)
_Concept_: Every significant architecture decision documented in a lightweight markdown ADR. ADRs are consumable by AI agents as project context. Folder: `/docs/decisions/`.
_Source_: Recommended by 3/4 guides as critical for AI-readable codebases.
_Novelty_: ADRs serve double duty — human documentation AND AI agent context.

**[#113]**: Monorepo with Shared Contracts
_Concept_: Single repository containing all components (Outlook plugin, web app, backend, agents, tools). Shared type definitions / JSON schemas as the single source of truth. Monorepo tool: Nx (structured) or Turborepo (lightweight).
_Source_: Recommended by 2/4 guides.
_Trade-off_: Monorepo adds build complexity but dramatically improves AI agent code generation quality (full context visibility).

---

### Coding Conventions & Quality

**[#114]**: Language-Specific Convention Documents
_Concept_: Maintain a `CONVENTIONS.md` per language (C#, Python, TypeScript) in the repo. These serve as "system prompts" for AI coding agents. Include naming, file structure, error handling, type usage, and forbidden patterns.
_Source_: Existing Python/Bash guardrails in `acontis-ai/Coding/CodingConventions` serve as a starting template. Expand to cover C# and TypeScript.

**[#115]**: AI-Readable Code Principles
_Concept_: Aggressive type hints everywhere. Small single-responsibility files (<300 lines). Intent-documenting docstrings. No "clever" code — explicit over implicit. These aren't just human best practices — they directly improve AI agent code quality.
_Source_: Opus guide specifically calls this out.

**[#116]**: Automated Architecture Enforcement
_Concept_: ArchUnitNET (C#) and Dependency Cruiser (TypeScript) write testable architecture rules: "nothing in the plugin layer may import from the infrastructure layer." Run in CI. Architecture violations break the build.
_Novelty_: Architecture constraints are code, not documentation.

**[#117]**: AI-Assisted Code Review Pipeline
_Concept_: PR pipeline: (1) Linter/formatter (automated), (2) Static analysis (SonarQube), (3) AI review (CodeRabbit or custom agent checking against CONVENTIONS.md and ADRs), (4) Human review. Each layer catches different classes of issues.

---

### Test-Driven Development

**[#118]**: Success-First TDD Protocol
_Concept_: Before any coding session, define a clear, unambiguous, fully testable success goal. Write the test first. AI agent runs autonomously: code → review → test → fix → repeat until all tests pass. Session ends only when tests are green AND code review passes.
_Source_: Directly from user requirements. This is the contract between human and AI agent.

**[#119]**: Regression Safety Net
_Concept_: Unit test suite runs on every PR. New features must not break existing tests. Coverage thresholds enforced in CI. Test categories: unit (fast, no external deps), integration (with mocks), E2E (full stack, slower).
_Frameworks_: C# → xUnit, Python → pytest, TypeScript → Vitest.

**[#120]**: Golden Dataset for AI Evaluation
_Concept_: Maintain a set of example emails, threads, attachments, and expected AI responses. Run automatically in CI before merging agent changes. Detects regressions in AI behavior quality.
_Source_: ChatGPT and Perplexity guides both recommend this.

---

### Language Choices

**[#121]**: Language-Per-Layer Strategy
_Concept_: C# for the Outlook VSTO plugin (Windows-only, existing expertise). Python for AI/ML backend, indexing, and agent orchestration (best AI ecosystem, venv isolation). TypeScript for web app and browser extensions. Shared contracts via JSON Schema or OpenAPI.
_Connects to_: #40 (Technology Stack — DEFERRED), #41 (Language-Agnostic Backend)
_Risk_: Three language runtimes is real complexity. Mitigated by clean API boundaries.

**[#122]**: Python Virtual Environment Discipline
_Concept_: Every Python component uses its own venv. `pyproject.toml` for dependency management. Pinned versions. No global installs. CI reproduces from lock files. This is non-negotiable — Python version conflicts are the #1 deployment headache.

**[#123]**: TypeScript Everywhere Possible
_Concept_: For components that don't need Python's AI libraries or C#'s COM interop, prefer TypeScript. One language for web app, browser extension, API gateway, and shared utilities. Reduces context-switching cost for both humans and AI agents.

---

### Step-by-Step Approach

**[#124]**: Define Step 1 Precisely, Keep Steps 2-N Flexible
_Concept_: Over-planning kills agility. Define Step 1 (Outlook plugin MVP) with concrete features and success criteria. For later steps, define only the architectural boundaries they must respect. Actual scope of each step decided at the start of that step, informed by learnings.
_Connects to_: #8 (Incremental Value Delivery), #36 (Evolutionary Layered Architecture)

**[#125]**: Step 1 = Outlook Plugin with Rules Engine + Optional AI
_Concept_: Step 1 delivers: smart filing (rules-based), email search (full-text + semantic), basic drafting (AI-assisted), and the architectural skeleton (interfaces for all future layers). AI is available but not required — the tool provides value even if the AI API is unreachable.
_Connects to_: #62 (Graceful Degradation), #106 (Deterministic First)

---

### Code Review Tooling (Pre-Coding Decision — Must Evaluate Before Real Coding Starts)

_Source: 3 survey documents — open_source_code_review_tools from ChatGPT, Gemini, and Perplexity_

**[#126]**: Multi-Layer Review Pipeline (Architecture Decision Required Before Coding)
_Concept_: Establish a 4-layer review pipeline before any production code is written:
1. **Pre-commit** — linters, formatters, type checkers (Ruff for Python, ESLint/Prettier for TS, dotnet format for C#)
2. **Automated static analysis** — SonarQube Community Edition or Semgrep (self-hosted, multi-language, CI-integrated)
3. **AI-powered PR review** — PR-Agent (Qodo, open-source) or Kodus AI (model-agnostic, bring-your-own-LLM)
4. **Human review** — final sign-off, focused on intent/architecture rather than syntax
_Why before coding_: The pipeline must exist before the first real PR, or bad patterns get baked in.

**[#127]**: PR-Agent (Qodo) as Primary AI Reviewer
_Concept_: PR-Agent is open-source, works with GitHub/Bitbucket/Azure DevOps and CLI. Auto-generates PR summaries, inline suggestions, and test proposals. Not bound to any specific LLM — can use Claude, GPT, or local models.
_Pro_: Most mature open-source AI code reviewer. Active development. Multi-platform.
_Con_: Needs configuration effort. Quality depends on model choice.
_Verdict_: Strong candidate for the AI review layer.

**[#128]**: Kodus AI as Alternative AI Reviewer
_Concept_: Model-agnostic, open-source AI code review. Key differentiator: bring-your-own-LLM (OpenAI, Claude, Ollama local models) with zero markup cost. Integrates with GitHub, Bitbucket, Azure Repos, and CI/CD.
_Pro_: No vendor lock-in on the AI model. Can use the same model-agnostic principle the product itself follows (#29).
_Con_: Newer, smaller community than PR-Agent.
_Verdict_: Worth evaluating alongside PR-Agent. May align better with the model-agnostic philosophy.

**[#129]**: SonarQube Community Edition as Static Analysis Backbone
_Concept_: Self-hosted, supports C#, Python, TypeScript/JavaScript. Detects bugs, security vulnerabilities, code smells, and technical debt. Quality gates block merges that fail thresholds. Free and open-source (Community Edition).
_Pro_: Industry standard. Multi-language. Rich dashboard. Tracks debt over time.
_Con_: Community Edition has limited branch analysis. Server Edition is commercial.
_Verdict_: Near-certain choice for the static analysis layer.

**[#130]**: Semgrep as Lightweight Alternative/Complement to SonarQube
_Concept_: Fast, open-source static analysis with customizable rule sets. Excels at pattern-based security checks and custom project-specific rules. Can run in CI and as pre-commit hook.
_Pro_: Write custom rules in minutes (e.g., "flag any direct COM property access without SafeGet"). Faster than SonarQube for targeted checks.
_Con_: Less comprehensive dashboard/tracking than SonarQube.
_Verdict_: Use alongside SonarQube, not instead of. SonarQube for broad coverage, Semgrep for project-specific custom rules.

**[#131]**: Architecture Enforcement via Testable Rules
_Concept_: Architecture constraints written as tests, not just documentation:
- **ArchUnitNET** (C#): "Controllers may not reference infrastructure directly"
- **Dependency Cruiser** (TypeScript): "No circular imports between modules"
- **Custom Semgrep rules**: "No `System.Text.Json` usage" or "No direct `mail.Body` access"
These run in CI. Architecture violations break the build.
_Connects to_: #116 (Automated Architecture Enforcement)
_Why critical_: AI coding agents are excellent at writing functional code but routinely violate layering conventions unless constraints are machine-enforced.

**[#132]**: Kilo for Pre-Push Local Review
_Concept_: Open-source AI code reviewer that runs in-IDE (VS Code, JetBrains) or CLI. Catches issues before code reaches the PR stage. Developer gets AI feedback during development, not after pushing.
_Pro_: Shift-left — issues caught earlier are cheaper to fix. Works offline with local models.
_Con_: Newer tool, less battle-tested.
_Verdict_: Interesting for developer workflow. Evaluate after the CI pipeline tools are chosen.

**[#133]**: Review Tool Evaluation Sprint (Pre-Coding Gate)
_Concept_: Before any production coding begins, dedicate a focused evaluation sprint: install PR-Agent and Kodus AI, run both against the existing prototype codebase, compare output quality, ease of setup, and model flexibility. Pick one. Same for SonarQube vs. Semgrep (likely: use both). Document decision as an ADR (#112).
_Why_: Choosing review tools after code is written means the first N commits have no quality gate. Choose first, code second.

**[#134]**: Hexmos LiveReview — Self-Hosted AI Review with Local Models
_Concept_: AI code review copilot that deploys with self-hosted Ollama models. No code or data leaves your infrastructure. Addresses data sovereignty requirements — critical for a tool handling company email data and CRM integrations.
_Pro_: Full data isolation. Uses local models (aligns with #29 model-agnostic, #64 local model fallback).
_Con_: Requires GPU resources for local model deployment. Smaller community.
_Verdict_: Interesting for the privacy-conscious layers. Evaluate alongside PR-Agent and Kodus.

**[#135]**: CodeQL for Semantic Vulnerability Detection
_Concept_: GitHub's semantic analysis engine — catches security vulnerabilities that pattern-based tools miss. Not AI-powered, but rule-based semantic analysis. Free for public repos, requires GitHub Advanced Security for private.
_Pro_: Catches deeper security issues than linters or Semgrep. Proven at scale.
_Con_: GitHub-native (tight coupling). Private repo analysis is commercial.
_Verdict_: If the project is on GitHub (likely), add CodeQL to the static analysis layer alongside SonarQube and Semgrep.

**[#136]**: Code Review Tool Selection Matrix (Decision Framework)
_Concept_: Before coding starts, evaluate tools across a structured matrix:

| Layer | Candidates | Selection Criteria |
|---|---|---|
| Pre-commit (lint/format) | Ruff (Python), ESLint/Prettier (TS), dotnet format (C#) | Speed, language coverage, zero-config |
| Static analysis | SonarQube CE, Semgrep OSS, CodeQL | Multi-language, self-hosted, false-positive rate |
| AI review | PR-Agent (Qodo), Kodus AI, Hexmos LiveReview | Model-agnostic, self-hosted, output quality |
| Architecture enforcement | ArchUnitNET, Dependency Cruiser, custom Semgrep | Testable rules, CI integration |
| Platform (if needed) | Gerrit, Review Board | Only if GitHub/Azure DevOps PR workflow insufficient |

_Key insight_: Traditional review platforms (Gerrit, Review Board, Phorge) are likely unnecessary — GitHub or Azure DevOps PR workflows cover the "human review" layer. The real decision is which AI reviewer and which static analysis combination to run in CI.

---

### Session Summary (2026-02-27)

**New ideas generated this session:** 45 (#92–#136)
**Running total:** 136
**Phase 1 technique:** What If Scenarios (continuing)
**Phase 1 status:** IN PROGRESS — user wants room to rethink and expand further

**New topic areas covered:**
- Broader product identity (not just email) — #92-#94
- Mail indexing & search infrastructure — #95-#100
- Cross-platform (Linux/macOS) — #101-#103
- Deterministic workflows with AI guardrails — #104-#107
- Architecture & middleware — #108-#113
- Coding conventions & quality — #114-#117
- Test-driven development — #118-#120
- Language choices — #121-#123
- Step-by-step approach — #124-#125
- Code review tooling (pre-coding gate) — #126-#136

**Key decisions/verdicts this session:**
- OpenClaw: Parked for later evaluation
- Code review tools: Must be evaluated before real coding starts (#133)
- Product name: Mail-related names killed (#93)
- Architecture: Clean/Hexagonal + MCP + Semantic Kernel emerging as consensus from 4 independent AI guides

### Continuation Notes

- Phase 1 remains open — user may want to add more ideas or rethink existing ones
- When ready, proceed to Phase 2: Morphological Analysis (map the solution space across dimensions)
- All 136 ideas from both sessions (#1-#91 in 2026-02-26, #92-#136 in 2026-02-27) should be considered together for Phase 2
