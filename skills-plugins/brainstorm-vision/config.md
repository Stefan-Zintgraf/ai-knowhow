# brainstorm-vision — Config

Session limits the skill reads **once at session start** (and again on every resume,
since the counter is per *sitting* — see below). Human-edited; the skill never writes
here. Missing file, missing key, or a blank/`off` value = that limit disabled.

```yaml
# Hard cap: enforce a pause once this many use-cases have been NEWLY added in the
# current sitting. Reached → follow the checkpoint-pause flow (divergence NOT
# saturated, same anchor), so resuming drops straight back into diverging.
# 0 / blank / off = no cap (skill runs to natural saturation as before).
max_new_use_cases: 10

# Advance notice: how many use-cases BEFORE the cap to tell the brainstorm partner
# an auto-pause is coming ("N more and I'll pause for a checkpoint"). Defines WHEN
# they're informed of the termination. 0 = no advance notice; announce only at the
# cap itself. Ignored when max_new_use_cases is off.
warn_before: 3
```

**Full semantics and enforcement mechanics:** see the **Use-case cap** entry in
[`GLOSSARY.md`](GLOSSARY.md) and [`usecase-cap.md`](usecase-cap.md) — this file holds only
the human-edited values.
