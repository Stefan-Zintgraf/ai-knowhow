"""
Browser (Chromium) smoke: open /ui/, set folder path + kb namespace, run ingest.

Uses Playwright (Chrome DevTools Protocol) — equivalent to "Chrome remote control" for automation.

Prereq:
  py -3.12 -m pip install playwright
  py -3.12 -m playwright install chromium

Env (optional):
  E2E_RAG_BASE_URL   — default http://127.0.0.1:8080
  E2E_UI_DATASET_PATH — default: repo datasets/simple or the path below
  PLAYWRIGHT_HEADLESS — default 1; set 0 to watch Chrome
  RAG_SERVICE_TOKEN / RAG_ADMIN_TOKEN — filled if auth form is visible (load .env from repo)

Expects the local stack (Ollama, Qdrant, LiteLLM, support_rag) already running, with
RAG_CONFIG=config.e2e.yaml and ollama_embed_* so ingest does not hit LiteLLM /v1/embeddings.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _default_dataset_path() -> str:
    env = os.environ.get("E2E_UI_DATASET_PATH", "").strip()
    if env:
        return env
    exact = r"C:\Users\s.zintgraf.ACONTIS\PROJ\ai\ai-support\datasets\simple"
    if Path(exact).is_dir():
        return exact
    rel = _repo_root() / "datasets" / "simple"
    return str(rel.resolve())


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Missing playwright. Run:", file=sys.stderr)
        print("  py -3.12 -m pip install playwright", file=sys.stderr)
        print("  py -3.12 -m playwright install chromium", file=sys.stderr)
        return 127

    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None  # type: ignore[assignment, misc]

    if load_dotenv:
        load_dotenv(_repo_root() / ".env")
        load_dotenv()

    base = os.environ.get("E2E_RAG_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    data_path = _default_dataset_path()
    if not Path(data_path).is_dir():
        print(f"Dataset folder not found: {data_path}", file=sys.stderr)
        return 2

    headless = os.environ.get("PLAYWRIGHT_HEADLESS", "1").lower() not in (
        "0",
        "false",
        "no",
    )

    print(f"Base URL: {base}")
    print(f"Dataset:  {data_path}")
    print(f"Headless: {headless}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(f"{base}/ui/", wait_until="domcontentloaded", timeout=60_000)
        except Exception as e:  # noqa: BLE001
            print(
                f"Failed to open {base}/ui/ — is support_rag running? ({e})",
                file=sys.stderr,
            )
            return 3

        # Optional token fields (shown when .env / server does not provide both)
        for sel, var in (("#svctok", "RAG_SERVICE_TOKEN"), ("#admtok", "RAG_ADMIN_TOKEN")):
            loc = page.locator(sel)
            if loc.count() and loc.is_visible():
                val = (os.environ.get(var) or "").strip()
                if val:
                    loc.fill(val)

        page.locator("#fpath").fill(data_path)
        page.select_option("#fns", "kb")
        page.locator("#binge").click()

        try:
            page.wait_for_function(
                """() => {
                  const e = document.getElementById('ingmsg');
                  if (!e || !e.textContent) return false;
                  const t = e.textContent;
                  if (t.includes('Ingesting')) return false;
                  return t.includes('Done:') || t.includes('Error:');
                }""",
                timeout=300_000,
            )
        except Exception as e:  # noqa: BLE001
            print(
                f"Timeout waiting for ingest to finish: {e}\n"
                f"Last #ingmsg: {page.locator('#ingmsg').inner_text()!r}",
                file=sys.stderr,
            )
            browser.close()
            return 4

        msg = page.locator("#ingmsg").inner_text()
        print("--- #ingmsg ---")
        print(msg)
        browser.close()

        if "Error:" in msg:
            return 1
        if "Done:" in msg:
            return 0
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
