---
marp: true
theme: default
size: 16:9
paginate: true
title: "Introduction to Anthropic Claude"
description: "Claude products, projects, and Claude Code"
style: |
  section {
    font-size: 22px;
    padding: 20px 48px 36px 48px;
    justify-content: flex-start;
  }
  section.lead {
    justify-content: center;
    font-size: 26px;
  }
  section.lead h1 { margin-top: 0; }
  h1 { font-size: 1.5em; margin: 0 0 0.4em; line-height: 1.25; }
  h2 { font-size: 1.3em; margin: 0.1em 0 0.4em; line-height: 1.25; }
  h3 { font-size: 1.1em; margin: 0.15em 0 0.35em; }
  h4 { font-size: 1.0em; margin: 0.15em 0 0.3em; }
  p { margin: 0.3em 0; line-height: 1.5; }
  ul, ol { margin: 0.25em 0; }
  li { margin: 0.15em 0; line-height: 1.45; }
  table { font-size: 0.88em; width: 100%; margin: 0.4em 0; }
  th, td { padding: 0.3em 0.5em; line-height: 1.4; }
  pre { font-size: 0.98em; line-height: 1.4; margin: 0.4em 0; }
  code { font-size: 1em; }
  blockquote { margin: 0.4em 0; padding: 0.4em 0.7em; font-size: 0.92em; }
  img { max-height: 40vh; }
  section.mode-decision table { font-size: 0.92em; }
  section.diagram-slide img {
    max-height: 54vh;
    max-width: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
  }
  section.diagram-flow h2 {
    margin: 0 0 0.2em 0;
  }
  section.diagram-flow > p {
    margin: 0.08em 0 0.15em 0;
    font-size: 0.92em;
    line-height: 1.4;
  }
  section.diagram-flow img {
    max-height: 64vh;
    display: block;
    margin-left: auto;
    margin-right: auto;
  }
  section.flow-wide img {
    width: 100%;
    max-width: 100%;
    max-height: none;
    height: auto;
    display: block;
    margin: 0.6em auto;
  }
  section.diagram-tall img {
    max-height: 82vh;
    max-width: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    display: block;
    margin: 0.2em auto;
  }
  section.diagram-tall h2,
  section.diagram-tall h3,
  section.diagram-tall h4 {
    margin: 0 0 0.15em 0;
  }
  /* slide-image-fill: one large screenshot per slide; add _class to any slide that needs it */
  section.slide-image-fill img {
    width: 100%;
    max-width: 100%;
    max-height: 75vh;
    height: auto;
    object-fit: contain;
    display: block;
    margin: 0 auto;
  }
  section.slide-image-fill ul,
  section.slide-image-fill ol {
    margin: 0.1em 0 0.2em 0;
  }
  section.slide-image-fill li {
    margin: 0.05em 0;
    line-height: 1.35;
  }
---

<!-- _class: lead -->
# Introduction into Anthropic Claude

---


## Table of Contents

1. [Claude Desktop App](#1-claude-desktop-app)
   - 1.1 [What is it?](#11-what-is-it)
   - 1.2 [When to Use Which Mode](#12-when-to-use-which-mode)
   - 1.3 [Installation](#13-installation)
   - 1.4 [Claude Projects - what is a Project?](#14-claude-projects---what-is-a-project)
2. [How Large Language Models Work — Basics](#2-how-large-language-models-work--basics)
   - 2.1 [The Three Building Blocks of a Request](#21-the-three-building-blocks-of-a-request)
   - 2.2 [A Single Turn — What Happens Under the Hood](#22-a-single-turn--what-happens-under-the-hood)
   - 2.3 [The REPL Loop — Why Context Grows Over Time](#23-the-repl-loop--why-context-grows-over-time)
   - 2.4 [Where this applies in Claude](#24-where-this-applies-in-claude)
3. [MCP servers — overview (Model Context Protocol)](#3-mcp-servers--overview-model-context-protocol)
   - [Who talks to whom](#who-talks-to-whom)
   - [MCP (continued) — one tool call](#mcp-continued--one-tool-call)
   - [MCP (continued) — takeaways](#mcp-continued--takeaways)
4. [Introduction to Skills](#4-introduction-to-skills)
   - 4.1 [What a skill looks like](#41-what-a-skill-looks-like)
   - 4.2 [Writing your own skill — key tips](#42-writing-your-own-skill--key-tips)

---

## Table of contents (continued)

5. [Claude in Chrome — Browser Extension](#5-claude-in-chrome--browser-extension)
   - 5.1 [What is it?](#51-what-is-it)
   - 5.2 [Installation](#52-installation)
   - 5.3 [Simple Usage Example](#53-simple-usage-example)
6. [Claude for Excel](#6-claude-for-excel)
   - 6.1 [What is it?](#61-what-is-it)
   - 6.2 [Installation/Usage](#62-installationusage)

---

## Table of contents (continued)

7. [Claude Code](#7-claude-code)
   - 7.1 [Claude Code CLI](#71-claude-code-cli)
     - [Non-interactive mode: `-p` / `--print`](#non-interactive-mode--p----print)
   - 7.2 [Claude Code Visual Studio Code PlugIn](#72-claude-code-visual-studio-code-plugin)
   - 7.3 [CLAUDE.md — Location and Meaning](#73-claudemd--location-and-meaning)
   - 7.4 [Settings Files](#74-settings-files)
   - 7.5 [Modes (Ask, Plan, …)](#75-modes-ask-plan-)
   - 7.6 [Context Window & Context Rot](#76-context-window--context-rot)
   - 7.7 [Adding MCP Servers](#77-adding-mcp-servers)
   - 7.8 [Skills — Scripts and MCP](#78-skills--scripts-and-mcp)
     - [Example — MR summary skill (GitLab MCP)](#example--merge-request-summary-skill-using-the-gitlab-mcp-server-from-77)
   - 7.9 [BMAD Method (quick pointer)](#79-bmad-method-quick-pointer)

---

## Table of contents (continued)

8. [Projects in Claude — 2](#8-projects-in-claude--2)
   - 8.1 [Two project types (Chat vs Cowork projects)](#81-two-project-types-chat-vs-cowork-projects)
   - 8.2 [Creating a Project (Web)](#82-creating-a-project-web)
   - 8.3 [Adding Custom Instructions](#83-adding-custom-instructions)
   - 8.4 [Uploading Files to the Project Knowledge Base](#84-uploading-files-to-the-project-knowledge-base)
   - 8.5 [When to Use Chat Projects vs. Cowork Projects](#85-when-to-use-chat-projects-vs-cowork-projects)
   - 8.6 [Starting in Chat, Continuing in Cowork](#86-starting-in-chat-continuing-in-cowork)
   - 8.7 [Important Limitations](#87-important-limitations)
   - 8.8 [Migrating a Chat Project to Cowork](#88-migrating-a-chat-project-to-cowork)
   - 8.9 [Projects in Claude Desktop](#89-projects-in-claude-desktop)

---

## Table of contents (continued)

9. [Example: Drafting a Customer Reply with Claude Chat](#9-example-drafting-a-customer-reply-with-claude-chat)
   - 9.1 [Scenario](#91-scenario)
   - 9.2 [Prerequisites](#92-prerequisites)
   - 9.3 [Step-by-Step Example](#93-step-by-step-example)

10. [Settings & Configuration Files](#10-settings--configuration-files)
   - 10.1 [Claude Code — Shared Configuration Model](#101-claude-code--shared-configuration-model)
   - 10.2 [Claude Code CLI — Settings File Locations](#102-claude-code-cli--settings-file-locations)
   - 10.3 [Claude Code VS Code Extension — Settings File Locations](#103-claude-code-vs-code-extension--settings-file-locations)
   - 10.4 [Claude Desktop App — Settings File Locations](#104-claude-desktop-app--settings-file-locations)

---

## Table of contents (continued)

11. [Claude Code — Beyond this tutorial](#11-claude-code--beyond-this-tutorial)
   - 11.1 [Hooks — gate and automate Claude's actions](#111-hooks--gate-and-automate-claudes-actions)
   - 11.2 [Slash commands — built-in `/…` plus custom workflows](#112-slash-commands--built-in--plus-custom-workflows)
   - 11.3 [Subagents and multi-agent setups](#113-subagents-and-multi-agent-setups)
   - 11.4 [Permissions, modes, and sandboxing](#114-permissions-modes-and-sandboxing)
   - 11.5 [Built-in tools and editor integration](#115-built-in-tools-and-editor-integration)
   - 11.6 [Memory, `.claude/` layout, and troubleshooting](#116-memory-claude-layout-and-troubleshooting)
   - 11.7 [MCP (advanced), authentication, models, and costs](#117-mcp-advanced-authentication-models-and-costs)
   - 11.8 [CLI: flags, headless use, environment variables](#118-cli-flags-headless-use-environment-variables)
   - 11.9 [Plugins, Agent SDK, enterprise backends, and CI](#119-plugins-agent-sdk-enterprise-backends-and-ci)

---

<!-- _class: diagram-slide -->
## 1. Claude Desktop App

### 1.1 What is it?

- Standalone application for **Windows** and **macOS**.
- Three distinct modes:

![Claude Desktop: Chat, Cowork, and Code modes](images/claude_4_1_desktop_modes.png)

#### Modes at a glance

| Mode | Best for |
|---|---|
| **Chat** | Quick questions, drafting, research, brainstorming — the classic Claude interface |
| **Cowork** | Multi-step tasks with your local files: documents, spreadsheets, folder organization, workflows |
| **Code** (Claude Code) | Developers: write, review, debug code in a project directory via terminal |

---

### 1.2 When to Use Which Mode

- **Chat** — quick answer, draft, summary. Like claude.ai, but on your desktop.
- **Cowork** — multi-step tasks involving your own files (e.g., *"read this mail and update our offer template"*). Opens, edits, saves files on your PC in a controlled way.
- **Code** — only for developers working in a code repository (command-line tool).

**Chat vs Cowork — side by side:**

| | Chat | Cowork |
|---|---|---|
| **Where** | claude.ai / Desktop app (Chat tab) | Claude Desktop app (Cowork tab) |
| **Core idea** | Enhanced conversations with shared context | Persistent, task-oriented local workspaces |
| **Output** | Text in chat, artifacts | Real files (.xlsx, .docx, .pptx, …) |
| **Autonomy** | Reactive — you prompt, Claude responds | Agentic — Claude plans and executes multi-step tasks |
| **File access** | Only what you upload | Reads/writes local folders on your machine |
| **Team sharing** | Yes — invite members, set permissions | No sharing (local to your machine) |
| **Scheduling** | Not available | Supports scheduled/recurring tasks |
| **Platform** | Web, desktop, mobile | Desktop only (macOS / Windows) |

---

<!-- _class: mode-decision -->
**Decision guide — which mode do I need?**
- Work through the rows **in order**; stop at the first cell that names **Chat** or **Cowork**.

| # | Question | If **Yes** | If **No** |
|:-:|---|---|---|
| 1 | Real files as output? (.xlsx, .docx, .pptx) | **Cowork** | go to 2 |
| 2 | Local folder access? | **Cowork** | go to 3 |
| 3 | Scheduled or recurring work? | **Cowork** | go to 4 |
| 4 | Share with teammates? | **Chat** | go to 5 |
| 5 | Web + mobile? | **Chat** | go to 6 |
| 6 | Explore ideas or simple questions? | **Chat** | **Cowork** |


---

### 1.3 Installation

- Visit [claude.ai/download](https://claude.ai/download).
- Select your OS:
  - **Windows** — download `.exe` installer → run setup wizard.
  - **macOS** — download `.dmg` → drag Claude to Applications.
- Launch from Start menu (Windows) / Applications folder (macOS).
- Sign in with your Claude account.

- **System requirements:**

- macOS 11 (Big Sur) or newer
- Windows 10 or newer

---

### 1.4 Claude Projects - what is a Project?

- A **Project** = dedicated workspace at [claude.ai/projects](https://claude.ai/projects).
- Keeps **shared context** across multiple conversations.
- Has:
  - Custom instructions
  - Knowledge base (uploaded reference documents)
- Context is applied automatically to every chat in the project.

---

- **Example: Overview (instructions, files, chat)**

<!-- _class: slide-image-fill -->
![Chat project with Start a task in Cowork link](images/sales_assistant_project.jpg)

---

<!-- _class: slide-image-fill -->
- **Example: project instructions**

![Chat project with Start a task in Cowork link](images/project_instructions.jpg)

---

<!-- _class: slide-image-fill -->
- **Example: project chat**

![Chat project with Start a task in Cowork link](images/project_chat.jpg)

---

## 2. How Large Language Models Work — Basics

### 2.1 The Three Building Blocks of a Request

- Every request to an LLM is assembled from three message types:

| Message type | Who writes it | Purpose |
|---|---|---|
| **System Prompt** | Product / project owner (often hidden) | Role, tone, rules (e.g., *"You are a sales assistant for acontis…"*) |
| **User Prompt** | You | The actual question or instruction |
| **Assistant Answer** | The LLM | The generated response |

- All three are sent to the model **together** on every call.
- The model itself is **stateless** — no memory between calls.
- Vendor terminology differs (*system* / *developer* / *instructions*) — the concept is identical.

#### Diagram — single request

<!-- _class: diagram-slide -->
![One LLM request bundles system prompt, user prompt, and history](images/claude_0_1_single_request.png)

---

<!-- _class: diagram-slide -->
### 2.2 A Single Turn — What Happens Under the Hood

![Inputs flow into a stateless LLM: system, attachments, KB, user prompt → answer](images/claude_0_2_single_turn.png)


- The LLM behaves like a **pure function**: same inputs → similar outputs, no hidden memory.
- Everything the model "knows" about your situation must come from:
  - System Prompt
  - Attached files / knowledge base
  - Conversation history

### 2.3 The REPL Loop — Why Context Grows Over Time

- A chat = classic **REPL** (Read – Eval – Print – Loop).
- Every new turn re-sends the **entire** conversation history plus the new message.
- Context **grows with every turn**.

---

<!-- _class: diagram-slide diagram-tall -->
#### Diagram — REPL turns

![REPL sequence: each new user message re-sends full prior history to the LLM](images/repl_diagram.png)

---

**Practical consequences (any LLM):**

- **Memory feels real, but isn't** — later answers only reference earlier messages because the full history is re-sent.
- **The context window is finite** — long chats eventually "forget" oldest messages.
- **A new chat is a hard reset** — System Prompt + knowledge stay; history is empty.
- **Long chats get slower and more expensive** — more tokens re-read each turn.
- **Tip:** When a chat drifts or slows down → start fresh, paste only the essentials.

- **"Long-term memory" features** (ChatGPT Memory, Gemini personalization, Claude Projects) just inject saved notes back into the System Prompt — the model itself stays stateless.

---

### 2.4 Where this applies in Claude

Same three building blocks, different names per product:

| Product | System Prompt | User Prompt | Conversation History |
|---|---|---|---|
| **Claude Chat / Projects** | Project instructions | Your messages | Per-chat, grows over time |
| **Claude for Excel / Chrome** | Built-in by the add-in | Your messages | Per-session |
| **Cowork** | Project instructions + available tools | Your messages | Per-task, plus file-system state |
| **Claude Code** | Repo-aware instructions | Your messages | Per-terminal session |

- Other vendors offer equivalents: ChatGPT *Custom Instructions* / *GPTs*, Gemini *Gems*.

- **Knowledge Base tip:** Files uploaded to a Claude Project become part of the effective context for **every** new chat in that project — no re-attaching needed.

---

## 3. MCP servers — overview (Model Context Protocol)

- **MCP** = **Model Context Protocol** — open standard (Anthropic) for **tools** the LLM can call.
- **One socket everywhere:** Claude Desktop, Cursor, VS Code, and other “hosts” use the same way to start **MCP servers** and expose their tools to the model.
- **MCP server** = a small process that advertises **tools** (e.g. GitLab, database, your own API). The **LLM** picks a tool and arguments; the **host** runs the server and returns the result into the chat.

- **Why it matters:** without MCP, users copy-paste data into the chat; with MCP, the assistant can **act** on your systems on demand (with your consent and local tokens).

<!-- _class: diagram-slide diagram-flow flow-wide -->
### Who talks to whom

- **Host** (e.g. Claude or Cursor) `<->` **MCP client** (inside the host) `<->` **MCP server** (your tool) `<->` **external system** (API, files, DB).

![MCP host, client, server, and external system](./images/mcp_three_actors.png)

---

<!-- _class: diagram-slide diagram-flow -->
## MCP (continued) — one tool call

- The **LLM** does not call your Git server directly.
- It returns a “call tool X with args Y”; the **host** invokes the **MCP server**, which calls the **API**, and the **result** is fed back to the model.

![MCP tool call: host mediates between LLM, MCP server, and external API](./images/mcp_tool_call_flow.png)

---

## MCP (continued) — takeaways

- The model only **proposes** tool calls; **you** and the **host** policies decide what actually runs.
- **Tool results** become part of the context — the model can chain steps (*list → pick → diff → summarize*).
- In **Claude Code**, MCP is configured in `C:\Users\<username>\.claude.json` and/or the repo’s **`.mcp.json`** (see [§7.7](#77-adding-mcp-servers)); in **Claude Desktop**, in **`%APPDATA%\Claude\claude_desktop_config.json`** (see [§10.4](#104-claude-desktop-app--settings-file-locations)).

---

## 4. Introduction to Skills

- A **Skill** = a `SKILL.md` file that teaches the agent a specialized, reusable workflow.
- The agent reads a skill **on demand** — when its description matches the current task.
- Only the short `name` + `description` always loaded (model can decide when to invoke). 
- Full `SKILL.md` body and bundled files are read **only when the skill fires** — keeping idle token cost minimal.

- **Two storage locations:**

| Location | Path | Scope |
|---|---|---|
| **Personal** | `C:\Users\<username>\.claude/skills/<skill-name>/SKILL.md` | Every project on your machine |
| **Project** | `<repo>/.claude/skills/<skill-name>/SKILL.md` | Shared with the team via git |

---

### 4.1 What a skill looks like

- A skill is a folder with a `SKILL.md` file containing YAML frontmatter + instructions.
- Two required frontmatter fields:
  - `name` — short identifier (lowercase, hyphens, max 64 chars).
  - `description` — **how the agent decides when to apply it**: write in third person, state *what* it does and *when* to use it.

```markdown
---
name: code-review
description: >-
  Review code for quality and security following team standards.
  Use when reviewing pull requests or when asked for a code review.
---

# Code Review
1. Check correctness and edge cases.
2. Verify security best practices.
3. Assess readability and maintainability.
```

---

### 4.2 Writing your own skill — key tips

- **Keep `SKILL.md` under 500 lines** — every token competes with the conversation for context space.
- **Progressive disclosure** — put essential steps in `SKILL.md`, link to `reference.md` for rarely needed detail.
- **Specific description with trigger terms** — vague descriptions mean the skill is never picked up.
- **One concern per skill** — focused skills are easier to discover and less likely to interfere with other tasks.

---

## 5. Claude in Chrome — Browser Extension

### 5.1 What is it?

- Browser extension that puts Claude in a **sidebar** while you browse.
- Can:
  - Read the current page
  - Research / summarize content
  - Draft emails
  - Take actions in the browser
- No copy-pasting, no leaving the tab.

---

### 5.2 Installation

- Open **Google Chrome** 
- Visit the Chrome Web Store: [Claude extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn)
- Click **Add to Chrome** → confirm permissions.
- Click the puzzle icon (🧩) in the toolbar → find **Claude** → pin it.
- Sign in with your Claude account.

---

<!-- _class: diagram-slide -->
### 5.3 Simple Usage Example

- **Scenario:** Customer's company website is open → you want a quick company overview before a call.
- Steps:
  - Navigate to the customer's website.
  - Click the **Claude icon** in the toolbar to open the sidebar.
  - Type: *"Summarize what this company does and what products they sell."*
  - Claude reads the page and returns a concise summary.

- **Step 1 — Pin Claude to the Chrome toolbar:**

![Claude pinned in the Chrome toolbar](images/chrome_extension_pin.jpg)

---

<!-- _class: diagram-slide -->
- **Step 2 — Sidebar reads the page and answers**

![Claude sidebar summarizing the acontis website](images/chrome_extension_sidebar.jpg)

- **Other quick uses:**

- Summarize a long Gmail thread.
- Look up technical specs on a supplier page.
- Draft a follow-up while viewing a LinkedIn profile.

---

## 6. Claude for Excel

### 6.1 What is it?

- Microsoft Office **Add-in** — adds a Claude panel inside Excel.
- Capabilities:
  - Write / explain formulas
  - Clean data
  - Generate summaries from spreadsheet data
  - Automate repetitive analysis tasks

---

### 6.2 Installation/Usage

- Select 'Add-Ins' and install Claude
- Start Claude panel inside Excel
- Start chatting about this sheet

![Claude sidebar for Excel](images/claude_excel.jpg)

---

## 7. Claude Code

- Claude Code is the developer-focused flavour — a terminal CLI and VS Code extension that works directly in a code repository.
- This chapter covers the concepts most relevant in day-to-day use: project instructions (`CLAUDE.md`):
  - settings files
  - operating modes
  - how the context window is managed
  - and how skills combine with scripts and MCP.
- General background on skills (`SKILL.md`, storage, writing tips) is in [Chapter 4 — Introduction to Skills](#4-introduction-to-skills).

---

## 7.1 Claude Code CLI

**The Claude Code Command Line Interface (start with `claude` command)**

<!-- _class: slide-image-fill -->
![Claude Code CLI](images/claude_code_cli.jpg)

---

### Non-interactive mode: `-p` / `--print`

- Add **`-p`** (or **`--print`**) to run Claude Code **non-interactively** — one prompt in, answer (and tool loop) out. 
  - This is what the docs call **running Claude Code programmatically** (the CLI used to be described as “headless mode”; behaviour is unchanged). See the official page: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless).
- Same **CLI options** apply as in interactive use, including:
  - **`--allowedTools`** — auto-approve named tools so scripted runs do not block on permission prompts (list the tools your session needs, e.g. `Read`, `Edit`, `Bash`, and **MCP tools** — in practice they appear as `mcp__<server>__<tool>`; see what your host lists for the exact strings).
  - **`--output-format`** — e.g. `text` (default), `json`, or `stream-json` for machine-readable output and CI.
  - **`--mcp-config <path>`** / **`--strict-mcp-config`** — point at specific MCP config or restrict to it. 
- Authentication for non-interactive runs typically comes from **`ANTHROPIC_API_KEY`**.
- Slash commands (e.g. `/commit`) and user-invoked **skills** are **interactive-only** — in `-p` mode, state the task in natural language instead.
- **GitLab MCP** must be configured (e.g. `.mcp.json` and env — [§7.7](#77-adding-mcp-servers)); the examples below assume the `gitlab` server from that section is available and allowed.

---

**Example 1 — Triage open merge requests (read-only GitLab MCP)**

```bash
claude -p "List open merge requests for project ec-embedded. 
           For each MR, give IID, title, author, and whether it has unresolved discussions. 
           Use the GitLab MCP tools only; do not guess." \
  --allowedTools "mcp__gitlab__list_merge_requests,mcp__gitlab__get_merge_request"
```

**Example 2 — CI job: summarize review threads on the current MR as JSON**

```bash
claude -p "Project ID ${CI_PROJECT_ID}, merge request IID ${CI_MERGE_REQUEST_IID}. 
           Fetch this MR and summarize all review / discussion threads: 
           thread id, author, and a one-line gist. Output as JSON." \
  --output-format json \
  --allowedTools "mcp__gitlab__get_merge_request,mcp__gitlab__mr_discussions"
```

(Adjust **`--allowedTools`** to match the exact tool names your GitLab MCP server registers — check `claude mcp list` / tool traces if a run is denied.)

---

## 7.2 Claude Code Visual Studio Code PlugIn

**Install the Claude Code PlugIn**

<!-- _class: slide-image-fill -->
![Claude Code CLI](images/claude_code_vsplugin.jpg)

---

### 7.3 CLAUDE.md — Location and Meaning

- `CLAUDE.md` is a **plain Markdown file** that Claude Code automatically loads into the system prompt at the start of every session.
- Acts as **persistent project memory** — instructions, conventions, pointers to important files, build/test commands.

- Multiple scopes are merged (most specific wins on conflicts):

| Scope | Path (Windows) | Purpose |
|---|---|---|
| **User (global)** | `C:\Users\<username>\.claude\CLAUDE.md` | Your personal instructions across all projects |
| **Project (shared)** | `<repo>\CLAUDE.md` | Team-shared conventions, checked into git |
| **Subdirectory** | `<repo>\<subdir>\CLAUDE.md` | Loaded on demand when Claude works in that subtree |
| **Local (personal)** | Use an `@`-import inside `CLAUDE.md` pointing at a gitignored file (e.g. `@.claude/CLAUDE.local.md`) | Personal overrides for one repo, not shared |

---

- Typical contents:
  - Repository layout / where things live
  - Coding conventions (naming, file structure)
  - Build, test, and run commands (verified, non-interactive)
  - Default workflows ("when asked to build X, do Y")
  - Links to deeper docs (e.g. `AI/` folder)
- Good `CLAUDE.md` hygiene:
  - Keep it **concise** — every token is re-sent on every turn.
  - Prefer **pointers** over long prose (e.g. *"see [AI/build.md](AI/build.md)"*).
  - Update it when conventions change — it's a living document.

---

### 7.4 Settings Files

- Claude Code uses a hierarchical `settings.json` system (user / project / local / managed) shared between the CLI and the VS Code extension.
- Full details — paths, scopes, precedence, MCP servers, managed policies — are in **[Chapter 10 — Settings & Configuration Files](#10-settings--configuration-files)**, specifically:
  - [10.1 Shared configuration model](#101-claude-code--shared-configuration-model)
  - [10.2 CLI settings file locations](#102-claude-code-cli--settings-file-locations)
  - [10.3 VS Code extension settings](#103-claude-code-vs-code-extension--settings-file-locations)

---

<!-- _class: diagram-slide -->
### 7.5 Modes (Ask, Plan, …)

- Claude Code runs in one of several **permission / behaviour modes**. The mode controls how autonomously Claude acts and what it is allowed to do without asking.

![Claude Code modes selector](images/ClaudeCodeModes.jpg)

- **Switching modes:**
  - Keyboard shortcut: `Shift+Tab` cycles through modes.
  - Via command: type `/` in the panel → pick the mode.
  - Initial mode configurable via `claudeCode.initialPermissionMode` (VS Code) or `--permission-mode <mode>` (CLI).

---

- The main modes:

| Mode | Behaviour |
|---|---|
| **Ask** (Default) | Claude asks for confirmation before running tools that modify files, execute commands, or touch the system. Safest — you review every action. |
| **Plan** | Claude analyses the task and produces a written implementation plan **without making changes**. Read-only tools (Read / Grep / Glob, etc.) still run so Claude can inspect the code; nothing is edited or executed until you approve the plan. |
| **Accept Edits** | File edits apply automatically; other tools (shell commands, etc.) still prompt. Good for iterative refactoring where you trust the edit flow. |
| **Bypass Permissions** (a.k.a. "YOLO") | Claude executes everything without prompting. Fast, but use only in sandboxed / disposable environments — no safety net (you only live once!). |

- **When to use which:**
  - **Plan** — start here for anything non-trivial. Review the plan, then switch to Ask/Accept to execute.
  - **Ask** — default for exploratory work and unfamiliar codebases.
  - **Accept Edits** — mechanical refactors, well-scoped changes, when you'll review the diff afterwards.
  - **Bypass** — CI containers, throwaway VMs, or tasks where confirmations would block progress.

---

<!-- _class: diagram-slide -->
### 7.6 Context Window & Context Rot

- The **context window** is the total amount of text (tokens) the model can see in a single request: system prompt + `CLAUDE.md` + conversation history + tool outputs + your new message.
- It is **finite** — typically 200k tokens, with a 1M-token tier available on current Opus / Sonnet models. Once full, something must give.
- **Context rot** = quality degradation that happens *before* the hard limit is reached:
  - As the window fills, the model's attention is spread thin → less accurate recall of early instructions.
  - Large tool outputs (file dumps, long logs, search results) crowd out the actually important signal.
  - Long sessions drift: old, no-longer-relevant exchanges still consume tokens and influence answers.
- **Compacting** — Claude Code periodically summarises older turns to keep the window healthy:

**Run the /compact skill to have more control (before auto-compacting starts at an unforeseen stage):**

![Context compacting in Claude Code](images/ContextCompacting.jpg)

---

- What compacting does:
  - Replaces older verbose messages with a condensed summary.
  - Preserves the gist (decisions, files touched, open questions) and drops the noise (full file dumps, intermediate tool chatter).
  - Happens **automatically** as the window fills, or **manually** via `/compact`.
- **Practical tips to fight context rot:**
  - Start a **fresh session** when switching to an unrelated task — cheaper and sharper than dragging old context.
  - Use `/clear` to reset the conversation while keeping `CLAUDE.md` and settings.
  - Keep `CLAUDE.md` lean — it's re-read on every turn.
  - If an answer starts feeling "off" after many turns, compact or restart rather than fighting through.

---

### 7.7 Adding MCP Servers

- **MCP (Model Context Protocol)** = standardised way to give Claude Code extra tools (GitLab, Jira, a database, an internal API, …). Each MCP server is a small process Claude Code launches and talks to over stdio / HTTP.
- Claude Code (CLI **and** VS Code extension) reads MCP server definitions from three scopes:

| Scope | File | When to use |
|---|---|---|
| **User (global)** | `%USERPROFILE%\.claude.json` (key: `mcpServers`) | Personal servers available in every project |
| **Project (shared)** | `<repo>\.mcp.json` *(at repo root, not under `.claude\`)* | Team-shared servers, checked into git |
| **Local (personal)** | `%USERPROFILE%\.claude.json` (per-project section) | Personal servers for one repo only |

- The VS Code extension uses the **same files** as the CLI — no separate "extension MCP config".

- **Three ways to add a server**

1. **CLI — `claude mcp add` (recommended):**
   - `claude mcp add <name> -- <command> [args...]` — user scope by default.
   - `claude mcp add <name> --scope project -- <command> [args...]` — writes to `./.mcp.json`.
   - `claude mcp list` / `claude mcp remove <name>` to inspect or delete.
2. **VS Code panel:** type `/` in the Claude panel → **MCP** → add / edit servers through the UI.
3. **Hand-edit the JSON** — fine for project scope, since `.mcp.json` is meant to be committed.

---

- **After adding a server**
- Restart Claude Code (close the VS Code panel / exit the CLI and reopen). Changes are **not** hot-reloaded.
- In a new session, the first time a project-scope `.mcp.json` is seen, Claude Code asks you to **approve** it — servers from an untrusted repo do not auto-run.
- Check `/mcp` (slash command) or `claude mcp list` to confirm the server is connected. Per-server stderr ends up in `mcp-server-<name>.log` (see Section 10.4 for log paths).

- **Example — the GitLab MCP server used in this repo**

- File: `<repo>\.mcp.json`

```json
{
  "mcpServers": {
    "gitlab": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@zereight/mcp-gitlab"],
      "env": {
        "GITLAB_API_URL": "http://at-dev-git/api/v4",
        "GITLAB_PERSONAL_ACCESS_TOKEN": "glpat-xxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

---

- `type: "stdio"` — Claude Code launches the command and talks to it over stdin/stdout.
- `command` + `args` — here `npx -y @zereight/mcp-gitlab` downloads and runs the GitLab MCP server from npm. Requires Node.js / `npx` on `PATH`.
- `env` — environment variables passed to the server process:
  - `GITLAB_API_URL` — the internal GitLab instance (`http://at-dev-git/api/v4`).
  - `GITLAB_PERSONAL_ACCESS_TOKEN` — a GitLab PAT with the scopes the server needs (typically `api`, `read_repository`).
- Once loaded, Claude gets tools like `list_merge_requests`, `get_merge_request`, `create_issue`, `mr_discussions`, … — they appear prefixed with `mcp__gitlab__` in tool output.

---

### 7.8 Skills — Scripts and MCP

- **Concepts and authoring basics** — what a skill is, `SKILL.md` structure, storage paths, and writing tips — are covered in [Chapter 4 — Introduction to Skills](#4-introduction-to-skills). Here we focus on **Claude Code**: combining skills with executable scripts and MCP tools.

- A skill folder can bundle **utility scripts** and reference **MCP servers**, turning a skill from passive instructions into an active toolkit.

| Capability | How it works |
|---|---|
| **Utility scripts** | Place scripts next to `SKILL.md` (e.g. `scripts/validate.py`). The skill tells the agent to *execute* them — more reliable than generating code on the fly and saves tokens. |
| **MCP server reference** | The skill can instruct the agent to call tools exposed by an MCP server (e.g. a database query tool or a GitLab API). The server must already be configured in `.mcp.json` or user config. |

- **Rule of thumb:** use a script when the operation is fragile or must be consistent (file transforms, formatting); reference an MCP tool when you need a live external service (APIs, databases, issue trackers).

---

#### Example — Merge Request summary skill using the GitLab MCP server from §7.7

```
mr-summary/
├── SKILL.md
└── scripts/
    └── format-summary.sh   # optional post-processing script
```

```markdown
---
name: mr-summary
description: >-
  Summarize a GitLab merge request. Use when the user asks
  to review, summarize, or explain an MR.
---

# MR Summary

Requires the `gitlab` MCP server (see §7.7).

1. Fetch the MR via `mcp__gitlab__get_merge_request`.
2. Fetch the discussion threads via `mcp__gitlab__mr_discussions`.
3. Produce a summary with these sections:
   - **What changed** — one-paragraph description.
   - **Open threads** — list unresolved discussions.
   - **Risk areas** — files with the most churn.

Optional — pipe the raw JSON through the bundled formatting script:

​```bash
bash scripts/format-summary.sh <mr_json>
​```
```

---

### 7.9 BMAD Method (quick pointer)

- **BMAD** (BMad Method) is a **structured, agent-driven workflow** you install in a repo: workflows, project context, and optional full planning (PRD, architecture) when scope is large.

- For **small, well-scoped changes** (e.g. a single API tweak in a brownfield codebase), **Quick Dev** (`bmad-quick-dev`) is usually enough: intent → spec → implement → review without the full planning stack.
- **Deeper method:** the same ecosystem supports PRD, epics, and architecture when you outgrow a one-shot change.

- **Handout / Marp quick guide (BMAD in practice):** [`bmad_intro.md`](bmad_intro.md) — same folder as this file.

---

## 8. Projects in Claude — 2

### 8.1 Two project types (Chat vs Cowork projects)

<!-- _class: diagram-slide diagram-tall -->

![Chat projects vs Cowork projects — feature split](images/claude_5_1_project_types.png)


---

#### Chat vs Cowork project types

- **Chat Projects:**
  - Conversational, cloud-based.
  - Great for Q&A over documents, drafting, team collaboration.
  - Multiple members can share the same project context.
- **Cowork Projects:**
  - Persistent local workspaces.
  - Claude acts as autonomous agent with direct folder access.
  - Produces real files, executes multi-step tasks, supports recurring workflows.

---

### 8.2 Creating a Project (Web)

- Go to [claude.ai/projects](https://claude.ai/projects).
- Click **+ New Project** (upper right).
- Enter **project name** (e.g., *"Sales Assistant — acontis"*) and optional description.
- Click **Create project**.

### 8.3 Adding Custom Instructions

- Custom instructions = how Claude should behave in every chat of this project (tone, focus, constraints).
- Steps:
  - Inside the project → click **Set project instructions**.
  - Write your instructions. Example:

    - *"You are a sales assistant for acontis technologies. We sell EtherCAT master software and related industrial automation solutions. Always be professional and concise. When drafting customer emails, use a friendly but technical tone. Our sales contacts are engineers and procurement managers."*

  - Click **Save instructions**.

---

### 8.4 Uploading Files to the Project Knowledge Base

- Files uploaded here = available as context to every chat in this project.
- Steps:
  - Inside the project → **knowledge base section** (right side).
  - Click **+**.
  - Upload relevant files, e.g.:
    - Product datasheets / brochures
    - Standard email templates
    - Price lists / offer templates
    - Customer FAQs
  - Claude uses these as background knowledge.

- **Tip:** Keep the knowledge base **focused and high-quality**. Fewer, targeted documents > dumping everything in.

---

### 8.5 When to Use Chat Projects vs. Cowork Projects

- **Use Chat Projects when you want to:**

| Use case | Example |
|---|---|
| **Team collaboration** | Shared "Brand Guidelines" project — multiple members chat with Claude using the same style docs. |
| **Q&A over documents** | Upload datasheets / contracts / specs → ask questions. |
| **Lightweight drafting** | Emails, proposals, marketing copy — output lives in the chat. |
| **Cross-device access** | Work seamlessly from web, mobile, desktop. |
| **Shared knowledge bases** | Sales team shares product docs — all members query with same context. |

---

- **Use Cowork Projects when you want to:**

| Use case | Example |
|---|---|
| **Real file production** | *"Take these meeting notes → produce a formatted slide deck + exec summary."* |
| **Recurring workflows** | Weekly customer report: drop data → consistent formatted output. |
| **Data processing** | Claude reads a folder of exports → cleans data → produces summary spreadsheets. |
| **File organization** | *"Organize this folder — rename files, sort into subfolders, create an index."* |
| **Scheduled automation** | *"Every Monday morning, compile a status report from the files in this folder."* |
| **Local / private files** | Files that cannot be uploaded to the cloud for privacy reasons. |

---

<!-- _class: diagram-slide -->
### 8.6 Starting in Chat, Continuing in Cowork

- Very common workflow:
  - **Start in a Chat project** → brainstorm, ask questions.
  - **Hand off to Cowork** → produce actual files / execute multi-step task.
- Claude Desktop makes this seamless: a **"Start a task in Cowork"** link sits directly below the chat input.

![Chat → Cowork handoff: same context, then real files](images/claude_5_6_chat_cowork_handoff.png)


![Chat project with Start a task in Cowork link](images/chat_to_cowork.jpg)

---

- **When this handoff makes sense**

- Discussed a customer inquiry in Chat → now draft a formal reply document / update an offer template.
- Asked product-spec questions in Chat → now need a formatted comparison spreadsheet.
- Colleague shared a Chat project → reviewed context → produce local deliverables.
- Used Chat on phone during a meeting → back at desk → turn notes into a slide deck.

- **How to do it:**

- Open your project in Claude Desktop (Chat tab).
- Use Chat to discuss / refine.
- Click **Start a task in Cowork** below the chat input.
- Claude switches to Cowork mode — same instructions + knowledge base, plus local folder access.
- Describe the concrete task, e.g.:

  - *"Draft a reply to the customer email from Thomas Müller and save it as a Word document."*

---

### 8.7 Important Limitations

- **Chat Projects:**

- Context **not shared across individual chats** — only the knowledge base is shared.
- Output stays in chat / as artifacts — no direct file creation on your machine.
- No scheduling / autonomous multi-step execution.

- **Cowork Projects:**

- **Desktop app only** (macOS / Windows) — no web / mobile.
- **No team sharing** — local to your machine, no cloud sync.
- Desktop app must remain open + computer awake for Claude to work.
- Still a **research preview** — always review outputs before sending to customers.
- Memory is scoped to individual projects — does not carry over.

---

### 8.8 Migrating a Chat Project to Cowork

- Use case: you already built up a Chat Project knowledge base → now you want autonomous file production.
- Steps:
  - Open **Cowork tab → Projects → +**.
  - Select **Import a project**.
  - Search for and select your existing Chat project.
  - Choose a local folder to save it to.
  - Files + instructions transfer → Cowork's agentic capabilities are now available on top.

---

### 8.9 Projects in Claude Desktop

- Projects created on claude.ai are **also accessible** in Claude Desktop — no separate system.

- **Accessing an existing project:**

- Open Claude Desktop.
- Left sidebar → **Projects** list.
- Click a project → custom instructions + knowledge base are automatically available.
- Start a new conversation → project context applied immediately.

- **Creating a new project from Claude Desktop:**

- Left sidebar → **+** next to "Projects" / **New Project**.
- Give it a name → **Create**.
- To add instructions/files → open the project view and follow the web steps.

- **Using a project with Cowork:**

- Point Claude to a **local folder** (e.g., your `sales_assistant` folder with offer templates and product docs).
- Combines cloud-based project knowledge (instructions + uploaded files) with direct local file access.

- **Note:** Projects sync automatically between Claude Desktop and claude.ai.

---

<!-- _class: diagram-slide -->
- **Where are project files stored locally?**

- Claude Desktop maintains a local cache of project files in the app data directory, under `.project-cache`.
- Typical Windows path:

  `C:\Users\<username>\AppData\Roaming\Claude\local-agent-mode-sessions\<session-id>\.project-cache\<project-id>\files\`

- Inside `files`:
  - Knowledge-base documents stored as PDF copies with UUID filenames.
  - `docs` subfolder may contain additional document metadata.

![Local project cache folder in Windows Explorer](images/project_cache_local.jpg)

---

- You do **not** need to touch this folder in normal use — Claude manages it.
- Useful to know when:
  - Verifying which files Claude has cached locally.
  - Clearing the cache to free disk space.

---
## 9. Example: Drafting a Customer Reply with Claude Chat

### 9.1 Scenario

- A customer sent an email with a technical question + request for a quote.
- Goal: use your **Sales Assistant** Chat project to draft a professional reply quickly.

- **Why Chat, not Cowork?**
- You paste the customer email and receive a draft.
- No local file access or multi-step execution needed.
- Chat can still produce downloadable file output when required.

### 9.2 Prerequisites

- Chat project **"Sales Assistant"** set up with product knowledge + instructions (see Section 8).
- Customer email copied to your clipboard.

---

### 9.3 Step-by-Step Example

- **Step 1 — Open your Sales Assistant project.**

- Go to [claude.ai](https://claude.ai) or open Claude Desktop.
- Select the **Sales Assistant** project from the sidebar.

- **Step 2 — Start a new conversation and provide the customer email.**

- Paste the customer email into the chat, e.g.:

  - *"Here is a customer email I received:*

    *'Dear acontis team, we are evaluating EtherCAT master solutions for our new robot controller platform running on a standard x86 PC with Windows. Could you let us know which of your products would fit best, and provide indicative pricing? We need support for at least 100 slaves. Best regards, Thomas Müller, Senior Engineer at RoboTec GmbH.'*

    *Please draft a professional reply that answers his question, recommends the right product, and offers a follow-up call. Provide the draft as a downloadable text file."*

---

- **Step 3 — Review Claude's draft.**

- Claude produces a personalized reply based on project instructions + uploaded product knowledge.
- Draft appears as a **downloadable file artifact**.
- Review and adjust:
  - Pricing figures
  - Specific part numbers
  - Contact names

- **Step 4 — Copy or download the reply.**

- Click **Download** on the artifact, or
- Copy the text → paste into your email client.

- **Tip:** Need local file work later (e.g., update an offer template on disk)? Switch to Cowork from the same project → see Section 8.6.

---

## 10. Settings & Configuration Files

- This section describes **where settings live on disk** for each of the Claude tools that run locally on your machine:

- Sections 10.1 – 10.3: **Claude Code** (CLI and VS Code extension — they share the same files).
- Section 10.4: **Claude Desktop App** — uses a *separate* configuration file in a different location.

---

### 10.1 Claude Code — Shared Configuration Model

- Claude Code ships in two flavours that **share the same configuration files**:
  - **CLI** — the `claude` command in a terminal.
  - **VS Code extension** — graphical panel inside VS Code (also works in Cursor). The extension bundles the CLI underneath.
- Claude Code uses a **hierarchical settings system**. More specific scopes override broader ones:

| Priority (high → low) | Scope | Purpose |
|---|---|---|
| 1 | **Managed** | IT-deployed policies for all users on the machine |
| 2 | Command-line arguments | Per-invocation overrides |
| 3 | **Local** | Your personal overrides in one repository (gitignored) |
| 4 | **Project** | Team-shared settings checked into the repo |
| 5 | **User (Global)** | Your personal defaults across all projects |

- The primary file for all scopes is `settings.json`.
- Reference: [Claude Code settings documentation](https://docs.claude.com/en/docs/claude-code/settings).

---

### 10.2 Claude Code CLI — Settings File Locations

- **Primary `settings.json` files (paths shown for Windows; `~` = `C:\Users\<username>`):**

| Scope | Path (Windows) | Committed to git? |
|---|---|---|
| **User (Global)** | `C:\Users\<username>\.claude\settings.json` | No |
| **Project (shared)** | `<repo>\.claude\settings.json` | Yes |
| **Local (personal)** | `<repo>\.claude\settings.local.json` | No (auto-gitignored) |
| **Managed (IT/MDM)** | `C:\Program Files\ClaudeCode\managed-settings.json` | No (deployed by admin) |

- **Equivalent paths on other operating systems**

| Scope | macOS | Linux / WSL |
|---|---|---|
| User (Global) | `~/.claude/settings.json` | `~/.claude/settings.json` |
| Managed | `/Library/Application Support/ClaudeCode/managed-settings.json` | `/etc/claude-code/managed-settings.json` |

---

- **Additional Claude Code configuration files (user scope)**

| File | Path (Windows) | Contents |
|---|---|---|
| `.claude.json` | `%USERPROFILE%\.claude.json` | UI preferences (theme, editor mode), OAuth session, user/local MCP server configs, per-project state, caches |
| `CLAUDE.md` (user memory) | `%USERPROFILE%\.claude\CLAUDE.md` | Personal instructions injected into every session |
| Subagents | `%USERPROFILE%\.claude\agents\` | User-defined subagent definitions |

- **Managed policy locations (for IT administrators):**

- **Windows Group Policy / Intune:** registry key `HKLM\SOFTWARE\Policies\ClaudeCode` — a `REG_SZ` or `REG_EXPAND_SZ` value containing the settings JSON.
- **Windows (user-level policy):** `HKCU\SOFTWARE\Policies\ClaudeCode` (lowest-priority policy source).
- **macOS MDM:** managed preferences domain `com.anthropic.claudecode` (Jamf, Kandji, etc.).

---

- **Drop-in directory (all platforms):** Alongside `managed-settings.json`, a `managed-settings.d/` directory is also read.
- All `*.json` files inside it are merged alphabetically on top of the base file — arrays are concatenated and de-duplicated, objects are deep-merged.
- Useful for splitting policies (e.g. `10-telemetry.json`, `20-security.json`).

| Platform | Drop-in directory |
|---|---|
| Windows | `C:\Program Files\ClaudeCode\managed-settings.d\` |
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.d/` |
| Linux / WSL | `/etc/claude-code/managed-settings.d/` |

- **Note:** Recent Claude Code versions deprecated the legacy Windows path `C:\ProgramData\ClaudeCode\managed-settings.json` in favour of `C:\Program Files\ClaudeCode\managed-settings.json`. Verify against the current [managed settings docs](https://docs.claude.com/en/docs/claude-code/settings) before rolling out — the supported path has changed once and may change again.

- **MCP servers — where they live:** User- and local-scope MCP server configs are stored in `%USERPROFILE%\.claude.json`. **Project-shared** MCP servers live in a separate file at the repo root, `.\.mcp.json` (not under `.claude\`) — this is the file your team checks into git to share MCP servers with colleagues.

---

<!-- _class: diagram-slide -->
### 10.3 Claude Code VS Code Extension — Settings File Locations

- The extension has **two distinct types of settings**:

![VS Code extension settings vs Claude Code settings (file locations)](images/claude_7_3_vscode_settings.png)


---

- **a) VS Code extension settings** — control how the extension behaves *inside* VS Code (panel position, initial permission mode, Python env activation, …). These use keys prefixed with `claudeCode.*` and are stored in VS Code's own settings files:

| Scope | Path (Windows) |
|---|---|
| **User (VS Code)** | `C:\Users\<username>\AppData\Roaming\Code\User\settings.json` |
| **Workspace (VS Code)** | `<repo>\.vscode\settings.json` |

- Open via `Ctrl+,` → **Extensions → Claude Code**, or type `/` in the Claude panel and pick **General Config**.
- Example keys: `claudeCode.initialPermissionMode`, `claudeCode.useTerminal`, `claudeCode.usePythonEnvironment`, `claudeCode.disableLoginPrompt`.

---

- **b) Claude Code settings (shared with the CLI)** — everything that defines *Claude's* behaviour (allowed commands, environment variables, hooks, MCP servers, permissions, model, …). These are stored in **exactly the same files as the CLI** — see Section 10.2:

| Scope | Path (Windows) |
|---|---|
| User (Global) | `C:\Users\<username>\.claude\settings.json` |
| Project (shared) | `<repo>\.claude\settings.json` |
| Local (personal) | `<repo>\.claude\settings.local.json` |

- **Tip:** Add `"$schema": "https://json.schemastore.org/claude-code-settings.json"` to your `settings.json` to get autocomplete and inline validation for Claude Code keys directly inside VS Code.

- **Rule of thumb — where should a setting go?**

| If the setting is about… | Put it in… |
|---|---|
| How the VS Code panel looks / behaves (IDE-only) | VS Code user or workspace `settings.json` (`claudeCode.*`) |
| What Claude is allowed to do, hooks, MCP servers, env vars, model | `%USERPROFILE%\.claude\settings.json` or `.claude\settings.json` |
| Personal tweaks for one repo, not shared with the team | `.claude\settings.local.json` |
| Org-wide lockdown policies | Managed settings (see Section 10.2) |

---

### 10.4 Claude Desktop App — Settings File Locations

- The Claude Desktop App (Chat / Cowork) uses a **completely separate** configuration system from Claude Code.
- It does **not** read `%USERPROFILE%\.claude\settings.json`.

- **Primary user-editable file — `claude_desktop_config.json`:**

| OS | Path |
|---|---|
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json`<br/>(expands to `C:\Users\<username>\AppData\Roaming\Claude\claude_desktop_config.json`) |
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |

- **Linux:** Anthropic officially ships Claude Desktop only for **Windows and macOS**. There is no supported Linux build; unofficial community packages typically use `~/.config/Claude/claude_desktop_config.json`, but this is not documented or supported by Anthropic.

---

- **Purpose:** primarily declares which **MCP servers** Claude Desktop starts at launch (key: `mcpServers`). It is the only Claude Desktop file officially documented for user editing.
- **Does not exist by default** — it is created the first time you click **Edit Config** (see below) or when you create it manually.
- **Changes are not hot-reloaded** — fully quit and restart Claude Desktop after editing.
- **Reference:** [MCP quickstart — Claude Desktop](https://modelcontextprotocol.io/quickstart/user).

- **Easy access from the UI:**

- Open Claude Desktop → click the **Claude** menu (menu bar on macOS, top-left on Windows — *not* the in-window settings) → **Settings…**
- Go to the **Developer** tab in the left sidebar → click **Edit Config**.
- Claude Desktop opens `claude_desktop_config.json` in your default editor (and creates it if missing).

---

- **Log files (useful for MCP troubleshooting)**

| OS | Log directory |
|---|---|
| Windows | `%APPDATA%\Claude\logs\` |
| macOS | `~/Library/Logs/Claude/` |

- `mcp.log` — general MCP connection events and failures.
- `mcp-server-<name>.log` — stderr of each individual MCP server.

- **Other data stored by Claude Desktop (managed automatically, not for manual editing):**

- **Cowork / project local cache** — where Claude Desktop keeps a local copy of uploaded knowledge-base files (see also Section 8.9):
  - Windows: `C:\Users\<username>\AppData\Roaming\Claude\local-agent-mode-sessions\<session-id>\.project-cache\<project-id>\files\`

- **Keep apart:** Claude Desktop's `%APPDATA%\Claude\` folder and Claude Code's `%USERPROFILE%\.claude\` folder are **different directories with different purposes**. Editing one has no effect on the other.

---

- **Comparison — Claude Code vs. Claude Desktop (Windows)**

| | Claude Code (CLI + VS Code) | Claude Desktop App |
|---|---|---|
| Main config file | `C:\Users\<user>\.claude\settings.json` | `C:\Users\<user>\AppData\Roaming\Claude\claude_desktop_config.json` |
| Scopes | User / Project / Local / Managed | User only |
| Primary purpose | Permissions, hooks, MCP, env vars, model | MCP servers |
| UI access | `/config` command, VS Code Settings | Settings → Developer → Edit Config |
| Shared between tools | Yes (CLI ↔ VS Code extension) | No (isolated) |

---

## 11. Claude Code — Beyond this tutorial

Use this chapter as a **signpost**. Full, up-to-date detail is always in **[Claude Code — documentation hub](https://code.claude.com/docs/en/overview)** (`code.claude.com`).

### 11.1 Hooks — gate and automate Claude’s actions

- **Hooks** run your scripts before/after tool use (lint, format, block risky commands).
- **[Hooks reference](https://code.claude.com/docs/en/hooks)** — events, matchers, stdin/stdout JSON schema, exit codes.
- **[Automate workflows with hooks (guide)](https://code.claude.com/docs/en/hooks-guide)** — practical patterns.

### 11.2 Slash commands — built-in `/…` plus custom workflows

- **Built-in commands** (`/compact`, `/mcp`, `/doctor`, …) and **team- or repo-scoped prompts** live under slash commands/skills flows.
- **[Commands reference](https://code.claude.com/docs/en/commands)** — built-in slash commands.
- **[Extend Claude with skills](https://code.claude.com/docs/en/skills)** — bundled skills & custom slash-style workflows tied to `.claude/`.

---

### 11.3 Subagents and multi-agent setups

- **Subagents** split work with isolated context; **agent teams** coordinate multiple agents.
- **[Create custom subagents](https://code.claude.com/docs/en/sub-agents)** — definitions in `.claude/agents/`, when to delegate.
- **[Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)** — multi-agent coordination.

### 11.4 Permissions, modes, and sandboxing

- Goes beyond *Ask / Plan / …* from §7.5: **declarative allow/deny rules**, extra paths, and **sandboxed Bash**.
- **[Configure permissions](https://code.claude.com/docs/en/permissions)** — rules in `settings.json`, `additionalDirectories`, etc.
- **[Choose a permission mode](https://code.claude.com/docs/en/permission-modes)** — permission modes in the UI/CLI.
- **[Sandboxing](https://code.claude.com/docs/en/sandboxing)** — isolated command execution.
- **[Security](https://code.claude.com/docs/en/security)** — safeguards and safe use.

---

### 11.5 Built-in tools and editor integration

- Native tools (read/edit files, **Bash**, search, web, todos, …) are separate from MCP.
- **[Tools reference](https://code.claude.com/docs/en/tools-reference)** — each tool and permission expectations.
- **[How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)** — agent loop and built-in tools overview.
- **[Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)** — `@` file/folder mentions, panel, diffs.
- **[JetBrains IDEs](https://code.claude.com/docs/en/jetbrains)** — IntelliJ / PyCharm / WebStorm plugin.

### 11.6 Memory, `.claude/` layout, and troubleshooting

- **`CLAUDE.md`**, **auto memory**, imports, and what lives under **`.claude/`** (hooks, skills, commands, agents).
- **[How Claude remembers your project](https://code.claude.com/docs/en/memory)** — memory & `CLAUDE.md`.
- **[Explore the `.claude` directory](https://code.claude.com/docs/en/claude-directory)** — project vs user `~/.claude`.
- **[Debug your configuration](https://code.claude.com/docs/en/debug-your-config)** — `/doctor`, `/context`, `/hooks`, `/mcp`.

---

### 11.7 MCP (advanced), authentication, models, and costs

- **OAuth / HTTP MCP**, server lifecycle, org policies — beyond §7.7’s stdio example.
- **[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)** — transports, approval, troubleshooting.
- **[Authentication](https://code.claude.com/docs/en/authentication)** — login, tokens, teams/organizations.
- **[Model configuration](https://code.claude.com/docs/en/model-config)** — aliases, choosing models.
- **[Manage costs effectively](https://code.claude.com/docs/en/costs)** — usage, limits, efficiency tips.
- **[Data usage](https://code.claude.com/docs/en/data-usage)** — what Anthropic processes for Claude Code.

### 11.8 CLI: flags, headless use, environment variables

- **Non-interactive** runs (`-p`), output formats, resume/continue — for scripts and CI.
- **[CLI reference](https://code.claude.com/docs/en/cli-reference)** — all `claude` subcommands and flags.
- **[Run Claude Code programmatically](https://code.claude.com/docs/en/headless)** — piping, automation patterns.
- **[Work with sessions](https://code.claude.com/docs/en/agent-sdk/sessions)** — continue, resume, fork (Agent SDK; relevant for advanced automation).
- **[Environment variables](https://code.claude.com/docs/en/env-vars)** — `ANTHROPIC_*`, provider toggles, tuning.

---

### 11.9 Plugins, Agent SDK, enterprise backends, and CI

- **Plugins** bundle skills, agents, hooks, MCP; **Agent SDK** embeds Claude Code in your apps; **Bedrock / Vertex / Foundry** for enterprise API routing; **GitHub/GitLab** for automated reviews.
- **[Extend Claude Code (features overview)](https://code.claude.com/docs/en/features-overview)** — when to use which extension mechanism.
- **[Create plugins](https://code.claude.com/docs/en/plugins)** · **[Plugins reference](https://code.claude.com/docs/en/plugins-reference)**.
- **[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)** — build on the same engine as the CLI.
- **[Enterprise deployment (third-party integrations)](https://code.claude.com/docs/en/third-party-integrations)** — overview of provider options.
- **[Claude Code on Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock)** · **[Claude Code on Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai)** · **[Claude Code on Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry)**.
- **[Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)** · **[Claude Code GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)**.

