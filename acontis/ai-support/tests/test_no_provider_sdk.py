"""R-17: RAG service must not import OpenAI, Anthropic, or Ollama client SDKs."""

import ast
from pathlib import Path

BANNED_ROOTS = ("openai", "anthropic", "ollama")


def test_no_banned_top_level_imports_in_support_rag() -> None:
    root = Path(__file__).resolve().parents[1] / "support_rag"
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    if n.name.split(".", 1)[0] in BANNED_ROOTS:
                        msg = f"Banned import {n.name} in {path}"
                        raise AssertionError(msg)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".", 1)[0] in BANNED_ROOTS:
                    msg = f"Banned import from {node.module} in {path}"
                    raise AssertionError(msg)
