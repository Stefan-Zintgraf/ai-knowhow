#!/usr/bin/env python3
"""E2E preflight: verify LiteLLM embed + chat paths via the same `LLMGatewayClient` as the app.

Usage (from repo root, with editable install: pip install -e ".[dev]"):

  py -3.12 scripts/e2e_gateway_preflight.py

Uses ``config.e2e.yaml`` or falls back to ``config.e2e.example.yaml`` in the repo root.
Override with ``RAG_CONFIG`` pointing at any valid YAML.

Exit 0 on success, non-zero on failure. Errors go to stderr (see runbook §8).
"""

from __future__ import annotations

import os
import socket
import sys
import traceback
import urllib.parse
from pathlib import Path

import httpx

# Allow `python scripts/...` from repo host without PYTHONPATH=.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _tcp_check_or_print(base: str) -> int:
    """If nothing accepts TCP, print help and return 1; else 0."""
    u = urllib.parse.urlparse(base)
    if u.scheme not in ("http", "https") or not u.hostname:
        return 0
    port = u.port
    if port is None:
        port = 443 if u.scheme == "https" else 80
    host = u.hostname
    try:
        with socket.create_connection((host, port), timeout=3.0):
            pass
    except OSError as e:
        print(
            f"E2E preflight: cannot open TCP to {host!r} port {port} ({e!r}).\n"
            f"  Start LiteLLM (same port as llm_gateway.base_url) before this script.\n"
            f"  With LiteLLM running, on this machine run:\n"
            f"    curl -sS {base.rstrip('/')}/v1/models\n"
            f"  If curl works in the same window but this script fails, report that.\n"
            f"  If both fail, nothing is bound on that port (wrong port, or not started).",
            file=sys.stderr,
        )
        return 1
    return 0


def _failure_message(
    exc: BaseException | None = None,
    *,
    base_url: str | None = None,
    connect_refused: bool = False,
) -> str:
    extra = ""
    if exc is not None:
        extra = f"\n\nCause: {exc!r}\n{traceback.format_exc()}"
    url = base_url or "(see config llm_gateway.base_url)"
    refused = ""
    if connect_refused:
        refused = f"""
- Connection refused to {url!r} — no process is listening (wrong host/port, or proxy not up).
- Use the same port as ``litellm`` (e.g. ``--port 4000``) or override without editing files:
  PowerShell: $env:RAG_LLM_GATEWAY__BASE_URL = 'http://127.0.0.1:PORT'
  Then re-run. Check:  curl {url!r}/v1/models
"""
    return f"""E2E preflight failed (target: {url}).

1) LiteLLM not reachable (llm_gateway.base_url) — default http://127.0.0.1:4000
   - Start: litellm --config docs/litellm-ollama-e2e.example.yaml --port 4000
{refused}
2) If LiteLLM returns errors for embeddings or chat, ensure Ollama is up and models are present:
   ollama serve
   ollama pull all-minilm
   ollama pull llama3.2:1b

3) Check embedding size matches Qdrant (default 384 for all-minilm):
   ollama show all-minilm

4) See docs/runbook-allow-remote-false-e2e.md{extra}"""


def main() -> int:
    try:
        from support_rag.config import load_config
        from support_rag.gateway import LLMGatewayClient
    except ImportError as e:
        print(_failure_message(e), file=sys.stderr)
        return 1

    path_env = os.environ.get("RAG_CONFIG", "config.e2e.yaml")
    cfg_path = Path(path_env)
    if not cfg_path.is_file() and not cfg_path.is_absolute():
        alt = _ROOT / path_env
        if alt.is_file():
            cfg_path = alt
    if not cfg_path.is_file() and Path(path_env).name == "config.e2e.yaml":
        example = _ROOT / "config.e2e.example.yaml"
        if example.is_file():
            print(
                f"Note: {path_env!r} not found; using {example.name} for preflight. "
                "Copy to config.e2e.yaml if you need local overrides.",
                file=sys.stderr,
            )
            cfg_path = example
    if not cfg_path.is_file():
        print(
            f"Config not found: {path_env!r} (CWD: {Path.cwd()}  repo: {_ROOT}).\n"
            f"  Expected config.e2e.example.yaml at: {_ROOT / 'config.e2e.example.yaml'}",
            file=sys.stderr,
        )
        return 1

    os.chdir(_ROOT)
    try:
        cfg_path = cfg_path.resolve()
    except OSError:
        pass

    try:
        cfg = load_config(str(cfg_path))
        burl = cfg.llm_gateway.base_url.rstrip("/")
        env_ow = os.environ.get("RAG_LLM_GATEWAY__BASE_URL", "")
        if env_ow:
            print(
                f"E2E preflight: RAG_LLM_GATEWAY__BASE_URL is set; effective URL: {burl!r} "
                "(clear this env if you want only config YAML).",
                file=sys.stderr,
            )
        else:
            print(
                f"E2E preflight: using llm_gateway.base_url = {burl!r} .",
                file=sys.stderr,
            )
    except Exception as e:
        print(_failure_message(e, base_url=None), file=sys.stderr)
        return 1

    if _tcp_check_or_print(burl) != 0:
        return 1

    g: object | None = None
    try:
        g = LLMGatewayClient(cfg.llm_gateway)
        try:
            vecs, _em = g.embed_sync(["e2e"], kind="query")
            if not vecs or not vecs[0]:
                print(
                    "embed_sync returned no vectors\n" + _failure_message(base_url=burl),
                    file=sys.stderr,
                )
                return 1
            _ = g.chat_completion_sync(
                [{"role": "user", "content": "Reply with the single word OK."}],
                max_tokens=8,
            )
        except httpx.HTTPStatusError as e:
            part = (e.response.text or "").replace("\n", " ")[:500]
            auth_hint = ""
            if e.response.status_code in (401, 403):
                auth_hint = (
                    "\n  Set $env:RAG_LLM_GATEWAY__API_KEY = '<master_key>' (LiteLLM master_key).\n"
                    "  Or drop `master_key` under `general_settings` for open local dev."
                )
            req = f"{e.request.method} {e.request.url!r}"
            print(
                f"E2E preflight: HTTP {e.response.status_code} from {burl!r} ({req}).\n"
                f"  Response (truncated): {part}{auth_hint}\n"
                f"  See docs/runbook-allow-remote-false-e2e.md §3.1 (auth) and Ollama models.",
                file=sys.stderr,
            )
            return 1
        except (httpx.ConnectError, httpx.ReadTimeout) as e:
            print(
                _failure_message(
                    e,
                    base_url=burl,
                    connect_refused=True,
                ),
                file=sys.stderr,
            )
            return 1
        except (KeyError, TypeError) as e:
            print(
                f"E2E preflight: unexpected response shape from LiteLLM: {e!r}.\n"
                "  If embed/chat JSON differs from OpenAI, check LiteLLM + Ollama versions.\n"
                f"  target={burl!r}",
                file=sys.stderr,
            )
            return 1
        except Exception as e:
            refused = "10061" in str(e) or "refused" in str(e).lower()
            print(
                _failure_message(
                    e,
                    base_url=burl,
                    connect_refused=bool(refused),
                ),
                file=sys.stderr,
            )
            return 1
    except Exception as e:
        bu = None
        try:
            bu = cfg.llm_gateway.base_url
        except Exception:
            bu = None
        print(_failure_message(e, base_url=bu), file=sys.stderr)
        return 1
    finally:
        if g is not None and hasattr(g, "close_sync"):
            g.close_sync()  # type: ignore[union-attr]

    print("E2E preflight OK (embedding + chat completions through LiteLLM).", file=sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
