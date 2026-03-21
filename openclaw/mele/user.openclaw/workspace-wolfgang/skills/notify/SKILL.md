---
name: notify
description: Schedule any time-based notification or action via cron. Use when the user wants something to happen at a future time or on a recurring schedule. Triggers include: 'remind me', 'notify me', 'send me a message at', 'in X minutes/hours/days', 'every morning', 'schedule', 'ping me', 'at 9am', 'tomorrow', 'every Monday', or any request involving future or recurring execution.
---

# Notify Skill

This skill schedules any time-based action via cron — reminders, recurring messages, emails,
notifications, or any other deferred task.

## When to Use

Use this skill when:
- User wants something sent or done at a future time: "in 5 minutes", "tomorrow at 9am"
- User wants a recurring action: "every morning", "every Monday"
- User says "remind me", "notify me", "ping me", "schedule"
- User wants a message sent via any channel at a specific time
- Any request involving future or recurring execution

## Workflow

1. **Parse**: Extract from the user's request:
   - What action to perform (send Telegram, send email, send WhatsApp, etc.)
   - When to execute (relative: "in 10 minutes"; absolute: "tomorrow at 10am"; recurring: "every day at 7am")
   - Any relevant details (message text, recipient, channel)

2. **STOP — check required fields before proceeding**:

   You **cannot build the job JSON until all three are known**. If any is missing, ask and wait
   for the answer. Do not proceed to step 3.

   | Required | Example of missing | What to ask |
   |---|---|---|
   | **Channel** (Telegram / WhatsApp / email / other) | "send me a message" | "Via which channel — Telegram, WhatsApp, or email?" |
   | **Message content** | "remind me at 9am" | "What should the message say?" |
   | **Timing** | "send me a WhatsApp" | "When should I send it?" |

   **"send me a message in 2 seconds"** → channel missing → ask, stop, wait. Do not schedule.
   **"remind me tomorrow"** → channel + content missing → ask both, stop, wait.

   The payload.text is written at scheduling time and is the only context available when the
   job fires. A vague or channel-less payload produces a vague or channel-less action.
   **There is no recovery once the job is scheduled with missing information.**

3. **Build job JSON**: Construct the cron job object (see `references/cron-patterns.md`)
   - Use `sessionTarget: "main"` + `payload.kind: "systemEvent"` — fires back into the main
     session where you execute the action
   - Use `sessionTarget: "isolated"` + `payload.kind: "agentTurn"` for standalone tasks

   **Cross-channel rule:** The main session is bound to the channel you're chatting on (e.g.
   Telegram). If the user asks to send a message via a **different** channel, `sessionTarget: "main"`
   will fail with "Cross-context messaging denied". Use `sessionTarget: "isolated"` for those cases.

   **WhatsApp always uses `sessionTarget: "isolated"` regardless of current channel** — see the
   **WhatsApp Rule** section below. Never use `sessionTarget: "main"` for WhatsApp.

4. **Validate**: Run `node skills/notify/scripts/validate.js '<job-json>'` to check the structure

5. **Execute**: Call `cron.add` once to schedule the job — **do not call it twice**

6. **Verify**: Call `cron({ action: "status", jobId: "<returned-id>" })` and check:
   - Job exists → if not, report failure
   - `enabled: true` → if false, report failure
   - `nextRunAtMs` is a number and in the future → **if `undefined` or in the past, the job was
     scheduled with a timestamp that had already elapsed — it will never fire.** In this case:
     delete the job, tell the user the delay was too short for the scheduling round-trip, and
     offer to reschedule with a safe delay (minimum 30 seconds from now)

7. **Confirm**: Report the **actual scheduled time** from `nextRunAtMs` — never the delay the
   user requested. If the delay was bumped (e.g. 2s → 30s), say so explicitly:
   > "Scheduled for 19:05:30 (bumped from 2s to 30s — minimum safe delay for scheduling)"
   Always convert `nextRunAtMs` to a human-readable local time (Europe/Berlin).

## Time Parsing

Convert natural language to ISO timestamps (use `Europe/Berlin` timezone):
- "in 40 seconds" → `new Date(Date.now() + 40000).toISOString()`
- "in 5 minutes" → `new Date(Date.now() + 300000).toISOString()`
- "in 2 hours" → `new Date(Date.now() + 7200000).toISOString()`
- "tomorrow at 9am" → Tomorrow 09:00:00+01:00 (or +02:00 in summer)
- "every morning at 7am" → Cron `0 7 * * *` with `tz: "Europe/Berlin"`

### Minimum Delay — Race Condition Guard

**Never schedule a one-time job (`kind: "at"`) less than 15 seconds in the future.**

The cron service discards any `at` job whose timestamp is already in the past at the moment
`cron.add` is processed (`atMs > nowMs ? atMs : undefined` — if past, `nextRunAtMs` is never
set and the job silently never fires). LLM inference + tool call round-trip typically takes
5–15 seconds, so very short delays are unreliable:

- User says "in 1 second" → schedule cron for **15 seconds** from now and tell the user
- User says "in 10 seconds" → schedule cron for **15 seconds** from now and tell the user
- User says "in 15+ seconds" → use as-is (but never less than 15s)

**For WhatsApp (two-stage):** The cron `schedule.at` is always **now + 15s** regardless of the
user's requested time. The actual delivery time goes in the `--at` argument of `schedule-send.sh`.
Even if the user says "in 5 minutes", stage 1 still fires in 15s — it just schedules the systemd
timer for 5 minutes from the original request time.

Always tell the user the actual scheduled delivery time, not the cron fire time.

## payload.text — Critical Rule

**The `payload.text` must be a self-contained action command.**

When the cron fires, the system injects this text back into the main session. You will only have
this text available — include everything needed to execute the action without any additional context.

The text should start with `ACTION:` for things you need to execute, or be a plain description
of what to do. Include:
- The action (send message, send email, etc.)
- The channel / tool (Telegram, WhatsApp, email, ...)
- The recipient (name, address, phone — whatever the tool needs)
- The exact content to deliver

**Examples:**
- `"ACTION: Send a Telegram message to Stefan: Good morning! Here's your daily check-in."`
- `"ACTION: Send an email to stefan@zintgraf.de with subject 'Daily report' and body: 'Your daily summary is ready.'"`

Never use vague text like `"Time is up!"` — the agent won't know what to do.

**WhatsApp notifications do NOT use `payload.text` / `systemEvent`.** They always use `payload.kind: "agentTurn"` with `sessionTarget: "isolated"`. See the **WhatsApp Rule** section below.

## WhatsApp Rule — Two-Stage Scheduling via schedule-send.sh

The native OpenClaw WhatsApp channel is **unreliable for scheduled/cron delivery** (the watchdog disconnects the listener between messages, and there are no retries as of OpenClaw 2026.3.12). **Never use the message tool for scheduled WhatsApp notifications.**

Instead, use a **two-stage approach** that eliminates the LLM loop at delivery time:

1. **Stage 1 (OpenClaw cron):** Fires ASAP (15s from now) → isolated agent runs `schedule-send.sh`
2. **Stage 2 (systemd timer):** `schedule-send.sh` creates a transient systemd timer that fires
   `send-safe.sh` at the exact target time — no LLM involved at delivery.

If the target time has already passed by the time stage 1 fires (e.g. user said "in 10 seconds"
but LLM inference took 15s), the systemd timer fires **immediately** — delivery is late but
**guaranteed**.

### Required structure for ALL WhatsApp notifications

```json
{
  "name": "descriptive name",
  "schedule": { "kind": "at", "at": "<15 seconds from now — ISO timestamp>" },
  "deleteAfterRun": true,
  "payload": {
    "kind": "agentTurn",
    "message": "Run this exact bash command: /home/dev/proj/ai-knowhow/openclaw/mele/user.openclaw/examples/send_whatsapp/schedule-send.sh --at TARGET_ISO_TIMESTAMP --to +491777960262 \"MESSAGE_TEXT_HERE\""
  },
  "sessionTarget": "isolated"
}
```

**Critical:** The `schedule.at` is always **15 seconds from now** (fires ASAP to launch the
scheduler). The **actual delivery time** goes in the `--at` argument of `schedule-send.sh`.

**Rules — no exceptions:**

| Rule | Value |
|---|---|
| `sessionTarget` | **always `"isolated"`** — never `"main"` |
| `payload.kind` | **always `"agentTurn"`** — never `"systemEvent"` |
| `schedule.at` | **always "now + 15s"** — this is when stage 1 fires, NOT the delivery time |
| `--at` in command | The **actual target delivery time** as ISO 8601 or epoch seconds |
| `payload.message` | Must contain the **exact bash command** with `schedule-send.sh` |
| Recipient | Replace `+491777960262` with the actual number if different |
| Message text | Replace `MESSAGE_TEXT_HERE` with the actual text; escape any `"` inside as `\"` |

The isolated agent receives the `message` and **runs it as a bash command — no reasoning, no
tool selection, just execute**. This is intentional and makes it work even with weak LLM models.

### How it works

```
User: "send WhatsApp in 5 minutes: Hallo"
  → cron.add: fires in 15s (stage 1)
    → isolated agent runs: schedule-send.sh --at <now+5min ISO> --to +49... "Hallo"
      → systemd-run --on-active=285s send-safe.sh --to +49... "Hallo"
        → [5 min later] send.ts sends via Baileys — no LLM involved
```

`schedule-send.sh` computes the delay from now to the `--at` target and creates a `systemd-run
--user --on-active=<delay>s` timer. If the target is in the past, delay is 0 (fires immediately).

### Why this two-stage approach?

The old approach had the openclaw cron fire an `agentTurn` at the target time, which then called
`send-safe.sh`. This meant an LLM had to spin up at delivery time just to run one bash command —
adding 5-15s latency, wasting API tokens, and depending on exec allowlists and LLM compliance.

The two-stage approach:
- **No LLM at delivery time** — systemd fires the script directly
- **No exec allowlist dependency at delivery** — systemd owns the process
- **Guaranteed delivery** — even if stage 1 is late, the message still fires (immediately if past)
- **Sub-second precision** — `--on-active` uses monotonic timers, not minute-resolution calendars

### Why `send-safe.sh` and not `send.ts` directly?

`send-safe.sh` launches `send.ts` via `systemd-run --user` in a **transient unit with
`OPENCLAW_SYSTEMD_UNIT=` (empty)** so `send.ts` does **not** stop the gateway. This prevents the
gateway from being killed before persisting job completion.

### Exec allowlist (required for stage 1)

The stage-1 cron agent runs `schedule-send.sh` via the exec tool. Add to the allowlist:

- **File:** `~/.openclaw/exec-approvals.json`
- **Per-agent allowlist:** Under `agents.wolfgang.allowlist` add entries for:
  - `/home/dev/proj/ai-knowhow/openclaw/mele/user.openclaw/examples/send_whatsapp/schedule-send.sh`
  - `/usr/bin/bash` (or `/bin/bash`) so the shell that runs the script is allowed

### If WhatsApp cron keeps firing (loop)

If a job is stuck (enabled, `runningAtMs` set but no `lastStatus`), disable it:
`openclaw cron disable <jobId>` or set `enabled: false` in `mele/user.openclaw/cron/jobs.json`
and restart the gateway.

## Job JSON Structure

```json
{
  "name": "descriptive name",
  "schedule": { "kind": "at", "at": "<ISO timestamp>" },
  "payload": { "kind": "systemEvent", "text": "ACTION: <full action description>" },
  "sessionTarget": "main"
}
```

See `references/cron-patterns.md` for all schedule types and examples.

## Scripts

- `scripts/detect.js` - Check if a message is a scheduling/notification request (returns `{isNotification, confidence}`)
- `scripts/validate.js` - Validate cron job JSON structure before calling `cron.add`

## Examples

**"Send me a Telegram message in 10 minutes"**
```json
{
  "name": "Telegram in 10 min",
  "schedule": { "kind": "at", "at": "<now+600s>" },
  "payload": { "kind": "systemEvent", "text": "ACTION: Send a Telegram message to Stefan: Your 10 minutes are up!" },
  "sessionTarget": "main"
}
```

**"Send me a good morning email every day at 7am"**
```json
{
  "name": "Daily good morning email",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "Europe/Berlin" },
  "payload": { "kind": "systemEvent", "text": "ACTION: Send an email to stefan@zintgraf.de with subject 'Good morning!' and body: 'Good morning, Stefan! Have a great day.'" },
  "sessionTarget": "main"
}
```

**"Send a Telegram message tomorrow at 10am"**
```json
{
  "name": "Telegram tomorrow 10am",
  "schedule": { "kind": "at", "at": "<tomorrow 10:00+01:00>" },
  "payload": { "kind": "systemEvent", "text": "ACTION: Send a Telegram message to Stefan: Good morning! This is your scheduled message." },
  "sessionTarget": "main"
}
```

**"Send me a WhatsApp message at 21:55"** (works regardless of which channel you're chatting on)
```json
{
  "name": "WhatsApp 21:55",
  "schedule": { "kind": "at", "at": "<now + 15s>" },
  "deleteAfterRun": true,
  "payload": {
    "kind": "agentTurn",
    "message": "Run this exact bash command: /home/dev/proj/ai-knowhow/openclaw/mele/user.openclaw/examples/send_whatsapp/schedule-send.sh --at <today 21:55+01:00 as ISO 8601> --to +491777960262 \"<the message content>\""
  },
  "sessionTarget": "isolated"
}
```

**"Send me a WhatsApp in 30 seconds: Hallo"** (short delay — stage 1 fires ASAP, stage 2 may fire immediately if target passed)
```json
{
  "name": "WhatsApp in 30s",
  "schedule": { "kind": "at", "at": "<now + 15s>" },
  "deleteAfterRun": true,
  "payload": {
    "kind": "agentTurn",
    "message": "Run this exact bash command: /home/dev/proj/ai-knowhow/openclaw/mele/user.openclaw/examples/send_whatsapp/schedule-send.sh --at <now+30s as ISO 8601> --to +491777960262 \"Hallo\""
  },
  "sessionTarget": "isolated"
}
```
