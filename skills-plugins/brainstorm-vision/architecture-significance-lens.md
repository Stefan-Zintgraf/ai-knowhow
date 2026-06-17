# Architecture-significance lens

The completeness backstop run at wrap-up — **step 1** of the finalize gate (see `SKILL.md` → Architecture-significance sweep). Use it to catch use-cases that, if they only surfaced *after* building started, would force expensive rework of one-way-door decisions: the overall architecture, the software design, the platform/language, the data model.

**This is a lens, not a layer.** Think in these architecturally-loaded terms privately; capture only what an ordinary user would say. Every item you keep is still a plain user-POV use-case ("As someone …, I can finally …") — never a note about sync, schemas, hosting, or tenancy. The scope boundary holds in full; you are only aiming the divergence at corners that are cheap to decide now and dear to change later.

**How to run it.** Walk each dimension. For each, ask yourself: *is there a user whose need on this axis we haven't captured yet?* If yes, offer one candidate use-case in plain language and let the user keep, sharpen, or drop it. When a whole pass produces only restatements of use-cases already in the file, step 1 is done — the session is ready to finalize.

## Dimensions

Each line: the private question → an example of the **user-POV use-case** it might surface (phrased for an inbox product; swap in the real domain).

- **Offline / flaky connection** — can someone need to act with no network? → "As someone who works on planes and trains, I can finally deal with my mail with no signal, and it catches up the moment I'm back online."
- **More than one person** — sharing, delegation, handoff, two people on the same thing at once? → "As someone with an assistant, I can finally hand a thread to them and we're both always looking at the latest version."
- **Scale & volume** — someone with an enormous pile, or power-user throughput? → "As someone with 200,000 emails, I can finally have it stay instant instead of choking."
- **History & longevity** — needing years of the past, a permanent record, an audit trail? → "As someone who has switched jobs three times, I can finally still reach a decision buried in mail from years ago."
- **Privacy & where data lives** — someone who can't let their data leave their device or reach a vendor? → "As a lawyer, I can finally use this without a single client message ever leaving my own machine."
- **Across devices & channels** — start on one device/channel, continue on another? → "As someone who starts on my phone and finishes at my desk, I can finally pick up exactly where I left off."
- **Other people's tools (interop)** — must work with systems the user already has; data in and out? → "As someone moving from another tool, I can finally bring my whole archive in — and take it back out if I ever leave."
- **Acting on the user's behalf (autonomy)** — does things while the user is away, not just shows them? → "As someone on holiday, I can finally let it handle the routine replies on its own and just brief me on the rest."
- **Reach (languages / regions / abilities)** — other languages, regulations, accessibility? → "As someone who lives in three languages, I can finally read and reply in each without switching anything."
- **Trust & control** — needing to review, undo, or veto what the product did? → "As someone who doesn't fully trust automation yet, I can finally see and undo anything it did before it becomes final."

(The list is a prompt, not a quota. A small product may light up two of these; a broad one most of them. Stop when fresh passes only restate what's already captured — that repetition is the signal step 1 is done.)
