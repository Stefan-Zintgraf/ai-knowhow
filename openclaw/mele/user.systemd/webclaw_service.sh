#!/usr/bin/env bash
# Install or uninstall the WebClaw app as a user systemd service. WebClaw
# starts after the OpenClaw gateway is running (After=openclaw-gateway.service).
# Uses the same pattern as openclaw_service.sh: paths derived from script location.
#
# Prerequisites:
# - OpenClaw gateway installed and enabled (openclaw gateway install).
# - Lingering enabled for the user (openclaw_service.sh --install does this).
# - apps/webclaw/.env.local exists with CLAWDBOT_GATEWAY_URL and CLAWDBOT_GATEWAY_TOKEN.
#
# Usage: $0 --install|-i [--force|-f] | --uninstall|-u | --status|-s | --log|-l [journalctl args]

set -e

WEBCLAW_UNIT_NAME=openclaw-webclaw.service
SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
MELE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WEBCLAW_DIR="${MELE_DIR}/user.webclaw"
USER_UNITS_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
WEBCLAW_UNIT_PATH="${USER_UNITS_DIR}/${WEBCLAW_UNIT_NAME}"
ENV_FILE="${WEBCLAW_DIR}/apps/webclaw/.env.local"
GATEWAY_UNIT_NAME=openclaw-gateway.service
NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

# Ensure XDG_RUNTIME_DIR and DBUS_SESSION_BUS_ADDRESS are set so that
# systemctl --user / journalctl --user work in SSH sessions and cron.
ensure_systemd_env() {
  if [[ -z "${XDG_RUNTIME_DIR:-}" ]]; then
    export XDG_RUNTIME_DIR="/run/user/$(id -u)"
  fi
  if [[ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]] && [[ -S "${XDG_RUNTIME_DIR}/bus" ]]; then
    export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"
  fi
}

ensure_systemd_env

usage() {
  echo "Usage: $0 --install|-i [--force|-f] | --uninstall|-u | --status|-s | --log|-l [journalctl args]"
  echo "  --install, -i     Install, enable and start WebClaw user service (starts after openclaw-gateway.service)."
  echo "  --force, -f       With --install: overwrite existing unit."
  echo "  --uninstall, -u   Disable and remove the WebClaw user service."
  echo "  --status, -s      Show WebClaw service status (systemctl --user status)."
  echo "  --log, -l         Show recent journal output. Extra args passed to journalctl (e.g. -f to follow, -n 200)."
}

resolve_pnpm() {
  local pnpm_bin
  pnpm_bin="$(command -v pnpm 2>/dev/null)" || true
  if [[ -z "$pnpm_bin" ]] && [[ -s "${NVM_DIR}/nvm.sh" ]]; then
    pnpm_bin="$(bash -c "export NVM_DIR=\"${NVM_DIR}\"; . \"\${NVM_DIR}/nvm.sh\"; command -v pnpm" 2>/dev/null)" || true
  fi
  if [[ -z "$pnpm_bin" ]]; then
    echo "Error: pnpm not found in PATH or via nvm (${NVM_DIR}). Install pnpm and retry." >&2
    exit 1
  fi
  echo "$pnpm_bin"
}

install_service() {
  local force="${1:-}"
  if [[ ! -d "$WEBCLAW_DIR" ]]; then
    echo "Error: WebClaw directory not found: $WEBCLAW_DIR" >&2
    exit 1
  fi
  if [[ ! -f "$ENV_FILE" ]]; then
    echo "Warning: $ENV_FILE not found. Create it with CLAWDBOT_GATEWAY_URL and CLAWDBOT_GATEWAY_TOKEN so WebClaw can connect to the gateway." >&2
  fi
  if [[ -f "$WEBCLAW_UNIT_PATH" ]] && [[ "$force" != "--force" && "$force" != "-f" ]]; then
    echo "WebClaw service already installed: $WEBCLAW_UNIT_PATH exists. Use --force to overwrite." >&2
    exit 1
  fi

  local pnpm_bin node_bin_dir
  pnpm_bin="$(resolve_pnpm)"
  node_bin_dir="$(dirname "$pnpm_bin")"
  echo "Resolved pnpm: $pnpm_bin"

  mkdir -p "$USER_UNITS_DIR"

  cat > "$WEBCLAW_UNIT_PATH" << EOF
[Unit]
Description=WebClaw dev server (OpenClaw web UI)
After=${GATEWAY_UNIT_NAME}
Wants=${GATEWAY_UNIT_NAME}

[Service]
Type=simple
WorkingDirectory=${WEBCLAW_DIR}
EnvironmentFile=-${ENV_FILE}
Environment=PATH=${node_bin_dir}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=HOME=${HOME}
ExecStart=${pnpm_bin} dev
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF
  chmod 644 "$WEBCLAW_UNIT_PATH"
  echo "Unit file written: $WEBCLAW_UNIT_PATH"

  systemctl --user daemon-reload
  systemctl --user enable "$WEBCLAW_UNIT_NAME"
  echo "Enabled: $WEBCLAW_UNIT_NAME"

  # Stop any previous instance, then start fresh
  systemctl --user stop "$WEBCLAW_UNIT_NAME" 2>/dev/null || true
  systemctl --user start "$WEBCLAW_UNIT_NAME"
  echo "Started: $WEBCLAW_UNIT_NAME"

  echo "  Starts after: $GATEWAY_UNIT_NAME"
  echo "  Env file: $ENV_FILE"
  echo "  pnpm: $pnpm_bin"

  # Wait for Vite to bind the port, then show initial logs
  echo ""
  echo "Waiting for port 3000..."
  local tries=0
  while [[ $tries -lt 15 ]]; do
    if ss -tlnp 2>/dev/null | grep -q ':3000 '; then
      echo "Port 3000 is listening."
      break
    fi
    sleep 1
    tries=$((tries + 1))
  done
  if [[ $tries -ge 15 ]]; then
    echo "Warning: port 3000 not listening after 15 s — check logs below."
  fi

  echo ""
  echo "--- Recent logs ---"
  journalctl --user -u "$WEBCLAW_UNIT_NAME" -n 20 --no-pager
  echo ""
  echo "Follow logs: $0 --log -f"
}

uninstall_service() {
  systemctl --user disable --now "$WEBCLAW_UNIT_NAME" 2>/dev/null || true
  if [[ -f "$WEBCLAW_UNIT_PATH" ]]; then
    rm -f "$WEBCLAW_UNIT_PATH"
    echo "Uninstalled: removed $WEBCLAW_UNIT_PATH"
  else
    echo "WebClaw service not installed: $WEBCLAW_UNIT_PATH does not exist."
  fi
  systemctl --user daemon-reload 2>/dev/null || true
}

status_service() {
  systemctl --user status "$WEBCLAW_UNIT_NAME"
}

log_service() {
  if [[ $# -eq 0 ]]; then
    exec journalctl --user -u "$WEBCLAW_UNIT_NAME" -n 50 --no-pager
  else
    exec journalctl --user -u "$WEBCLAW_UNIT_NAME" "$@"
  fi
}

case "${1:-}" in
  --install|-i)   install_service "${2:-}" ;;
  --uninstall|-u) uninstall_service ;;
  --status|-s)    status_service ;;
  --log|-l)       shift; log_service "$@" ;;
  *)              usage >&2; exit 1 ;;
esac
