# Comprehensive Claude Code Guide: Basic to Advanced

This document merges resources from multiple tutorials and references into a single, comprehensive guide for **Claude Code**. It covers everything from basic CLI usage to advanced agentic workflows, programmatic SDKs, and enterprise configuration.

**Sources**:
- *Claude Code Tutorials 1b* (Advanced Resources & Feature Map)
- *Claude Code Tutorials 2b* (Feature-Complete Index)
- *Claude Code Tutorials 2* (Practical Text-Based Tutorials)


---

## Table of Contents

1. [Feature Matrix: When to Use Which Mechanism](#0-feature-matrix-when-to-use-which-mechanism)
2. [PART I: Core Operation & Basics](#part-i-core-operation--basics)
   - [1. CLI Modes & Core Operation](#1-cli-modes--core-operation)
   - [2. Interactive Mode & Session UX](#2-interactive-mode--session-ux)
   - [3. IDE & Editor Integrations](#3-ide--editor-integrations)
   - [4. Project Memory & Configuration (CLAUDE.md, Settings)](#4-project-memory--configuration-claudemd-settings)
   - [5. Slash Commands & Custom Commands](#5-slash-commands--custom-commands)
   - [6. Usage, Cost Tracking, Privacy & Data Usage](#6-usage-cost-tracking-privacy--data-usage)
3. [PART II: Advanced Functionality](#part-ii-advanced-functionality)
   - [7. Tools, Permissions, IAM & Security](#7-tools-permissions-iam--security)
   - [8. Checkpointing, Rewind & Safety Nets](#8-checkpointing-rewind--safety-nets)
   - [9. Browser Automation / Chrome Extension](#9-browser-automation--chrome-extension)
   - [10. Sandboxing, Environments & Enterprise Network Setup](#10-sandboxing-environments--enterprise-network-setup)
   - [11. Output Styles & Structured Outputs](#11-output-styles--structured-outputs)
4. [PART III: Agentic Workflow (Subagents & Skills)](#part-iii-agentic-workflow-subagents--skills)
   - [12. Delegation & Orchestration (Subagents)](#12-delegation--orchestration-subagents)
   - [13. Automatic Procedures (Agent Skills)](#13-automatic-procedures-agent-skills)
   - [14. Agent Design Patterns & Concepts](#14-agent-design-patterns--concepts)
5. [PART IV: Extensibility System (Hooks, Plugins, MCP)](#part-iv-extensibility-system-hooks-plugins-mcp)
   - [15. Hooks & Enforcement](#15-hooks--enforcement)
   - [16. Plugins (Packaging Capabilities)](#16-plugins-packaging-capabilities)
   - [17. External Context & Integrations (MCP)](#17-external-context--integrations-mcp)
6. [PART V: Expert & Programmatic Usage](#part-v-expert--programmatic-usage)
   - [18. Programmatic / Headless Usage (Agent SDK)](#18-programmatic--headless-usage-agent-sdk)
7. [PART VI: Additional Resources](#part-vi-additional-resources)
   - [19. Multi-Agent Collaboration Setups](#19-multi-agent-collaboration-setups)
   - [20. End‑to‑End “All Features” Tutorials](#20-endtoend-all-features-tutorials)
   - [21. Written “Power User” Cheat-Sheets & Capability Maps](#21-written-power-user-cheat-sheets--capability-maps)
   - [22. Recommended Learning Path (Text-Only)](#22-recommended-learning-path-text-only)

---

## 0. Feature Matrix: When to Use Which Mechanism

This table summarizes the key mechanisms in Claude Code, combining the feature map from *Tutorial 1b* with the expanded capabilities listed in *Tutorial 2b*.

| Mechanism | What it Extends | Typical Use Cases | Key Docs / Guides |
|----------|------------------|-------------------|-------------------|
| **IDE Integration** | Workflow environment | Using Claude Code directly within VS Code or JetBrains | [VS Code docs](https://code.claude.com/docs/en/vs-code), [JetBrains docs](https://code.claude.com/docs/en/jetbrains) |
| **CLAUDE.md / Memory** | Persistent project-specific instructions | Project conventions, architecture notes, coding standards | [Best practices](https://www.anthropic.com/engineering/claude-code-best-practices), [Builder.io guide](https://www.builder.io/blog/claude-code) |
| **Settings / Config** | Tooling, hooks, plugins, model defaults | Enabling/disabling features per project/user | [Hooks guide](https://code.claude.com/docs/en/hooks-guide), [Plugins reference](https://code.claude.com/docs/en/plugins-reference) |
| **Slash Commands** | UX shortcuts and custom commands | `/format`, `/security-scan`, `/init-project`, invoking skills or hooks | [Ultimate guide](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45), [Builder.io guide](https://www.builder.io/blog/claude-code) |
| **Checkpointing** | Session safety and history | Refactoring with safety nets, "undo trails", persistent sessions | [Checkpointing docs](https://code.claude.com/docs/en/checkpointing) |
| **Browser Integration** | Capabilities | End-to-end testing, reading documentation from web, web extraction | [Chrome extension](https://code.claude.com/docs/en/chrome-extension) |
| **Sandboxing** | Execution environment | Enterprise network constraints, sandboxed bash execution, dev containers | [Dev Containers](https://code.claude.com/docs/en/devcontainer), [Network Config](https://code.claude.com/docs/en/network-config) |
| **Agents / Subagents** | Behavior, role, and tools of Claude within a project or globally | Architect/Builder/Reviewer personas, parallel sessions, role-specialized workflows | [Subagents docs](https://code.claude.com/docs/en/sub-agents), [Agent SDK article](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) |
| **Skills (Agent Skills)** | Procedural knowledge and workflows as reusable folders | Profilers, simulators, data pipelines, domain-specific workflows | [Skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) |
| **Hooks** | Automation triggered by events (e.g., tool use, prompts, stop) | Auto-formatting, logging, policy enforcement, notifications, safety rails | [Hooks reference](https://code.claude.com/docs/en/hooks), [Hooks guide](https://code.claude.com/docs/en/hooks-guide) |
| **Plugins** | Bundled feature packs: agents, skills, hooks, MCP, slash commands | Installable “toolboxes” adding many capabilities at once | [Plugins docs](https://anthropic.mintlify.app/en/docs/claude-code/plugins), [Plugin repos](https://github.com/jeremylongshore/claude-code-plugins-plus) |
| **MCP Servers** | External tools/services integrated as callable tools | Databases, web APIs, internal services, code search, Perplexity integration | [Plugins + MCP docs](https://anthropic.mintlify.app/en/docs/claude-code/plugins), [Composio plugin blog](https://composio.dev/blog/claude-code-plugin) |

---

# PART I: Core Operation & Basics

## 1. CLI Modes & Core Operation

### What it is
- Start interactive REPL, start with an initial prompt, continue/resume sessions, update the CLI, configure MCP from CLI, and run non-interactively.

### Official docs
- **CLI reference (commands + flags)**: https://code.claude.com/docs/en/cli-reference  
- **Setup & authentication**: https://code.claude.com/docs/en/setup  
- **Common workflows (advanced usage patterns)**: https://code.claude.com/docs/en/common-workflows

### Useful deep dives (written)
- **DeepWiki “CLI Commands & Interaction Modes”**: https://deepwiki.com/anthropics/claude-code/2.3-cli-commands-and-interaction-modes  
- **Shipyard CLI cheatsheet (text)**: https://shipyard.build/blog/claude-code-cheat-sheet/

---

## 2. Interactive Mode & Session UX

### What it is
- Keyboard shortcuts, multiline input, background bash tasks, vim mode, history, verbosity toggles, model switching, permission mode switching.

### Official docs
- **Interactive mode reference**: https://code.claude.com/docs/en/interactive-mode

---

## 3. IDE & Editor Integrations

### What it is
- Use Claude Code inside VS Code or JetBrains with native UX, diffs, selections, and shortcuts.

### Official docs
- **VS Code**: https://code.claude.com/docs/en/vs-code  
- **JetBrains**: https://code.claude.com/docs/en/jetbrains

---

## 4. Project Memory & Configuration (CLAUDE.md, Settings)

### What it is
- `CLAUDE.md` project memory files, and configuration via global/user/project settings.
- Configurable hooks and permission rules, tool behavior, and other runtime preferences.

### Official docs
- **Settings (global + project)**: https://code.claude.com/docs/en/settings  
- **Overview & navigation**: https://code.claude.com/docs/en/overview

### Additional Details (Feature Map)
**CLAUDE.md (Project Memory)**
- Described in tips/guides such as Builder.io and “20 tips to master Claude Code”.
- Stores persistent project context, conventions, and preferences that all agents in the project can read.
- **Reference**: https://www.builder.io/blog/claude-code

**Settings and Config Files**
- User and project settings JSON define tools, hooks, plugins, models, and feature toggles.
- Many guides show having Claude generate a starter settings file with hooks and custom commands.
- **Reference**: https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45

---

## 5. Slash Commands & Custom Commands

### What it is
- Built-in slash commands (e.g., `/agents`, `/hooks`, `/mcp`, `/plugin`, `/memory`, `/sandbox`, `/rewind`, `/statusline`, `/review`, `/security-review`, etc.)
- Custom slash commands stored as Markdown files (project- or user-scoped), including arguments and namespacing.
- Plugin-provided commands and MCP slash commands.

### Official docs
- **Slash commands (built-in + custom + plugin/MCP command mechanics)**: https://code.claude.com/docs/en/slash-commands

### Additional Details (Feature Map)
- **Slash Commands**: Part of the plugin system; custom commands registered via plugin schemas (e.g. `/format`, `/security-scan`). Used as shortcuts for common tasks or to trigger Skills/hook‑backed workflows.
- **Built‑in Commands & Config**: Examples: `/agents`, `/hooks`, `/plugins`, `/init`, `/output-style`, etc., documented in practice in long-form tips articles.
- **Tutorial**: https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45

---

## 6. Usage, Cost Tracking, Privacy & Data Usage

### What it is
- Cost/usage views and plan limits (often via slash commands like `/cost` and `/usage`).
- Privacy settings and data usage/training preferences for eligible plans.

### Official docs
- **Data usage policy and settings**: https://code.claude.com/docs/en/data-usage  
- **Overview (links to privacy/security sections)**: https://code.claude.com/docs/en/overview

---

# PART II: Advanced Functionality

## 7. Tools, Permissions, IAM & Security

### What it is
- Tool scoping: which tools exist and how they’re authorized.
- Permission modes and policy controls.
- Enterprise IAM and access control.

### Official docs
- **Tools**: https://code.claude.com/docs/en/tools  
- **Permissions**: https://code.claude.com/docs/en/permissions  
- **Security overview**: https://code.claude.com/docs/en/security  
- **Identity and Access Management (IAM)**: https://code.claude.com/docs/en/iam

---

## 8. Checkpointing, Rewind & Safety Nets

### What it is
- Automatic checkpoints before edits, persistence across sessions, and rewind/restore.
- Supports ambitious refactors with an “undo trail”.

### Official docs
- **Checkpointing**: https://code.claude.com/docs/en/checkpointing

---

## 9. Browser Automation / Chrome Extension

### What it is
- Browser automation and web-testing style workflows via the Claude Code Chrome extension.

### Official docs
- **Chrome extension (see “See also” from CLI reference)**: https://code.claude.com/docs/en/chrome-extension

---

## 10. Sandboxing, Environments & Enterprise Network Setup

### What it is
- Sandboxed execution modes (e.g., sandboxed bash), consistent dev environments, and enterprise networking constraints.

### Official docs
- **Development containers**: https://code.claude.com/docs/en/devcontainer  
- **Enterprise network configuration**: https://code.claude.com/docs/en/network-config  
- **Claude Code on the web**: https://code.claude.com/docs/en/claude-code-on-the-web

---

## 11. Output Styles & Structured Outputs

### What it is
- Output styles: use Claude Code as different “agent personas” while keeping tools and workflow support.
- Structured output formats in print/headless mode (e.g., JSON / stream-JSON + optional JSON schema).

### Official docs
- **Output styles**: https://code.claude.com/docs/en/output-styles  
- **Programmatic usage (includes `--output-format`)**: https://code.claude.com/docs/en/headless

---

# PART III: Agentic Workflow (Subagents & Skills)

## 12. Delegation & Orchestration (Subagents)

### Overview
- **Agents / Subagents (roles/personas)**: Define project‑ and user‑scoped subagents with their own instructions, tools, and behaviors. Used for multi‑agent setups (Architect, Builder, Reviewer, Scribe, etc.) and parallel work sessions.
- **What it is (CLI)**: Specialized subagents with separate prompts, tools, permissions, and (optionally) Skills. Advanced patterns: chaining subagents, dynamic subagent selection, resumable subagents.

### Official Documentation
- **Subagents Guide**: `https://code.claude.com/docs/en/sub-agents`
  - Explains how to create and manage subagents via `/agents`, including project vs. user scope and allowed tools.
  - Describes how delegation works, context separation, and example workflows such as using a planner agent plus specialist subagents.

### Tutorials & Practical Guides (Text)
1.  **Shipyard.dev – Claude Code Subagents Quickstart**
    - *Why it’s useful*: Clear explanation of what subagents are; Concrete `.md` agent configuration examples; Focus on real developer workflows.
    - *Article*: https://dev.to/shipyard/claude-code-subagents-quickstart-what-they-are-how-to-use-them-2jgc

2.  **Dev.to – Subagents & Task Delegation (Series)**
    - *Why it’s useful*: Shows how to delegate complex tasks; Explains how Claude decides to invoke subagents; Practical delegation strategies.
    - *Article*: https://dev.to/letanure/claude-code-part-6-subagents-and-task-delegation-k6f

### Templates & Examples
- **Subagent Best Practices & Templates**: Reusable agent personas; Best-practice YAML frontmatter; Prompt design patterns for subagents.  
  - *Repo*: https://github.com/rvalen1123/ai-resources-and-guides/blob/main/guides/claude-code/subagent-best-practices.md

---

## 13. Automatic Procedures (Agent Skills)

### Overview
- **Skills System (Agent Skills)**: Skills are folder‑based capabilities (SKILL.md + scripts/templates) that agents can auto‑load for specialized workflows. `allowed-tools` allow restrictions.
- **What it is (CLI)**: Model-invoked capabilities (“procedures with rails”) defined via `SKILL.md`. Multi-file Skills supported via progressive disclosure.

### Official Documentation
- **Skill Authoring Best Practices**: `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`
  - Documents SKILL.md format, metadata, and discovery rules so agents can load skills efficiently.
  - Provides guidance on keeping skills concise, deterministic, and reusable across Claude Code, Claude.ai, and the API.

### Tutorials & Deep Dives
1.  **Claude Agent Skills Deep Dive**
    - *Content*: First-principles explanation of skills as folder-based capabilities with workflows and scripts. Shows patterns like Search–Analyze–Report and Read–Process–Write.
    - *URL*: https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/

2.  **Ultimate Guide to Extending Claude Code with Skills (Gist)**
    - *Content*: A text-only “ultimate guide” to extending Claude Code with custom skills and utilities. Covers folder layouts, SKILL.md design, and advanced integration patterns like skill factories.
    - *URL*: https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935

3.  **.NET‑Focused Skills Guide**
    - *Content*: Walks through creating and using Claude Code skills specifically in a C#/.NET environment. Shows real project examples, including architecture validation and multi-step workflows.
    - *URL*: https://www.hrishidigital.com.au/blog/claude-code-skills-dotnet-guide/

### Templates & Repositories
1.  **Awesome Claude Skills**
    - *Content*: Curated list of skills, example SKILL.md files, and usage notes for different domains.
    - *Repo*: https://github.com/VoltAgent/awesome-claude-skills

2.  **Claude Code Skills – Example Repository**
    - *Content*: Real `SKILL.md` examples; Multi-file skill layouts; Practical descriptions that trigger correct Skill usage.
    - *Repo*: https://github.com/alirezarezvani/claude-code-skills-examples

---

## 14. Agent Design Patterns & Concepts

### Understanding Agents & Workflows
- **Agent Design Lessons from Claude Code**: Discusses agent roles, subagent patterns, TODO‑driven design, and tool usage strategies. Gives concrete configuration examples and design heuristics for stable behaviors.
  - *URL*: https://jannesklaas.github.io/ai/2025/07/20/claude-code-agent-design.html

- **Understanding Skills, Agents, Subagents & MCP**: Explains when to use Skills vs subagents; Connects Claude Code concepts into a coherent system; Helpful for designing larger workflows.
  - *URL*: https://colinmcnamara.com/blog/understanding-skills-agents-and-mcp-in-claude-code

- **Understanding the Claude Code Full Stack**: Covers Skills, subagents, MCP, hooks; Written from an experienced developer perspective.
  - *URL*: https://alexop.dev/posts/understanding-claude-code-full-stack/

---

# PART IV: Extensibility System (Hooks, Plugins, MCP)

## 15. Hooks & Enforcement

### What it is
- Deterministic lifecycle automation: run shell commands before/after tool execution or at session lifecycle points.
- Typical uses: enforce formatting, block sensitive file edits, auto-run linters/tests, set up environments.
- Hooks are configured via project/user settings or plugin config (e.g. hook JSON referenced from `hooks` in `plugin.json`).

### Official Documentation
- **Hooks guide (how-to)**: https://code.claude.com/docs/en/hooks-guide  
- **Hooks reference (spec)**: https://code.claude.com/docs/en/hooks

### Tutorials & Use Cases
- **Hooks in Claude Code (Full Tutorial)**: https://www.eesel.ai/blog/hooks-in-claude-code
- **Project-Specific Hooks (Builder.io)**: https://www.builder.io/blog/claude-code (concrete examples)
- **Community Hooks Plugins**: https://www.reddit.com/r/ClaudeCode/comments/1o7jyim/i_built_5_productionready_hook_plugins_for_claude/

---

## 16. Plugins (Packaging Capabilities)

### What it is
- Shareable packages that can bundle **slash commands**, **agents**, **Skills**, **hooks**, and **MCP servers**.
- Plugins bundle multiple components: custom agents, Skills, hooks, MCP servers, and slash commands into installable units.
- Plugin install/enable/disable/update and marketplaces.

### Official Documentation
- **Create plugins**: https://code.claude.com/docs/en/plugins  
- **Plugins reference (schemas + CLI commands)**: https://code.claude.com/docs/en/plugins-reference
- **Official Plugins README**: https://github.com/anthropics/claude-code/blob/main/plugins/README.md

### Repositories
- **Claude Code Plugins: Orchestration and Automation**: Contains dozens of agents and orchestrators with documentation.
  - *Repo*: https://github.com/wshobson/agents
- **Claude Code Plugins Plus**: Community plugin hub and skills-centric plugin pack.
  - *Repo*: https://github.com/jeremylongshore/claude-code-plugins-plus
- **Marketplace Example**: https://github.com/Dev-GOM/claude-code-marketplace
- **Claude Code Capabilities**: Reference pack (includes plugins, hooks, skills, subagents).
  - *Repo*: https://github.com/ebeloded/claude-code-capabilities

---

## 17. External Context & Integrations (MCP)

### What it is
- Connect external systems/tools/data sources through the Model Context Protocol.
- Manage connections and auth (often via `/mcp`), and use MCP-provided tools/resources/prompts.
- Enable Claude Code to call external tools/services (APIs, databases, search, proprietary backends) as tools.

### Official Documentation
- **MCP Docs**: https://code.claude.com/docs/en/mcp

### Tutorials
- **Composio Plugin Guide**: Community example of MCP integration.
  - *URL*: https://composio.dev/blog/claude-code-plugin
- **Runtime Management**: Plugin docs and update posts describe runtime enable/disable of MCP servers.
  - *Reference*: https://anthropic.mintlify.app/en/docs/claude-code/plugins

---

# PART V: Expert & Programmatic Usage

## 18. Programmatic / Headless Usage (Agent SDK)

### What it is
- Run Claude Code non-interactively in scripts/CI (`-p` / print mode).
- Use Agent SDK packages (Python/TypeScript) for structured output, callbacks, and native message objects.
- Lets you build and orchestrate agents/subagents in code, outside the CLI/IDE.

### Official Documentation
- **Run programmatically (Agent SDK via CLI + links to SDKs)**: https://code.claude.com/docs/en/headless
- **Building Agents with the Claude Agent SDK**: Describes how to design agents and subagents in code using the Agent SDK. Includes examples of multi-agent orchestration.
  - *URL*: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk

### Demos
- **Claude Agent SDK Demos**: Official demos showing how to build agent and subagent logic programmatically. Includes patterns for tools, skills, and multi-step flows with code examples.
  - *Repo*: https://github.com/anthropics/claude-agent-sdk-demos

---

# PART VI: Additional Resources

## 19. Multi-Agent Collaboration Setups

- **Claude Code Multi-Agent Collaboration Setup**: Provides a concrete multi-agent collaboration setup including configs and examples. Shows how to coordinate agents for code review, implementation, and testing.
  - *Repo*: https://github.com/mkXultra/claude_code_setup

- **CCSwarm: Multi-Agent Orchestration**: A multi-agent orchestration system built on Claude Code, with docs and sample workflows. Useful to study orchestration concepts even if you do not adopt the exact framework.
  - *Repo*: https://github.com/nwiizo/ccswarm

## 20. End‑to‑End “All Features” Tutorials

For written “tour of everything” resources (agents, Skills, hooks, plugins, MCP, CLAUDE.md, slash commands) in one place:

- **Claude Code Best Practices**: https://www.anthropic.com/engineering/claude-code-best-practices
- **Ultimate Claude Code Guide (Dev.to)**: https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45
- **Builder.io: How I use Claude Code (+ best tips)**: https://www.builder.io/blog/claude-code
- **AI‑Native Panaversity: Plugins – putting it all together**: https://ai-native.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows/plugins-putting-it-all-together

## 21. Written “Power User” Cheat-Sheets & Capability Maps

These are useful as **“one-pagers”** for feature discovery (text-only):

- **Claude Code docs map (auto-generated index of documentation pages)**: https://code.claude.com/docs/en/claude_code_docs_map
- **AwesomeClaude “Claude Code Cheatsheet”**: https://awesomeclaude.ai/code-cheatsheet
- **Community capability pack (GitHub)**: https://github.com/ebeloded/claude-code-capabilities

---

## 22. Recommended Learning Path (Text-Only)

For an advanced, non-beginner, text-only path (no videos):

1.  **Foundation**
    - Read Subagents docs for configuration and delegation.
    - Read Claude Code best practices to understand agentic workflows.
2.  **Skills Design**
    - Study Skill authoring best practices for SKILL.md structure.
    - Read the Skills Deep Dive and the .NET guide to see concrete designs.
3.  **Multi-Agent Patterns**
    - Read agent design lessons and “How I Use Every Claude Code Feature” for real-world patterns.
    - Explore multi-agent GitHub setups (awesome skills, plugins, CCSwarm).
4.  **Programmatic Agents**
    - Use the Agent SDK article and demos to move from manual to programmatic orchestration.

---
_Last updated: Merged from 2026-01-03 source files_
