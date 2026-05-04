"""
Browser automation: Web UI persists Chat + AnythingLLM ingest fields across reload.

Requires support_rag with a writable RAG_CONFIG (e.g. config.e2e.yaml) and either
env-based UI auth (RAG_SERVICE_TOKEN + RAG_ADMIN_TOKEN) or paste tokens in the form.

Run:
  uv run pytest tests/e2e/test_web_ui_persistence_playwright.py -m browser_e2e -s

Env:
  E2E_RAG_BASE_URL — default http://127.0.0.1:8080
  PLAYWRIGHT_HEADLESS — default 1
"""

from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

import pytest

pytestmark = pytest.mark.browser_e2e


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def test_web_ui_persists_rag_and_alm_ingest_fields_after_reload() -> None:
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
    suffix = uuid.uuid4().hex[:8]
    folder_label = f"e2e-folder-{suffix}"
    ws_slug = f"e2e-ws-{suffix}"
    alm_path = rf"C:\e2e\alm-path-{suffix}"

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

            if page.locator("#alm_ws_mode_override").count() == 0:
                pytest.skip(
                    f"Web UI at {base}/ui/ has no AnythingLLM workspace controls; restart support_rag "
                    "with the current codebase."
                )

            page.locator("#alm_fld").fill(folder_label)
            page.locator("#alm_ws_mode_override").click()
            page.locator("#alm_ws_manual").fill(ws_slug)
            page.locator("#fpath_alm").fill(alm_path)
            page.locator('input[name=ragsource][value="anythingllm"]').click()
            page.locator("#userag").set_checked(True)
            page.locator('[data-testid="chat-src-llm-gateway"]').click()
            # anything_llm.top_n in config may cap chat retrieval; keep within typical e2e YAML (e.g. 4).
            page.locator("#itopn").fill("3")

            time.sleep(0.55)

            page.reload(wait_until="domcontentloaded")

            assert page.locator("#alm_fld").input_value() == folder_label
            assert page.locator("#alm_ws_manual").input_value() == ws_slug
            assert page.locator("#fpath_alm").input_value() == alm_path
            assert page.locator('input[name=ragsource][value="anythingllm"]').is_checked()
            assert page.locator("#userag").is_checked()
            assert page.locator('[data-testid="chat-src-llm-gateway"]').is_checked()
            assert page.locator("#itopn").input_value() == "3"

            page.locator('input[name=models_src][value="alm_desktop"]').click()
            page.locator('[data-testid="chat-src-anythingllm"]').click()
            time.sleep(0.55)
            page.reload(wait_until="domcontentloaded")
            assert page.locator('[data-testid="chat-src-anythingllm"]').is_checked()
        finally:
            browser.close()
