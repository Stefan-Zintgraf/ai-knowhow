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

Never use vague text like `"Time is up!"` or `"Do the thing"`. For **WhatsApp**, do not use this notify/cron path — use the **whatsapp** skill and `send-whatsapp.sh` only.

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

## WhatsApp

Do **not** schedule WhatsApp through OpenClaw cron in this workflow. Use the **whatsapp** skill:
outbound messages only via `/home/dev/proj/ai-knowhow/tools/whatsapp_client/send-whatsapp.sh`
(see `skills/whatsapp/SKILL.md`).

## Common Mistakes to Avoid

1. **sessionTarget inside payload** → Must be at top level
2. **Wrong payload.kind for sessionTarget** → `main` needs `systemEvent`, `isolated` needs `agentTurn`
3. **Missing required fields** → Always include `name`, `schedule`, `payload`, `sessionTarget`
4. **Invalid ISO timestamp** → Use proper timezone offset (+01:00 for Germany, +02:00 in summer)
5. **Vague payload.text** → Must include action + channel + recipient + exact message body
6. **WhatsApp** → Use the **whatsapp** skill and `send-whatsapp.sh` only — not this notify/cron JSON path
