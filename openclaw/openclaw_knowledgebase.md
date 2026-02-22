# OpenClaw knowledge base

## Contents

1. [User systemd services: locations and lifecycle](#user-systemd-services-locations-and-lifecycle)
2. [Gateway service startup and lingering](#gateway-service-startup-and-lingering)
   - [OpenClaw gateway service via CLI](#openclaw-gateway-service-via-cli)
   - [Gateway install / uninstall behind the scenes (Linux systemd)](#gateway-install--uninstall-behind-the-scenes-linux-systemd)
   - [Repo script: `mele/user.systemd/openclaw_service.sh` (prep service, gateway drop-in, shell env)](#repo-script-meleusersystemdopenclaw_servicesh-prep-service-gateway-drop-in-shell-env)

---

## User systemd services: locations and lifecycle

**Filesystem:** User units live under `~/.config/systemd/user/` (primary); other search paths are `~/.local/share/systemd/user/` and `/etc/systemd/user/`. When you **enable** a unit (e.g. `systemctl --user enable openclaw-gateway.service`), systemd creates symlinks in a `*.target.wants/` directory (e.g. `~/.config/systemd/user/default.target.wants/openclaw-gateway.service` → `../openclaw-gateway.service`). Those symlinks define which services start with the target (e.g. default.target). **Disable** removes the symlinks; **start** / **stop** / **restart** affect the current run state only. Commands: `systemctl --user enable|disable|start|stop|restart|status <unit>`.

## Gateway service startup and lingering

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
