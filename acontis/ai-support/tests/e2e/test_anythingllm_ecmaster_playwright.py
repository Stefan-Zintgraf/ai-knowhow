"""
E2E: Ingest datasets/simple into AnythingLLM, then chat must answer EC-Master from KB
(not a generic "European Master" degree).

Prerequisites: Start-E2E-Stack.ps1 (or AnythingLLM on :3001 + support_rag on :8080 with config.e2e.yaml).
API key: RAG_ANYTHING_LLM__API_KEY or anything_llm.api_key in config.e2e.yaml.

Run:
  uv run pytest tests/e2e/test_anythingllm_ecmaster_playwright.py -m browser_e2e -s
"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
import pytest
import yaml

pytestmark = pytest.mark.browser_e2e


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _alm_api_key() -> str:
    k = (os.environ.get("RAG_ANYTHING_LLM__API_KEY") or "").strip()
    if k:
        return k
    cfg = _repo_root() / "config.e2e.yaml"
    if not cfg.is_file():
        return ""
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            alm = data.get("anything_llm")
            if isinstance(alm, dict):
                return str(alm.get("api_key") or "").strip()
    except OSError:
        pass
    return ""


def _first_workspace_slug(base_url: str, api_key: str) -> str | None:
    url = base_url.rstrip("/") + "/api/v1/workspaces"
    try:
        r = httpx.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0,
        )
        r.raise_for_status()
        data = r.json()
    except (httpx.HTTPError, ValueError):
        return None
    arr = data.get("workspaces") if isinstance(data, dict) else None
    if not isinstance(arr, list):
        return None
    for item in arr:
        if isinstance(item, dict):
            s = item.get("slug")
            if isinstance(s, str) and s.strip():
                return s.strip()
    return None


def test_anythingllm_chat_retrieves_ec_master_not_generic_degree() -> None:
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

    repo = _repo_root()
    simple_dir = repo / "datasets" / "simple"
    if not simple_dir.is_dir():
        pytest.skip(f"missing fixture folder: {simple_dir}")

    alm_base = os.environ.get("RAG_ANYTHING_LLM__BASE_URL", "http://127.0.0.1:3001").rstrip(
        "/"
    )
    api_key = _alm_api_key()
    if not api_key:
        pytest.skip("Set RAG_ANYTHING_LLM__API_KEY or anything_llm.api_key in config.e2e.yaml")

    slug = _first_workspace_slug(alm_base, api_key)
    if not slug:
        pytest.skip(
            f"AnythingLLM has no workspace or API unreachable ({alm_base}). "
            "Start AnythingLLM Desktop and create a workspace."
        )

    # Fresh ingest for this run (avoid only "skipped" if state thinks files unchanged in wrong workspace)
    state_path = repo / "var" / "anythingllm_ingest_state.json"
    try:
        state_path.unlink()
    except OSError:
        pass

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
            page.goto(f"{base}/ui/", wait_until="domcontentloaded", timeout=60_000)
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
                    elif var == "RAG_SERVICE_TOKEN":
                        loc.fill("dev-service")
                    elif var == "RAG_ADMIN_TOKEN":
                        loc.fill("dev-admin")

            if page.locator("#alm_ws_mode_override").count() == 0:
                pytest.skip(
                    f"Web UI at {base}/ui/ has no AnythingLLM workspace controls; restart support_rag "
                    "with the current codebase."
                )

            page.locator("#fpath_alm").fill(str(simple_dir.resolve()))
            page.locator("#alm_ws_mode_override").click()
            page.locator("#alm_ws_manual").fill(slug)
            page.locator("#balm_ingest").click()
            page.locator("#alm_ingest_msg").wait_for(
                state="visible", timeout=180_000
            )
            page.wait_for_function(
                """() => {
                  const el = document.getElementById('alm_ingest_msg');
                  if (!el || !el.textContent) return false;
                  const t = el.textContent;
                  return t.includes('Done:') || t.startsWith('Error:');
                }""",
                timeout=180_000,
            )
            ingest_status = page.locator("#alm_ingest_msg").inner_text()
            assert not ingest_status.startswith("Error:"), ingest_status
            assert "Done:" in ingest_status, ingest_status

            page.locator('input[name=ragsource][value="anythingllm"]').click()
            page.locator("#userag").set_checked(True)
            page.locator('[data-testid="chat-src-llm-gateway"]').click()
            page.locator("#ishowret").set_checked(True)
            page.locator("#msg").fill("what is EC-Master")
            page.locator("#bsend").click()

            page.wait_for_function(
                """() => {
                  const el = document.getElementById('out');
                  return el && el.textContent && el.textContent.trim().length > 20;
                }""",
                timeout=300_000,
            )
            reply = page.locator("#out").inner_text().strip()
            low = reply.lower()

            # Degenerate LLM answer when RAG returns nothing:
            assert "european master" not in low, (
                f"Expected KB-grounded EC-Master (EtherCAT/Acontis), got generic degree text: {reply[:500]}"
            )
            assert "master of science" not in low, (
                f"Expected technical EC-Master, not MSc boilerplate: {reply[:500]}"
            )
            assert (
                "acontis" in low or "ethercat" in low or "ec-master" in low
            ), f"Reply should mention Acontis, EtherCAT, or EC-Master product: {reply[:800]}"

            ret = page.locator("#retout")
            if not ret.is_hidden():
                raw = ret.inner_text()
                assert "chunks" in raw.lower() or "[" in raw, raw[:1200]
        finally:
            browser.close()
