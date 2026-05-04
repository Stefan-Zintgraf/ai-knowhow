"""
E2E: Option B disables AnythingLLM chat source; PUT invalid combo returns 400.

Run: uv run pytest tests/e2e/test_web_ui_invalid_optionb_chat_anythingllm_playwright.py -m browser_e2e -s
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.browser_e2e


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def test_option_b_disables_anythingllm_chat_and_put_returns_400() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        pytest.skip("install dev deps: pip install playwright && playwright install chromium")

    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None  # type: ignore[assignment, misc]

    if load_dotenv:
        load_dotenv(_repo_root() / ".env")
        load_dotenv()

    base = os.environ.get("E2E_RAG_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    headless = os.environ.get("PLAYWRIGHT_HEADLESS", "1").lower() not in (
        "0",
        "false",
        "no",
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        try:
            page.goto(f"{base}/ui/", wait_until="domcontentloaded", timeout=30_000)
        except Exception as exc:
            browser.close()
            pytest.skip(f"support_rag Web UI not reachable at {base}/ui/ ({exc})")

        try:
            for sel, var in (
                ("#svctok", "RAG_SERVICE_TOKEN"),
                ("#admtok", "RAG_ADMIN_TOKEN"),
            ):
                loc = page.locator(sel)
                if loc.count() and loc.is_visible():
                    val = (os.environ.get(var) or "").strip()
                    if val:
                        loc.fill(val)

            page.locator('input[name=models_src][value="llm_gateway"]').click()
            page.wait_for_timeout(200)
            alm = page.locator('[data-testid="chat-src-anythingllm"]')
            assert alm.is_disabled()
            hint = page.locator('[data-testid="optb-disabled-hint"]')
            assert hint.is_visible()
            ht = hint.inner_text().lower()
            assert "circular" in ht or "redundant" in ht or "already" in ht or "gateway" in ht

            err = page.evaluate(
                """async () => {
                  const t = document.querySelector('#svctok') && document.querySelector('#svctok').value || '';
                  const h = { 'Content-Type': 'application/json' };
                  if (t) h['Authorization'] = 'Bearer ' + t;
                  const r = await fetch('/ui/api/web-ui', {
                    method: 'PUT',
                    headers: h,
                    body: JSON.stringify({ chat_model_source: 'anythingllm', anythingllm_models_source: 'llm_gateway' }),
                  });
                  const j = await r.json().catch(() => ({}));
                  return { status: r.status, detail: j.detail };
                }"""
            )
            assert err["status"] == 400
            det = str(err.get("detail") or "")
            assert "Option B" in det or "redundant" in det.lower() or "circular" in det.lower()
        finally:
            browser.close()
