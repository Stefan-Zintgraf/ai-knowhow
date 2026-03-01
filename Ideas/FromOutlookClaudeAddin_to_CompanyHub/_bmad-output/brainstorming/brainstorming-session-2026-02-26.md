---
stepsCompleted: [1, 2]
inputDocuments: ['brainstorming/brainstorming_startingpoint.md']
session_topic: 'Future evolution of the Outlook Claude Plugin — product vision, architecture strategy, and build strategy with no hard constraints'
session_goals: 'Open exploration of features, architecture, rewrite-vs-enhance, roadmap — everything on the table'
selected_approach: 'progressive-flow'
techniques_used: ['what-if-scenarios']
ideas_generated: 91
current_phase: 'Phase 1 - Expansive Exploration (What If Scenarios) — COMPLETE'
next_phase: 'Phase 2 - Pattern Recognition (Morphological Analysis) — NOT STARTED'
context_file: 'brainstorming/brainstorming_startingpoint.md'
environment:
  mail_server: 'Kerio Connect with KoffBackend (Kerio Outlook Connector Offline Edition)'
  mail_client: 'Outlook Desktop (German UI)'
  internal_chat: 'Google Chat'
  ticketing: 'Zammad (self-hosted)'
  crm: 'Pipedrive'
  project_mgmt: 'Asana (marketing)'
  erp: 'easyWinArt (https://www.netsoftec.de/produkte/easywinart)'
  file_storage: 'Server with organized folder structure (proposals, contracts, docs, specs)'
  proprietary: 'Custom tools for customer deliveries and maintenance tracking'
  calendar: 'Outlook Calendar'
session_notes: |
  User wants to review and solidify brainstorming output before any implementation.
  Next session should review all 91 ideas, then proceed to Phase 2 (Morphological Analysis)
  to map the solution space systematically. The idea numbers are just labels, NOT implementation order.
  Technology stack decision deliberately deferred — to be decided after brainstorming is solid.
  Architecture sketches are directional, not prescriptive.
---

# Brainstorming Session Results

**Facilitator:** S.zintgraf
**Date:** 2026-02-26

## Session Overview

**Topic:** Future evolution of the Outlook Claude Plugin — from working prototype to indispensable daily tool. Product vision, architecture strategy, and build strategy are all open.

**Goals:** Completely open brainstorming. All existing ideas and architecture assumptions are inputs, not constraints. Explore what this AI-powered Outlook companion could become and how to get there.

### Context Guidance

_Loaded from brainstorming_startingpoint.md: Working VSTO prototype with 18 tools, WPF chat UI, metadata-only privacy model, 8 known tech debt items, and ChatGPT sprint plans as one input. All of these are starting points for discussion, not fixed decisions._

### Session Setup

_Open session — no hard constraints. Everything from architecture to feature scope to the fundamental product concept is on the table for exploration._

## Technique Selection

**Approach:** Progressive Technique Flow
**Journey Design:** Systematic development from exploration to action

**Progressive Techniques:**

- **Phase 1 - Exploration:** What If Scenarios for maximum idea generation — COMPLETE (91 ideas)
- **Phase 2 - Pattern Recognition:** Morphological Analysis for mapping the solution space — NOT STARTED
- **Phase 3 - Development:** Six Thinking Hats for multi-perspective refinement — NOT STARTED
- **Phase 4 - Action Planning:** Constraint Mapping for implementation planning — NOT STARTED

---

## Phase 1: Expansive Exploration — What If Scenarios (COMPLETE)

### Key Design Decisions (User confirmed as MUST HAVE)

- **Email body reading** — full access to email content is a must, not optional
- **Model-agnostic AI layer** — Claude, OpenAI, Gemini, OpenRouter, local LLMs (Ollama). Not bound to one provider.
- **Task-to-model routing** — different models for different tasks, pre-configured, user-overridable
- **Vector DB agnostic** — same swappable-adapter principle for embeddings storage
- **Audit logging** — comprehensive logging of all AI interactions, data access, and actions
- **Outlook plugin remains primary UI** — staff lives in Outlook, it stays as the main interface
- **Web app as secondary interface** — for independence from Outlook
- **Rules-first, AI-enhanced** — not everything needs a language model; hard rules for known patterns, AI for fuzzy edges
- **Incremental/agile delivery** — start simple, see quick results, iterate in small steps
- **Team features** — must have but later stage
- **Never auto-send (with narrow exceptions)** — AI never sends email without user confirmation. Exception: explicitly whitelisted simple templates for specific triggers, requiring admin approval to enable.
- **Internal tool first, product-ready design** — build for own company, but loosely coupled connectors so external tools can be swapped (Pipedrive→HubSpot, Zammad→Zendesk, etc.)
- **Connector categories, not connector names** — system thinks in "CRM connector," "Ticketing connector," etc., not specific product names

### All Ideas Generated (91 total)

_Note: Idea numbers are discussion-order labels only. They do NOT represent implementation sequence. Ideas may be merged, split, reprioritized, or removed during later phases._

---

#### Email Intelligence & Drafting

**[#1]**: RAG-Powered Auto-Drafting
_Concept_: Plugin reads incoming email, retrieves relevant context from a vector database (company knowledge, past decisions, project docs, policies), and drafts a contextually rich reply.
_Novelty_: The AI is the bridge between your inbox and your organization's collective knowledge.

**[#2]**: Triple-Draft with Tone Selection
_Concept_: Every auto-draft presents 3 tonal variants as clickable buttons (A: Diplomatic, B: Direct [default], C: Pushback). Default is configurable per-user.
_Novelty_: AI gives strategic communication choices, not just text generation.

**[#3]**: Adaptive Default Tone
_Concept_: System learns draft preferences over time. Defaults adapt per-sender ("always diplomatic with the CEO, always direct with engineering"). Configurable in settings.
_Novelty_: The plugin develops a communication strategy model of the user.

**[#4]**: Communication Relationship Graph
_Concept_: Plugin builds an implicit relationship model from email patterns — frequency, tone, response times, CC patterns — and uses it to personalize behavior, prioritize inbox, and adapt draft defaults per contact.
_Novelty_: Relationship-aware email AI. Treats inbox as a social network with dynamics.

---

#### Proactive Intelligence

**[#5]**: Configurable Proactive Assist
_Concept_: Granular toggles for proactive behaviors — meeting prep summaries, missed commitment reminders, duplicate question detection, follow-up nudges. Each category independently toggleable.
_Novelty_: User controls a mixing board for AI autonomy. Not "dumb assistant" or "creepy autopilot."

**[#6]**: Proactive Notification Center
_Concept_: Non-intrusive "AI Suggestions" sidebar panel. Badge count shows suggestions waiting. Respects attention while delivering value.
_Novelty_: Plugin earns trust by never forcing itself on the user.

**[#53]**: Proactive Email Composition from Cross-System Triggers (LATER STAGE — requires RAG/connectors)
_Concept_: AI detects situations that warrant an email (new CRM lead without follow-up, overdue ticket without status update) and drafts the email with full context pulled from relevant systems. User reviews and sends with one click.
_Novelty_: The AI doesn't just help you write faster — it reminds you what to write and does the cross-system research for you.

**[#54]**: Context-Assembled Drafts (LATER STAGE — requires RAG/connectors)
_Concept_: When composing, the AI automatically pulls relevant attachments from the file server, checks calendar availability for proposed meeting times, includes relevant ticket/deal status, and matches your writing style to the recipient relationship.
_Novelty_: Moves from "draft the words" to "assemble the complete communication."

---

#### Team Intelligence (LATER STAGE)

**[#7]**: Shared Knowledge & Team Context
_Concept_: Team-wide shared vector DB, collective knowledge for drafting, workload visibility, handoff support, shared templates.
_Novelty_: Elevates from personal productivity to organizational intelligence.

---

#### Product & Design Philosophy

**[#8]**: Incremental Value Delivery
_Concept_: Start with "wow moment" in week 1. Each iteration adds one capability layer. Team features come after single-user experience is solid.
_Novelty_: Prove the chapel before building the cathedral.

**[#42]**: Internal-First, Product-Ready Design
_Concept_: Build for own company's needs, but with loosely coupled connectors so swapping tools is just a new adapter module. Internal tool today, potential product tomorrow.
_Novelty_: Connector architecture naturally enables productization without the product aspiration slowing delivery.

**[#43]**: Connector Categories, Not Connector Names
_Concept_: System thinks in categories: "CRM connector," "Ticketing connector," "ERP connector" — not "Pipedrive connector." Specific tool adapters implement category interfaces.
_Novelty_: A customer using Salesforce instead of Pipedrive sees the exact same UI and workflows.

---

#### Architecture

**[#9]**: Platform-Agnostic Email Intelligence Layer
_Concept_: The product isn't an "Outlook plugin" — it's an AI email intelligence engine. Core is a standalone service talking to mail servers directly, with thin UI layers for Outlook, web, or standalone.
_Novelty_: Decouples from Microsoft's plugin ecosystem. Kerio/KoffBackend makes this easier to justify.

**[#10]**: Kerio-Native Connection
_Concept_: Bypass Outlook and talk to Kerio's JSON-RPC API or IMAP directly. The "plugin" becomes a standalone app or system tray service.
_Novelty_: Eliminates COM Interop / VSTO fragility.

**[#14]**: Hybrid Plugin + Backend + Optional Web
_Concept_: Outlook VSTO plugin = primary UI (thin shell). Local backend service = all intelligence. Web app = alternative interface. Three-tier architecture for a "plugin."
_Novelty_: The Outlook add-in becomes a view layer, not the product.

**[#15]**: Kerio Access Strategy — Pragmatic Fallback
_Concept_: Two mail access modes: (A) Direct Kerio API (when IT enables). (B) Outlook COM fallback (works today). Start with B, migrate to A later.
_Novelty_: No blocked-by-IT dependency. Ship now, upgrade plumbing later.

**[#29]**: Model-Agnostic AI Layer (MUST HAVE)
_Concept_: Unified AI service interface with pluggable providers: Claude, OpenAI, Gemini, OpenRouter, Ollama. Each provider is a module. Adding a new provider = one adapter, zero business logic changes.
_Novelty_: Treats AI models like database drivers — interchangeable infrastructure.

**[#30]**: Model-Agnostic AI Service with Provider Registry
_Concept_: Pluggable providers behind unified interface. Provider registry for discovery and configuration.
_Novelty_: Most AI products are welded to one provider.

**[#31]**: Task-to-Model Routing Table
_Concept_: Pre-configured mapping: classification = cheap fast model, drafting = Claude/GPT-4o, reasoning = Opus/Ultra. Users can override. System benchmarks and suggests better mappings.
_Novelty_: Optimizes cost, speed, and quality per-task.

**[#32]**: Centralized Settings & API Key Management
_Concept_: Settings panel for provider config + API keys. Later: centralized server-based key management for teams with per-user/per-team usage tracking.
_Novelty_: Scales from solo developer to enterprise without architecture changes.

**[#33]**: Vector DB Agnostic Layer
_Concept_: Swappable adapters for ChromaDB, Qdrant, Pinecone, pgvector, FAISS. Embeddings provider also swappable (OpenAI, Cohere, local sentence-transformers). Start with ChromaDB, migrate when needed.
_Novelty_: Zero-dependency start, enterprise-scale end.

**[#36]**: Evolutionary Layered Architecture
_Concept_: Concentric-ring architecture where innermost ring is v0.1 (basic plugin + rules) and each outer ring adds capability (AI, RAG, connectors, team, roles). Interfaces between rings designed on day 1, implementations behind them grow incrementally.
_Novelty_: Each version step is a small migration, not a rewrite, because the interfaces were right from the start.

**[#37]**: Critical v0.1 Interfaces
_Concept_: Even in v0.1, define IEmailAccess, IFilingDecisionEngine, IAuditLog interfaces. Implementations start trivial (Outlook COM, SQLite lookup, file logger) but the interfaces support all future backends.
_Novelty_: The skeleton supports the full product from day one; only the muscles grow.

**[#38]**: Service Bus Pattern (Evolutionary)
_Concept_: v0.1: direct method calls. v0.3: HTTP/gRPC to local backend. v0.6: shared server with auth. v0.8: cross-system orchestration. Each step is a small migration.
_Novelty_: Grows from in-process to distributed without redesign.

**[#39]**: Role-Based Access — Designed In, Enforced Later
_Concept_: Every action carries a UserContext (userId, roles, permissions) from day 1. In v0.1 it's a stub (one user, all permissions). Real enforcement activates later without restructuring.
_Novelty_: Roles are a configuration change, not an architecture change.

**[#40]**: Technology Stack (DECISION DEFERRED)
_Concept_: Candidates: C#/.NET 8, Python/FastAPI, TypeScript/Node, or Hybrid (C# plugin + Python backend). The hybrid is common in the industry for this type of product.
_Novelty_: Decision to be made after brainstorming is solidified.

**[#41]**: Language-Agnostic Backend via API
_Concept_: If the backend exposes clean REST/gRPC, the Outlook plugin doesn't care what language it's written in. Could start with Python, rewrite hot paths later, or keep Python forever.
_Novelty_: Technology choice becomes less permanent because it hides behind an API contract.

---

#### Design Philosophy

**[#16]**: Rules-First, AI-Enhanced
_Concept_: Three-layer decision engine: hard rules (DB lookups, free/instant), smart rules (heuristics, cheap), AI reasoning (Claude/etc., powerful but costs tokens). Each email cascades through layers.
_Novelty_: Industrial-grade approach (edge before cloud) applied to email AI.

**[#17]**: Progressive Intelligence Stack
_Concept_: Three tiers: (1) Hard rules — database lookups. (2) Smart rules — learned patterns. (3) AI reasoning — full model analysis. Cheaper layers handle what they can; AI fires only for genuinely ambiguous cases.
_Novelty_: Optimizes cost, speed, and quality simultaneously.

---

#### Workflow Automation & Filing

**[#11]**: AI-Powered Email Filing
_Concept_: AI reads incoming email, identifies customer, matches to folder hierarchy (e.g., Sales/Vertrieb/2026/0_PreSales/A/ABB (SE)), presents one-click filing button. Creates folders for new customers.
_Novelty_: Understands organizational taxonomy and applies it intelligently.

**[#12]**: Smart Filing with Learning
_Concept_: Progressive autonomy — week 1: suggest folder, user confirms. Week 2: auto-file with undo. Month 2: fully automatic. Edge cases surface for decision.
_Novelty_: Starts as suggestion engine, earns its way to autopilot.

**[#13]**: Filing Rule Intelligence
_Concept_: AI reads content to understand WHICH CUSTOMER an email is about, not just who sent it. A logistics email about ABB goes to the ABB folder.
_Novelty_: Current Outlook rules match on headers. This matches on meaning.

**[#18]**: Rule Management UI
_Concept_: Interface to manage filing rules manually. AI suggests rules: "You filed 12 emails from @abb.com to the same folder — create a rule?" AI bootstraps itself out of a job for repetitive patterns.
_Novelty_: The AI is honest enough to say "you don't need me for this."

---

#### Integrations & Connectors

**[#19]**: Full Tool Ecosystem Map
_Concept_: Product eventually becomes unified intelligence layer across: Outlook, Google Chat, Zammad, Pipedrive, Asana, easyWinArt, file server, proprietary delivery/maintenance tools.
_Novelty_: AI connective tissue for a mid-size company's operation. Built one connector at a time.

**[#20]**: Connector Architecture
_Concept_: Each external system gets a small independent "connector" module implementing a standard interface. New integrations = new connectors, zero core changes.
_Novelty_: Plugin architecture for integrations. Grows without rewrites.

**[#21]**: Staged Connector Roadmap
_Concept_: (1) Email, (2) Pipedrive CRM, (3) File server, (4) Zammad, (5) Calendar, (6) easyWinArt, (7) Proprietary tools, (8) Google Chat, (9) Asana.
_Novelty_: Ordered by value-to-effort ratio.

---

#### Product Vision

**[#22]**: Role-Based AI Assistants
_Concept_: Role-specific modes — Sales mode (drafting + CRM context), Support mode (ticket linking + customer history), Manager mode (summaries + dashboards). Same engine, different configs.
_Novelty_: Adapts to workflow instead of treating every user the same.

**[#23]**: "One Question" Promise
_Concept_: "Ask one question, get one answer — from across all your systems." The AI connects the dots you're connecting manually in your head every day.
_Novelty_: Value prop isn't "AI in email" — it's "AI that unifies your fragmented tools."

---

#### User Experience

**[#24]**: Action-First Interface, Chat-Second
_Concept_: Primary UI is structured (buttons, lists, contextual actions). Chat exists as one panel within a larger workspace, not as the entire interface.
_Novelty_: Workflow-first with AI embedded, not chat-first with tools bolted on.

**[#25]**: Lookeen-Style Independent Window
_Concept_: Dedicated window launched from Outlook — email list with inline action buttons, filing/triage panel, search, context viewer, collapsible chat panel. Structured like a real application.
_Novelty_: Combines GUI discoverability with AI flexibility. Users who never chat still get full value.

**[#26]**: Inline Outlook Actions
_Concept_: Right-click context menu on emails in Outlook: "File to customer folder," "Draft reply," "Summarize thread," "Link to Pipedrive deal." Zero-friction quick actions.
_Novelty_: AI actions that feel like native Outlook features.

**[#27]**: Command Palette (Ctrl+K)
_Concept_: Quick-launch overlay for natural language commands: "file selected to ABB," "draft reply diplomatic," "show all emails from ABB this month." Fuzzy matching, keyboard-first.
_Novelty_: Power-user speed. Beginners use buttons, experts use the palette.

**[#28]**: Optional Morning Briefing
_Concept_: Daily summary on Outlook open: "12 new emails. 5 auto-filed. 3 need replies. 1 deadline tomorrow. Top priority: ABB wants a revised quote." Configurable detail level.
_Novelty_: Transforms inbox-opening from anxiety to confidence.

---

#### Security & Compliance

**[#34]**: Comprehensive Audit Logging (MUST HAVE)
_Concept_: Every AI interaction logged: timestamp, user, action, emails accessed, model called, prompt (or hash), response, action taken. Local storage with optional export.
_Novelty_: Full transparency — critical for enterprise adoption and compliance.

**[#35]**: Data Flow Transparency
_Concept_: UI indicator showing where data goes per operation: "Local" (Ollama), "Cloud: Anthropic," "Cloud: OpenAI." User always knows which operations send data externally.
_Novelty_: Radically transparent about data flow. Builds trust.

**[#58]**: Undo Everything
_Concept_: Every AI action has a 1-click undo. Filed to wrong folder? Undo. Moved 50 emails in batch? Undo the whole batch. Nothing is irreversible.
_Novelty_: Fundamental safety net. The AI proposes, the user disposes.

**[#59]**: Confidence Scores and Guardrails
_Concept_: Every AI decision comes with a confidence indicator. High confidence? Auto-act (with undo). Medium? Show options. Low? Don't act, just ask. Thresholds user-configurable.
_Novelty_: The AI is honest about uncertainty instead of confidently wrong.

**[#60]**: Never Auto-Send (Core Safety Rule)
_Concept_: Hard architectural rule — the AI NEVER sends an email without explicit user confirmation. Drafts go to review queue or Outlook Drafts.
_Novelty_: Simple rule that prevents the scariest failure mode.

**[#61]**: Granular Auto-Action Permissions
_Concept_: Permission matrix where each action type has its own automation level, configurable per context. Auto-filing = allowed. Auto-sending = blocked except for explicitly whitelisted templates + triggers + admin approval.
_Novelty_: Fine-grained trust. Like giving the AI a specific power of attorney, not a blank check.

**[#69]**: AI-Powered Phishing Detection
_Concept_: AI flags suspicious patterns: CEO fraud, impersonation, urgency manipulation, link mismatches. Confidence-scored alerts.
_Novelty_: Contextual understanding, not just rule-based spam filtering. "Your CEO has never asked for wire transfers via email before."

**[#70]**: Vendor Impersonation Alert
_Concept_: Relationship graph detects when a sender claims to be from a known company but doesn't match known contacts. "This sender claims to be from ABB but doesn't match any known ABB contacts."
_Novelty_: Uses relationship intelligence for security, not just productivity.

**[#71]**: GDPR-Aware Data Processing
_Concept_: Tracks what personal data the AI has processed. Supports right-to-deletion: purges embeddings, rule associations, and cached content for a specific person. Audit log proves compliance.
_Novelty_: Built-in GDPR compliance framework.

**[#72]**: Data Retention Policies
_Concept_: Configurable retention: vector DB embeddings auto-purge after X months, audit logs retained for Y years, draft history deleted after Z days. Policies enforced automatically.
_Novelty_: The tool manages its own data lifecycle.

**[#73]**: Consent & Transparency for Team Use
_Concept_: Every user gets clear notice about AI processing. Opt-in per feature. Anticipates Betriebsrat considerations for German labor law.
_Novelty_: Transparency built in, not bolted on. Prevents the Betriebsrat conversation from becoming a blocker.

---

#### Attachments

**[#44]**: Attachment Awareness & Classification
_Concept_: Incoming attachments auto-classified: RFQ, contract, invoice, technical spec, datasheet, etc. Uses cheap/fast model or rules.
_Novelty_: Treats attachments as typed business objects with meaning, not blobs.

**[#45]**: Attachment Content Extraction
_Concept_: AI reads PDF/Word/Excel attachments and extracts structured data: customer name, part numbers, quantities, prices, deadlines, terms. Presented as summary card.
_Novelty_: Read a 3-line summary instead of opening a 5-page PDF.

**[#46]**: Smart Attachment Filing
_Concept_: When filing an email, attachments auto-saved to corresponding server folder with consistent naming conventions.
_Novelty_: Solves "was that spec sheet in the email or on the server?"

**[#47]**: Attachment Deduplication
_Concept_: Same PDF forwarded through 4 people? Recognized (hash + fuzzy matching), stored once, linked to all related emails.
_Novelty_: Stops 12 copies of the same contract accumulating.

**[#48]**: Attachment-Triggered Workflows
_Concept_: Specific attachment types trigger actions. Signed contract? Prompt to update CRM. Invoice? Log in ERP. Each trigger configurable.
_Novelty_: Attachments become workflow triggers, not just files to open.

**[#49]**: Attachment Search Across Everything
_Concept_: "Find the last quote we sent ABB" — searches emails AND server file structure. Returns the document regardless of where it lives.
_Novelty_: Unified document search across email + file system.

---

#### Search & Knowledge Retrieval

**[#50]**: Unified Natural Language Search
_Concept_: One search box. "ABB delivery discussion from January" — returns emails, attachments, server files, Pipedrive notes, Zammad tickets. All in one result list.
_Novelty_: Google-for-your-company.

**[#51]**: Contextual Search from Email
_Concept_: Reading an email from ABB? Sidebar auto-shows: related recent emails, quotes on server, Pipedrive deal stage, open Zammad tickets. No active search needed.
_Novelty_: Ambient context that anticipates what you need.

**[#52]**: Conversational Investigation
_Concept_: "What did we agree on pricing with ABB?" → synthesized answer from multiple email threads, attachments, and connected systems. Follow-up questions refine the answer.
_Novelty_: Not "find the document" but "answer the question."

---

#### Multi-Language

**[#55]**: Language-Aware Drafting
_Concept_: AI detects incoming email language and drafts reply in the same language. German email → German reply. English email → English reply. Override available.
_Novelty_: No switching mental gears between languages.

**[#56]**: Cross-Language Search and Summarization
_Concept_: Searches German AND English emails, summarizes findings in your preferred language regardless of source languages.
_Novelty_: Language stops being a barrier to finding information.

**[#57]**: Translation on Demand
_Concept_: One-click "Show in German" translation overlay. Draft in German, AI translates before sending (with review).
_Novelty_: Cheap to implement once AI layer exists. High value for international sales.

---

#### Resilience & Offline

**[#62]**: Graceful Degradation
_Concept_: Three operating modes: Full (all AI + rules), Rules-only (API unreachable, hard rules still fire), Manual (nothing works, tool hides AI features gracefully).
_Novelty_: Rules-first architecture pays off — rule engine is local, needs no internet.

**[#63]**: Offline Queue
_Concept_: AI-dependent actions queue when offline. Process automatically when connection returns. "3 actions pending."
_Novelty_: Never blocked. Work continues, AI catches up later.

**[#64]**: Local Model Fallback
_Concept_: Cloud AI unreachable? Automatically fall back to local Ollama model. Quality may be lower, but AI-assisted features still work.
_Novelty_: Model-agnostic architecture naturally enables resilience.

---

#### Multi-Account

**[#74]**: Account-Aware Context Switching
_Concept_: Tool operates across multiple mailboxes (personal + shared Sales). Rules, filing targets, and AI behavior adapt per account.
_Novelty_: Models the reality that professionals work across multiple email identities.

**[#75]**: Shared Mailbox Collaboration
_Concept_: Shared mailbox shows "claimed by" status. Prevents duplicate work. Tracks who handled what.
_Novelty_: Turns shared mailbox from chaos into coordinated team inbox.

---

#### Email Threading

**[#76]**: Conversation Summarization
_Concept_: One click on a 47-message thread → paragraph summary with key points, decisions, and current status.
_Novelty_: Never read 47 emails again.

**[#77]**: Thread Split Detection
_Concept_: AI detects when a thread has gone off-topic and offers to split tracking into separate items.
_Novelty_: Acknowledges how email threads actually behave in the real world.

---

#### Contact Intelligence

**[#78]**: Auto-Profile from Email Signatures
_Concept_: AI extracts contact details from signatures: name, title, phone, address, LinkedIn. Auto-builds contact profiles.
_Novelty_: Never manually type a contact again.

**[#79]**: Company Intelligence Cards
_Concept_: Sidebar card when reading email from a company: all known contacts, recent email volume, CRM deal stage, open tickets, last filed documents.
_Novelty_: Mini-CRM that builds itself from email.

---

#### Notifications

**[#80]**: Tiered Notification System
_Concept_: Three tiers: Silent (routine actions logged only), Badge (counter in window), Alert (toast for things needing attention). Each action category maps to a tier. User configurable.
_Novelty_: As quiet or as loud as you want. Default: mostly silent.

**[#81]**: Daily Digest Instead of Real-Time
_Concept_: One daily summary panel instead of constant notifications. "Today: 34 emails auto-filed, 3 drafts waiting, 2 phishing alerts."
_Novelty_: Anti-notification design. Respects deep work.

---

#### Templates

**[#67]**: Smart Template Library
_Concept_: Reusable response templates with context-aware placeholders that auto-fill from email context. Accessible via command palette.
_Novelty_: Templates aren't static text — they pull real data from the email they're replying to.

**[#68]**: AI-Generated Templates from History
_Concept_: AI analyzes sent emails and proposes templates: "You've written this 'quote follow-up' email 23 times. Here's a template." Library builds itself.
_Novelty_: Templates born from real behavior, not created from scratch.

---

#### Data Management

**[#82]**: Full State Export
_Concept_: One-click export of everything: filing rules, vector DB, preferences, templates, audit logs, configuration. Import on new machine or by new team member.
_Novelty_: You own your data. Nothing is lost if you switch tools or rebuild.

**[#83]**: Rule Sharing
_Concept_: Export/import filing rules between team members. New sales team member imports existing rules, productive on day one.
_Novelty_: Institutional knowledge becomes transferable.

---

#### Performance

**[#84]**: Incremental Indexing
_Concept_: Index new emails as they arrive. Optionally backfill historical emails in background. User chooses depth. Useful immediately, smarter over time.
_Novelty_: No "wait 4 hours" barrier. Value from minute one.

**[#85]**: Tiered Storage
_Concept_: Recent emails in hot vector DB (instant). Older emails in compressed cold storage (slower). Very old emails indexed on demand.
_Novelty_: System stays fast regardless of mailbox size.

---

#### Email Scheduling

**[#86]**: Send Later with Smart Timing
_Concept_: "Send at 8 AM tomorrow" plus AI-suggested timing based on recipient response patterns.
_Novelty_: Strategically timed communication, not just a delay timer.

---

#### Strategy & Prototype

**[#87]**: Prototype as Learning, Not Foundation
_Concept_: Existing VSTO prototype's value is the knowledge gained, not the code. Reuse: tool schemas, UX patterns. Discard: monolithic architecture, direct API calls from UI.
_Novelty_: Honest assessment — build fresh with right foundations, informed by prototype.

**[#88]**: Prototype as V0 Demo
_Concept_: Keep prototype running for demos and daily use while building new architecture in parallel. Switch over when new system matches + exceeds prototype capabilities.
_Novelty_: No "dark period" during rebuild. Prototype is safety net.

---

#### Naming (TO BE DECIDED)

**[#89]**: Functional names: MailMind, InboxPilot, MailFlow, ContextMail
**[#90]**: Abstract/brand names: Cortex, Nexus, Hermes, Archon
**[#91]**: German-flavored: Postmeister, Briefkasten+, Werkpost

---

### Session Summary

**Total ideas generated:** 91
**Phase 1 technique used:** What If Scenarios
**Session duration:** ~60 minutes of active ideation
**User's creative strengths:** Strong product instinct for pragmatic incremental delivery, clear distinction between must-haves and later-stage features, consistent "user is always the boss" design philosophy

### Continuation Notes

- Next session should REVIEW all 91 ideas before proceeding
- Then proceed to Phase 2: Morphological Analysis (map the multi-dimensional solution space)
- Followed by Phase 3: Six Thinking Hats (stress-test top concepts)
- Followed by Phase 4: Constraint Mapping (real vs imagined constraints, actionable roadmap)
- User explicitly wants brainstorming output to be SOLID before any implementation discussion
- Technology stack decision intentionally deferred
- Architecture sketches are directional, not final
