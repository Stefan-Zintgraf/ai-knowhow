"""
Browser automation (Playwright / CDP): Option B verify shows structured messages.

Requires a running support_rag Web UI (same as scripts/e2e_web_ui_ingest_playwright.py).
Skipped automatically if /ui/ is unreachable.

Run:
  # terminal 1: start stack + support_rag
  uv run pytest tests/e2e/test_web_ui_verify_option_b_playwright.py -m browser_e2e -s

Env:
  E2E_RAG_BASE_URL — default http://127.0.0.1:8080
  PLAYWRIGHT_HEADLESS — default 1
  RAG_SERVICE_TOKEN / RAG_ADMIN_TOKEN — from .env when auth form is shown
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.browser_e2e


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def test_verify_option_b_ui_structured_messages() -> None:
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

    hint = ""
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
            page.locator("#bverifyb").click()

            page.wait_for_function(
                """() => {
                  const e = document.getElementById('verifyst');
                  if (!e || !e.textContent) return false;
                  const t = e.textContent;
                  if (t.includes('Checking')) return false;
                  return t.includes('Gateway:') && t.includes('AnythingLLM:')
                    && t.includes('Gateway vs Desktop:');
                }""",
                timeout=120_000,
            )
            text = page.locator("#verifyst").inner_text()

            page.wait_for_function(
                """() => {
                  const e = document.getElementById('chatRouteHint');
                  if (!e || !e.textContent) return false;
                  const t = e.textContent;
                  if (t.includes('Loading')) return false;
                  return t.includes('User chat:') && t.includes('X-Slot');
                }""",
                timeout=30_000,
            )
            hint = page.locator("#chatRouteHint").inner_text()
        finally:
            browser.close()

    assert "Gateway:" in text
    assert "AnythingLLM:" in text
    assert "Gateway vs Desktop:" in text
    assert "User chat:" in hint
    assert "retrieval" in hint
    assert "HTTPStatusError" not in text, (
        "verify should surface human-readable errors, not raw types"
    )
    assert "unavailable (" not in text.lower(), (
        "avoid generic 'unavailable (ExceptionName)' copy"
    )
