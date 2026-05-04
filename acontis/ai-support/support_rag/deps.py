"""Shared FastAPI dependencies (used by `app` and `web_routes` without circular imports)."""

from __future__ import annotations

import os
from typing import Annotated

from fastapi import HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from support_rag.service import RAGService

_bearer = HTTPBearer(auto_error=False)


def _ui_use_server_tokens_from_env(request: Request) -> bool:
    """
    If ``RAG_UI_AUTH_FROM_ENV`` is set, it wins. When unset, use server-side
    tokens for /ui/ API (no browser Authorization) when both service and
    admin tokens are present in their configured env vars (e.g. from ``.env``).
    Set ``RAG_UI_AUTH_FROM_ENV=0`` to require the browser to send Bearer tokens.
    """
    v = os.environ.get("RAG_UI_AUTH_FROM_ENV", "").lower()
    if v in ("1", "true", "yes", "on"):
        return True
    if v in ("0", "false", "no", "off"):
        return False
    cfg = request.app.state.config
    s = os.environ.get(cfg.service.service_token_env, "")
    a = os.environ.get(cfg.service.admin_token_env, "")
    return bool(s and a)


def get_service(request: Request) -> RAGService:
    s = request.app.state.rag
    if not isinstance(s, RAGService):
        raise HTTPException(500, "RAG not initialized")
    return s


def _trace_ctx(request: Request) -> dict[str, str]:
    cfg = request.app.state.config
    h = cfg.service.langfuse_header_name
    out: dict[str, str] = {}
    if h and (tid := request.headers.get(h)):
        out[h] = tid
    if tp := request.headers.get("traceparent"):
        out["traceparent"] = tp
    return out


def _require_bearer(
    request: Request,
    cred: Annotated[HTTPAuthorizationCredentials | None, Security(_bearer)],
    env_name: str,
) -> str:
    expected = os.environ.get(env_name)
    if not expected:
        raise HTTPException(500, f"Set {env_name} for auth")
    if not cred or cred.scheme.lower() != "bearer":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "bearer required")
    if cred.credentials != expected:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")
    return cred.credentials


def require_service(
    request: Request,
    cred: Annotated[HTTPAuthorizationCredentials | None, Security(_bearer)],
) -> str:
    return _require_bearer(
        request, cred, request.app.state.config.service.service_token_env
    )


def require_admin(
    request: Request,
    cred: Annotated[HTTPAuthorizationCredentials | None, Security(_bearer)],
) -> str:
    return _require_bearer(
        request, cred, request.app.state.config.service.admin_token_env
    )


def require_service_ui(
    request: Request,
    cred: Annotated[HTTPAuthorizationCredentials | None, Security(_bearer)],
) -> str:
    """
    Same as `require_service`, but if ``RAG_UI_AUTH_FROM_ENV`` is set and the
    service token is present in the environment, allow requests **without** a
    ``Authorization`` header (browser uses server-side env only; local dev / E2E).
    A wrong Bearer value still returns 401.
    """
    env_name = request.app.state.config.service.service_token_env
    expected = os.environ.get(env_name)
    if _ui_use_server_tokens_from_env(request) and expected:
        if cred is None or cred.scheme.lower() != "bearer":
            return expected
        if cred.credentials != expected:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")
        return cred.credentials
    return _require_bearer(request, cred, env_name)


def require_admin_ui(
    request: Request,
    cred: Annotated[HTTPAuthorizationCredentials | None, Security(_bearer)],
) -> str:
    """See `require_service_ui` — for admin (folder ingest) with optional env-based UI."""
    env_name = request.app.state.config.service.admin_token_env
    expected = os.environ.get(env_name)
    if _ui_use_server_tokens_from_env(request) and expected:
        if cred is None or cred.scheme.lower() != "bearer":
            return expected
        if cred.credentials != expected:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")
        return cred.credentials
    return _require_bearer(request, cred, env_name)
