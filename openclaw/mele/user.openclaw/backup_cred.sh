#!/usr/bin/env bash
# =============================================================================
# OpenClaw Credentials-Only Backup Script
# =============================================================================
# Creates a password-protected zip of credentials and auth-related data only
# (no workspace, no session logs, no deleteme). Use for credential backup
# alongside full backup.sh.
#
# Usage: ./backup_cred.sh [-h] [-v] [-n=NAME] [-pw=PASSWORD]
# Output: $HOME/openclaw-cred[-NAME]-YYYYMMDD-HHMMSS.zip
#
# -----------------------------------------------------------------------------
# What is backed up
# -----------------------------------------------------------------------------
#
# Path                              Contents
# --------------------------------  -------------------------------------------
# $OPENCLAW_STATE_DIR/credentials/  WhatsApp and other channel credentials
# $OPENCLAW_STATE_DIR/.env         Env vars (tokens, API keys)
# $OPENCLAW_STATE_DIR/identity/    Device auth
# $OPENCLAW_STATE_DIR/devices/     Paired/pending devices
# $OPENCLAW_STATE_DIR/openclaw.json  Config (tokens / substitution refs)
# $OPENCLAW_STATE_DIR/exec-approvals.json  Exec approval state
# $OPENCLAW_STATE_DIR/cron/        Cron jobs config
# $OPENCLAW_STATE_DIR/agents/*/agent/  Agent auth-profiles, models (excl. sessions)
# (Default OPENCLAW_STATE_DIR: ~/.openclaw)
#
# ~/.config/systemd/                User systemd units (gateway, env)
# ~/.config/gogcli/                 Google CLI config and keyring
# ~/.config/gcloud/                 Google Cloud SDK auth (excl. logs)
#
# -----------------------------------------------------------------------------
# Excluded
# -----------------------------------------------------------------------------
# - *deleteme* / *delete.me*  Any path containing deleteme or delete.me in name
# - .../agents/*/sessions/        Session logs
# - .../completions/               Generated
# - .../media/                     Ephemeral
# - .config/gcloud/logs/           Logs
# - */venv/*, */.venv/*            Virtual envs
# =============================================================================
set -e

usage() {
  echo "Usage: $0 [-h] [-v] [-n=NAME] [-pw=PASSWORD]"
  echo "  -h         show this help"
  echo "  -v         verbose (show backup path and ls)"
  echo "  -n=NAME    optional name suffix (e.g. -n=wolfgang)"
  echo "  -pw=PASS   use PASS as backup password (otherwise you will be prompted)"
  echo ""
  echo "Writes: \$HOME/openclaw-cred[-NAME]-YYYYMMDD-HHMMSS.zip"
}

VERBOSE=0
NAME=""
for arg in "$@"; do
  if [[ "$arg" == -h || "$arg" == --help ]]; then
    usage
    exit 0
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
OUT="$HOME/openclaw-cred${NAME_SUFFIX}-$(date +%Y%m%d-%H%M%S).zip"

STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"

# Path prefix for state in archive: relative to $HOME when under $HOME, else absolute
if [[ "$STATE_DIR" == "$HOME" ]]; then
  STATE_PREFIX="."
elif [[ "$STATE_DIR" == "$HOME"/* ]]; then
  STATE_PREFIX="${STATE_DIR#$HOME/}"
else
  STATE_PREFIX="$STATE_DIR"
fi

# Build list of credential-related paths (no deleteme). OpenClaw state from STATE_DIR.
ITEMS=()
[[ -d "$STATE_DIR/credentials" ]]   && ITEMS+=("$STATE_PREFIX/credentials")
[[ -f "$STATE_DIR/.env" ]]          && ITEMS+=("$STATE_PREFIX/.env")
[[ -d "$STATE_DIR/identity" ]]      && ITEMS+=("$STATE_PREFIX/identity")
[[ -d "$STATE_DIR/devices" ]]        && ITEMS+=("$STATE_PREFIX/devices")
[[ -f "$STATE_DIR/openclaw.json" ]] && ITEMS+=("$STATE_PREFIX/openclaw.json")
[[ -f "$STATE_DIR/exec-approvals.json" ]] && ITEMS+=("$STATE_PREFIX/exec-approvals.json")
[[ -d "$STATE_DIR/cron" ]]          && ITEMS+=("$STATE_PREFIX/cron")
[[ -d "$STATE_DIR/agents" ]]        && ITEMS+=("$STATE_PREFIX/agents")
[[ -d "$HOME/.config/systemd" ]]    && ITEMS+=(".config/systemd")
[[ -d "$HOME/.config/gogcli" ]]     && ITEMS+=(".config/gogcli")
[[ -d "$HOME/.config/gcloud" ]]     && ITEMS+=(".config/gcloud")

[[ ${#ITEMS[@]} -eq 0 ]] && { echo "No credential paths found. Aborting." >&2; exit 1; }

# Exclude deleteme/delete.me (anywhere in path) and other non-credential paths. Run from HOME so state and .config paths resolve.
(cd "$HOME" && zip -q -r -P "$PASSWORD" "$OUT" "${ITEMS[@]}" \
  -x "*deleteme*" \
  -x "*delete.me*" \
  -x "$STATE_PREFIX/agents/*/sessions/*" \
  -x "$STATE_PREFIX/completions/*" \
  -x "$STATE_PREFIX/media/*" \
  -x ".config/gcloud/logs/*" \
  -x "*/venv/*" \
  -x "*/.venv/*")

unset PASSWORD PASSWORD2 2>/dev/null

echo "Backup written: $OUT"
if [[ "$VERBOSE" -eq 1 ]]; then
  ls -la "$OUT"
fi
