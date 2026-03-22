#!/usr/bin/env bash
#
# Send a WhatsApp message via the local whatsapp_client HTTP API.
# API key: -k/--api-key, then WHATSAPP_SENDER_API_KEY, then API_KEY from .env next to this script.
#
# Usage:
#   ./send-whatsapp.sh -n <digits> -m <message> [-u <baseUrl>] [-k <apiKey>]
#   ./send-whatsapp.sh --number 4915111111111 --message "Hello"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

NUMBER=""
MESSAGE=""
BASE_URL="${BASE_URL:-http://127.0.0.1:3000}"
API_KEY="${WHATSAPP_SENDER_API_KEY:-}"

usage() {
  cat <<'EOF'
Send a WhatsApp message through the whatsapp_client REST API.

Usage:
  ./send-whatsapp.sh -n <digits-only> -m <text> [-u <url>] [-k <key>]
  ./send-whatsapp.sh --number <digits> --message <text> [--base-url <url>] [--api-key <key>]

Options:
  -n, --number     Target phone number, digits only (no +); must be in ALLOWED_NUMBERS.
  -m, --message    Message body to send.
  -u, --base-url   API root URL (default: http://127.0.0.1:3000, or env BASE_URL).
  -k, --api-key    x-api-key header. Else WHATSAPP_SENDER_API_KEY, else API_KEY from .env beside this script.
  -h, --help       Show this help.

Prerequisites:
  - whatsapp_client is running (node index.js).
  - curl and node on PATH; .env with API_KEY if not using -k / env.

Example:
  ./send-whatsapp.sh -n '4915111111111' -m 'Hello from Bash!'
EOF
}

# Read KEY=value from .env (skip blanks/comments; strip optional quotes).
dotenv_get() {
  local file="$1" want="$2" line k v
  [[ -f "$file" ]] || return 1
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line#"${line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"
    [[ -z "$line" || "$line" == \#* ]] && continue
    if [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
      k="${BASH_REMATCH[1]}"
      v="${BASH_REMATCH[2]}"
      v="${v#"${v%%[![:space:]]*}"}"
      v="${v%"${v##*[![:space:]]}"}"
      if [[ ${#v} -ge 2 ]]; then
        local f="${v:0:1}" l="${v: -1}"
        if [[ ( "$f" == '"' && "$l" == '"' ) || ( "$f" == "'" && "$l" == "'" ) ]]; then
          v="${v:1:${#v}-2}"
        fi
      fi
      if [[ "$k" == "$want" ]]; then
        printf '%s' "$v"
        return 0
      fi
    fi
  done <"$file"
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n)
      NUMBER="${2:-}"
      shift 2
      ;;
    --number)
      NUMBER="${2:-}"
      shift 2
      ;;
    -m)
      MESSAGE="${2:-}"
      shift 2
      ;;
    --message)
      MESSAGE="${2:-}"
      shift 2
      ;;
    -u)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    -k)
      API_KEY="${2:-}"
      shift 2
      ;;
    --api-key)
      API_KEY="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "${NUMBER// }" || -z "$MESSAGE" ]]; then
  usage >&2
  exit 1
fi

NUMBER="${NUMBER//[[:space:]]/}"

if [[ -z "${API_KEY// }" ]]; then
  if v="$(dotenv_get "$ENV_FILE" "API_KEY" 2>/dev/null)"; then
    API_KEY="$v"
  fi
fi

if [[ -z "${API_KEY// }" ]]; then
  echo "Missing API key. Pass -k/--api-key, set WHATSAPP_SENDER_API_KEY, or set API_KEY in .env next to this script (${ENV_FILE})." >&2
  exit 1
fi

BASE_URL="${BASE_URL%/}"
URL="${BASE_URL}/send"

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required but not found on PATH." >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "node is required (for JSON encoding) but not found on PATH." >&2
  exit 1
fi

PAYLOAD="$(node -e "console.log(JSON.stringify({ number: process.argv[1], message: process.argv[2] }))" "$NUMBER" "$MESSAGE")"

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

HTTP_CODE="$(
  curl -sS -o "$TMP" -w '%{http_code}' -X POST "$URL" \
    -H "Content-Type: application/json; charset=utf-8" \
    -H "x-api-key: ${API_KEY}" \
    -d "$PAYLOAD"
)"

BODY="$(cat "$TMP")"

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "Request failed (HTTP ${HTTP_CODE}): ${BODY}" >&2
  exit 1
fi

if node -e "const b=JSON.parse(process.argv[1]); process.exit(b.success===true?0:1)" "$BODY" 2>/dev/null; then
  echo "OK: message queued/sent (success=true)."
else
  echo "API returned success=false or invalid JSON: ${BODY}" >&2
  exit 1
fi
