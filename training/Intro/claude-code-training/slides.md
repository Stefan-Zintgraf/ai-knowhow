---
theme: seriph
background: https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80

addons:
  - slidev-component-progress
  - slidev-addon-asciinema
  - slidev-addon-qrcode
  - slidev-addon-bluesky

class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Claude Code Training
  
  By Kenneth Kousen
  
  Learn more at [KouseniT](https://kousenit.com)
drawings:
  persist: false
transition: slide-left
title: "Claude Code Training"
mdc: true
slidev:
  slide-number: true
  controls: true
  progress: true
css: unocss
---

<style>
.slidev-page-num {
  display: block !important;
  opacity: 1 !important;
  visibility: visible !important;
  position: fixed !important;
  bottom: 1rem !important;
  right: 1rem !important;
  z-index: 100 !important;
  color: #666 !important;
  font-size: 0.875rem !important;
}
</style>

# Claude Code Training

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

---

# Contact Info

Ken Kousen  
Kousen IT, Inc.

- ken.kousen@kousenit.com
- http://www.kousenit.com
- http://kousenit.org (blog)
- Social Media:
  - [@kenkousen](https://twitter.com/kenkousen) (twitter)
  - [@kenkousen@foojay.social](https://foojay.social/@kenkousen) (mastodon)
  - [@kousenit.com](https://bsky.app/profile/kousenit.com) (bluesky)
- *Tales from the jar side* (free newsletter)
  - https://kenkousen.substack.com
  - https://youtube.com/@talesfromthejarside

---

# Course Overview

<v-clicks>

- **Duration**: 5 hours of hands-on learning
- **Format**: Instructor-led with multiple labs
- **Hands-on Labs**: Real codebases in Python, JavaScript, Java
- **Prerequisites**: Command-line experience, development background

</v-clicks>

---

# Topics Covered

<v-clicks>

- **Foundation**: Installation, surfaces, CLI basics, code exploration
- **Core Skills**: Testing, documentation, git operations
- **Customization**: CLAUDE.md, skills, hooks, output styles
- **Extensibility**: Plugins, MCP integration
- **Advanced**: Effort Levels, Plan Mode, Ultraplan, Subagents, Agent Teams, SDKs

</v-clicks>

---

# Pricing Plans

<v-clicks>

- **Pro Plan** - $20/month
  - ~10-40 prompts per 5 hours
  - Sonnet 4.6 only
- **Max Plan 5x** - $100/month
  - ~50-200 prompts per 5 hours
  - Sonnet 4.6 or Opus 4.6
- **Max Plan 20x** - $200/month
  - ~200-800 prompts per 5 hours
  - Sonnet 4.6 or Opus 4.6
- **Note**: Opus 4.6 uses 5x more credits than Sonnet 4.6
- **Limits reset**: Every 5 hours

</v-clicks>

📖 **Full details**: [Using Claude Code with your Pro or Max plan](https://support.anthropic.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)

---

# What is Claude Code?

<v-clicks>

- AI development tool across **5 surfaces**: CLI, VS Code, JetBrains, Desktop, Web
- Context-aware codebase understanding
- Autonomous, collaborative, and **multi-agent** modes
- Multi-language support with **LSP code intelligence**
- Integrated git operations
- **Extensible**: Skills, Plugins, MCP, Hooks

</v-clicks>

---
layout: image-right
image: https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80
backgroundSize: cover
---

# Five Surfaces

<v-clicks>

- **CLI (Terminal)** — Full-featured, primary interface
- **VS Code Extension** — Inline diffs, @-mentions, plan review
- **JetBrains Plugin** — IntelliJ, PyCharm, WebStorm
- **Desktop App** — Native Mac/Windows with visual diffs, scheduling, connectors
- **Web (claude.ai/code)** — Browser-based, no local setup required

Local surfaces share: settings, CLAUDE.md, MCP servers, skills, and hooks. Web sessions only inherit repo-committed config — not user-level `~/.claude` settings.

</v-clicks>

---

# Claude Desktop App

<v-clicks>

- **Three tabs**: Chat (general), Cowork (background agent), Code (interactive coding)
- **Visual diff review** with inline comments and "Review code" button
- **Live app preview** with embedded browser and auto-verify
- **Scheduled tasks** — persistent, local, survives restarts
- **Connectors** — GitHub, Slack, Linear, Notion, Google Calendar
- **Computer use** (research preview) — Claude controls screen on macOS/Windows
- **Parallel sessions** with automatic git worktree isolation

</v-clicks>

---

# Claude Code on the Web

<v-clicks>

- **claude.ai/code** — Run tasks on Anthropic cloud infrastructure
- **`--remote` flag**: Start a web session from CLI: `claude --remote "Fix the auth bug"`
- **Diff view**: Review changes file-by-file before creating PRs
- **Auto-fix PRs**: Claude responds to CI failures and review comments automatically
  - **Caveat**: Replies post under your account — may trigger automation (Atlantis, Actions)
- **`/teleport`**: Pull web sessions back to your local terminal
- **Setup**: Connect GitHub, install Claude GitHub App, select environment
- Also accessible from **Claude iOS and Android apps**

</v-clicks>

---

# Dispatch & Remote Control

<v-clicks>

### Dispatch
- Send tasks from your **phone** to your **Desktop app**
- Dispatch routes dev tasks to Code tab, others to Cowork
- Push notification when done or needs approval

### Remote Control
- Continue a **running CLI session** from phone or browser
- `claude --rc` to start with Remote Control enabled
- `/remote-control` to enable mid-session
- Session runs locally — web/mobile is just a window into it

</v-clicks>

---

# Ultraplan

<v-clicks>

- **Cloud-based planning** for complex, codebase-wide changes
- Launch: `/ultraplan migrate the auth service from sessions to JWTs`
- Or include "ultraplan" in any prompt
- Claude drafts the plan in the cloud while **you keep working locally**
- **Browser review**: Inline comments, emoji reactions, outline navigation
- **Execute options**: Run in cloud (creates PR) or teleport back to terminal

</v-clicks>

```
Terminal status indicators:
◇ ultraplan           — Claude is researching and drafting
◇ ultraplan needs your input  — Clarifying question
◆ ultraplan ready     — Plan ready to review in browser
```

---

# Installation

<v-clicks>

- **Preferred**: Native binary installer:
  ```bash
  curl -fsSL https://storage.googleapis.com/anthropic-releases/claude-cli/install.sh | bash
  ```
- Legacy (deprecated): `npm install -g @anthropic-ai/claude-code`
- Set API key: `export ANTHROPIC_API_KEY="your-key"`
- Verify: `claude --version`

</v-clicks>

---

# Basic Usage

<v-clicks>

- Start Claude Code: `claude`
- Natural language prompts
- File-specific requests
- Multi-step workflows

</v-clicks>

---

# Creating Projects from Scratch

<v-clicks>

- **Start from nothing**: Empty directory + idea = working application
- **Iterative development**: Concept → foundation → enhancements
- **Full-stack creation**: UI, logic, styling, tests in one session
- **Real example**: Our `lyrics-trainer` exercise started exactly this way

</v-clicks>

```bash
mkdir my-project && cd my-project && git init
claude
"Create a web app that displays song lyrics one line at a time
with Next, Previous, and Play buttons"
```

---

# Operation Modes

<v-clicks>

- **Command Mode** (default) - Interactive conversation
- **Auto-Accept Mode** (Shift+Tab) - Autonomous execution
- **Plan Mode** (`/plan` or cycle with `Shift+Tab`) - Review plans before execution
- **Auto Mode** - Safety classifier eliminates permission prompts (opt-in)
- **Effort levels**: `/effort low|medium|high` to control reasoning depth
- **Model switch**: `Alt+P` / `Option+P` to change models mid-conversation

</v-clicks>

---
layout: image-right
image: https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80
backgroundSize: cover
---

# Core Productivity Features

<div class="text-center mt-20">
  <h2 class="text-4xl font-bold text-white bg-black bg-opacity-60 px-6 py-3 rounded-lg">
    Get Productive Immediately
  </h2>
  <p class="text-xl text-white bg-black bg-opacity-60 px-4 py-2 rounded mt-4">
    Essential features for daily development work
  </p>
</div>

---

# Code Exploration

<v-clicks>

- Find files, functions, patterns
- Understand system architecture
- Trace dependencies
- Identify frameworks
- Reference specific files with `@path/to/file.java`

</v-clicks>

```bash
"Analyze the UserService class"
"Explain @src/main/java/com/example/UserController.java"
"How does @pom.xml configure Spring Boot?"
```

---

# Test Generation

<v-clicks>

- Unit test creation
- Edge case identification
- Integration tests
- Mock object setup

</v-clicks>

```bash
"Create unit tests for the UserService"
"Add tests for error scenarios"
```

---

# Refactoring Capabilities

<v-clicks>

- Multi-file operations
- Smart refactoring
- Pattern replacement
- Modern syntax adoption

</v-clicks>

---
layout: image-right
image: https://images.unsplash.com/photo-1556075798-4825dfaaf498?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80
---

# Git Integration

<v-clicks>

- Commit message generation
- Branch management
- Merge conflict resolution
- Pull request creation

</v-clicks>

```bash
"Commit these changes with an appropriate message"
"Create a pull request for this feature"
```

---

# Multi-Tool Workflows

<v-clicks>

- **Batch operations**: Call multiple tools in single response
- **Parallel execution**: Run git status + diff + log simultaneously
- **Performance optimization**: Reduces round-trips
- **Complex workflows**: Chain dependent operations

</v-clicks>

```bash
# Parallel git operations
"Show me git status, recent commits, and current diff"

# Multi-file analysis
"Check all test files and their coverage simultaneously"
```

💡 **Pro tip**: Request "in parallel" for faster execution

---

# Documentation Generation

<v-clicks>

- Inline comments
- `README.md` files
- API documentation
- Architecture docs
- `CLAUDE.md` project configuration (covered later)

</v-clicks>

---

# Debugging Workflows

<v-clicks>

- Error message analysis
- Stack trace navigation
- Configuration debugging
- Integration debugging

</v-clicks>

---
layout: image-left
image: https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80
backgroundSize: cover
---

# Essential Workflow Tools

<div class="text-center mt-20">
  <h2 class="text-4xl font-bold text-white bg-black bg-opacity-60 px-6 py-3 rounded-lg">
    Customize Your Experience
  </h2>
  <p class="text-xl text-white bg-black bg-opacity-60 px-4 py-2 rounded mt-4">
    Session management and personalization
  </p>
</div>

---

# CLAUDE.md Files

<v-clicks>

- **Project memory**: `./CLAUDE.md` (shared with team)
- **User memory**: `~/.claude/CLAUDE.md` (personal preferences)
- **Rules directory**: `.claude/rules/` for organized project rules
- Auto-discovered up directory tree
- **Quick add**: Start input with `#` to add memory
- **Automatic memory**: Claude records and recalls across sessions
- **Commands**: `/memory` to edit, `/init` to bootstrap
- **Import files**: Use `@path/to/import` syntax

</v-clicks>

---

# Custom Statusline

<v-clicks>

- **Configure context display**: `~/.claude/settings.json` or `/statusline`
- Shows git branch, status, working directory, custom info
- Keeps important context visible without asking
- Reduces repetitive status checks

</v-clicks>

```json
{
  "statusline": {
    "items": [
      {"type": "git_branch"},
      {"type": "git_status"},
      {"type": "cwd"},
      {"type": "custom", "command": "node -v"}
    ]
  }
}
```

Perfect for teams wanting standardized context visibility

---

# Custom Slash Commands (Skills-First)

<v-clicks>

- **Skills** (`.claude/skills/`) are the modern, recommended approach
- **Commands** (`.claude/commands/`) still work as a lightweight alternative
- Both: filename becomes command name, `$ARGUMENTS` for dynamic content
- **Project scope**: Shared with team via `.claude/skills/` or `.claude/commands/`
- **User scope**: Personal via `~/.claude/skills/` or `~/.claude/commands/`

</v-clicks>

---

# Creating Custom Commands

<v-clicks>

- **Simple commands**: Just a markdown file — no frontmatter needed
- **Skills**: Add YAML frontmatter for model, effort, tools, paths
- **Use `$ARGUMENTS`** or `$0`, `$1` for dynamic content

</v-clicks>

```bash
# Quick command (lightweight)
mkdir -p .claude/commands
echo "Create service for $ARGUMENTS entity" > .claude/commands/service.md

# User command (personal, requires /user: prefix)
mkdir -p ~/.claude/commands  
echo "Fix issue #$ARGUMENTS" > ~/.claude/commands/fix.md

# Usage: /service User  or  /user:fix 123
```

Real-world example:
```markdown
# ~/.claude/commands/docs.md
Update both the README.md and CLAUDE.md files as appropriate.
If either file does not exist, please create it. Generate the
CLAUDE.md file as though the user invoked the init task.
```

---

# Hooks & Automation

<v-clicks>

- **Event-driven workflow automation** with four hook types:
  - **Command hooks**: Run shell commands on events
  - **HTTP hooks**: POST JSON to a URL endpoint
  - **Prompt hooks**: Ask Claude for yes/no decisions
  - **Agent hooks**: Spawn subagents to verify conditions
- **Conditional hooks**: `if` field filters when hooks run (permission rule syntax)
- **PreToolUse**: Modify tool inputs, block dangerous operations
- **Security controls**: Validate and filter operations before they run
- **Configuration**: `~/.claude/settings.json` or `.claude/settings.json`

</v-clicks>

---

# Hook Example: Security Validation

<v-clicks>

- **Pre-validate file edits** before they happen
- Block dangerous operations automatically
- Provide feedback that Claude can respond to

</v-clicks>

```json
{
  "hooks": {
    "PreToolUse": [{
      "type": "command",
      "command": "validate-edit.sh",
      "if": "Edit(**)"
    }]
  }
}
```

---

# Hook Example: Workflow Automation

<v-clicks>

- **Auto-format code** on file write
- Run linters, formatters, or validators
- Maintain code quality automatically

</v-clicks>

```json
{
  "hooks": {
    "PreToolUse": [{
      "type": "command",
      "command": "prettier --write $FILE",
      "if": "Write(**)"
    }]
  }
}
```

---

# Hook Example: Session Management

<v-clicks>

- **SessionEnd hooks** run when conversation ends
- Generate summary reports or logs
- Clean up resources or finalize work

</v-clicks>

```json
{
  "hooks": {
    "SessionEnd": [{
      "type": "command",
      "command": "generate-session-report.sh"
    }]
  }
}
```

**Important**: Treat hook feedback as user input - Claude adjusts if blocked

---

# Hook Events

<v-clicks>

- **Session**: `SessionStart`, `SessionEnd`, `InstructionsLoaded`
- **Tools**: `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PermissionDenied`
- **Teams**: `TeammateIdle`, `TaskCreated`, `TaskCompleted`
- **Files**: `FileChanged`, `CwdChanged`, `WorktreeCreate`, `WorktreeRemove`
- **Config**: `ConfigChange`, `Notification`
- **Context**: `PreCompact`, `PostCompact`
- **MCP**: `Elicitation`, `ElicitationResult`
- **Agent-level hooks**: Skills and agents define their own hooks in frontmatter

</v-clicks>

---

# Customizable Keybindings

<v-clicks>

- **`/keybindings`** command to configure keyboard shortcuts
- **Config file**: `~/.claude/keybindings.json`
- Remap any action to preferred key combinations
- **`chat:newline`** action for configurable multi-line input
- **Argument shorthand**: `$0`, `$1` in custom commands (not just `$ARGUMENTS`)

</v-clicks>

```json
{
  "chat:submit": "enter",
  "chat:newline": "shift+enter",
  "chat:switch_model": "alt+p",
  "chat:open_external_editor": "ctrl+x ctrl+e"
}
```

Key shortcuts: `Ctrl+B` (background), `Ctrl+X Ctrl+K` (kill agents), `Ctrl+X Ctrl+E` (external editor)

---

# LSP: Code Intelligence

<v-clicks>

- **Language Server Protocol** integration for precise code navigation
- **Go to definition**: Jump to where symbols are defined
- **Find references**: Locate all usages across the codebase
- **Hover info**: Get type information and documentation
- **Call hierarchy**: Trace incoming and outgoing calls
- **Workspace symbols**: Search for symbols across the project
- Works with any configured LSP server (TypeScript, Java, Python, etc.)

</v-clicks>

---

# Output Styles

<v-clicks>

- **Customize how Claude presents solutions** to match learning preferences
- **Built-in styles**: "Explanatory" and "Learning" modes
- **Custom styles**: Create your own in `~/.claude/output-styles/`
- **Configure via settings**: Set default style or switch per-session
- **Use cases**:
  - Educational contexts (verbose explanations)
  - Production work (concise, action-focused)
  - Code review (detailed analysis)
  - Quick fixes (minimal commentary)

</v-clicks>

---

# Using Built-in Output Styles

<v-clicks>

- **Explanatory**: Verbose with detailed explanations
- **Learning**: Teaching-focused with step-by-step guidance
- **Configure in settings** or via command line

</v-clicks>

```json
{
  "outputStyle": "explanatory"
}
```

```bash
claude --output-style learning
```

---

# Creating Custom Output Styles

Create `~/.claude/output-styles/production.md`:

```markdown
---
name: Production
description: Concise output for experienced developers
---

# Instructions for Claude

- Be concise and action-focused
- Skip explanations unless asked
- Show code without lengthy preambles
- Assume expert-level knowledge
```

Then use: `claude --output-style production`

---

# Resuming Conversations

<v-clicks>

- **`--continue`**: Automatically resume most recent conversation
- **`--resume`**: Interactive picker showing conversation history with timestamps and message counts
- **Full history restored**: Complete message context maintained (even hundreds of messages)
- **Original settings preserved**: Model and configuration retained
- **Stored locally**: Complete conversation database maintained on your machine

</v-clicks>

```bash
# Continue most recent conversation
claude --continue

# Show conversation picker with details
claude --resume

# Continue with new prompt
claude --continue --print "Continue with my task"
```

---
layout: image-right
image: https://images.unsplash.com/photo-1586953208448-b95a79798f07?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80
---

# Working with Images

<v-clicks>

- **Drag and drop** images into Claude Code window
- **Copy/paste** with `Ctrl+V` (not `Cmd+V` even on a Mac!)
- **Provide file path**: "Analyze this image: `/path/to/screenshot.png`"
- Analyze UI designs, error screenshots, diagrams
- Generate code from visual mockups
- Debug visual issues and layouts

</v-clicks>

```bash
# Common image workflows
"Analyze this error screenshot and suggest fixes"
"Generate HTML/CSS for this UI mockup"
"Explain what this diagram shows"
"Convert this whiteboard sketch to code"
```

---

# Jupyter & Data Science Support

<v-clicks>

- **Read .ipynb files** with full cell outputs
- **Analyze notebooks**: Code, markdown, and visualizations
- **Edit notebook cells**: Use NotebookEdit tool
- **Data analysis workflows**: Process datasets and results
- **Visualization understanding**: Interpret charts and graphs

</v-clicks>

```bash
"Analyze this Jupyter notebook and explain the data pipeline"
"Add error handling to the data processing cells"
"Convert this notebook to a production Python script"
```

---
layout: image-right
image: https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80
backgroundSize: cover
---

# Advanced Features

<div class="mt-20">
  <h2 class="text-4xl font-bold text-white bg-black bg-opacity-60 px-6 py-3 rounded-lg">
    Power User Capabilities
  </h2>
  <p class="text-xl text-white bg-black bg-opacity-60 px-4 py-2 rounded mt-4">
    Complex features for sophisticated workflows
  </p>
</div>

---

# Skills: Persistent Domain Expertise

<v-clicks>

- **Modular capabilities** that extend Claude's functionality beyond the base model
- **Unified with slash commands** (v2.1): Skills and commands merged into one system
- **Three-tier loading system** for efficiency:
  - Metadata (always loaded): Name and description (~100 tokens)
  - Instructions (triggered): Main SKILL.md with procedures
  - Resources (on-demand): Scripts, templates, reference files
- **Hot-reload**: Edit SKILL.md and changes take effect immediately
- **Automatic activation** when contextually relevant
- **Progressive disclosure**: Load only what's needed for each task

</v-clicks>

---

# Built-in Skills

<v-clicks>

Anthropic provides four production-ready Agent Skills:

- **📊 Excel (xlsx)**: Build spreadsheets, generate reports with charts
- **📄 Word (docx)**: Create and format professional documents
- **📽️ PowerPoint (pptx)**: Create and edit presentations
- **📑 PDF (pdf)**: Generate formatted PDF documents and reports

**Usage**: These skills activate automatically when you reference relevant file types or request document creation

</v-clicks>

```bash
# Skills activate automatically
"Create a quarterly report spreadsheet with sales data"
"Generate a PDF proposal document with our company branding"
"Build a presentation deck for the product launch"
```

---

# Creating Custom Skills

<v-clicks>

### Skill Structure
```
~/.claude/skills/my-skill/
├── SKILL.md          # Required: Instructions with YAML frontmatter
├── templates/        # Optional: Reusable templates
├── scripts/          # Optional: Helper scripts
└── reference/        # Optional: Documentation, schemas
```

### Example SKILL.md
```markdown
---
name: Java Spring Generator
description: Generate Spring Boot components following team patterns
effort: high
paths:
  - "src/**/*.java"
---

# Instructions

When generating Spring Boot code:
1. Use constructor injection, not @Autowired
2. Follow package conventions: controller/service/repository
3. Include comprehensive JavaDoc
4. Generate corresponding test files with @SpringBootTest
```

New frontmatter: `effort`, `context: fork`, `paths`, `shell`, `model`

</v-clicks>

---

# Plugins: Team-Wide Extensibility

<v-clicks>

- **Plugin system** (v2.0.12+) provides installable packages of commands, agents, hooks, and MCP servers
- **Plugin marketplace**: Discover and share team workflows
- **Repository-level config**: `extraKnownMarketplaces` for enterprise control
- **Management commands**:
  - `/plugin install <name>` - Install from marketplace
  - `/plugin enable/disable <name>` - Control active plugins
  - `/plugin marketplace` - Browse available plugins
  - `/plugin list` - View installed plugins

</v-clicks>

---

# Plugin Use Cases

<v-clicks>

### Enterprise Workflows
- Standardize code generation patterns across teams
- Enforce security review processes
- Automate compliance documentation
- Integrate with internal tools and APIs

### Team Collaboration
- Share custom commands and agents
- Distribute MCP server configurations
- Maintain consistent development practices
- Onboard new team members faster

### Example
```bash
# Install company's internal plugin
/plugin install acme-corp-standards

# Plugin provides:
# - Custom slash commands for service generation
# - Security review hooks
# - MCP servers for internal APIs
# - Pre-configured output styles
```

</v-clicks>

---
layout: image-right
image: https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80
---

# Effort Levels

<v-clicks>

- **`/effort low|medium|high`** controls reasoning depth
- **Low**: Fast responses for simple tasks
- **Medium**: Balanced reasoning (default)
- **High**: Deep analysis for complex architecture
- **Keywords still work**: "think", "think harder", "ultrathink"
- Can set in skill frontmatter: `effort: high`

</v-clicks>

```bash
/effort high

# Or use keywords in your prompt
"Ultrathink about the best approach for implementing OAuth2"
```

---

# Plan Mode

<v-clicks>

- Type **`/plan`** or cycle with `Shift+Tab` to activate
- Claude presents implementation plan before writing code
- Review strategy, approve, or modify approach
- Perfect for complex, multi-file changes
- **Uses the Plan subagent** behind the scenes
- **`/ultraplan`**: Cloud-based planning for codebase-wide changes (see Surfaces section)

</v-clicks>

---

# Subagents: Specialized Task Handlers

<v-clicks>

- **Autonomous agents** that Claude launches for specialized tasks
- **Dynamic selection**: Claude chooses appropriate subagent automatically
- **Model selection**: Different subagents can use different models
- **Built-in types**:
  - **Plan**: Strategic task decomposition and planning
  - **Explore**: Fast codebase exploration and search
  - **General-purpose**: Full read/write access for complex work
- **Custom agents**: Define in `.claude/agents/` as markdown with YAML frontmatter
  - Specify: `model`, `tools`, `effort`, `hooks`, `permissionMode`
- **Background execution**: `Ctrl+B` to background, `Ctrl+X Ctrl+K` to kill
- **Worktree isolation**: `isolation: "worktree"` for safe parallel work

</v-clicks>

---

# When Claude Uses Subagents

<v-clicks>

### Automatic Activation
Claude launches subagents when tasks match specialized capabilities:

```bash
# Triggers Explore subagent (read-only, fast search)
"Find all API endpoints in this codebase"
"How does authentication work across the project?"

# Triggers Plan subagent
/plan or "Create a plan for adding OAuth"

# Triggers General-purpose subagent (full read/write)
"Generate comprehensive test coverage for UserService"
"Create API documentation for all REST endpoints"
```

**You don't manage this** - Claude handles subagent selection automatically for optimal results

</v-clicks>

---

# Agent Teams (Research Preview)

<v-clicks>

- **Multi-agent orchestration**: A lead agent coordinates multiple teammates
- **Shared task list**: Tasks with dependencies, ownership, and status tracking
- **Independent context**: Each teammate gets its own context window
- **Inter-agent messaging**: Direct messages, broadcasts, and shutdown coordination
- **Automatic work distribution**: Teammates self-claim tasks as they finish

</v-clicks>

```bash
# Enable teams (research preview)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Example prompt
"Create a team to refactor the auth module: one agent updates
the service layer, another updates tests, a third updates docs"
```

---

# How Agent Teams Work

<v-clicks>

- **Lead agent** creates team, breaks work into tasks, assigns teammates
- **Teammates** work independently, report back, claim new tasks
- **Task coordination**: `blocks`/`blockedBy` dependencies prevent conflicts
- **Idle state is normal**: Teammates go idle between turns, wake on message
- **Hook events**: `TeammateIdle`, `TaskCompleted` for automation
- **Best for**: Large refactors, multi-file features, parallel code + test work

</v-clicks>

```
Lead Agent ──→ creates tasks ──→ assigns teammates
     ↑                              │
     └── receives results ←─────────┘
         (via shared task list + messages)
```

---

# Background Agents & Worktree Isolation

<v-clicks>

- **Background agents**: Run tasks while you keep working
  - `Ctrl+B` to background a running agent
  - `Ctrl+X Ctrl+K` to kill all background agents
- **Worktree isolation**: Agents work in temporary git worktrees
  - `claude -w` or `claude --worktree` starts in isolated worktree
  - Subagents support `isolation: "worktree"` for safe parallel work
  - Changes are on a separate branch — merge when ready
- **`/batch` skill**: Parallel changes across many files using worktrees
- **Combined power**: Background + worktree = fearless parallel development

</v-clicks>

---

# Session Management & Cross-Surface Workflows

<v-clicks>

- **`--remote`**: Start a cloud session: `claude --remote "Fix the auth bug"`
- **`/teleport`**: Pull a web session back to your terminal
- **Dispatch**: Send tasks from phone → Desktop app (Pro/Max)
- **Named sessions**: `/rename my-feature` for easy identification
- **PR-linked sessions**: `claude --from-pr 123` resumes PR context
- **Session branching**: `/branch` to branch a conversation
- **Resume picker**: `claude --resume` shows up to 50 recent sessions
- **Auto-memory**: Claude records and recalls context across sessions

</v-clicks>

---

# Auto-Memory

<v-clicks>

- Claude **automatically records and recalls** memories as it works
- Stored at `~/.claude/projects/<project>/memory/`
- **`MEMORY.md`** index file loaded at session start (first 200 lines)
- Topic files loaded on demand when relevant
- **`/memory`** command to view and manage memories
- Memory types: user preferences, feedback, project context, references
- Subagents can maintain their own auto memory
- Toggle with `autoMemoryEnabled` setting

</v-clicks>

---

# Auto Mode

<v-clicks>

- **Eliminates permission prompts** via a background safety classifier
- Classifier reviews each action and allows/blocks automatically
- **Different from Auto-Accept** (`Shift+Tab`): Auto Mode is intelligent, not blanket
- **Allows**: Local file ops, dependency installs, read-only HTTP, pushing to current branch
- **Blocks**: Downloading + executing code, production deploys, force pushes, IAM changes
- **Requirements**: Team/Enterprise/API plan, Sonnet 4.6 or Opus 4.6
- Enable: `--enable-auto-mode` or cycle with `Shift+Tab`

</v-clicks>

---

# Scheduled Tasks: Three Tiers

<v-clicks>

| | **`/loop`** | **Desktop** | **Cloud** |
|---|---|---|---|
| **Runs on** | Your machine | Your machine | Anthropic cloud |
| **Requires open session** | Yes | No | No |
| **Persistent** | No | Yes | Yes |
| **Local file access** | Yes | Yes | No |
| **Min interval** | 1 minute | 1 minute | 1 hour |

</v-clicks>

---

# Using Scheduled Tasks

<v-clicks>

- **`/loop`** — Session-scoped polling: `/loop 5m check if the deployment finished`
- **Desktop** — Persistent local tasks that survive restarts
- **Cloud** — Always-on via `/schedule` — runs even with your machine off
- Cloud tasks clone the repo fresh each run (default branch)

</v-clicks>

---

# Channels (Research Preview)

<v-clicks>

- **Push events** from external sources into running Claude Code sessions
- Supported: **Telegram**, **Discord**, **iMessage** (via plugins)
- Two-way: Claude reads events and replies back
- Use cases: chat bridge from phone, CI/monitoring webhooks
- **`--channels`** flag to enable: `claude --channels plugin:telegram@claude-plugins-official`
- Requires claude.ai login
- Enterprise: admin must enable `channelsEnabled`

</v-clicks>

---

# Model Context Protocol (MCP)

<v-clicks>

- Standard protocol for AI-to-system connections
- Tool integration (APIs, databases, services)
- Context enhancement for better AI responses
- Security controls and permissions
- **MCP Tool Search** (default since v2.1): Lazy-loads tools on demand
  - Reduces context usage by ~95% with many MCP tools
  - Tools discovered automatically when needed

</v-clicks>

---

# MCP Configuration

<v-clicks>

```bash
# Import from Claude Desktop
claude mcp add-from-claude-desktop

# Add remote server (HTTP)
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# Add local server
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

- **Project config**: `.mcp.json` in project root
- **Management**: `claude mcp list`, `/mcp enable|disable`

</v-clicks>

---

# MCP Server Examples

<v-clicks>

- **GitHub MCP** - Repository operations, issues, PRs
- **Context7** - Downloads latest API docs and examples for modern code
- **Docker MCP Toolkit** - Container management and operations
- **Playwright MCP** - UI test generation and browser automation
- **Heroku MCP** - Deployment and app management

</v-clicks>

---

# Setting Up MCP Servers

<v-clicks>

- Interactive setup: `claude mcp`
- Local servers: Full configuration control
- Remote servers: OAuth authentication, zero maintenance
- Docker MCP Toolkit: `docker mcp gateway run`

</v-clicks>

```bash
# List existing MCP servers
claude mcp list

# Add local server
claude mcp add my-server -e API_KEY=123 -- /path/to/server

# Add remote server (HTTP)
claude mcp add --transport http remote-server https://example.com/mcp

# Add Docker MCP toolkit
claude mcp add docker-mcp docker mcp gateway run
```

---

# Claude Code SDKs

<v-clicks>

- **Available SDKs**: TypeScript, Python, Command Line
- **Build AI-powered coding assistants** into your workflows
- **Multi-turn conversations** and session management
- **Custom system prompts** and flexible I/O formats
- **MCP integration** for extended capabilities

</v-clicks>

```bash
# Command line usage
claude -p "Write a function to calculate Fibonacci numbers"
claude -p "Generate a hello world function" --output-format json
```

```typescript
// TypeScript SDK
import { query } from "@anthropic-ai/claude-code";

for await (const message of query({
  prompt: "Write a haiku about foo.py",
  options: { maxTurns: 3 }
})) {
  // Process messages
}
```

---

# SDK: Python Integration

<v-clicks>

- **Async iteration** over Claude responses
- **Context files** passed directly to queries
- **Turn limits** for controlled execution

</v-clicks>

```python
from claude_code import query

async for msg in query("Refactor this module",
                       context_files=["app.py"],
                       max_turns=3):
    print(msg.content)
```

---

# SDK: CI/CD Integration

<v-clicks>

- **Automate code reviews** in pull requests
- **JSON output** for parsing results
- **Integrate with GitHub Actions**, GitLab CI, etc.

</v-clicks>

```yaml
# GitHub Actions example
- name: AI Code Review
  run: |
    claude -p "Review PR changes" --output-format json > review.json
```

---

# SDK: Git Hooks

<v-clicks>

- **Pre-commit security checks** before code is committed
- **Limit tools** for focused, fast execution
- **Fail-fast** on security issues

</v-clicks>

```bash
#!/bin/bash
# .git/hooks/pre-commit
claude -p "Check for security issues" --allowed-tools read,grep
```

---

# VS Code Extension

<v-clicks>

- **Native IDE integration** bringing Claude Code into your editor
- **In-editor experience**: Work with Claude without leaving VS Code
- **Context-aware**: Accesses your workspace files and settings
- **All Claude Code features**: Skills, MCP, custom commands available
- **Installation**: Search "Claude Code" in VS Code Extensions marketplace

</v-clicks>

---

# VS Code Extension Features

<v-clicks>

### Integrated Workflow
- Reference files with `@` syntax directly in VS Code
- View diffs and approve changes inline
- **Session management** with AI-generated titles, rename, fork
- **Plan view panel** with full markdown and commenting
- **MCP server management** via `/mcp` in extension
- **Compaction display** as collapsible card

### Also Available
- **JetBrains Plugin**: IntelliJ, PyCharm, WebStorm — same core features

</v-clicks>

---
layout: image-left
image: https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80
backgroundSize: cover
---

# Management & Control

<div class="mt-20">
  <h2 class="text-4xl font-bold text-white bg-black bg-opacity-70 px-6 py-3 rounded-lg">
    Monitor and Control
  </h2>
  <p class="text-xl text-white bg-black bg-opacity-70 px-4 py-2 rounded mt-4">
    Cost, context, and permission management
  </p>
</div>

---

# Cost Monitoring

<v-clicks>

- Use `/cost` command to check usage
- Shows current usage and limits
- Pro Plan: Displays prompt count vs limit
- Max Plans: Shows monthly usage summary
- Limits reset every 5 hours
- Plan ahead for intensive work sessions

</v-clicks>

```bash
# Check your current usage
/cost

# Example output (Pro Plan):
# 📊 Cost information:
#    - Input tokens: 1,245
#    - Output tokens: 3,782
#    - Total cost: $0.076

# Example output (Max Plan):
# With your Claude Max subscription, no need to monitor cost
# — your subscription includes Claude Code usage
```

---

# Context Management

<v-clicks>

- Use `/compact` command to compress conversation history
- Claude Code automatically compacts when context limit approaches
- Warning message appears before auto-compaction
- Preserves essential information while reducing token usage
- Manual compaction gives you control over timing

</v-clicks>

```bash
# Manually compact the conversation
/compact

# Warning message example:
# ⚠️ Context limit approaching. Auto-compacting in next response
# to preserve conversation history and continue working.
```

---

# Smart Context Management

<v-clicks>

- **Auto-compaction**: Automatic when approaching limits
- **Warning messages**: Advance notice before compaction
- **Preservation strategy**: Keeps essential information
- **Manual control**: Use `/compact` proactively
- **Long conversations**: Maintains context over hundreds of messages

</v-clicks>

```bash
# Warning you'll see:
⚠️ Context limit approaching. Auto-compacting in next response
to preserve conversation history and continue working.

# Proactive management:
/compact  # Compress conversation manually
```

---

# Configuring Permissions

<v-clicks>

- **Fine-grained control** over Claude Code's capabilities
- **Use `/permissions` UI** to manage tool permissions
- **Allow/Deny rules** for specific tools and actions
- **Enterprise policies** for organization-wide control
- **Permission precedence**: Enterprise → CLI → Project → User

</v-clicks>

```bash
# Example permission rules
Bash(npm run test:*)     # Allow npm test commands
Edit(docs/**)           # Allow editing docs directory
Read(src/*)             # Allow reading source files

# Access permissions UI
/permissions
```

---

# Permission Modes

<v-clicks>

### Six modes (cycle with `Shift+Tab`)
- **Default**: Prompts for each action
- **Accept Edits**: Auto-approves file edits
- **Plan**: Read-only exploration, no edits
- **Auto**: Safety classifier decides (Team/Enterprise/API)
- **Don't Ask**: Only pre-approved tools run (CI/CD)
- **Bypass Permissions**: No prompts at all

</v-clicks>

```bash
# Quick permission profiles via aliases
alias claude-dev='claude --allowed-tools all'
alias claude-review='claude --allowed-tools read,grep'
alias claude-safe='claude --disabled-tools bash,webfetch'
alias claude-ci='claude --allowed-tools bash,git,test'
```

---
layout: image-left
image: https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80
backgroundSize: cover
---

# Team & Best Practices

<div class="text-center mt-20">
  <h2 class="text-4xl font-bold text-white bg-black bg-opacity-60 px-6 py-3 rounded-lg">
    Collaborate Effectively
  </h2>
  <p class="text-xl text-white bg-black bg-opacity-60 px-4 py-2 rounded mt-4">
    Team workflows and professional practices
  </p>
</div>

---

# Git Worktrees for Parallel Sessions

<v-clicks>

- **Built-in worktree support**: `claude -w` or `claude --worktree`
  - Automatically creates isolated worktree + new branch
  - Prompts to keep or remove on session exit
- **Manual worktrees** also work for full control
- Share git history while isolating working files
- Perfect for multi-feature development

</v-clicks>

```bash
# Built-in (preferred) — automatic isolation
claude -w                     # Start in new worktree
claude --worktree             # Same thing

# Manual worktrees for full control
git worktree add ../project-feature-a -b feature-a
cd ../project-feature-a && claude

# Manage worktrees
git worktree list
git worktree remove ../project-feature-a
```

---

# Effective Prompting & Best Practices

<div class="grid grid-cols-2 gap-8">
<div>

### Effective Prompting
<v-clicks>

- **Be specific** about what you want to achieve
- **Provide context** about your goals and constraints
- **Use iterative refinement** for complex tasks
- **Include examples** when possible to show desired patterns

</v-clicks>

</div>
<div>

### Best Practices
<v-clicks>

- **Create a git branch first** for any significant changes
- **Commit checkpoints regularly** during development
- **Review all AI-generated code** before accepting
- **Test generated code** thoroughly

</v-clicks>

</div>
</div>

---

# Troubleshooting & Configuration

<v-clicks>

### System Health Check
```bash
claude /doctor  # Diagnose installation issues
```

### Global Configuration
```bash
claude config set -g model claude-sonnet-4-6
claude config set -g verbose true
claude config set -g max_conversation_turns 10
```

### Check Current Settings
```bash
claude config list  # View all settings
echo $ANTHROPIC_API_KEY  # Verify API key
```

</v-clicks>

---

# Security & Permissions

<v-clicks>

### Security-Focused Aliases
```bash
# Safe mode - limited tools
alias claude-safe='claude --allowed-tools read,write,edit'

# Review mode - read-only
alias claude-review='claude --allowed-tools read,grep'

# Development mode - all tools
alias claude-dev='claude --allowed-tools all'
```

### Tool Restrictions
```bash
# Disable specific tools
claude --disabled-tools bash,webfetch

# Allow only specific tools
claude --allowed-tools read,write,edit,task
```

</v-clicks>

---

# Common Issues: Installation

<v-clicks>

- **Command not found** → Check PATH: `npm list -g @anthropic/claude-code`
- **Permission denied** → Use correct npm prefix or sudo
- **Windows users** → WSL is required (not native Windows)

</v-clicks>

```bash
# Preferred: Native binary installer
curl -fsSL https://storage.googleapis.com/anthropic-releases/claude-cli/install.sh | bash

# Legacy npm (deprecated but still works)
npm uninstall -g @anthropic/claude-code
npm install -g @anthropic/claude-code
```

---

# Common Issues: Runtime

<v-clicks>

- **API key not found** → Set `ANTHROPIC_API_KEY` environment variable
- **Rate limits** → Use `/cost` to monitor usage
- **Context too large** → Use `/compact` to reduce conversation size

</v-clicks>

```bash
# Alternative installation: Direct binary
curl -fsSL https://storage.googleapis.com/anthropic-releases/claude-cli/install.sh | bash
```

---

# Development Process

<v-clicks>

- Start with clean git state
- Generate tests if none exist
- Commit checkpoints regularly
- Use Claude for git workflows (commits, issues, merges)
- Use git worktrees for parallel sessions on different branches
- Review changes before accepting
- Test generated code thoroughly

</v-clicks>

---

# Team Collaboration

<v-clicks>

- Share `CLAUDE.md` configurations
- Document successful patterns
- Review AI-generated code together
- Establish team conventions

</v-clicks>

---

# New Commands: Workflow

<v-clicks>

| Command | Description |
|---------|-------------|
| `/effort low\|medium\|high` | Set reasoning depth |
| `/plan` | Enter Plan Mode from prompt |
| `/ultraplan` | Cloud-based planning session |
| `/batch` | Parallel changes across codebase |
| `/loop 5m prompt` | Recurring prompt execution |
| `/memory` | View and manage auto-memory |

</v-clicks>

---

# New Commands: Utilities

<v-clicks>

| Command | Description |
|---------|-------------|
| `/branch` | Branch the conversation (was `/fork`) |
| `/copy N` | Copy Nth-latest response to clipboard |
| `/context` | Get context optimization suggestions |
| `/color` | Set prompt-bar color for session |
| `/powerup` | Interactive feature lessons |

**Removed**: `/tag`, `/vim` (use `/config`). **Deprecated**: `/output-style` (use `/config`)

</v-clicks>

---

# Quick Access

<div class="grid grid-cols-2 gap-8 mt-8 place-items-center">
  <div class="flex flex-col items-center">
    <h3>Claude Code Docs</h3>
    <QRCode
      :width="200"
      :height="200"
      type="svg"
      data="https://docs.anthropic.com/en/docs/claude-code/overview"
      :margin="5"
      :dotsOptions="{ type: 'rounded', color: '#3b82f6' }"
    />
    <p class="text-sm mt-2">docs.anthropic.com/claude-code</p>
  </div>
  <div class="flex flex-col items-center">
    <h3>Course Repository</h3>
    <QRCode
      :width="200"
      :height="200"
      type="svg"
      data="https://github.com/kousen/claude-code-training"
      :margin="5"
      :dotsOptions="{ type: 'rounded', color: '#10b981' }"
    />
    <p class="text-sm mt-2">github.com/kousen/claude-code-training</p>
  </div>
</div>

---

# Important Links

<div class="mt-8 space-y-6 text-xl">

<v-clicks>

### 📚 Claude Code Documentation
`https://docs.anthropic.com/en/docs/claude-code`

### 🐙 Official GitHub Repository  
`https://github.com/anthropics/claude-code`

### 💻 Course Source Code & Exercises
`https://github.com/kousen/claude-code-training`

### 🆘 Support & Issues
`https://github.com/anthropics/claude-code/issues`

</v-clicks>

</div>

---

# Thank You!

<div class="text-center">

## Questions?

<div class="pt-12">
  <span class="text-6xl"><carbon:logo-github /></span>
</div>

**Kenneth Kousen**  
*Author, Speaker, Java & AI Expert*

[kousenit.com](https://kousenit.com) | [@kenkousen](https://twitter.com/kenkousen)

</div>