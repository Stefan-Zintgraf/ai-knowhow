"""Contract: optional web UI routes (GET /ui/, POST /ui/api/*) and root redirect."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.requests import Request
from starlette.testclient import TestClient


@pytest.fixture
def web_ui_client(
    monkeypatch: pytest.MonkeyPatch,
) -> Any:
    monkeypatch.setenv("RAG_SERVICE_TOKEN", "contract-test-service-token")
    monkeypatch.setenv("RAG_ADMIN_TOKEN", "contract-test-admin-token")
    # Do not inherit RAG_UI_AUTH_FROM_ENV from the test runner (e.g. dev shell with =1), which
    # would make optional Bearer in /ui/ behave as authenticated without headers.
    monkeypatch.setenv("RAG_UI_AUTH_FROM_ENV", "0")
    fake_rag = MagicMock()
    fake_rag.aclose = AsyncMock()
    fake_rag.retrieve = AsyncMock()
    fake_rag.chat_complete = AsyncMock(return_value="model says hi")
    fake_rag.health = AsyncMock(
        return_value={
            "status": "ok",
            "version": "0.1.0",
            "contract_version": "1.0",
            "capabilities": {},
            "models": {
                "embedding": "emb",
                "retrieval_llm": "contract-test-llm",
                "chat": "contract-test-chat",
                "reranker": "ce",
            },
            "stores": {"qdrant": "ok"},
        }
    )
    fake_rag.index = AsyncMock()
    fake_rag.rebind_config = MagicMock()
    # Load app module first so `patch("support_rag.app.RAGService", ...)` resolves.
    import support_rag.app  # noqa: F401
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


def test_get_root_redirects_to_ui(web_ui_client: Any) -> None:
    client, _ = web_ui_client
    r = client.get("/", follow_redirects=False)
    assert r.status_code == 302
    assert r.headers.get("location") == "/ui/"


def test_get_ui_returns_html(web_ui_client: Any) -> None:
    client, _ = web_ui_client
    r = client.get("/ui/")
    assert r.status_code == 200
    assert "text/html" in (r.headers.get("content-type") or "")
    assert "Support RAG" in r.text


def test_ui_chat_requires_bearer(web_ui_client: Any) -> None:
    client, fake_rag = web_ui_client
    r = client.post("/ui/api/chat", json={"message": "hi", "use_rag": False})
    assert r.status_code == 401
    fake_rag.chat_complete.assert_not_called()


def test_ui_ingest_requires_admin_bearer(web_ui_client: Any) -> None:
    client, fake_rag = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.post(
        "/ui/api/ingest-folder",
        json={"path": "C:\\\\nope", "namespace": "kb"},
        headers=h,
    )
    assert r.status_code == 401
    fake_rag.index.assert_not_called()


def test_ui_chat_no_rag_200(web_ui_client: Any) -> None:
    client, fake_rag = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.post(
        "/ui/api/chat",
        json={"message": "hello", "use_rag": False},
        headers=h,
    )
    assert r.status_code == 200
    j = r.json()
    assert j["reply"] == "model says hi"
    assert j.get("rag_source") == "none"
    assert j.get("completion_route") == "llm_gateway"
    assert "meta" in j
    assert j["meta"].get("request_id")
    fake_rag.retrieve.assert_not_called()
    fake_rag.chat_complete.assert_called_once()


def test_get_ui_api_web_ui_requires_bearer(web_ui_client: Any) -> None:
    client, _ = web_ui_client
    r = client.get("/ui/api/web-ui")
    assert r.status_code == 401


def test_get_ui_api_web_ui_200(web_ui_client: Any) -> None:
    client, _ = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.get("/ui/api/web-ui", headers=h)
    assert r.status_code == 200
    j = r.json()
    assert "config_path" in j
    assert "web_ui" in j
    assert "auth_from_env" in j
    assert "folder_path" in j["web_ui"]
    assert "alm_ingest_folder_path" in j["web_ui"]


def test_get_ui_api_chat_context_includes_effective_chat(web_ui_client: Any) -> None:
    client, fake_rag = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.get("/ui/api/chat-context", headers=h)
    assert r.status_code == 200
    j = r.json()
    assert "ui_chat_effective" in j
    eff = j["ui_chat_effective"]
    assert eff.get("completion_route") == "llm_gateway"
    assert eff.get("option_a_b_does_not_affect_this") is True
    lg = eff.get("llm_gateway") or {}
    assert lg.get("body_model") == "retrieval"
    assert lg.get("chat_model") == "retrieval"
    assert lg.get("chat_label") == "contract-test-chat"
    assert lg.get("retrieval_llm_label") == "contract-test-llm"
    fake_rag.health.assert_called()


def test_ui_chat_with_rag_calls_retrieve(web_ui_client: Any) -> None:
    from support_rag.schemas import ChunkResult, RetrievalResponse

    client, fake_rag = web_ui_client
    fake_rag.retrieve = AsyncMock(
        return_value=(
            RetrievalResponse(
                chunks=[
                    ChunkResult(
                        id="c1",
                        text="context text",
                        metadata={},
                        parent_id="p1",
                        score=0.9,
                    )
                ],
                rewritten_queries=[],
                debug={},
            ),
            0.01,
        )
    )
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.post(
        "/ui/api/chat",
        json={
            "message": "q",
            "use_rag": True,
            "rag_source": "support_rag",
            "top_k": 2,
        },
        headers=h,
    )
    assert r.status_code == 200
    fake_rag.retrieve.assert_called_once()
    fake_rag.chat_complete.assert_called_once()


def _test_config_path(tmp_path: Any) -> Path:
    p = tmp_path / "ui_settings.yaml"
    root = Path(__file__).resolve().parent.parent.parent
    p.write_text((root / "config.example.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return p


def test_get_ui_api_settings_requires_bearer(web_ui_client: Any) -> None:
    client, _ = web_ui_client
    r = client.get("/ui/api/settings")
    assert r.status_code == 401


def test_get_ui_api_settings_200(web_ui_client: Any) -> None:
    client, _ = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.get("/ui/api/settings", headers=h)
    assert r.status_code == 200
    j = r.json()
    assert "config" in j
    assert "field_meta" in j
    assert "llm_gateway" in j["config"]


def test_put_ui_api_settings_requires_admin(web_ui_client: Any) -> None:
    client, _ = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.put(
        "/ui/api/settings",
        json={"retrieval": {"top_k_dense": 1}},
        headers=h,
    )
    assert r.status_code == 401


def test_put_ui_api_settings_409_risky_qdrant(web_ui_client: Any, tmp_path: Any) -> None:
    from support_rag.app import app

    p = _test_config_path(tmp_path)
    app.state.config_path = str(p.resolve())
    client, _ = web_ui_client
    h = {"Authorization": "Bearer contract-test-admin-token"}
    r = client.put(
        "/ui/api/settings",
        json={"qdrant": {"vector_size": 256}, "confirmed": False},
        headers=h,
    )
    assert r.status_code == 409
    j = r.json()
    assert j.get("require_confirmation") is True
    assert "warnings" in j


def test_put_ui_api_settings_rebind(web_ui_client: Any, tmp_path: Any) -> None:
    from support_rag.app import app

    p = _test_config_path(tmp_path)
    app.state.config_path = str(p.resolve())
    client, fake_rag = web_ui_client
    fake_rag.rebind_config.reset_mock()
    h = {"Authorization": "Bearer contract-test-admin-token"}
    r = client.put(
        "/ui/api/settings",
        json={"retrieval": {"top_k_dense": 7}},
        headers=h,
    )
    assert r.status_code == 200
    fake_rag.rebind_config.assert_called_once()
    j = r.json()
    assert j["config"]["retrieval"]["top_k_dense"] == 7


def test_verify_option_b_requires_admin(web_ui_client: Any) -> None:
    client, _ = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.post("/ui/api/anythingllm/verify-option-b", headers=h)
    assert r.status_code == 401


def test_verify_option_b_anythingllm_unreadable(web_ui_client: Any) -> None:
    from unittest.mock import patch

    client, _ = web_ui_client
    with (
        patch("support_rag.web_routes.litellm_gateway_reachable", return_value=True),
        patch(
            "support_rag.web_routes.try_get_system_settings",
            return_value=(
                None,
                "AnythingLLM rejected the API key (403). "
                "Set RAG_ANYTHING_LLM__API_KEY to a valid key.",
            ),
        ),
    ):
        h = {"Authorization": "Bearer contract-test-admin-token"}
        r = client.post("/ui/api/anythingllm/verify-option-b", headers=h)
    assert r.status_code == 200
    j = r.json()
    assert j["litellm_reachable"] is True
    assert "OK" in j["litellm_message"] or "health" in j["litellm_message"].lower()
    assert j["anythingllm_ok"] is False
    assert "403" in j["anythingllm_message"] or "key" in j["anythingllm_message"].lower()
    assert j["host_match"] is None
    assert "skipped" in j["host_match_message"].lower()


def test_verify_option_b_host_match_ok(web_ui_client: Any) -> None:
    from unittest.mock import patch

    raw = {
        "settings": {
            "LLMProvider": "generic-openai",
            "GenericOpenAiBasePath": "http://127.0.0.1:4000/v1",
        }
    }
    client, _ = web_ui_client
    with (
        patch("support_rag.web_routes.litellm_gateway_reachable", return_value=True),
        patch("support_rag.web_routes.try_get_system_settings", return_value=(raw, None)),
    ):
        h = {"Authorization": "Bearer contract-test-admin-token"}
        r = client.post("/ui/api/anythingllm/verify-option-b", headers=h)
    assert r.status_code == 200
    j = r.json()
    assert j["anythingllm_ok"] is True
    assert j["host_match"] is True
    assert "match" in j["host_match_message"].lower()


def test_verify_option_b_host_mismatch(web_ui_client: Any) -> None:
    from unittest.mock import patch

    raw = {
        "settings": {
            "LLMProvider": "generic-openai",
            "GenericOpenAiBasePath": "http://10.0.0.99:4000/v1",
        }
    }
    client, _ = web_ui_client
    with (
        patch("support_rag.web_routes.litellm_gateway_reachable", return_value=False),
        patch("support_rag.web_routes.try_get_system_settings", return_value=(raw, None)),
    ):
        h = {"Authorization": "Bearer contract-test-admin-token"}
        r = client.post("/ui/api/anythingllm/verify-option-b", headers=h)
    assert r.status_code == 200
    j = r.json()
    assert j["litellm_reachable"] is False
    assert j["anythingllm_ok"] is True
    assert j["host_match"] is False
    assert "mismatch" in j["host_match_message"].lower()


def test_put_ui_api_settings_rebuild_replaces_rag(web_ui_client: Any, tmp_path: Any) -> None:
    from support_rag.app import app

    p = _test_config_path(tmp_path)
    app.state.config_path = str(p.resolve())
    client, fake_rag = web_ui_client
    new_r = MagicMock()
    new_r.aclose = AsyncMock()
    with patch("support_rag.web_routes.RAGService", return_value=new_r):
        h = {"Authorization": "Bearer contract-test-admin-token"}
        r = client.put(
            "/ui/api/settings",
            json={"llm_gateway": {"base_url": "http://127.0.0.1:4999"}, "confirmed": True},
            headers=h,
        )
    assert r.status_code == 200
    assert app.state.rag is new_r
    fake_rag.aclose.assert_called()


def test_put_ui_api_web_ui_400_option_b_plus_chat_anythingllm(
    web_ui_client: Any, tmp_path: Any
) -> None:
    from support_rag.app import app
    from support_rag.config import WebUiState

    p = _test_config_path(tmp_path)
    app.state.config_path = str(p.resolve())
    app.state.config.web_ui = WebUiState(
        anythingllm_models_source="llm_gateway",
        chat_model_source="llm_gateway",
    )
    client, _ = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.put(
        "/ui/api/web-ui",
        json={"chat_model_source": "anythingllm", "anythingllm_models_source": "llm_gateway"},
        headers=h,
    )
    assert r.status_code == 400
    assert "redundant" in (r.json().get("detail") or "").lower()


def test_put_ui_api_web_ui_coerces_legacy_litellm_key(web_ui_client: Any, tmp_path: Any) -> None:
    from support_rag.app import app
    from support_rag.config import WebUiState

    p = _test_config_path(tmp_path)
    app.state.config_path = str(p.resolve())
    app.state.config.web_ui = WebUiState()
    client, _ = web_ui_client
    h = {"Authorization": "Bearer contract-test-service-token"}
    r = client.put(
        "/ui/api/web-ui",
        json={"anythingllm_models_source": "litellm_gateway"},
        headers=h,
    )
    assert r.status_code == 200
    assert r.json()["web_ui"]["anythingllm_models_source"] == "llm_gateway"
