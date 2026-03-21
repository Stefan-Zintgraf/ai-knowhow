# Cron Job Patterns Reference

## Schedule Types

### One-time (at)
```json
{
  "kind": "at",
  "at": "2026-02-27T18:00:00+01:00"
}
```

### Recurring Interval (every)
```json
{
  "kind": "every",
  "everyMs": 3600000
}
```

### Cron Expression
```json
{
  "kind": "cron",
  "expr": "0 8 * * *",
  "tz": "Europe/Berlin"
}
```

## Common Cron Expressions

| Pattern | Expression | Description |
|---------|------------|-------------|
| Every minute | `* * * * *` | Every minute |
| Every hour | `0 * * * *` | At minute 0 of every hour |
| Daily 7am | `0 7 * * *` | Every day at 7:00 AM |
| Weekdays 9am | `0 9 * * 1-5` | Monday-Friday at 9:00 AM |
| Weekly Monday | `0 9 * * 1` | Every Monday at 9:00 AM |
| Monthly 1st | `0 9 1 * *` | 1st of every month at 9:00 AM |

## Payload Types

### System Event (for main session)
```json
{
  "kind": "systemEvent",
  "text": "ACTION: <full self-contained action command>"
}
```
SessionTarget: `main`

**Critical:** The text must be fully self-contained — include action, channel, recipient, and
message body. When this fires, the agent has only this text to act on.

Examples of good `payload.text` values:
- `"ACTION: Send a Telegram message to Stefan: Good morning! Have a great day."`
- `"ACTION: Send an email to stefan@zintgraf.de with subject 'Report' and body: 'Your daily report is ready.'"`
- `"ACTION: Send a WhatsApp message to +491777960262: Your meeting starts in 15 minutes!"`

Never use vague text like `"Time is up!"` or `"Do the thing"`.

### Agent Turn (for isolated session)
```json
{
  "kind": "agentTurn",
  "message": "Send Stefan a daily weather summary via Telegram",
  "model": "openrouter/auto"
}
```
SessionTarget: `isolated`

Use `isolated` for tasks that should run independently (e.g. fetch data and send a report),
without main session context.

## Complete Example — Daily good morning email

```json
{
  "name": "Daily good morning email",
  "schedule": {
    "kind": "cron",
    "expr": "0 7 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "ACTION: Send an email to stefan@zintgraf.de with subject 'Good morning!' and body: 'Good morning, Stefan! Have a great day.'"
  },
  "sessionTarget": "main"
}
```

## WhatsApp — Two-Stage Scheduling

WhatsApp notifications use a two-stage approach. The cron job fires ASAP (15s) and runs
`schedule-send.sh`, which creates a systemd timer for the actual delivery time.

```json
{
  "name": "WhatsApp reminder",
  "schedule": { "kind": "at", "at": "<now + 15s as ISO 8601>" },
  "deleteAfterRun": true,
  "payload": {
    "kind": "agentTurn",
    "message": "Run this exact bash command: /home/dev/proj/ai-knowhow/openclaw/mele/user.openclaw/examples/send_whatsapp/schedule-send.sh --at <ACTUAL_DELIVERY_TIME as ISO 8601> --to +491777960262 \"MESSAGE_TEXT\""
  },
  "sessionTarget": "isolated"
}
```

- `schedule.at`: always **now + 15s** (when stage 1 fires)
- `--at` in the command: the **actual delivery time** (ISO 8601 or epoch seconds)
- If target time has passed by the time stage 1 fires, delivery happens immediately

## Common Mistakes to Avoid

1. **sessionTarget inside payload** → Must be at top level
2. **Wrong payload.kind for sessionTarget** → `main` needs `systemEvent`, `isolated` needs `agentTurn`
3. **Missing required fields** → Always include `name`, `schedule`, `payload`, `sessionTarget`
4. **Invalid ISO timestamp** → Use proper timezone offset (+01:00 for Germany, +02:00 in summer)
5. **Vague payload.text** → Must include action + channel + recipient + exact message body
6. **WhatsApp: using send-safe.sh directly in cron** → Always use `schedule-send.sh` (two-stage); never schedule `send-safe.sh` at the target time via openclaw cron (wastes an LLM loop at delivery)
