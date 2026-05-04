# Pre–Step <N> rework (conditional)

**Status:** [ ]

**Session rule:** When this playbook applies, treat it as **one** implementation session: follow the checklist, run gates, commit, mark this file and the [overview](<plan_name>.md) row `[x]`, then **stop**. Do **not** start Step <N> in the same conversation.

---

## When this applies (triggers)

Run the rework sequence if **any** of the following is true **before** Step <N>:

1. <trigger 1>
2. <trigger 2>
3. <trigger 3>

If **none** apply, you may **skip** the rework sequence: document "N/A" in the commit message, mark this row `[x]`, and proceed. Step <N> still starts in a **new** session.

---

## Ordered rework sequence

Repeat until stable (same ordering every time):

1. <action 1 — link to relevant step>
2. <action 2>
3. <action 3>

**Git:** Commit artifacts after each wave; do not skip gates.

---

## Verifiable result

- [ ] Triggers evaluated and documented (result or N/A reason).
- [ ] Rework sequence completed, or skipped as N/A.
- [ ] Overview row and this file's Status updated to `[x]`.

---

## Automated gate

No single global command — use the gates defined in the referenced steps in sequence. If N/A, no command is required.

---

## Related

- [<plan_name>.md](<plan_name>.md) — execution order and session rules
- [<plan_name>.step<N>.md](<plan_name>.step<N>.md) — next step after rework is complete
