"""E2E: session preflight for `e2e_privacy` when `RUN_E2E_PRIVACY=1`."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def e2e_gateway_preflight():
    """Re-run `scripts/e2e_gateway_preflight.py` before E2E HTTP tests (same checks as the CLI)."""
    if os.environ.get("RUN_E2E_PRIVACY", "").lower() not in ("1", "true", "yes"):
        yield
        return
    r = subprocess.run(
        [sys.executable, str(_ROOT / "scripts" / "e2e_gateway_preflight.py")],
        cwd=str(_ROOT),
        env=os.environ.copy(),
        timeout=300,
    )
    if r.returncode != 0:
        pytest.fail(
            "E2E gateway preflight failed (see stderr). "
            "See runbook; start LiteLLM, Ollama, and models from config.e2e.",
        )
    yield
