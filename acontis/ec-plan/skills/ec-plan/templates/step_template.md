# Step <N> — <short name>

**Status:** [ ]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

**Prerequisites:** <reference to prior step(s) and any gates that must be green; state "none" if Step 1>

---

## Goal

<One short paragraph: what artifact(s) this step produces and why.>

---

## Tasks

1. <concrete action>
2. <concrete action>
3. <concrete action>

---

## Verifiable result

- [ ] <artifact exists at expected path>
- [ ] <field / condition is set>
- [ ] <test / gate is green>
- [ ] Git: changes committed.

---

## Automated gate

```bash
<exact command(s) to run from the stated cwd>
```

<If the primary gate is manual, say so and list supplementary automated checks here.>

---

## Notes for the agent

- <policy / guardrail specific to this step>
- <common pitfall to avoid>
- If blocked or unclear, stop and ask the user rather than guessing.
