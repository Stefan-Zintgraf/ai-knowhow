# OpenClaw knowledge base

## Contents

1. [User systemd services: locations and lifecycle](#user-systemd-services-locations-and-lifecycle)
2. [Gateway service startup and lingering](#gateway-service-startup-and-lingering)
   - [OpenClaw gateway service via CLI](#openclaw-gateway-service-via-cli)
   - [Gateway install / uninstall behind the scenes (Linux systemd)](#gateway-install--uninstall-behind-the-scenes-linux-systemd)
   - [Repo script: `mele/user.systemd/openclaw_service.sh` (prep service, gateway drop-in, shell env)](#repo-script-meleusersystemdopenclaw_servicesh-prep-service-gateway-drop-in-shell-env)
3. [WebClaw](#webclaw)
   - [Repo script: `mele/user.systemd/webclaw_service.sh` (WebClaw as user service, after gateway)](#repo-script-meleusersystemdwebclaw_servicesh-webclaw-as-user-service-after-gateway)
4. [Gateway clients: concept, API, and use cases](#gateway-clients-concept-api-and-use-cases)
   - [What is a gateway client?](#what-is-a-gateway-client)
   - [Gateway WebSocket protocol](#gateway-websocket-protocol)
   - [Available RPC methods](#available-rpc-methods)
   - [Use cases beyond WebClaw](#use-cases-beyond-webclaw)

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

**`openclaw gateway uninstall`** (on Linux): (1) Runs `systemctl --user disable --now <unit>` — stops the service and removes the symlink from `default.target.wants/`. (2) Deletes the unit file `~/.config/systemd/user/openclaw-gateway[-<profile>].service`. The user’s systemd config dir and lingering are left unchanged.

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
     - Appends a block that sources `state-dir.sh` and a **conditional completion** line: only sources `$OPENCLAW_STATE_DIR/completions/openclaw.bash` when that file exists, avoiding “No such file or directory” when the CLI had previously pointed completions at `~/.openclaw`.

**Uninstall (`--uninstall` or `-u`):**

1. **Prep service** — `systemctl --user disable --now openclaw-gateway-prep.service`, then delete the prep unit file.
2. **Drop-in** — Remove `openclaw-gateway.service.d/10-state-env.conf` (and remove the drop-in directory if empty).
3. **Shell env** — Remove `~/.config/openclaw/state-dir.sh` and remove the state-dir and completion lines from `~/.profile`, `~/.bash_profile`, `~/.bashrc`, and `~/.zshrc`.
4. **daemon-reload** — So systemd forgets the prep unit and drop-in.

**Status (`--status` or `-s`):** Runs `systemctl --user status openclaw-gateway-prep.service`.

**Environment variables (summary):**

- **OPENCLAW_STATE_DIR** — Set by the gateway drop-in for the gateway process and by `state-dir.sh` for the CLI. Points to `mele/user.openclaw` (config dir: `openclaw.json`, `.env`, plugins under `examples/plugins/`, etc.). Path is derived at install time from the script’s directory.


## 3. WebClaw

- Download into specific folder:
  npx webclaw init ./user.webclaw

- **Run WebClaw as a user service (like the gateway):** Use **`mele/user.systemd/webclaw_service.sh`** to install a systemd user unit so WebClaw starts after the OpenClaw gateway. See [Repo script: webclaw_service.sh (WebClaw as user service, after gateway)](#repo-script-meleusersystemdwebclaw_servicesh-webclaw-as-user-service-after-gateway) below.

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

- **Browser shows "page didn’t load" / net::ERR_CONNECTION_REFUSED:** The dev server is not running or not reachable. (1) **Start the server first:** in a terminal, `cd user.webclaw && pnpm dev`; wait until Vite prints "ready" and the Local/Network URLs. (2) **Then** open in the browser the **exact** URL Vite shows (e.g. `http://localhost:3000/` or `http://127.0.0.1:3000/`). (3) If the browser is on a **different machine** than where you ran `pnpm dev`, use the **Network** URL Vite prints (e.g. `http://192.168.x.x:3000/`), not localhost. (4) Keep the terminal where `pnpm dev` runs open; closing it stops the server. Dev script uses `--host` so both local and network URLs work.

- **Diagnosing connection issues:** In Chrome, press **F12** → open the **Network** tab, then (re)load the page. Check the first request (the document to `localhost` or `127.0.0.1:3000`): a failed status (e.g. `(failed) net::ERR_CONNECTION_REFUSED`) means the dev server isn’t reachable; a successful document plus failed `/api/ping` points to gateway/credentials.

- **One-liner with token (and clean install):** To start the dev server with the gateway token in the environment: `CLAWDBOT_GATEWAY_TOKEN=<your_token> pnpm dev` (run from `user.webclaw`; or from repo root: `pnpm -C apps/webclaw exec -- env CLAWDBOT_GATEWAY_TOKEN=<your_token> pnpm dev`). For a **new, clean installation** create **`apps/webclaw/.env.local`** with at least `CLAWDBOT_GATEWAY_URL=ws://127.0.0.1:18789` and `CLAWDBOT_GATEWAY_TOKEN=<same value as OPENCLAW_GATEWAY_TOKEN in mele/user.openclaw/.env>`; copy the token from `mele/user.openclaw/.env` (variable `OPENCLAW_GATEWAY_TOKEN`). No other files need changing for a minimal setup.

### WebClaw as user service, 

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


## 4. Gateway clients: concept, API, and use cases

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


