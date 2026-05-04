#!/usr/bin/env sh
# Optional E2E smoke: gateway preflight, then RAG + Qdrant health, minimal index/retrieve.
# Requires: curl, RAG on 8080, Qdrant on 6333, tokens in env, RAG built with the same RAG_CONFIG.
# This profile is local Ollama via LiteLLM only — do not set allow_remote: true in the
# documented LiteLLM file for this smoke.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
export RAG_CONFIG="${RAG_CONFIG:-config.e2e.yaml}"
python3 scripts/e2e_gateway_preflight.py || exit 1

E2E_RAG_BASE_URL="${E2E_RAG_BASE_URL:-http://127.0.0.1:8080}"
QDRANT_URL="${E2E_QDRANT_URL:-http://127.0.0.1:6333}"
ST="${RAG_SERVICE_TOKEN:-}"
AD="${RAG_ADMIN_TOKEN:-}"
if [ -z "$ST" ] || [ -z "$AD" ]; then
  echo "set RAG_SERVICE_TOKEN and RAG_ADMIN_TOKEN" >&2
  exit 1
fi

i=0
while [ "$i" -lt 30 ]; do
  if curl -sf "$QDRANT_URL/collections" >/dev/null; then break; fi
  i=$((i + 1))
  sleep 1
done
curl -sf "$QDRANT_URL/collections" >/dev/null || { echo "Qdrant not reachable at $QDRANT_URL" >&2; exit 1; }

i=0
while [ "$i" -lt 30 ]; do
  if curl -sf -H "Authorization: Bearer $ST" "$E2E_RAG_BASE_URL/rag/health" >/dev/null; then break; fi
  i=$((i + 1))
  sleep 1
done
curl -sf -H "Authorization: Bearer $ST" "$E2E_RAG_BASE_URL/rag/health" >/dev/null || {
  echo "RAG not reachable at $E2E_RAG_BASE_URL/rag/health" >&2
  exit 1
}

curl -sf -X POST -H "Authorization: Bearer $AD" -H "Content-Type: application/json" \
  -d '{"docs":[{"id":"smoke-1","text":"hello smoke","metadata":{}}]}' \
  "$E2E_RAG_BASE_URL/rag/index/kb" >/dev/null
curl -sf -X POST -H "Authorization: Bearer $ST" -H "Content-Type: application/json" \
  -d '{"query":"hello","top_k":2}' \
  "$E2E_RAG_BASE_URL/rag/retrieve" | python3 -c "import json,sys; d=json.load(sys.stdin); assert 'chunks' in d" \
  || { echo "retrieve JSON missing chunks" >&2; exit 1; }
echo "smoke_allow_remote OK"
