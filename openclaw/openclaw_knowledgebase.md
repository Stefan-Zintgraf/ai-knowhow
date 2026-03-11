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
10. [Agent workspace memory](#agent-workspace-memory)
    - [Overview](#overview)
    - [Memory files](#memory-files)
    - [Who creates the files and when](#who-creates-the-files-and-when)
    - [Automatic memory flush (pre-compaction)](#automatic-memory-flush-pre-compaction)
    - [Housekeeping / retention](#housekeeping--retention)
    - [Vector indexing](#vector-indexing)
    - [Memory retrieval as agentic RAG](#memory-retrieval-as-agentic-rag)
11. [Full message lifecycle: from Telegram prompt to LLM reply](#full-message-lifecycle-from-telegram-prompt-to-llm-reply)
    - [Step 1 — Telegram reception and routing](#step-1--telegram-reception-and-routing)
    - [Step 2 — Message context assembly](#step-2--message-context-assembly)
    - [Step 3 — Session initialization](#step-3--session-initialization)
    - [Step 4 — System prompt and bootstrap context assembly](#step-4--system-prompt-and-bootstrap-context-assembly)
    - [Step 5 — The prompt sent to the LLM](#step-5--the-prompt-sent-to-the-llm)
    - [Step 6 — The agent loop (multi-turn tool use)](#step-6--the-agent-loop-multi-turn-tool-use)
    - [Step 7 — Post-processing the response](#step-7--post-processing-the-response)
    - [Step 8 — Delivery back to Telegram](#step-8--delivery-back-to-telegram)
    - [Step 9 — What is persisted to disk](#step-9--what-is-persisted-to-disk)
    - [Call graph summary](#call-graph-summary)
    - [Step 10 — Subsequent prompts in the same session](#step-10--subsequent-prompts-in-the-same-session)
12. [Cron jobs: scheduling, execution, and delivery](#cron-jobs-scheduling-execution-and-delivery)
    - [Stage 1 — Prompt reception and cron job creation](#stage-1--prompt-reception-and-cron-job-creation)
    - [Stage 2 — How the job is stored and scheduled](#stage-2--how-the-job-is-stored-and-scheduled)
    - [Stage 3 — What happens when the job fires](#stage-3--what-happens-when-the-job-fires)
    - [Cron job configuration options](#cron-job-configuration-options)

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

---

## 10. Agent workspace memory

### Overview

LLMs have no native persistence — every session starts fresh. OpenClaw solves this by giving each agent a **workspace** on disk (default `~/.openclaw/workspace`) that acts as its persistent home. The `memory/` subdirectory is the agent's journal: plain Markdown files that survive session resets and compaction.

### Memory files

| File | Purpose |
|---|---|
| `IDENTITY.md` | Agent's persona (name, vibe, birthday). Written once at bootstrap, rarely changes. |
| `memory/YYYY-MM-DD.md` | Daily log (one file per day). Read today + yesterday at session start. |
| `memory/YYYY-MM-DD-HHMM.md` | Fine-grained variant used when multiple sessions occur on the same day. |
| `MEMORY.md` | Curated long-term memory. Only loaded in the main private session (never in group/shared contexts). |

All files except `IDENTITY.md` are written **by the agent itself**, not by a human.

### Who creates the files and when

- **`IDENTITY.md`** — created by the human (or the bootstrap ritual) once, at agent setup.
- **Daily notes** — created/appended by the agent autonomously during sessions. The `AGENTS.md` instruction file tells the agent to log decisions, context, and things worth remembering.

At every session start the agent reads `AGENTS.md`, `SOUL.md`, `USER.md`, and the last one or two daily memory files to reconstruct context.

### Automatic memory flush (pre-compaction)

When a session approaches its context window limit, OpenClaw's Gateway runs a **silent background turn** (invisible to the user) that instructs the agent to write durable notes before compaction erases the context:

1. Gateway monitors session token usage continuously.
2. When usage crosses a soft threshold (`contextWindow − reserveTokens − softThresholdTokens`), a silent "write memory now" instruction is injected.
3. The agent writes to `memory/YYYY-MM-DD.md` and replies `NO_REPLY` — the user sees nothing.
4. Compaction then runs; the key facts are already on disk.

Config path: `agents.defaults.compaction.memoryFlush`. Defaults: `enabled: true`, `softThresholdTokens: 4000`.

### Housekeeping / retention

**There is no automatic deletion.** Daily memory files accumulate indefinitely — OpenClaw has no retention window, no archiving, and no expiry mechanism for `memory/*.md` files.

The intended workflow is **distillation, not deletion**:
- During periodic heartbeat runs the agent reviews recent daily files, extracts what matters, and writes it into `MEMORY.md`.
- `MEMORY.md` is then pruned of outdated entries over time.
- The raw daily files remain on disk but fade in relevance naturally through the vector index's temporal decay scoring.

Manual cleanup is left to the operator (e.g. `git` archiving of old files).

### Vector indexing

The `memory_search` tool lets the agent query its own past notes semantically, without reading every file. The pipeline:

**Indexing:**
- Markdown files are split into overlapping chunks (default: 400 tokens, 80-token overlap).
- Each chunk is embedded by an embedding model (local GGUF, OpenAI `text-embedding-3-small`, Gemini `gemini-embedding-001`, or Voyage `voyage-4-large`; auto-selected if not configured).
- Embeddings are stored in SQLite (`~/.openclaw/memory/<agentId>.sqlite`), with a `vec0` virtual table for fast cosine distance queries (via the `sqlite-vec` extension) and an FTS5 table for keyword search.
- The index is kept fresh via a file watcher (1.5 s debounce), on session start, and on each search call.
- Unchanged chunks are never re-embedded (embedding cache, up to 50 k entries). If the provider/model changes, the index is fully rebuilt.

**Querying (hybrid search, on by default):**

```
Query text
    │
    ├─► Vector search  (cosine similarity via sqlite-vec)     ─┐
    │                                                           ├─► Weighted merge  (0.7 vector + 0.3 BM25)
    └─► BM25 keyword search  (FTS5, catches exact tokens)     ─┘
                                          │
                              Optional: temporal decay
                              (dated files decay with half-life 30 d;
                               MEMORY.md and undated files never decay)
                                          │
                              Optional: MMR re-ranking
                              (removes near-duplicate results)
                                          │
                              Score threshold (default 0.35) + top-K (default 6)
                                          │
                              Snippets (~700 chars) + file path + line range
                              returned to agent via memory_search tool
```

**Architecture summary:**

```
memory/*.md files on disk
        │
        ▼  file watcher / session start / on-search sync
   Chunker  (400 tokens, 80-token overlap)
        │
        ▼
   Embedding model  (local GGUF / OpenAI / Gemini / Voyage)
        │
        ▼
   SQLite  (~/.openclaw/memory/<agentId>.sqlite)
     ├── chunks table     (text + metadata + raw embedding fallback)
     ├── vec0 table       (float32 vectors, sqlite-vec extension)
     └── FTS5 table       (BM25 full-text index)
        │
        ▼  memory_search tool call
   Vector search  +  BM25 keyword search
        │
        ▼  (optional post-processing)
   Temporal decay  →  MMR re-ranking
        │
        ▼
   Top-K snippets returned to the agent
```

The agent also has a `memory_get` tool to read a specific memory file by path when it needs the full content rather than a snippet.

### Memory retrieval as agentic RAG

#### What kind of RAG is this?

The memory retrieval system is a form of **Retrieval-Augmented Generation (RAG)**, but not the classic pipeline-driven variety. OpenClaw implements **agentic RAG** (also called self-RAG), where the LLM itself decides whether, when, and what to retrieve — rather than having the infrastructure retrieve automatically before each LLM call.

**Classic pipeline-driven RAG:**
```
User query
    │
    ▼  (automatic, unconditional)
Retrieval system  →  top-K chunks injected into prompt
    │
    ▼
LLM generates answer
```
Retrieval happens *always*, for *every* query, before the LLM is involved. The LLM never decides whether it is needed.

**OpenClaw's agentic RAG:**
```
User query
    │
    ▼
LLM turn 1  →  decides to call memory_search("network setup decision")
                   │
                   ▼
              SQLite hybrid search (vector + BM25)  →  top-K snippets
                   │
                   ▼
LLM turn 2  →  optionally calls memory_get("memory/2026-02-18.md", from=5, lines=10)
                   │
                   ▼
LLM turn 3  →  produces final answer incorporating retrieved context
```
The LLM decides *whether* to retrieve (not every message needs it), *what query* to issue (can refine across multiple calls), and *how many times* to retrieve. Retrieval is an explicit tool call inside the agent loop.

#### Comparison: pipeline RAG vs. agentic RAG

| | Pipeline RAG | OpenClaw agentic RAG |
|---|---|---|
| **Trigger** | Automatic, every query | LLM decides (tool call) |
| **Query** | Fixed: reuse of user input | LLM-formulated, can differ from user wording |
| **Iterations** | One retrieval per user turn | Multiple sequential retrievals possible |
| **Skippable?** | No | Yes — LLM skips it for irrelevant queries |
| **Query refinement** | No | Yes — LLM issues follow-up searches |
| **Overhead** | Always paid | Only when relevant |
| **Control** | Infrastructure | LLM judgment |

#### Three memory layers working together

OpenClaw actually combines three distinct memory mechanisms. The vector index is just one of them:

| Layer | Mechanism | Scope | Automatic? |
|---|---|---|---|
| **Direct injection** | `MEMORY.md` + last 2 daily notes pasted verbatim into system prompt | Recent / curated context | Yes — every session start |
| **Agentic RAG** | `memory_search` tool (vector + BM25 hybrid) | All historical notes, any age | No — LLM tool call |
| **Targeted read** | `memory_get` tool (read specific file/lines) | Specific file the LLM wants to read fully | No — LLM tool call, typically after search |

The direct injection handles short-term memory cheaply (no retrieval cost). The vector index fills the gap for long-term recall — notes from days, weeks, or months ago that were not in the injected files.

#### How the LLM is guided to use the RAG layer

Two mechanisms in the system prompt steer the LLM:

**Tool description** (`src/agents/tools/memory-tool.ts`):
> *"Mandatory recall step: semantically search MEMORY.md + memory/*.md … before answering questions about prior work, decisions, dates, people, preferences, or todos; returns top snippets with path + lines."*

**System prompt section** (`src/agents/system-prompt.ts`, `## Memory Recall`):
> *"Before answering anything about prior work, decisions, dates, people, preferences, or todos: run `memory_search` on MEMORY.md + memory/*.md; then use `memory_get` to pull only the needed lines. If low confidence after search, say you checked."*

The word "Mandatory" in the tool description and the "Before answering…" instruction in the system prompt make retrieval effectively automatic for the right class of questions — while keeping it skippable for queries that clearly don't need it (e.g. "what is 2+2?" or "send me a WhatsApp in 60 seconds").

#### Configurability of the RAG instructions

The two pieces of text above have different levels of configurability:

| What | Configurable? | How |
|---|---|---|
| `## Memory Recall` section text | No — hardcoded in `src/agents/system-prompt.ts` | Can only be *suppressed* (see below) |
| Citations line (`Source: <path#line>`) | Yes | `memory.citations: "auto" / "on" / "off"` in `openclaw.json` |
| `memory_search` tool description | No — hardcoded in `src/agents/tools/memory-tool.ts` | Can only be *suppressed* (see below) |
| Override/soften without disabling | Yes | Add instructions to workspace `AGENTS.md` |

**Suppressing the entire `## Memory Recall` section and both tools:**

The section is only injected when `memory_search` or `memory_get` are registered. Disabling them removes both the tools and the system prompt section:

```json5
// Option A — disable memory search in openclaw.json:
{ agents: { defaults: { memorySearch: { enabled: false } } } }

// Option B — disable the memory plugin slot entirely:
{ plugins: { slots: { memory: "none" } } }
```

**Controlling citation behaviour** (`memory.citations` in `openclaw.json`):

```json5
{ memory: { citations: "off" } }   // LLM told not to mention file paths/line numbers
{ memory: { citations: "on" } }    // always include Source: <path#line>
{ memory: { citations: "auto" } }  // include when helpful (default)
```

**Softening without disabling — use `AGENTS.md`:**
Because workspace files are injected *after* the hardcoded system prompt sections, instructions in `AGENTS.md` effectively override or refine them. For example, adding the following to `AGENTS.md` narrows when `memory_search` is called:

```markdown
Only use `memory_search` when the user explicitly asks about past events,
past decisions, or something from a prior session. Do not search for
routine tasks or general knowledge questions.
```

#### What changes in the prompt workflow when vector search is enabled vs. disabled

The chapter below (chapter 11) traces the full message lifecycle. When `memorySearch.enabled = true` (the default), the following elements are different compared to a setup with no vector database:

**System prompt — extra `## Memory Recall` section:**
When `memory_search` and/or `memory_get` tools are registered, `buildAgentSystemPrompt()` in `src/agents/system-prompt.ts` injects an additional section into the system prompt:
```
## Memory Recall
Before answering anything about prior work, decisions, dates, people,
preferences, or todos: run memory_search on MEMORY.md + memory/*.md;
then use memory_get to pull only the needed lines. If low confidence
after search, say you checked.
Citations: include Source: <path#line> when it helps the user verify
memory snippets.
```
Without vector search this entire section is absent.

**Tool definitions — two extra tools in the LLM API call:**
`createOpenClawCodingTools()` (`src/agents/pi-embedded-runner/run/attempt.ts`) registers `memory_search` and `memory_get` only when `memorySearch.enabled` resolves to true. These are added to the `tools[]` array sent to the LLM. Without vector search, neither tool exists and the LLM has no way to query past notes beyond what was injected at session start.

**Agent loop — additional turns for retrieval:**
When the LLM issues a `memory_search` call, the agent loop executes an extra turn: the SQLite query runs, snippets are returned as a `tool_result`, and the LLM makes another API call with the results in context. A typical memory-aware response therefore costs 2–3 LLM API calls instead of 1. Without vector search, no extra turns occur for memory retrieval.

**Index sync — triggered on search:**
`src/agents/memory-search.ts` configures `sync.onSearch = true` by default, meaning the SQLite index is checked for freshness and updated if any memory files changed *at the moment the `memory_search` tool is called*. This happens inside the agent loop, transparently to the user. Without vector search this sync never runs.

**What does NOT change:**
- The direct file injection at session start (`MEMORY.md`, today's + yesterday's daily notes) is **independent** of vector search and happens regardless
- All other steps (reception, routing, session init, delivery) are identical
- The `memory_get` tool can technically be used even without the vector index to read a known file by path, but in practice it is almost always called after a `memory_search` result

---

## 11. Full message lifecycle: from Telegram prompt to LLM reply

This chapter traces everything that happens when a user sends the **very first message** of a new session via Telegram, from packet arrival to the reply appearing in the chat.

### Step 1 — Telegram reception and routing

**`src/telegram/monitor.ts` — `monitorTelegramProvider()`**

The Gateway process runs a grammY long-polling loop (or webhook) that calls the Telegram `getUpdates` API every 30 seconds. Incoming updates are fed into a concurrent sink controlled by `resolveAgentMaxConcurrent()`.

Before any handler fires, a `sequentialize()` middleware (`src/telegram/bot.ts`) ensures all updates from the same `chatId` (and `threadId` for forum topics) are processed **sequentially** — preventing two agent runs from starting in parallel for the same conversation.

A deduplication layer drops replayed or already-seen update IDs.

**`src/telegram/bot-handlers.ts` — `registerTelegramHandlers()`**

The `bot.on("message")` handler:
1. Extracts `chatId`, group/DM flag, and optional `messageThreadId`.
2. Evaluates group access policy (`evaluateTelegramGroupBaseAccess`, `evaluateTelegramGroupPolicyAccess`) — drops the message if the group or topic is disabled, or the sender is not on the allowlist.
3. Checks mention gating for group chats (`requireMention`).
4. Passes the message to `processInboundMessage()`.

**Inbound debouncer:** rapid consecutive messages from the same sender are coalesced (configurable wait). A single first message is flushed immediately.

---

### Step 2 — Message context assembly

**`src/telegram/bot-message-context.ts` — `buildTelegramMessageContext()`**

This builds the `ctxPayload` object that travels through the rest of the pipeline:

| Field | Content |
|---|---|
| `Body` | Formatted envelope: `[From: …] [Timestamp: …] [Channel: Telegram] [ChatType: direct]` + user text |
| `BodyForAgent` | Raw user text only |
| `SessionKey` | e.g. `agent:wolfgang:telegram:6672375440` |
| `From` / `To` | Sender ID / account routing |
| `MediaPath(s)` | Local file paths for any downloaded audio/image attachments |
| `ChatType` | `direct` / `group` |
| `OriginatingChannel` | `telegram` |

**Route resolution** (`src/routing/resolve-route.ts`): maps `(channel="telegram", accountId, chatId)` → `agentId` + `sessionKey` via config bindings.

**Access control (DM):** `dmPolicy` is evaluated — options are `"pairing"` (default), `"allowlist"`, `"open"`, `"disabled"`. An unrecognized user under `"pairing"` gets a pairing code and no agent response.

**Session recording:** `recordInboundSession()` updates `sessions.json` with `lastRoute` so replies know where to send back.

**ACK reaction:** if configured, an emoji reaction is set on the inbound message immediately (fire-and-forget "seen" signal).

---

### Step 3 — Session initialization

**`src/auto-reply/reply/session.ts` — `initSessionState()`**

This resolves the session identity before any agent work begins:

1. **Reset trigger check:** if the message body matches a reset trigger (`/new`, `/reset`), `isNewSession = true`.
2. **Load `sessions.json`:** existing `SessionEntry` for this `sessionKey` is read from disk.
3. **Freshness check:** `evaluateSessionFreshness()` compares `entry.updatedAt` against the idle-timeout policy. For a brand-new conversation: no entry exists → `isNewSession = true`.
4. **New session ID:** `crypto.randomUUID()` → `sessionId`. This UUID names the JSONL transcript file.
5. **Write `sessions.json`:** a new `SessionEntry` is written immediately with `{ sessionId, updatedAt: now(), systemSent: false, abortedLastRun: false, ... }`.
6. **Plugin hook:** `session_start` hook fires (fire-and-forget) — can be used by plugins for custom on-session-start logic.

---

### Step 4 — System prompt and bootstrap context assembly

**`src/agents/pi-embedded-runner/run/attempt.ts` → `src/agents/system-prompt.ts`**

#### Bootstrap file loading

`resolveBootstrapContextForRun()` scans the workspace directory and loads these files:

| File | Loaded when |
|---|---|
| `AGENTS.md` | Always |
| `SOUL.md` | Always |
| `USER.md` | Always |
| `TOOLS.md` | Always |
| `IDENTITY.md` | Always |
| `MEMORY.md` | Main/private session only |
| `memory/YYYY-MM-DD.md` | Today + yesterday |
| `BOOTSTRAP.md` | Once at first run, then deleted by the agent |

Each file is truncated individually (`bootstrapMaxChars`, default 20 000 chars) and collectively (`bootstrapTotalMaxChars`, default 150 000 chars) to protect the context window. Plugin hooks can inject or override files via `applyBootstrapHookOverrides()`.

#### System prompt structure

`buildAgentSystemPrompt()` assembles the full system prompt string in this order:

```
Role: "You are a personal assistant running inside OpenClaw."

## Tooling          ← list of available tools + usage guidance
## Tool Call Style
## Safety
## OpenClaw CLI Quick Reference
## Skills           ← if skills are configured
## Memory Recall    ← if memory_search/memory_get tools available
## Workspace        ← working directory path
## Documentation    ← path to OpenClaw docs (if configured)
## User Identity    ← owner phone/contact if configured
## Current Date & Time
## Workspace Files (injected)
## Reply Tags
## Messaging        ← per-platform formatting rules
## Voice            ← if TTS configured
## Group Chat Context  ← for group sessions (mention gating, history, etc.)
## Reactions        ← if reaction guidance configured
## Silent Replies   ← "When you have nothing to say, reply with ONLY: NO_REPLY"
## Heartbeats
## Runtime          ← agent=<id>, host=<machine>, model=<provider/model>, channel=telegram, ...

# Project Context
## AGENTS.md        ← full file content
## SOUL.md          ← full file content
## USER.md          ← full file content
## MEMORY.md        ← full file content  (main session only)
## memory/2026-03-01.md  ← today's notes
## memory/2026-02-28.md  ← yesterday's notes
```

This entire string is set as the system prompt of the `pi-coding-agent` session.

---

### Step 5 — The prompt sent to the LLM

**`src/auto-reply/reply/get-reply-run.ts` — `runPreparedReply()`**

The user turn (the actual prompt content) is assembled as:

```
[New session]                           ← injected for first message of a new session
[inbound context prefix if any]
<formatted envelope + user message text>
```

For a typical first Telegram message from Stefan, what actually arrives at the LLM looks like:

```
System: <full system prompt as above>

User:
[New session]
Conversation info (untrusted metadata):
{ "message_id": "1234", "sender": "6672375440" }

[Fri 2026-03-01 12:34 GMT+1] Hello, what can you do?
```

**Tool definitions** are attached to the API call — all available tools (`read`, `write`, `edit`, `grep`, `find`, `ls`, `exec`, `web_search`, `web_fetch`, `cron`, `message`, `memory_search`, `memory_get`, `image`, etc.) with their full JSON schemas.

For a **new session** the `messages[]` conversation history is empty — the system prompt carries all prior context via the injected workspace files.

---

### Step 6 — The agent loop (multi-turn tool use)

**`@mariozechner/pi-coding-agent` — the agentic loop, driven from `attempt.ts`**

`activeSession.prompt(userText)` kicks off the loop. During streaming:
- `onPartialReply` fires for each text delta → the Gateway edits a "draft" Telegram message in real time so the user sees the reply being typed.

The loop:

```
LLM call
    │
    ├─ text reply only → loop ends, text is the final response
    │
    └─ tool_use block(s)
            │
            ├─ tool handler executes (read file, web search, run exec, write file, ...)
            │
            └─ tool_result appended to transcript
                    │
                    └─ LLM call again (with full history + tool results)
                            │
                            └─ (repeat until no more tool calls)
```

Each LLM turn and tool call is **immediately appended** to the JSONL transcript by `SessionManager`. The loop terminates when the LLM produces a final assistant text with no tool calls, or when an abort/timeout fires.

**Compaction** can also happen mid-loop: if the context fills up, `pi-coding-agent` summarizes older turns into a `compaction` entry in the transcript and retries the last LLM call with the compacted context.

**Memory flush** may run as a *separate pre-check* before the main loop: if `sessions.json` shows token usage is near the soft threshold, a silent agent turn writes to `memory/YYYY-MM-DD.md` first, then the main loop runs. The user never sees this turn.

---

### Step 7 — Post-processing the response

**`src/auto-reply/reply/reply-delivery.ts` — `normalizeReplyPayloadDirectives()`**

After the loop ends, each assistant text block is processed:

- **`NO_REPLY`:** if the text is exactly `NO_REPLY`, `isSilent = true` → payload is suppressed entirely, nothing is sent to the user.
- **`[[reply_to_current]]` / `[[reply_to:<id>]]`:** stripped from text, sets the Telegram `reply_to_message_id` on the outgoing message.
- **`MEDIA:<path>`:** parsed out, converted to `mediaUrl` for attachment delivery.
- **Unscheduled reminder detection:** if the LLM said "I'll remind you" but didn't call the `cron` tool, a note is appended to the reply: *"Note: I did not schedule a reminder in this turn, so this will not trigger automatically."*

**Token usage** (`persistRunSessionUsage()`) is written back to `sessions.json`: `totalTokens`, `inputTokens`, `outputTokens`, `contextTokens`.

**`systemSent = true`** is written to `sessions.json` after the first successful turn — subsequent turns in the same session don't re-inject the full bootstrap context.

---

### Step 8 — Delivery back to Telegram

**`src/telegram/bot/delivery.ts` — `deliverReplies()`**

1. **Markdown → Telegram HTML:** `markdownToTelegramHtml()` converts the LLM's Markdown to Telegram's HTML subset (`<b>`, `<i>`, `<code>`, `<pre>`, `<a>`). Tables are converted based on `tableMode` config.
2. **Chunking:** messages exceeding Telegram's 4096-char limit are split by `chunkMarkdownTextWithMode()` (by length or by newline boundary).
3. **Draft finalization:** if a streaming draft message was being edited in real time, the final chunk replaces it with `editMessageTelegram()` — avoiding an extra new message for typical replies.
4. **Send:** `bot.api.sendMessage(chatId, html, { parse_mode: "HTML", ... })` for text. `sendPhoto`, `sendDocument`, `sendAudio`, `sendVoice`, etc. for media.
5. **Reply threading:** if `replyToCurrent` is set, `reply_parameters` is included so the Telegram message threads correctly.
6. **Retry:** transient Telegram API errors (rate limits, network errors) are retried via `retryAsync()`.
7. **ACK removal:** if `removeAckAfterReply` is configured, the "seen" emoji reaction on the inbound message is cleared.
8. **Fallback:** if all delivery attempts failed but the agent did produce a non-silent response, a fallback `"No response generated. Please try again."` is sent.

---

### Step 9 — What is persisted to disk

| What | Where | When |
|---|---|---|
| **JSONL transcript** | `~/.openclaw/sessions/<agentId>/<timestamp>_<uuid>.jsonl` | After every LLM turn and tool call (streaming, not batched at end) |
| **`sessions.json`** | `~/.openclaw/sessions/<agentId>/sessions.json` | On session init, after run (token usage), after compaction |
| **Memory files** | `~/.openclaw/workspace/memory/YYYY-MM-DD.md` | Written by agent during memory flush turns (via `write` tool) |
| **Telegram update offset** | `~/.openclaw/update-offset-<accountId>.json` | After each processed update (prevents replay on restart) |

---

### Call graph summary

```
monitorTelegramProvider()  [monitor.ts]
  └─ grammY bot loop (long-poll / webhook)
       └─ sequentialize(getTelegramSequentialKey)   ← serializes same-chat updates
       └─ bot.on("message")  [bot-handlers.ts]
            └─ access / group policy checks
            └─ processInboundMessage()
                 └─ inboundDebouncer (coalesces rapid messages)
                 └─ buildTelegramMessageContext()  [bot-message-context.ts]
                      └─ resolveAgentRoute()  →  sessionKey
                      └─ access control (DM/group policy)
                      └─ formatInboundEnvelope()  →  Body (with metadata header)
                      └─ recordInboundSession()  →  sessions.json (lastRoute)
                      └─ ACK reaction (fire-and-forget)
                 └─ dispatchTelegramMessage()  [bot-message-dispatch.ts]
                      └─ createTelegramDraftStream()  ← live "typing" preview
                      └─ getReplyFromConfig()  [get-reply.ts]
                           └─ ensureAgentWorkspace()
                           └─ applyMediaUnderstanding()  (audio transcript / image)
                           └─ initSessionState()  [session.ts]
                                └─ loadSessionStore()  →  sessions.json
                                └─ crypto.randomUUID()  →  sessionId
                                └─ updateSessionStore()  →  sessions.json
                                └─ session_start plugin hook
                           └─ runPreparedReply()  [get-reply-run.ts]
                                └─ buildInboundMetaSystemPrompt()
                                └─ runReplyAgent()  [agent-runner.ts]
                                     └─ runMemoryFlushIfNeeded()  ← silent pre-turn
                                     └─ runEmbeddedAttempt()  [attempt.ts]
                                          └─ resolveBootstrapContextForRun()
                                               └─ loadWorkspaceBootstrapFiles()
                                                    (AGENTS.md, SOUL.md, USER.md,
                                                     MEMORY.md, memory/*.md, ...)
                                          └─ buildAgentSystemPrompt()  [system-prompt.ts]
                                          └─ createOpenClawCodingTools()  →  tools[]
                                          └─ SessionManager.open(sessionFile)  →  JSONL
                                          └─ activeSession.prompt(userText)
                                               └─ ── pi-coding-agent agentic loop ──
                                               └─ LLM API call  (Anthropic/OpenAI/Gemini/…)
                                                    streaming delta → onPartialReply
                                                         → editMessageTelegram() (draft update)
                                               └─ tool_use → tool handler → tool_result
                                                    → next LLM call  (repeat)
                                               └─ final text reply  →  loop ends
                                               └─ JSONL written after every turn/tool
                                          └─ persistRunSessionUsage()  →  sessions.json
                                     └─ buildReplyPayloads()
                                └─ normalizeReplyPayloadDirectives()
                                     (NO_REPLY filter, reply-tag strip, MEDIA parse)
                      └─ deliver(payload, {kind:"final"})
                           └─ flushDraft()  (stop streaming preview)
                           └─ markdownToTelegramHtml()  →  Telegram HTML
                           └─ bot.api.sendMessage(chatId, html)
                                → message visible to user in Telegram
                           └─ persistRunSessionUsage() / sessionSent=true → sessions.json
                           └─ removeAckReaction (if configured)
```

---

### Step 10 — Subsequent prompts in the same session

The chapter above describes the **first** message of a new session. For every subsequent message in the same session, most steps are identical (reception, routing, context assembly, agent loop, delivery). The differences are precise and all stem from a single flag: `systemSent = true` in `sessions.json`.

The key computed variable in `get-reply-run.ts` is:

```typescript
const isFirstTurnInSession = isNewSession || !currentSystemSent;
// → false for all subsequent turns
```

Here is what changes (and what does not) for turns 2, 3, 4, …:

#### What is the same on every turn

| Aspect | Behaviour |
|---|---|
| Telegram reception, sequentialization, deduplication | Identical |
| Message envelope assembly (`Body`, `BodyForAgent`, metadata) | Identical |
| Session key resolution | Identical — same `sessionKey`, same `sessionId` returned from `sessions.json` |
| Agent loop (tool calls, multi-turn LLM, streaming draft) | Identical |
| Post-processing (`NO_REPLY`, reply tags, token usage persistence) | Identical |
| Delivery (Telegram HTML, chunking, send) | Identical |
| Memory flush check | Identical — runs if token threshold is crossed |

#### What is different on subsequent turns

**1. `initSessionState()` — no new session, no new UUID**

`sessions.json` has a fresh entry with `systemSent: true` and `updatedAt` within the idle timeout window. `evaluateSessionFreshness()` returns `fresh: true`. Therefore:
- `isNewSession = false`
- `systemSent = true` (read from the stored entry)
- The **same `sessionId`** UUID is reused → the **same JSONL transcript file** is continued
- `compactionCount`, `memoryFlushAt`, token metrics are carried over (not reset)
- No `session_start` / `session_end` plugin hooks fire

**2. System prompt — same structure, but bootstrap files are re-read from disk**

The system prompt is **rebuilt from scratch** on every single turn. `resolveBootstrapContextForRun()` reads `AGENTS.md`, `SOUL.md`, `USER.md`, etc. from disk again. This means if you edited a workspace file between two messages, the agent sees the update immediately — there is no in-memory cache of the system prompt.

However, `pi-coding-agent` only writes bootstrap files into the system prompt **when the transcript is new**. On subsequent turns, the system prompt override (`applySystemPromptOverrideToSession()`) is still applied to the running session, but the bootstrap file contents were already baked into the first message's context window. In practice the system prompt is re-sent to the LLM on every API call because the `pi-coding-agent` always includes it in the `system` field — but the model's actual "memory" of earlier turns comes from the **conversation history** in the transcript, not from re-reading the bootstrap files.

**3. Prompt — no `[New session]` prefix, no thread history**

`inboundUserContext` is built differently:

```
First turn:   [New session] + thread history/starter (if any) + message body
Subsequent:   message body only (no [New session], no ThreadStarterBody)
```

Specifically:
- `buildInboundMetaSystemPrompt()` receives `{ ...sessionCtx, ThreadStarterBody: undefined }` — thread starter context is suppressed after the first turn
- `threadContextNote` (the `[Thread history - for context]` prefix) is only added when `isNewSession`
- `inboundUserContext` has no new-session markers

**4. `messages[]` conversation history — grows with each turn**

For the first turn, `messages[]` is empty. For turn N, the JSONL transcript already contains all previous user/assistant/tool turns. `SessionManager.open(sessionFile)` loads them and they are included in the LLM API call as the full conversation history. The model therefore has the complete dialogue in its context window (until compaction kicks in).

**5. Skills snapshot — not rebuilt unless stale**

`ensureSkillSnapshot()` is called with `isFirstTurnInSession = false`. It only rebuilds the skills snapshot if it is stale (skills files changed on disk). On a normal subsequent turn, the cached `skillsSnapshot` in `sessions.json` is reused, saving some disk work.

**6. Group chat intro — suppressed**

For group sessions, `buildGroupIntro()` (activation mode, lurking rules, etc.) is only injected when `isFirstTurnInSession || groupActivationNeedsSystemIntro`. On subsequent turns it is skipped, keeping the extra system prompt shorter.

**7. `session_start` hook — does not fire**

The `session_start` plugin hook only fires when `isNewSession`. On subsequent turns it is skipped entirely.

#### When does a "subsequent turn" become a new session?

`initSessionState()` will set `isNewSession = true` and assign a fresh `sessionId` (effectively restarting everything as if it were a first turn) in these cases:

| Trigger | Mechanism |
|---|---|
| User sends `/new` or `/reset` | `resetTriggers` match → `resetTriggered = true` → `isNewSession = true` |
| Idle timeout expires | `evaluateSessionFreshness()` returns `fresh: false` → `isNewSession = true` |
| Daily reset (default: 04:00 local time) | Same freshness check with daily reset policy |
| Gateway restart | `sessions.json` survives restart; session is **resumed** as long as it is still fresh |

When the Gateway restarts mid-session, `sessions.json` is read from disk and the same `sessionId` (same JSONL file) is picked up — so the conversation continues seamlessly as if no restart happened, provided the idle timeout has not expired.

---

## 12. Cron jobs: scheduling, execution, and delivery

This chapter explains the full lifecycle of a cron job: from the moment a user asks the agent to schedule a future action, through storage and scheduling, to the actual execution when the timer fires.

> **Prerequisites:** This chapter builds on the concepts from [Chapter 11](#full-message-lifecycle-from-telegram-prompt-to-llm-reply) (message lifecycle) and [Chapter 10](#agent-workspace-memory) (memory / sessions). Overlapping details are not repeated here.

### Stage 1 — Prompt reception and cron job creation

#### How the user triggers a cron job

The user does not need to know about `cron` as a technical concept. They can simply send a natural-language request, for example:

> *"Send me a WhatsApp message tomorrow at 9 AM with a weather summary."*

This message arrives via the normal inbound channel (Telegram, WhatsApp, etc.) and goes through the standard message lifecycle described in Chapter 11 — reception, session initialization, system prompt assembly, and the LLM agent loop.

#### Who decides to create a cron job?

The **LLM** itself decides. There is no keyword-matching or hard-coded cron-detection layer. The LLM receives the user's request as a standard user message and, based on:
- the `cron` tool description in the system prompt, and
- the general instructions to prefer `cron` for scheduled or timed tasks,

it decides to call the `cron` tool with `action: "add"`. The decision is entirely agentic — the LLM understands the intent and selects the appropriate tool.

The `cron` tool description (from `src/agents/tools/cron-tool.ts`) gives the LLM enough guidance to make good scheduling choices:
- Use `sessionTarget: "isolated"` with `payload.kind: "agentTurn"` for standalone tasks that run independently (default preferred).
- Use `sessionTarget: "main"` with `payload.kind: "systemEvent"` when the event should appear in the main session context and be handled during the next heartbeat.

#### What the LLM emits: the `cron` tool call

A typical LLM tool call to schedule an isolated one-shot job looks like:

```json
{
  "action": "add",
  "job": {
    "name": "WhatsApp weather reminder",
    "schedule": { "kind": "at", "at": "2026-03-02T09:00:00+01:00" },
    "sessionTarget": "isolated",
    "payload": {
      "kind": "agentTurn",
      "message": "Fetch today's weather summary and send it to the user."
    },
    "delivery": {
      "mode": "announce",
      "channel": "whatsapp",
      "to": "+49123456789"
    },
    "deleteAfterRun": true
  }
}
```

Key fields resolved at tool-call time:
- **`agentId`** — automatically injected by the tool handler from the calling session's context (so the job runs under the same agent that created it).
- **`sessionKey`** — the originating session key is recorded so a main-session summary can later be posted there.
- **`delivery.to`** — if omitted, the handler infers it by parsing the calling session key (e.g. `telegram:direct:123456789` → `to: "123456789"`, `channel: "telegram"`). This means "send back to whoever asked me".

#### Flat-params recovery

Some non-frontier LLMs (e.g. Grok) sometimes flatten job fields to the top level instead of nesting them inside `job`. The tool handler detects this and reconstructs a synthetic `job` object from recognized top-level keys (`name`, `schedule`, `payload`, `message`, `text`, `model`, etc.).

#### Context injection for main-session jobs

For `systemEvent` payloads, the tool handler can optionally embed recent conversation history into the event text via `contextMessages` (0–10 messages). This gives the future heartbeat turn enough context about what the user originally asked for.

---

### Stage 2 — How the job is stored and scheduled

#### Persistence: `~/.openclaw/cron/jobs.json`

After the `cron.add` Gateway RPC returns, the job is written to `~/.openclaw/cron/jobs.json` by `CronService`. Each job record includes:

| Field | Purpose |
|---|---|
| `id` | Stable UUID for the job |
| `name` | Human-readable label |
| `schedule` | `at` / `every` / `cron` descriptor |
| `sessionTarget` | `"main"` or `"isolated"` |
| `payload` | `systemEvent` or `agentTurn` with the message |
| `delivery` | Channel, target, mode |
| `agentId` | Which agent should run the job |
| `sessionKey` | Originating session (for main-session summary) |
| `deleteAfterRun` | Whether to auto-delete after a successful run |
| `state.nextRunAtMs` | When the scheduler will next fire this job |

The store is an in-memory JSON object that is flushed to disk on every change. Manual edits while the Gateway is running are unsafe.

#### Run history: `~/.openclaw/cron/runs/<jobId>.jsonl`

Each execution appends a JSONL entry with timestamps, status, model used, token usage, and any error message. The file is auto-pruned.

#### The scheduler timer

Inside `CronService` (`src/cron/service/timer.ts`), a single `setTimeout` loop drives execution:

1. **`armTimer()`** — sets a `setTimeout` for `min(nextRunAtMs - now, 60 s)`. The 60-second cap ensures the scheduler wakes at least once per minute to recover from clock drift or process pauses.
2. **`onTimer()`** fires when the timeout expires, collects all due jobs (`nextRunAtMs ≤ now`), marks each as `runningAtMs`, and executes them.
3. After each job finishes, `armTimer()` is called again to set the next wake time.

#### Schedule kinds

| Kind | Config | Use case |
|---|---|---|
| `at` | `{ kind: "at", at: "<ISO-8601>" }` | One-shot at exact UTC time |
| `every` | `{ kind: "every", everyMs: <ms> }` | Fixed interval from anchor |
| `cron` | `{ kind: "cron", expr: "0 7 * * *", tz: "Europe/Berlin" }` | Standard 5- or 6-field cron expression with timezone |

For recurring top-of-hour cron expressions (e.g. `0 * * * *`), OpenClaw applies a **deterministic per-job stagger** of up to 5 minutes (derived from a SHA-256 hash of the job ID) to spread Gateway load. Fixed-hour expressions like `0 7 * * *` fire exactly on schedule. Stagger can be overridden with `schedule.staggerMs`.

#### Error backoff

Recurring jobs that fail get exponential backoff: 30 s → 1 min → 5 min → 15 min → 60 min between retries. Backoff resets after the next successful run. One-shot (`at`) jobs disable themselves after any terminal outcome (ok, error, or skipped).

---

### Stage 3 — What happens when the job fires

Two fundamentally different execution paths exist depending on `sessionTarget`.

#### Path A: Main-session jobs (`sessionTarget: "main"`)

1. `CronService` calls `enqueueSystemEvent(text, { sessionKey, agentId })`.
2. The system event is inserted into the in-memory event queue for the target session.
3. If `wakeMode: "now"`, `runHeartbeatOnce()` is called immediately. The heartbeat runner picks up the system event alongside `HEARTBEAT.md` and runs a normal heartbeat agent turn (see [Gateway heartbeat docs](/gateway/heartbeat)).
4. If `wakeMode: "next-heartbeat"`, `requestHeartbeatNow()` signals the heartbeat scheduler to trigger on its next cycle.
5. The heartbeat turn's output is handled exactly like any other heartbeat: delivered if non-`HEARTBEAT_OK`, suppressed otherwise.

Main-session jobs do **not** create a new isolated session. They piggyback on the existing main-session context and share the same conversation history.

#### Path B: Isolated jobs (`sessionTarget: "isolated"`)

Isolated jobs run in a dedicated session, independent of the main session. This is the default and most common path.

##### Step B-1: Session resolution

`resolveCronSession()` (`src/cron/isolated-agent/session.ts`) loads or creates a session entry for the session key `cron:<jobId>`:

- If a valid session already exists for this `jobId` (e.g. from a prior run) **and** it has not expired (the freshness policy applies the "direct" reset type — same as WhatsApp/Telegram direct conversations), the existing `sessionId` is reused.
- Otherwise a fresh `sessionId` (UUID) is created. Each run typically starts a completely **fresh conversation** — no prior chat history carries over.
- The session is stored under `sessions.json` using the key `cron:<jobId>` and a per-run sub-key `cron:<jobId>:run:<sessionId>`.

##### Step B-2: Prompt construction

The prompt sent to the LLM is built in `runCronIsolatedAgentTurn()` (`src/cron/isolated-agent/run.ts`):

```
[cron:<jobId> <job name>] <payload.message>
Now: <date-time in configured locale/timezone>
```

Additionally:
- If `delivery.mode` is `announce`, an instruction is appended: *"Return your summary as plain text; it will be delivered automatically. If the task explicitly calls for messaging a specific external recipient, note who/where it should go instead of sending it yourself."*
- For external hook sessions (e.g. Gmail), the content is wrapped with security boundaries to prevent prompt injection (unless `allowUnsafeExternalContent` is set).
- The `message` tool is **disabled** (`disableMessageTool: true`) when `delivery` is requested — the agent is not supposed to send messages directly; the cron infrastructure handles delivery.

##### Step B-3: System prompt and context

The isolated cron turn calls `runEmbeddedPiAgent()` (same function used for the normal message lifecycle, see [Chapter 11 Step 5](#step-5--the-prompt-sent-to-the-llm)). This means:
- The full system prompt is assembled (agent rules, tool definitions, `## Memory Recall` section).
- **Bootstrap files are loaded** from the agent's workspace: `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, and recent `memory/YYYY-MM-DD.md` files — the same context injection as a normal first turn.
- `systemSent` is set to `true` in the session store before the run, so on the next run the system prompt is treated as already having been sent (relevant if the session is reused).

Because each isolated run starts with a **fresh session** (no history), there is **no** `messages[]` conversation history carried over from previous runs of the same job. The context window contains only the system prompt + bootstrap files + the single user-turn prompt.

##### Step B-4: Model and thinking selection

Model resolution priority (highest wins):
1. Per-job `payload.model` override (e.g. `"opus"` or `"anthropic/claude-opus-4-20250514"`).
2. Session `modelOverride` stored in `sessions.json` (set by prior `/model` commands in that cron session).
3. Hook-specific model (e.g. `hooks.gmail.model` for Gmail hooks).
4. Agent config default (`agents.defaults.model`).

Similarly for thinking level: per-job `payload.thinking` > `hooks.gmail.thinking` > `agents.defaults.thinkingDefault`.

##### Step B-5: Agent loop execution

`runEmbeddedPiAgent()` runs the standard multi-turn LLM loop (see [Chapter 11 Step 6](#step-6--the-agent-loop-multi-turn-tool-use)):
- The LLM receives the prompt and available tools.
- It may call tools (`memory_search`, `memory_get`, `exec`, `web`, etc.) in multiple loops.
- The `message` tool is suppressed; `disableMessageTool: true` prevents the agent from directly sending messages during the run.
- The loop ends when the LLM emits a final text response without further tool calls (or when the timeout fires).

The run has a configurable timeout: `payload.timeoutSeconds` > `agents.defaults.timeoutSeconds`. The hard safety-net cap is 10 minutes (`DEFAULT_JOB_TIMEOUT_MS`).

##### Step B-6: Output collection and delivery

After the agent loop completes, `runCronIsolatedAgentTurn()` collects the payloads (the LLM's final text outputs) and decides how to deliver them:

**`delivery.mode = "announce"` (default):**

1. The last non-empty text payload is taken as the summary.
2. If the summary is just `HEARTBEAT_OK` (or a short ack), delivery is **skipped** entirely — no message is sent.
3. Otherwise, the summary is delivered via `runSubagentAnnounceFlow()`:
   - The announce flow injects a system event into the main session: `"Cron: <summary>"`.
   - The main session's chat channel is resolved from the delivery config (`channel` + `to`).
   - The actual message is sent to the user's chat (e.g. Telegram or WhatsApp) via the outbound channel adapter — same path as a normal reply (Markdown → HTML conversion, message chunking, etc.).
   - A brief summary is also posted to the **main session** via system event, and `wakeMode` controls whether an immediate heartbeat is triggered (`now`) or whether it waits for the next scheduled one (`next-heartbeat`).
4. If the isolated run already sent a message to the same target via the `message` tool, delivery is **skipped** to avoid duplicates (`skipMessagingToolDelivery`).

**`delivery.mode = "webhook"`:**

- No channel delivery.
- When the job finishes, the Gateway POSTs the full `cron:finished` event JSON to `delivery.to` (the webhook URL) with an optional `Authorization: Bearer <token>` header.
- No main-session summary is posted.

**`delivery.mode = "none"`:**

- Internal only. Nothing is sent to the user.
- A main-session summary is still posted if applicable (it was explicitly set to `none` for channel delivery only).

##### Step B-7: Post-run bookkeeping

After delivery:
- Token usage, model/provider used, and duration are written back to `sessions.json`.
- A run log entry is appended to `~/.openclaw/cron/runs/<jobId>.jsonl`.
- `applyJobResult()` computes `nextRunAtMs`:
  - One-shot (`at`): job is disabled and optionally deleted (`deleteAfterRun: true`).
  - Recurring: natural next schedule time is computed; error backoff is applied if the run failed.
- `armTimer()` re-arms the scheduler for the next job.

#### Call graph summary (isolated job)

```
CronService.onTimer()
  └─ executeJobCore()
       └─ runIsolatedAgentJob({ job, message })   [via server-cron.ts]
            └─ runCronIsolatedAgentTurn()          [isolated-agent/run.ts]
                 ├─ resolveCronSession()            → session store lookup/create
                 ├─ resolveDeliveryTarget()         → channel + to resolution
                 ├─ build commandBody               → "[cron:<id> <name>] <message>\nNow: <time>"
                 ├─ runEmbeddedPiAgent()            → full LLM agent loop (see Ch.11)
                 │    ├─ system prompt + bootstrap files (AGENTS.md, SOUL.md, MEMORY.md, ...)
                 │    ├─ LLM call(s) with tool use
                 │    └─ final text payloads
                 ├─ pickLastNonEmptyTextFromPayloads()
                 └─ runSubagentAnnounceFlow()       → deliver to chat channel
                      └─ outbound channel adapter   → Telegram / WhatsApp / etc.
  └─ applyJobResult()                              → update nextRunAtMs, error backoff
  └─ appendCronRunLog()                            → ~/.openclaw/cron/runs/<jobId>.jsonl
  └─ armTimer()                                    → re-arm scheduler
```

---

### Cron job configuration options

#### `openclaw.json` global cron config

```json5
{
  cron: {
    enabled: true,                       // disable cron entirely
    store: "~/.openclaw/cron/jobs.json", // custom path for job store
    maxConcurrentRuns: 1,                // concurrent job limit (default: 1)
    webhookToken: "secret",             // bearer token for webhook deliveries
    webhook: "https://...",             // deprecated fallback for notify:true jobs
  }
}
```

Cron can also be disabled via env: `OPENCLAW_SKIP_CRON=1`.

#### Per-job overrides

| Field | Description |
|---|---|
| `payload.model` | Override the model for this job only (e.g. `"opus"`, `"anthropic/claude-haiku-3-5"`) |
| `payload.thinking` | Override thinking level: `off` / `minimal` / `low` / `medium` / `high` / `xhigh` |
| `payload.timeoutSeconds` | Job-level timeout in seconds (0 = no timeout) |
| `schedule.staggerMs` | Override the stagger window (0 = exact timing) |
| `deleteAfterRun` | One-shot jobs default to `true`; set `false` to keep |
| `delivery.bestEffort` | If `true`, delivery failures are logged but do not fail the job |
| `agentId` | Pin the job to a specific agent (multi-agent setups) |

#### Session reuse vs. fresh session

Each isolated job runs in session key `cron:<jobId>`. By default, OpenClaw uses the "direct" freshness policy:
- If the last run for that job was recent enough (within the configured idle timeout), the **same `sessionId`** is reused — the LLM would see prior cron conversation history.
- In practice most cron jobs fire infrequently enough that the session has expired, so each run starts with a fresh context window.

The bootstrap files (`AGENTS.md`, `MEMORY.md`, recent `memory/YYYY-MM-DD.md`) are always re-injected regardless of session reuse, providing persistent memory to the isolated run.

#### Heartbeat vs. cron: decision guide

| Use case | Recommended |
|---|---|
| One-shot reminder ("in 20 minutes") | `cron --at`, `sessionTarget: main` |
| Exact-time recurring task ("every Monday 9 AM") | `cron --cron`, `sessionTarget: isolated` |
| Periodic monitoring batched with other checks | Heartbeat (`HEARTBEAT.md`) |
| Task needing a different model or heavy thinking | `cron` isolated with `model` + `thinking` override |
| Task that should not clutter main session history | `cron` isolated |
| Task that needs full main-session context | Heartbeat or `cron` main with `systemEvent` |
