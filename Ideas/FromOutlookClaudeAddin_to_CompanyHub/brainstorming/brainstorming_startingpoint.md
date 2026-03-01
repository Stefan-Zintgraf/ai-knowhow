# Brainstorming Context: Outlook Claude Plugin Enhancement

## 1. Origin Story

This Outlook Claude plugin was generated in a ~1 hour vibe coding session. The original brief (in the author's words):

> Ich hab ihm nur gesagt, ich will ein outlook plug in, welches mittels claude api Zugriff auf alle Email ohne Inhalt haben soll. Stil wie claude für excel, powerpoint, chrome. Soll-Ist-Definitionen habe ich mir gespart, ausnahmsweise bin ich in der loop geblieben, weil es mich interessiert hat wie er das macht. Nach ca. einer Stunde mit diversen kleinen üblichen Wehwehchen war er fertig.

Translation: "I just told it I want an Outlook plugin with Claude API access to all emails without content. Style like Claude for Excel, PowerPoint, Chrome. I skipped requirements definitions; I stayed in the loop because I was curious how it works. After about an hour with the usual small hiccups it was done."

The result is a functional prototype — not production-grade, but working and demonstrating the core concept.

## 2. What the Prototype Does Today

### Architecture at a Glance
- **VSTO Outlook Add-in** (.NET Framework 4.7.2, C#)
- **WPF chat interface** hosted inside Outlook's task pane (dark theme, Outlook-blue accent)
- **Claude API integration** via direct HTTP (no SDK — none exists for .NET Framework)
- **19 tool schemas** (18 active) enabling Claude to operate on Outlook programmatically
- **MVVM + Service Layer + Tool/Command pattern**

### Current Capabilities (18 active tools)
| Category | Tools | What They Do |
|---|---|---|
| Search (4) | `list_recent_emails`, `search_by_subject`, `search_by_sender`, `search_by_recipient` | Find emails by various metadata criteria |
| Viewing (4) | `view_cache`, `get_by_number`, `load_by_folder`, `clear_cache` | Browse and inspect email metadata |
| Email Ops (5) | `reply`, `compose`, `move`, `delete`, `batch_forward` | Act on emails |
| Folder Mgmt (5) | `get_folder_list`, `list_subfolders`, `create`, `remove`, `move_folder` | Manage Outlook folder structure |

### Privacy Constraint
Email body content (`Body`, `HTMLBody`) is **never accessed** — this is a hardcoded architectural constraint. All tools operate on metadata only (subject, sender, recipients, date, attachments, flags).

### Key Technical Constraints
- .NET Framework 4.7.2 (classic, NOT .NET Core/5+/6+)
- COM Interop with Outlook via Office PIAs
- VSTO requires WinForms bridge for task panes (WPF hosted via `ElementHost`)
- `Application.Current` is always null in VSTO — must use stored `Dispatcher` reference
- No automated tests, no logging framework, no retry/backoff
- German UI, English tool results, hardcoded strings (no i18n framework)

## 3. Goal of This Brainstorming

Plan a **significant enhancement** of this plugin. The scope is deliberately wide:

- **Feature expansion** — What capabilities would make this truly useful day-to-day?
- **Architecture evolution** — Should we stay with VSTO/.NET Framework, move to Office.js web add-in, or adopt a hybrid approach?
- **Rewrite vs. enhance** — The existing code may be incrementally enhanced, or we may start fresh and reuse select snippets. The brainstorming should inform this decision, not assume one path.
- **Roadmap** — Prioritize what to build first and what to defer.

## 4. Open Questions to Explore

### Feature Direction
- Should email body access become opt-in? What use cases unlock if Claude can read email content (summarization, drafting, classification)?
- What about calendar, contacts, and tasks integration?
- Could Claude help with email triage/prioritization (flag, categorize, suggest actions)?
- What about attachment handling (preview, extract info, generate)?
- Multi-model support (switch between Claude models, or integrate other providers)?
- Conversation persistence — save/resume chat sessions across Outlook restarts?
- Templates/shortcuts — user-defined prompt templates for common tasks?

### Architecture Direction
- **VSTO vs. Office.js (web add-in)**: VSTO is powerful (full COM access) but is a legacy platform. Office.js is the modern path, works cross-platform (including Outlook Web), but has a more limited API surface. Which trade-offs are acceptable?
- **Monolith vs. extracted core**: Should business logic live in a separate .NET Standard library that could be reused across different host platforms?
- **Local vs. server-mediated**: Should Claude API calls go direct from the client, or through an intermediate server (enabling shared context, team features, audit logging)?
- **Plugin marketplace**: Is eventual publication to the Office Add-in Store a goal?

### Quality & Operations
- What testing strategy makes sense given COM/VSTO constraints?
- Should we add logging, telemetry, error reporting?
- How should API keys and configuration be managed for multi-user scenarios?
- What about update/deployment mechanisms beyond F5 debug?

## 5. Known Technical Debt (from docs/architecture.md)

1. No automated tests — all testing is manual
2. `ConversationManager` class exists but is unused (reserved for future)
3. `search_email_by_body` is dead code (disabled for privacy)
4. No retry/backoff on API failures
5. No conversation persistence (lost on restart or "New Chat")
6. Model and token limit hardcoded (`claude-sonnet-4-6`, 4096 tokens)
7. Single-threaded tool execution (sequential even for parallel tool calls)
8. No localization framework (German strings hardcoded)

## 6. Prior Ideas (ChatGPT Sprint Plans)

The `brainstorming/` folder contains three sprint templates generated by ChatGPT as one input. These represent a **conservative modernization-first approach** — stabilize before enhancing. Key themes:

- **Sprint 1 (Discovery)**: Reverse-engineer existing features, map architecture, inventory dependencies, assess risks. No code changes.
- **Sprint 2 (Stability)**: Runtime stability audit, add logging/observability, isolate Claude API behind abstraction, create test harness.
- **Sprint 3 (Modernization)**: Extract business logic to .NET Standard 2.0 library, dependency inversion, feature flags, clean architecture baseline.

These are valid technical considerations but are **not prescriptive** — the brainstorming may surface a different priority order, or conclude that a rewrite makes the modernization sprints moot.

## 7. Reference Documents

The following project documentation is available for deeper context during brainstorming:

| Document | Path | Content |
|---|---|---|
| Project Context (AI rules) | `_bmad-output/project-context.md` | 42 implementation rules and conventions |
| Architecture | `docs/architecture.md` | Layered architecture, data flows, security model |
| Component Inventory | `docs/component-inventory.md` | Full catalog of all classes and tools |
| Development Guide | `docs/development-guide.md` | Build, debug, certificate setup |
| Source Tree | `docs/source-tree-analysis.md` | Annotated directory structure |
| Sprint 1 (ChatGPT) | `brainstorming/BMAD_Sprint_1_Discovery.md` | Discovery & reverse engineering plan |
| Sprint 2 (ChatGPT) | `brainstorming/BMAD_Sprint_2_Stability.md` | Stability & technical baseline plan |
| Sprint 3 (ChatGPT) | `brainstorming/BMAD_Sprint_3_Modernization.md` | Core extraction & modernization plan |
