# WhatsApp pairing: `whatsapp_client` vs OpenClaw

This document compares how **WhatsApp Web (Baileys) pairing** is implemented in **`C:\PROJ\ai-knowhow\tools\whatsapp_client`** with **OpenClaw** (`extensions/whatsapp` + gateway). It explains why OpenClaw’s flow is **robust after a QR scan**, and which gaps in `whatsapp_client` commonly cause **“pairing worked once then broke”**, **endless reconnect loops**, or **sessions that never reach `connection === 'open'`** reliably.

No code was changed in either project for this write-up; conclusions are from reading the sources.

---

## 1. What `whatsapp_client` does

**Entry:** `index.js` — `connectToWhatsApp()`.

1. Ensures `AUTH_FOLDER` exists (`config.js`, default `auth_info_sender`).
2. `useMultiFileAuthState(config.authFolder)` → `{ state, saveCreds }`.
3. Optionally removes listeners from a previous `sock`, then **`makeWASocket({ auth: state, logger: noopLogger })`**.
4. On **`connection.update`**:
   - If **`qr`**: logs and prints QR via **`qrcode-terminal`**.
   - Tracks **`connectionState`** from `connection` updates.
   - On **`connection === 'close'`**: handles **`loggedOut`**, **`405`**, otherwise increments **`consecutiveFailures`**, logs, and **`setTimeout(..., 5000)`** → **`connectToWhatsApp()`** again.
   - On **`connection === 'open'`**: resets **`consecutiveFailures`**.
5. On **`creds.update`**: **`await saveCreds()`** (per event).

**HTTP:** Express starts in **`main()`** after **`await connectToWhatsApp()`**. Note that **`connectToWhatsApp()` does not wait for `connection === 'open'`**; it only registers handlers and returns. The server can accept traffic while WhatsApp is still pairing or reconnecting (send route then returns 503 via `getSocket()` until `connectionState === 'open'`).

**Dependencies:** `@whiskeysockets/baileys` **7.0.0-rc.9** (same major/rc line as OpenClaw’s WhatsApp extension).

---

## 2. What OpenClaw does (pairing-relevant parts)

**Socket creation:** `extensions/whatsapp/src/session.ts` — `createWaSocket`.

- **`fetchLatestBaileysVersion()`** and passes **`version`** into **`makeWASocket`**.
- **`auth`**: `{ creds: state.creds, keys: makeCacheableSignalKeyStore(state.keys, logger) }` (not the raw `state` object alone).
- **`browser: ["openclaw", "cli", VERSION]`**, **`printQRInTerminal: false`**, **`syncFullHistory: false`**, **`markOnlineOnConnect: false`**, structured logger (or silent).
- **`creds.update`** → **queued** `saveCreds` per auth dir, with **backup of `creds.json`** before write (`safeSaveCreds`).

**After QR (interactive CLI login):** `extensions/whatsapp/src/login.ts` — `loginWeb`.

- Waits until the socket is **open** via **`waitForWaConnection(sock)`**.
- If disconnect status is **515** (WhatsApp asking for a **restart right after pairing**):
  - Closes the WebSocket.
  - **`waitForCredsSaveQueueWithTimeout(authDir)`** so persisted keys/creds are flushed.
  - Opens a **new** socket **without** expecting a new QR (`createWaSocket(false, ...)`), then waits for **open** again.

**Split QR (gateway / UI):** `extensions/whatsapp/src/login-qr.ts` implements the same **515 → flush creds → new socket** idea for **`startWebLoginWithQr` / `waitForWebLogin`**.

OpenClaw treats **515** as a **normal step** in the pairing lifecycle, not as a generic failure.

---

## 3. Side-by-side comparison

| Topic | `whatsapp_client` | OpenClaw |
|--------|---------------------|----------|
| Baileys version | 7.0.0-rc.9 | 7.0.0-rc.9 (extension) |
| WA Web **protobuf / client version** | Not set (library default) | **`fetchLatestBaileysVersion()`** passed as **`version`** |
| **Browser / client id** | Default | Explicit **`browser: [...]`** |
| **Auth keys** | `auth: state` (raw from `useMultiFileAuthState`) | **`creds` + `makeCacheableSignalKeyStore(keys)`** |
| **515 after scan** | Treated like any other close → **5s reconnect** | **Dedicated path**: close, **await cred save queue**, **new socket**, wait **open** |
| **Credential persistence** | `await saveCreds()` on each `creds.update` | **Serialized queue** + **backup** before overwrite |
| **Startup vs “linked”** | Server starts immediately after handlers attached | Login flows **await** open where required; gateway registers send API only when monitor is up |
| **405 / loggedOut** | Logged, no auto-reconnect for those | Logout clears cache / user action (documented elsewhere) |

---

## 4. Why OpenClaw “works” (reliably completes pairing)

1. **Post-QR restart (515)**  
   After a successful QR scan, WhatsApp often **drops the connection once** and expects the client to **come back with the credentials it just wrote**. OpenClaw **waits for creds to be saved** and then **creates a fresh socket**, matching that protocol behavior.

2. **Version alignment**  
   Passing **`version` from `fetchLatestBaileysVersion()`** tracks the **current WhatsApp Web pairing/version expectations**. That reduces **rejection or flaky handshakes** that show up as odd close codes or **405**-class failures when defaults lag.

3. **Stable, explicit client fingerprint**  
   The **`browser`** tuple makes the session look like a **consistent linked-device client**, which matters for **anti-abuse / compatibility** (exact impact is server-side, but OpenClaw follows the Baileys-recommended pattern).

4. **Safer creds I/O**  
   Queued saves + backup reduce **partial `creds.json` / key files** during rapid updates around pairing—exactly when **515** and **`creds.update`** bursts happen.

Together, these are the same class of fixes people describe as “scan QR → disconnect → works on retry”: OpenClaw **implements the retry in a controlled way** immediately after pairing instead of relying on a blind 5-second reconnect.

---

## 5. Why `whatsapp_client` often “does not work” (or feels broken)

The project is **not wrong** to use Baileys and multi-file auth; the gaps are **lifecycle and hardening**. Typical symptoms:

### A. Missing **515 + creds flush + immediate clean reconnect**

On close, **`whatsapp_client`** always goes through **`consecutiveFailures`**, a **5 s delay**, and a generic **`connectToWhatsApp()`**. For a **515** right after pairing:

- **`saveCreds()`** may still be running or **ordered behind** other work; the **next** socket can start with **incomplete disk state**.
- The **delay** and **failure counter** turn a **normal** handshake step into a **degraded** path (extra races, user thinks “it crashed”).
- There is **no** equivalent of **`waitForCredsSaveQueueWithTimeout`** before the second connection.

So pairing can **appear** to fail even when the QR was accepted.

### B. No explicit **`version` (and no custom `browser`)**

With **defaults only**, behavior depends on whatever **Baileys 7.0.0-rc.9** ships internally. When WhatsApp moves forward, **OpenClaw’s explicit `fetchLatestBaileysVersion()`** is strictly **more aligned** than **omitting `version`**. That can manifest as **harder pairing**, **405**, or **unstable** first connection—especially on **new accounts** or **strict** regions.

### C. `auth: state` vs wrapped keys

Passing **`auth: state`** is usually **equivalent** to `{ creds, keys }` **if** `state` is exactly the authentication state object. OpenClaw still wraps **`keys`** in **`makeCacheableSignalKeyStore`** for **correctness/perf** under load. This is **unlikely** to be the *primary* pairing bug by itself, but it is **one more** difference from a **known-good** production setup.

### D. `connectToWhatsApp()` resolves before “open”

This does **not** stop pairing, but it means **logs and HTTP readiness are decoupled**: the process looks “up” while WhatsApp is still **connecting** or **waiting for QR**. That can confuse operators who hit **`/send`** and see **503** and assume pairing failed.

### E. Reconnect loop and `consecutiveFailures`

Every **close** (including a **515** that should be handled cleanly) **increments** failure counts toward **exit after 10**. OpenClaw’s **515** path does **not** treat that as a generic failure in the same way.

---

## 6. Summary

| Question | Answer |
|----------|--------|
| Does `whatsapp_client` implement QR pairing? | **Yes** — `connection.update` + `qrcode-terminal` + `useMultiFileAuthState`. |
| Why does OpenClaw succeed more often after scan? | **Handles 515 with creds flush and a fresh socket**, uses **fetched WA Web version**, explicit **browser** id, and **queued/backup creds** writes. |
| Why can `whatsapp_client` fail or feel flaky? | **Treats 515 like a generic disconnect**, **no creds-queue flush**, **5 s blind reconnect**, **no `fetchLatestBaileysVersion`**, and **stricter failure counting**—all of which race with **post-scan persistence**. |

To make `whatsapp_client` behave closer to OpenClaw **without copying the whole gateway**, the **highest-impact** changes would be: **detect 515 (and similar restart signals)**, **await credential persistence before a second socket**, **pass `version` from `fetchLatestBaileysVersion()`**, and optionally align **`browser`** and **key store** usage with Baileys examples. (This document does **not** implement those changes.)

---

## 7. References (repo-relative, OpenClaw)

- `extensions/whatsapp/src/session.ts` — `createWaSocket`, creds queue, Baileys options  
- `extensions/whatsapp/src/login.ts` — `loginWeb`, **515** handling  
- `extensions/whatsapp/src/login-qr.ts` — gateway QR flow, **515** handling  
- `extensions/whatsapp/src/session-errors.ts` — `getStatusCode`  

**Analyzed external project paths**

- `C:\PROJ\ai-knowhow\tools\whatsapp_client\index.js`  
- `C:\PROJ\ai-knowhow\tools\whatsapp_client\config.js`  
- `C:\PROJ\ai-knowhow\tools\whatsapp_client\package.json`  
