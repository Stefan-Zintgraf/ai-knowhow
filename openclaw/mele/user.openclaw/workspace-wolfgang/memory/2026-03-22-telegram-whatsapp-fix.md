# Root cause: Telegram → WhatsApp notification failed (2026-03-22)

**Issue:** User sent a message via Telegram to be notified via WhatsApp. It did not work.

**Root cause:** The `whatsapp` skill was **not registered** in the wolfgang agent's `skills` array in `openclaw.json`. The agent only had `remind` (which pointed to a non-existent `skills/remind/` directory) and had no `notify` or `whatsapp` skills loaded. Therefore:

- When the user said "notify me via WhatsApp", the agent never saw the whatsapp skill instructions
- The agent fell back to `cron.add` with `sessionTarget: "isolated"` and `payload.kind: "agentTurn"`
- That path fails: OpenClaw cron jobs with agentTurn for WhatsApp delivery have historically failed with "Message failed" or "cron delivery target is missing"
- The whatsapp skill prescribes **systemd-run + send-whatsapp.sh** (direct script, no LLM at fire time) — but the agent couldn't follow it because it never had the skill

**Fix applied:** Updated `openclaw.json` to add `notify` and `whatsapp` to the wolfgang agent's skills, and removed the non-existent `remind` entry. Restart the gateway for changes to take effect: `systemctl --user restart openclaw-gateway`.

**Going forward:** For "notify me via WhatsApp" from Telegram, the agent will now have the whatsapp skill and should use `systemd-run --user --on-calendar=...` + `send-whatsapp.sh` instead of OpenClaw cron.

**Update (12:46 retry):** After the fix, user sent another request at 12:46 — still no WhatsApp. Root cause: `whatsapp` was loaded after `notify`; "notify me via WhatsApp" matched notify first and the agent did not properly switch. No `send-whatsapp.sh` call was made (no SENT in wa-sender log). **Fix:** Reordered skills so `whatsapp` comes before `notify`; added explicit "Telegram → WhatsApp" rule in the skill.
