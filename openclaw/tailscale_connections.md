# Tailscale + OpenClaw: Device Connection

## Finding Your Tailscale MagicDNS Name

The name `mele.tailfdf682.ts.net` is not stored in OpenClaw — it comes from Tailscale.

**From the terminal on `mele`:**
```bash
tailscale status           # shows node name + tailnet domain
tailscale whois $(tailscale ip)  # shows full MagicDNS name under "Machine: Name"
```

**From the Tailscale admin console:**
`https://login.tailscale.com/admin/machines`

**How the name is composed:**
`<machine-hostname>.<tailnet-id>.ts.net`
- `mele` = Linux hostname (`hostname` command)
- `tailfdf682` = your tailnet's unique ID (assigned by Tailscale)
- `.ts.net` = Tailscale's MagicDNS domain

---

## Setup (already done)

- Gateway on `mele` (Linux), bound to loopback + Tailscale Serve enabled
- `trustedProxies: ["127.0.0.1"]` set in `~/.openclaw/openclaw.json` (required for correct IP resolution through Tailscale Serve)
- Tailscale account: `stefanzintgraf@gmail.com`
- Serve URL: `https://mele.tailfdf682.ts.net` → proxies to `ws://127.0.0.1:18789`
- Gateway token: stored in `~/.openclaw/openclaw.json` under `gateway.auth.token`

**Gateway config location:** `~/.openclaw/openclaw.json`
```json
"gateway": {
  "auth": { "mode": "token", "token": "<token>" },
  "tailscale": { "mode": "serve", "resetOnExit": true },
  "trustedProxies": ["127.0.0.1"]
}
```

---

## Pairing Model

- **Local connections** (`127.0.0.1`) are auto-approved (loopback = trusted)
- **Remote connections** via Tailscale Serve require **manual approval** because the gateway correctly identifies the real client IP (Android's Tailscale IP `100.105.180.59`, Windows PC's `100.101.181.29`, etc.) which is not loopback
- Pairing requests expire after **5 minutes** — act quickly

---

## Browser (Windows/any device on tailnet)

1. Install Tailscale, sign in as `stefanzintgraf@gmail.com`
2. Open `https://mele.tailfdf682.ts.net`
3. First visit: gateway rejects with `1008: pairing required`
4. On `mele`, immediately run:
   ```bash
   openclaw devices list        # look for Pending section
   openclaw devices approve <requestId>
   ```
5. Browser reconnects and stays paired permanently

---

## OpenClaw Android App

1. Install Tailscale on Android, sign in as `stefanzintgraf@gmail.com`
2. In OpenClaw app → Self-Hosted:
   - **Instance URL**: `wss://mele.tailfdf682.ts.net`
   - **Gateway Token**: (from `~/.openclaw/openclaw.json` → `gateway.auth.token`)
3. Tap Connect — the app will show `1008: pairing required` and disconnect
4. **Within 5 minutes**, on `mele`:
   ```bash
   openclaw devices list        # look for Pending section with Android device
   openclaw devices approve <requestId>
   ```
5. App reconnects automatically and stays paired

**Note:** The app uses device identity (cryptographic key pair stored on the phone). Uninstalling/reinstalling the app generates a new key → re-pairing required.

---

## Key Commands

```bash
openclaw devices list                    # show paired + pending
openclaw devices approve <requestId>     # approve a pending request
```

---

## Troubleshooting

- **No pending device in list**: request expired (5 min TTL) — retry connection from app/browser
- **`missing scope: operator.read`**: device connected but paired with wrong scopes — delete device from list and re-pair
- **`1008: pairing required` loop**: approve the request quickly after connecting
