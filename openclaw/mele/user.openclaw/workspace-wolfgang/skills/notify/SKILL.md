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

**Never schedule a one-time job (`kind: "at"`) less than 30 seconds in the future.**

The cron service discards any `at` job whose timestamp is already in the past at the moment
`cron.add` is processed (`atMs > nowMs ? atMs : undefined` — if past, `nextRunAtMs` is never
set and the job silently never fires). LLM inference + tool call round-trip typically takes
5–15 seconds, so very short delays are unreliable:

- User says "in 1 second" → schedule for **30 seconds** from now and tell the user
- User says "in 10 seconds" → schedule for **30 seconds** from now and tell the user
- User says "in 20 seconds" → schedule for **30 seconds** from now and tell the user
- User says "in 30+ seconds" → use as-is
- User says "in 5 minutes" → use as-is

Always tell the user the actual scheduled time, not the requested time.

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
- `"ACTION: Send a WhatsApp message to +491777960262: Your meeting starts in 15 minutes!"`

Never use vague text like `"Time is up!"` — the agent won't know what to do.

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
