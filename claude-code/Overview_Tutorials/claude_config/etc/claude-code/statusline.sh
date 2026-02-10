#!/bin/bash

# ==============================================================================
# Claude Code Statusline Script
# ==============================================================================
# Displays: Workspace | Model | TokensUsed/Total [Progress] Percentage | Cost
# Toggle DEBUG below to enable/disable JSON logging to /tmp/claude-statusline-*
# ==============================================================================

# DEBUG MODE: Set to 1 to enable JSON logging, 0 to disable
DEBUG=0

# Maximum length for workspace path before truncation
MAX_WORKSPACE_LEN=40

# Read session data from stdin
SESSION_DATA=$(cat)

# --- DEBUG LOGGING ---
if [ "$DEBUG" -eq 1 ]; then
    # Save raw JSON to temporary files
    # Latest JSON snapshot (overwrites each time)
    echo "$SESSION_DATA" > /tmp/claude-statusline-latest.json

    # Historical log with timestamps (appends)
    {
        echo "=== $(date '+%Y-%m-%d %H:%M:%S') ==="
        echo "$SESSION_DATA"
        echo ""
    } >> /tmp/claude-statusline-history.log
fi

# --- JSON PARSING ---
# Try to use jq if available, otherwise fall back to grep/sed
if command -v jq &> /dev/null; then
    # Use jq for robust JSON parsing
    MODEL=$(echo "$SESSION_DATA" | jq -r '.model.display_name // "unknown"')
    WORKSPACE=$(echo "$SESSION_DATA" | jq -r '.workspace.current_dir // .cwd // ""')
    WINDOW_SIZE=$(echo "$SESSION_DATA" | jq -r '.context_window.context_window_size // 200000')
    CURRENT_INPUT=$(echo "$SESSION_DATA" | jq -r '.context_window.current_usage.input_tokens // 0')
    CACHE_CREATE=$(echo "$SESSION_DATA" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
    CACHE_READ=$(echo "$SESSION_DATA" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')
    SESSION_COST=$(echo "$SESSION_DATA" | jq -r '.cost.total_cost_usd // 0')
else
    # Fallback to grep/sed (less reliable but works without jq)
    MODEL=$(echo "$SESSION_DATA" | grep -o '"display_name":"[^"]*"' | head -1 | sed 's/"display_name":"\([^"]*\)"/\1/')

    # Try to extract workspace from current_dir first, fallback to cwd
    WORKSPACE=$(echo "$SESSION_DATA" | grep -o '"current_dir":"[^"]*"' | head -1 | sed 's/"current_dir":"\([^"]*\)"/\1/')
    [ -z "$WORKSPACE" ] && WORKSPACE=$(echo "$SESSION_DATA" | grep -o '"cwd":"[^"]*"' | head -1 | sed 's/"cwd":"\([^"]*\)"/\1/')

    WINDOW_SIZE=$(echo "$SESSION_DATA" | grep -o '"context_window_size":[0-9]*' | sed 's/"context_window_size"://')

    # Extract from context_window.current_usage by finding the right section
    CURRENT_USAGE=$(echo "$SESSION_DATA" | grep -o '"current_usage":{[^}]*"input_tokens":[0-9]*[^}]*"cache_creation_input_tokens":[0-9]*[^}]*"cache_read_input_tokens":[0-9]*[^}]*}')
    CURRENT_INPUT=$(echo "$CURRENT_USAGE" | grep -o '"input_tokens":[0-9]*' | sed 's/"input_tokens"://')
    CACHE_CREATE=$(echo "$CURRENT_USAGE" | grep -o '"cache_creation_input_tokens":[0-9]*' | sed 's/"cache_creation_input_tokens"://')
    CACHE_READ=$(echo "$CURRENT_USAGE" | grep -o '"cache_read_input_tokens":[0-9]*' | sed 's/"cache_read_input_tokens"://')

    SESSION_COST=$(echo "$SESSION_DATA" | grep -o '"total_cost_usd":[0-9.]*' | head -1 | sed 's/"total_cost_usd"://')
fi

# Set defaults if values are empty
[ -z "$MODEL" ] && MODEL="unknown"
[ -z "$WORKSPACE" ] && WORKSPACE="~"
[ -z "$CURRENT_INPUT" ] && CURRENT_INPUT=0
[ -z "$CACHE_CREATE" ] && CACHE_CREATE=0
[ -z "$CACHE_READ" ] && CACHE_READ=0
[ -z "$WINDOW_SIZE" ] && WINDOW_SIZE=200000
[ -z "$SESSION_COST" ] && SESSION_COST=0

# --- WORKSPACE FORMATTING ---
# Truncate workspace path if too long, showing trailing portion
if [ ${#WORKSPACE} -gt $MAX_WORKSPACE_LEN ]; then
    # Calculate how many characters to keep from the end
    KEEP_LEN=$((MAX_WORKSPACE_LEN - 3))  # Reserve 3 chars for "..."
    # Extract the trailing portion
    WORKSPACE_DISPLAY="...${WORKSPACE: -$KEEP_LEN}"
else
    WORKSPACE_DISPLAY="$WORKSPACE"
fi

# --- CALCULATIONS ---
# Calculate current context usage (matches what /context shows)
TOKENS_USED=$((CURRENT_INPUT + CACHE_CREATE + CACHE_READ))

# If tokens_used is very low (< 1000), we're probably at startup before first API call
# Estimate initial context: ~3k system prompt + ~16k system tools + ~1k MCP tools = ~20k
if [ "$TOKENS_USED" -lt 1000 ]; then
    TOKENS_USED=20000
fi

# Calculate percentage
PERCENTAGE=$(awk "BEGIN {printf \"%.1f\", ($TOKENS_USED/$WINDOW_SIZE)*100}")

# Format tokens in k (thousands)
TOKENS_USED_K=$(awk "BEGIN {printf \"%.0f\", $TOKENS_USED/1000}")
TOKENS_TOTAL_K=$(awk "BEGIN {printf \"%.0f\", $WINDOW_SIZE/1000}")

# Format session cost
COST_FORMATTED=$(awk "BEGIN {printf \"%.2f\", $SESSION_COST}")

# Create progress bar (10 characters wide)
FILLED=$(awk "BEGIN {printf \"%.0f\", ($TOKENS_USED/$WINDOW_SIZE)*10}")
BAR=""
for i in {1..10}; do
    if [ "$i" -le "$FILLED" ]; then
        BAR="${BAR}█"
    else
        BAR="${BAR}░"
    fi
done

# --- OUTPUT ---
# Color codes:
# \033[1;34m = blue bold (workspace)
# \033[1;36m = cyan bold (model)
# \033[1;32m = green bold (tokens/percentage)
# \033[1;33m = yellow bold (progress bar)
# \033[1;35m = magenta bold (cost)
# \033[0m = reset
echo -e "\033[1;34m${WORKSPACE_DISPLAY}\033[0m | \033[1;36m${MODEL}\033[0m | \033[1;32m${TOKENS_USED_K}k/${TOKENS_TOTAL_K}k\033[0m [\033[1;33m${BAR}\033[0m] \033[1;32m${PERCENTAGE}%\033[0m | \033[1;35m\$${COST_FORMATTED}\033[0m"
