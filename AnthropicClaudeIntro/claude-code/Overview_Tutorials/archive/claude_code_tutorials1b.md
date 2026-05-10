# Advanced Claude Code Tutorial Resources (Text-Only)

This document lists online, **non‑video** tutorials and references for advanced Claude Code usage, focusing on subagents, skills, multi‑agent workflows, plugins, hooks, MCP, and configuration.[1][2][3][4][51][52][56][62][66]

---

## 0. Feature Matrix: When to Use Which Mechanism

| Mechanism | What it Extends | Typical Use Cases | Key Docs / Guides |
|----------|------------------|-------------------|-------------------|
| **Agents / Subagents** | Behavior, role, and tools of Claude within a project or globally | Architect/Builder/Reviewer personas, parallel sessions, role-specialized workflows | Subagents docs[1], Agent SDK article[5] |
| **Skills (Agent Skills)** | Procedural knowledge and workflows as reusable folders | Profilers, simulators, data pipelines, domain-specific workflows | Skill best practices[4], Skills deep dive[3] |
| **Plugins** | Bundled feature packs: agents, skills, hooks, MCP, slash commands | Installable “toolboxes” adding many capabilities at once | Plugins docs[62], Plugins reference[56], Plugin repos[53][55][69] |
| **Hooks** | Automation triggered by events (e.g., tool use, prompts, stop) | Auto-formatting, logging, policy enforcement, notifications, safety rails | Hooks reference[51], Hooks guide[52], Hooks blog[61] |
| **MCP Servers** | External tools/services integrated as callable tools | Databases, web APIs, internal services, code search, Perplexity integration | Plugins + MCP docs[62][56], MCP plugin blog[68] |
| **Slash Commands / Commands** | UX shortcuts and custom commands | `/format`, `/security-scan`, `/init-project`, invoking skills or hooks | Ultimate guide[66], Builder.io guide[63] |
| **CLAUDE.md / Project Knowledge** | Persistent project-specific instructions | Project conventions, architecture notes, coding standards | Best practices[2], Builder.io guide[63] |
| **Settings / Config** | Tooling, hooks, plugins, model defaults | Enabling/disabling features per project/user | Hooks guide[52], Plugins reference[56], Ultimate guide[66] |

---

## 1. Official Anthropic Documentation

### 1.1 Subagents Guide

- **URL**: `https://code.claude.com/docs/en/sub-agents`  
- Explains how to create and manage subagents via `/agents`, including project vs. user scope and allowed tools.[1]  
- Describes how delegation works, context separation, and example workflows such as using a planner agent plus specialist subagents.[1]

### 1.2 Claude Code Best Practices

- **URL**: `https://www.anthropic.com/engineering/claude-code-best-practices`  
- Covers agentic coding patterns, multi-session worktrees, and using Claude Code effectively on real projects.[2]  
- Includes concrete advice on structuring tasks, using tools (Read/Edit/Bash/MCP), and running parallel work via multiple sessions or agents.[2]

### 1.3 Skill Authoring Best Practices

- **URL**: `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`  
- Documents SKILL.md format, metadata, and discovery rules so agents can load skills efficiently.[4]  
- Provides guidance on keeping skills concise, deterministic, and reusable across Claude Code, Claude.ai, and the API.[4]

---

## 2. Advanced Blog Tutorials

### 2.1 Claude Agent Skills Deep Dive

- **URL**: `https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/`  
- First-principles explanation of skills as folder-based capabilities with workflows and scripts.[3]  
- Shows patterns like Search–Analyze–Report and Read–Process–Write, and how to chain skills with subagents for realistic tasks.[3]

### 2.2 Building Agents with the Claude Agent SDK

- **URL**: `https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk`  
- Describes how to design agents and subagents in code using the Agent SDK (beyond the CLI/IDE).[5]  
- Includes examples of multi-agent orchestration, context isolation, and integrating tools/skills in programmatic workflows.[5]

### 2.3 Agent Design Lessons from Claude Code

- **URL**: `https://jannesklaas.github.io/ai/2025/07/20/claude-code-agent-design.html`  
- Discusses agent roles, subagent patterns, TODO‑driven design, and tool usage strategies.[6]  
- Gives concrete configuration examples and design heuristics for stable, predictable agent behaviors.[6]

### 2.4 .NET‑Focused Skills Guide

- **URL**: `https://www.hrishidigital.com.au/blog/claude-code-skills-dotnet-guide/`  
- Walks through creating and using Claude Code skills specifically in a C#/.NET environment.[7]  
- Shows real project examples, including architecture validation and multi-step workflows with skills.[7]

### 2.5 How I Use Every Claude Code Feature

- **URL**: `https://blog.sshh.io/p/how-i-use-every-claude-code-feature`  
- Explains practical use of Claude Code features (agents, subagents, tools, skills) in a unified workflow.[8]  
- Includes advanced patterns for daily development, refactors, and larger multi-agent collaborations.[8]

---

## 3. GitHub Repositories with Tutorials and Configs

### 3.1 Awesome Claude Skills

- **URL**: `https://github.com/VoltAgent/awesome-claude-skills`  
- Curated list of skills, example SKILL.md files, and usage notes for different domains.[9]  
- Helps bootstrap your own skills and see how others structure workflows, scripts, and instructions.[9]

### 3.2 Claude Code Plugins: Orchestration and Automation

- **URL**: `https://github.com/wshobson/agents`  
- Contains dozens of agents and orchestrators with documentation on installation and use.[10]  
- Demonstrates multi-agent setups, plugin-like skills, and automation patterns around Claude Code.[10]

### 3.3 Claude Code Multi-Agent Collaboration Setup

- **URL**: `https://github.com/mkXultra/claude_code_setup`  
- Provides a concrete multi-agent collaboration setup including configs and examples.[11]  
- Shows how to coordinate agents for code review, implementation, and testing across a shared project.[11]

### 3.4 CCSwarm: Multi-Agent Orchestration

- **URL**: `https://github.com/nwiizo/ccswarm`  
- A multi-agent orchestration system built on Claude Code, with docs and sample workflows.[12]  
- Useful to study orchestration concepts even if you do not adopt the exact framework.[12]

### 3.5 Claude Agent SDK Demos

- **URL**: `https://github.com/anthropics/claude-agent-sdk-demos`  
- Official demos showing how to build agent and subagent logic programmatically.[13]  
- Includes patterns for tools, skills, and multi-step flows with code examples.[13]

### 3.6 Ultimate Guide to Extending Claude Code with Skills (Gist)

- **URL**: `https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935`  
- A text-only “ultimate guide” to extending Claude Code with custom skills and utilities.[14]  
- Covers folder layouts, SKILL.md design, and advanced integration patterns like skill factories.[14]

---

## 4. Recommended Learning Path (Text-Only)

For an advanced, non-beginner, text-only path (no videos):[2][3][1]

1. **Foundation**  
   - Read Subagents docs for configuration and delegation.[1]  
   - Read Claude Code best practices to understand agentic workflows.[2]

2. **Skills Design**  
   - Study Skill authoring best practices for SKILL.md structure.[4]  
   - Read the Skills Deep Dive and the .NET guide to see concrete designs.[3][7]

3. **Multi-Agent Patterns**  
   - Read agent design lessons and “How I Use Every Claude Code Feature” for real-world patterns.[6][8]  
   - Explore multi-agent GitHub setups (awesome skills, plugins, CCSwarm).[9][10][12]

4. **Programmatic Agents**  
   - Use the Agent SDK article and demos to move from manual to programmatic orchestration.[5][13]

---

## 5. Claude Code Feature Map (Agents, Skills, Hooks, Plugins, MCP, etc.)

This section lists the main feature mechanisms Claude Code offers, with docs or high‑quality text tutorials for each.[21][51][52][56][62][66]

### 5.1 Agents and Subagents

- **Main Agent & Subagents (roles/personas)**  
  - Docs: `https://code.claude.com/docs/en/sub-agents`[1]  
  - Define project‑ and user‑scoped subagents with their own instructions, tools, and behaviors.  
  - Used for multi‑agent setups (Architect, Builder, Reviewer, Scribe, etc.) and parallel work sessions.[2][25]

- **Agent SDK & Programmatic Agents**  
  - Docs: `https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk`[5]  
  - GitHub demos: `https://github.com/anthropics/claude-agent-sdk-demos`[13]  
  - Lets you build and orchestrate agents/subagents in code, outside the CLI/IDE.

### 5.2 Skills (Agent Skills)

- **Skills System (Agent Skills)**  
  - Best practices: `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`[4]  
  - Deep dive: `https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/`[3]  
  - Skills are folder‑based capabilities (SKILL.md + scripts/templates) that agents can auto‑load for specialized workflows.[3][9]

- **Example and Community Skills**  
  - Awesome list: `https://github.com/VoltAgent/awesome-claude-skills`[9]  
  - Skills‑centric plugin pack: `https://github.com/jeremylongshore/claude-code-plugins-plus`[55]  
  - .NET‑oriented guide: `https://www.hrishidigital.com.au/blog/claude-code-skills-dotnet-guide/`[7]

### 5.3 Plugins and Marketplace

- **Plugin System Overview**  
  - Docs: `https://anthropic.mintlify.app/en/docs/claude-code/plugins`[62]  
  - Reference: `https://code.claude.com/docs/en/plugins-reference`[56]  
  - Plugins bundle multiple components: custom agents, Skills, hooks, MCP servers, and slash commands into installable units.[55][62]

- **Plugin Repositories and Marketplaces**  
  - Official plugins README: `https://github.com/anthropics/claude-code/blob/main/plugins/README.md`[53]  
  - Community plugin hub: `https://github.com/jeremylongshore/claude-code-plugins-plus`[55]  
  - Marketplace example: `https://github.com/Dev-GOM/claude-code-marketplace`[69]  
  - Plugins can add extra Skills directories, hook configs, and MCP server definitions via `plugin.json`.[56]

### 5.4 Hooks (Automation on Events)

- **Hook Docs (Reference + Guide)**  
  - Reference: `https://code.claude.com/docs/en/hooks`[51]  
  - Getting started: `https://code.claude.com/docs/en/hooks-guide`[52]  
  - Hooks let you run shell commands on events such as `PreToolUse`, `PostToolUse`, `PermissionRequest`, `UserPromptSubmit`, `Notification`, and `Stop`.[51][52]

- **Use Cases and Examples**  
  - Full text tutorial: `https://www.eesel.ai/blog/hooks-in-claude-code`[61]  
  - Builder.io: `https://www.builder.io/blog/claude-code` (project‑specific hooks and commands with concrete examples).[63]  
  - Community hooks plugins: `https://www.reddit.com/r/ClaudeCode/comments/1o7jyim/i_built_5_productionready_hook_plugins_for_claude/`[54]

Hooks are configured via project/user settings or plugin config (e.g. hook JSON referenced from `hooks` in `plugin.json`), and can enforce policies, auto‑format, log usage, or send notifications.[51][52][56]

### 5.5 MCP (Model Context Protocol) Integration

- **MCP Servers**  
  - Included in plugins via `.mcp.json` or inline `mcpServers` in `plugin.json`.[56][62]  
  - Enable Claude Code to call external tools/services (APIs, databases, search, proprietary backends) as tools.  
  - Community example: Composio plugin guide: `https://composio.dev/blog/claude-code-plugin`[68]

- **Runtime Management**  
  - Plugin docs and update posts describe runtime enable/disable of MCP servers and context‑window management when many servers are active.[62][59]

### 5.6 Slash Commands and Commands

- **Slash Commands**  
  - Part of the plugin system; custom commands registered via plugin schemas (e.g. `/format`, `/security-scan`).[55][56][62]  
  - Used as shortcuts for common tasks or to trigger Skills/hook‑backed workflows.

- **Built‑in Commands & Config**  
  - Examples: `/agents`, `/hooks`, `/plugins`, `/init`, `/output-style`, etc., documented in practice in long-form tips articles.[63][66]  
  - Tutorial: `https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45`[66]

### 5.7 Project Knowledge and Configuration

- **CLAUDE.md (Project Memory)**  
  - Described in tips/guides such as Builder.io and “20 tips to master Claude Code”.[63][60]  
  - Stores persistent project context, conventions, and preferences that all agents in the project can read.

- **Settings and Config Files**  
  - User and project settings JSON define tools, hooks, plugins, models, and feature toggles.[52][56][63]  
  - Many guides show having Claude generate a starter settings file with hooks and custom commands.[63][66]

### 5.8 End‑to‑End “All Features” Tutorials

For written “tour of everything” resources (agents, Skills, hooks, plugins, MCP, CLAUDE.md, slash commands) in one place:[21][63][66][67]

- **Claude Code Best Practices**  
  - `https://www.anthropic.com/engineering/claude-code-best-practices`[2]

- **Ultimate Claude Code Guide (Dev.to)**  
  - `https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45`[66]

- **Builder.io: How I use Claude Code (+ best tips)**  
  - `https://www.builder.io/blog/claude-code`[63]

- **AI‑Native Panaversity: Plugins – putting it all together**  
  - `https://ai-native.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows/plugins-putting-it-all-together`[67]

---

[1](https://code.claude.com/docs/en/sub-agents)  
[2](https://www.anthropic.com/engineering/claude-code-best-practices)  
[3](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)  
[4](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)  
[5](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)  
[6](https://jannesklaas.github.io/ai/2025/07/20/claude-code-agent-design.html)  
[7](https://www.hrishidigital.com.au/blog/claude-code-skills-dotnet-guide/)  
[8](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)  
[9](https://github.com/VoltAgent/awesome-claude-skills)  
[10](https://github.com/wshobson/agents)  
[11](https://github.com/mkXultra/claude_code_setup)  
[12](https://github.com/nwiizo/ccswarm)  
[13](https://github.com/anthropics/claude-agent-sdk-demos)  
[14](https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935)  
[21](https://www.anthropic.com/engineering/claude-code-best-practices)  
[51](https://code.claude.com/docs/en/hooks)  
[52](https://code.claude.com/docs/en/hooks-guide)  
[53](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)  
[54](https://www.reddit.com/r/ClaudeCode/comments/1o7jyim/i_built_5_productionready_hook_plugins_for_claude/)  
[55](https://github.com/jeremylongshore/claude-code-plugins-plus)  
[56](https://code.claude.com/docs/en/plugins-reference)  
[59](https://www.youtube.com/watch?v=wHHNtetJV0c)  
[60](https://creatoreconomy.so/p/20-tips-to-master-claude-code-in-35-min-build-an-app)  
[61](https://www.eesel.ai/blog/hooks-in-claude-code)  
[62](https://anthropic.mintlify.app/en/docs/claude-code/plugins)  
[63](https://www.builder.io/blog/claude-code)  
[66](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45)  
[67](https://ai-native.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows/plugins-putting-it-all-together)  
[68](https://composio.dev/blog/claude-code-plugin)  
[69](https://github.com/Dev-GOM/claude-code-marketplace)
