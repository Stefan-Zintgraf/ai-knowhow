"""
Browser (Chromium) check: Option B → Verify shows LiteLLM / AnythingLLM / gateway lines.

Same stack prerequisites as scripts/e2e_web_ui_ingest_playwright.py.
Install: uv sync --dev && uv run playwright install chromium

Usage:
  uv run python scripts/e2e_web_ui_verify_option_b_playwright.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    test = root / "tests" / "e2e" / "test_web_ui_verify_option_b_playwright.py"
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(test),
        "-m",
        "browser_e2e",
        "-v",
        "--tb=short",
    ]
    return subprocess.call(cmd, cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())
