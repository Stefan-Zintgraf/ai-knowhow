# Architecture-significance lens — template

The **seed** for the wrap-up sweep — **step 1** of the finalize gate. This is not any product's lens; it's the example clusters the sweep derives *from*. The product's real lens is written to a separate `<slug>-architecture-lens.md` artifact (see `SKILL.md` → file format). `SKILL.md` → Architecture-significance sweep covers what the sweep is, the lens-not-a-layer rule, and how it differs from the parking lot; this file is just the corners to walk. For each dimension ask privately: *is there a user whose need on this axis we haven't captured yet?* — if yes, offer one candidate use-case in plain user language and let the user keep, sharpen, or drop it.

**The invariant is the question, not the list.** The one thing that always holds: *which decisions are cheap to make now and expensive to discover after building starts?* Those one-way doors — the ones that quietly fix the architecture, the platform, the data model — are what the sweep hunts, whatever the product. The dimension lists below are **starter sets, not a canon**: pick the cluster that fits the product's family — but treat even a fitting cluster as a *prompt*, not a checklist. Always close by asking the invariant of *this specific* product, because its defining one-way door is often one no list names: a hypervisor's partitioning of cores and devices between guests, a simulator's fidelity-vs-speed trade, a control stack's redundancy failover. If neither cluster fits at all, drop the lists and generate the axes from the invariant alone. A consumer app and a real-time control library have almost disjoint one-way doors — don't force a product through the wrong list.

## Dimensions — consumer / prosumer software

Each line: the private question → an example of the **user-POV use-case** it might surface. The examples deliberately span *different* products — the dimension is what's generic, not the domain; phrase yours for the product in front of you.

- **Offline / flaky connection** — can someone need to act with no network? → *(field-survey app)* "As a surveyor working deep in the mountains, I can finally record everything with no signal, and it catches up the moment I'm back in range."
- **More than one person** — sharing, delegation, handoff, two people on the same thing at once? → *(design tool)* "As a designer handing a project to a teammate, I can finally pass it over with both of us always seeing the latest version."
- **Scale & volume** — someone with an enormous pile, or power-user throughput? → *(photo library)* "As someone with 100,000 photos, I can finally scroll through them all without it ever stuttering."
- **History & longevity** — needing years of the past, a permanent record, an audit trail? → *(accounting app)* "As a business owner, I can finally pull up an invoice from seven years ago the moment an auditor asks."
- **Privacy & where data lives** — someone who can't let their data leave their device or reach a vendor? → *(health journal)* "As someone tracking my health, I can finally keep every entry on my own device, never on someone's server."
- **Across devices & channels** — start on one device/channel, continue on another? → *(reading app)* "As someone who starts on my phone and finishes on my tablet, I can finally pick up on the exact page I left."
- **Other people's tools (interop)** — must work with systems the user already has; data in and out? → *(project tracker)* "As a team leaving another tool, I can finally bring our whole history in — and take it back out if we ever move on."
- **Acting on the user's behalf (autonomy)** — does things while the user is away, not just shows them? → *(personal assistant)* "As someone away for the weekend, I can finally let it handle the routine bookings on its own and just brief me on the rest."
- **Reach (languages / regions / abilities)** — other languages, regulations, accessibility? → *(online store)* "As a shopper who reads Arabic, I can finally browse and check out entirely in my own language, right to left."
- **Trust & control** — needing to review, undo, or veto what the product did? → *(photo editor)* "As someone wary of automatic edits, I can finally preview and undo anything it changed before it's saved for good."

## Dimensions — embedded / real-time / developer tools & libraries

For a control stack, communication library, device firmware, or engineering/diagnosis tool, the expensive-late corners are almost disjoint from the consumer set. The output is *still* a plain use-case in the voice of whoever depends on the product — an integrating engineer, an operator, a machine builder — never an architecture note.

- **Real-time & determinism** — must it act within a hard time bound, cycle after cycle, with bounded jitter? → *(motion-control stack)* "As a machine builder, I can finally count on every cycle landing on time, even under heavy load, so the axes never lose sync."
- **Target platform / OS / RTOS** — which OS/RTOS or bare-metal targets must it run on, now and later? → *(comms library)* "As a team shipping on both Linux and VxWorks, I can finally run the exact same stack on each without rewriting our integration."
- **Hardware, topology & redundancy** — which controllers/buses/wiring, and what happens when a link or node drops? → *(fieldbus master)* "As a plant engineer, I can finally have the line keep running when a cable fails, with a redundant path taking over unnoticed."
- **Scale of the system** — node counts, data-image size, throughput at the top of the range? → *(large installation)* "As an integrator with a thousand nodes on one segment, I can finally bring them all up and keep them in lockstep."
- **Safety & certification** — functional-safety requirements, standards, and the evidence trail a certifier demands? → *(safety-rated product)* "As a supplier to a certified machine, I can finally hand the auditor every record they need without reconstructing it by hand."
- **Diagnostics & observability** — capturing, tracing, and explaining what the system did at the wire/protocol level? → *(diagnosis tool)* "As a commissioning engineer, I can finally see exactly which node caused a fault and when, instead of guessing from a dead line."
- **Integration & bindings** — the languages, APIs, and config formats through which others build on it? → *(embeddable library)* "As a developer, I can finally drop it into my C++ control app and import the vendor's config files as-is."

(The lists are a prompt, not a quota. A small product may light up two axes; a broad one most. When neither cluster fits, ask the invariant question of the product directly and build the axes from the answers. Stop at **saturation** — when fresh passes only restate what's already captured.)
