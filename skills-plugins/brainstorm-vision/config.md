# brainstorm-vision — Config

Session limits the skill reads **once at session start** (and again on every resume,
since the counter is per *sitting* — see below). Human-edited; the skill never writes
here. Missing file, missing key, or a blank/`off` value = that limit disabled.

```yaml
# Hard cap: enforce a pause once this many use-cases have been NEWLY added in the
# current sitting. Reached → follow the checkpoint-pause flow (divergence NOT
# saturated, same anchor), so resuming drops straight back into diverging.
# 0 / blank / off = no cap (skill runs to natural saturation as before).
max_new_use_cases: 3

# Advance notice: how many use-cases BEFORE the cap to tell the brainstorm partner
# an auto-pause is coming ("N more and I'll pause for a checkpoint"). Defines WHEN
# they're informed of the termination. 0 = no advance notice; announce only at the
# cap itself. Ignored when max_new_use_cases is off.
warn_before: 1
```

**What "newly added" counts.** Only **use-cases** (`UC…`) appended during the current
sitting — the run since the session started or was last resumed. Use-cases carried in
from a prior sitting don't count; the counter resets to zero on every resume. Vision
points, parking-lot items, and edits to existing use-cases don't count.

**The single checkpoint control.** This cap is the *only* mid-session checkpoint
mechanism — it replaces the old question-count checkpoint offer entirely. When off, the
session simply runs to natural saturation with no automatic pause.

**How it's enforced.** Not by self-discipline — by a hard `UserPromptSubmit` hook
(`usecase-cap.sh`; see [`usecase-cap.md`](usecase-cap.md)). At the cap it makes Claude
Code **discard further prompts** in the current session and tells the human to `/clear`
and re-invoke to start a fresh sitting. The count is recomputed from the `.wip.md` on
disk every turn, so it can't be argued around or lost to context rot.
