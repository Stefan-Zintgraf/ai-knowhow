# WhatsApp Sender Service

A simple, secure WhatsApp messaging service that sends messages via a local REST API, restricted to a predefined list of recipients.

## Prerequisites

- Node.js 18+
- A WhatsApp account for pairing

## Installation

```bash
npm install
cp .env.example .env
# Edit .env — set API_KEY and ALLOWED_NUMBERS at minimum
```

Generate a secure API key:

```bash
# Linux / Git Bash / macOS
openssl rand -hex 32

# Windows PowerShell
-join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Max 256) })

# Windows CMD
powershell -command "-join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Max 256) })"
```

## First-Time Pairing

```bash
node index.js
```

Scan the QR code with WhatsApp on your phone (Linked Devices → Link a Device). Session data is saved in `auth_info_sender/` for subsequent starts.

## Running as a systemd Service (Linux)

```bash
cp wa-sender.service ~/.config/systemd/user/
# Edit WorkingDirectory in the service file if needed
loginctl enable-linger $USER
systemctl --user enable wa-sender
systemctl --user start wa-sender
```

## API Usage

### Send a Message

```bash
curl -X POST http://127.0.0.1:3000/send \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"number": "4915111111111", "message": "Hello from the API!"}'
```

**Success response** (200):

```json
{ "success": true }
```

**Error responses** return `{ "success": false, "error": "..." }` with appropriate HTTP status codes (401, 400, 403, 429, 503, 500).

## Configuration Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `API_KEY` | Yes | — | API authentication key (min 32 characters) |
| `PORT` | No | `3000` | Express server port |
| `ALLOWED_NUMBERS` | Yes | — | Comma-separated allowed phone numbers (digits only, 7-15 chars) |
| `AUTH_FOLDER` | No | `auth_info_sender` | Baileys session data folder |
| `LOG_FILE` | No | `logs/wa-sender` | Log file base path (app appends `-YYYY-MM-DD.log`) |
| `LOG_RETENTION_DAYS` | No | `7` | Days to keep log files before auto-deletion |
| `RATE_LIMIT_PER_MINUTE` | No | `10` | Global max messages per minute |
| `RATE_LIMIT_PER_NUMBER_PER_HOUR` | No | `5` | Max messages per hour to a single number |

## Testing

```bash
# Run unit + integration tests
npm test

# Rerun only failed tests
npm run test:failed

# Run E2E tests (requires running service + paired session)
npm run test:e2e
```

## Log Format

Log files are written to `{LOG_FILE}-YYYY-MM-DD.log`:

```
[2026-03-21 14:30:00] SENT 4915111111111 "Hello from the API!"
[2026-03-21 14:30:05] REJECTED 4915199999999 "Unauthorized message attempt"
[2026-03-21 00:00:00] HOUSEKEEPING "Deleted 3 log files"
```

## Troubleshooting

- **401 Unauthorized** — Check that the `x-api-key` header matches `API_KEY` in `.env`
- **403 Forbidden** — The target number is not in `ALLOWED_NUMBERS`
- **503 Not Ready** — WhatsApp is not connected. Check if the session needs re-pairing
- **429 Rate Limited** — Too many messages sent. Wait and retry
- **Connection keeps dropping** — After 10 consecutive failures, the service exits and systemd restarts it. Check WhatsApp account status
