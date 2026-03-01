# OutlookClaudeAddin - Documentation Index

**Generated:** 2026-02-26 | **Scan Level:** Deep | **Mode:** Initial Scan

## Project Overview

- **Type:** Monolith (single VSTO Outlook Add-in)
- **Primary Language:** C# (.NET Framework 4.7.2)
- **Architecture:** MVVM + Service Layer + Tool/Command Pattern
- **Purpose:** AI-powered email assistant integrating Claude into Microsoft Outlook via a chat-based task pane

## Quick Reference

- **Tech Stack:** C# / .NET 4.7.2 / VSTO 4.0 / WPF / Newtonsoft.Json / Anthropic Claude API
- **Entry Point:** `ThisAddIn.cs` → `ThisAddIn_Startup`
- **Architecture Pattern:** MVVM with Service Layer and Tool/Command dispatch
- **Source Files:** 22 C# + 2 XAML
- **AI Model:** claude-sonnet-4-6 (4096 tokens, tool_use protocol)
- **Tools:** 19 Outlook automation tools (18 active, 1 disabled)
- **UI Language:** German | **Tool Results:** English

## Generated Documentation

- [Project Overview](./project-overview.md) — Executive summary, tech stack, classification
- [Architecture](./architecture.md) — Full architecture with diagrams, layers, data flow, security
- [Source Tree Analysis](./source-tree-analysis.md) — Annotated directory tree with entry points
- [Component Inventory](./component-inventory.md) — All UI, tool, core, and service components
- [Development Guide](./development-guide.md) — Prerequisites, build, debug, adding tools, testing

## Existing Project Documentation

- [CLAUDE.md](../CLAUDE.md) — Build environment notes, MSBuild commands, certificate setup
- [AGENTS.md](../AGENTS.md) — AI agent instructions (points to CLAUDE.md)
- [Project Context](../_bmad-output/project-context.md) — Comprehensive AI coding rules (42 rules)
- [Sprint 1: Discovery](../brainstorming/BMAD_Sprint_1_Discovery.md) — Reverse engineering sprint plan
- [Sprint 2: Stability](../brainstorming/BMAD_Sprint_2_Stability.md) — Stability improvements plan
- [Sprint 3: Modernization](../brainstorming/BMAD_Sprint_3_Modernization.md) — Modernization plan

## Getting Started

1. **New developer?** Start with the [Development Guide](./development-guide.md) for setup instructions
2. **Understanding the codebase?** Read [Architecture](./architecture.md) for the full system overview
3. **Looking for a specific component?** Check the [Component Inventory](./component-inventory.md)
4. **Navigating the code?** See the [Source Tree Analysis](./source-tree-analysis.md)
5. **Working with AI agents?** Read [Project Context](../_bmad-output/project-context.md) for coding rules
6. **Planning features?** Use this index as input to the BMAD PRD workflow
