# Advanced Claude Code Tutorial Resources (Text-Only)

This document lists online, **non‑video** tutorials and references for advanced Claude Code usage, focusing on subagents, skills, and multi‑agent workflows.[1][2][3]

***

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

***

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

***

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

***

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

You can save this text as `claude-code-advanced-resources.md` locally and open it in your editor for quick access.

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
