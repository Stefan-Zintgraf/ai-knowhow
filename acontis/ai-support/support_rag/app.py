"""FastAPI app — RAG routes & auth (PRD 2.5 / §12.5)."""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from opentelemetry import trace

from support_rag.config import load_config
from support_rag.deps import _trace_ctx, get_service, require_admin, require_service
from support_rag.otel import setup_telemetry
from support_rag.schemas import DeleteRequest, IndexRequest, RetrievalRequest, RetrievalResponse
from support_rag.service import RAGService
from support_rag.web_routes import build_ui_router, is_web_ui_enabled, root_page_router

logger = logging.getLogger(__name__)

# Re-export for contract tests: `from support_rag.app import get_service`
__all__ = ("app", "get_service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg_path = os.environ.get("RAG_CONFIG", "config.yaml")
    app.state.config_path = str(Path(cfg_path).resolve())
    app.state.config = load_config()
    app.state.settings_lock = asyncio.Lock()
    setup_telemetry(app.state.config)
    app.state.rag = RAGService(app.state.config)
    st = app.state.config.service
    if not os.environ.get(st.service_token_env):
        logger.warning(
            "Set %s for authentication before production", st.service_token_env
        )
    yield
    await app.state.rag.aclose()


app = FastAPI(title="Support RAG", lifespan=lifespan)
api = APIRouter(prefix="/rag", tags=["rag"])


@api.get("/health")
async def get_health(
    _t: str = Depends(require_service),
    service: RAGService = Depends(get_service),
) -> dict[str, Any]:
    return await service.health()


@api.post("/retrieve", response_model=RetrievalResponse)
async def post_retrieve(
    body: RetrievalRequest,
    request: Request,
    _t: str = Depends(require_service),
    service: RAGService = Depends(get_service),
) -> RetrievalResponse:
    tracer = trace.get_tracer("support_rag")
    with tracer.start_as_current_span("rag.retrieve"):
        return (await service.retrieve(body, trace_ctx=_trace_ctx(request)))[0]


@api.post("/index/{namespace}")
async def post_index(
    namespace: str,
    request: Request,
    body: IndexRequest,
    _a: str = Depends(require_admin),
    service: RAGService = Depends(get_service),
) -> dict[str, str]:
    if namespace not in ("kb", "tickets"):
        raise HTTPException(400, "namespace must be kb or tickets")
    tracer = trace.get_tracer("support_rag")
    with tracer.start_as_current_span("rag.index"):
        await service.index(namespace, body.docs, trace_ctx=_trace_ctx(request))
    return {"status": "ok"}


@api.delete("/index/{namespace}")
async def del_index(
    namespace: str,
    request: Request,
    body: DeleteRequest,
    service: RAGService = Depends(get_service),
    _a: str = Depends(require_admin),
) -> dict[str, str]:
    if namespace not in ("kb", "tickets"):
        raise HTTPException(400, "namespace must be kb or tickets")
    tracer = trace.get_tracer("support_rag")
    with tracer.start_as_current_span("rag.delete"):
        await service.delete(
            namespace, body.ids, trace_ctx=_trace_ctx(request)
        )
    return {"status": "ok"}


app.include_router(api)

if is_web_ui_enabled():
    app.include_router(root_page_router())
    app.include_router(build_ui_router())
