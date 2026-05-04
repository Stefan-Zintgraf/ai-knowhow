# ai-support — agent rules

## Web UI changes and browser automation

Any work that **modifies the Web UI** must end with **browser automation tests being run** (not only unit or API contract tests). Treat the run as part of the same change, not optional follow-up.

**What counts as Web UI work**

- [`support_rag/web_routes.py`](support_rag/web_routes.py) (HTML, inline script, `/ui/api/*`, `WebUiState`, etc.)
- Embedded UI strings, layout, or behavior in that module
- Persisted `web_ui` fields in YAML or `WebUiPatch` / chat payload models

**How to run browser automation**

From the repo root (with dev deps and Chromium for Playwright installed):

```bash
uv run pytest tests/e2e -m browser_e2e -s
```

Tests are marked `browser_e2e` and skip if the UI is unreachable; for a full check, start the stack (see `tests/e2e/scripts/Start-E2E-Stack.ps1` and project runbooks) so `/ui/` is live.

**Helper scripts** (optional; use when you need a standalone repro or parity with CI)

- [`scripts/e2e_web_ui_verify_option_b_playwright.py`](scripts/e2e_web_ui_verify_option_b_playwright.py)
- [`scripts/e2e_web_ui_persistence_playwright.py`](scripts/e2e_web_ui_persistence_playwright.py)
- [`scripts/e2e_web_ui_ingest_playwright.py`](scripts/e2e_web_ui_ingest_playwright.py)
- [`scripts/e2e_gateway_preflight.py`](scripts/e2e_gateway_preflight.py) (gateway health before some E2E flows)

If a browser test fails, fix the implementation or update the test when the behavior change is intentional—do not merge Web UI changes with failing or skipped browser automation without an explicit, reviewed reason.

## Cursor: always-on rule file

For **Cursor** to load this expectation in every chat, add the following as
`.cursor/rules/web-ui-browser-e2e.mdc` (YAML frontmatter + body). If that path
does not exist yet, create the `rules` directory first.

```text
---
description: Web UI changes require Playwright browser_e2e tests; optional scripts/ helpers.
alwaysApply: true
---

# Web UI — run browser automation

If the task **modifies the Web UI** (e.g. `support_rag/web_routes.py`, embedded HTML/JS, `/ui/api/*`, `web_ui` persistence or chat models), you **must run** the browser automation suite before finishing:

`uv run pytest tests/e2e -m browser_e2e -s`

Optional standalone repros or preflight: `scripts/e2e_web_ui_*.py`, `scripts/e2e_gateway_preflight.py`. Start the stack when needed (`tests/e2e/scripts/Start-E2E-Stack.ps1`). See root `AGENTS.md` for details.
```

Save the file above with the **`.mdc` extension** (not `.md`).
