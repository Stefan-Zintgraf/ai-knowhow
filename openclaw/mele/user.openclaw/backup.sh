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
# ~/.config/systemd/    User systemd units (gateway, GOG_KEYRING_PASSWORD, etc.)
# ~/.config/gogcli/     Google CLI (gog) config, credentials, keyring, gmail-watch
# ~/.config/gcloud/     Google Cloud SDK auth (excl. logs)
#
# -----------------------------------------------------------------------------
# Credentials-only (-cred or default): what is backed up
# -----------------------------------------------------------------------------
# $OPENCLAW_STATE_DIR/credentials/, .env, identity/, devices/, openclaw.json,
# exec-approvals.json, cron/, agents/, workspace-wolfgang/client_secret_gmail.json;
# ~/.config/openclaw/, systemd/, gogcli/, gcloud/
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
  # Full backup: .openclaw + .config/systemd, gogcli, gcloud
  ITEMS=(".openclaw")
  [ -d "$HOME/.config/systemd" ]  && ITEMS+=(".config/systemd")
  [ -d "$HOME/.config/gogcli" ]   && ITEMS+=(".config/gogcli")
  [ -d "$HOME/.config/gcloud" ]   && ITEMS+=(".config/gcloud")

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
fi

unset PASSWORD PASSWORD2 2>/dev/null

if [[ "$VERBOSE" -eq 1 ]]; then
  echo "Backup written: $OUT"
  ls -la "$OUT"
fi
