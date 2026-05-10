# Claude Code – Feature-Complete, Text-Only Tutorial Index (Advanced)

This is a **cross-checked (against current Claude Code CLI + docs)**, **non-video**, **advanced** index of *all major Claude Code mechanisms* and where to learn them via **written documentation and templates**.

**No additional sample `.md` files are included** here by design — only direct links to authoritative docs and specific template/example sources.

_Last updated: 2026-01-03_

---

## Table of contents

1. [CLI modes & core operation](#cli-modes--core-operation)  
2. [Interactive mode & session UX](#interactive-mode--session-ux)  
3. [Slash commands & custom commands](#slash-commands--custom-commands)  
4. [Project memory & configuration (CLAUDE.md, settings)](#project-memory--configuration-claudemd-settings)  
5. [Delegation & orchestration (Subagents)](#delegation--orchestration-subagents)  
6. [Automatic procedures (Agent Skills)](#automatic-procedures-agent-skills)  
7. [Hooks & enforcement](#hooks--enforcement)  
8. [Plugins (packaging commands/agents/skills/hooks/MCP)](#plugins-packaging-commandsagentsskillshooksmcp)  
9. [External context & integrations (MCP)](#external-context--integrations-mcp)  
10. [Tools, permissions, IAM & security](#tools-permissions-iam--security)  
11. [Checkpointing, rewind & safety nets](#checkpointing-rewind--safety-nets)  
12. [Output styles & structured outputs](#output-styles--structured-outputs)  
13. [Programmatic / headless usage (Agent SDK)](#programmatic--headless-usage-agent-sdk)  
14. [IDE & editor integrations](#ide--editor-integrations)  
15. [Browser automation / Chrome extension](#browser-automation--chrome-extension)  
16. [Sandboxing, environments & enterprise network setup](#sandboxing-environments--enterprise-network-setup)  
17. [Usage, cost tracking, privacy & data usage](#usage-cost-tracking-privacy--data-usage)  
18. [Written “power user” cheat-sheets & capability maps](#written-power-user-cheat-sheets--capability-maps)

---

## CLI modes & core operation

**What it is**
- Start interactive REPL, start with an initial prompt, continue/resume sessions, update the CLI, configure MCP from CLI, and run non-interactively.

**Official docs**
- CLI reference (commands + flags): https://code.claude.com/docs/en/cli-reference  
- Setup & authentication: https://code.claude.com/docs/en/setup  
- Common workflows (advanced usage patterns): https://code.claude.com/docs/en/common-workflows

**Useful deep dives (written)**
- DeepWiki “CLI Commands & Interaction Modes”: https://deepwiki.com/anthropics/claude-code/2.3-cli-commands-and-interaction-modes  
- Shipyard CLI cheatsheet (text): https://shipyard.build/blog/claude-code-cheat-sheet/

---

## Interactive mode & session UX

**What it is**
- Keyboard shortcuts, multiline input, background bash tasks, vim mode, history, verbosity toggles, model switching, permission mode switching.

**Official docs**
- Interactive mode reference: https://code.claude.com/docs/en/interactive-mode

---

## Slash commands & custom commands

**What it is**
- Built-in slash commands (e.g., /agents, /hooks, /mcp, /plugin, /memory, /sandbox, /rewind, /statusline, /review, /security-review, etc.)
- Custom slash commands stored as Markdown files (project- or user-scoped), including arguments and namespacing.
- Plugin-provided commands and MCP slash commands.

**Official docs**
- Slash commands (built-in + custom + plugin/MCP command mechanics): https://code.claude.com/docs/en/slash-commands

---

## Project memory & configuration (CLAUDE.md, settings)

**What it is**
- `CLAUDE.md` project memory files, and configuration via global/user/project settings.
- Configurable hooks and permission rules, tool behavior, and other runtime preferences.

**Official docs**
- Settings (global + project): https://code.claude.com/docs/en/settings  
- Overview & navigation: https://code.claude.com/docs/en/overview

---

## Delegation & orchestration (Subagents)

**What it is**
- Specialized subagents with separate prompts, tools, permissions, and (optionally) Skills.
- Advanced patterns: chaining subagents, dynamic subagent selection, resumable subagents.

**Official docs**
- Subagents: https://code.claude.com/docs/en/sub-agents

**Practical, written tutorials**
- Subagents quickstart (article, text): https://dev.to/shipyard/claude-code-subagents-quickstart-what-they-are-how-to-use-them-2jgc  
- Subagents + delegation (article, text): https://dev.to/letanure/claude-code-part-6-subagents-and-task-delegation-k6f

**Direct templates / examples**
- Subagent best practices & templates (GitHub):  
  https://github.com/rvalen1123/ai-resources-and-guides/blob/main/guides/claude-code/subagent-best-practices.md

---

## Automatic procedures (Agent Skills)

**What it is**
- Model-invoked capabilities (“procedures with rails”) defined via `SKILL.md`.
- Tool restrictions via `allowed-tools`.
- Multi-file Skills via progressive disclosure.

**Official docs**
- Agent Skills: https://code.claude.com/docs/en/skills

**Direct templates / examples**
- Skills examples repository (GitHub):  
  https://github.com/alirezarezvani/claude-code-skills-examples

---

## Hooks & enforcement

**What it is**
- Deterministic lifecycle automation: run shell commands before/after tool execution or at session lifecycle points.
- Typical uses: enforce formatting, block sensitive file edits, auto-run linters/tests, set up environments.

**Official docs**
- Hooks guide (how-to): https://code.claude.com/docs/en/hooks-guide  
- Hooks reference (spec): https://code.claude.com/docs/en/hooks

---

## Plugins (packaging commands/agents/skills/hooks/MCP)

**What it is**
- Shareable packages that can bundle **slash commands**, **agents**, **Skills**, **hooks**, and **MCP servers**.
- Plugin install/enable/disable/update and marketplaces.

**Official docs**
- Create plugins: https://code.claude.com/docs/en/plugins  
- Plugins reference (schemas + CLI commands): https://code.claude.com/docs/en/plugins-reference

**Direct template / examples**
- “Claude Code capabilities” reference pack (GitHub; includes plugins, hooks, skills, subagents, etc.):  
  https://github.com/ebeloded/claude-code-capabilities

---

## External context & integrations (MCP)

**What it is**
- Connect external systems/tools/data sources through the Model Context Protocol.
- Manage connections and auth (often via `/mcp`), and use MCP-provided tools/resources/prompts.

**Official docs**
- MCP: https://code.claude.com/docs/en/mcp

---

## Tools, permissions, IAM & security

**What it is**
- Tool scoping: which tools exist and how they’re authorized.
- Permission modes and policy controls.
- Enterprise IAM and access control.

**Official docs**
- Tools: https://code.claude.com/docs/en/tools  
- Permissions: https://code.claude.com/docs/en/permissions  
- Security overview: https://code.claude.com/docs/en/security  
- Identity and Access Management (IAM): https://code.claude.com/docs/en/iam

---

## Checkpointing, rewind & safety nets

**What it is**
- Automatic checkpoints before edits, persistence across sessions, and rewind/restore.
- Supports ambitious refactors with an “undo trail”.

**Official docs**
- Checkpointing: https://code.claude.com/docs/en/checkpointing

---

## Output styles & structured outputs

**What it is**
- Output styles: use Claude Code as different “agent personas” while keeping tools and workflow support.
- Structured output formats in print/headless mode (e.g., JSON / stream-JSON + optional JSON schema).

**Official docs**
- Output styles: https://code.claude.com/docs/en/output-styles  
- Programmatic usage includes `--output-format` and JSON schema examples: https://code.claude.com/docs/en/headless

---

## Programmatic / headless usage (Agent SDK)

**What it is**
- Run Claude Code non-interactively in scripts/CI (`-p` / print mode).
- Use Agent SDK packages (Python/TypeScript) for structured output, callbacks, and native message objects.

**Official docs**
- Run programmatically (Agent SDK via CLI + links to SDKs): https://code.claude.com/docs/en/headless

---

## IDE & editor integrations

**What it is**
- Use Claude Code inside VS Code or JetBrains with native UX, diffs, selections, and shortcuts.

**Official docs**
- VS Code: https://code.claude.com/docs/en/vs-code  
- JetBrains: https://code.claude.com/docs/en/jetbrains

---

## Browser automation / Chrome extension

**What it is**
- Browser automation and web-testing style workflows via the Claude Code Chrome extension.

**Official docs**
- Chrome extension (see “See also” from CLI reference if you prefer navigating from there):  
  https://code.claude.com/docs/en/chrome-extension

---

## Sandboxing, environments & enterprise network setup

**What it is**
- Sandboxed execution modes (e.g., sandboxed bash), consistent dev environments, and enterprise networking constraints.

**Official docs**
- Development containers: https://code.claude.com/docs/en/devcontainer  
- Enterprise network configuration: https://code.claude.com/docs/en/network-config  
- Claude Code on the web (environments + network access levels): https://code.claude.com/docs/en/claude-code-on-the-web

---

## Usage, cost tracking, privacy & data usage

**What it is**
- Cost/usage views and plan limits (often via slash commands like `/cost` and `/usage`).
- Privacy settings and data usage/training preferences for eligible plans.

**Official docs**
- Data usage policy and settings: https://code.claude.com/docs/en/data-usage  
- Overview (links to privacy/security sections): https://code.claude.com/docs/en/overview

---

## Written “power user” cheat-sheets & capability maps

These are useful as **“one-pagers”** for feature discovery (text-only):

- Claude Code docs map (auto-generated index of documentation pages):  
  https://code.claude.com/docs/en/claude_code_docs_map  
- AwesomeClaude “Claude Code Cheatsheet” (PDF/PNG links, but the page itself is written):  
  https://awesomeclaude.ai/code-cheatsheet  
- Community capability pack (GitHub):  
  https://github.com/ebeloded/claude-code-capabilities

---

## Notes on completeness

This index was cross-checked against:
- The current **CLI reference** (commands + flags)  
- Built-in **slash commands** list  
- The docs “map” page that enumerates documentation topics

