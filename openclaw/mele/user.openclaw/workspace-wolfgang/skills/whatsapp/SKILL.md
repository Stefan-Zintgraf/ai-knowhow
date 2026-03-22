---
name: whatsapp
description: Send or schedule WhatsApp messages via tools/whatsapp_client/send-whatsapp.sh. Use only when the user explicitly asks to be notified or to send a message via WhatsApp (remind on WhatsApp, WA message, etc.). For Telegram, email, or channel-agnostic reminders, use the notify skill instead.
---

# WhatsApp Skill

This skill covers **outbound WhatsApp** only: immediate send or **deterministic** future/recurring delivery by having the **system scheduler** run `send-whatsapp.sh` directly.

**Canonical sender script (always this path):**

`/home/dev/proj/ai-knowhow/tools/whatsapp_client/send-whatsapp.sh`

Do not use other send scripts (for example Baileys helpers elsewhere in the tree) for outbound WhatsApp in this workspace — **only** this script.

## When to Use

Use this skill when the user clearly wants **WhatsApp** as the channel, for example:

- "Remind me on WhatsApp in 10 minutes …"
- "Send me a WhatsApp at 9am …"
- "Notify me via WA when …"
- "Message +49… on WhatsApp with …"

Do **not** use this skill for generic "remind me" / "notify me" with no channel — use **notify** and ask which channel, or follow workspace defaults in `AGENTS.md` / `USER.md`.

## When Not to Use

- Telegram, email, or unspecified channel → **notify** (or the appropriate tool), not this skill.
- Installing or debugging the WhatsApp **listener** service → `whatsapp-client.sh --install` etc., not this skill’s send flow.

## Required Fields (Same Spirit as Notify)

Before scheduling or sending, you need:

| Required | If missing, ask |
|----------|-----------------|
| **Recipient** | E.164 digits for `-n` (no `+` in the flag value; digits only). If unknown, ask. |
| **Message body** | Exact text to send. |
| **Timing** | For scheduled jobs: when (absolute, relative, or cron). For immediate: say "now". |

`send-whatsapp.sh` reads API base URL and key from `tools/whatsapp_client/.env` unless overridden with `-u` / `-k`.

## Immediate Send

Run **one** non-interactive command (exec/bash), no extra LLM turn at delivery:

```bash
/home/dev/proj/ai-knowhow/tools/whatsapp_client/send-whatsapp.sh \
  -n '491777960262' \
  -m 'Exact message text here.'
```

Escape embedded `'` in the message for the shell (e.g. use `"` around `-m` and escape inner `"` as needed).

## Scheduled Send — No OpenClaw Cron LLM

**Do not** use OpenClaw `cron.add` with `sessionTarget: "isolated"` and `payload.kind: "agentTurn"` for WhatsApp delivery. That path starts an **isolated agent** at fire time (tokens, latency, nondeterminism).

Instead, the **scheduler must invoke `send-whatsapp.sh` directly** at the right time. Prefer, in order:

1. **`systemd-run` (user)** — good for one-shot relative delay ("in N minutes/seconds"):
   ```bash
   systemd-run --user --on-active=300s --unit=wa-send-once \
     /home/dev/proj/ai-knowhow/tools/whatsapp_client/send-whatsapp.sh \
     -n '491777960262' -m 'Reminder text.'
   ```
   Use a sensible `--unit=` name (unique enough not to collide). Compute seconds from now to the target for `--on-active=` when the user asked for a relative delay.

2. **`systemd-run` with calendar** — one-shot or recurring wall-clock times (when you know the user’s timezone, e.g. `Europe/Berlin`):
   ```bash
   systemd-run --user --on-calendar='2026-03-23 09:00:00' --unit=wa-morning \
     /home/dev/proj/ai-knowhow/tools/whatsapp_client/send-whatsapp.sh \
     -n '491777960262' -m 'Good morning.'
   ```
   Validate `systemd-run` / timer syntax on the host if unsure; timezone behavior follows systemd user session.

3. **User crontab** — recurring jobs (e.g. every weekday 8:00). Add a line that runs the **full path** to `send-whatsapp.sh` with `-n` and `-m`. Ensure cron’s environment has what the script needs (often fine if `.env` is beside the script and paths are absolute).

4. **`at`** — if available, you can queue a one-shot run at a wall time; the queued command must be the same `send-whatsapp.sh` invocation.

**Minimum delay:** If the user asks for "in 1 second", scheduling may still need a **minimum ~15s** effective delay to account for tool round-trip (same idea as notify). Prefer stating the actual scheduled time after you queue the job.

## Validation

Before you run or schedule:

```bash
node skills/whatsapp/scripts/validate.js '{"number":"491777960262","message":"Hi","mode":"immediate"}'
```

For delayed jobs, include `"mode":"delayed"` and `"delaySeconds"` or `"atIso"` as appropriate for your own checklist (script checks presence and format only).

## Scripts

- `scripts/detect.js` — whether a message looks like a WhatsApp send/remind request (`isWhatsAppIntent`, `confidence`).
- `scripts/validate.js` — lightweight JSON check for number/message before exec.

## Examples

**User:** "Send a WhatsApp to +49 177 7960262 now: Running late."

→ Exec `send-whatsapp.sh -n '491777960262' -m 'Running late.'`

**User:** "In 20 minutes, WhatsApp me: Time to stretch."

→ `systemd-run --user --on-active=1200s --unit=wa-stretch-$(date +%s)` … `send-whatsapp.sh -n '…' -m 'Time to stretch.'`

**User:** "Every weekday at 8:00 WhatsApp me Good morning."

→ User crontab (minute/hour/dow) calling `send-whatsapp.sh` with `-n` and `-m 'Good morning.'` — **not** OpenClaw cron.

## Relation to the Notify Skill

- **notify** — OpenClaw `cron.add` + `systemEvent` / other channels; includes non-WhatsApp scheduling.
- **whatsapp** — This file: **only** explicit WhatsApp asks; delivery via **`send-whatsapp.sh`** and **system** timers/cron, not an LLM at fire time.
