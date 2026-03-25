---
description: "BMAD Phase 1: Skill-based brainstorming integration for the wolfgang workspace"
name: bmad-brainstorm-skill
---

# BMAD → OpenClaw — Phase 1: Skill Integration

Version: 4.0
Purpose: Machine-executable build instructions for the **wolfgang** workspace

---

# 0. OBJECTIVE

Add a `bmad-brainstorm` skill to the **wolfgang** agent that enables structured
brainstorming, idea refinement, and concept validation via any connected channel
(Telegram, WhatsApp, voice).

The skill registers a single slash command `/bmad-brainstorm` (derived from
its `name` field). It also responds to prefixed commands (`bmad brainstorm`,
`bmad discuss`, `bmad refine`, `bmad validate`) and natural language
("let's brainstorm", "can we discuss", "help me think through").

**Note:** OpenClaw skills can only register one slash command — the skill
name itself. Convenience aliases like `/brainstorm`, `/discuss`, `/refine`,
and `/validate` require a plugin and are covered in a separate spec:
`BMAD_Phase2_Plugin_spec.md`.

---

# 1. AGENT INSTRUCTIONS — READ THIS FIRST

You are implementing this spec **autonomously**. Follow each numbered step in
order. Do NOT skip steps. Do NOT ask for human confirmation between steps.

**Workflow:**

1. Read the ENVIRONMENT section to orient yourself.
2. Read one existing skill (e.g. `workspace-wolfgang/skills/greet/SKILL.md`)
   to see the concrete pattern you must follow.
3. Execute all IMPLEMENTATION STEPS (section 3) in order.
4. Run the VALIDATION CHECKLIST (section 4) — every box must pass.
5. Create the test script and run full automated tests (section 5).
6. If any test fails, diagnose, fix, and re-run until ALL tests pass.
7. Only report "done" when the test script exits with code 0.

**Rules:**

- Follow existing skill patterns in the workspace (`backup`, `greet`, `remind`).
  Read at least one before writing yours.
- Register the skill in `openclaw.json` so it loads at startup.
- Do NOT invent CLI commands — use the real config and systemd restart.
- Do NOT hardcode model names — use whatever model the agent is configured with.
- All file paths are relative to `${OPENCLAW_STATE_DIR}` (`mele/user.openclaw`).
- If you encounter an error, fix it and retry. Do not give up or ask for help
  unless you have attempted at least 3 different fixes.

---

# 2. ENVIRONMENT

| Item | Value |
|---|---|
| State dir (`OPENCLAW_STATE_DIR`) | `mele/user.openclaw` |
| Agent | `wolfgang` (default agent) |
| Workspace | `${OPENCLAW_STATE_DIR}/workspace-wolfgang` |
| Existing skills | `backup`, `greet`, `testnode-skill`, `remind` (in `workspace-wolfgang/skills/`) |
| Config file | `${OPENCLAW_STATE_DIR}/openclaw.json` |
| Channels | Telegram (`wolfgang` account), WhatsApp (`default` account) — both already bound |
| Audio | Groq Whisper `whisper-large-v3` — voice messages are auto-transcribed |
| Gateway restart | `systemctl --user restart openclaw-gateway` |
| Test client | `examples/gateway_clients/claw_client/claw_client.py` (with venv) |
| Test spec | `plans/BMAD_Phase1_Skill_test.md` — full test plan and reference script |

### openclaw.json structure (important)

The agent config is NOT a flat dict. The structure is:

```json
{
  "agents": {
    "list": [
      {
        "id": "wolfgang",
        "name": "wolfgang",
        "skills": ["backup", "greet", "testnode-skill", "remind"],
        ...
      }
    ]
  }
}
```

You must find the object in `agents.list[]` where `id` equals `"wolfgang"`
and append `"bmad-brainstorm"` to its `skills` array. Do NOT create a new agent
object. Do NOT change any other fields.

### How skills are loaded

At gateway startup, for each skill name in the agent's `skills` array, the
gateway reads `<workspace>/skills/<name>/SKILL.md` and injects its content
into the agent's system prompt. If the file is missing or the name is not in
the `skills` array, the agent never sees the skill.

---

# 3. IMPLEMENTATION STEPS

Execute these steps in order. Each step lists the exact action and the
expected outcome.

## Step 1 — Read an existing skill for reference

Read `workspace-wolfgang/skills/greet/SKILL.md` to see the concrete file
format: YAML front-matter followed by markdown instructions.

**Expected outcome:** You understand the pattern — `---` delimited YAML
with `name`, `description`, `user-invocable`, then free-form markdown.

## Step 2 — Create the skill directory

```bash
mkdir -p workspace-wolfgang/skills/bmad-brainstorm
```

**Expected outcome:** Directory exists.

## Step 3 — Create SKILL.md

**File:** `workspace-wolfgang/skills/bmad-brainstorm/SKILL.md`

Write this file with **exactly** the following content:

```markdown
---
name: bmad-brainstorm
description: >-
  BMAD structured brainstorming skill. Triggers via /bmad-brainstorm slash
  command, natural language ("let's brainstorm", "can we discuss", "help me
  think through"), or prefixed commands ("bmad brainstorm", "bmad discuss").
  Additional slash commands (/brainstorm, /discuss, /refine, /validate) are
  available when the Phase 2 plugin is installed.
user-invocable: true
---

# BMAD — Structured Brainstorming & Discussion

You are operating under the BMAD methodology — a structured brainstorming,
discussion, and idea development framework.

## Triggers

Activate this skill when the user message matches any of:

### Slash command
- `/bmad-brainstorm` — the registered skill command (with optional arguments)

### Prefixed commands (bmad qualifier)
- `bmad brainstorm <topic>`, `bmad discuss <topic>`
- `bmad refine <idea>`, `bmad validate <concept>`
- `bmad help`

### Natural language
- "let's brainstorm", "help me brainstorm", "brainstorm session"
- "let's discuss", "can we discuss", "discuss this idea"
- "help me think through", "think through this with me"

Do NOT activate on just "bmad" alone — that is too generic.

## Commands

### help (bmad help)

Explain:
- BMAD philosophy (structured brainstorming → refinement → validation)
- Available modes: brainstorm/discuss, refine, validate
- How to invoke (e.g. `bmad brainstorm AI-powered robotics`,
  or `let's brainstorm about AI-powered robotics`)

### brainstorm / discuss <topic>

1. Clarify the objective — ask if the topic is ambiguous or missing
2. Define constraints (time, budget, technology, scope)
3. Generate 3–7 structured idea clusters
4. Expand the top 3 ideas with pros, cons, and feasibility
5. **Recommend concrete next actions** — always include a
   "Recommended Next Steps" or "Recommended Actions" section at the end

Output with clear headings, bullet clusters, and action steps.
You MUST always include the words "Recommended" and "Next" in a heading
for the action items.

### refine <idea>

1. Restate the idea clearly
2. Identify weaknesses and blind spots
3. Improve clarity and positioning
4. Suggest iteration steps and alternatives

### validate <concept>

1. List underlying assumptions
2. Identify failure risks and edge cases
3. Suggest low-cost experiments to test the concept
4. Propose validation metrics and success criteria
```

**Expected outcome:** File exists at the correct path with valid YAML
front-matter and all command sections.

## Step 4 — Register the skill in openclaw.json

Edit `${OPENCLAW_STATE_DIR}/openclaw.json`:

1. Parse the JSON.
2. In `agents.list`, find the object where `id` equals `"wolfgang"`.
3. Append `"bmad-brainstorm"` to its `skills` array (if not already present).
4. Write the file back, preserving all other fields and formatting.

**Before:**

```json
"skills": [
  "backup",
  "greet",
  "testnode-skill",
  "remind"
]
```

**After:**

```json
"skills": [
  "backup",
  "greet",
  "testnode-skill",
  "remind",
  "bmad-brainstorm"
]
```

**Expected outcome:** `"bmad-brainstorm"` appears in the skills array and no
other fields were modified.

## Step 5 — Restart the gateway

```bash
systemctl --user restart openclaw-gateway
```

Wait 5 seconds, then verify:

```bash
systemctl --user status openclaw-gateway
```

**Expected outcome:** Output contains `active (running)`.

If the gateway fails to start, check the journal for errors:

```bash
journalctl --user -u openclaw-gateway -n 30 --no-pager
```

Fix any issues (usually a JSON syntax error in `openclaw.json`) and retry.

---

# 4. VALIDATION CHECKLIST

Run these checks immediately after completing the implementation steps.
Every item must pass before moving to the test phase.

- [ ] `workspace-wolfgang/skills/bmad-brainstorm/SKILL.md` exists and is non-empty
- [ ] YAML front-matter has `name: bmad-brainstorm`, `description:` (non-empty),
      `user-invocable: true`
- [ ] File body contains `/bmad-brainstorm` as the registered slash command
- [ ] File body contains `brainstorm`, `refine`, `validate` as subcommand instructions
- [ ] File body does NOT treat bare `bmad` alone as a trigger
- [ ] `openclaw.json` → `agents.list[]` → `id: "wolfgang"` → `skills` array
      contains `"bmad-brainstorm"`
- [ ] Gateway restarted successfully (`active (running)`)

---

# 5. TESTING — CREATE SCRIPT AND RUN UNTIL GREEN

After the validation checklist passes, you MUST create and run a comprehensive
test script. This is NOT optional.

## 5.1 Read the test spec

Read the file `plans/BMAD_Phase1_Skill_test.md`. It contains:

- The full test plan with all static and behavioral test cases
- A complete reference Python test script
- Instructions for running tests and interpreting results

## 5.2 Create the test script

Extract the Python test script from section 5 ("Reference Test Script") of
`BMAD_Phase1_Skill_test.md` and save it to:

```
examples/gateway_clients/claw_client/bmad_phase1_test.py
```

Make it executable: `chmod +x` the file.

## 5.3 Run the tests

```bash
cd mele/user.openclaw/examples/gateway_clients/claw_client
source venv_activate.sh
python bmad_phase1_test.py
```

## 5.4 Fix and re-run until all tests pass

If any test fails:

1. Read the PASS/FAIL/SKIP output carefully.
2. Diagnose the root cause using the troubleshooting table in the test spec
   (section 6.4, "Interpreting results as an agent").
3. Fix the issue (edit SKILL.md, openclaw.json, restart gateway, etc.).
4. Re-run `python bmad_phase1_test.py`.
5. Repeat until exit code is 0 (all tests pass).

**Common fixes:**

| Failure pattern | Fix |
|---|---|
| Static checks fail on SKILL.md | Re-read step 3 and fix the file content |
| Static checks fail on openclaw.json | Re-read step 4 and fix the JSON |
| Gateway not running after restart | Check `journalctl --user -u openclaw-gateway -n 30` |
| Behavioral tests timeout | Gateway may need more time — wait 10s and retry |
| Behavioral tests: empty/generic responses | Skill not loaded — verify static checks pass, then restart gateway |
| Behavioral tests: keyword assertions fail | Refine the SKILL.md instructions to be more explicit about output format |

## 5.5 Completion criteria

You are done ONLY when:

```
Results: N passed, 0 failed, 0 skipped
```

and the script exits with code 0. Report the final test output to confirm.

---

# 6. ARCHITECTURE RULES

- BMAD logic MUST reside in the skill layer (`SKILL.md`).
- Telegram and WhatsApp are transport layers only — no channel-specific logic.
- No hardcoded model names — use whatever model the agent is configured with.
- No undocumented OpenClaw features — follow existing patterns from `backup`, `greet`.
- All file paths relative to `${OPENCLAW_STATE_DIR}` or the workspace root.

---

# 7. FILES SUMMARY

| File | Action | Purpose |
|---|---|---|
| `workspace-wolfgang/skills/bmad-brainstorm/SKILL.md` | Create | Skill instructions |
| `openclaw.json` (agent `skills` array) | Edit | Register skill for loading |
| `examples/gateway_clients/claw_client/bmad_phase1_test.py` | Create | Automated test script |
| `plans/BMAD_Phase1_Skill_test.md` | Read | Test plan and reference script |

---

# 8. DEFINITION OF DONE

All of the following must be true:

1. `SKILL.md` created with correct content and YAML front-matter.
2. `"bmad-brainstorm"` registered in `openclaw.json` wolfgang agent skills.
3. Gateway restarted and running.
4. `bmad_phase1_test.py` created from the test spec reference script.
5. Test script executed with **0 failures and 0 skips**.
6. Final test output reported.

Do NOT report completion until condition 5 is met.

---

END OF SPECIFICATION
