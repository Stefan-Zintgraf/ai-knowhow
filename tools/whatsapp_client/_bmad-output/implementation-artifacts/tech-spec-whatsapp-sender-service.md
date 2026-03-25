---
title: 'WhatsApp Sender Service'
slug: 'whatsapp-sender-service'
created: '2026-03-21'
status: 'completed'
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['Node.js 18+', 'Baileys (@whiskeysockets/baileys)', 'Express', 'dotenv', 'Jest', 'supertest']
files_to_modify: []
code_patterns: ['modular file structure', 'centralized config', 'reusable logging', 'separated route definitions']
test_patterns: ['Jest unit tests', 'Jest + supertest integration tests', 'E2E tests against live service', 'Jest --onlyFailures for rerun workflow']
---

# Tech-Spec: WhatsApp Sender Service

**Created:** 2026-03-21

## Overview

### Problem Statement

Need a simple, secure WhatsApp messaging tool that sends messages via a local REST API, restricted to a predefined list of recipients, with all configuration externalized in a `.env` file. Replaces an earlier prototype (HTML guides + bash script) with a clean, production-ready implementation.

### Solution

Node.js service using Baileys (WhatsApp Web API) + Express (local REST API) with `.env`-driven configuration, phone number allowlisting, daily rotating log files, and automatic log housekeeping. Runs as a systemd user service on Linux.

### Scope

**In Scope:**

- `index.js` — Baileys connection + Express API (`POST /send`) + file-based logging + daily housekeeping
- `.env` / `.env.example` — 8 config variables (API_KEY, PORT, ALLOWED_NUMBERS, AUTH_FOLDER, LOG_FILE, LOG_RETENTION_DAYS, RATE_LIMIT_PER_MINUTE, RATE_LIMIT_PER_NUMBER_PER_HOUR)
- `wa-sender.service` — systemd user service file
- `README.md` — setup guide, curl examples, config reference
- `package.json` — project manifest with dependencies
- Automated test suite (unit, integration, E2E)

**Out of Scope (planned for later stages — design for easy addition):**

- Multiple API routes beyond `POST /send`
- External/remote access (currently localhost only)
- Message queuing or retry logic
- Incoming message handling
- Web UI

## Context for Development

### Codebase Patterns

- **Greenfield project (confirmed clean slate)** — no existing code to maintain compatibility with
- Code must be structured for extensibility without over-engineering:
  - Express app setup separated from route definitions (easy to add routes later)
  - Baileys socket accessible to future modules (not buried in a closure)
  - Config loading centralized (easy to add new `.env` vars)
  - Logging as a reusable function (not inline calls everywhere)
- All code, comments, log messages, and API responses in English
- Node.js 18+ minimum (Baileys requirement), no version pinning — use whatever is installed

### Files to Create

| File | Purpose |
| ---- | ------- |
| `index.js` | Main entry point — starts Baileys, Express, housekeeping, graceful shutdown |
| `config.js` | Centralized `.env` loading and validation (exports `loadConfig()`) |
| `logger.js` | Reusable logging function + housekeeping (exports `createLogger()`) |
| `rate-limiter.js` | In-memory rate limiting (exports `createRateLimiter()`) |
| `routes/send.js` | POST /send route handler (separated for extensibility) |
| `.env.example` | Template with documented defaults (8 variables) |
| `.gitignore` | Ignore `.env`, `auth_info_sender/`, `logs/`, `node_modules/` |
| `package.json` | Dependencies and test scripts |
| `wa-sender.service` | systemd user service file |
| `README.md` | Setup guide, curl examples, config reference |
| `jest.config.js` | Jest config for unit + integration tests |
| `jest.e2e.config.js` | Jest config for E2E tests (separate) |
| `tests/unit/config.test.js` | Config validation tests |
| `tests/unit/logger.test.js` | Logging format and housekeeping tests |
| `tests/unit/rate-limiter.test.js` | Rate limiter tests |
| `tests/integration/send.test.js` | Express API route tests (mocked Baileys) |
| `tests/e2e/send-live.test.js` | Real message delivery test (requires paired session) |

### Files to Reference

| File | Purpose |
| ---- | ------- |
| Brainstorming session | `_bmad-output/brainstorming/brainstorming-session-2026-03-21-1017.md` — full design decisions |

### Technical Decisions

- **Sequential validation in handler** — API key check first, then phone number format, then allowlist check, then rate limit. No middleware (single-route app).
- **Bind to 127.0.0.1 only** — hardcoded, never configurable, never exposed externally.
- **Startup config validation** — fail fast with clear error if any required `.env` var is missing or invalid.
- **API key strength requirement** — minimum 32 characters. `.env.example` documents generating with `openssl rand -hex 32`.
- **Phone number format validation** — digits only, 7-15 characters. Validated both at config load (ALLOWED_NUMBERS entries) and at request time (incoming number field). Numbers coerced to string via `String()` before comparison.
- **Rate limiting** — in-memory rate limiter to protect WhatsApp account from ban. Global limit (`RATE_LIMIT_PER_MINUTE`, default 10) and per-number limit (`RATE_LIMIT_PER_NUMBER_PER_HOUR`, default 5). Returns 429 with clear error when exceeded.
- **Graceful shutdown** — SIGTERM/SIGINT handlers that close Baileys socket, stop Express server via `server.close()`, flush pending log writes, then `process.exit(0)`.
- **Connection state tracking** — track WhatsApp connection state separately from socket object. `getSocket()` returns socket only when state is `"open"`, otherwise returns null (triggers 503).
- **Reconnection with backoff** — on disconnect (except `DisconnectReason.loggedOut` from `@whiskeysockets/baileys`), wait 5 seconds then reconnect. Max 10 consecutive reconnect failures logs FATAL and exits (systemd restarts the process).
- **Auto-create directories** — app creates log dir and auth dir on startup if they don't exist.
- **Daily rotating logs** — files named `{LOG_FILE}-YYYY-MM-DD.log` (date in local system timezone). Log format: `[YYYY-MM-DD HH:mm:ss] EVENT target_number "first 200 chars"`. Housekeeping matches files by regex `-\d{4}-\d{2}-\d{2}\.log$` to extract date — unambiguous regardless of LOG_FILE containing hyphens.
- **Daily housekeeping** — `setInterval` (24h) + run at startup. Wrapped in try-catch — errors are logged but never crash the process. Deletes log files older than `LOG_RETENTION_DAYS`.
- **Consistent JSON responses** — all API responses: `{ success: bool, error?: string }`.
- **Explicit allowlist rejection** — 403 status with clear error message + logged as REJECTED event.

## Implementation Plan

### Tasks

- [x] Task 1: Initialize project and install dependencies
  - File: `package.json`
  - Action: Run `npm init -y`, then `npm install --save-exact @whiskeysockets/baileys express dotenv`, then `npm install --save-dev jest supertest`
  - Notes: Add npm scripts for test, test:failed, test:e2e. Set `"type": "commonjs"` (Baileys uses CommonJS). Use `--save-exact` for Baileys to pin the version (unofficial API, can break on updates). Do NOT install `pino` — use a no-op logger object for Baileys instead (see Task 5). Commit `package-lock.json` for reproducible installs.

- [x] Task 2: Create configuration module
  - File: `config.js`
  - Action: Create module that exports a `loadConfig()` function (not a static object — enables test isolation without `jest.resetModules()`). The function loads `.env` via `dotenv`, validates, and returns a config object. On validation failure, log the specific missing/invalid variable and call `process.exit(1)`.
  - Notes: Validation rules:
    - `API_KEY` — required, non-empty string, minimum 32 characters
    - `PORT` — optional, valid integer, default `3000`
    - `ALLOWED_NUMBERS` — required, non-empty comma-separated string, parsed into array of trimmed strings. Each entry validated: digits only, 7-15 characters (regex: `/^\d{7,15}$/`)
    - `AUTH_FOLDER` — optional, default `auth_info_sender`
    - `LOG_FILE` — optional, default `logs/wa-sender`
    - `LOG_RETENTION_DAYS` — optional, valid integer, default `7`
    - `RATE_LIMIT_PER_MINUTE` — optional, valid integer, default `10`
    - `RATE_LIMIT_PER_NUMBER_PER_HOUR` — optional, valid integer, default `5`
  - Export: `loadConfig()` returning `{ apiKey, port, allowedNumbers: string[], authFolder, logFile, logRetentionDays, rateLimitPerMinute, rateLimitPerNumberPerHour }`

- [x] Task 3: Create logging module
  - File: `logger.js`
  - Action: Create module that exports a `createLogger(config)` factory function returning `{ log, runHousekeeping }`.
  - Notes:
    - `log(event, targetNumber, message)` writes a line to `{LOG_FILE}-YYYY-MM-DD.log`: `[YYYY-MM-DD HH:mm:ss] EVENT target_number "first 200 chars of message"`
    - Timestamps use local system timezone
    - If `targetNumber` or `message` is null/undefined, omit from log line (for STARTUP, HOUSEKEEPING, FATAL events)
    - Auto-create log directory on first write if it doesn't exist (use `fs.mkdirSync` with `recursive: true`)
    - `runHousekeeping()` reads the log directory, matches files by regex `-\d{4}-\d{2}-\d{2}\.log$` to extract the date (last 14 chars before `.log`). Deletes files with dates older than `LOG_RETENTION_DAYS`. Logs a HOUSEKEEPING event with count of deleted files. **Entire function wrapped in try-catch** — errors are logged to console but never thrown (prevents crashing the process from setInterval).
    - Also write to `console.log` so systemd journal captures output too

- [x] Task 4: Create rate limiter module
  - File: `rate-limiter.js`
  - Action: Create simple in-memory rate limiter. Exports `createRateLimiter(config)` returning `{ checkLimit(number) }`. Returns `{ allowed: true }` or `{ allowed: false, reason: string }`.
  - Notes:
    - Track two counters: global messages per minute, per-number messages per hour
    - Use simple arrays of timestamps, pruned on each check (no external dependencies)
    - Global limit: `config.rateLimitPerMinute` (default 10) — across all numbers
    - Per-number limit: `config.rateLimitPerNumberPerHour` (default 5) — per recipient
    - Return descriptive reason: `"Global rate limit exceeded (max N/min)"` or `"Per-number rate limit exceeded for NUMBER (max M/hr)"`

- [x] Task 5: Create send route handler
  - File: `routes/send.js`
  - Action: Create module that exports a function `createSendRoute(getSocket, config, log, rateLimiter)` returning an Express router. The function receives a `getSocket` callback (returns current Baileys socket only when connection state is `"open"`, null otherwise), the config object, the log function, and the rate limiter.
  - Notes:
    - `POST /send` handler sequence:
      1. Check `x-api-key` header against `config.apiKey` — if mismatch, return `401 { success: false, error: "Unauthorized: invalid or missing API key" }`
      2. Extract `{ number, message }` from `req.body` — coerce number to string via `String(req.body.number)`. If either is missing or `message` is not a non-empty string, return `400 { success: false, error: "Missing required fields: number and message" }`
      3. Validate number format with regex `/^\d{7,15}$/` — if invalid, return `400 { success: false, error: "Invalid phone number format" }`
      4. Check `number` against `config.allowedNumbers` — if not found, log REJECTED event, return `403 { success: false, error: "Forbidden: number not in allowlist" }`
      5. Check rate limiter — if exceeded, log RATE_LIMITED event, return `429 { success: false, error: rateLimiter reason string }`
      6. Check socket is connected — if null (not open), return `503 { success: false, error: "WhatsApp connection not ready" }`
      7. Send message via `socket.sendMessage(number + "@s.whatsapp.net", { text: message })`
      8. Log SENT event, return `200 { success: true }`
      9. On error: log ERROR event, return `500 { success: false, error: "Internal server error" }`

- [x] Task 6: Create main entry point
  - File: `index.js`
  - Action: Create main script that wires everything together:
    1. Load config via `loadConfig()` (will exit if invalid)
    2. Create logger via `createLogger(config)`
    3. Create rate limiter via `createRateLimiter(config)`
    4. Auto-create auth directory if missing (`fs.mkdirSync` with `recursive: true`)
    5. Initialize Baileys connection with `useMultiFileAuthState(config.authFolder)`, `printQRInTerminal: true`, no-op logger object `{ info(){}, error(){}, warn(){}, debug(){}, trace(){}, child(){ return this } }` (replaces pino dependency)
    6. Handle `connection.update`:
       - Track connection state in a module-level `connectionState` variable (updated on every event)
       - On `connection === 'close'`: check `lastDisconnect?.error?.output?.statusCode` against `DisconnectReason.loggedOut` (import from `@whiskeysockets/baileys`). If logged out: log FATAL event, do NOT reconnect. If other reason: increment consecutive-failure counter, if counter > 10 log FATAL and `process.exit(1)` (let systemd restart). Otherwise wait 5 seconds (`setTimeout`) then call `connectToWhatsApp()` again.
       - On `connection === 'open'`: reset consecutive-failure counter to 0, log STARTUP event
    7. Handle `creds.update` — save credentials
    8. Store socket reference in module-level variable. `getSocket()` returns socket only if `connectionState === 'open'`, otherwise returns `null`
    9. Create Express app, `app.use(express.json({ limit: '16kb' }))`, mount send route
    10. Bind Express to `127.0.0.1` on `config.port`, store server reference for shutdown
    11. Run initial housekeeping, then `setInterval(runHousekeeping, 24 * 60 * 60 * 1000)`
    12. Log STARTUP event with count of allowed numbers
    13. Register graceful shutdown handlers for SIGTERM and SIGINT:
        - Close Baileys socket via `sock.end()` (if connected)
        - Stop Express via `server.close()`
        - Log SHUTDOWN event
        - `process.exit(0)`
  - Notes: Baileys socket variable must be accessible to the route handler via the `getSocket` callback pattern. On reconnect, update the socket reference. Import `DisconnectReason` from `@whiskeysockets/baileys`.

- [x] Task 7: Create .env.example
  - File: `.env.example`
  - Action: Create template file with all 8 variables, documented with comments:
    ```
    # WhatsApp Sender Configuration

    # API authentication key (required, minimum 32 characters)
    # Generate with: openssl rand -hex 32
    API_KEY=your-secret-key-here

    # Express server port (default: 3000)
    PORT=3000

    # Comma-separated list of allowed recipient phone numbers
    # International format, digits only, no + prefix (e.g. 4915111111111)
    ALLOWED_NUMBERS=4915111111111,4915122222222

    # Baileys session data folder (default: auth_info_sender)
    AUTH_FOLDER=auth_info_sender

    # Log file base path — app appends -YYYY-MM-DD.log (default: logs/wa-sender)
    LOG_FILE=logs/wa-sender

    # Days to keep log files before auto-deletion (default: 7)
    LOG_RETENTION_DAYS=7

    # Global rate limit: max messages per minute across all numbers (default: 10)
    RATE_LIMIT_PER_MINUTE=10

    # Per-number rate limit: max messages per hour to a single number (default: 5)
    RATE_LIMIT_PER_NUMBER_PER_HOUR=5
    ```

- [x] Task 8: Create .gitignore
  - File: `.gitignore`
  - Action: Create with entries: `.env`, `auth_info_sender/`, `logs/`, `node_modules/`

- [x] Task 9: Create systemd service file
  - File: `wa-sender.service`
  - Action: Create systemd user service unit file:
    ```ini
    [Unit]
    Description=WhatsApp Baileys Sender Service
    After=network.target

    [Service]
    Type=simple
    ExecStart=/usr/bin/node index.js
    WorkingDirectory=%h/wa-sender
    Restart=on-failure
    RestartSec=10
    StandardOutput=journal
    StandardError=journal

    [Install]
    WantedBy=default.target
    ```
  - Notes: Uses `%h` for home directory (systemd user service variable). User must adjust `WorkingDirectory` if installed elsewhere.

- [x] Task 10: Create Jest configuration
  - File: `jest.config.js`
  - Action: Create config that runs `tests/unit/**` and `tests/integration/**`, excludes `tests/e2e/**`
  - File: `jest.e2e.config.js`
  - Action: Create config that runs only `tests/e2e/**`, with longer timeout (30s)

- [x] Task 11: Create unit tests — config
  - File: `tests/unit/config.test.js`
  - Action: Test `config.js` by setting `process.env` then calling `loadConfig()` (function export — no module caching issues)
  - Test cases:
    - Valid config with all vars set — returns correct parsed object
    - Missing API_KEY — exits with error
    - API_KEY shorter than 32 chars — exits with error
    - Missing ALLOWED_NUMBERS — exits with error
    - Empty ALLOWED_NUMBERS — exits with error
    - ALLOWED_NUMBERS with non-digit entry (e.g. "49abc") — exits with error
    - ALLOWED_NUMBERS with too-short number (e.g. "123") — exits with error
    - Invalid PORT (non-numeric) — exits with error
    - Defaults applied: PORT=3000, AUTH_FOLDER=auth_info_sender, LOG_FILE=logs/wa-sender, LOG_RETENTION_DAYS=7, RATE_LIMIT_PER_MINUTE=10, RATE_LIMIT_PER_NUMBER_PER_HOUR=5
    - ALLOWED_NUMBERS parsed correctly: `"111222333,444555666"` → `["111222333","444555666"]`
    - ALLOWED_NUMBERS with spaces: `"111222333, 444555666 "` → `["111222333","444555666"]` (trimmed)
    - Rate limit values parsed correctly from env

- [x] Task 12: Create unit tests — logger
  - File: `tests/unit/logger.test.js`
  - Action: Test `logger.js` using temp directories via `createLogger(config)`
  - Test cases:
    - Log line format: `[YYYY-MM-DD HH:mm:ss] SENT 4915111111111 "Hello world"`
    - Message truncation: message over 200 chars is truncated to 200 in log
    - Event without target number: `[YYYY-MM-DD HH:mm:ss] STARTUP "Service started, 3 allowed numbers loaded"`
    - Log file created with correct date-stamped name
    - Log directory auto-created if missing
    - Housekeeping: create fake log files with old dates, run housekeeping, verify old ones deleted and recent ones kept
    - Housekeeping: empty log directory — no error, logs "Deleted 0 log files"
    - Housekeeping: exception during file deletion does not throw (try-catch works)
    - Housekeeping: LOG_FILE with hyphens (e.g. `my-wa-sender`) — date extraction uses regex `-\d{4}-\d{2}-\d{2}\.log$`, correctly identifies date portion

- [x] Task 13: Create unit tests — rate limiter
  - File: `tests/unit/rate-limiter.test.js`
  - Action: Test `rate-limiter.js` via `createRateLimiter(config)`
  - Test cases:
    - Under global limit — returns `{ allowed: true }`
    - Exceeds global limit (N+1 calls in same minute) — returns `{ allowed: false, reason: "..." }`
    - Under per-number limit — returns `{ allowed: true }`
    - Exceeds per-number limit (M+1 calls to same number in same hour) — returns `{ allowed: false, reason: "..." }`
    - Different numbers have independent per-number counters
    - Old timestamps are pruned (calls from >1 min ago don't count toward global limit)

- [x] Task 14: Create integration tests — send route
  - File: `tests/integration/send.test.js`
  - Action: Test Express app with supertest. Mock Baileys socket as a simple object with a `sendMessage` jest.fn(). Use a test config object directly (not from .env).
  - Test cases:
    - Valid request with correct API key + allowed number → 200 `{ success: true }`
    - Wrong API key → 401 `{ success: false, error: "Unauthorized..." }`
    - Missing API key header → 401 `{ success: false, error: "Unauthorized..." }`
    - Missing number field → 400 `{ success: false, error: "Missing required fields..." }`
    - Missing message field → 400 `{ success: false, error: "Missing required fields..." }`
    - Empty body → 400
    - Number as integer (not string) → still works (coerced to string)
    - Invalid phone number format (e.g. "hello", "49+151") → 400 `{ success: false, error: "Invalid phone number format" }`
    - Number not in allowlist → 403 `{ success: false, error: "Forbidden..." }` + REJECTED logged
    - Rate limit exceeded → 429 `{ success: false, error: "..." }` + RATE_LIMITED logged
    - Socket is null (not connected / not open) → 503 `{ success: false, error: "WhatsApp connection not ready" }`
    - Socket.sendMessage throws error → 500 `{ success: false, error: "Internal server error" }`
    - Verify sendMessage called with correct JID format: `number@s.whatsapp.net`
    - Verify all responses are JSON with `{ success, error? }` shape

- [x] Task 15: Create E2E tests
  - File: `tests/e2e/send-live.test.js`
  - Action: Test against a running live service instance. Reads API_KEY, PORT, and a test allowed number from `.env.test` or environment variables.
  - Test cases:
    - Send real message to an allowed number → 200 `{ success: true }`
    - Verify SENT entry appears in today's log file
    - Send to a non-allowed number → 403 (does not send)
  - Notes: Requires paired WhatsApp session. Test message should include a timestamp to identify test messages. Skip gracefully if service is not running.

- [x] Task 16: Create README
  - File: `README.md`
  - Action: Create documentation covering:
    - Project description (1-2 sentences)
    - Prerequisites (Node.js 18+)
    - Installation steps (`npm install`, copy `.env.example` to `.env`, configure)
    - First-time pairing (run `node index.js`, scan QR code)
    - Running as systemd service (copy service file, enable linger, enable + start)
    - API usage with curl examples (successful send, with API key header)
    - Configuration reference (table of all `.env` variables with defaults)
    - Testing (`npm test`, `npm run test:failed`, `npm run test:e2e`)
    - Log file location and format
    - Troubleshooting (common issues: wrong API key, number not in allowlist, connection lost)

## Acceptance Criteria

### Configuration

- [x] AC 1: Given a valid `.env` file with all required variables, when the app starts, then it loads config successfully and logs a STARTUP event with the count of allowed numbers
- [x] AC 2: Given a `.env` file missing `API_KEY`, when the app starts, then it exits immediately with a clear error message naming the missing variable
- [x] AC 3: Given a `.env` file missing `ALLOWED_NUMBERS`, when the app starts, then it exits immediately with a clear error message
- [x] AC 4: Given a `.env` file with `PORT` set to a non-numeric value, when the app starts, then it exits with a clear error message
- [x] AC 5: Given optional variables are not set, when the app starts, then defaults are applied (PORT=3000, AUTH_FOLDER=auth_info_sender, LOG_FILE=logs/wa-sender, LOG_RETENTION_DAYS=7)

### API Authentication

- [x] AC 6: Given a request with correct `x-api-key` header, when `POST /send` is called, then the request proceeds to validation
- [x] AC 7: Given a request with wrong or missing `x-api-key` header, when `POST /send` is called, then it returns 401 `{ success: false, error: "Unauthorized: invalid or missing API key" }`

### Allowlist

- [x] AC 8: Given a request to an allowed number, when `POST /send` is called, then the message is sent and a SENT event is logged
- [x] AC 9: Given a request to a number NOT in the allowlist, when `POST /send` is called, then it returns 403 `{ success: false, error: "Forbidden: number not in allowlist" }` and a REJECTED event is logged
- [x] AC 10: Given a request to a non-allowed number, when checking the log file, then the REJECTED entry includes the target number and first 200 chars of message

### Request Validation

- [x] AC 11: Given a request body missing `number`, when `POST /send` is called, then it returns 400 `{ success: false, error: "Missing required fields: number and message" }`
- [x] AC 12: Given a request body missing `message`, when `POST /send` is called, then it returns 400 with the same error

### Message Sending

- [x] AC 13: Given a valid request and a connected WhatsApp socket, when `POST /send` is called, then Baileys `sendMessage` is called with `{number}@s.whatsapp.net` and `{ text: message }`
- [x] AC 14: Given a valid request but the WhatsApp socket is not connected, when `POST /send` is called, then it returns 503 `{ success: false, error: "WhatsApp connection not ready" }`

### Logging

- [x] AC 15: Given any API event (SENT, REJECTED, ERROR), when the event occurs, then a log line is written to `{LOG_FILE}-YYYY-MM-DD.log` with format `[YYYY-MM-DD HH:mm:ss] EVENT target_number "first 200 chars"`
- [x] AC 16: Given a message longer than 200 characters, when logged, then only the first 200 characters appear in the log entry
- [x] AC 17: Given the log directory does not exist, when the first log event occurs, then the directory is created automatically

### Housekeeping

- [x] AC 18: Given log files older than `LOG_RETENTION_DAYS`, when housekeeping runs, then those files are deleted and a HOUSEKEEPING event is logged with the count
- [x] AC 19: Given the app starts, when initialization completes, then housekeeping runs immediately
- [x] AC 20: Given the app has been running, when 24 hours pass, then housekeeping runs again automatically

### Network Security

- [x] AC 21: Given the Express server starts, when checking the bind address, then it is bound to `127.0.0.1` only (not `0.0.0.0`)

### Directory Auto-Creation

- [x] AC 22: Given the auth folder does not exist, when the app starts, then it is created automatically
- [x] AC 23: Given the log directory does not exist, when the first log is written, then it is created automatically

### WhatsApp Connection

- [x] AC 24: Given the WhatsApp connection drops (not logged out), when the disconnect event fires, then the app automatically reconnects
- [x] AC 25: Given the WhatsApp session is logged out remotely, when the disconnect event fires, then the app logs the event and does NOT reconnect

### API Key Strength (F3)

- [x] AC 26: Given an API_KEY shorter than 32 characters in `.env`, when the app starts, then it exits with error "API_KEY must be at least 32 characters"

### Phone Number Format Validation (F4)

- [x] AC 27: Given an ALLOWED_NUMBERS entry with non-digit characters, when the app starts, then it exits with a clear error identifying the invalid number
- [x] AC 28: Given a request with `number: "hello"`, when `POST /send` is called, then it returns 400 `{ success: false, error: "Invalid phone number format" }`
- [x] AC 29: Given a request with `number: 4915111111111` (integer type), when `POST /send` is called, then the number is coerced to string and processed normally

### Rate Limiting (F1)

- [x] AC 30: Given more than `RATE_LIMIT_PER_MINUTE` requests within one minute, when `POST /send` is called, then it returns 429 `{ success: false, error: "Global rate limit exceeded..." }` and a RATE_LIMITED event is logged
- [x] AC 31: Given more than `RATE_LIMIT_PER_NUMBER_PER_HOUR` requests to the same number within one hour, when `POST /send` is called, then it returns 429 with per-number error and the message is NOT sent

### Graceful Shutdown (F2)

- [x] AC 32: Given the app receives SIGTERM, when the signal is handled, then the Baileys socket is closed, Express server is stopped, a SHUTDOWN event is logged, and the process exits cleanly
- [x] AC 33: Given the app receives SIGINT, when the signal is handled, then the same graceful shutdown sequence executes

### Connection State Tracking (F6)

- [x] AC 34: Given the Baileys socket exists but connection state is not "open" (e.g. reconnecting), when `POST /send` is called, then it returns 503 (not 500)

### Reconnection with Backoff (F5)

- [x] AC 35: Given the WhatsApp connection drops (not logged out), when the disconnect event fires, then the app waits 5 seconds before attempting reconnection
- [x] AC 36: Given 10 consecutive reconnection failures, when the 11th failure occurs, then the app logs a FATAL event and exits with non-zero code (letting systemd restart it)

### Housekeeping Robustness (F7, F8)

- [x] AC 37: Given housekeeping encounters a file deletion error, when the error occurs, then it is logged to console but does NOT crash the process
- [x] AC 38: Given LOG_FILE is set to `logs/my-wa-sender` (contains hyphens), when housekeeping runs, then it correctly identifies the date portion using regex and deletes only files older than retention period

### Response Format

- [x] AC 39: Given any API call to `POST /send`, when the response is returned, then it is always JSON with shape `{ success: boolean, error?: string }`

## Additional Context

### Dependencies

| Package | Purpose | Dev? |
|---|---|---|
| `@whiskeysockets/baileys` | WhatsApp Web API client (pin exact version with `--save-exact`) | No |
| `express` | HTTP server for REST API | No |
| `dotenv` | Load `.env` configuration | No |
| `jest` | Test framework | Yes |
| `supertest` | HTTP assertion library for Express | Yes |

**Note:** `pino` is NOT needed — Baileys accepts a no-op logger object instead (see Task 6).

### Testing Strategy

**Three-tier automated testing:**

| Tier | What | How | Mocking | Command |
|---|---|---|---|---|
| **Unit** | Config validation, allowlist logic, logging format, message truncation, housekeeping | Jest | File system via temp dirs | `npm test` |
| **Integration** | Express routes, API key auth, allowlist rejection, request validation, JSON response format | Jest + supertest | Baileys socket mocked | `npm test` |
| **E2E** | Real message delivery to an allowed number, verify API response + log entry | Jest hitting live service | None — real Baileys connection | `npm run test:e2e` |

**Failed-test-first workflow:**

1. `npm test` — full suite
2. On failure: `npm run test:failed` — reruns only failed tests (Jest `--onlyFailures`)
3. After fixes pass: `npm test` — full suite again to confirm no regressions

**npm scripts:**

```json
{
  "test": "jest",
  "test:failed": "jest --onlyFailures",
  "test:e2e": "jest --config jest.e2e.config.js"
}
```

**Not automatically testable:**

- QR code pairing (one-time manual step)

### Notes

**High-risk items:**

- Baileys is an unofficial WhatsApp API — WhatsApp could change their protocol at any time, breaking the library. Pin the Baileys version in `package.json` to avoid surprise breakage on `npm install`.
- Session data in `auth_info_sender/` is sensitive — must be gitignored and backed up separately.

**Future extensibility (out of scope, but architecture supports):**

- Adding routes: create new file in `routes/`, mount in `index.js`
- Adding config vars: add to `config.js` validation, update `.env.example`
- Adding message types (images, documents): extend the route handler's Baileys `sendMessage` call
- Remote access: change bind address + add HTTPS/reverse proxy (requires security review)
- Incoming messages: add Baileys `messages.upsert` event handler in `index.js`

## Review Notes

- Adversarial review completed
- Findings: 23 total, 10 real (fixed), 13 noise (skipped)
- Resolution approach: auto-fix
- Fixes applied:
  - F1: Timing-safe API key comparison (`crypto.timingSafeEqual`)
  - F2: Old socket event listener cleanup on reconnect
  - F3: Shutdown flag prevents reconnection during shutdown
  - F4: Reconnect-path `connectToWhatsApp` wrapped in try/catch
  - F5: Port range validation (1-65535), positive integer validation for rate limits and retention
  - F6: Log injection prevention (strip newlines/control chars from messages)
  - F7: Rate limit slots consumed only after successful send (split `checkLimit`/`recordUsage`)
  - F8: `unhandledRejection` and `uncaughtException` process handlers added
  - F9: `saveCreds` callback wrapped in try/catch
  - F10: Housekeeping only deletes files matching configured logName prefix
