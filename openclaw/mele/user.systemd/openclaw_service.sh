#!/usr/bin/env bash
# Install or uninstall the OpenClaw gateway prep user systemd service and
# a drop-in for the gateway so it uses mele/user.openclaw/.env and
# OPENCLAW_STATE_DIR (not ~/.openclaw). The prep service runs Tailscale
# funnel/rebind before the gateway. Enables lingering so user services
# run without login.
#
# Use alongside the OpenClaw CLI–installed gateway unit. On install, if the
# gateway is already running it is stopped/disabled, then re-enabled/started
# after the drop-in is in place so it picks up the correct environment.
#
# Same CLI options as openclaw_gateway_service.sh.
#
# After updating this script, refresh with: $0 --uninstall && $0 --install
# or: $0 --install --force

set -e

PREP_UNIT_NAME=openclaw-gateway-prep.service
GATEWAY_UNIT_NAME=openclaw-gateway.service
SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
MELE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
STATE_DIR="${MELE_DIR}/user.openclaw"
USER_UNITS_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
PREP_UNIT_PATH="${USER_UNITS_DIR}/${PREP_UNIT_NAME}"
GATEWAY_DROPIN_DIR="${USER_UNITS_DIR}/${GATEWAY_UNIT_NAME}.d"
DROPIN_FILE="${GATEWAY_DROPIN_DIR}/10-state-env.conf"
OPENCLAW_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/openclaw"
STATE_DIR_SNIPPET="${OPENCLAW_CONFIG_DIR}/state-dir.sh"
PROFILE_FILE="${HOME}/.profile"

usage() {
  echo "Usage: $0 --install|-i [--force|-f] | --uninstall|-u | --status|-s"
  echo "  --install, -i     Install prep service and gateway drop-in (correct .env and OPENCLAW_STATE_DIR); enable lingering. If gateway is running, stop then re-enable/start after."
  echo "  --force, -f       With --install: overwrite existing prep unit and drop-in (use after updating this script)."
  echo "  --uninstall, -u   Remove the prep service and the gateway drop-in; disable prep."
  echo "  --status, -s      Show prep service status (systemctl --user status)."
}

ensure_linger() {
  local user="${USER:-${LOGNAME:-$(id -un)}}"
  local linger
  linger=$(loginctl show-user "$user" -p Linger --value 2>/dev/null) || true
  if [[ "$linger" != "yes" ]]; then
    echo "Enabling lingering for user $user (user services will run without login)."
    sudo loginctl enable-linger "$user"
  fi
}

# Remove old OPENCLAW_STATE_DIR / state-dir / completion lines, then add state-dir source and correct completion line.
add_state_dir_and_completions_to_file() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  grep -v "OPENCLAW_STATE_DIR=" "$f" \
    | grep -v "openclaw/state-dir.sh" \
    | grep -v "OpenClaw CLI: use same state dir" \
    | grep -v "OpenClaw bash completions" \
    | grep -v ".openclaw/completions/openclaw.bash" \
    | grep -v 'OPENCLAW_STATE_DIR/completions/openclaw.bash' \
    > "${f}.openclaw.tmp" || true
  mv "${f}.openclaw.tmp" "$f"
  if ! grep -q "openclaw/state-dir.sh" "$f"; then
    echo "" >> "$f"
    echo "# OpenClaw CLI: use same state dir as gateway service (openclaw_service.sh)" >> "$f"
    printf '[ -f "%s" ] && . "%s"\n' "$STATE_DIR_SNIPPET" "$STATE_DIR_SNIPPET" >> "$f"
  fi
  if ! grep -q 'OPENCLAW_STATE_DIR/completions/openclaw.bash' "$f"; then
    echo "# OpenClaw bash completions (when state dir is set and completions exist)" >> "$f"
    printf '[ -n "$OPENCLAW_STATE_DIR" ] && [ -f "$OPENCLAW_STATE_DIR/completions/openclaw.bash" ] && . "$OPENCLAW_STATE_DIR/completions/openclaw.bash"\n' >> "$f"
  fi
  echo "Shell env: OPENCLAW_STATE_DIR + completions in $f → $STATE_DIR_SNIPPET"
}

# Write OPENCLAW_STATE_DIR snippet and ensure profile + rc files source it and use correct completions.
install_state_dir_env() {
  mkdir -p "$OPENCLAW_CONFIG_DIR"
  cat > "$STATE_DIR_SNIPPET" << EOF
# OpenClaw CLI state dir (managed by openclaw_service.sh — do not edit)
export OPENCLAW_STATE_DIR="${STATE_DIR}"
EOF
  if [[ ! -f "$PROFILE_FILE" ]] && [[ -f "${HOME}/.bash_profile" ]]; then
    PROFILE_FILE="${HOME}/.bash_profile"
  fi
  [[ -f "$PROFILE_FILE" ]] || touch "$PROFILE_FILE"
  add_state_dir_and_completions_to_file "$PROFILE_FILE"
  [[ -f "${HOME}/.bashrc" ]] && add_state_dir_and_completions_to_file "${HOME}/.bashrc"
  [[ -f "${HOME}/.zshrc" ]] && add_state_dir_and_completions_to_file "${HOME}/.zshrc"
}

# Remove state-dir snippet and its source/completion lines from profile and rc files.
uninstall_state_dir_env() {
  if [[ -f "$STATE_DIR_SNIPPET" ]]; then
    rm -f "$STATE_DIR_SNIPPET"
    echo "Removed $STATE_DIR_SNIPPET"
  fi
  for pf in "${HOME}/.profile" "${HOME}/.bash_profile" "${HOME}/.bashrc" "${HOME}/.zshrc"; do
    if [[ -f "$pf" ]]; then
      if grep -q "openclaw/state-dir.sh" "$pf" 2>/dev/null || grep -q "OpenClaw CLI: use same state dir" "$pf" 2>/dev/null || grep -q "openclaw.bash" "$pf" 2>/dev/null || grep -q "OPENCLAW_STATE_DIR/completions" "$pf" 2>/dev/null; then
        grep -v "openclaw/state-dir.sh" "$pf" \
          | grep -v "OpenClaw CLI: use same state dir" \
          | grep -v "OpenClaw bash completions" \
          | grep -v ".openclaw/completions/openclaw.bash" \
          | grep -v 'OPENCLAW_STATE_DIR/completions/openclaw.bash' \
          > "${pf}.openclaw.tmp"
        mv "${pf}.openclaw.tmp" "$pf"
        echo "Removed OPENCLAW_STATE_DIR and completions from $pf"
      fi
    fi
  done
}

install_service() {
  local force="${1:-}"
  if [[ -f "$PREP_UNIT_PATH" ]] && [[ "$force" != "--force" && "$force" != "-f" ]]; then
    echo "Prep service already installed: $PREP_UNIT_PATH exists. Use --force to overwrite." >&2
    exit 1
  fi
  mkdir -p "$USER_UNITS_DIR"

  # If gateway is running, stop and disable so drop-in is picked up on re-enable
  local gateway_was_running=0
  if systemctl --user is-active --quiet "$GATEWAY_UNIT_NAME" 2>/dev/null; then
    gateway_was_running=1
    echo "Gateway is running; stopping and disabling so drop-in will apply."
    systemctl --user stop "$GATEWAY_UNIT_NAME" 2>/dev/null || true
    systemctl --user disable "$GATEWAY_UNIT_NAME" 2>/dev/null || true
  fi

  # Prep service unit
  cat > "$PREP_UNIT_PATH" << 'EOF'
[Unit]
Description=OpenClaw Gateway prep (Tailscale funnel/rebind)
Before=openclaw-gateway.service

[Service]
Type=oneshot
ExecStart=-/usr/bin/tailscale funnel --bg --set-path /gmail-pubsub --yes 8788
ExecStart=-/usr/bin/curl -s -X POST --unix-socket /var/run/tailscale/tailscaled.sock http://local-tailscaled.sock/localapi/v0/debug?action=rebind
RemainAfterExit=yes

[Install]
WantedBy=default.target
EOF
  chmod 644 "$PREP_UNIT_PATH"

  # Drop-in: gateway uses mele/user.openclaw/.env and OPENCLAW_STATE_DIR (not ~/.openclaw)
  mkdir -p "$GATEWAY_DROPIN_DIR"
  cat > "$DROPIN_FILE" << EOF
[Service]
# Use repo state dir and .env (allows OpenClaw CLI–installed gateway unit)
EnvironmentFile=${STATE_DIR}/.env
Environment=OPENCLAW_STATE_DIR=${STATE_DIR}
EOF
  chmod 644 "$DROPIN_FILE"

  systemctl --user daemon-reload
  systemctl --user enable "$PREP_UNIT_NAME"
  echo "Installed and enabled: $PREP_UNIT_NAME (runs before openclaw-gateway.service)"
  echo "Drop-in added: $DROPIN_FILE (gateway will use ${STATE_DIR}/.env and OPENCLAW_STATE_DIR)"

  if [[ "$gateway_was_running" -eq 1 ]]; then
    echo "Re-enabling and starting gateway so it uses the new environment."
    systemctl --user enable "$GATEWAY_UNIT_NAME" 2>/dev/null || true
    systemctl --user start "$GATEWAY_UNIT_NAME" 2>/dev/null || true
  fi

  ensure_linger
  install_state_dir_env
}

uninstall_service() {
  if [[ -f "$PREP_UNIT_PATH" ]]; then
    systemctl --user disable --now "$PREP_UNIT_NAME" 2>/dev/null || true
    rm -f "$PREP_UNIT_PATH"
    echo "Uninstalled: removed $PREP_UNIT_PATH"
  else
    echo "Prep service not installed: $PREP_UNIT_PATH does not exist."
  fi
  if [[ -f "$DROPIN_FILE" ]]; then
    rm -f "$DROPIN_FILE"
    echo "Removed drop-in: $DROPIN_FILE"
  fi
  if [[ -d "$GATEWAY_DROPIN_DIR" ]] && [[ -z "$(ls -A "$GATEWAY_DROPIN_DIR" 2>/dev/null)" ]]; then
    rmdir "$GATEWAY_DROPIN_DIR" 2>/dev/null || true
  fi
  uninstall_state_dir_env
  systemctl --user daemon-reload 2>/dev/null || true
}

status_service() {
  systemctl --user status "$PREP_UNIT_NAME"
}

case "${1:-}" in
  --install|-i)   install_service "${2:-}" ;;
  --uninstall|-u) uninstall_service ;;
  --status|-s)    status_service ;;
  *)             usage >&2; exit 1 ;;
esac
