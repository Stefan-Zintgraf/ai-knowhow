# AI Agent Project Architecture Guide

## Context

Starting a large project from scratch that shall be created via AI agents. Multiple techniques will be used (e.g. Outlook plugins, webapp, maybe browser plugins, Python, C#, TypeScript, JavaScript). The goal is to keep a stable and maintainable architecture, human as well as AI readable and maintainable solution that can be enhanced starting from a small POC (Outlook plugin) up to an AI-driven company helper agent.

This guide covers potential agent middleware software, architecture templates, coding conventions, code and architecture review approaches, and more.

---

## Agent Orchestration & Middleware

These tools help you coordinate multiple AI agents, manage workflows, and abstract away the plumbing:

### Open Source

- **LangGraph** (by LangChain) — graph-based agent orchestration, supports multi-step workflows, tool use, human-in-the-loop. Python & JS/TS. Very popular for exactly this kind of "start small, grow into complex agent flows" pattern.
- **CrewAI** — multi-agent framework where you define agents with roles, goals, and tools. Good for team-of-agents patterns.
- **AutoGen** (Microsoft) — multi-agent conversation framework. Strong in .NET/Python ecosystems, relevant given your C#/Outlook angle.
- **Semantic Kernel** (Microsoft) — SDK for integrating LLMs into apps. First-class C# and Python support. Excellent fit for your Outlook plugin starting point since it's deeply integrated with the Microsoft ecosystem.
- **Haystack** (deepset) — pipeline-based framework, more RAG-focused but extensible to agents.

### Commercial

- **Azure AI Agent Service** — managed agent hosting, integrates with Semantic Kernel, Office/Outlook, and Azure resources out of the box.
- **AWS Bedrock Agents** — similar managed approach on AWS.
- **Anthropic's Claude with MCP (Model Context Protocol)** — open protocol for connecting AI to tools/data sources. Growing ecosystem of connectors.

### Recommendation

Start with **Semantic Kernel** for the Outlook plugin (natural C# fit), and use **MCP** as your tool connectivity standard so you can plug in new capabilities without rewriting agent logic.

---

## Architecture Templates & Patterns

There's no single "AI agent architecture template repo" that dominates yet, but strong patterns are emerging:

- **Microsoft's AI App Templates** — GitHub org `Azure-Samples` has dozens of reference architectures (RAG apps, agent apps, Office add-ins with AI). Search for "semantic-kernel-starters" and "ai-app-templates."
- **LangChain Templates** — pre-built agent architectures you can fork and customize.
- **The "Agent Protocol"** (agent-protocol.ai) — an open spec for standardizing how agents expose their capabilities. Helps if you want interoperability between your agents regardless of language.
- **Monorepo structure** — for a multi-tech project like yours, consider a monorepo (using **Nx**, **Turborepo**, or even just a well-structured folder convention) with shared schemas/contracts. This is critical for AI readability — agents work best when there's a single source of truth for data models and interfaces.

### Practical Architecture for This Scenario

```
/repo
  /packages
    /shared-types        # TypeScript/JSON Schema — contracts everything shares
    /outlook-plugin      # C# / VSTO or Web Add-in (TS)
    /webapp              # React/TS frontend
    /browser-extension   # TS
    /agent-core          # Python — orchestration, LLM calls, tool routing
    /api-gateway         # Python or TS — unified REST/WebSocket API
  /docs
    /architecture        # ADRs (Architecture Decision Records)
    /conventions         # Coding standards per language
  /tools
    /mcp-servers         # MCP tool connectors
```

---

## Coding Conventions & AI-Readable Code

This is underrated but crucial. AI agents (including coding agents) work dramatically better with:

- **Architecture Decision Records (ADRs)** — lightweight markdown docs explaining *why* decisions were made. Tools: `adr-tools`, or just a `/docs/decisions` folder. AI agents can read these to understand context.
- **Structured README and CONVENTIONS.md files** — per-package files describing the module's purpose, key patterns, and constraints. This is essentially a "system prompt" for any AI that works on that code.
- **OpenAPI / JSON Schema for all interfaces** — machine-readable contracts between services. Generate types from these for each language.
- **EditorConfig + language-specific linters** — `.editorconfig`, ESLint/Prettier (TS/JS), Ruff/Black (Python), .editorconfig + Roslyn analyzers (C#). Consistency helps AI agents produce conforming code.
- **Conventional Commits** — structured commit messages that AI can parse for changelog generation and impact analysis.

---

## Code & Architecture Review

- **SonarQube / SonarCloud** — multi-language static analysis (C#, Python, TS, JS all supported). Free for open source, commercial for private repos.
- **CodeRabbit** — AI-powered code review bot for PRs. Understands architectural patterns and can enforce conventions.
- **GitHub Copilot Code Review** — newer, but integrated into the PR workflow.
- **ArchUnit** (.NET: ArchUnitNET) — write testable architecture rules (e.g., "nothing in the plugin layer may depend on the webapp layer"). These are executable architecture constraints.
- **Dependency Cruiser** (JS/TS) — validates and visualizes module dependencies against rules you define.
- **Claude Code / Cursor / Aider** — for AI-assisted development with codebase awareness. Claude Code in particular can work across your monorepo and understand cross-cutting concerns.

---

## Practical Starting Path

1. **Start with Semantic Kernel + Outlook Web Add-in** (TypeScript-based add-ins are more portable than VSTO). Get a working POC that calls an LLM to do something useful with email.
2. **Define shared contracts early** — even if it's just a few JSON schemas for "what is a task" or "what is a conversation context."
3. **Set up MCP servers** for your tool integrations from the start — this gives you a uniform way to add capabilities later.
4. **Use ADRs from day one** — even simple ones. Your future self and your AI agents will thank you.
5. **Pick a monorepo tool** (Nx if you want heavy structure, Turborepo if you want lightweight, or just clean folder conventions if you want minimal tooling).

---

## Next Steps to Explore

- A concrete architecture document for the project
- A comparison of Semantic Kernel vs LangGraph for this use case
- A starter project structure with boilerplate
