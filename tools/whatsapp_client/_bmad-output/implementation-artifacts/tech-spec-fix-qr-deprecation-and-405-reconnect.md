---
title: 'Fix QR deprecation warning and code-405 reconnect loop'
slug: 'fix-qr-deprecation-and-405-reconnect'
created: '2026-03-21'
status: 'completed'
# NOTE: stepsCompleted tracks spec authoring workflow steps (1=understand, 2=investigate, 3=generate, 4=review) — NOT implementation task completion
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['Node.js CJS', '@whiskeysockets/baileys 7.0.0-rc.9', 'express 5.2.1', 'jest 30']
files_to_modify: ['index.js', 'package.json', 'package-lock.json']
code_patterns: ['makeWASocket options object', 'connection.update event handler', 'log(LEVEL, null, message)']
test_patterns: ['jest unit/integration in tests/ — no existing tests for index.js connection logic']
---

# Tech-Spec: Fix QR deprecation warning and code-405 reconnect loop

**Created:** 2026-03-21

## Overview

### Problem Statement

Two bugs in `index.js`: (1) `makeWASocket` is called with `printQRInTerminal: true`, a deprecated option that triggers a console warning on every connection attempt; (2) disconnect code 405 ("Not Acceptable") is not handled as a non-retryable error — the reconnect loop retries up to 10 times even though 405 indicates WhatsApp has rejected the session credentials, making recovery impossible without re-pairing.

### Solution

Remove `printQRInTerminal: true` from `makeWASocket` options and add QR extraction from the `connection.update` event using `qrcode-terminal`. Add code 405 to the fatal-disconnect guard alongside the existing `loggedOut` (401) check.

### Scope

**In Scope:**
- Remove deprecated `printQRInTerminal` option from `makeWASocket` call
- Add QR display via `connection.update` using `qrcode-terminal`
- Treat disconnect code 405 as non-retryable (log FATAL + return, no reconnect)
- Add `qrcode-terminal` to `package.json` dependencies

**Out of Scope:**
- Serving QR over HTTP endpoint
- Changing reconnect delay or backoff logic
- Any other reconnect/connection changes

## Context for Development

### Codebase Patterns

- Single-file entry point: `index.js` — all connection logic lives here
- Logging via `log(level, null, message)` — existing levels: `STARTUP`, `RECONNECT`, `FATAL`, `ERROR`, `SHUTDOWN`
- `DisconnectReason` is imported from `@whiskeysockets/baileys` and used for `loggedOut` comparison
- `DisconnectReason` enum confirmed values: 401=loggedOut, 403=forbidden, 408=connectionLost/timedOut, 411=multideviceMismatch, 428=connectionClosed, 440=connectionReplaced, 500=badSession, 515=restartRequired. **Code 405 is NOT in the enum** — it is a raw HTTP-style status code from the Boom error (`lastDisconnect.error.output.statusCode`)
- `makeWASocket` options object at `index.js:45–49`; `printQRInTerminal: true` triggers warning at baileys `socket.js:25`
- `connection.update` handler at `index.js:51–99`; baileys emits `{ qr }` string via `ev.emit('connection.update', { qr })` at `socket.js:710`. Note: baileys also explicitly emits `{ qr: undefined }` after successful pairing and during reconnect — `if (qr)` correctly filters these since `undefined` is falsy
- No existing tests cover `index.js` connection logic — test coverage is on `routes/send`, `config`, `logger`, `rate-limiter`
- `qrcode-terminal` is NOT in node_modules — must be added as a production dependency

### Files to Reference

| File | Purpose |
| ---- | ------- |
| `index.js` | All code changes — makeWASocket options + connection.update handler |
| `package.json` | Add `qrcode-terminal` dependency |
| `package-lock.json` | Updated automatically by `npm install` |
| `node_modules/@whiskeysockets/baileys/lib/Types/index.js` | DisconnectReason enum source of truth (reference only) |
| `node_modules/@whiskeysockets/baileys/lib/Socket/socket.js` | QR emit and printQRInTerminal warning (reference only) |

### Technical Decisions

- **QR display**: Add `qrcode-terminal@0.12.0` as a production dependency. **License note:** npm registry reports the package as "Proprietary" but the GitHub source (gtanner/qrcode-terminal) is MIT-licensed — verify from GitHub before installing; if in doubt use `qrcode` (npm, definitively MIT) as fallback. In `connection.update`, if `update.qr` is present, call `qrcode.generate(update.qr, { small: true })` to render a scannable QR in the terminal.
- **Code 405 handling**: 405 is not in `DisconnectReason` but must be treated as non-retryable. Mirror the existing `loggedOut` pattern exactly: add `statusCode === 405` check immediately after the `loggedOut` check, log FATAL with message `"Session rejected by WhatsApp (code 405). Delete auth folder and re-pair."`, then `return`.
- **`printQRInTerminal`**: Remove the option entirely from `makeWASocket` call (omitting it defaults to `false` and eliminates the warning).

## Implementation Plan

### Tasks

- [x] Task 1: Verify `qrcode-terminal` license, then install
  - File: `package.json`, `package-lock.json`
  - Action: Check the GitHub repo (gtanner/qrcode-terminal) to confirm MIT license, then run `npm install qrcode-terminal@0.12.0` — adds to `dependencies` and updates lock file
  - Notes: Production dependency (needed at runtime). If license is unacceptable, substitute `qrcode` (MIT) — its API differs: use `require('qrcode').toString(str, { type: 'terminal', small: true }, (err, url) => console.log(url))`

- [x] Task 2: Add `qrcode-terminal` require at top of `index.js`
  - File: `index.js`
  - Action: Add `const qrcode = require('qrcode-terminal');` after the last existing `require()` statement and before the `const config = loadConfig();` call
  - Notes: **Must only be done after Task 1 completes.** Adding this require before the package is installed will crash the server on startup with `Error: Cannot find module 'qrcode-terminal'`

- [x] Task 3: Remove `printQRInTerminal: true` from `makeWASocket` options
  - File: `index.js`
  - Action: In the `makeWASocket` call at lines 45–49, remove the line `printQRInTerminal: true,`. Result should be:
    ```js
    sock = makeWASocket({
      auth: state,
      logger: noopLogger,
    });
    ```
  - Notes: Omitting the option is equivalent to `false`; this eliminates the deprecation warning

- [x] Task 4: Handle `update.qr` in the `connection.update` listener
  - File: `index.js`
  - Action: In the `connection.update` handler (starting at line 51), destructure `qr` from `update` and add a QR render block before the existing `if (connection !== undefined)` check:
    ```js
    sock.ev.on('connection.update', (update) => {
      const { connection, lastDisconnect, qr } = update;

      if (qr) {
        qrcode.generate(qr, { small: true });
      }

      if (connection !== undefined) {
        // ... existing code unchanged
    ```
  - Notes: baileys emits `{ qr: undefined }` explicitly during reconnects and after pairing — `if (qr)` correctly suppresses these since `undefined` is falsy

- [x] Task 5: Add code 405 as non-retryable disconnect reason
  - File: `index.js`
  - Action: In the `connection === 'close'` block, immediately after the existing `loggedOut` guard (currently at lines 64–67), add:
    ```js
    if (statusCode === 405) {
      log('FATAL', null, 'Session rejected by WhatsApp (code 405). Delete auth folder and re-pair.');
      return;
    }
    ```
  - Notes: Place this block directly after the `loggedOut` block so both non-retryable codes are grouped together at the top of the close handler

### Acceptance Criteria

- [x] AC 1: Given `makeWASocket` is called, when the server starts, then no deprecation warning about `printQRInTerminal` appears in the console

- [x] AC2: Given the server is not yet authenticated (no valid auth session), when a new QR is emitted by baileys via `connection.update`, then a scannable QR code is rendered in the terminal using `qrcode-terminal`

- [x] AC3: Given a valid QR is rendered and scanned successfully, when the connection opens, then no further QR codes are printed (this is passively guaranteed by baileys stopping QR emission after successful pairing)

- [x] AC4: Given the server is running with stale/invalid credentials, when WhatsApp closes the connection with status code 405, then a FATAL log message is emitted with text containing "405" and "re-pair", and no reconnect attempt is made

- [x] AC5: Given a 405 disconnect occurs, when shutdown is not in progress, then `consecutiveFailures` is NOT incremented and the reconnect `setTimeout` is NOT called

- [x] AC6: Given a non-405, non-loggedOut disconnect (e.g. 428), when the connection closes, then the existing reconnect logic fires normally (behavior unchanged)

## Additional Context

### Dependencies

- `qrcode-terminal@0.12.0` npm package — new production dependency. Verify MIT license from GitHub (gtanner/qrcode-terminal) before installing; npm registry metadata reports "Proprietary" which may be a metadata error.
- No other external dependencies. No API or data dependencies.

### Testing Strategy

No new automated tests — connection logic in `index.js` has no unit test infrastructure and adding it is out of scope. Run `npm test` after implementation to confirm no regressions in existing tests.

**Guided manual test sequence (run after implementation, with human in the loop):**

**Phase 1 — Regression check**
1. Run `npm test` — all existing tests must pass

**Phase 2 — No deprecation warning (AC 1)**
1. Start the server: `node index.js`
2. Observe startup output
3. **Pass:** No line containing `printQRInTerminal` warning appears
4. **Fail:** Warning still appears → Task 3 not applied correctly

**Phase 3 — QR display (AC 2 & 3)**
1. Delete or rename `auth_info_sender/` folder to force fresh pairing
2. Start the server: `node index.js`
3. **Pass:** A QR code graphic renders in the terminal (block characters, scannable with WhatsApp)
4. **Fail — no QR appears:** Task 4 not applied; check `update.qr` destructuring
5. **Fail — raw string instead of graphic:** `qrcode-terminal` not installed or wrong API call
6. Scan the QR with WhatsApp on your phone
7. **Pass:** Connection opens, `STARTUP "WhatsApp connection established"` logged, no further QR printed
8. **Fail — QR keeps printing:** Guard `if (qr)` may be triggering repeatedly

**Phase 4 — Code 405 non-retryable (AC 4 & 5)**

> Note: SIGINT cannot be used to trigger this path — the shutdown handler calls `sock.ev.removeAllListeners()` and sets `isShuttingDown = true` before any `connection.update` close event fires, so the 405 guard would never be reached. The only reliable way to exercise this path is a genuine WhatsApp-initiated 405 close.

Approach A — Observe in production (preferred):
1. Deploy the fix with stale credentials that previously produced code 405
2. Start the server and observe: **Pass** if `FATAL "...code 405...re-pair..."` appears and no `RECONNECT` lines follow

Approach B — Targeted code injection for local verification:
1. In `index.js`, in the `connection === 'close'` block, **replace** (not add above) the existing line:
   `const statusCode = lastDisconnect?.error?.output?.statusCode;`
   with:
   `const statusCode = 405; // TEST OVERRIDE — revert after testing`
2. Start the server: `node index.js`
3. Wait for a natural WebSocket close (baileys will close the connection during initial handshake when auth is present)
4. **Pass:** Single `FATAL "Session rejected by WhatsApp (code 405). Delete auth folder and re-pair."` log, no `RECONNECT` lines follow
5. **Fail:** `RECONNECT` lines appear and/or process exits with code 1 after 10 retries → Task 5 not applied or placed after the reconnect logic
6. **Revert the override** before committing

**Phase 5 — Normal reconnect unaffected (AC 6)**
1. Restore real code (no override)
2. Start connected, then simulate a normal disconnect (e.g. disable network briefly)
3. **Pass:** `RECONNECT "Connection closed (code: 428). Reconnecting in 5s..."` appears and retries
4. **Fail:** Process exits or logs FATAL unexpectedly

### Notes

- The `qrcode-terminal` API: `qrcode.generate(str, { small: true }, callback)` — the callback is optional; without it the QR prints to stdout directly.
- Default to no size option first if scan fails — some phone cameras need a larger QR. `{ small: true }` is a space optimization only; remove it if the QR cannot be scanned.
- If code 405 recurs even after re-pairing, the root cause may be a banned number or WhatsApp policy enforcement — outside scope of this fix.
- `DisconnectReason.forbidden` is 403 (not 405) — these are distinct. 403 is deferred: it is rarer in practice and was not observed in the failure that motivated this spec. Treating it separately is tracked for future work.

## Review Notes
- Adversarial review completed
- Findings: 7 total, 2 fixed (F1, F3), 4 acknowledged out-of-scope (F2, F4, F5, F6), 1 skipped undecided (F7)
- Resolution approach: auto-fix
