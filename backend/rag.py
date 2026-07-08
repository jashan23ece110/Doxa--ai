"""
RAG (Retrieval-Augmented Generation) module for the AI Evaluation Pipeline.

Handles document ingestion, chunking, embedding, storage (ChromaDB),
and context retrieval for augmenting LLM prompts.
"""

import hashlib
import os
from datetime import datetime, timezone
from typing import Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import PyPDF2
import io


# ---------------------------------------------------------------------------
# Singletons / lazy-loaded resources
# ---------------------------------------------------------------------------

_chroma_client: Optional[chromadb.ClientAPI] = None
_chroma_collection = None
_embedding_model: Optional[SentenceTransformer] = None


def get_chroma_collection():
    """Return (or create) the persistent ChromaDB collection."""
    global _chroma_client, _chroma_collection
    if _chroma_collection is None:
        persist_dir = os.getenv('CHROMA_PERSIST_DIR', os.path.join(os.path.dirname(__file__), "chroma_data"))
        _chroma_client = chromadb.PersistentClient(path=persist_dir)
        _chroma_collection = _chroma_client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )
    return _chroma_collection


def get_embedding_model() -> SentenceTransformer:
    """Lazy-load the sentence-transformer embedding model."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def generate_doc_id(filename: str) -> str:
    """Generate a deterministic document ID from the filename (MD5, first 12 chars)."""
    return hashlib.md5(filename.encode("utf-8")).hexdigest()[:12]


def extract_text_from_file(filename: str, content_bytes: bytes) -> str:
    """
    Extract plain text from uploaded file content.

    Supported formats:
      - .txt  — decoded as UTF-8
      - .pdf  — text extracted page-by-page via PyPDF2
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".txt":
        return content_bytes.decode("utf-8", errors="replace")

    if ext == ".pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(content_bytes))
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        return "\n".join(pages_text)

    raise ValueError(f"Unsupported file type: {ext}. Only .txt and .pdf are supported.")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split *text* into overlapping chunks based on word count.

    Parameters
    ----------
    text : str
        The full document text.
    chunk_size : int
        Maximum number of words per chunk.
    overlap : int
        Number of words to overlap between consecutive chunks.

    Returns
    -------
    list[str]
        A list of text chunks.
    """
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


# ---------------------------------------------------------------------------
# Document CRUD
# ---------------------------------------------------------------------------


def add_document(filename: str, content_bytes: bytes) -> dict:
    """
    Ingest a document: extract text, chunk, embed, and store in ChromaDB.

    If a document with the same filename was previously uploaded it will be
    replaced (all old chunks are deleted first).

    Returns
    -------
    dict
        ``{doc_id, filename, chunks_count}``
    """
    doc_id = generate_doc_id(filename)
    collection = get_chroma_collection()
    model = get_embedding_model()

    # Remove existing chunks for this document (re-upload replaces)
    _delete_chunks_by_doc_id(collection, doc_id)

    # Extract & chunk
    text = extract_text_from_file(filename, content_bytes)
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("No text could be extracted from the file.")

    # Embed all chunks
    embeddings = model.encode(chunks).tolist()

    # Build ChromaDB entries
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "doc_id": doc_id,
            "filename": filename,
            "chunk_index": i,
            "upload_date": datetime.now(timezone.utc).isoformat(),
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )

    return {
        "doc_id": doc_id,
        "filename": filename,
        "chunks_count": len(chunks),
    }


def list_documents() -> list[dict]:
    """
    Return a list of unique documents stored in ChromaDB.

    Each entry contains ``{doc_id, filename, upload_date, chunks_count}``.
    """
    collection = get_chroma_collection()
    all_data = collection.get(include=["metadatas"])

    if not all_data["metadatas"]:
        return []

    docs: dict[str, dict] = {}
    for meta in all_data["metadatas"]:
        did = meta["doc_id"]
        if did not in docs:
            docs[did] = {
                "doc_id": did,
                "filename": meta["filename"],
                "upload_date": meta.get("upload_date", ""),
                "chunks_count": 0,
            }
        docs[did]["chunks_count"] += 1

    return list(docs.values())


def delete_document(doc_id: str) -> dict:
    """
    Delete all chunks belonging to *doc_id*.

    Returns
    -------
    dict
        ``{doc_id, deleted: True}``
    """
    collection = get_chroma_collection()
    _delete_chunks_by_doc_id(collection, doc_id)
    return {"doc_id": doc_id, "deleted": True}


def _delete_chunks_by_doc_id(collection, doc_id: str) -> None:
    """Remove every chunk whose metadata ``doc_id`` matches."""
    existing = collection.get(where={"doc_id": doc_id}, include=["metadatas"])
    if existing["ids"]:
        collection.delete(ids=existing["ids"])


# ---------------------------------------------------------------------------
# Retrieval & prompt building
# ---------------------------------------------------------------------------


def retrieve_context(query: str, n_results: int = 3) -> list[dict]:
    """
    Embed *query* and perform a cosine-similarity search against the
    stored document chunks.

    Returns
    -------
    list[dict]
        Each dict: ``{text, filename, chunk_index, similarity}``
    """
    collection = get_chroma_collection()
    model = get_embedding_model()

    # Check if the collection has any documents
    if collection.count() == 0:
        return []

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    contexts: list[dict] = []
    if results["documents"] and results["documents"][0]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            # ChromaDB cosine distance is in [0, 2]; similarity = 1 - distance
            similarity = round(1.0 - dist, 4)
            contexts.append(
                {
                    "text": doc,
                    "filename": meta.get("filename", ""),
                    "chunk_index": meta.get("chunk_index", 0),
                    "similarity": similarity,
                }
            )

    return contexts


def build_rag_prompt(user_prompt: str, contexts: list[dict]) -> str:
    """
    Build an augmented prompt that injects retrieved context before the
    user's original question.
    """
    if not contexts:
        return user_prompt

    context_block = "\n\n---\n\n".join(
        f"[Source: {ctx['filename']} | Chunk {ctx['chunk_index']}]\n{ctx['text']}"
        for ctx in contexts
    )

    return (
        "Use the following retrieved context to help answer the user's question. "
        "If the context is not relevant, you may ignore it and answer based on "
        "your own knowledge.\n\n"
        "=== RETRIEVED CONTEXT ===\n\n"
        f"{context_block}\n\n"
        "=== END CONTEXT ===\n\n"
        f"User's Question: {user_prompt}"
    )
