#!/usr/bin/env bash
# Install or uninstall the WhatsApp client (tools/whatsapp_client) as a user
# systemd service. Starts after the OpenClaw gateway is running
# (After=openclaw-gateway.service). Paths are derived from this script's
# location (same pattern as webclaw_service.sh).
#
# Prerequisites:
# - OpenClaw gateway installed (optional but matches WebClaw ordering).
# - Lingering enabled if you want the service without login (openclaw_service.sh --install does this).
# - In tools/whatsapp_client: npm install, and .env from .env.example (API_KEY, ALLOWED_NUMBERS, etc.).
# - Pair WhatsApp once with `node index.js` (no --server); the unit uses --server and exits if unpaired.
# - Generated unit: RestartSec=30 (min delay between restarts); StartLimitIntervalSec=300 + StartLimitBurst=5
#   caps rapid restart storms (use systemctl --user reset-failed after fixing unpaired state).
#
# Usage: $0 --install|-i [--force|-f] | --uninstall|-u | --status|-s | --log|-l [journalctl args]

set -e

WHATSAPP_UNIT_NAME=openclaw-whatsapp-client.service
SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
WHATSAPP_DIR="${REPO_ROOT}/tools/whatsapp_client"
USER_UNITS_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
WHATSAPP_UNIT_PATH="${USER_UNITS_DIR}/${WHATSAPP_UNIT_NAME}"
ENV_FILE="${WHATSAPP_DIR}/.env"
GATEWAY_UNIT_NAME=openclaw-gateway.service
NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

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
  echo "  --install, -i     Install, enable and start WhatsApp client user service (starts after ${GATEWAY_UNIT_NAME})."
  echo "  --force, -f       With --install: overwrite existing unit."
  echo "  --uninstall, -u   Disable and remove the WhatsApp client user service."
  echo "  --status, -s      Show service status (systemctl --user status)."
  echo "  --log, -l         Show recent journal output. Extra args passed to journalctl (e.g. -f to follow, -n 200)."
}

resolve_node() {
  local node_bin
  node_bin="$(command -v node 2>/dev/null)" || true
  if [[ -z "$node_bin" ]] && [[ -s "${NVM_DIR}/nvm.sh" ]]; then
    node_bin="$(bash -c "export NVM_DIR=\"${NVM_DIR}\"; . \"\${NVM_DIR}/nvm.sh\"; command -v node" 2>/dev/null)" || true
  fi
  if [[ -z "$node_bin" ]]; then
    echo "Error: node not found in PATH or via nvm (${NVM_DIR}). Install Node.js and retry." >&2
    exit 1
  fi
  echo "$node_bin"
}

install_service() {
  local force="${1:-}"
  if [[ ! -d "$WHATSAPP_DIR" ]]; then
    echo "Error: WhatsApp client directory not found: $WHATSAPP_DIR" >&2
    exit 1
  fi
  if [[ ! -f "${WHATSAPP_DIR}/index.js" ]]; then
    echo "Error: ${WHATSAPP_DIR}/index.js not found." >&2
    exit 1
  fi
  if [[ ! -d "${WHATSAPP_DIR}/node_modules" ]]; then
    echo "Warning: ${WHATSAPP_DIR}/node_modules missing. Run: (cd \"$WHATSAPP_DIR\" && npm install)" >&2
  fi
  if [[ ! -f "$ENV_FILE" ]]; then
    echo "Warning: $ENV_FILE not found. Copy .env.example to .env and set API_KEY, ALLOWED_NUMBERS, etc." >&2
  fi
  if [[ -f "$WHATSAPP_UNIT_PATH" ]] && [[ "$force" != "--force" && "$force" != "-f" ]]; then
    echo "WhatsApp client service already installed: $WHATSAPP_UNIT_PATH exists. Use --force to overwrite." >&2
    exit 1
  fi

  local node_bin node_bin_dir
  node_bin="$(resolve_node)"
  node_bin_dir="$(dirname "$node_bin")"
  echo "Resolved node: $node_bin"

  mkdir -p "$USER_UNITS_DIR"

  cat > "$WHATSAPP_UNIT_PATH" << EOF
[Unit]
Description=WhatsApp client (Baileys HTTP API) for OpenClaw
After=${GATEWAY_UNIT_NAME}
Wants=${GATEWAY_UNIT_NAME}
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple
WorkingDirectory=${WHATSAPP_DIR}
EnvironmentFile=-${ENV_FILE}
Environment=PATH=${node_bin_dir}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=HOME=${HOME}
Environment=WHATSAPP_SERVICE_MODE=1
ExecStart=${node_bin} index.js --server
Restart=on-failure
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF
  chmod 644 "$WHATSAPP_UNIT_PATH"
  echo "Unit file written: $WHATSAPP_UNIT_PATH"

  systemctl --user daemon-reload
  systemctl --user enable "$WHATSAPP_UNIT_NAME"
  echo "Enabled: $WHATSAPP_UNIT_NAME"

  systemctl --user stop "$WHATSAPP_UNIT_NAME" 2>/dev/null || true
  systemctl --user start "$WHATSAPP_UNIT_NAME"
  echo "Started: $WHATSAPP_UNIT_NAME"

  echo "  Starts after: $GATEWAY_UNIT_NAME"
  echo "  Env file: $ENV_FILE"
  echo "  node: $node_bin"
  echo "  WorkingDirectory: $WHATSAPP_DIR"

  echo ""
  echo "--- Recent logs ---"
  journalctl --user -u "$WHATSAPP_UNIT_NAME" -n 20 --no-pager
  echo ""
  echo "Follow logs: $0 --log -f"
}

uninstall_service() {
  systemctl --user disable --now "$WHATSAPP_UNIT_NAME" 2>/dev/null || true
  if [[ -f "$WHATSAPP_UNIT_PATH" ]]; then
    rm -f "$WHATSAPP_UNIT_PATH"
    echo "Uninstalled: removed $WHATSAPP_UNIT_PATH"
  else
    echo "WhatsApp client service not installed: $WHATSAPP_UNIT_PATH does not exist."
  fi
  systemctl --user daemon-reload 2>/dev/null || true
}

status_service() {
  systemctl --user status "$WHATSAPP_UNIT_NAME"
}

log_service() {
  if [[ $# -eq 0 ]]; then
    exec journalctl --user -u "$WHATSAPP_UNIT_NAME" -n 50 --no-pager
  else
    exec journalctl --user -u "$WHATSAPP_UNIT_NAME" "$@"
  fi
}

case "${1:-}" in
  --install|-i)   install_service "${2:-}" ;;
  --uninstall|-u) uninstall_service ;;
  --status|-s)    status_service ;;
  --log|-l)       shift; log_service "$@" ;;
  *)              usage >&2; exit 1 ;;
esac
