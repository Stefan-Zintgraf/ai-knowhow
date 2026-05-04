"""
Browser + HTTP: AnythingLLM workspace block — YAML vs automatic resolution (chat-context API).

Requires live support_rag (/ui/) and AnythingLLM with at least one workspace.
Uses service + admin tokens from env or form (same as other browser_e2e tests).

Run:
  uv run pytest tests/e2e/test_anythingllm_workspace_ui_playwright.py -m browser_e2e -s
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

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


def _tokens() -> tuple[str, str]:
    svc = (os.environ.get("RAG_SERVICE_TOKEN") or "").strip()
    adm = (os.environ.get("RAG_ADMIN_TOKEN") or "").strip()
    if not svc:
        svc = "dev-service"
    if not adm:
        adm = "dev-admin"
    return svc, adm


def _chat_context(base: str, service_token: str) -> dict[str, Any]:
    r = httpx.get(
        f"{base}/ui/api/chat-context",
        headers={
            "Authorization": f"Bearer {service_token}",
            "Accept": "application/json",
        },
        timeout=60.0,
    )
    r.raise_for_status()
    j = r.json()
    return j if isinstance(j, dict) else {}


def _put_settings(base: str, admin_token: str, patch: dict[str, Any]) -> None:
    r = httpx.put(
        f"{base}/ui/api/settings",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "Content-Type": "application/json",
        },
        json=patch,
        timeout=120.0,
    )
    if r.status_code == 409:
        r = httpx.put(
            f"{base}/ui/api/settings",
            headers={
                "Authorization": f"Bearer {admin_token}",
                "Content-Type": "application/json",
            },
            json={**patch, "confirmed": True},
            timeout=120.0,
        )
    r.raise_for_status()


def _put_web_ui(base: str, service_token: str, patch: dict[str, Any]) -> None:
    r = httpx.put(
        f"{base}/ui/api/web-ui",
        headers={
            "Authorization": f"Bearer {service_token}",
            "Content-Type": "application/json",
        },
        json=patch,
        timeout=60.0,
    )
    r.raise_for_status()


def test_workspace_yaml_automatic_clears_override_configured_resolution() -> None:
    """Case A: YAML workspace_slug set; stray override cleared via Automatic → configured."""
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

    alm_base = os.environ.get("RAG_ANYTHING_LLM__BASE_URL", "http://127.0.0.1:3001").rstrip(
        "/"
    )
    api_key = _alm_api_key()
    if not api_key:
        pytest.skip("Set RAG_ANYTHING_LLM__API_KEY or anything_llm.api_key in config.e2e.yaml")

    slug = _first_workspace_slug(alm_base, api_key)
    if not slug:
        pytest.skip("AnythingLLM has no workspace or API unreachable")

    base = os.environ.get("E2E_RAG_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    svc, adm = _tokens()
    headless = os.environ.get("PLAYWRIGHT_HEADLESS", "1").lower() not in (
        "0",
        "false",
        "no",
    )

    orig_cfg: dict[str, Any] | None = None
    try:
        gr = httpx.get(
            f"{base}/ui/api/settings",
            headers={"Authorization": f"Bearer {svc}"},
            timeout=30.0,
        )
        if gr.is_success:
            j = gr.json()
            if isinstance(j, dict) and isinstance(j.get("config"), dict):
                c = j["config"]
                orig_alm = (
                    dict(c["anything_llm"]) if isinstance(c.get("anything_llm"), dict) else {}
                )
                orig_wu = dict(c["web_ui"]) if isinstance(c.get("web_ui"), dict) else {}
                orig_cfg = {"anything_llm": orig_alm, "web_ui": orig_wu}
    except (httpx.HTTPError, ValueError):
        orig_cfg = None

    try:
        _put_settings(base, adm, {"anything_llm": {"workspace_slug": slug}})
        _put_web_ui(
            base,
            svc,
            {"anythingllm_workspace_slug_override": "e2e-temp-override-wrong"},
        )
        ctx0 = _chat_context(base, svc)
        alm0 = ctx0.get("anythingllm") if isinstance(ctx0.get("anythingllm"), dict) else {}
        if "effective_resolution" not in alm0:
            pytest.skip(
                "GET /ui/api/chat-context has no effective_resolution; restart support_rag "
                "with the current codebase."
            )
        assert alm0.get("effective_resolution") == "override", alm0

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
                            loc.fill(svc)
                        elif var == "RAG_ADMIN_TOKEN":
                            loc.fill(adm)

                cfg_disp = page.locator("#alm_cfg_slug_display")
                cfg_disp.wait_for(state="visible", timeout=30_000)
                time.sleep(0.6)
                assert slug in (cfg_disp.inner_text() or "")

                page.locator("#alm_ws_mode_auto").click()
                time.sleep(0.7)

                ctx1 = _chat_context(base, svc)
                alm1 = (
                    ctx1.get("anythingllm") if isinstance(ctx1.get("anythingllm"), dict) else {}
                )
                assert alm1.get("override_workspace_slug") in ("", None), alm1
                assert alm1.get("effective_resolution") == "configured", alm1
                assert alm1.get("effective_workspace_slug") == slug, alm1
            finally:
                browser.close()
    finally:
        if orig_cfg is not None:
            try:
                oa = orig_cfg.get("anything_llm") or {}
                ow = orig_cfg.get("web_ui") or {}
                if oa:
                    _put_settings(base, adm, {"anything_llm": {"workspace_slug": oa.get("workspace_slug", "")}})
                if ow:
                    _put_web_ui(
                        base,
                        svc,
                        {
                            "anythingllm_workspace_slug_override": ow.get(
                                "anythingllm_workspace_slug_override", ""
                            )
                            or ""
                        },
                    )
            except httpx.HTTPError:
                pass


def test_workspace_implicit_first_when_yaml_empty_and_override_cleared() -> None:
    """Case B: empty YAML workspace_slug + no override → implicit_first matches first ALM slug."""
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

    alm_base = os.environ.get("RAG_ANYTHING_LLM__BASE_URL", "http://127.0.0.1:3001").rstrip(
        "/"
    )
    api_key = _alm_api_key()
    if not api_key:
        pytest.skip("Set RAG_ANYTHING_LLM__API_KEY or anything_llm.api_key in config.e2e.yaml")

    first = _first_workspace_slug(alm_base, api_key)
    if not first:
        pytest.skip("AnythingLLM has no workspace or API unreachable")

    base = os.environ.get("E2E_RAG_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    svc, adm = _tokens()

    orig_cfg: dict[str, Any] | None = None
    try:
        gr = httpx.get(
            f"{base}/ui/api/settings",
            headers={"Authorization": f"Bearer {svc}"},
            timeout=30.0,
        )
        if gr.is_success:
            j = gr.json()
            if isinstance(j, dict) and isinstance(j.get("config"), dict):
                c = j["config"]
                orig_alm = (
                    dict(c["anything_llm"]) if isinstance(c.get("anything_llm"), dict) else {}
                )
                orig_wu = dict(c["web_ui"]) if isinstance(c.get("web_ui"), dict) else {}
                orig_cfg = {"anything_llm": orig_alm, "web_ui": orig_wu}
    except (httpx.HTTPError, ValueError):
        orig_cfg = None

    try:
        _put_settings(base, adm, {"anything_llm": {"workspace_slug": ""}})
        _put_web_ui(base, svc, {"anythingllm_workspace_slug_override": ""})

        ctx = _chat_context(base, svc)
        alm = ctx.get("anythingllm") if isinstance(ctx.get("anythingllm"), dict) else {}
        if "effective_resolution" not in alm:
            pytest.skip(
                "GET /ui/api/chat-context has no effective_resolution; restart support_rag "
                "with the current codebase."
            )
        assert alm.get("effective_resolution") == "implicit_first", alm
        assert alm.get("effective_workspace_slug") == first, alm

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=os.environ.get("PLAYWRIGHT_HEADLESS", "1").lower()
                not in ("0", "false", "no")
            )
            page = browser.new_page()
            try:
                page.goto(f"{base}/ui/", wait_until="domcontentloaded", timeout=60_000)
            except Exception as exc:
                browser.close()
                pytest.skip(f"support_rag Web UI not reachable at {base}/ui/ ({exc})")
            try:
                eff = page.locator("#alm_effective_status")
                eff.wait_for(state="visible", timeout=30_000)
                time.sleep(0.5)
                txt = eff.inner_text() or ""
                assert first in txt, txt
                assert "implicit_first" not in txt.lower()
                assert "first workspace" in txt.lower() or "via first" in txt.lower(), txt
            finally:
                browser.close()
    finally:
        if orig_cfg is not None:
            try:
                oa = orig_cfg.get("anything_llm") or {}
                ow = orig_cfg.get("web_ui") or {}
                if oa:
                    _put_settings(
                        base,
                        adm,
                        {"anything_llm": {"workspace_slug": oa.get("workspace_slug", "")}},
                    )
                if ow:
                    _put_web_ui(
                        base,
                        svc,
                        {
                            "anythingllm_workspace_slug_override": ow.get(
                                "anythingllm_workspace_slug_override", ""
                            )
                            or ""
                        },
                    )
            except httpx.HTTPError:
                pass
