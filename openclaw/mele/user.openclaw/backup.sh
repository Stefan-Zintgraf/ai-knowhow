#!/usr/bin/env bash
# =============================================================================
# OpenClaw Backup Script
# =============================================================================
# Creates a password-protected zip. Two modes:
#   -full    Full backup: all config, credentials, sessions (last 3 per agent).
#   -cred    Credentials-only (default): credentials and auth-related data only.
#
# Usage: ./backup.sh [-full | -cred] [-h] [-v] [-n=NAME] [-pw=PASSWORD]
# Output: <script-dir>/openclaw[-NAME]-YYYYMMDD-HHMMSS.full.zip  (with -full)
#         <script-dir>/openclaw[-NAME]-YYYYMMDD-HHMMSS.cred.zip (with -cred or no option)
# (Script dir = directory containing backup.sh. Backup zip files are excluded from the backup.)
#
# -----------------------------------------------------------------------------
# Full backup (-full): what is backed up
# -----------------------------------------------------------------------------
# ~/.openclaw/          OpenClaw config, hooks, sessions (last 3/agent), workspace, workspace-wolfgang
# ~/.config/openclaw/  OpenClaw CLI state-dir.sh and related config (sources OPENCLAW_STATE_DIR)
# ~/.config/systemd/   User systemd units (gateway, gateway-prep, GOG_KEYRING_PASSWORD, etc.)
# ~/.config/gogcli/    Google CLI (gog) config, credentials, keyring, gmail-watch
# ~/.config/gcloud/    Google Cloud SDK auth (excl. logs)
# mele/user.webclaw/   WebClaw app (excl. node_modules, .git, dist, .turbo)
# mele/user.openclaw/examples/  Gateway client examples (excl. .venv, __pycache__)
# Shell/login files    ~/.bashrc, ~/.profile, ~/.bash_profile, ~/.zshrc, ~/.zshenv, ~/.zprofile
#                      (only if present; may contain OPENCLAW_STATE_DIR and completion sourcing)
#
# -----------------------------------------------------------------------------
# Credentials-only (-cred or default): what is backed up
# -----------------------------------------------------------------------------
# $OPENCLAW_STATE_DIR/credentials/, .env, identity/, devices/, openclaw.json,
# exec-approvals.json, cron/, agents/, workspace-wolfgang/client_secret_gmail.json;
# WebClaw: mele/user.webclaw/apps/webclaw/.env.local (CLAWDBOT_GATEWAY_*),
#          mele/user.webclaw/apps/webclaw/.device-keys.json (ed25519 device identity);
# Gateway client: mele/user.openclaw/examples/gateway_clients/claw_client/.env (OPENCLAW_GATEWAY_TOKEN);
# ~/.config/openclaw/, systemd/, gogcli/, gcloud/
# Shell/login files    ~/.bashrc, ~/.profile, ~/.bash_profile, ~/.zshrc, ~/.zshenv, ~/.zprofile
#                      (only if present; may contain OPENCLAW_STATE_DIR and completion sourcing)
# (Default OPENCLAW_STATE_DIR: ~/.openclaw)
#
# -----------------------------------------------------------------------------
# Always excluded: *deleteme* / *delete.me*, *.full.zip / *.cred.zip (backup outputs), venv, gcloud/logs, etc.
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  echo "Usage: $0 [-full | -cred] [-h] [-v] [-n=NAME] [-pw=PASSWORD]"
  echo "  -full      full backup (all content including credentials) → .full.zip"
  echo "  -cred      credentials-only backup (default) → .cred.zip"
  echo "  -h         show this help"
  echo "  -v         verbose (show backup path and ls)"
  echo "  -n=NAME    optional name suffix (e.g. -n=wolfgang)"
  echo "  -pw=PASS   use PASS as backup password (otherwise you will be prompted)"
  echo ""
  echo "Output: <script-dir>/openclaw[-NAME]-YYYYMMDD-HHMMSS.full.zip or .cred.zip"
}

VERBOSE=0
NAME=""
FULL=0
for arg in "$@"; do
  if [[ "$arg" == -h || "$arg" == --help ]]; then
    usage
    exit 0
  fi
  if [[ "$arg" == -full ]]; then
    FULL=1
  fi
  if [[ "$arg" == -cred ]]; then
    FULL=0
  fi
  if [[ "$arg" == -v ]]; then
    VERBOSE=1
  fi
  if [[ "$arg" == -n=* ]]; then
    NAME="${arg#-n=}"
  fi
done

PASSWORD=""
for arg in "$@"; do
  if [[ "$arg" == -pw=* ]]; then
    PASSWORD="${arg#-pw=}"
    break
  fi
done

if [[ -z "$PASSWORD" ]]; then
  read -rs -p "Password for backup: " PASSWORD
  echo
  if [[ -z "$PASSWORD" ]]; then
    echo "No password given. Aborting." >&2
    exit 1
  fi
  read -rs -p "Confirm password: " PASSWORD2
  echo
  if [[ "$PASSWORD" != "$PASSWORD2" ]]; then
    echo "Passwords do not match. Aborting." >&2
    exit 1
  fi
fi

NAME_SUFFIX="${NAME:+-$NAME}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
if [[ "$FULL" -eq 1 ]]; then
  OUT="$SCRIPT_DIR/openclaw${NAME_SUFFIX}-${TIMESTAMP}.full.zip"
else
  OUT="$SCRIPT_DIR/openclaw${NAME_SUFFIX}-${TIMESTAMP}.cred.zip"
fi

if [[ "$FULL" -eq 1 ]]; then
  # Full backup: .openclaw + .config/openclaw, systemd, gogcli, gcloud + shell/login files
  ITEMS=(".openclaw")
  [ -d "$HOME/.config/openclaw" ] && ITEMS+=(".config/openclaw")
  [ -d "$HOME/.config/systemd" ]  && ITEMS+=(".config/systemd")
  [ -d "$HOME/.config/gogcli" ]   && ITEMS+=(".config/gogcli")
  [ -d "$HOME/.config/gcloud" ]   && ITEMS+=(".config/gcloud")
  for f in .bashrc .profile .bash_profile .zshrc .zshenv .zprofile; do
    [ -f "$HOME/$f" ] && ITEMS+=("$f")
  done

  (cd "$HOME" && zip -q -r -P "$PASSWORD" "$OUT" "${ITEMS[@]}" \
    -x ".config/gcloud/logs/*" \
    -x ".openclaw/completions/*" \
    -x ".openclaw/media/inbound/*" \
    -x ".openclaw/agents/*/sessions/*.jsonl" \
    -x "*/venv/*" \
    -x "*/.venv/*" \
    -x "*deleteme*" \
    -x "*delete.me*" \
    -x "*.full.zip" \
    -x "*.cred.zip")

  # Re-add the 3 most recent session logs per agent
  for session_dir in "$HOME"/.openclaw/agents/*/sessions; do
    [ -d "$session_dir" ] || continue
    mapfile -t last3 < <(ls -t "$session_dir"/*.jsonl 2>/dev/null | head -3)
    for f in "${last3[@]}"; do
      (cd "$HOME" && zip -q -P "$PASSWORD" "$OUT" "${f#$HOME/}")
    done
  done

  # WebClaw installation (mele/user.webclaw, relative to script's parent mele/)
  MELE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
  if [[ -d "${MELE_DIR}/user.webclaw" ]]; then
    (cd "$MELE_DIR" && zip -q -r -P "$PASSWORD" "$OUT" user.webclaw \
      -x "user.webclaw/node_modules/*" \
      -x "user.webclaw/*/node_modules/*" \
      -x "user.webclaw/.git/*" \
      -x "user.webclaw/*/dist/*" \
      -x "user.webclaw/.turbo/*" \
      -x "user.webclaw/*/.turbo/*" \
      -x "*deleteme*" \
      -x "*delete.me*" \
      -x "*.full.zip" \
      -x "*.cred.zip")
  fi

  # examples/ (gateway clients, etc.) — relative to user.openclaw (SCRIPT_DIR)
  if [[ -d "$SCRIPT_DIR/examples" ]]; then
    (cd "$SCRIPT_DIR" && zip -q -r -P "$PASSWORD" "$OUT" examples \
      -x "examples/*/.venv/*" \
      -x "examples/*/venv/*" \
      -x "examples*/__pycache__/*" \
      -x "examples*/*.pyc" \
      -x "*deleteme*" \
      -x "*delete.me*" \
      -x "*.full.zip" \
      -x "*.cred.zip")
  fi
else
  # Credentials-only: same set as former backup_cred.sh
  STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
  if [[ "$STATE_DIR" == "$HOME" ]]; then
    STATE_PREFIX="."
  elif [[ "$STATE_DIR" == "$HOME"/* ]]; then
    STATE_PREFIX="${STATE_DIR#$HOME/}"
  else
    STATE_PREFIX="$STATE_DIR"
  fi

  ITEMS=()
  [[ -d "$STATE_DIR/credentials" ]]   && ITEMS+=("$STATE_PREFIX/credentials")
  [[ -f "$STATE_DIR/.env" ]]          && ITEMS+=("$STATE_PREFIX/.env")
  [[ -d "$STATE_DIR/identity" ]]     && ITEMS+=("$STATE_PREFIX/identity")
  [[ -d "$STATE_DIR/devices" ]]       && ITEMS+=("$STATE_PREFIX/devices")
  [[ -f "$STATE_DIR/openclaw.json" ]] && ITEMS+=("$STATE_PREFIX/openclaw.json")
  [[ -f "$STATE_DIR/exec-approvals.json" ]] && ITEMS+=("$STATE_PREFIX/exec-approvals.json")
  [[ -d "$STATE_DIR/cron" ]]          && ITEMS+=("$STATE_PREFIX/cron")
  [[ -d "$STATE_DIR/agents" ]]        && ITEMS+=("$STATE_PREFIX/agents")
  [[ -f "$STATE_DIR/workspace-wolfgang/client_secret_gmail.json" ]] && ITEMS+=("$STATE_PREFIX/workspace-wolfgang/client_secret_gmail.json")
  [[ -d "$HOME/.config/openclaw" ]]   && ITEMS+=(".config/openclaw")
  [[ -d "$HOME/.config/systemd" ]]    && ITEMS+=(".config/systemd")
  [[ -d "$HOME/.config/gogcli" ]]     && ITEMS+=(".config/gogcli")
  [[ -d "$HOME/.config/gcloud" ]]     && ITEMS+=(".config/gcloud")
  for f in .bashrc .profile .bash_profile .zshrc .zshenv .zprofile; do
    [[ -f "$HOME/$f" ]] && ITEMS+=("$f")
  done

  [[ ${#ITEMS[@]} -eq 0 ]] && { echo "No credential paths found. Aborting." >&2; exit 1; }

  (cd "$HOME" && zip -q -r -P "$PASSWORD" "$OUT" "${ITEMS[@]}" \
    -x "*deleteme*" \
    -x "*delete.me*" \
    -x "*.full.zip" \
    -x "*.cred.zip" \
    -x "$STATE_PREFIX/agents/*/sessions/*" \
    -x "$STATE_PREFIX/completions/*" \
    -x "$STATE_PREFIX/media/*" \
    -x ".config/gcloud/logs/*" \
    -x "*/venv/*" \
    -x "*/.venv/*")

  # WebClaw credentials (mele/user.webclaw/apps/webclaw/.env.local, .device-keys.json)
  MELE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
  WEBCLAW_ENV="${MELE_DIR}/user.webclaw/apps/webclaw/.env.local"
  if [[ -f "$WEBCLAW_ENV" ]]; then
    (cd "$MELE_DIR" && zip -q -r -P "$PASSWORD" "$OUT" user.webclaw/apps/webclaw/.env.local)
  fi
  WEBCLAW_KEYS="${MELE_DIR}/user.webclaw/apps/webclaw/.device-keys.json"
  if [[ -f "$WEBCLAW_KEYS" ]]; then
    (cd "$MELE_DIR" && zip -q -r -P "$PASSWORD" "$OUT" user.webclaw/apps/webclaw/.device-keys.json)
  fi

  # Gateway client credentials (examples/gateway_clients/claw_client/.env → OPENCLAW_GATEWAY_TOKEN)
  CLAW_CLIENT_ENV="$SCRIPT_DIR/examples/gateway_clients/claw_client/.env"
  if [[ -f "$CLAW_CLIENT_ENV" ]]; then
    (cd "$SCRIPT_DIR" && zip -q -P "$PASSWORD" "$OUT" examples/gateway_clients/claw_client/.env)
  fi
fi

unset PASSWORD PASSWORD2 2>/dev/null

if [[ "$VERBOSE" -eq 1 ]]; then
  echo "Backup written: $OUT"
  ls -la "$OUT"
fi
