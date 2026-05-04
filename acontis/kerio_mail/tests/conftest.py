"""Pytest hooks: integration tests run only when ``KERIO_INTEGRATION=1``."""

from __future__ import annotations

import os

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if os.environ.get("KERIO_INTEGRATION", "").strip().lower() in ("1", "true", "yes"):
        return
    skip = pytest.mark.skip(
        reason="Set KERIO_INTEGRATION=1 and Kerio credentials (see .env.example) to run integration tests.",
    )
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)
