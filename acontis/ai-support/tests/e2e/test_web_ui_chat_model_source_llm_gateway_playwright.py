"""
E2E: chat-context / chat route hint reflect llm_gateway.chat_slot and chat_model (E2E profile).

Requires stack with config.e2e-style `chat_slot` / `chat_model` (see config.e2e.yaml).

Run: uv run pytest tests/e2e/test_web_ui_chat_model_source_llm_gateway_playwright.py -m browser_e2e -s
"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
import pytest

pytestmark = pytest.mark.browser_e2e


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def test_chat_context_shows_chat_slot_and_model_for_llm_gateway() -> None:
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
    svc = (os.environ.get("RAG_SERVICE_TOKEN") or "").strip() or "dev-service"
    prev_chat_src: str | None = None
    try:
        gr = httpx.get(
            f"{base}/ui/api/web-ui",
            headers={"Authorization": f"Bearer {svc}"},
            timeout=30.0,
        )
        if gr.is_success:
            j = gr.json()
            wu = j.get("web_ui") if isinstance(j, dict) else None
            if isinstance(wu, dict) and isinstance(wu.get("chat_model_source"), str):
                prev_chat_src = wu["chat_model_source"]
        httpx.put(
            f"{base}/ui/api/web-ui",
            headers={
                "Authorization": f"Bearer {svc}",
                "Content-Type": "application/json",
            },
            json={"chat_model_source": "llm_gateway"},
            timeout=30.0,
        ).raise_for_status()
    except httpx.HTTPError:
        prev_chat_src = None

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

            j = page.evaluate(
                """async () => {
                  const t = document.querySelector('#svctok') && document.querySelector('#svctok').value || '';
                  const h = { 'Content-Type': 'application/json' };
                  if (t) h['Authorization'] = 'Bearer ' + t;
                  const r = await fetch('/ui/api/chat-context', { headers: h });
                  return { status: r.status, body: await r.json() };
                }"""
            )
            assert j["status"] == 200, j
            body = j["body"]
            eff = body.get("ui_chat_effective") or {}
            assert eff.get("completion_route") == "llm_gateway"
            lg = eff.get("llm_gateway") or {}
            # E2E config uses chat_llm + chat (see config.e2e.yaml); default dev may differ.
            assert lg.get("x_slot")
            assert lg.get("chat_model")
        finally:
            browser.close()

    if prev_chat_src is not None:
        try:
            httpx.put(
                f"{base}/ui/api/web-ui",
                headers={
                    "Authorization": f"Bearer {svc}",
                    "Content-Type": "application/json",
                },
                json={"chat_model_source": prev_chat_src},
                timeout=30.0,
            ).raise_for_status()
        except httpx.HTTPError:
            pass
