"""
E2E: YAML with legacy `anythingllm_models_source: litellm_gateway` shows Option B as llm_gateway.

Start the app with:
  set RAG_CONFIG=tests/e2e/fixtures/legacy_litellm_web_ui.yaml
(from repo root), or set env E2E_LEGACY_LITELLM_YAML=1 when using that config.

Run: uv run pytest tests/e2e/test_web_ui_legacy_litellm_gateway_yaml_playwright.py -m browser_e2e -s
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.browser_e2e


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def test_legacy_litellm_gateway_yaml_shows_coerced_option_b() -> None:
    if os.environ.get("E2E_LEGACY_LITELLM_YAML", "").lower() not in ("1", "true", "yes"):
        pytest.skip(
            "Set E2E_LEGACY_LITELLM_YAML=1 and start support_rag with "
            "RAG_CONFIG=tests/e2e/fixtures/legacy_litellm_web_ui.yaml"
        )

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

            assert page.locator('input[name=models_src][value="llm_gateway"]').is_checked()
        finally:
            browser.close()
