---
description: "BMAD Phase 1: Test instructions for validating the bmad-brainstorm skill"
name: bmad-brainstorm-skill-test
requires: BMAD_Phase1_Skill_spec.md
---

# BMAD Phase 1 — Test Instructions

Version: 3.0
Purpose: Machine-executable test plan for verifying the `bmad-brainstorm` skill
deployment in the **wolfgang** workspace.

Tests are split into three stages:

1. **Pre-flight** — gateway health and environment sanity
2. **Static checks** — file layout and configuration (no running gateway needed)
3. **Behavioral checks** — send prompts via the gateway and assert on responses

---

# 0. CONTEXT — What You Are Testing

This test plan validates the **bmad-brainstorm** skill as specified in
`BMAD_Phase1_Skill_spec.md`. That spec defines a brainstorming skill for the
**wolfgang** agent in the OpenClaw framework. The skill:

- Lives at `workspace-wolfgang/skills/bmad-brainstorm/SKILL.md`
- Must be registered in `openclaw.json` under the `wolfgang` agent's `skills` array
- Registers `/bmad-brainstorm` as its slash command (the only real slash command
  from the skill — additional slash commands like `/brainstorm` require the
  Phase 2 plugin)
- Responds to prefixed commands: `bmad brainstorm`, `bmad discuss`, `bmad refine`,
  `bmad validate`, `bmad help`
- Responds to natural language triggers: "let's brainstorm", "can we discuss",
  "help me think through", etc.
- Does NOT trigger on bare `bmad` alone (too generic)
- Produces structured output with headings, bullet clusters, and action steps

The skill file follows the standard OpenClaw SKILL.md pattern: YAML front-matter
(`name`, `description`, `user-invocable`) followed by natural-language LLM instructions.

### How the agent loads skills

At startup the gateway reads `openclaw.json`, finds the `wolfgang` agent in
`agents.list[]`, loads each skill name from its `skills` array by reading
`<workspace>/skills/<name>/SKILL.md`, and injects those instructions into the
agent's system prompt. A missing file or missing registration means the agent
never sees the skill.

### How behavioral tests work

The `claw_client` library opens a WebSocket to the OpenClaw gateway,
authenticates with Ed25519 device identity, sends a `chat.send` RPC, and
collects streamed token deltas until the agent run completes. The response
is returned as a `ClawResponse` with `.text`, `.run_id`, `.elapsed_seconds`.

---

# 1. PREREQUISITES

| Requirement | Details |
|---|---|
| Build spec | `BMAD_Phase1_Skill_spec.md` must have been executed first |
| State dir | `OPENCLAW_STATE_DIR` = `mele/user.openclaw` |
| claw_client | `examples/gateway_clients/claw_client/claw_client.py` (with venv) |
| Gateway token | `OPENCLAW_GATEWAY_TOKEN` set in environment or claw_client `.env` |
| Gateway running | `systemctl --user status openclaw-gateway` shows active |

### Agent interactive testing — quick start

If you are an AI agent with shell access and want to test interactively:

```bash
# 1. Check gateway health
systemctl --user status openclaw-gateway

# 2. Activate the claw_client venv
cd mele/user.openclaw/examples/gateway_clients/claw_client
source venv_activate.sh

# 3. Run the full automated test suite
python bmad_phase1_test.py

# 4. Or send individual prompts and inspect output
python claw_client.py --session bmad-test "/bmad-brainstorm help"
python claw_client.py --session bmad-test "bmad brainstorm AI robotics"
```

For programmatic testing in Python:

```python
import sys
sys.path.insert(0, "mele/user.openclaw/examples/gateway_clients/claw_client")
from claw_client import prompt_sync
r = prompt_sync("/bmad-brainstorm help", session_key="agent-test", timeout=180)
print(r.text)
```

---

# 2. PRE-FLIGHT CHECKS

These verify the environment is ready before running any tests.

## 2.0 Gateway is running

```bash
systemctl --user status openclaw-gateway
```

Assert: output contains `active (running)`. If not, restart with
`systemctl --user restart openclaw-gateway` and wait 5 seconds.

## 2.1 Gateway token is configured

Assert: `OPENCLAW_GATEWAY_TOKEN` is set (non-empty) in the environment or in
`examples/gateway_clients/claw_client/.env`.

## 2.2 claw_client is importable

```python
from claw_client import prompt_sync, ClawResponse
```

Assert: no ImportError. If it fails, activate the venv:
`source examples/gateway_clients/claw_client/venv_activate.sh`

---

# 3. STATIC CHECKS

These verify that the implementation created the right files with the right
content. They do **not** require the gateway to be running and can be performed
with standard file operations.

## 3.1 SKILL.md exists

```
workspace-wolfgang/skills/bmad-brainstorm/SKILL.md
```

Assert: file exists and is non-empty.

## 3.2 YAML front-matter is correct

The first lines of `SKILL.md` must contain valid YAML front-matter with at
minimum these fields:

```yaml
---
name: bmad-brainstorm
description: <non-empty string mentioning "brainstorm">
user-invocable: true
---
```

Assert:
- `name` equals `bmad-brainstorm` (exact match, accounting for quoting)
- `description` is present and non-empty (may use YAML folded/block scalar `>-` or `|`)
- `user-invocable` is `true`

## 3.3 Skill body contains required sections

The markdown body (below the front-matter) must mention:

- `/bmad-brainstorm` (the registered slash command)
- `brainstorm` (subcommand / mode)
- `refine` (subcommand / mode)
- `validate` (subcommand / mode)

Assert: each of the four strings appears at least once in the file.

## 3.4 openclaw.json registers the skill

In `${OPENCLAW_STATE_DIR}/openclaw.json`, the `wolfgang` agent's `skills`
array must include `"bmad-brainstorm"`.

The `openclaw.json` structure uses:

```json
{
  "agents": {
    "list": [
      { "id": "wolfgang", "skills": ["backup", "greet", ...] }
    ]
  }
}
```

Assert: in the `agents.list` array, the object with `"id": "wolfgang"` has
`"bmad-brainstorm"` in its `skills` array.

---

# 4. BEHAVIORAL CHECKS

These send real prompts to the running agent via `claw_client` and assert on
the response text. They require the gateway to be running with the updated
config (i.e. after `systemctl --user restart openclaw-gateway`).

All behavioral tests use a dedicated session key (`bmad-phase1-test`) to isolate
test conversation context from other sessions. Each test run should use a unique
session key (e.g. with a timestamp suffix) to avoid context bleed from prior runs.

### Interpreting failures

- **Response is empty or very short** → skill not loaded (check static checks)
- **Response ignores the command** → triggers not matching (check SKILL.md trigger list)
- **Response is relevant but missing structure** → skill loaded but instructions need refinement
- **Timeout** → gateway overloaded or agent stuck (check `systemctl --user status openclaw-gateway`)

## 4.1 Test: /bmad-brainstorm help (skill slash command)

**Prompt:** `/bmad-brainstorm help`

**Expected:** The response explains the BMAD framework and lists the available
modes. Assert ALL of the following substrings appear (case-insensitive) in
the response text:

- `brainstorm`
- `refine`
- `validate`

**Pass criteria:** All three substrings found, response length > 100 characters.

## 4.2 Test: bmad brainstorm <topic> (prefixed command)

**Prompt:** `bmad brainstorm AI-powered home automation`

**Expected:** A structured brainstorming output with multiple idea clusters,
pros/cons, and action steps. Assert ALL of the following:

- Response length > 300 characters (structured output is substantial)
- At least one of: `idea`, `cluster`, `concept`, `approach` (case-insensitive)
- At least one of: `pro`, `con`, `advantage`, `disadvantage`, `feasibility`
  (case-insensitive)
- At least one of: `next step`, `action`, `recommend` (case-insensitive)

**Pass criteria:** All assertion groups pass.

## 4.3 Test: bmad discuss <topic> (prefixed command)

**Prompt:** `bmad discuss sustainable packaging alternatives for e-commerce`

**Expected:** The `bmad discuss` prefix should produce brainstorming output just
like `bmad brainstorm`. Assert ALL of:

- Response length > 300 characters
- At least one of: `idea`, `concept`, `approach`, `option`, `alternative`
  (case-insensitive)

**Pass criteria:** All assertion groups pass.

## 4.4 Test: bmad refine <idea> (prefixed command)

**Prompt:** `bmad refine A voice-controlled smart mirror that displays calendar, weather, and news`

**Expected:** The response restates the idea, identifies weaknesses, and
suggests improvements. Assert ALL of:

- Response length > 200 characters
- At least one of: `weakness`, `blind spot`, `limitation`, `risk`, `challenge`
  (case-insensitive)
- At least one of: `improve`, `iteration`, `alternative`, `suggestion`,
  `refinement` (case-insensitive)

**Pass criteria:** All assertion groups pass.

## 4.5 Test: bmad validate <concept> (prefixed command)

**Prompt:** `bmad validate A subscription service for AI-generated bedtime stories for children`

**Expected:** The response lists assumptions, failure risks, and validation
experiments. Assert ALL of:

- Response length > 200 characters
- At least one of: `assumption`, `hypothes` (case-insensitive)
- At least one of: `risk`, `failure`, `edge case` (case-insensitive)
- At least one of: `experiment`, `test`, `metric`, `validation`, `measure`
  (case-insensitive)

**Pass criteria:** All assertion groups pass.

## 4.6 Test: natural language trigger (no bmad word)

**Prompt:** `I'd like to discuss ideas for a community garden project`

**Expected:** The skill activates from natural "discuss" language without
any `/command` or `bmad` prefix and produces structured brainstorming output.
Assert:

- Response length > 200 characters
- At least one of: `garden`, `community`, `idea`, `concept`
  (case-insensitive)

**Pass criteria:** Both assertions pass, confirming natural language activation
without the word "bmad".

## 4.7 Test: natural language "brainstorm" trigger (no bmad word)

**Prompt:** `Let's brainstorm about decentralized identity systems`

**Expected:** The skill activates from natural "brainstorm" language without
any `bmad` prefix. Assert:

- Response length > 200 characters
- At least one of: `identity`, `decentralized`, `idea`, `concept`
  (case-insensitive)

**Pass criteria:** Both assertions pass.

## 4.8 Test: "help me think through" trigger (no bmad word)

**Prompt:** `Help me think through the pros and cons of remote work policies`

**Expected:** The skill activates from the "think through" natural language
trigger. Assert:

- Response length > 200 characters
- At least one of: `remote`, `work`, `pro`, `con` (case-insensitive)

**Pass criteria:** Both assertions pass.

## 4.9 Test: bmad brainstorm (additional prefixed command)

**Prompt:** `bmad brainstorm renewable energy storage solutions`

**Expected:** The `bmad brainstorm` prefix triggers the skill. Assert:

- Response length > 300 characters
- At least one of: `energy`, `storage`, `idea`, `concept`, `approach`
  (case-insensitive)

**Pass criteria:** Both assertions pass.

## 4.10 Test: edge case — /bmad-brainstorm with no topic

**Prompt:** `/bmad-brainstorm`

**Expected:** Per the spec, the agent should "clarify the objective — ask if
the topic is ambiguous". With no topic at all, it should ask for one.

**Assertions:**
- Response length > 50 characters
- At least one of: `topic`, `what`, `about`, `specify`, `provide`, `?`
  (case-insensitive) — indicating a clarification question

**Pass criteria:** Both assertions pass.

---

# 5. REFERENCE TEST SCRIPT

The following Python script implements all checks from sections 2–4 using
the `claw_client` library API. An AI agent or human can execute it directly.

**Save as:** `examples/gateway_clients/claw_client/bmad_phase1_test.py`

**Run from:** the `examples/gateway_clients/claw_client/` directory with the
venv active.

```python
#!/usr/bin/env python3
"""
BMAD Phase 1 — automated test script.

Validates the bmad-brainstorm skill: environment pre-flight, file layout,
openclaw.json registration, and live agent responses via the gateway.

Usage:
    cd mele/user.openclaw/examples/gateway_clients/claw_client
    source venv_activate.sh
    python bmad_phase1_test.py                # run all stages
    python bmad_phase1_test.py --static-only  # skip behavioral tests
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# ── paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
STATE_DIR = SCRIPT_DIR.parents[2]  # mele/user.openclaw

SKILL_FILE = STATE_DIR / "workspace-wolfgang" / "skills" / "bmad-brainstorm" / "SKILL.md"
CONFIG_FILE = STATE_DIR / "openclaw.json"

TIMEOUT = 180  # seconds per prompt; agent runs can be slow


# ── helpers ───────────────────────────────────────────────────────────────────

passed = 0
failed = 0
skipped = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        msg = f"  FAIL  {name}"
        if detail:
            msg += f"  ({detail})"
        print(msg)
    return condition


def skip(name: str, reason: str) -> None:
    global skipped
    skipped += 1
    print(f"  SKIP  {name}  ({reason})")


def any_present(text: str, keywords: list[str]) -> bool:
    lower = text.lower()
    return any(kw.lower() in lower for kw in keywords)


def unique_session_key() -> str:
    return f"bmad-phase1-test-{int(time.time())}"


# ── stage 0: pre-flight ──────────────────────────────────────────────────────

def run_preflight() -> bool:
    print("\n=== Stage 0: Pre-flight Checks ===\n")

    # 0.1 Gateway token
    token = os.getenv("OPENCLAW_GATEWAY_TOKEN", "")
    if not token:
        env_file = SCRIPT_DIR / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("OPENCLAW_GATEWAY_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip("'\"")
    check("0.1 OPENCLAW_GATEWAY_TOKEN set", bool(token))

    # 0.2 Gateway running
    gateway_ok = False
    try:
        result = subprocess.run(
            ["systemctl", "--user", "status", "openclaw-gateway"],
            capture_output=True, text=True, timeout=10,
        )
        gateway_ok = "active (running)" in result.stdout
    except Exception:
        pass
    check("0.2 Gateway is running", gateway_ok,
          "run: systemctl --user restart openclaw-gateway")

    # 0.3 claw_client importable
    try:
        from claw_client import prompt_sync  # noqa: F401
        check("0.3 claw_client importable", True)
    except ImportError as e:
        check("0.3 claw_client importable", False, str(e))
        return False

    return gateway_ok


# ── stage 1: static checks ───────────────────────────────────────────────────

def run_static_checks() -> bool:
    print("\n=== Stage 1: Static Checks ===\n")

    # 1.1 SKILL.md exists
    if not check("1.1 SKILL.md exists", SKILL_FILE.exists()):
        print("       Cannot continue static checks without SKILL.md")
        return False

    content = SKILL_FILE.read_text()
    check("1.1a SKILL.md is non-empty", len(content.strip()) > 0)

    # 1.2 YAML front-matter
    fm_match = re.match(r"^---\s*\n(.+?)\n---", content, re.DOTALL)
    check("1.2 YAML front-matter block present", fm_match is not None)
    if fm_match:
        fm = fm_match.group(1)
        name_ok = bool(re.search(r"name:\s*['\"]?bmad-brainstorm['\"]?", fm))
        check("1.2a name: bmad-brainstorm", name_ok)
        desc_ok = bool(re.search(r"description:\s*\S", fm))
        check("1.2b description present", desc_ok)
        invocable_ok = bool(re.search(r"user-invocable:\s*true", fm))
        check("1.2c user-invocable: true", invocable_ok)

    # 1.3 Required strings in body
    check("1.3 body contains '/bmad-brainstorm'", "/bmad-brainstorm" in content)
    for keyword in ["brainstorm", "refine", "validate"]:
        check(f"1.3 body contains '{keyword}'", keyword in content)

    # 1.4 openclaw.json registration
    if not check("1.4 openclaw.json exists", CONFIG_FILE.exists()):
        return True

    try:
        cfg = json.loads(CONFIG_FILE.read_text())
    except json.JSONDecodeError as e:
        check("1.4 openclaw.json valid JSON", False, str(e))
        return True

    agents_section = cfg.get("agents", {})
    agent_list = agents_section.get("list", [])
    wolfgang = next((a for a in agent_list if a.get("id") == "wolfgang"), None)
    if wolfgang is None:
        check("1.4a wolfgang agent found in agents.list", False,
              "looked for object with id='wolfgang' in agents.list[]")
    else:
        check("1.4a wolfgang agent found in agents.list", True)
        skills = wolfgang.get("skills", [])
        check("1.4b 'bmad-brainstorm' in wolfgang skills",
              "bmad-brainstorm" in skills,
              f"current skills: {skills}")

    return True


# ── stage 2: behavioral checks ───────────────────────────────────────────────

def run_behavioral_checks() -> None:
    print("\n=== Stage 2: Behavioral Checks ===\n")

    try:
        from claw_client import prompt_sync
    except ImportError:
        skip("all behavioral", "claw_client not importable")
        return

    session = unique_session_key()
    print(f"  Session key: {session}\n")

    def send(label: str, prompt: str) -> str | None:
        print(f"  [{label}] Sending: {prompt[:70]}{'...' if len(prompt) > 70 else ''}")
        try:
            r = prompt_sync(prompt, session_key=session, timeout=TIMEOUT)
            print(f"         Response: {len(r.text)} chars, {r.elapsed_seconds:.1f}s")
            return r.text
        except Exception as e:
            check(f"{label} prompt succeeded", False, str(e))
            return None

    # 2.1 /bmad-brainstorm help (skill slash command)
    text = send("2.1", "/bmad-brainstorm help")
    if text is not None:
        check("2.1 response length > 100", len(text) > 100, f"got {len(text)} chars")
        check("2.1 mentions 'brainstorm'", any_present(text, ["brainstorm"]))
        check("2.1 mentions 'refine'", any_present(text, ["refine"]))
        check("2.1 mentions 'validate'", any_present(text, ["validate"]))
    else:
        skip("2.1 assertions", "no response")

    # 2.2 bmad brainstorm <topic> (prefixed command)
    text = send("2.2", "bmad brainstorm AI-powered home automation")
    if text is not None:
        check("2.2 response length > 300", len(text) > 300, f"got {len(text)} chars")
        check("2.2 idea/cluster keywords",
              any_present(text, ["idea", "cluster", "concept", "approach"]))
        check("2.2 pros/cons keywords",
              any_present(text, ["pro", "con", "advantage", "disadvantage", "feasibility"]))
        check("2.2 action keywords",
              any_present(text, ["next step", "action", "recommend"]))
    else:
        skip("2.2 assertions", "no response")

    # 2.3 bmad discuss <topic> (prefixed command)
    text = send("2.3", "bmad discuss sustainable packaging alternatives for e-commerce")
    if text is not None:
        check("2.3 response length > 300", len(text) > 300, f"got {len(text)} chars")
        check("2.3 idea/concept keywords",
              any_present(text, ["idea", "concept", "approach", "option", "alternative"]))
    else:
        skip("2.3 assertions", "no response")

    # 2.4 bmad refine <idea> (prefixed command)
    text = send("2.4",
                "bmad refine A voice-controlled smart mirror that displays "
                "calendar, weather, and news")
    if text is not None:
        check("2.4 response length > 200", len(text) > 200, f"got {len(text)} chars")
        check("2.4 weakness keywords",
              any_present(text, ["weakness", "blind spot", "limitation", "risk", "challenge"]))
        check("2.4 improvement keywords",
              any_present(text, ["improve", "iteration", "alternative", "suggestion", "refinement"]))
    else:
        skip("2.4 assertions", "no response")

    # 2.5 bmad validate <concept> (prefixed command)
    text = send("2.5",
                "bmad validate A subscription service for AI-generated "
                "bedtime stories for children")
    if text is not None:
        check("2.5 response length > 200", len(text) > 200, f"got {len(text)} chars")
        check("2.5 assumption keywords",
              any_present(text, ["assumption", "hypothes"]))
        check("2.5 risk keywords",
              any_present(text, ["risk", "failure", "edge case"]))
        check("2.5 validation keywords",
              any_present(text, ["experiment", "test", "metric", "validation", "measure"]))
    else:
        skip("2.5 assertions", "no response")

    # 2.6 Natural language: "discuss" (no bmad word)
    text = send("2.6", "I'd like to discuss ideas for a community garden project")
    if text is not None:
        check("2.6 response length > 200", len(text) > 200, f"got {len(text)} chars")
        check("2.6 topic keywords",
              any_present(text, ["garden", "community", "idea", "concept"]))
    else:
        skip("2.6 assertions", "no response")

    # 2.7 Natural language: "brainstorm" (no bmad word)
    text = send("2.7", "Let's brainstorm about decentralized identity systems")
    if text is not None:
        check("2.7 response length > 200", len(text) > 200, f"got {len(text)} chars")
        check("2.7 topic keywords",
              any_present(text, ["identity", "decentralized", "idea", "concept"]))
    else:
        skip("2.7 assertions", "no response")

    # 2.8 Natural language: "think through" (no bmad word)
    text = send("2.8", "Help me think through the pros and cons of remote work policies")
    if text is not None:
        check("2.8 response length > 200", len(text) > 200, f"got {len(text)} chars")
        check("2.8 topic keywords",
              any_present(text, ["remote", "work", "pro", "con"]))
    else:
        skip("2.8 assertions", "no response")

    # 2.9 bmad-prefixed command
    text = send("2.9", "bmad brainstorm renewable energy storage solutions")
    if text is not None:
        check("2.9 response length > 300", len(text) > 300, f"got {len(text)} chars")
        check("2.9 topic keywords",
              any_present(text, ["energy", "storage", "idea", "concept", "approach"]))
    else:
        skip("2.9 assertions", "no response")

    # 2.10 Edge case: /bmad-brainstorm with no topic
    text = send("2.10", "/bmad-brainstorm")
    if text is not None:
        check("2.10 response length > 50", len(text) > 50, f"got {len(text)} chars")
        check("2.10 asks for clarification",
              any_present(text, ["topic", "what", "about", "specify", "provide", "?"]))
    else:
        skip("2.10 assertions", "no response")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="BMAD Phase 1 skill validation")
    parser.add_argument("--static-only", action="store_true",
                        help="Run only static checks, skip behavioral tests")
    args = parser.parse_args()

    print("BMAD Phase 1 — Skill Validation (bmad-brainstorm)")
    print("=" * 50)

    preflight_ok = run_preflight()
    static_ok = run_static_checks()

    if args.static_only:
        print("\n  (--static-only: skipping behavioral checks)")
    elif not static_ok:
        print("\n  Static checks failed — skipping behavioral checks.")
    elif not preflight_ok:
        print("\n  Pre-flight failed — skipping behavioral checks.")
        print("  Fix gateway/token issues and re-run.")
    else:
        run_behavioral_checks()

    print(f"\n{'=' * 50}")
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
```

---

# 6. RUNNING THE TESTS

## 6.1 Full automated run

```bash
cd mele/user.openclaw/examples/gateway_clients/claw_client
source venv_activate.sh
python bmad_phase1_test.py
```

Exit code 0 = all passed, 1 = at least one failure.

## 6.2 Static checks only (no gateway needed)

```bash
python bmad_phase1_test.py --static-only
```

Or replicate them with shell commands:

```bash
# 1.1 File exists
test -f workspace-wolfgang/skills/bmad-brainstorm/SKILL.md && echo PASS || echo FAIL

# 1.2 YAML front-matter
head -5 workspace-wolfgang/skills/bmad-brainstorm/SKILL.md

# 1.3 Required strings present
grep -q "/bmad-brainstorm" workspace-wolfgang/skills/bmad-brainstorm/SKILL.md && echo PASS || echo FAIL
grep -q "brainstorm"       workspace-wolfgang/skills/bmad-brainstorm/SKILL.md && echo PASS || echo FAIL
grep -q "refine"           workspace-wolfgang/skills/bmad-brainstorm/SKILL.md && echo PASS || echo FAIL
grep -q "validate"         workspace-wolfgang/skills/bmad-brainstorm/SKILL.md && echo PASS || echo FAIL

# 1.4 Registered in openclaw.json
python3 -c "
import json
cfg = json.load(open('openclaw.json'))
skills = next(a for a in cfg['agents']['list'] if a['id']=='wolfgang')['skills']
print('PASS' if 'bmad-brainstorm' in skills else 'FAIL', '— skills:', skills)
"
```

## 6.3 Single behavioral check via CLI

```bash
cd mele/user.openclaw/examples/gateway_clients/claw_client
source venv_activate.sh
python claw_client.py --session bmad-test "/bmad-brainstorm help"
python claw_client.py --session bmad-test "bmad brainstorm AI-powered home automation"
python claw_client.py --session bmad-test "bmad discuss sustainable packaging"
python claw_client.py --session bmad-test "bmad refine A voice-controlled smart mirror"
python claw_client.py --session bmad-test "bmad validate AI-generated bedtime stories"
python claw_client.py --session bmad-test "Let's brainstorm about decentralized identity systems"
python claw_client.py --session bmad-test "I'd like to discuss ideas for a community garden project"
```

Inspect stdout manually.

## 6.4 AI agent usage

An AI agent with shell access can:

1. Run `python bmad_phase1_test.py` and parse the PASS/FAIL/SKIP output.
2. Or import `claw_client` directly in a Python tool call:

```python
import sys
sys.path.insert(0, "mele/user.openclaw/examples/gateway_clients/claw_client")
from claw_client import prompt_sync

r = prompt_sync("/bmad-brainstorm help", session_key="agent-test", timeout=180)
print(r.text)
```

### Interpreting results as an agent

| Symptom | Likely cause | Fix |
|---|---|---|
| All behavioral tests fail with timeout | Gateway not running | `systemctl --user restart openclaw-gateway` |
| All behavioral tests return empty/generic text | Skill not loaded | Check static tests — is `bmad-brainstorm` in `openclaw.json`? Did you restart the gateway? |
| `/bmad-brainstorm help` works but `bmad discuss` returns generic text | Trigger matching issue | Check the SKILL.md trigger section |
| Natural language tests fail but slash commands work | SKILL.md natural language triggers need more examples | Add more trigger phrases to SKILL.md |
| Static tests pass, behavioral tests partially fail | Skill instructions need tuning | Inspect the actual response text for clues |
| `claw_client` import fails | venv not active | `source venv_activate.sh` |

---

# 7. PASS / FAIL CRITERIA

| Stage | Pass condition |
|---|---|
| Pre-flight | Gateway running and token configured |
| Static | All checks in section 3 pass |
| Behavioral | All checks in section 4 pass |
| Overall | All three stages pass |

If any behavioral check fails, inspect the response text (printed to stdout
by the script) to determine whether the skill produced partial output (skill
loaded but response structure is off) vs. no BMAD-related output at all (skill
not loaded or triggers not matching).

---

END OF TEST INSTRUCTIONS
