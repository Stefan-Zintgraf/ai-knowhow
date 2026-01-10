# Claude Code Know-How

This document is a know how document, how to work with Claude Code.

---

## Table of Contents

1. [Installation](#1-installation)
   - [1.1 macOS, Linux, WSL](#11-macos-linux-wsl)
   - [1.2 Windows PowerShell](#12-windows-powershell)
   - [1.3 Windows CMD](#13-windows-cmd)
   - [1.4 Login](#14-login)
2. [Cheat Sheet (important commands)](#2-cheat-sheet-important-commands)
   - [2.1 CLI commands](#21-cli-commands)
   - [2.2 Keyboard shortcuts](#22-keyboard-shortcuts)
   - [2.3 Key CLI flags](#23-key-cli-flags)
   - [2.4 Advanced CLI flags](#24-advanced-cli-flags)
   - [2.5 Built-in slash commands](#25-built-in-slash-commands)
3. [Settings and Configuration](#3-settings-and-configuration)
   - [3.1 Configuration scopes](#31-configuration-scopes)
   - [3.2 Settings files](#32-settings-files)
   - [3.3 Available settings](#33-available-settings)
   - [3.4 Permission settings](#34-permission-settings)
   - [3.5 Sandbox settings](#35-sandbox-settings)
   - [3.6 Attribution settings](#36-attribution-settings)
   - [3.7 File suggestion settings](#37-file-suggestion-settings)
   - [3.8 Hook configuration](#38-hook-configuration)
   - [3.9 Settings precedence](#39-settings-precedence)
   - [3.10 System prompt](#310-system-prompt)
   - [3.11 Excluding sensitive files](#311-excluding-sensitive-files)
   - [3.12 Subagent configuration](#312-subagent-configuration)
   - [3.13 Plugin configuration](#313-plugin-configuration)
   - [3.14 Custom commands](#314-custom-commands)
   - [3.15 Environment variables](#315-environment-variables)
   - [3.16 Tools available to Claude](#316-tools-available-to-claude)
   - [3.17 Bash tool behavior](#317-bash-tool-behavior)
   - [3.18 Extending tools with hooks](#318-extending-tools-with-hooks)
4. [Sessions](#4-sessions)
   - [4.1 workflow](#41-workflow)
5. [MCP Servers](#5-mcp-servers)
   - [5.1 Overview](#51-overview)
   - [5.2 Server Types](#52-server-types)
   - [5.3 Configuration via JSON Files](#53-configuration-via-json-files)
   - [5.4 Using MCP Tools in Commands](#54-using-mcp-tools-in-commands)

---

## 1 Installation

### 1.1 macOS, Linux, WSL:
```
curl -fsSL https://claude.ai/install.sh | bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

### 1.2 Windows PowerShell:
```
irm https://claude.ai/install.ps1 | iex
```

### 1.3 Windows CMD:
```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```


### 1.4 Login

```
claude
# You'll be prompted to log in on first use
```

```
/login
# Follow the prompts to log in with your account
```

## 2 Cheat Sheet (important commands)

### 2.1 CLI commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive mode |
| `claude "task"` | Start with initial prompt (e.g., `claude "fix the build error"`) |
| `claude -p "query"` | Run one-off query, then exit |
| `cat file \| claude -p "query"` | Process piped content |
| `claude -c` | Continue most recent conversation in current directory |
| `claude -c -p "query"` | Continue conversation in non-interactive mode |
| `claude -r` | Resume a previous conversation |
| `claude -r "session" "query"` | Resume specific session by ID or name |
| `claude commit` | Create a Git commit |
| `claude update` | Update Claude Code to latest version |
| `claude mcp` | Configure Model Context Protocol (MCP) servers |
| `/clear` | Clear conversation history |
| `/help` | Show available commands |
| `exit` or `Ctrl+C` | Exit Claude Code |
| `! command` | Run a bash command (e.g., `! ls`, `! git status`) |

### 2.2 Keyboard shortcuts

| Shortcut | Description |
|----------|-------------|
| `Shift+Tab` | Switch between modes in Claude Code |

### 2.3 Key CLI flags

| Flag | Description | Example |
|------|-------------|---------|
| `--model` | Set model (`sonnet`, `opus`) | `claude --model opus "fix bug"` |
| `--output-format` | Output: `text`, `json`, `stream-json` | `claude -p "query" --output-format json` |
| `--verbose` | Verbose logging with turn-by-turn output | `claude --verbose "refactor this"` |
| `--max-turns` | Limit agentic turns (non-interactive) | `claude --max-turns 5 -p "fix errors"` |
| `--add-dir` | Add additional working directories | `claude --add-dir /other/project` |
| `--system-prompt` | Replace system prompt | `claude --system-prompt "Be concise"` |
| `--append-system-prompt` | Append to default system prompt | `claude --append-system-prompt "Use TypeScript"` |
| `--tools` | Restrict available tools | `claude --tools Read,Grep "search code"` |
| `--debug` | Enable debug mode | `claude --debug` |
| `--version, -v` | Output version number | `claude --version` |

### 2.4 Advanced CLI flags

| Flag | Description | Example |
|------|-------------|---------|
| `--permission-mode` | Permission mode for session (choices: `acceptEdits`, `bypassPermissions`, `default`, `delegate`, `dontAsk`, `plan`) | `claude --permission-mode plan "design the system"` |
| `--agent` | Specify agent for the current session | `claude --agent reviewer "review this code"` |
| `--agents` | Define custom agents as JSON | `claude --agents '{"reviewer": {"description": "Reviews code"}}'` |
| `--allowed-tools` | Whitelist specific tools (comma-separated) | `claude --allowed-tools "Bash(git:*) Edit"` |
| `--disallowed-tools` | Blacklist specific tools (comma-separated) | `claude --disallowed-tools "Bash(git:*) Edit"` |
| `--session-id` | Use a specific session ID (UUID format) | `claude --session-id "uuid-here" -c` |
| `--fork-session` | Create new session ID when resuming | `claude -r --fork-session` |
| `--mcp-config` | Load MCP servers from JSON files/strings | `claude --mcp-config ~/mcp-config.json` |
| `--settings` | Load additional settings from file or JSON | `claude --settings ~/settings.json` |
| `--max-budget-usd` | Set maximum spending limit for API calls | `claude -p "task" --max-budget-usd 1.00` |
| `--json-schema` | Validate output against JSON Schema | `claude -p "query" --json-schema '{"type":"object",...}'` |
| `--no-session-persistence` | Disable session saving (use with `-p`) | `claude -p "query" --no-session-persistence` |
| `--disable-slash-commands` | Disable all slash commands in session | `claude --disable-slash-commands` |
| `--input-format` | Input format (`text` or `stream-json`) | `claude -p "query" --input-format stream-json` |
| `--ide` | Auto-connect to IDE if available | `claude --ide` |
| `--chrome` | Enable Claude in Chrome integration | `claude --chrome` |
| `--fallback-model` | Fallback model if primary is overloaded | `claude -p "task" --fallback-model sonnet` |

### 2.5 Built-in slash commands

| Command | Description |
|---------|-------------|
| `/add-dir` | Add additional working directories |
| `/agents` | Manage custom AI subagents for specialized tasks |
| `/bashes` | List and manage background tasks |
| `/bug` | Report bugs (sends conversation to Anthropic) |
| `/clear` | Clear conversation history |
| `/compact [instructions]` | Compact conversation with optional focus instructions |
| `/config` | Open the Settings interface (Config tab) |
| `/context` | Visualize current context usage as a colored grid |
| `/cost` | Show token usage statistics (see cost tracking guide for subscription-specific details) |
| `/doctor` | Checks the health of your Claude Code installation |
| `/exit` | Exit the REPL |
| `/export [filename]` | Export the current conversation to a file or clipboard |
| `/help` | Get usage help |
| `/hooks` | Manage hook configurations for tool events |
| `/ide` | Manage IDE integrations and show status |
| `/init` | Initialize project with CLAUDE.md guide |
| `/install-github-app` | Set up Claude GitHub Actions for a repository |
| `/login` | Switch Anthropic accounts |
| `/logout` | Sign out from your Anthropic account |
| `/mcp` | Manage MCP server connections and OAuth authentication |
| `/memory` | Edit CLAUDE.md memory files |
| `/model` | Select or change the AI model |
| `/output-style [style]` | Set the output style directly or from a selection menu |
| `/permissions` | View or update permissions |
| `/plan` | Enter plan mode directly from the prompt |
| `/plugin` | Manage Claude Code plugins |
| `/pr-comments` | View pull request comments |
| `/privacy-settings` | View and update your privacy settings |
| `/release-notes` | View release notes |
| `/rename <name>` | Rename the current session for easier identification |
| `/remote-env` | Configure remote session environment (claude.ai subscribers) |
| `/resume [session]` | Resume a conversation by ID or name, or open the session picker |
| `/review` | Request code review |
| `/rewind` | Rewind the conversation and/or code |
| `/sandbox` | Enable sandboxed bash tool with filesystem and network isolation for safer, more autonomous execution |
| `/security-review` | Complete a security review of pending changes on the current branch |
| `/stats` | Visualize daily usage, session history, streaks, and model preferences |
| `/status` | Open the Settings interface (Status tab) showing version, model, account, and connectivity |
| `/statusline` | Set up Claude Code's status line UI |
| `/teleport` | Resume a remote session from claude.ai by session ID, or open a picker (claude.ai subscribers) |
| `/terminal-setup` | Install Shift+Enter key binding for newlines (VS Code, Alacritty, Zed, Warp) |
| `/theme` | Change the color theme |
| `/todos` | List current TODO items |
| `/usage` | For subscription plans only: show plan usage limits and rate limit status |
| `/vim` | Enter vim mode for alternating insert and command modes |

**Custom slash commands:** Create reusable commands by saving `.md` files in `.claude/commands/` (project) or `~/.claude/commands/` (personal). The filename becomes the command (e.g., `fix-tests.md` → `/fix-tests`).

## 3 Settings and Configuration

Claude Code offers a variety of settings to configure its behavior. You can configure Claude Code by running the `/config` command when using the interactive REPL, which opens a tabbed Settings interface where you can view status information and modify configuration options.

> **Reference**: For the most up-to-date and comprehensive settings documentation, see the [official Claude Code settings documentation](https://code.claude.com/docs/en/settings).

### 3.1 Configuration scopes

Claude Code uses a **scope system** to determine where configurations apply and who they're shared with. Understanding scopes helps you decide how to configure Claude Code for personal use, team collaboration, or enterprise deployment.

#### Available scopes

| Scope       | Location                           | Who it affects                       | Shared with team?      |
| ----------- | ---------------------------------- | ------------------------------------ | ---------------------- |
| **Managed** | System-level managed-settings.json | All users on the machine             | Yes (deployed by IT)   |
| **User**    | ~/.claude/ directory              | You, across all projects             | No                     |
| **Project** | .claude/ in repository             | All collaborators on this repository | Yes (committed to git) |
| **Local**   | .claude/*.local.* files          | You, in this repository only         | No (gitignored)        |

#### When to use each scope

**Managed scope** is for:
- Security policies that must be enforced organization-wide
- Compliance requirements that can't be overridden
- Standardized configurations deployed by IT/DevOps

**User scope** is best for:
- Personal preferences you want everywhere (themes, editor settings)
- Tools and plugins you use across all projects
- API keys and authentication (stored securely)

**Project scope** is best for:
- Team-shared settings (permissions, hooks, MCP servers)
- Plugins the whole team should have
- Standardizing tooling across collaborators

**Local scope** is best for:
- Personal overrides for a specific project
- Testing configurations before sharing with the team
- Machine-specific settings that won't work for others

#### How scopes interact

When the same setting is configured in multiple scopes, more specific scopes take precedence:
1. **Managed** (highest) - can't be overridden by anything
2. **Command line arguments** - temporary session overrides
3. **Local** - overrides project and user settings
4. **Project** - overrides user settings
5. **User** (lowest) - applies when nothing else specifies the setting

For example, if a permission is allowed in user settings but denied in project settings, the project setting takes precedence and the permission is blocked.

#### What uses scopes

Scopes apply to many Claude Code features:

| Feature         | User location            | Project location               | Local location                |
| --------------- | ------------------------ | ------------------------------ | ----------------------------- |
| **Settings**    | ~/.claude/settings.json | .claude/settings.json          | .claude/settings.local.json   |
| **Subagents**   | ~/.claude/agents/       | .claude/agents/                | —                             |
| **MCP servers** | ~/.claude.json          | .mcp.json                      | ~/.claude.json (per-project) |
| **Plugins**     | ~/.claude/settings.json | .claude/settings.json          | .claude/settings.local.json   |
| **CLAUDE.md**   | ~/.claude/CLAUDE.md     | CLAUDE.md or .claude/CLAUDE.md | CLAUDE.local.md               |

### 3.2 Settings files

The `settings.json` file is the official mechanism for configuring Claude Code through hierarchical settings:

- **User settings** are defined in `~/.claude/settings.json` and apply to all projects.
- **Project settings** are saved in your project directory:
  - `.claude/settings.json` for settings that are checked into source control and shared with your team
  - `.claude/settings.local.json` for settings that are not checked in, useful for personal preferences and experimentation. Claude Code will configure git to ignore `.claude/settings.local.json` when it is created.
- **Managed settings**: For organizations that need centralized control, Claude Code supports `managed-settings.json` and `managed-mcp.json` files that can be deployed to system directories:
  - macOS: `/Library/Application Support/ClaudeCode/`
  - Linux and WSL: `/etc/claude-code/`
  - Windows: `C:\ProgramData\ClaudeCode\`
  
  These are system-wide paths (not user home directories like `~/Library/...`) that require administrator privileges. They are designed to be deployed by IT administrators. Managed settings take the highest precedence and cannot be overridden by user or project settings.
  
  Managed deployments can also restrict **plugin marketplace additions** using `strictKnownMarketplaces`. For more information, see [Managed marketplace restrictions](https://code.claude.com/docs/en/settings#managed-marketplace-restrictions).

- **Other configuration** is stored in `~/.claude.json`. This file contains your preferences (theme, notification settings, editor mode), OAuth session, MCP server configurations for user and local scopes, per-project state (allowed tools, trust settings), and various caches. Project-scoped MCP servers are stored separately in `.mcp.json`.

- **Managed MCP configuration**: For enterprise deployments, MCP servers can be centrally managed via `managed-mcp.json` files in the same system directories as managed settings. This allows IT administrators to deploy standardized MCP server configurations across the organization.

Example `settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

### 3.3 Available settings

`settings.json` supports a number of options:

| Key                        | Description                                                                                                                                                                                                                                                                          | Example                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| `apiKeyHelper`             | Custom script, to be executed in /bin/sh, to generate an auth value. This value will be sent as X-Api-Key and Authorization: Bearer headers for model requests                                                                                                                       | `/bin/generate_temp_api_key.sh`                                        |
| `cleanupPeriodDays`        | Sessions inactive for longer than this period are deleted at startup. Setting to 0 immediately deletes all sessions. (default: 30 days)                                                                                                                                              | `20`                                                                      |
| `companyAnnouncements`     | Announcement to display to users at startup. If multiple announcements are provided, they will be cycled through at random.                                                                                                                                                          | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                      | Environment variables that will be applied to every session                                                                                                                                                                                                                          | `{"FOO": "bar"}`                                                          |
| `attribution`              | Customize attribution for git commits and pull requests. See [Attribution settings](#36-attribution-settings)                                                                                                                                                                       | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                   |
| `includeCoAuthoredBy`      | **Deprecated**: Use attribution instead. Whether to include the co-authored-by Claude byline in git commits and pull requests (default: true)                                                                                                                                        | `false`                                                                   |
| `permissions`              | See [Permission settings](#34-permission-settings) for structure of permissions.                                                                                                                                                                                                   |                                                                         |
| `hooks`                    | Configure custom commands to run before or after tool executions. See [Hook configuration](#38-hook-configuration)                                                                                                                                                               | `{"PreToolUse": {"Bash": "echo 'Running command...'"}}`                   |
| `disableAllHooks`          | Disable all hooks                                                                                                                                                                                                                                                                    | `true`                                                                    |
| `allowManagedHooksOnly`    | (Managed settings only) Prevent loading of user, project, and plugin hooks. Only allows managed hooks and SDK hooks. See [Hook configuration](#38-hook-configuration)                                                                                                               | `true`                                                                    |
| `model`                    | Override the default model to use for Claude Code                                                                                                                                                                                                                                    | `"claude-sonnet-4-5-20250929"`                                            |
| `otelHeadersHelper`        | Script to generate dynamic OpenTelemetry headers. Runs at startup and periodically (see Dynamic headers)                                                                                                                                                                             | `/bin/generate_otel_headers.sh`                                          |
| `statusLine`               | Configure a custom status line to display context. See statusLine documentation                                                                                                                                                                                                      | `{"type": "command", "command": "~/.claude/statusline.sh"}`              |
| `fileSuggestion`           | Configure a custom script for @ file autocomplete. See [File suggestion settings](#37-file-suggestion-settings)                                                                                                                                                                     | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`         |
| `respectGitignore`         | Control whether the @ file picker respects .gitignore patterns. When true (default), files matching .gitignore patterns are excluded from suggestions                                                                                                                                  | `true`                                                                    |
| `systemPrompt`             | Replace the default system prompt with a custom one                                                                                                                                                                                                                                  | `"You are a helpful coding assistant."`                                   |
| `appendSystemPrompt`       | Append text to the default system prompt                                                                                                                                                                                                                                              | `"Always use TypeScript for new code."`                                   |
| `subagents`                | Configure custom subagents. See [Subagent configuration](#312-subagent-configuration)                                                                                                                                                                                               |                                                                         |
| `enabledPlugins`            | List of plugin IDs to enable. See [Plugin configuration](#313-plugin-configuration)                                                                                                                                                                                                  | `["plugin-id-1", "plugin-id-2"]`                                         |
| `extraKnownMarketplaces`   | Additional plugin marketplaces to search. See [Plugin configuration](#313-plugin-configuration)                                                                                                                                                                                      | `["https://custom-marketplace.com"]`                                  |
| `strictKnownMarketplaces`  | (Managed settings only) Restrict plugin installation to only these marketplaces. See [Plugin configuration](#313-plugin-configuration)                                                                                                                                               | `["https://official-marketplace.com"]`                                  |

### 3.4 Permission settings

Permissions control which tools Claude can use and which files it can access. Configure permissions in the `permissions` object:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
```

Permission rules support wildcards and patterns:
- `Bash(npm run *)` - Allow all npm run commands
- `Read(./secrets/**)` - Deny reading any file in secrets directory
- `Write(./src/**/*.ts)` - Allow writing TypeScript files in src

You can also use `/permissions` command or `/allowed-tools` to manage permissions interactively.

**Tool-specific permission rules**: You can configure permissions for specific tools using patterns. For example:
- `Bash(git:*)` - Allow all git commands
- `Bash(curl:*)` - Deny all curl commands
- `Read(./.env*)` - Deny reading any .env files
- `Write(./config/production.json)` - Deny writing to production config

### 3.5 Sandbox settings

Sandbox mode provides filesystem and network isolation for safer, more autonomous execution. Enable it with the `/sandbox` command or configure in settings:

```json
{
  "sandbox": {
    "enabled": true,
    "allowNetwork": false,
    "allowedPaths": ["/tmp", "/home/user/projects"]
  }
}
```

### 3.6 Attribution settings

Customize how Claude Code attributes its work in git commits and pull requests:

```json
{
  "attribution": {
    "commit": "🤖 Generated with Claude Code",
    "pr": "AI-assisted changes"
  }
}
```

- `commit`: Text appended to commit messages
- `pr`: Text added to pull request descriptions

Set to empty string `""` to disable attribution for that type.

### 3.7 File suggestion settings

Configure a custom script for @ file autocomplete:

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

The script should output file paths, one per line, that will be used for autocomplete suggestions.

### 3.8 Hook configuration

Hooks allow you to run custom commands before or after tool executions. Configure hooks in `settings.json`:

```json
{
  "hooks": {
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Validate file write safety."
        }
      ]
    }
  ],
    "PostToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Commit made' >> ~/commits.log"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ],
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verify task completion."
        }
      ]
    }
    ]
  }
}
```

Hook types:
- `PreToolUse`: Runs before a tool executes
- `PostToolUse`: Runs after a tool executes
- `SessionStart`: Runs when a session starts
- `Stop`: Runs when Claude stops

Hook actions:
- `type: "prompt"`: Asks the user a question before proceeding
- `type: "command"`: Executes a shell command

Use `/hooks` command to manage hooks interactively.

### 3.9 Settings precedence

Settings are applied in the following order (later overrides earlier):
1. **Managed** settings (highest priority, cannot be overridden)
2. **Command line arguments** (temporary session overrides)
3. **Local** settings (`.claude/settings.local.json`)
4. **Project** settings (`.claude/settings.json`)
5. **User** settings (`~/.claude/settings.json`)

**Key points about the configuration system:**
- More specific scopes always override less specific ones
- Managed settings cannot be overridden by any other scope
- Command line arguments provide temporary session-level overrides
- Local settings allow personal customization without affecting team members
- Project settings enable team-wide standardization
- User settings provide personal defaults across all projects

### 3.10 System prompt

Customize Claude's behavior by modifying the system prompt:

```json
{
  "systemPrompt": "You are a helpful coding assistant specialized in Python.",
  "appendSystemPrompt": "Always write comprehensive tests for new code."
}
```

- `systemPrompt`: Replaces the entire default system prompt
- `appendSystemPrompt`: Appends to the default system prompt

### 3.11 Excluding sensitive files

Protect sensitive files from being read by Claude:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)"
    ]
  }
}
```

You can also use `.claudeignore` file (similar to `.gitignore`) to exclude files from being read or suggested.

### 3.12 Subagent configuration

Configure custom AI subagents for specialized tasks:

```json
{
  "subagents": {
    "reviewer": {
      "description": "Reviews code for bugs and best practices",
      "systemPrompt": "You are a code reviewer. Focus on security and performance."
    },
    "tester": {
      "description": "Writes and runs tests",
      "systemPrompt": "You are a testing specialist. Write comprehensive tests."
    }
  }
}
```

Use subagents with the `/agents` command or `--agent` CLI flag.

### 3.13 Plugin configuration

Configure plugins in `settings.json`:

```json
{
  "enabledPlugins": ["plugin-id-1", "plugin-id-2"],
  "extraKnownMarketplaces": ["https://custom-marketplace.com"],
  "strictKnownMarketplaces": ["https://official-marketplace.com"]
}
```

- `enabledPlugins`: List of plugin IDs to enable
- `extraKnownMarketplaces`: Additional marketplaces to search for plugins
- `strictKnownMarketplaces`: (Managed only) Restrict installation to only these marketplaces

Use `/plugin` command to manage plugins interactively.

Plugin-specific settings can be stored in:
- `.claude/plugin-name.local.md` (with YAML frontmatter)
- `.claude/plugin-name.local.json`

Example `.local.md` format:

```markdown
---
enabled: true
validation_mode: strict
max_file_size: 1000000
notify_on_errors: true
---

# Plugin Configuration

Your plugin is configured with strict validation mode.
```

**Important:** Add `.claude/*.local.md` and `.claude/*.local.json` to your `.gitignore` to keep these files user-local.

### 3.14 Custom commands

Create reusable slash commands by saving `.md` files in:

- **Project-specific:** `.claude/commands/` (in project root)
- **Personal/global:** `~/.claude/commands/` (in home directory)

The filename becomes the command name (e.g., `fix-tests.md` → `/fix-tests`).

Example `.claude/commands/fix-tests.md`:

```markdown
# Fix Tests

Run the test suite and fix any failing tests.

Focus on:
- Unit tests first
- Integration tests second
- Update test documentation if needed
```

When you type `/fix-tests` in Claude Code, it will execute the instructions in this file.

### 3.15 Environment variables

Claude Code uses environment variables for various purposes:

#### Setting environment variables in settings

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "MY_CUSTOM_VAR": "value"
  }
}
```

#### Using environment variables in MCP configurations

Reference environment variables in MCP server configurations using `${VAR_NAME}` syntax:

```json
{
  "database": {
    "command": "python",
    "args": ["-m", "mcp_server_db"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}",
      "DB_USER": "${DB_USER}",
      "DB_PASSWORD": "${DB_PASSWORD}"
    }
  }
}
```

Set environment variables in your shell:

```bash
export DATABASE_URL="postgresql://localhost/mydb"
export DB_USER="myuser"
export DB_PASSWORD="mypassword"
```

#### Persistent environment with CLAUDE_ENV_FILE

Use `$CLAUDE_ENV_FILE` to persist environment variables across Bash commands. See [Bash tool behavior](#317-bash-tool-behavior) for details.

#### Important environment variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_ENV_FILE` | Path to shell script sourced before each Bash command |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | Set to `1` to reset to project directory after each command |
| `DISABLE_PROMPT_CACHING_OPUS` | Set to `1` to disable prompt caching for Opus models |
| `DISABLE_PROMPT_CACHING_SONNET` | Set to `1` to disable prompt caching for Sonnet models |
| `DISABLE_TELEMETRY` | Set to `1` to opt out of Statsig telemetry (note that Statsig events do not include user data like code, file paths, or bash commands) |
| `HTTP_PROXY` | Specify HTTP proxy server for network connections |
| `HTTPS_PROXY` | Specify HTTPS proxy server for network connections |
| `MAX_MCP_OUTPUT_TOKENS` | Maximum number of tokens allowed in MCP tool responses. Claude Code displays a warning when output exceeds 10,000 tokens (default: 25000) |
| `MAX_THINKING_TOKENS` | Enable [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) and set the token budget for the thinking process. Extended thinking improves performance on complex reasoning and coding tasks but impacts [prompt caching efficiency](https://docs.claude.com/en/docs/build-with-claude/prompt-caching#caching-with-thinking-blocks). Disabled by default. |
| `MCP_TIMEOUT` | Timeout in milliseconds for MCP server startup |
| `MCP_TOOL_TIMEOUT` | Timeout in milliseconds for MCP tool execution |
| `NO_PROXY` | List of domains and IPs to which requests will be directly issued, bypassing proxy |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Maximum number of characters for slash command metadata shown to the [Skill tool](/docs/en/slash-commands#skill-tool) (default: 15000) |
| `USE_BUILTIN_RIPGREP` | Set to `0` to use system-installed rg instead of rg included with Claude Code |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU` | Override region for Claude 3.5 Haiku when using Vertex AI |
| `VERTEX_REGION_CLAUDE_3_7_SONNET` | Override region for Claude 3.7 Sonnet when using Vertex AI |
| `VERTEX_REGION_CLAUDE_4_0_OPUS` | Override region for Claude 4.0 Opus when using Vertex AI |
| `VERTEX_REGION_CLAUDE_4_0_SONNET` | Override region for Claude 4.0 Sonnet when using Vertex AI |
| `VERTEX_REGION_CLAUDE_4_1_OPUS` | Override region for Claude 4.1 Opus when using Vertex AI |

### 3.16 Tools available to Claude

Claude Code has access to a set of powerful tools:

| Tool                | Description                                                                                          | Permission Required |
| ------------------- | ---------------------------------------------------------------------------------------------------- | ------------------- |
| **AskUserQuestion** | Asks the user multiple choice questions to gather information or clarify ambiguity                   | No                  |
| **Bash**            | Executes shell commands in your environment (see [Bash tool behavior](#317-bash-tool-behavior))    | Yes                 |
| **BashOutput**      | Retrieves output from a background bash shell                                                        | No                  |
| **Edit**            | Makes targeted edits to specific files                                                               | Yes                 |
| **ExitPlanMode**    | Prompts the user to exit plan mode and start coding                                                  | Yes                 |
| **Glob**            | Finds files based on pattern matching                                                                | No                  |
| **Grep**            | Searches for patterns in file contents                                                               | No                  |
| **KillShell**       | Kills a running background bash shell by its ID                                                      | No                  |
| **NotebookEdit**    | Modifies Jupyter notebook cells                                                                      | Yes                 |
| **Read**            | Reads the contents of files                                                                          | No                  |
| **Skill**           | Executes a skill or slash command within the main conversation | Yes                 |
| **Task**            | Runs a sub-agent to handle complex, multi-step tasks                                                 | No                  |
| **TodoWrite**       | Creates and manages structured task lists                                                            | No                  |
| **WebFetch**        | Fetches content from a specified URL                                                                 | Yes                 |
| **WebSearch**       | Performs web searches with domain filtering                                                          | Yes                 |
| **Write**           | Creates or overwrites files                                                                          | Yes                 |

Permission rules can be configured using `/allowed-tools` or in permission settings.

### 3.17 Bash tool behavior

The Bash tool executes shell commands with the following persistence behavior:

- **Working directory persists**: When Claude changes the working directory (for example, `cd /path/to/dir`), subsequent Bash commands will execute in that directory. You can use `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` to reset to the project directory after each command.
- **Environment variables do NOT persist**: Environment variables set in one Bash command (for example, `export MY_VAR=value`) are **not** available in subsequent Bash commands. Each Bash command runs in a fresh shell environment.

To make environment variables available in Bash commands, you have **three options**:

**Option 1: Activate environment before starting Claude Code** (simplest approach)

Activate your virtual environment in your terminal before launching Claude Code:

```bash
conda activate myenv
# or: source /path/to/venv/bin/activate
claude
```

This works for shell environments but environment variables set within Claude's Bash commands will not persist between commands.

**Option 2: Set CLAUDE_ENV_FILE before starting Claude Code** (persistent environment setup)

Export the path to a shell script containing your environment setup:

```bash
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

Where `/path/to/env-setup.sh` contains:

```bash
conda activate myenv
# or: source /path/to/venv/bin/activate
# or: export MY_VAR=value
```

Claude Code will source this file before each Bash command, making the environment persistent across all commands.

**Option 3: Use a SessionStart hook** (project-specific configuration)

Configure in `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

The hook writes to `$CLAUDE_ENV_FILE`, which is then sourced before each Bash command. This is ideal for team-shared project configurations.

### 3.18 Extending tools with hooks

You can run custom commands before or after any tool executes using Claude Code hooks. For example, you could automatically run a Python formatter after Claude modifies Python files, or prevent modifications to production configuration files by blocking Write operations to certain paths.

Example: Auto-format Python files after Edit:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(**/*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "black \"$CLAUDE_TOOL_FILE\" && isort \"$CLAUDE_TOOL_FILE\""
          }
        ]
      }
    ]
  }
}
```

Example: Block writes to production config:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write(./config/production.json)",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Are you sure you want to modify production config? This is dangerous!"
          }
        ]
      }
    ]
  }
}
```

See [Hook configuration](#38-hook-configuration) for more details.

## 4 Sessions

Sessions are related to the folder where claude code is running.
When starting claude code in a different folder, sessions in other folders are not known.

### 4.1 Session handling workflow

#### from command line:

| Command | Description |
|---------|-------------|
| `cd /myFolder` | Change to the claude code working folder |
| `claude -r "session-name"` | Resume a session with specific session name |
| `claude -r` | Resume an existing session using the session picker |

#### inside a claude session:

| Command | Description |
|---------|-------------|
| `/resume "session-name"` | Resume a session with specific session name (old session will be stored) |
| `/resume` | Resume an existing session using the session picker |
| `/rename "new-name"` | Rename the existing session |
| `/exit` | Terminate claude and save current session |

---

## 5 MCP Servers

### 5.1 Overview

MCP (Model Context Protocol) servers allow Claude Code to integrate with external tools, databases, APIs, and services. MCP servers can be configured in JSON files to extend Claude Code's capabilities beyond its built-in tools.

Once configured, MCP server tools become available with a specific naming prefix (`mcp__server_name__tool_name`) and can be used just like built-in Claude Code tools.

### 5.2 Server Types

Claude Code supports multiple MCP server transport types:

| Server Type | Description | Use Case |
|-------------|-------------|----------|
| **stdio** | Executes local MCP servers as child processes | Local development tools, custom servers, NPM packages |
| **sse** | Server-Sent Events for hosted services | Cloud platforms with OAuth support |
| **http** | HTTP-based services | RESTful APIs and HTTP endpoints |
| **ws** | WebSocket connections | Real-time bidirectional communication |

### 5.3 Configuration via JSON Files

MCP servers can be configured using `.mcp.json` files (for project scope) or inline in `plugin.json` (for plugins). The configuration uses the `mcpServers` object.

#### 5.3.1 Stdio Server (Local Process)

Execute local processes and NPM packages:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"],
      "env": {
        "LOG_LEVEL": "debug"
      }
    }
  }
}
```

Key points:
- Ideal for custom servers and local tools
- Claude Code manages the process lifecycle
- Communicates via stdin/stdout
- Process terminates when Claude Code exits

#### 5.3.2 SSE Server (Server-Sent Events)

Connect to hosted services with OAuth:

```json
{
  "mcpServers": {
    "asana": {
      "type": "sse",
      "url": "https://mcp.asana.com/sse"
    }
  }
}
```

Key points:
- Automatically handles OAuth flows
- No local installation required
- Token management handled by Claude Code

#### 5.3.3 Server with Environment Variables

Configure servers with custom environment variables:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/custom-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "API_KEY": "${MY_API_KEY}",
        "LOG_LEVEL": "debug",
        "DATABASE_URL": "${DB_URL}"
      }
    }
  }
}
```

Important:
- Use `${CLAUDE_PLUGIN_ROOT}` for portable file paths in plugins
- Reference environment variables using `${VAR_NAME}` syntax
- Environment variables are expanded at runtime

#### 5.3.4 Configuration Locations

MCP server configurations can be stored in different locations based on scope:

| Scope | Location | Description |
|-------|----------|-------------|
| **User** | `~/.claude.json` | Personal servers across all projects |
| **Project** | `.mcp.json` | Team-shared servers (committed to git) |
| **Local** | `~/.claude.json` | Per-project personal servers |
| **Managed** | System directories | Enterprise-deployed servers |

Managed MCP configuration paths:
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux/WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\ProgramData\ClaudeCode\managed-mcp.json`

### 5.4 Using MCP Tools in Commands

Once an MCP server is configured, its tools can be used in custom commands and agents.

#### 5.4.1 Allow MCP Tools in Command Frontmatter

Explicitly list allowed MCP tools in custom command files:

```markdown
---
description: Search and create Asana tasks
allowed-tools: [
  "mcp__plugin_asana_asana__asana_search_tasks",
  "mcp__plugin_asana_asana__asana_create_task"
]
---

# Asana Task Management

## Searching Tasks

To search for tasks:
1. Use mcp__plugin_asana_asana__asana_search_tasks
2. Provide search filters (assignee, project, etc.)
3. Display results to user

## Creating Tasks

To create a task:
1. Gather task details (title, description, project)
2. Use mcp__plugin_asana_asana__asana_create_task
3. Show confirmation with task link
```

#### 5.4.2 Tool Naming Convention

MCP tools follow this naming pattern:
```
mcp__<plugin_name>_<server_name>__<tool_name>
```

Examples:
- `mcp__plugin_asana_asana__asana_create_task`
- `mcp__plugin_api_server__read_data`
- `mcp__plugin_api_server__create_item`

#### 5.4.3 Security Best Practices

- **Scope allowed tools**: Only list necessary MCP tools in `allowed-tools`
- **Avoid wildcards**: Don't use wildcard permissions for MCP tools
- **Document requirements**: Clearly document required environment variables in README
- **Test integration**: Use `/mcp` command to test MCP server connections
- **Handle authentication**: Properly configure OAuth or token-based authentication

#### 5.4.4 Testing MCP Integration

Use the `/mcp` command to:
- View configured MCP servers
- Test server connections
- Manage OAuth authentication
- Clear authentication tokens
- Verify tool availability

**Note:** For CLI-based MCP server management (using `claude mcp add`, `claude mcp list`, etc.), refer to the official documentation at https://code.claude.com/docs/en/mcp.md
