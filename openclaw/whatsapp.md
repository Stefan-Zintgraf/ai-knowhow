# OpenClaw: WhatsApp (Web channel)

This note is derived from the OpenClaw source tree (`openclaw` repo). It covers **session linking (QR)**, **DM pairing (security)**, **outbound sends**, and **inbound message handling** for the WhatsApp Web (Baileys) integration.

**“Pairing”** shows up in two separate places:

1. **WhatsApp Web session linking** — you scan a QR code so the gateway acts as a *Linked Device* (Baileys / WhatsApp Web protocol).
2. **OpenClaw DM pairing** — when `dmPolicy` is `pairing`, unknown senders get a challenge and must be approved with `openclaw pairing approve` before the bot processes their DMs.

---

## Table of contents

- [1. WhatsApp Web session linking (QR + credentials)](#1-whatsapp-web-session-linking-qr--credentials)
- [2. OpenClaw DM pairing (access control, not WhatsApp Web)](#2-openclaw-dm-pairing-access-control-not-whatsapp-web)
- [3. Sending WhatsApp messages](#3-sending-whatsapp-messages)
- [4. Receiving WhatsApp messages](#4-receiving-whatsapp-messages)
- [5. Quick mental model](#5-quick-mental-model)
- [6. Key source files (repo-relative)](#6-key-source-files-repo-relative)

---

## 1. WhatsApp Web session linking (QR + credentials)

### Library and socket

- The integration uses **Baileys** (`@whiskeysockets/baileys`): `makeWASocket`, `useMultiFileAuthState`, `fetchLatestBaileysVersion`, etc.
- Core socket creation lives in `extensions/whatsapp/src/session.ts` (`createWaSocket`).
- Auth is **multi-file** under a per-account directory (see below). Credential updates are persisted on `creds.update` via a **per-`authDir` queue** so concurrent saves do not corrupt state. There is a best-effort `creds.json.bak` before writes (`safeSaveCreds`).

### Connection / QR behavior

- `createWaSocket(printQr, verbose, { authDir?, onQr? })`:
  - Loads or creates auth state with `useMultiFileAuthState(authDir)`.
  - Subscribes to `connection.update`. When WhatsApp emits a `qr` string:
    - If `onQr` is provided (non-interactive / gateway flows), it is called with the raw QR payload.
    - If `printQr` is true (CLI), a terminal QR is printed via `qrcode-terminal`.
  - `printQRInTerminal` is forced **false** on `makeWASocket`; QR is handled manually.
  - Browser fingerprint passed to Baileys: `["openclaw", "cli", VERSION]`.
  - `syncFullHistory: false`, `markOnlineOnConnect: false`.

### Waiting until “linked”

- `waitForWaConnection(sock)` resolves when `connection.update` reports `connection === "open"`, and rejects on close (used by both CLI login and QR wait loops).

### Where credentials live

- Default directory: `resolveOAuthDir()/whatsapp/<accountId>` (see `extensions/whatsapp/src/auth-store.ts` — `resolveDefaultWebAuthDir`, and `extensions/whatsapp/src/accounts.ts` — `resolveDefaultAuthDir`).
- **Legacy**: for the default account only, if creds exist under the old flat OAuth dir and not under `whatsapp/default`, `resolveWhatsAppAuthDir` still points at the legacy path and sets `isLegacyAuthDir` (affects logout: selective file delete vs full directory rm).
- “Linked” is determined by `webAuthExists(authDir)`: directory exists, `creds.json` is a non-trivial file, and JSON parses. `maybeRestoreCredsFromBackup` can restore from `creds.json.bak` if `creds.json` is missing/invalid.
- Self identity for status/UI: `readWebSelfId` reads `creds.json` → `me.id` (JID) and maps to E.164 when possible (`jidToE164`).

### CLI path: `openclaw channels login --channel whatsapp`

- The channel plugin’s `auth.login` delegates to `loginWeb` (`extensions/whatsapp/src/login.ts`):
  - Resolves account via `resolveWhatsAppAccount`.
  - `createWaSocket(true, verbose, { authDir })` — **printQr true** → terminal QR.
  - `waitForWaConnection(sock)`.
  - **Disconnect code 515** (“restart after pairing”): close socket, `waitForCredsSaveQueueWithTimeout(authDir)`, open a **new** socket with `printQr: false`, wait again.
  - **Logged out**: `logoutWeb` clears cache, user must scan again.
  - Socket is closed shortly after success (500 ms delay) so Baileys can flush.

### Split QR path: gateway + UIs + agent tool

For environments that cannot show a terminal QR (gateway, macOS app, web UI, chat surfaces), OpenClaw uses a **two-phase** flow implemented in `extensions/whatsapp/src/login-qr.ts`:

| Phase | Function | Role |
|--------|-----------|------|
| Start | `startWebLoginWithQr` | Creates socket with `onQr`, waits until first QR (or timeout), renders PNG as `data:image/png;base64,...`, stores active login state in an in-memory `Map` keyed by **accountId** |
| Wait | `waitForWebLogin` | Polls/races on the same `waitPromise` until connected, timeout, or error |

Details:

- **Already linked**: if `webAuthExists` and no `force`, returns a message (no new QR). User must “relink” with `force`.
- **Dedup**: if a fresh login (< 3 minutes TTL) already has `qrDataUrl`, returns the same QR.
- **QR wait timeout**: default 30s minimum 5s for receiving the QR string from Baileys.
- **Active login TTL**: 3 minutes (`ACTIVE_LOGIN_TTL_MS`). Expired logins are reset with a user-facing message.
- **Wait loop timeout**: default 120s minimum 1s per call; can return “still waiting” so clients can call `wait` again.
- **515 handling**: same pattern as CLI — swap socket after creds flush, single `restartAttempted` guard.
- **PNG rendering**: `extensions/whatsapp/src/qr-image.ts` builds a matrix via `qrcode-terminal`’s embedded QR implementation, draws scaled black/white pixels, encodes PNG via `encodePngRgba` from the plugin SDK.

### Gateway RPC

- The WhatsApp plugin registers `gatewayMethods: ["web.login.start", "web.login.wait"]` (`extensions/whatsapp/src/shared.ts`).
- Handlers: `src/gateway/server-methods/web.ts`:
  - **`web.login.start`**: finds the first channel plugin that advertises those methods (today: WhatsApp), calls `context.stopChannel(provider.id, accountId)` to avoid conflicting listeners, then `provider.gateway.loginWithQrStart({ force, timeoutMs, verbose, accountId })`. Returns `{ qrDataUrl?, message }`.
  - **`web.login.wait`**: `loginWithQrWait`. If `result.connected`, calls **`context.startChannel(provider.id, accountId)`** so the gateway starts the normal monitor after a successful link.

Plugin wiring: `extensions/whatsapp/src/channel.ts` maps `loginWithQrStart` / `loginWithQrWait` to `startWebLoginWithQr` / `waitForWebLogin`.

### Agent tool `whatsapp_login`

- Defined in `extensions/whatsapp/src/agent-tools-login.ts`, registered on the channel plugin (`channel.ts` `agentTools`).
- Owner-only. Actions: `start` (default) or `wait`.
- Imports `startWebLoginWithQr` / `waitForWebLogin` from `openclaw/plugin-sdk/whatsapp-login-qr`, which resolves through `src/plugins/runtime/runtime-whatsapp-boundary.ts` into the installed WhatsApp extension.
- On `start` with a QR: returns markdown embedding `![whatsapp-qr](data:...)`.

### Multi-account

- `resolveWhatsAppAccount({ cfg, accountId })` picks the account; `authDir` comes from `channels.whatsapp.accounts.<id>.authDir` or the default path under `whatsapp/<normalizedAccountId>`.
- In-memory active QR logins are **per `accountId`**, so different accounts do not clobber each other.

---

## 2. OpenClaw DM pairing (access control, not WhatsApp Web)

This is independent of scanning the Linked Devices QR. It controls **who may talk to the bot** over WhatsApp once the session is already linked.

### Configuration

- Default `dmPolicy` for WhatsApp is **`pairing`** when unset (`extensions/whatsapp/src/inbound/access-control.ts`).
- `allowFrom` / stored allowlist entries (including post-approval) participate in `resolveDmGroupAccessWithLists` via `readStoreAllowFromForDmPolicy`.

### Inbound flow

- `checkInboundAccessControl` (same file) runs for DMs and groups.
- For DMs, if the decision is **`pairing`** and the sender is not the same phone as the linked self-number (`!isSamePhone`):
  - Unless suppressed (historical message grace around reconnect), it runs `createChannelPairingChallengeIssuer` which upserts a pairing request through `upsertChannelPairingRequest` (`channel: "whatsapp"`, `accountId`, metadata including optional `pushName`).
  - Sends the pairing instructions back over the socket: `sock.sendMessage(remoteJid, { text })`.
  - Returns **`allowed: false`** so the message is not processed as a normal chat turn until approved.
- The channel plugin exposes `pairing: { idLabel: "whatsappSenderId" }` (`channel.ts`) so pairing records label the sender id field consistently for WhatsApp (E.164-style sender id).

### Operator approval

- Documented user flow: `openclaw pairing list whatsapp` / `openclaw pairing approve whatsapp <CODE>` (see `docs/channels/whatsapp.md`). Pairing store and limits are in `src/pairing/*`.

---

## 3. Sending WhatsApp messages

Sending always ultimately uses the **same Baileys socket** as the running gateway listener, but there are **two call styles**: (A) **programmatic / cross-feature** sends that look up a process-wide “active listener”, and (B) **auto-reply** sends that use closures bound to the inbound message (same underlying `sock.sendMessage`).

### 3.1 Active listener registry (why the gateway must be running)

- `extensions/whatsapp/src/active-listener.ts` keeps a **`Map<accountId, ActiveWebListener>`** on **`globalThis`** (not plain module state) so bundled chunks share one registry (see comment re issue #14406).
- When `monitorWebChannel` finishes connecting (`extensions/whatsapp/src/auto-reply/monitor.ts`), it calls `setActiveWebListener(account.accountId, listener)` where `listener` is the object returned from `monitorWebInbox` (spread with `createWebSendApi`: `sendMessage`, `sendPoll`, `sendReaction`, `sendComposingTo`, `close`, etc.).
- **`sendMessageWhatsApp`** (`extensions/whatsapp/src/send.ts`) calls **`requireActiveWebListener(accountId)`**. If no listener is registered for that account, it throws with a hint to start the gateway and link WhatsApp. So **`openclaw message send`** (and similar) need the **gateway monitor** running for that account.

### 3.2 Channel outbound adapter (agent replies, CLI send, chunked delivery)

- The WhatsApp channel registers an outbound stack in `extensions/whatsapp/src/outbound-adapter.ts` (`whatsappOutbound`):
  - `deliveryMode: "gateway"` — orchestration expects the gateway-side channel runtime.
  - `resolveTarget` uses `resolveWhatsAppOutboundTarget` (allowlist / mode rules).
  - `sendPayload` delegates to `sendTextMediaPayload` from the plugin SDK, which splits text vs media and calls `sendText` / `sendMedia` / `sendPoll` hooks.
- Those hooks call **`sendMessageWhatsApp`** / **`sendPollWhatsApp`** from `send.ts` (or injected test doubles via `resolveOutboundSendDep`).

### 3.3 `sendMessageWhatsApp` pipeline (text + media)

Path: `extensions/whatsapp/src/send.ts`.

1. **Target**: `toWhatsappJid(to)` normalizes E.164 or JID to a WhatsApp JID.
2. **Early exit**: empty trimmed text and no `mediaUrl` → returns `{ messageId: "", toJid: jid }`.
3. **Listener**: `requireActiveWebListener(options.accountId)` → `{ listener: active, accountId: resolvedAccountId }`.
4. **Config**: `resolveWhatsAppAccount` for markdown table mode and media limits.
5. **Text shaping**: `convertMarkdownTables` (per `resolveMarkdownTableMode`) then **`markdownToWhatsApp`** so outbound text matches WhatsApp formatting expectations.
6. **Media** (optional): `loadWebMedia` with `resolveWhatsAppMediaMaxBytes(account)` and optional `mediaLocalRoots`. MIME kind drives later payload shape; audio OGG may be tagged `codecs=opus` for voice notes; documents get a filename.
7. **Typing indicator**: `await active.sendComposingTo(to)` before send.
8. **Send**: `active.sendMessage(to, text, mediaBuffer, mediaType, sendOptions?)` where `sendOptions` can carry `gifPlayback`, `fileName`, or explicit `accountId` for telemetry.
9. **Implementation of `active.sendMessage`**: `extensions/whatsapp/src/inbound/send-api.ts` (`createWebSendApi`) builds a Baileys **`AnyMessageContent`**:
   - image / audio (PTT) / video / document vs plain `{ text }`
   - then `sock.sendMessage(jid, payload)`
10. **Metrics**: `recordChannelActivity` for outbound; structured logs under `gateway/channels/whatsapp`.

Polls follow **`sendPollWhatsApp`** → same send API with a `poll` content object (`selectableCount` from `maxSelections`).

### 3.4 Auto-reply delivery (different entry, same socket)

- When the agent produces a reply, `processMessage` / `createChannelReplyPipeline` eventually calls **`deliverWebReply`** (`extensions/whatsapp/src/auto-reply/deliver-reply.ts`).
- That path does **not** call `sendMessageWhatsApp`. It uses the **`WebInboundMsg`** helpers attached in `monitor.ts`:
  - **`msg.reply(text)`** → `sock.sendMessage(chatJid, { text })` for the **same chat** as the inbound message.
  - **`msg.sendMedia(payload)`** → `sock.sendMessage(chatJid, payload)` for images, audio, video, documents.
- Text is still converted: `markdownToWhatsApp(convertMarkdownTables(...))`, then chunked with `chunkMarkdownTextWithMode` using account text limits / chunk mode. **Reasoning** payloads can be suppressed (`shouldSuppressReasoningReply`). Sends use a small **retry loop** on transient socket errors.
- **Reactions** (if configured) can run via the listener’s `sendReaction` / action runtime; the inbound monitor also exposes composing updates per chat.

---

## 4. Receiving WhatsApp messages

Inbound handling is centered on **`monitorWebInbox`** (`extensions/whatsapp/src/inbound/monitor.ts`), which is started by **`monitorWebChannel`** (`extensions/whatsapp/src/auto-reply/monitor.ts`).

### 4.1 Socket setup

- Creates a socket with `createWaSocket(false, verbose, { authDir })`, **`waitForWaConnection`**, records **`connectedAtMs`**.
- Sends **`sendPresenceUpdate("available")`** globally after connect.
- Resolves **self** JID / E.164 from `sock.user` for `from`/`to` fields and access control.

### 4.2 Event source

- Subscribes to Baileys **`messages.upsert`**.
- Only processes `type === "notify"` or **`append`** (history / catch-up). For **`append`**, messages older than ~60s before connect are **read-marked but not auto-replied** (anti flood on reconnect).

### 4.3 Per-message pipeline

For each `WAMessage`:

1. **`recordChannelActivity`** inbound.
2. **`normalizeInboundMessage`**:
   - Drops status/broadcast JIDs; **dedupes** by `accountId:remoteJid:messageId`.
   - Determines group vs DM; resolves participant JIDs to E.164 where possible (`resolveJidToE164`, optional LID mapping).
   - Fetches **group metadata** (subject, participants) with a short TTL cache.
   - Runs **`checkInboundAccessControl`** (DM policy, group policy, pairing challenge). If not allowed, returns **`null`** — no auto-reply pipeline (pairing replies already sent inside access control when applicable).
3. **`maybeMarkInboundAsRead`**: optional **`readMessages`** (respects `sendReadReceipts`; skips in self-chat mode).
4. **`enrichInboundMessage`**:
   - **`extractText`**, **`extractLocationData`** (appended as text), **`extractMediaPlaceholder`** if no text.
   - **`describeReplyContext`** for reply threading metadata.
   - **`downloadInboundMedia`** + **`saveMediaBuffer`** (size cap from `mediaMaxMb`, default 50MB).
5. Builds **`WebInboundMessage`** with `reply` / `sendComposing` / `sendMedia` closures, **`mentionedJids`**, group fields, media paths, etc.
6. **`debouncer.enqueue`** (if configured): batches rapid consecutive messages from the same sender/conversation unless media, location, reply thread, or control commands — then **`onMessage`** from the monitor.

### 4.4 Auto-reply routing (`createWebOnMessageHandler`)

File: `extensions/whatsapp/src/auto-reply/monitor/on-message.ts`.

- Resolves **`resolveAgentRoute`** (bindings: channel `whatsapp`, account, peer group vs direct).
- **Echo suppression**: if body matches recently sent text tracked by **`EchoTracker`**, skip (prevents loops).
- **Groups**: group gating (mentions, activation), optional **broadcast** to multiple agents, **group history** for context; then **`processMessage`**.
- **`processMessage`** (`auto-reply/monitor/process-message.ts`) runs the shared **`createChannelReplyPipeline`**: command gating, session envelope, model call, then **`deliverWebReply`** as in §3.4.

### 4.5 Lifecycle and errors

- **`connection.update`**: on close, resolves `onClose` with disconnect reason; `monitorWebChannel` handles **reconnect backoff**, logout detection, watchdog (no inbound messages for a long time can force reconnect), and unhandled rejection hook for likely crypto errors.
- On shutdown, **`setActiveWebListener(accountId, null)`** clears the registry so sends fail fast until the next connection.

---

## 5. Quick mental model

| Concern | Mechanism | Typical user action |
|---------|-----------|-------------------|
| Link phone to gateway | Baileys + multi-file auth + QR | `openclaw channels login --channel whatsapp`, or gateway `web.login.start` / `web.login.wait`, or agent `whatsapp_login` |
| Let a stranger DM the bot | `dmPolicy: pairing` + pairing store | `openclaw pairing approve whatsapp …` |
| Relink after logout / new device | Clear auth + new QR | `force` on QR start, or logout then login again |
| Send while gateway down | Requires active listener | Start gateway so `monitorWebChannel` registers the send API |
| Inbound auto-reply | `messages.upsert` → access → enrich → debounce → route → agent → `deliverWebReply` | Configure bindings + models; keep gateway running |
| Outbound from tools / CLI | `sendMessageWhatsApp` → active listener → `createWebSendApi` | Same running gateway as inbox |

---

## 6. Key source files (repo-relative)

| Area | Path |
|------|------|
| Baileys socket + creds queue | `extensions/whatsapp/src/session.ts` |
| CLI login (terminal QR) | `extensions/whatsapp/src/login.ts` |
| Split QR start/wait | `extensions/whatsapp/src/login-qr.ts` |
| Auth paths, logout, self id | `extensions/whatsapp/src/auth-store.ts` |
| Account / authDir resolution | `extensions/whatsapp/src/accounts.ts` |
| Channel plugin (gateway, auth, pairing metadata) | `extensions/whatsapp/src/channel.ts` |
| Plugin base (gatewayMethods) | `extensions/whatsapp/src/shared.ts` |
| Gateway RPC | `src/gateway/server-methods/web.ts` |
| DM pairing gate | `extensions/whatsapp/src/inbound/access-control.ts` |
| Inbound socket + upsert + normalize + debounce | `extensions/whatsapp/src/inbound/monitor.ts` |
| Baileys outbound payload builder | `extensions/whatsapp/src/inbound/send-api.ts` |
| Active listener registry | `extensions/whatsapp/src/active-listener.ts` |
| Outbound send (CLI / adapter) | `extensions/whatsapp/src/send.ts` |
| Channel outbound adapter | `extensions/whatsapp/src/outbound-adapter.ts` |
| Gateway monitor loop + listener install | `extensions/whatsapp/src/auto-reply/monitor.ts` |
| Inbound handler (routing, echo, groups) | `extensions/whatsapp/src/auto-reply/monitor/on-message.ts` |
| Agent pipeline + reply | `extensions/whatsapp/src/auto-reply/monitor/process-message.ts` |
| Auto-reply text/media delivery | `extensions/whatsapp/src/auto-reply/deliver-reply.ts` |
| Runtime boundary (loads extension) | `src/plugins/runtime/runtime-whatsapp-boundary.ts` |
| Public SDK re-export for QR helpers | `src/plugin-sdk/whatsapp-login-qr.ts` |

---

*Generated from OpenClaw codebase analysis. For product-facing setup steps, see the published docs on WhatsApp / pairing / gateway configuration.*
