"""NFR-7: single maintainable table — protected `/rag` routes return 401 without valid bearer.

**Public routes under `/rag`:** none (all use `require_service` or `require_admin`).
When a new public route is added, add it to `PUBLIC_ROUTES` and keep it out of
`PROTECTED_ROUTE_CASES` (or document why it is absent from this file).

`auth=none` — no `Authorization` header. `auth=wrong` — `Authorization: Bearer <invalid>`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.requests import Request
from starlette.testclient import TestClient

from support_rag.schemas import ChunkResult, RetrievalResponse

# If the API gains anonymous routes, list (method, path) here and exclude from 401 table.
PUBLIC_ROUTES: set[tuple[str, str]] = set()

_INDEX_DOC = {"docs": [{"id": "doc-1", "text": "hello", "metadata": {}}]}


@dataclass(frozen=True, slots=True)
class RouteCase:
    id: str
    method: str
    path: str
    json_body: dict[str, Any] | None
    # optional: if set, assert this mock on RAGService was not called on 401
    assert_retrieve_not_called: bool = False
    assert_index_not_called: bool = False
    assert_delete_not_called: bool = False


PROTECTED_ROUTE_CASES: tuple[RouteCase, ...] = (
    RouteCase("health", "GET", "/rag/health", None),
    RouteCase(
        "retrieve",
        "POST",
        "/rag/retrieve",
        {"query": "q", "top_k": 1},
        assert_retrieve_not_called=True,
    ),
    RouteCase(
        "index_kb",
        "POST",
        "/rag/index/kb",
        _INDEX_DOC,
        assert_index_not_called=True,
    ),
    RouteCase(
        "delete_kb",
        "DELETE",
        "/rag/index/kb",
        {"ids": ["parent-a"]},
        assert_delete_not_called=True,
    ),
)


@pytest.fixture
def nfr7_client(
    monkeypatch: pytest.MonkeyPatch,
) -> Any:
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "contract-test-service-token")
    monkeypatch.setenv("RAG_ADMIN_TOKEN", "contract-test-admin-token")
    ok = RetrievalResponse(
        chunks=[
            ChunkResult(
                id="c1",
                text="t",
                metadata={"k": 1},
                parent_id="p1",
                score=0.5,
            )
        ],
        rewritten_queries=[],
        debug={},
    )
    fake_rag = MagicMock()
    fake_rag.aclose = AsyncMock()
    fake_rag.retrieve = AsyncMock(return_value=(ok, 0.01))
    fake_rag.index = AsyncMock()
    fake_rag.delete = AsyncMock()
    with patch("support_rag.app.RAGService", return_value=fake_rag):
        from support_rag.app import app, get_service

        def _override_get_service(_request: Request) -> Any:
            return fake_rag

        app.dependency_overrides[get_service] = _override_get_service
        try:
            with TestClient(app) as client:
                yield client, fake_rag
        finally:
            app.dependency_overrides.clear()


def test_admin_routes_reject_service_token(
    nfr7_client: Any,
) -> None:
    """Index/delete require admin bearer; valid service token alone is 401 (NFR-7)."""
    client, fake_rag = nfr7_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r1 = client.post("/rag/index/kb", json=_INDEX_DOC, headers=h)
    assert r1.status_code == 401
    fake_rag.index.assert_not_called()
    r2 = client.request(
        "DELETE",
        "/rag/index/kb",
        json={"ids": ["x"]},
        headers=h,
    )
    assert r2.status_code == 401
    fake_rag.delete.assert_not_called()


@pytest.mark.parametrize("auth", ["none", "wrong"])
@pytest.mark.parametrize(
    "case",
    PROTECTED_ROUTE_CASES,
    ids=[c.id for c in PROTECTED_ROUTE_CASES],
)
def test_protected_routes_401_unauthorized(
    nfr7_client: Any,
    case: RouteCase,
    auth: str,
) -> None:
    (method, path) = (case.method, case.path)
    if (method, path.split("?")[0]) in PUBLIC_ROUTES:
        pytest.skip("public route")
    client, fake_rag = nfr7_client
    headers: dict[str, str] = {}
    if auth == "wrong":
        headers["Authorization"] = "Bearer not-the-token"
    # GET has no body
    kwargs: dict[str, Any] = {"headers": headers}
    if case.json_body is not None and method != "GET":
        kwargs["json"] = case.json_body
    if method == "GET":
        r = client.get(path, **kwargs)
    elif method == "POST":
        r = client.post(path, **kwargs)
    elif method == "DELETE":
        r = client.request("DELETE", path, **kwargs)
    else:
        raise AssertionError(method)

    assert r.status_code == 401, f"{case.id} {auth} body={r.text[:200]!r}"
    if case.assert_retrieve_not_called:
        fake_rag.retrieve.assert_not_called()
    if case.assert_index_not_called:
        fake_rag.index.assert_not_called()
    if case.assert_delete_not_called:
        fake_rag.delete.assert_not_called()


def test_protected_routes_table_covers_rag_routes() -> None:
    """Guardrail: new `/rag` OpenAPI operations must map to the table or PUBLIC_ROUTES."""
    from support_rag.app import app

    spec = app.openapi()
    paths = spec.get("paths") or {}
    http_verbs = frozenset({"get", "post", "put", "delete", "patch", "head"})
    for path_key, path_item in paths.items():
        if not path_key.startswith("/rag"):
            continue
        for op_key, _op_val in path_item.items():
            if op_key not in http_verbs:
                continue
            m = op_key.upper()
            if (m, path_key) in PUBLIC_ROUTES:
                continue
            # Table uses /rag/index/kb; OpenAPI has /rag/index/{namespace}
            covered = any(
                c.method == m
                and (
                    c.path == path_key
                    or (
                        path_key == "/rag/index/{namespace}"
                        and c.path == "/rag/index/kb"
                        and m in ("POST", "DELETE")
                    )
                )
                for c in PROTECTED_ROUTE_CASES
            )
            if not covered:
                extra = "add to PROTECTED_ROUTE_CASES or PUBLIC_ROUTES (this module)"
                pytest.fail(
                    f"NFR-7: OpenAPI has unrouted protected path {m} {path_key} — {extra}",
                )
