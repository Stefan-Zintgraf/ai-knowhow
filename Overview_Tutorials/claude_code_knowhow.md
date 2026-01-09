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
| `/help` | Show available commands and options |
| `/clear` | Clear conversation history |
| `/commit` | Create git commits (analyzes diff and generates Conventional Commit messages) |
| `/compact` | Compress context to save tokens |
| `/context` | View current context usage and token limits |
| `/memory` | Edit CLAUDE.md file for persistent session memory |
| `/agents` | Manage agents for specialized tasks |
| `/review` | Perform code review on files or changes |
| `/permissions` | Manage tool permissions and security |
| `/cost` | Show token usage and costs<br>(not available for Claude Max/Pro subscribers - it only works when using Claude Code with the API (pay-per-token) |
| `/status` | View current session status |

**Custom slash commands:** Create reusable commands by saving `.md` files in `.claude/commands/` (project) or `~/.claude/commands/` (personal). The filename becomes the command (e.g., `fix-tests.md` → `/fix-tests`).

