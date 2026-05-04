---
title: 'Web interface review and contract test run'
type: 'chore'
created: '2026-04-26'
status: 'done'
route: 'one-shot'
---

# Web interface review and contract test run

## Intent

**Problem:** The optional browser UI (`/ui/`) and its contract tests needed a structured review and an executed test pass to confirm behavior and test health.

**Approach:** Read `support_rag/web_routes.py` and `support_rag/app.py` for routing and auth; run `tests/contract/test_web_ui.py` under the project venv. Fix the test fixture so `patch("support_rag.app.RAGService", …)` resolves after `support_rag.app` is loaded.

## Suggested Review Order

- Entry: embedded HTML/JS for `/ui/`, server routes and auth for `/ui/api/chat` and `/ui/api/ingest-folder`
  [`web_routes.py:27`](../../support_rag/web_routes.py#L27)

- Root redirect to `/ui/` for bookmarking
  [`web_routes.py:264`](../../support_rag/web_routes.py#L264)

- App mounts UI when `RAG_ENABLE_WEB_UI` is on
  [`app.py:100`](../../support_rag/app.py#L100)

- Contract tests: redirect, HTML shell, 401s, RAG on/off, retrieve wiring
  [`test_web_ui.py:38`](../../tests/contract/test_web_ui.py#L38)
