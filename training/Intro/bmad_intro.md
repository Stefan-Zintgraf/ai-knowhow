---
marp: true
theme: default
size: 16:9
paginate: true
title: "BMAD Method — Quick Guide"
description: "Simple API enhancement in a big brownfield project"
style: |
  section {
    font-size: 22px;
    padding: 12px 40px 32px 40px;
    justify-content: flex-start;
  }
  section.lead {
    justify-content: center;
    font-size: 24px;
  }
  section.lead h1 { margin-top: 0; }
  h1 { font-size: 1.4em; margin: 0 0 0.3em; line-height: 1.2; }
  h2 { font-size: 1.2em; margin: 0.05em 0 0.3em; line-height: 1.2; }
  h3 { font-size: 1.02em; margin: 0.1em 0 0.25em; }
  h4 { font-size: 0.95em; margin: 0.1em 0 0.2em; }
  p { margin: 0.2em 0; line-height: 1.32; }
  ul, ol { margin: 0.15em 0; }
  li { margin: 0.08em 0; line-height: 1.3; }
  table { font-size: 0.82em; width: 100%; margin: 0.2em 0; }
  th, td { padding: 0.2em 0.35em; line-height: 1.3; }
  pre { font-size: 0.72em; line-height: 1.3; margin: 0.25em 0; }
  code { font-size: 0.9em; }
  blockquote { margin: 0.3em 0; padding: 0.35em 0.6em; font-size: 0.88em; }
  img { max-height: 48vh; }
  section.diagram-slide img {
    max-height: 54vh;
    max-width: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
  }
---

<!-- _class: lead -->
# BMAD Method — Quick Guide: Simple API Enhancement in a Big Brownfield Project

> For a **single API tweak** in a large repo: use **[Quick Dev](#section-3)**, not the full [PRD/architecture path](#section-6).

---

## Table of contents

- [TL;DR — the 30-second version](#section-tldr)
- [1. Why Quick Dev (and not full BMAD)](#section-1)
  - [1.1 The full spectrum](#section-11)
  - [1.2 Middle ground A — Quick Dev + Checkpoint Preview](#section-12b)
  - [1.3 Middle ground B — PRD only → Quick Dev](#section-12c)
  - [1.4 How to decide — quick heuristics](#section-14)
- [2. One-time prep for a big brownfield repo](#section-2)
  - [2.1 Install BMAD in the repo](#section-21)
  - [Switching the knowledge folder (migrate)](#section-21-migrate)
  - [2.2 Create `project-context.md`](#section-22)
  - [2.2.1 During `bmad-generate-project-context`: Continue vs. deepen](#section-221)
  - [2.3 Document the project if docs are stale](#section-23)
  - [2.4 Make `project-context` easy to find](#section-24)
  - [2.5 Conventions in repo: `AI/acontis/CodingConventions/`](#section-25)
- [3. The per-change workflow (Quick Dev)](#section-3)
- [4. Brownfield-specific tips](#section-4)
- [5. Deferred work](#section-5)
- [6. When to escalate to full BMAD Method](#section-6)
- [7. Cheat sheet — commands you will actually use](#section-7)

---

<a id="section-tldr"></a>

## TL;DR — the 30-second version

### Installation and setup (1/2)

- **[`npx bmad-method install`](#section-21)** → tick **BMad Method Agile-AI Driven-Development** (Core stays on), finish IDE/tool prompts → `_bmad/` and your chosen **output folder** (default repo-root **`_bmad-output/`**; **suggested:** **`AI/ec-master/_bmad-output/`** — see **[§2.1](#section-21)**).

### Installation and setup (2/2)

- **User-defined docs / project knowledge root:** When **Module configuration** appears, choose **Customize** — **not** **Express Setup**. Next, **“Select modules to customize”** — **no module is selected by default**; you **must tick BMM** (BMad Method Agile-AI Driven-Development). If BMM is **not** selected, it is applied with **defaults only** in the background (no prompts—same outcome as Express for BMM). After BMM is selected, set **“Where should long-term project knowledge be stored? (docs, research, references)”** to a **repo-relative** path (default **`docs`**; e.g. **`AI/docs`**). That folder is what **`bmad-document-project`** fills. If you skipped BMM or used **Express Setup**, re-run **Modify BMAD installation** → **Customize** → **select BMM** → set the path. **[§2.1](#section-21)**. To **move** existing knowledge (e.g. from **`docs/`**) to a **new** path, see **[§2.1 (migrate)](#section-21-migrate)**.

---

### Brownfield onboarding (1/2)

- **Mental model (two different outputs):** **`bmad-document-project`** → *what the system is* — broader documentation in your **[project-knowledge folder](#section-21)** (e.g. `docs` / `AI/docs`). **`bmad-generate-project-context`** → *how to change the code without fighting the repo* — lean rules in **`{output_folder}/project-context.md`** (default **`_bmad-output/project-context.md`**; e.g. **`AI/ec-master/_bmad-output/project-context.md`**) — **[§2.1](#section-21)**, **[§2.2](#section-22)**.
- **One-time (per repo) — `bmad-document-project` (quick scan):** new chat → run from **repo root** → finish the **initial / quick** pass → review what lands under your **[project-knowledge folder](#section-21)** (not necessarily top-level `docs/`). Omit if docs already good; more **[§2.3](#section-23)**.
- **Repeat (per area) — `bmad-document-project` (deep dives):** **new chat per area** → run **`bmad-document-project`** again → set scope via **prompts, menu, or first-message intent** (repo-relative path or module)—**stay at repo root**; don’t `cd` into a subfolder to “select” scope unless the workflow says so. Resume/start-fresh if offered. **[§2.3](#section-23)**.

---

### Brownfield onboarding (2/2)

- **One-time (per repo) — `bmad-generate-project-context`:** new chat → [`bmad-generate-project-context`](#section-22) → **each time** the workflow offers **Continue** vs. **Advanced Elicitation** / **Party Mode**, **default: choose Continue** (see **[§2.2.1](#section-221)**) → trim **`project-context.md`** under your output folder (optional: [register that path in persistent instructions](#section-24)).
- **Same-repo coding rules:** Wire **[`AI/acontis/CodingConventions/…`](#section-25)** into **`project-context.md`** in that output folder (References + optional paste; detail in **[§2.5](#section-25)**).
- **Per change:** new chat → **[`bmad-quick-dev`](#section-3) —** *(method, path, module, auth, errors, side effects, analog endpoint, no unrelated refactors)* → approve spec → skim diff → push; wrong intent → `git revert HEAD`, new chat, retry.

[Details below](#section-2).

---

<a id="section-1"></a>

## 1. Why Quick Dev (and not full BMAD) for most cases

BMAD has **three official planning tracks**:

| Track                | Best for                                           | Artifacts created                      |
| -------------------- | -------------------------------------------------- | -------------------------------------- |
| **Quick Flow / Quick Dev** | Bug fixes, small features, clear scope (~1–15 stories) | Tech-spec only (often inline)          |
| **BMad Method**      | Products, complex features (10–50+ stories)        | PRD + Architecture + UX                |
| **Enterprise**       | Compliance, multi-tenant (30+ stories)             | PRD + Architecture + Security + DevOps |

> Key idea: "Apply **as much or as little rigor as needed**." BMAD is a **spectrum**, not a strict ladder — see **[§1.1](#section-11)** for the practical middle grounds.

---

## 1. Why Quick Dev (continued)

A single API enhancement → **Quick Dev**. From
[`docs/how-to/established-projects.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/how-to/established-projects.md):

> Small updates or additions → Run `bmad-quick-dev` to clarify intent, plan,
> implement, and review in a single workflow. **The full four-phase BMad Method
> is likely overkill.**

Quick Dev still gives you BMAD's value (intent compression, spec gating,
self-review, deferred-work triage) without the PRD/architecture ceremony.

---

<a id="section-11"></a>

## 1.1 The full spectrum — from simplest to heaviest

Start at the **top** and only move down when the change genuinely needs more structure:

| # | Approach | Upfront ceremony | Artifacts | Best when |
| - | -------- | ---------------- | --------- | --------- |
| 1 | **`bmad-quick-dev` alone** | Minimal | Inline tech-spec | Clear scope, small blast radius |
| 2 | **`bmad-quick-dev` + [`bmad-checkpoint-preview`](#section-12b)** | Minimal | Spec + guided review | Diff wider than expected; brownfield; >~10 files touched |
| 3 | **PRD only → [`bmad-quick-dev`](#section-12c)** | Light | `PRD.md` + inline spec | Needs documented intent / cross-team alignment, no arch decision |
| 4 | **Full BMad Method** ([§6](#section-6)) | Full | PRD + Architecture + Epics/Stories | Multi-context, unclear scope, recorded arch decision needed |
| 5 | **Enterprise** | Heaviest | PRD + Arch + Security + DevOps | Compliance, multi-tenant, 30+ stories |

---

<a id="section-12b"></a>

## 1.2 Middle ground A — Quick Dev + Checkpoint Preview

- **What:** Run **`bmad-quick-dev`** as usual; when it finishes, say **"checkpoint"** to launch **`bmad-checkpoint-preview`**.
- **What you get:** A 5-step guided review — **Orientation → Walkthrough (by *concern*, not by file) → Detail pass (highest blast-radius spots, tagged `[auth]` / `[schema]` / `[public API]` …) → Testing suggestions → Ship / rework / discuss**.
- **Why it helps:** Raw `git diff` ordering fails around **~10–20 files**; you lose the thread. Checkpoint Preview reorders the change for **comprehension**, not for git.
- **Still zero upfront ceremony** — it is a *post-implementation* layer, not a planning layer.
- **Good fit:** Brownfield changes that *look* small but touch more files than expected; cross-cutting edits; PR reviews you didn't author.
- **Invoke standalone** too: *"checkpoint"* or *"walk me through this change"* on any PR / branch / spec.

---

<a id="section-12c"></a>

## 1.3 Middle ground B — PRD only → Quick Dev

- **What:** Run **`bmad-agent-pm` → `bmad-create-prd`** to produce **`PRD.md`**, then feed it into **`bmad-quick-dev`** as the spec input. **Skip** `bmad-create-architecture`, `bmad-create-epics-and-stories`, sprint planning, per-story ceremony.
- **Why this exists:** *"Quick Flow skips from spec to implementation"* and *"apply as much or as little rigor as needed"* — an explicit permission to mix levels.
- **What you get:** A **recorded requirements document** (users, scope, acceptance) for team / audit / async review, without paying for architecture docs or story breakdown.
- **Good fit:** Change needs **documented intent** (stakeholders, auditors, other teams must agree) but has **no non-trivial architectural decision** (no new table, no new pattern, no breaking API).
- **Bad fit:** Anything needing a recorded architectural decision — go to [§6 full method](#section-6) instead.
- **Tip:** Feed the PRD in via the intent line, e.g. `run bmad-quick-dev — implement _bmad-output/planning-artifacts/PRD.md`.

---

<a id="section-14"></a>

## 1.4 How to decide — quick heuristics

- **One endpoint / bug, clear scope →** option **1** (`bmad-quick-dev` alone).
- **Same as above, but diff ended up touching many files or crossing modules →** option **2** (add `checkpoint-preview` at the end).
- **Need a written, shareable requirements doc, but no arch decision →** option **3** (PRD → `bmad-quick-dev`).
- **Multiple services, unclear scope, or arch record required →** option **4** ([full method, §6](#section-6)).
- **Compliance / multi-tenant / 30+ stories →** option **5** (Enterprise).
- **Stuck / unsure?** Run **`bmad-help`** — it inspects the repo and recommends the next step.

---

<a id="section-2"></a>

## 2. One-time prep for a big brownfield repo

Do this **once per repo**, not per change.

<a id="section-21"></a>

### 2.1 Install BMAD in the repo (if not already part of it)

```bash
npx bmad-method install
```

This creates / wires:

- `_bmad/` — agents, workflows, tasks, configuration
- **BMAD output folder (Core)** — during install, Core asks **“Where should output files be saved?”** (repo-relative). Default: **`_bmad-output/`** at the repo root. **Suggested** when you already keep AI-facing material under **`AI/`**: use a nested path such as **`AI/ec-master/_bmad-output/`** (swap **`ec-master`** for your product or area name). That folder becomes the home for **`project-context.md`**, default **`planning-artifacts/`**, **`implementation-artifacts/`**, and other BMAD-generated outputs. Non-interactive installs can pass e.g. **`--output-folder AI/ec-master/_bmad-output`**. To **change the path later**, use **Modify BMAD installation** (same idea as moving the knowledge folder — update config, **`git mv`** if needed, fix references).

---

### 2.1 Install (continued) — modules & knowledge

- **Module configuration: Customize, not Express Setup** — the installer offers **Express Setup** (accept all defaults) vs **Customize** (pick which modules to configure). You **must** pick **Customize** if you need a non-default **BMAD output folder** (Core) or **project knowledge** path. **Express Setup** applies defaults to every non-core module without per-module prompts.
- **“Select modules to customize” — include BMM** — after **Customize**, a **multiselect** lists modules (e.g. BMM). **Nothing is selected by default** (do not assume BMM is checked). You **must select BMM** (BMad Method Agile-AI Driven-Development). Any module you **leave unchecked** is configured **silently with defaults only**—equivalent to Express for that module—so you will **not** see BMM’s questions (including the knowledge path) unless BMM is explicitly selected.
- **Project knowledge folder** — once **BMM** is in the customize list, the installer asks **“Where should long-term project knowledge be stored? (docs, research, references)”** (default **`docs`**). Enter any **path relative to the repo root** (e.g. **`AI/docs`**). **`bmad-document-project` writes here**. If you used **Express Setup**, or **Customize** without selecting **BMM**, use **Modify BMAD installation** → **Customize** → **select BMM** → set or change the path.

**Convention in the rest of this guide:** **`_bmad-output/`** refers to **whatever path you set as the Core output folder** (default repo-root **`_bmad-output/`**, or e.g. **`AI/ec-master/_bmad-output/`**).

---

<a id="section-21-migrate"></a>

#### Switching the knowledge folder when you already have content (e.g. under `docs/`)

You can **change the path later** and **move** what you already generated — no full “from scratch” reinstall is required.

| Step | What to do |
| ---- | ---------- |
| **1. Update BMM** | Run **`npx bmad-method install`** → **Modify BMAD installation** → **Module configuration** → **Customize** → **select BMM** → set **“Where should long-term project knowledge be stored?”** to the **new** repo-relative folder (e.g. from `docs` to `AI/docs`). This updates the stored config so **`bmad-document-project`** and related workflows use the new root. |
| **2. Move files** | Move the existing content from the old folder to the new one (e.g. `git mv docs AI/docs` for a wholesale move, or `git mv` subtrees) so you do not keep two competing trees. Create the new path first if needed. You may delete or repurpose the old directory afterward (optional: a tiny `docs/README.md` that points to the new location for anyone following stale links). |
| **3. Fix references** | Search the repo for the old path in links, `AGENTS.md`, **`[project-context.md`](#section-22)`**, CI, and hand-written notes; update to the new path. BMad does not rewrite those for you. |

**Summary:** Re-run the installer in **modify** mode, point BMM at the new knowledge root, then **`git mv`** (or equivalent) the content and **update** any non-BMad references. Future BMad runs write to the **new** folder only.

---

<a id="section-22"></a>

### 2.2 Create `project-context.md` (strongly recommended for brownfield)

This is the single most important file for brownfield work. It tells every
future agent run **"follow these conventions, don't reinvent anything"**.

Auto-generate it in a fresh chat:

```text
bmad-generate-project-context
```

After each **category**, the workflow may offer **Continue** vs. **Advanced Elicitation** / **Party Mode**. **Rule:** unless you have a concrete reason to deepen that category, **always pick Continue** — see **[§2.2.1](#section-221)**.

The workflow scans the codebase for:

- Tech stack & versions
- Code organization patterns
- Naming conventions
- Testing approach
- Framework-specific patterns (e.g. Spring controller layout, NestJS
  modules, FastAPI routers…)

Review the generated `_bmad-output/project-context.md` and trim it to the
**non-obvious** rules only (it is loaded on every run, so keep it lean).

---

### 2.2 Example `project-context` shape

Example shape for an API-heavy project:

```markdown
## Critical Implementation Rules

**API layer:**
- All endpoints live under `src/api/v1/<domain>/` and use the
  `RouterFactory` — never register routes directly on the app.
- Request DTOs: `*-request.ts`; response DTOs: `*-response.ts`.
- Validation via Zod schemas co-located with the DTO.
- All errors go through `ApiError` → `errorMiddleware`. Never
  `res.status(...).json(...)` directly.

**Auth:**
- Use `requireScope('customers:write')`, not ad-hoc header checks.

**Testing:**
- Contract tests in `test/contract/**`, use `supertest` + MSW.
- Every new endpoint needs a happy-path + 4xx + authz test.
```

---

<a id="section-221"></a>

#### 2.2.1 During `bmad-generate-project-context`: **Continue** vs. deepen

**Default rule (this guide):** Every time this menu appears, **choose Continue** unless you **explicitly** need more depth in **that** category. The goal is a **complete** `project-context.md` in one pass; you can edit the file afterward. Stopping for **Advanced Elicitation** or **Party Mode** on every step burns context and often leaves the file half-built.

The generator walks **categories** (e.g. build/CI, then language rules). When it shows a summary and asks what to do next, you typically see:

| Choice | Meaning | When to use it |
| ------ | ------- | ---------------- |
| **Continue** | Save this category and move to the **next** one. | **Default — use every time** unless you deliberately need **Advanced Elicitation** or **Party Mode** for this category (see those rows). Keeps the run short and avoids an empty or half-finished `project-context.md`. Prefer this when the chat is **low on context headroom**. |
| **Advanced Elicitation** | Dig deeper on **this** category (versions, pins, supported combinations, toolchain constraints). | When the summary is **too shallow** for safe edits (e.g. canonical CMake presets, compiler floors, known-bad OS×NIC pairs, CI/toolchain gotchas). |
| **Party Mode** | Multi-role review of **this** category (e.g. build vs. CI vs. porting). | When you want **deliberate** debate before locking text — better in a **fresh chat** if context is already tight. |

You can **trim or patch** `project-context.md` after the run; you do not have to perfect each category inside the wizard.

---

<a id="section-23"></a>

### 2.3 (Optional) Document the project if docs are stale — quick scan, then deep dives

If `docs/` is empty or out of date and the repo is genuinely large, run **`bmad-document-project`**. The workflow is effectively **two stages** (same skill, separate runs or guided follow-on steps):

| Stage | What it is | How you run it |
| ----- | ---------- | -------------- |
| **Quick scan** | First pass: project-type detection, broad layout, initial index/overview — fast map of the whole tree. | **New chat.** From **repository root** (where `_bmad/` lives), invoke **`bmad-document-project`** / `/bmad-document-project` and complete that pass. Review what landed in **`docs/`** (or whatever you set as project-knowledge during install). |
| **Deep dives** | One focus at a time: richer documentation for a **subsystem, package, or path**. | **New chat per dive** (keeps context clean and matches BMAD’s “fresh chat per workflow” idea). Invoke **`bmad-document-project`** again. **Select scope in the workflow** — typically by **answering prompts**, choosing from a **menu**, or **stating the target** in your opening line (e.g. “Deep dive on `src/hal/network/`” or “Document the billing service only”). **Stay in the repo root** when invoking; you choose the subfolder **through the workflow**, not by `cd`-ing into it, so paths in generated docs stay consistent and `_bmad` resolution does not break. *(If your build only works when cwd is a package, only change directory when the tool or README says to — that is an exception.)* |

**Resume / state:** If the workflow offers **resume** vs **start fresh** (it may keep scan state in a report file under the project), use **resume** to continue ladder-style documentation; use **start fresh** if you intentionally want to rebuild after big repo changes.

**When to skip:** Skip **`bmad-document-project`** entirely if architecture/overview docs are already accurate and maintained.

**Order with the rest of the [TL;DR](#section-tldr):** Run the **quick scan** (and any **deep dives** you care about) **before** [`bmad-generate-project-context`](#section-22), so conventions and structure are reflected in the scan outputs you review while editing [`project-context.md`](#section-22).

---

<a id="section-24"></a>

### 2.4 Make `project-context` easy to find

Optionally register `_bmad-output/project-context.md` wherever your environment keeps persistent instructions, so workflows load it by default.

<a id="section-25"></a>

### 2.5 Conventions in repo: `AI/acontis/CodingConventions/`

Your handbook and examples live next to the product tree. **`project-context.md` should point at them and, if useful, contain a short pasted excerpt** so one file still gives a fast “what to obey” signal.

**Paths (repo root–relative):**

| Role | Path |
| ------ | ------ |
| English conventions | `AI/acontis/CodingConventions/CodingConventionsEN.md` |
| Example implementation | `AI/acontis/CodingConventions/Module.cpp` |
| Example header | `AI/acontis/CodingConventions/Module.h` |

**Steps:**

1. Open **`_bmad-output/project-context.md`** (create the folder/file if install left it empty).
2. Add a **`## References`** section (near the top, after any YAML front matter) so every workflow can resolve the authoritative sources:

   ```markdown
   ## References

   - `AI/acontis/CodingConventions/CodingConventionsEN.md` — coding standards (EN)
   - `AI/acontis/CodingConventions/Module.h` — example header layout / patterns
   - `AI/acontis/CodingConventions/Module.cpp` — example implementation patterns
   ```

---

3. **Optional but practical:** Under **`## Acontis conventions (apply to all changes)`** (or similar), **paste** the fragments you actually want enforced every time—typically copied from **`CodingConventionsEN.md`** (e.g. naming, includes, error handling, threading/logging rules). Do **not** paste the entire document; paste the **rule bullets and tables** the agent would violate if it only skimmed prose.

4. **Optional:** Right under that, paste **short excerpts** from **`Module.h`** / **`Module.cpp`** (or reference them with “match file/class layout and style of these examples”) so the agent has an inline **canonical pattern** when the examples are small enough. If the examples are long, keep only the struct of a typical module (header guards, namespace, public API shape) in `project-context.md` and rely on the **References** paths for the rest.
5. Save. On later edits, **update `project-context.md` when the conventions files move or change materially**—stale paths hurt more than missing prose.

**Why both “References” and paste:** References let the agent open the real files in the repo. A **short pasted excerpt** catches rules that matter on every edit without requiring three file hops; it is the same idea as “cut and paste from the documentation,” trimmed to what is non‑negotiable for your team.

---

<a id="section-3"></a>

## 3. The per-change workflow (Quick Dev)

This is the loop you run **every time** you enhance an API.

### Step 1 — Fresh chat

Always start a new chat session. Carrying context across workflows is the #1
cause of confused agents.

### Step 2 — Compress intent

Quick Dev accepts free-form intent. Good intent = small, clear,
contradiction-free. Examples that work:

```text
run bmad-quick-dev — Add POST /v1/customers/{id}/deactivate.
Sets customer.status = 'inactive', emits CustomerDeactivated on the
domain bus, returns 204. 404 if customer missing, 409 if already
inactive. Must use existing requireScope('customers:write') auth.
```

```text
run bmad-quick-dev — implement the spec in
_bmad-output/implementation-artifacts/deactivate-endpoint.md
```

```text
run bmad-quick-dev — fix https://github.com/acme/api/issues/842
```

---

### Step 2 — more intent examples

```text
run bmad-quick-dev - create an implementation and test plan and then implement/test the issue 6664 in gitlab.
```

*Issue-tracker shorthand like this is most useful when the environment can **read GitLab** (e.g. a **GitLab MCP** server) so issue **#6664** is loaded from the tracker. If not, put the issue **URL** and/or paste the **description, acceptance criteria, and reproduction** in the same chat so intent is not guessed.*

For a brownfield API change, include at minimum:

- **Path + method + verb semantics** (REST action)
- **Request / response shape** (or "follow existing pattern X")
- **Error cases** you care about
- **Auth / authorization** requirements
- **Side effects** (events, audit logs, cache invalidations)
- **Which existing module/feature** it belongs to (helps the agent locate
  code in a large repo)

---

### Step 3 — Clarify + approve the spec

Quick Dev will likely ask 2–5 clarifying questions and then present a short
spec. This is your **gate**. Review it carefully — fixing intent here is
cheap, fixing it after code is written is expensive.

Typical questions for an API change:

- Idempotency semantics?
- Pagination / filtering on GETs?
- Which existing service class should own the new method?
- Breaking change vs. versioned addition?

---

### Step 4 — Let it run

Once the spec is approved, Quick Dev runs longer without supervision. It:

- Locates the right files in the big repo (this is where
  [`project-context.md`](#section-22) pays off)
- Implements the change
- Runs/updates tests
- Self-reviews (triages findings into "fix now" vs. "defer")
- Commits locally with a conventional commit message

---

### Step 5 — Review the diff

It opens the changed files in your editor. Skim for:

- Did it touch the **right** layer (router → service → repo)?
- Did it follow **your** patterns (from [`project-context.md`](#section-22))?
- Are tests meaningful, not tautological?
- Any accidental refactor of unrelated code? (tell it to revert)

If something is wrong, tell it in the same chat — it iterates. Only start
over (fresh chat + revert) if intent itself was wrong.

---

### Step 6 — Push

Quick Dev will offer to push + open a PR. Accept, or do it manually.

If the push causes problems in CI or prod:

```bash
git revert HEAD
```

Then start a fresh chat and run Quick Dev again with corrected intent.

---

<a id="section-4"></a>

## 4. Brownfield-specific tips (1/2)

These are the things that bite in big existing codebases:

1. **Always call out the module/feature name.** "Add endpoint X in the
   `billing` service" is 10x better than "Add endpoint X" in a 500-file repo.
2. **Point at an analogous existing endpoint.** "Follow the same pattern as
   `POST /v1/customers/{id}/suspend`" — the agent will copy the structure,
   auth, tests, error handling.
3. **Forbid reinvention explicitly.** Add to intent: "Do not add a new HTTP
   client / new error type / new validation library. Use existing ones."

---

## 4. Brownfield-specific tips (2/2)

4. **Scope-lock the change.** Add: "Do not refactor unrelated code. Defer
   any improvements you notice to [`deferred-work.md`](#section-5)."
5. **Architecture guardrail.** If the endpoint has any non-trivial design
   choice (new table? new event? sync vs. async?), add one line to the
   intent stating the choice — don't let Quick Dev invent it silently.
6. **Tests are the contract.** In a big brownfield repo, a passing test
   suite is your only honest signal that nothing else broke. Insist that
   the relevant contract/integration tests pass before the commit.

---

<a id="section-5"></a>

## 5. Deferred work — don't let it derail the change

Quick Dev's review will often surface pre-existing issues unrelated to your
endpoint ("this service has a race condition", "this DTO isn't validated").

It will write those to:

```text
_bmad-output/implementation-artifacts/deferred-work.md
```

**Leave them there.** Each one is a candidate for its own future Quick Dev
run. Do not let them swell the current PR — that is exactly the failure
mode Quick Dev is designed to prevent.

---

<a id="section-6"></a>

## 6. When to escalate to full BMAD Method

Stop using Quick Dev and switch to the full method when **any** of these are
true:

- The change touches multiple bounded contexts / services coordinated.
- Scope is unclear — you need requirements discovery, not implementation.
- You need a recorded architectural decision (new dependency, new pattern,
  breaking API change) for the team / auditors.
- UX design is involved (new admin screens, developer portal changes).

In that case, the flow becomes:

1. **`bmad-agent-pm` → `bmad-create-prd`** — Lock what to build: problem, users, scope, priorities, and acceptance-level requirements in a PRD. This is the contract before anyone designs or codes.

2. **`bmad-agent-architect` → `bmad-create-architecture`** — Decide how it fits the system: components, integrations, data, risks, and major technical choices so implementation does not fight itself.

3. **`bmad-agent-pm` → `bmad-create-epics-and-stories`** — Break the PRD and architecture into epics and implementable stories with clear boundaries and ordering for delivery.

---

## 6. Full BMAD flow (continued)

4. **`bmad-agent-architect` → `bmad-check-implementation-readiness`** — Sanity-check that plans, stories, and constraints align (no hidden gaps, contradictions, or missing decisions) before sprint work starts.

5. **`bmad-agent-dev` → `bmad-sprint-planning` →** per-story **`bmad-create-story` → `bmad-dev-story` → `bmad-code-review`** — Run delivery like a mini sprint: plan the batch, refine each story, implement, then review so quality stays gated story by story.

But again: for a single API enhancement, you almost never need this.

---

<a id="section-7"></a>

## 7. Cheat sheet — commands you will actually use

| When                              | Command                              |
| --------------------------------- | ------------------------------------ |
| Install BMAD in the repo          | [`npx bmad-method install`](#section-21)            |
| "What should I do next?"          | `bmad-help`                          |
| Generate project conventions file | [`bmad-generate-project-context`](#section-22)      |
| Document a messy existing repo    | [`bmad-document-project`](#section-23)              |
| **Do the actual API change**      | [`bmad-quick-dev`](#section-3)                     |
| Guided review of a wide diff      | [`bmad-checkpoint-preview`](#section-12b) *(say "checkpoint")* |
| Recorded requirements, no arch    | [`bmad-create-prd`](#section-12c) → `bmad-quick-dev` |
| Mid-change, rethink scope         | `bmad-correct-course`                |
