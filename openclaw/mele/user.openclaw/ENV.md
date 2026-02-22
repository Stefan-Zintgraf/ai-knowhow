# Environment variables for openclaw.json

`openclaw.json.example` uses **env var substitution** (`${VAR_NAME}`) so you can commit the example and keep secrets out of the repo.

## Setup

1. Copy the example: `cp openclaw.json.example openclaw.json`
2. Set the variables below (e.g. in `~/.openclaw/.env`, or export in your shell/systemd).
3. OpenClaw substitutes them when loading config. Do **not** put real tokens in `openclaw.json` if you use this pattern.

## Variables referenced in the example

| Variable | Used in config | Purpose |
|----------|----------------|---------|
| `PERPLEXITY_API_KEY` | `tools.web.search.perplexity.apiKey` | Perplexity web search |
| `OPENCLAW_GATEWAY_TOKEN` | `gateway.auth.token` | Gateway API auth (also supported by OpenClaw as documented) |
| `OPENCLAW_HOOKS_TOKEN` | `hooks.token` | Webhook auth |
| `TELEGRAM_BOT_TOKEN` | `channels.telegram.botToken` (and per-account) | Telegram bot |
| `GMAIL_PUSH_TOKEN` | `hooks.gmail.pushToken` | Gmail Pub/Sub push subscription |
| `GMAIL_ACCOUNT` | `hooks.gmail.account` | Gmail address for the hook |
| `GCP_PROJECT_ID` | `hooks.gmail.topic` | Google Cloud project ID for Pub/Sub topic |

Optional: create `~/.openclaw/.env` with the same variable names; OpenClaw loads it (see [Environment Variables](https://docs.openclaw.ai/help/environment)).
