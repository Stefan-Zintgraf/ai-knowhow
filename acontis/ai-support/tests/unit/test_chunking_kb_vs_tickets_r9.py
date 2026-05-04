"""R-9: kb vs tickets chunking yield different chunk counts (PRD §2.3.2).

Max-length policy: ``chunking.kb.chunk_size`` is enforced via LlamaIndex ``SentenceSplitter``;
each KB chunk text is at most **N tokens** (``get_tokenizer()``, same as the splitter).
Windows use ``SentenceWindowNodeParser`` over those segments.
"""

from __future__ import annotations

from llama_index.core.utils import get_tokenizer

from support_rag.chunking import chunk_kb, chunk_tickets
from support_rag.config import AppConfig
from support_rag.schemas import IngestDocument

# chunk_kb: sentence windows; chunk_tickets without qa_pairs: one body chunk.
_PARAGRAPH = (
    "First sentence. Second sentence. Third sentence. Fourth. Fifth. Sixth. "
    "Seventh. Eighth. Ninth. Tenth. Eleven. Twelve. Thirteen. Fourteen. Fifteen. "
    "Sixteen. Seventeen. Eighteen. Nineteen. Twenty. Twenty-one. Twenty-two. "
    "Twenty-three. Twenty-four. Twenty-five. Twenty-six. Twenty-seven. Twenty-eight. "
    "Twenty-nine. Thirty. Thirty-one. Thirty-two. Thirty-three. Thirty-four. Thirty-five. "
    "Thirty-six. Thirty-seven. Thirty-eight. Thirty-nine. Forty. Forty-one. "
    "Forty-two. Forty-three. Forty-four. Forty-five. Forty-six. Forty-seven. Forty-eight. "
    "Forty-nine. Fifty."
)

_TOKENIZER = get_tokenizer()


def _app_with_kb_chunk_size(size: int) -> AppConfig:
    cfg = AppConfig()
    kb = cfg.chunking.kb.model_copy(update={"chunk_size": size})
    ch = cfg.chunking.model_copy(update={"kb": kb})
    return cfg.model_copy(update={"chunking": ch})


def test_kb_produces_at_least_one_more_chunk_than_tickets_body_only() -> None:
    # Whole fixture is ~140 tokens: at default 512, KB yields one window node; use a tight N
    # so the splitter emits multiple segments and we still see kb (many) vs tickets (one body).
    cfg = _app_with_kb_chunk_size(32)
    did = "shared-parent-1"
    doc_kb = IngestDocument(id=did, text=_PARAGRAPH, metadata={})
    doc_tickets = IngestDocument(
        id=did,
        text=_PARAGRAPH,
        metadata={},
    )
    n_kb = len(chunk_kb(cfg, doc_kb, "kb"))
    n_ti = len(chunk_tickets(cfg, doc_tickets, "tickets"))
    assert n_kb >= 1
    assert n_ti == 1
    assert n_kb > n_ti, "tickets (body-only) is one body chunk; kb uses token-bounded + windowing"


def test_chunk_kb_respects_max_chunk_size_tokens() -> None:
    n = 64
    cfg = _app_with_kb_chunk_size(n)
    doc = IngestDocument(id="p1", text=_PARAGRAPH, metadata={})
    for node in chunk_kb(cfg, doc, "kb"):
        toks = _TOKENIZER(node.get_content() or "")
        assert len(toks) <= n, f"chunk exceeds {n} tokens: {len(toks)}"


def test_smaller_chunk_size_increases_split_count() -> None:
    doc = IngestDocument(id="p1", text=_PARAGRAPH, metadata={})
    small = _app_with_kb_chunk_size(48)
    default = _app_with_kb_chunk_size(512)
    assert len(chunk_kb(small, doc, "kb")) > len(chunk_kb(default, doc, "kb"))


def test_tickets_with_qa_pairs_count_differs_from_kb() -> None:
    cfg = AppConfig()
    did = "ticket-2"
    doc_kb = IngestDocument(id=did, text=_PARAGRAPH, metadata={})
    doc_ti = IngestDocument(
        id=did,
        text="",
        metadata={
            "qa_pairs": [
                {"question": "Q1", "resolution": "A1 long enough. " * 3},
                {"question": "Q2", "resolution": "A2. " * 2},
            ],
            "summary": "Short",
        },
    )
    n_kb = len(chunk_kb(cfg, doc_kb, "kb"))
    n_ti = len(chunk_tickets(cfg, doc_ti, "tickets"))
    # Two QA nodes + one summary
    assert n_ti == 3
    assert n_kb != n_ti
