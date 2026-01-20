# BMad Know-How

This document is a know how document, how to work with BMad.

---

## Table of Contents

1. [Installation](#1-installation)
   - [1.1 Prerequisites](#11-prerequisites)
   - [1.2 Installation](#12-installation)
   - [1.3 Quick Path](#13-quick-path)

---

## 1 Installation

### 1.1 Prerequisites

- **Node.js 20+** — Required for the installer
- **Git** — Recommended for version control
- **AI-powered IDE** — Claude Code, Cursor, Windsurf, or similar
- **A project idea** — Even a simple one works for learning

### 1.2 Installation

Open a terminal in your project directory and run:

```bash
npx bmad-method@alpha install
```

The interactive installer guides you through setup and creates a `_bmad/` folder with all agents and workflows.

Verify your installation:

```
your-project/
├── _bmad/
│   ├── bmm/            # Method module
│   │   ├── agents/     # Agent files
│   │   ├── workflows/  # Workflow files
│   │   └── config.yaml # Module config
│   └── core/           # Core utilities
├── _bmad-output/       # Generated artifacts (created later)
└── .claude/            # IDE configuration (if using Claude Code)
```

### 1.3 Quick Path

- **Install**: `npx bmad-method@alpha install`
- **Initialize**: Load Analyst agent, run `workflow-init`
- **Plan**: PM creates PRD, Architect creates architecture
- **Build**: SM manages sprints, DEV implements stories

**Always use fresh chats** for each workflow to avoid context issues.

