"""§2.11: `scripts/reindex.py` / `scripts/seed_kb.py` --help and golden set size (offline)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


def test_reindex_help_exits_zero() -> None:
    r = subprocess.run(
        [sys.executable, str(_ROOT / "scripts" / "reindex.py"), "--help"],
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert "export_path" in r.stdout or "JSONL" in r.stdout


def test_seed_kb_help_exits_zero() -> None:
    r = subprocess.run(
        [sys.executable, str(_ROOT / "scripts" / "seed_kb.py"), "--help"],
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr


def test_golden_questions_jsonl_at_least_30_lines() -> None:
    path = _ROOT / "eval" / "golden" / "questions.jsonl"
    assert path.is_file(), path
    n = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    assert n >= 30, f"expected >= 30 non-empty lines, got {n}"
