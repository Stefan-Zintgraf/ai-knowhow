"""Per-namespace chunkers (PRD §2.3.2 R-9)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter, SentenceWindowNodeParser
from llama_index.core.schema import TextNode

from support_rag.chunk_id import stable_chunk_id
from support_rag.config import AppConfig
from support_rag.schemas import IngestDocument


def _base_metadata(
    namespace: str,
    parent_id: str,
    chunk_index: int,
    chunker_version: str,
    src: dict[str, Any],
) -> dict[str, Any]:
    out = {
        "parent_id": parent_id,
        "namespace": namespace,
        "chunk_index": chunk_index,
        "chunker_version": chunker_version,
        "source_uri": src.get("source_uri", src.get("url", "")),
        "product": src.get("product"),
        "lang": src.get("lang"),
        "created_at": int(src.get("created_at", 0)),
        "status": src.get("status"),
    }
    keep = ("parent_id", "namespace", "chunk_index", "chunker_version", "source_uri")
    return {k: v for k, v in out.items() if v is not None or k in keep}


def _kb_splitter_split_text(config: AppConfig) -> Callable[[str], list[str]]:
    """Token-bounded segments for `SentenceWindowNodeParser` (Honors `chunking.kb.chunk_size`)."""
    cs = config.chunking.kb.chunk_size
    # SentenceSplitter overlap must be < chunk_size; default 200 is valid for PRD default 512.
    overlap = min(200, max(0, cs - 1))
    splitter = SentenceSplitter.from_defaults(chunk_size=cs, chunk_overlap=overlap)
    return splitter.split_text


def chunk_kb(config: AppConfig, doc: IngestDocument, namespace: str) -> list[TextNode]:
    cv = config.chunker_version.kb
    parser = SentenceWindowNodeParser.from_defaults(
        sentence_splitter=_kb_splitter_split_text(config),
        window_size=config.chunking.kb.window_size,
    )
    md = dict(doc.metadata)
    md["parent_id"] = doc.id
    md["namespace"] = namespace
    d = Document(text=doc.text, metadata=md, id_=doc.id)
    raw_nodes = parser.get_nodes_from_documents([d])
    nodes: list[TextNode] = []
    for i, n in enumerate(raw_nodes):
        chunk_id = stable_chunk_id(namespace, doc.id, i, cv)
        text = n.get_content()
        base_meta = dict(n.metadata) if n.metadata is not None else {}
        merged = {**base_meta, **_base_metadata(namespace, doc.id, i, cv, md)}
        nodes.append(TextNode(id_=chunk_id, text=text, metadata=merged, ref_doc_id=doc.id))
    return nodes


def chunk_tickets(config: AppConfig, doc: IngestDocument, namespace: str) -> list[TextNode]:
    cv = config.chunker_version.tickets
    md = dict(doc.metadata)
    md["parent_id"] = doc.id
    md["namespace"] = namespace
    nodes: list[TextNode] = []
    idx = 0

    qa = md.get("qa_pairs")
    if isinstance(qa, list) and len(qa) > 0:
        for row in qa:
            if not isinstance(row, dict):
                continue
            q = str(row.get("question", "")).strip()
            a = str(row.get("resolution", "")).strip()
            if not (q or a):
                continue
            text = f"Q: {q}\nA: {a}" if q and a else (q or a)
            chunk_id = stable_chunk_id(namespace, doc.id, idx, cv)
            meta = {**_base_metadata(namespace, doc.id, idx, cv, md), "kind": "qa_pair"}
            nodes.append(TextNode(id_=chunk_id, text=text, metadata=meta, ref_doc_id=doc.id))
            idx += 1
    else:
        text = doc.text.strip()
        if text:
            chunk_id = stable_chunk_id(namespace, doc.id, idx, cv)
            meta = {**_base_metadata(namespace, doc.id, idx, cv, md), "kind": "body"}
            nodes.append(TextNode(id_=chunk_id, text=text, metadata=meta, ref_doc_id=doc.id))
            idx += 1

    summary = str(md.get("summary", "")).strip()
    if summary:
        chunk_id = stable_chunk_id(namespace, doc.id, idx, cv)
        sm = {**_base_metadata(namespace, doc.id, idx, cv, md), "kind": "summary"}
        nodes.append(TextNode(id_=chunk_id, text=summary, metadata=sm, ref_doc_id=doc.id))
    return nodes
