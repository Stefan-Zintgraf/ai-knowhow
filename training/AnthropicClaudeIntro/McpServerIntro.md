---
marp: true
theme: default
size: 16:9
paginate: true
title: "Introduction to MCP Servers"
description: "Model Context Protocol — tools, flow, and GitLab examples"
style: |
  section {
    font-size: 22px;
    padding: 12px 40px 32px 40px;
    justify-content: flex-start;
  }
  section.lead {
    justify-content: center;
    font-size: 24px;
  }
  section.lead h1 { margin-top: 0; }
  h1 { font-size: 1.4em; margin: 0 0 0.3em; line-height: 1.2; }
  h2 { font-size: 1.2em; margin: 0.05em 0 0.3em; line-height: 1.2; }
  h3 { font-size: 1.02em; margin: 0.1em 0 0.25em; }
  p { margin: 0.2em 0; line-height: 1.32; }
  ul, ol { margin: 0.15em 0; }
  li { margin: 0.08em 0; line-height: 1.3; }
  table { font-size: 0.82em; width: 100%; margin: 0.2em 0; }
  th, td { padding: 0.2em 0.35em; line-height: 1.3; }
  pre { font-size: 0.98em; line-height: 1.4; margin: 0.25em 0; }
  code { font-size: 1em; }
  blockquote { margin: 0.3em 0; padding: 0.35em 0.6em; font-size: 0.88em; }
  img { max-height: 42vh; }
  section.diagram-slide img {
    max-height: 54vh;
    max-width: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
  }
  section.diagram-flow h2 {
    margin: 0 0 0.12em 0;
  }
  section.diagram-flow > p {
    margin: 0.04em 0 0.1em 0;
    font-size: 0.9em;
    line-height: 1.28;
  }
  section.diagram-flow img {
    max-height: 64vh;
    display: block;
    margin-left: auto;
    margin-right: auto;
  }
  section.flow-wide img {
    width: 100%;
    max-width: 100%;
    max-height: none;
    height: auto;
    display: block;
    margin: 0.6em auto;
  }
---

<!-- _class: lead -->
# Introduction to MCP Servers

## Table of Contents

1. [What is MCP?](#1-what-is-mcp)
2. [How a Tool Call Flows Through MCP](#2-how-a-tool-call-flows-through-mcp)
3. [Example: a minimal tool in Python (FastMCP)](#3-example-a-minimal-tool-in-python-fastmcp)
4. [Installing an MCP Server in Claude Desktop](#4-installing-an-mcp-server-in-claude-desktop)
5. [Two GitLab Use Cases](#5-two-gitlab-use-cases)

---

## 1. What is MCP?

- **MCP** = **Model Context Protocol**
- Open standard, originally from Anthropic
- Uniform way for LLM apps (Claude Desktop, Cursor, VS Code, …) to talk to external tools
- Analogy: a *USB port for AI assistants* — every tool plugs into the same socket

**An MCP server is:**

- A small program that exposes a set of tools the LLM can use
- Typical examples:
  - **Filesystem** — read/write files on your disk
  - **GitLab / GitHub** — list merge requests, comment on issues, inspect pipelines
  - **Database** — run read-only SQL queries

**Why it matters:**

- Without MCP → copy-paste everything into the chat
- With MCP → the LLM calls tools on demand, like a developer calling an API

<!-- _class: diagram-slide diagram-flow flow-wide -->
## 1. (continued) — three actors

**The three actors:**

![MCP host, client, server, and external system](./images/mcp_three_actors.png)


---

<!-- _class: diagram-slide diagram-flow -->
## 2. How a Tool Call Flows Through MCP

![MCP tool call: host mediates between LLM, MCP server, and external API](./images/mcp_tool_call_flow.png)


---

## 2. (continued) — takeaways

**Key takeaways:**

- The **LLM never talks to GitLab directly**
  - It only *decides* which tool to call
  - The host executes the call and feeds the result back
- **Tool calls become part of the conversation history**
  - The LLM can chain them: *list MRs → pick one → fetch diff → summarize*

---

## 3. Example: a minimal tool in Python (FastMCP)

The **MCP Python SDK** ships **FastMCP** — you implement a **normal Python function**; the SDK exposes it as a **tool** (name, description, parameters) to the host.

- **Input:** the function’s **parameters** and their type hints; the function **docstring** is the **tool description** the LLM sees.
- **Output:** the **return value** (e.g. a `dict`) is sent back as the tool result — there is no separate “out parameter” in the schema.

**Dependency:** `pip install "mcp[cli]"` (or `uv add "mcp[cli]"`).

---

## 3. (continued) — `greeting_server.py`

```python
"""MCP server exposing one tool: format_greeting (stdio for Claude Desktop / Cursor)."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Greeting", json_response=True)


@mcp.tool()
def format_greeting(name: str) -> dict:
    """Return a one-line greeting for a person.

    Use when the user wants a short, personalized hello and nothing more.
    """
    n = (name or "").strip()
    if not n:
        raise ValueError("name must be non-empty")
    return {"greeting": f"Hello, {n}!"}


if __name__ == "__main__":
    mcp.run()  # stdio — what most local clients use
```

- `json_response=True` — structured return values (e.g. a dict) are passed cleanly to the client.
- The LLM only sees what you declare: **function name** → tool name, **docstring** → description, **parameters** → JSON Schema for arguments.

---

## 3. (continued) — register in Claude Desktop

Point **`command`** at the same Python interpreter you used to install `mcp` (or use `uv run` / a venv). Adjust the path to your `greeting_server.py`.

```json
{
  "mcpServers": {
    "greeting": {
      "command": "python",
      "args": ["C:/path/to/greeting_server.py"]
    }
  }
}
```

Restart Claude Desktop, then use the `greeting` server like any other MCP: the model can call the **`format_greeting`** tool with a `name` argument and receive `{"greeting": "…"}` in the tool result.

---

<!-- _class: diagram-slide flow-wide -->
## 4. Installing an MCP Server in Claude Desktop

**Steps:**

![Install MCP server: Settings -> mcp.json -> save -> restart -> running](./images/mcp_install_claude_desktop.png)


- Config file location on Windows: `%APPDATA%\Claude\mcp.json`
- Prerequisite: **Node.js 18+** on your `PATH`

---

## 4. (continued) — minimal `mcp.json`

**Minimal config for the `zereight` GitLab server:**

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "npx",
      "args": ["-y", "@zereight/mcp-gitlab"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "glpat-xxxxxxxxxxxxxxxx",
        "GITLAB_API_URL": "https://gitlab.com/api/v4",
        "GITLAB_READ_ONLY_MODE": "true"
      }
    }
  }
}
```

**Notes on each setting:**

- **Personal access token**
  - Create in GitLab under *Preferences → Access Tokens*
  - Scope `read_api` → enough for read-only use
  - Scope `api` → only if Claude should comment, merge, or edit
- **API URL**
  - Default: `https://gitlab.com/api/v4`
  - Self-hosted: `https://gitlab.your-company.com/api/v4`
- **Read-only mode**
  - Start with `GITLAB_READ_ONLY_MODE=true`
  - You can still list and inspect everything
  - Claude cannot accidentally close issues or merge MRs

---

## 4. (continued) — troubleshooting

**Troubleshooting — if the server is not "running" after restart, use *View Logs*. Typical causes:**

- Node.js missing or wrong version
- Wrong / expired token
- Blocked network / proxy

---

## 5. Two GitLab Use Cases

- Prompts below can be pasted directly into Claude Desktop
- Prerequisite: the `gitlab` MCP server is running

### 5.1 Triage — "What's on my plate today?"

**Scenario:**

- Monday morning
- Goal: know what is waiting for you in GitLab — without clicking through five tabs

**Prompt:**

> *"Use the gitlab MCP server to list all merge requests assigned to me that are still open, grouped by project, and summarize any blocking review comments. Also list my open issues that have a due date in the next 7 days."*

<!-- _class: diagram-slide flow-wide -->
### 5.1 (continued) — what Claude does

**What Claude does:**

![GitLab triage: prompt -> list MRs -> notes -> issues -> summary](./images/mcp_gitlab_triage.png)

---

### 5.2 Investigate a Failing Pipeline

**Scenario:**

- Nightly build on `main` failed
- Goal: know *why* — fast

**Prompt:**

> *"In project ec-embedded, get the latest pipeline on branch `main`. If it failed, tell me which jobs failed, fetch their logs, and explain the most likely root cause in plain English."*

<!-- _class: diagram-slide flow-wide -->

**What Claude does:**

![Failing pipeline: prompt -> list pipelines -> jobs -> logs -> root cause](./images/mcp_gitlab_pipeline.png)


- Saves a lot of scrolling through noisy CMake / CTest output

