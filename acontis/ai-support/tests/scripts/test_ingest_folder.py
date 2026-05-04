"""Offline tests for `scripts/ingest_folder.py` (importlib load)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load_ingest() -> object:
    root = Path(__file__).resolve().parents[2]
    path = root / "scripts" / "ingest_folder.py"
    spec = importlib.util.spec_from_file_location("ingest_folder_cli", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


ing = _load_ingest()


def test_safe_doc_id_short() -> None:
    assert ing._safe_doc_id("a/b.md") == "a/b.md"


def test_safe_doc_id_long_uses_hash() -> None:
    s = "x" * 300
    out = ing._safe_doc_id(s)
    assert out.startswith("h")
    assert len(out) < len(s)


def test_collect_docs_happy(tmp_path: Path) -> None:
    (tmp_path / "n.md").write_text("# hello\n", encoding="utf-8")
    (tmp_path / "t.txt").write_text("ok", encoding="utf-8")
    docs, n_skip, n_read_err, _ = ing.collect_docs(
        tmp_path, ("*.md", "*.txt", "*.rst")
    )
    assert n_read_err == 0
    assert n_skip == 0
    assert len(docs) == 2
    ids = {d["id"] for d in docs}
    assert "n.md" in ids and "t.txt" in ids


def test_collect_docs_skips_invalid_utf8(tmp_path: Path) -> None:
    p = tmp_path / "b.md"
    p.write_bytes(b"\xff\xff\xff")
    docs, n_skip, n_read_err, msgs = ing.collect_docs(
        tmp_path, ("*.md", "*.txt", "*.rst")
    )
    assert not docs
    assert n_read_err == 1
    assert n_skip == 1
    assert any("utf-8" in m for m in msgs)


def test_is_under_root_rejects_outside(tmp_path: Path) -> None:
    root = tmp_path / "r"
    root.mkdir()
    (root / "a.md").write_text("x", encoding="utf-8")
    other = tmp_path / "other.md"
    other.write_text("y", encoding="utf-8")
    assert ing._is_under_root(root, root / "a.md")
    assert not ing._is_under_root(root, other)


def test_main_exits_1_when_all_files_unreadable(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "b.md").write_bytes(b"\xff\xff")
    monkeypatch.setattr(
        ing.sys, "argv", ["ingest", "--root", str(tmp_path), "--namespace", "kb"]
    )
    with pytest.raises(SystemExit) as se:
        ing.main()
    assert se.value.code == 1
