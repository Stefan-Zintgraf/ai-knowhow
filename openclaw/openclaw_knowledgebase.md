# OpenClaw knowledge base

## Contents

1. [User systemd services: locations and lifecycle](#user-systemd-services-locations-and-lifecycle)
2. [Gateway service startup and lingering](#gateway-service-startup-and-lingering)
   - [OpenClaw gateway service via CLI](#openclaw-gateway-service-via-cli)
   - [Gateway install / uninstall behind the scenes (Linux systemd)](#gateway-install--uninstall-behind-the-scenes-linux-systemd)
   - [Repo script: `mele/user.systemd/openclaw_service.sh` (prep service, gateway drop-in, shell env)](#repo-script-meleusersystemdopenclaw_servicesh-prep-service-gateway-drop-in-shell-env)
3. [Gateway clients: concept, API, and use cases](#gateway-clients-concept-api-and-use-cases)
   - [What is a gateway client?](#what-is-a-gateway-client)
   - [Gateway WebSocket protocol](#gateway-websocket-protocol)
   - [Available RPC methods](#available-rpc-methods)
   - [Use cases beyond WebClaw](#use-cases-beyond-webclaw)
   - [3.1 WebClaw](#31-webclaw)
4. [Skills](#skills)
   - [`backup` — password-protected config backup](#backup--password-protected-config-backup)
   - [`greet` — friendly greeting](#greet--friendly-greeting)
   - [`testnode-skill` — control the Testnode from chat](#testnode-skill--control-the-testnode-from-chat)
5. [Nodes](#nodes)
   - [`testnode` — Python echo node example](#testnode--python-echo-node-example)
6. [Plugins](#plugins)
   - [`hello` — minimal slash-command example](#hello--minimal-slash-command-example)
   - [`testnode` — slash-command wrapper for the Testnode](#testnode--slash-command-wrapper-for-the-testnode)
7. [ACP clients: IDE and tool integration via the ACP bridge](#acp-clients-ide-and-tool-integration-via-the-acp-bridge)
   - [What is an ACP client?](#what-is-an-acp-client)
   - [How the ACP bridge works](#how-the-acp-bridge-works)
   - [Use cases](#use-cases)
   - [Session mapping](#session-mapping)
   - [Zed editor setup](#zed-editor-setup)
   - [Which editors and tools support ACP?](#which-editors-and-tools-support-acp)
   - [ACP client vs. gateway client](#acp-client-vs-gateway-client)
8. [OpenAI Chat Completions HTTP API](#openai-chat-completions-http-api)
   - [What is the Chat Completions endpoint?](#what-is-the-chat-completions-endpoint)
   - [Enabling the endpoint](#enabling-the-chat-completions-endpoint)
   - [Compatible tools](#compatible-tools)
   - [Connecting Cursor to OpenClaw via Chat Completions](#connecting-cursor-to-openclaw-via-chat-completions)
9. [OpenResponses HTTP API](#openresponses-http-api)
   - [What is the OpenResponses endpoint?](#what-is-the-openresponses-endpoint)
   - [Enabling the endpoint](#enabling-the-openresponses-endpoint)
   - [Connecting Cursor to OpenClaw via OpenResponses](#connecting-cursor-to-openclaw-via-openresponses)
   - [CLI backends: Claude Code, Gemini CLI, Codex CLI](#cli-backends-claude-code-gemini-cli-codex-cli)
   - [Chat Completions vs. OpenResponses](#chat-completions-vs-openresponses)

---

## 1. User systemd services: locations and lifecycle

**Filesystem:** User units live under `~/.config/systemd/user/` (primary); other search paths are `~/.local/share/systemd/user/` and `/etc/systemd/user/`. When you **enable** a unit (e.g. `systemctl --user enable openclaw-gateway.service`), systemd creates symlinks in a `*.target.wants/` directory (e.g. `~/.config/systemd/user/default.target.wants/openclaw-gateway.service` → `../openclaw-gateway.service`). Those symlinks define which services start with the target (e.g. default.target). **Disable** removes the symlinks; **start** / **stop** / **restart** affect the current run state only. Commands: `systemctl --user enable|disable|start|stop|restart|status <unit>`.

## 2. Gateway service startup and lingering

The OpenClaw gateway can run as a **user** systemd service (unit under `~/.config/systemd/user/openclaw-gateway.service`). 
User systemd normally runs only when the user is logged in, so the service stops when you log out. 
To have the gateway start at boot and keep running without any login session, enable **lingering** for that user:
 `loginctl enable-linger <username>` (run as root). 
 Then the user's systemd instance starts at boot and user services like the gateway run as that user even with no active session. 
 Check with `loginctl show-user <username> --property=Linger` (Linger=yes means enabled). 
 The service must be enabled: `systemctl --user enable openclaw-gateway.service`.

### OpenClaw gateway service via CLI

Use the OpenClaw CLI to manage the gateway service regardless of OS (launchd on macOS, systemd on Linux, schtasks on Windows). Commands: `openclaw gateway status` (show status and optionally probe the gateway), `openclaw gateway install` (install and enable the service), `openclaw gateway uninstall`, `openclaw gateway start`, `openclaw gateway stop`, `openclaw gateway restart`. On Linux the service name is `openclaw-gateway.service` (or `openclaw-gateway-<profile>.service` for a named profile); the CLI invokes `systemctl --user` under the hood.

### Gateway install / uninstall behind the scenes (Linux systemd)

**`openclaw gateway install`** (on Linux): (1) Creates `~/.config/systemd/user/` if missing. (2) Writes the unit file `~/.config/systemd/user/openclaw-gateway[-<profile>].service` with `[Unit]`, `[Service]` (ExecStart, env, Restart, etc.), and `[Install] WantedBy=default.target`. (3) Runs `systemctl --user daemon-reload`. (4) Runs `systemctl --user enable <unit>` — **systemd** then creates the symlink `~/.config/systemd/user/default.target.wants/openclaw-gateway[-<profile>].service` → `../openclaw-gateway[-<profile>].service`. (5) Runs `systemctl --user restart <unit>` so the service starts. Install does not enable lingering; use `loginctl enable-linger <user>` separately (or `openclaw doctor` can prompt for it).

**`openclaw gateway uninstall`** (on Linux): (1) Runs `systemctl --user disable --now <unit>` — stops the service and removes the symlink from `default.target.wants/`. (2) Deletes the unit file `~/.config/systemd/user/openclaw-gateway[-<profile>].service`. The user's systemd config dir and lingering are left unchanged.

### Repo script: `mele/user.systemd/openclaw_service.sh` (prep service, gateway drop-in, shell env)

This repo script is intended for use **alongside** the OpenClaw CLI–installed gateway unit. It does not replace the gateway unit; it adds a **prep** service, a **drop-in** so the gateway uses the repo state dir and `.env`, and **shell env + completions** so the CLI and gateway use the same config.

**Install (`--install` or `-i`, optionally `--force` / `-f` to overwrite):**

1. **Gateway already running** — If `openclaw-gateway.service` is active, the script stops and disables it so the drop-in is applied on re-start.
2. **Prep service** — Writes and enables `~/.config/systemd/user/openclaw-gateway-prep.service` (Type=oneshot): runs Tailscale funnel and rebind before the gateway. The unit has `Before=openclaw-gateway.service` so it starts first when both are in `default.target`.
3. **Gateway drop-in** — Creates `~/.config/systemd/user/openclaw-gateway.service.d/10-state-env.conf` with:
   - **EnvironmentFile** = `mele/user.openclaw/.env` (absolute path derived from script location).
   - **Environment=OPENCLAW_STATE_DIR** = absolute path to `mele/user.openclaw`.
   So the CLI-installed gateway unit keeps running but loads the repo `.env` and state dir instead of `~/.openclaw`.
4. **systemctl** — `daemon-reload`, enable prep service. If the gateway was running in step 1, re-enables and starts it so it picks up the new environment.
5. **Lingering** — Ensures user lingering is enabled so user services run without login.
6. **Shell env for CLI** — So `openclaw` commands and completions use the same state dir:
   - Creates **`~/.config/openclaw/state-dir.sh`** with `export OPENCLAW_STATE_DIR="<absolute path to mele/user.openclaw>"`.
   - Updates **`~/.profile`** (or `~/.bash_profile`), **`~/.bashrc`**, and **`~/.zshrc`**:
     - Removes any existing lines that set `OPENCLAW_STATE_DIR=`, source `openclaw/state-dir.sh`, or source **completion** scripts (e.g. `~/.openclaw/completions/openclaw.bash`).
     - Appends a block that sources `state-dir.sh` and a **conditional completion** line: only sources `$OPENCLAW_STATE_DIR/completions/openclaw.bash` when that file exists, avoiding "No such file or directory" when the CLI had previously pointed completions at `~/.openclaw`.

**Uninstall (`--uninstall` or `-u`):**

1. **Prep service** — `systemctl --user disable --now openclaw-gateway-prep.service`, then delete the prep unit file.
2. **Drop-in** — Remove `openclaw-gateway.service.d/10-state-env.conf` (and remove the drop-in directory if empty).
3. **Shell env** — Remove `~/.config/openclaw/state-dir.sh` and remove the state-dir and completion lines from `~/.profile`, `~/.bash_profile`, `~/.bashrc`, and `~/.zshrc`.
4. **daemon-reload** — So systemd forgets the prep unit and drop-in.

**Status (`--status` or `-s`):** Runs `systemctl --user status openclaw-gateway-prep.service`.

**Environment variables (summary):**

- **OPENCLAW_STATE_DIR** — Set by the gateway drop-in for the gateway process and by `state-dir.sh` for the CLI. Points to `mele/user.openclaw` (config dir: `openclaw.json`, `.env`, plugins under `examples/plugins/`, etc.). Path is derived at install time from the script's directory.


## 3. Gateway clients: concept, API, and use cases

### What is a gateway client?

The OpenClaw gateway is the central hub: it manages sessions, routes messages, and runs the AI agent (node). Any external process that connects to it is a **gateway client**. There are two distinct roles a client can declare during the connection handshake:

- **`operator`** — a controller/UI that sends messages, manages sessions, and reads results. WebClaw, the CLI, the macOS app, and Telegram bot adapters are all operators.
- **`node`** — a worker that the gateway routes AI tasks to (e.g. the Claude agent process). Nodes are not discussed here.

WebClaw is an **operator client with `operator.admin` scope** — the highest level of access. It identifies itself as `mode: "ui"` in the handshake. Any program that speaks the gateway WebSocket protocol can be an operator client; it does not have to be a web UI.

**Official documentation:**
- Gateway protocol overview: `https://docs.openclaw.ai/gateway/protocol`
- Architecture (operator vs. node): `https://docs.openclaw.ai/concepts/architecture`
- Web clients (WebClaw, WebChat): `https://docs.openclaw.ai/web`
- HTTP Tools Invoke API (alternative to WebSocket): `https://docs.openclaw.ai/gateway/tools-invoke-http-api`
- OpenResponses-compatible HTTP API: `https://docs.openclaw.ai/gateway/openresponses-http-api`

### Gateway WebSocket protocol

The gateway uses a WebSocket connection as its single control plane. All messages are JSON text frames. Three frame types exist:

- **Request:** `{ type: "req", id: "<uuid>", method: "<name>", params: { ... } }`
- **Response:** `{ type: "res", id: "<uuid>", ok: true|false, payload: { ... } }` (or `error`)
- **Event:** `{ type: "event", event: "<name>", payload: { ... }, seq?: number }`

**Connection handshake** (must be the first request after the WebSocket opens):

```json
{
  "type": "req",
  "id": "<uuid>",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "my-client",
      "displayName": "my-client",
      "version": "1.0",
      "platform": "linux",
      "mode": "ui"
    },
    "auth": { "token": "<OPENCLAW_GATEWAY_TOKEN>" },
    "role": "operator",
    "scopes": ["operator.admin"]
  }
}
```

Authentication: use `auth.token` (recommended, matches `OPENCLAW_GATEWAY_TOKEN`) or `auth.password`. Side-effecting calls should include an `idempotencyKey` (a UUID) so they are safe to retry.

### Available RPC methods

These are the methods an operator client can call (derived from WebClaw's source code and official docs):

**Sessions**

| Method | Key params | What it does |
|--------|-----------|-------------|
| `sessions.list` | `limit`, `includeLastMessage`, `includeDerivedTitles` | List all sessions with metadata |
| `sessions.patch` | `key`, `label` | Create a new session or rename an existing one |
| `sessions.resolve` | `key`, `includeUnknown`, `includeGlobal` | Resolve a friendly session name to its internal key |
| `sessions.delete` | `key` | Delete a session and its history |

**Chat**

| Method | Key params | What it does |
|--------|-----------|-------------|
| `chat.send` | `sessionKey`, `message`, `attachments`, `idempotencyKey`, `deliver`, `timeoutMs` | Send a user message; triggers the AI agent to respond |
| `chat.history` | `sessionKey`, `limit` | Retrieve message history for a session |
| `chat.subscribe` | `sessionKey` or `friendlyId` | Subscribe to real-time push events (streaming response tokens, status changes) |

**Infrastructure**

| Method | What it does |
|--------|-------------|
| `connect` | Authenticate and declare role/scope (must be first call) |

After calling `chat.subscribe` the gateway pushes `event` frames for every token or status change in that session — this is how streaming responses work.

### Use cases beyond WebClaw

Any program that implements the connect handshake and calls the methods above is a fully functional gateway client. Here are ten concrete use cases:

1. **CLI / terminal chat client** — A shell script or small program that sends a message and prints the streaming response. Useful for piping command output into the agent: `some-command | my-client send --session main`.

2. **Notification / alerting bot** — A daemon that subscribes to `chat.subscribe` events and forwards them to Slack, email, or a webhook when the agent finishes a task or reports an error. No human in the loop.

3. **Scheduled / automated message sender** — A cron job that sends a message on a schedule ("every morning, summarize yesterday's emails") and stores or forwards the response. Uses only `chat.send` + `chat.history`.

4. **Multi-channel relay** — The Telegram bot in this repo is already an example: it translates between the Telegram API and the gateway. The same pattern works for WhatsApp, Discord, SMS (Twilio), Slack, Teams, etc. Each channel becomes a thin adapter on top of the same gateway calls.

5. **IDE / editor plugin** — A plugin for VS Code, Neovim, or JetBrains that sends selected code plus a question to the agent and inserts the response inline. Cursor itself is a close analogy.

6. **Headless test runner / CI integration** — A client that sends predefined prompts to the agent in CI, collects responses, and asserts on them — useful for regression-testing agent behavior or skills.

7. **Voice interface** — A client that converts speech to text, sends it via `chat.send`, receives the text response, and converts it back to speech. The gateway only sees plain text messages.

8. **Session archiver / logger** — A client that periodically calls `sessions.list` + `chat.history` and writes everything to a database or file for audit logs, search indexing, or analytics.

9. **Multi-agent orchestrator** — A client that manages multiple sessions in parallel — e.g. sends the same question to different agent configurations (different skills/tools enabled) and compares or merges the results.

10. **LLM framework adapter (LangChain, Claude Desktop, Cursor)** — Connect LangChain, Claude Desktop, or Cursor to OpenClaw via the gateway client protocol or the OpenResponses-compatible HTTP endpoint (`http://localhost:18789/v1/responses`). The gateway becomes just another LLM backend those frameworks can call. (See also `todo.md`: "acp client: man kann cursor, claude code dranhaengen".)

**The pattern is always the same:**

```
[your client]  --WebSocket-->  [OpenClaw gateway]  -->  [AI agent / node]
```

A minimal client only needs ~50 lines of code: open a WebSocket, send `connect`, then call whichever methods are needed. See `mele/user.webclaw/apps/webclaw/src/server/gateway.ts` for a complete, production-ready TypeScript reference implementation.


### 3.1 WebClaw

WebClaw is the official web client for OpenClaw. It is a fast, browser-based chat UI that connects to the OpenClaw gateway over WebSocket and lets you chat with the AI agent, manage sessions, and view streaming responses in real time. It is built with React, TanStack Router, and Tailwind CSS and is currently in beta. The source is at [webclaw.dev](https://webclaw.dev).

WebClaw is a **gateway operator client** (see [chapter 3](#gateway-clients-concept-api-and-use-cases)): it authenticates with `operator.admin` scope and drives all gateway features — session list, chat history, message delivery, and streaming token events — through the standard WebSocket protocol. It is the reference implementation for how to build a gateway client in TypeScript (see `apps/webclaw/src/server/gateway.ts`).

- Download into specific folder:
  npx webclaw init ./user.webclaw

- **Run WebClaw as a user service (like the gateway):** Use **`mele/user.systemd/webclaw_service.sh`** to install a systemd user unit so WebClaw starts after the OpenClaw gateway. See [WebClaw as user service](#webclaw-as-user-service) below.

- credentials:
  CLAWDBOT_GATEWAY_URL: ws://127.0.0.1:18789
  CLAWDBOT_GATEWAY_TOKEN: see OPENCLAW_GATEWAY_TOKEN in openclaw's .env 

- Put them in **`apps/webclaw/.env.local`** (or the server will try that path and `./.env.local` from the process cwd).
- Restart the dev server after changing env; refresh the browser.

- Install
  cd user.webclaw
  pnpm install
  pnpm dev

- If "no connection" persists: ensure the OpenClaw gateway is running (`openclaw gateway status`). You can also run dev with env in the shell: `CLAWDBOT_GATEWAY_TOKEN=<token> pnpm dev` (from repo root or from `apps/webclaw`).

- **Browser shows "page didn't load" / net::ERR_CONNECTION_REFUSED:** The dev server is not running or not reachable. (1) **Start the server first:** in a terminal, `cd user.webclaw && pnpm dev`; wait until Vite prints "ready" and the Local/Network URLs. (2) **Then** open in the browser the **exact** URL Vite shows (e.g. `http://localhost:3000/` or `http://127.0.0.1:3000/`). (3) If the browser is on a **different machine** than where you ran `pnpm dev`, use the **Network** URL Vite prints (e.g. `http://192.168.x.x:3000/`), not localhost. (4) Keep the terminal where `pnpm dev` runs open; closing it stops the server. Dev script uses `--host` so both local and network URLs work.

- **Diagnosing connection issues:** In Chrome, press **F12** → open the **Network** tab, then (re)load the page. Check the first request (the document to `localhost` or `127.0.0.1:3000`): a failed status (e.g. `(failed) net::ERR_CONNECTION_REFUSED`) means the dev server isn't reachable; a successful document plus failed `/api/ping` points to gateway/credentials.

- **One-liner with token (and clean install):** To start the dev server with the gateway token in the environment: `CLAWDBOT_GATEWAY_TOKEN=<your_token> pnpm dev` (run from `user.webclaw`; or from repo root: `pnpm -C apps/webclaw exec -- env CLAWDBOT_GATEWAY_TOKEN=<your_token> pnpm dev`). For a **new, clean installation** create **`apps/webclaw/.env.local`** with at least `CLAWDBOT_GATEWAY_URL=ws://127.0.0.1:18789` and `CLAWDBOT_GATEWAY_TOKEN=<same value as OPENCLAW_GATEWAY_TOKEN in mele/user.openclaw/.env>`; copy the token from `mele/user.openclaw/.env` (variable `OPENCLAW_GATEWAY_TOKEN`). No other files need changing for a minimal setup.

#### WebClaw as user service

Repo script: `mele/user.systemd/webclaw_service.sh` (started after openclaw gateway)

This script installs the **WebClaw** app as a **user** systemd service, in the same way the OpenClaw gateway runs as a user service. WebClaw is configured to start **after** the OpenClaw gateway is up (`After=openclaw-gateway.service`, `Wants=openclaw-gateway.service`), so the gateway is running before the WebClaw dev server tries to connect.

**Prerequisites:**

- OpenClaw gateway installed and enabled (`openclaw gateway install`; or use `openclaw_service.sh --install` for repo state dir and drop-in).
- User lingering enabled (so user services run without login; `openclaw_service.sh --install` enables it).
- **`mele/user.webclaw/apps/webclaw/.env.local`** exists with `CLAWDBOT_GATEWAY_URL=ws://127.0.0.1:18789` and `CLAWDBOT_GATEWAY_TOKEN=<same as OPENCLAW_GATEWAY_TOKEN in mele/user.openclaw/.env>`.

**Install (`--install` or `-i`, optionally `--force` / `-f` to overwrite):**

1. From the repo (e.g. from `mele/user.systemd`): run `./webclaw_service.sh --install`.
2. The script writes **`~/.config/systemd/user/openclaw-webclaw.service`** with:
   - **After=openclaw-gateway.service**, **Wants=openclaw-gateway.service** — starts only after the gateway is up.
   - **WorkingDirectory** = absolute path to `mele/user.webclaw`.
   - **EnvironmentFile** = `mele/user.webclaw/apps/webclaw/.env.local` (optional; if missing, the app still loads it from disk).
   - **ExecStart** = `pnpm dev` in that directory (run via a login shell so `pnpm`/node from your profile are in PATH).
   - **Restart=on-failure**, **RestartSec=5**.
3. Runs **systemctl --user daemon-reload** and **systemctl --user enable openclaw-webclaw.service**.
4. To start immediately: **systemctl --user start openclaw-webclaw.service**. It will also start at next login (or at boot if lingering is enabled).

**Uninstall (`--uninstall` or `-u`):**

1. **systemctl --user disable --now openclaw-webclaw.service**.
2. Remove **`~/.config/systemd/user/openclaw-webclaw.service`**.
3. **systemctl --user daemon-reload**.

**Status (`--status` or `-s`):** Runs **systemctl --user status openclaw-webclaw.service**.

**Useful commands (same pattern as gateway):**

- **systemctl --user start openclaw-webclaw.service** — start WebClaw.
- **systemctl --user stop openclaw-webclaw.service** — stop WebClaw.
- **systemctl --user restart openclaw-webclaw.service** — restart WebClaw.
- **journalctl --user -u openclaw-webclaw.service -f** — follow WebClaw logs.

After starting, open the URL Vite prints (e.g. **http://localhost:3000/** or the Network URL) in your browser.


## 4. Skills

Skills are markdown instruction files (`SKILL.md`) that teach the AI agent how to respond to specific chat triggers or slash commands. They live in the workspace and are loaded by the agent at session start. Each skill has a YAML front-matter block (`name`, `description`, `user-invocable`) followed by plain-language instructions.

**Location:** `mele/user.openclaw/workspace-wolfgang/skills/<skill-name>/SKILL.md`

### `backup` — password-protected config backup

**File:** `mele/user.openclaw/workspace-wolfgang/skills/backup/SKILL.md`

Triggered by `/backup <password>`. Calls `backup.sh -cred -n=wolfgang -v -pw=<password>` via the gateway `exec` tool and reports the output zip path. Requires a password argument; refuses to run without one (the script would hang waiting for stdin).

### `greet` — friendly greeting

**File:** `mele/user.openclaw/workspace-wolfgang/skills/greet/SKILL.md`

Activated when the user sends any greeting phrase ("hello", "hi", "hey", "good morning", etc.). Responds with a time-of-day-aware greeting (morning / afternoon / evening / night owl) and offers to help. No external tools needed — pure conversational skill.

### `testnode-skill` — control the Testnode from chat

**File:** `mele/user.openclaw/workspace-wolfgang/skills/testnode-skill/SKILL.md`

Triggered by messages starting with `testnode` or `test node` (without a leading `/`). Manages the Testnode Python process via the `exec` tool:

- `testnode on|start` — starts the node if not already running.
- `testnode off|stop` — stops the node.
- `testnode restart` — hard-restarts the node.
- `testnode <text>` — ensures the node is running, reads `identity.json` to get the device ID, then calls `nodes.invoke` with `testnode.echo` and the provided text.


## 5. Nodes

Nodes are external worker processes that connect to the gateway with the `node` role. The gateway routes AI tool invocations to them. A node registers one or more named commands; the gateway calls those commands when the AI agent (or a plugin) invokes them. Nodes authenticate with the gateway token and use a persistent `identity.json` to keep a stable device ID across restarts.

**Location:** `mele/user.openclaw/examples/nodes/<node-name>/`

### `testnode` — Python echo node example

**Files:** `mele/user.openclaw/examples/nodes/testnode/testnode.py`, `start.sh`, `stop.sh`, `requirements.txt`, `identity.json`

A minimal Python node that demonstrates the full node lifecycle: WebSocket connection to the gateway, Ed25519 key-pair identity, registration of a single command (`testnode.echo`), and replying to invoke requests with a greeting. Reads `OPENCLAW_GATEWAY_TOKEN` (and host/port overrides) from `.env` next to the script. Local connections are auto-approved by the gateway, so no manual pairing is needed.

**Setup:**
```bash
cd mele/user.openclaw/examples/nodes/testnode
bash venv_install.sh        # creates .venv and installs requirements
bash start.sh               # starts testnode.py in background, writes .testnode.pid
```

**Invoke from CLI:**
```bash
openclaw nodes invoke --node <nodeId> --command testnode.echo --params '{"text":"world"}'
```

The `nodeId` is read from `identity.json` (`deviceId` field) after the node has connected at least once.


## 6. Plugins

Plugins are Node.js ES-module packages loaded by the gateway at startup. Each plugin directory must contain an `openclaw.plugin.json` manifest and an `index.js` entry point that exports a default function receiving an `api` object. Plugins register slash commands via `api.registerCommand(...)`. When a user types `/commandname [args]`, the gateway calls the plugin's handler with a `ctx` object (`ctx.args` contains the argument string).

**Location:** `mele/user.openclaw/examples/plugins/<plugin-name>/`

The plugins directory is referenced by `OPENCLAW_STATE_DIR` — the gateway loads plugins from `$OPENCLAW_STATE_DIR/examples/plugins/` (or wherever `openclaw.json` points).

### `hello` — minimal slash-command example

**Files:** `mele/user.openclaw/examples/plugins/hello/index.js`, `hello.sh`, `openclaw.plugin.json`

Registers `/hello [text]`. The handler calls `hello.sh` (a two-line bash script) with the optional argument and returns the shell output as a chat message. Demonstrates the simplest possible plugin pattern: register a command, run a script, return text. The bash script echoes `"hello world from hello.sh"` (with the received text if provided).

### `testnode` — slash-command wrapper for the Testnode

**Files:** `mele/user.openclaw/examples/plugins/testnode/index.js`, `openclaw.plugin.json`

Registers `/testnode [on|off|restart|<message>]`. Provides the same start/stop/restart/echo functionality as the `testnode-skill` but as a plugin slash command instead of a skill trigger. The plugin manages the Testnode Python process directly via `execFile` bash scripts and invokes `testnode.echo` via the `openclaw nodes invoke` CLI. Includes retry logic for transient connection errors and a debug log at `testnode-plugin-debug.log`.


## 7. ACP clients: IDE and tool integration via the ACP bridge

### What is an ACP client?

**ACP** stands for **Agent Client Protocol** — an open, standardized protocol for IDEs and coding tools to communicate with AI agents. An ACP client is any IDE, editor, or tool that speaks this protocol and wants to drive an OpenClaw agent session.

The `openclaw acp` command acts as a **bridge**: it sits between the ACP client (e.g. Zed editor) and the OpenClaw Gateway, translating between the two protocols in real time.

**Official documentation:** `https://docs.openclaw.ai/cli/acp`

### How the ACP bridge works

The bridge is a separate process spawned by the IDE. It speaks ACP over stdio (NDJSON — newline-delimited JSON) toward the IDE and speaks the Gateway WebSocket protocol toward the running Gateway:

```
IDE / ACP Client
   │  (ACP over stdio, NDJSON)
   ▼
openclaw acp   ← bridge process
   │  (WebSocket, Gateway protocol)
   ▼
OpenClaw Gateway
   │
   ▼
Agent (Claude, etc.)
```

The bridge translates between the two protocol surfaces:

| ACP (IDE side) | Gateway (agent side) |
|---|---|
| `prompt` request | `chat.send` RPC call |
| `cancel` notification | `chat.abort` RPC call |
| `newSession` / `loadSession` | resolves / creates a Gateway session key |
| `listSessions` | `sessions.list` RPC call |
| `setSessionMode` | `sessions.patch` (thinkingLevel) |
| Gateway `chat` delta events | ACP `agent_message_chunk` stream updates |
| Gateway `agent` tool events | ACP `tool_call` / `tool_call_update` stream updates |

The ACP client never talks to the Gateway directly — it only speaks ACP over stdio to the bridge process it spawned. The bridge holds the actual WebSocket connection to the Gateway.

**Basic usage:**

```bash
# Run the ACP bridge (IDE points to this)
openclaw acp

# Target a remote Gateway
openclaw acp --url wss://gateway-host:18789 --token <token>

# Target a specific agent session
openclaw acp --session agent:main:main

# Interactive debug client (no IDE needed)
openclaw acp client
```

### Use cases

1. **IDE integration (primary use case):** Any IDE implementing ACP (e.g. Zed) can be configured to drive an OpenClaw agent. The user gets a native AI panel in the IDE backed by a running Gateway.

2. **Remote Gateway access from IDE:** Point the bridge at a remote Gateway so the IDE on your laptop drives an agent running on a server — without any changes to the IDE's ACP configuration.

3. **Targeting specific agents/sessions from the IDE:** A team might have multiple named agents (`agent:design:main`, `agent:qa:bug-123`). Each IDE window or config entry can target a different agent by passing `--session`.

4. **Debugging without an IDE:** `openclaw acp client` is a built-in interactive ACP client. It spawns the bridge and lets you type prompts interactively to verify the bridge is working:
   ```bash
   openclaw acp client
   # Point at a remote Gateway:
   openclaw acp client --server-args --url wss://gateway-host:18789 --token <token>
   ```

### Session mapping

By default, each ACP session gets an isolated Gateway session key with the prefix `acp:<uuid>`. Override this to target a specific agent or named session:

```bash
openclaw acp --session agent:main:main       # target the main agent
openclaw acp --session agent:design:main     # target a different agent
openclaw acp --session-label "support inbox" # resolve by label
openclaw acp --reset-session                 # fresh transcript, same key
```

If the ACP client supports metadata, you can override per session via the `_meta` object:

```json
{
  "_meta": {
    "sessionKey": "agent:main:main",
    "sessionLabel": "support inbox",
    "resetSession": true
  }
}
```

### Zed editor setup

Add a custom ACP agent in `~/.config/zed/settings.json` (or via Zed's Settings UI):

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": ["acp"],
      "env": {}
    }
  }
}
```

To target a specific Gateway or agent session:

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": [
        "acp",
        "--url", "wss://gateway-host:18789",
        "--token", "<token>",
        "--session", "agent:design:main"
      ],
      "env": {}
    }
  }
}
```

In Zed, open the Agent panel and select "OpenClaw ACP" to start a thread.

### Which editors and tools support ACP?

ACP has two distinct sides: the **editor side** (the IDE that sends prompts) and the **agent side** (the process that receives and answers them). `openclaw acp` is always the **agent side**. Only editors that implement the ACP *client/editor* role can connect to it directly.

| Tool | ACP role | Can connect to `openclaw acp`? | Alternative path to OpenClaw |
|---|---|---|---|
| **Zed** | ACP editor — native | **Yes** | Configure as shown above |
| **JetBrains IDEs** | ACP editor — in progress | **Yes (when available)** | Same ACP config pattern |
| **Neovim / Emacs** | ACP editor — via plugin | **Yes** | Via CodeCompanion / avante.nvim / agent-shell |
| **Cursor (IDE)** | ACP *agent* via adapter, not editor | No (wrong direction) | OpenResponses HTTP endpoint — see [chapter 8](#openresponses-http-api) |
| **Claude Code CLI** | Terminal agent, not an editor | No | OpenClaw calls it as a CLI backend — see [chapter 8](#openresponses-http-api) |
| **Gemini CLI** | Terminal agent, not an editor | No | OpenClaw calls it as a CLI backend — see [chapter 8](#openresponses-http-api) |

### ACP client vs. gateway client

Both ultimately drive the same OpenClaw Gateway, but at different levels of abstraction:

| Aspect | ACP client | Gateway client |
|---|---|---|
| **Protocol** | Agent Client Protocol (open standard) | OpenClaw's own WebSocket/JSON protocol |
| **Transport** | stdio (NDJSON) | WebSocket (TCP) |
| **Bridge required** | Yes — `openclaw acp` sits in between | No — connects directly to port 18789 |
| **Connection model** | IDE spawns the bridge as a child process | App opens a WebSocket connection |
| **Who uses it** | IDEs, editor plugins, ACP-compatible tools | Apps, nodes, CLI scripts, web UI, mobile apps |
| **Session handling** | ACP sessions mapped to Gateway session keys; isolated `acp:<uuid>` by default | Directly specifies Gateway session keys |
| **Protocol surface** | Narrow: prompt, cancel, session management | Full Gateway RPC surface (sessions, nodes, presence, health, hooks, etc.) |
| **SDK** | `@agentclientprotocol/sdk` | Custom Gateway client (e.g. `claw_client.py`, `GatewayClient` TS class) |
| **Example** | Zed editor integration | WebClaw, macOS app, iOS node, Telegram bot |

**Rule of thumb:** use an **ACP client** when you want an IDE or standard ACP-compatible tool to interact with a running OpenClaw agent without writing Gateway-protocol code. Use a **gateway client** when you are building your own app or service that needs deep integration with the full Gateway API.


## 8. OpenAI Chat Completions HTTP API

### What is the Chat Completions endpoint?

OpenClaw's Gateway can serve an **OpenAI-compatible `POST /v1/chat/completions` endpoint** on the same port as the WebSocket Gateway (default `18789`). This is the classic OpenAI Chat Completions API format (the `messages: [{role, content}]` shape that has been the industry standard since GPT-3) and is supported by the widest range of tools and frameworks.

Like the OpenResponses endpoint, requests are executed as a normal Gateway agent run — routing, permissions, and config all match your Gateway setup.

The endpoint is **disabled by default** and must be enabled in config.

**Official documentation:** `https://docs.openclaw.ai/gateway/openai-http-api`

### Enabling the Chat Completions endpoint

In `openclaw.json` (or via `openclaw config set`):

```json5
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: true }
      }
    }
  }
}
```

The endpoint is then available at:
`http://<gateway-host>:18789/v1/chat/completions`

Authentication uses a bearer token: `Authorization: Bearer <OPENCLAW_GATEWAY_TOKEN>`.

Agent targeting works the same as the OpenResponses endpoint — via the `model` field or headers:

```bash
# model field:
"model": "openclaw:main"

# or via header:
x-openclaw-agent-id: main
x-openclaw-session-key: agent:main:main
```

**Session behavior:** stateless by default (new session per request). Pass a stable `user` string to get a persistent session derived from it.

### Compatible tools

Chat Completions (`/v1/chat/completions`) has been the standard since 2023 and is supported by virtually every AI-aware tool. Use this endpoint — not OpenResponses — when connecting the following:

- **Cursor** — its custom model provider setting expects `/v1/chat/completions`
- **Continue.dev** — VS Code / JetBrains AI extension; uses Chat Completions for custom providers
- **LangChain / LlamaIndex** — their OpenAI client wrappers use `chat.completions.create()`
- **Open WebUI** — uses Chat Completions
- **LiteLLM** — proxies Chat Completions
- **Neovim / VS Code AI plugins** (Avante, CodeCompanion, etc.) — use Chat Completions for custom backends
- **`openai` Python/JS SDK** (any version) — `client.chat.completions.create()`
- **Any tool with an "OpenAI-compatible custom endpoint" setting** — almost all expect this format

### Connecting Cursor to OpenClaw via Chat Completions

1. Enable the endpoint in `openclaw.json` as shown above.
2. In Cursor → Settings → Models, add a custom provider.
3. Set the base URL to `http://<gateway-host>:18789`.
4. Set the API key to your `OPENCLAW_GATEWAY_TOKEN`.
5. Set the model name to `openclaw:main` (or `openclaw:<agentId>` for a specific agent).

Cursor's AI panel will send prompts to your OpenClaw agent and receive streamed SSE responses, backed by your agent's full session memory, skills, and tools.

**Example curl:**

```bash
# Non-streaming:
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{"model": "openclaw", "messages": [{"role": "user", "content": "hi"}]}'

# Streaming:
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{"model": "openclaw", "stream": true, "messages": [{"role": "user", "content": "hi"}]}'
```


## 9. OpenResponses HTTP API

### What is the OpenResponses endpoint?

OpenClaw's Gateway can serve an **OpenResponses-compatible `POST /v1/responses` endpoint** on the same port as the WebSocket Gateway (default `18789`). This is OpenAI's newer Responses API format (launched 2025), which supports richer input types (files, images, item-based multi-turn) compared to Chat Completions. Use it when a tool explicitly targets the Responses API, or when you need file/image input support.

The endpoint is **disabled by default** and must be enabled in config.

**Official documentation:** `https://docs.openclaw.ai/gateway/openresponses-http-api`

### Enabling the OpenResponses endpoint

In `openclaw.json` (or via `openclaw config set`):

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: true }
      }
    }
  }
}
```

The endpoint is then available at:
`http://<gateway-host>:18789/v1/responses`

Authentication uses a bearer token: `Authorization: Bearer <OPENCLAW_GATEWAY_TOKEN>`.

To select which agent to target, either encode it in the `model` field or use a header:

```bash
# model field variants:
"model": "openclaw:main"
"model": "openclaw:design"

# or via header:
x-openclaw-agent-id: main
x-openclaw-session-key: agent:main:main   # full session key
```

### Connecting Cursor to OpenClaw via OpenResponses

Cursor supports adding custom OpenAI-compatible model providers. Once the endpoint is enabled:

1. In Cursor's settings, add a custom model provider.
2. Set the base URL to `http://<gateway-host>:18789` (Cursor appends `/v1/responses` automatically, or check Cursor's docs for the exact path field).
3. Set the API key to your `OPENCLAW_GATEWAY_TOKEN`.
4. Set the model name to `openclaw:main` (or whichever agent you want to target).

Cursor's AI panel will then send prompts to your OpenClaw agent and receive streamed responses (SSE), backed by your agent's full session memory, skills, and tools.

**Session behavior:** by default each request is stateless (new session per call). Pass a stable `user` string in the request body to get a persistent session derived from that identifier.

### CLI backends: Claude Code, Gemini CLI, Codex CLI

Terminal-based agent CLIs (Claude Code, Gemini CLI, Codex CLI) are not HTTP consumers — they call AI model APIs themselves. The integration is therefore the **reverse**: OpenClaw calls *them* as **CLI backends**, using them as a model provider (primary or fallback).

```bash
# Use Claude Code CLI as the model for an OpenClaw agent run:
openclaw agent --message "hi" --model claude-cli/opus-4.6

# Codex CLI works the same way:
openclaw agent --message "hi" --model codex-cli/gpt-5.3-codex
```

Configure in `openclaw.json` under `agents.defaults.cliBackends`:

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": { command: "/usr/local/bin/claude" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["claude-cli/opus-4.6"],
      },
    },
  },
}
```

**Limitations of CLI backends:** tools are disabled (text in/out only), no streaming (output collected then returned), sessions supported via CLI session IDs.

**Official documentation:** `https://docs.openclaw.ai/gateway/cli-backends`

### Chat Completions vs. OpenResponses

Both endpoints expose OpenClaw as an HTTP model server and can be enabled simultaneously. Choose based on what your client supports:

| | Chat Completions (`/v1/chat/completions`) | OpenResponses (`/v1/responses`) |
|---|---|---|
| **API age** | Since 2023 — universal standard | Since 2025 — newer, less adopted |
| **Input format** | `messages: [{role, content}]` | `input`: string or item array |
| **File / image input** | Not supported | Yes — `input_image`, `input_file` |
| **Streaming** | SSE, ends with `data: [DONE]` | SSE, richer event types |
| **Sessions** | Stateless by default; stable via `user` | Same |
| **Config key** | `gateway.http.endpoints.chatCompletions.enabled` | `gateway.http.endpoints.responses.enabled` |
| **Best for** | Cursor, LangChain, Continue.dev, Open WebUI, any OpenAI SDK client, most plugins | Vercel AI SDK, OpenAI SDK v2+, tools explicitly targeting the Responses API |

**Rule of thumb:** enable Chat Completions for maximum compatibility. Enable OpenResponses when you need file/image input or are integrating a framework that targets the newer API. Both can be active at the same time.
