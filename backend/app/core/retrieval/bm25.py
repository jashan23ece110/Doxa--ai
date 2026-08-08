"""
Persistent BM25 Okapi Sparse Keyword Search Index.

Provides thread-safe, lightweight, pure-Python Okapi BM25 keyword indexing and retrieval
with JSON disk persistence to complement ChromaDB dense vector search.
"""

import json
import math
import os
import re
import threading
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from app.core.config import settings
from app.core.logging import logger


class BM25Index:
    """Okapi BM25 sparse keyword search index with disk persistence."""

    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
        persistence_path: Optional[str] = None,
    ):
        self.k1 = k1
        self.b = b
        self.persistence_path = persistence_path or settings.BM25_INDEX_PATH
        self._lock = threading.Lock()

        # In-memory index data structures
        self.doc_chunks: Dict[str, Dict[str, Any]] = {}  # chunk_id -> {text, metadata, tokens, doc_len}
        self.inverted_index: Dict[str, Dict[str, int]] = {}  # term -> {chunk_id -> tf}
        self.avg_doc_len: float = 0.0
        self.total_docs: int = 0

        self._load_from_disk()

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenizes text into lowercase alphanumeric term tokens."""
        if not text:
            return []
        tokens = re.findall(r'\b\w+\b', text.lower())
        # Filter single char or numeric tokens
        return [t for t in tokens if len(t) > 1 and not t.isdigit()]

    def _recalculate_stats(self) -> None:
        """Recalculates average document chunk length."""
        self.total_docs = len(self.doc_chunks)
        if self.total_docs > 0:
            total_len = sum(d["doc_len"] for d in self.doc_chunks.values())
            self.avg_doc_len = total_len / self.total_docs
        else:
            self.avg_doc_len = 0.0

    def _save_to_disk(self) -> None:
        """Persists index state to JSON file on disk."""
        if not self.persistence_path:
            return
        try:
            parent_dir = Path(self.persistence_path).parent
            parent_dir.mkdir(parents=True, exist_ok=True)

            data = {
                "doc_chunks": self.doc_chunks,
                "inverted_index": self.inverted_index,
                "avg_doc_len": self.avg_doc_len,
                "total_docs": self.total_docs,
            }
            with open(self.persistence_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            logger.debug(f"Persisted BM25 index ({self.total_docs} chunks) to {self.persistence_path}")
        except Exception as e:
            logger.error(f"Failed to persist BM25 index to disk: {e}")

    def _load_from_disk(self) -> None:
        """Loads index state from JSON file on disk if exists."""
        if not self.persistence_path or not os.path.exists(self.persistence_path):
            return
        try:
            with open(self.persistence_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.doc_chunks = data.get("doc_chunks", {})
            self.inverted_index = data.get("inverted_index", {})
            self.avg_doc_len = data.get("avg_doc_len", 0.0)
            self.total_docs = data.get("total_docs", 0)
            logger.info(f"Loaded BM25 index ({self.total_docs} chunks) from {self.persistence_path}")
        except Exception as e:
            logger.warning(f"Failed to load BM25 index from disk: {e}")

    def add_document_chunks(
        self,
        doc_id: str,
        chunks: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        """Indexes text chunks for a document into BM25 index."""
        with self._lock:
            # 1. Purge existing chunks for doc_id
            self._sync_delete_chunks_by_doc_id(doc_id)

            # 2. Index new chunks
            for idx, (text, meta) in enumerate(zip(chunks, metadatas)):
                chunk_id = f"{doc_id}_chunk_{idx}"
                tokens = self.tokenize(text)
                doc_len = len(tokens)

                tf_counts: Dict[str, int] = {}
                for t in tokens:
                    tf_counts[t] = tf_counts.get(t, 0) + 1

                self.doc_chunks[chunk_id] = {
                    "text": text,
                    "metadata": meta,
                    "doc_len": doc_len,
                }

                for term, tf in tf_counts.items():
                    if term not in self.inverted_index:
                        self.inverted_index[term] = {}
                    self.inverted_index[term][chunk_id] = tf

            self._recalculate_stats()
            self._save_to_disk()

    def _sync_delete_chunks_by_doc_id(self, doc_id: str) -> None:
        """Internal un-locked deletion of chunks belonging to doc_id."""
        to_delete = [
            cid for cid, cdata in self.doc_chunks.items()
            if cdata.get("metadata", {}).get("doc_id") == doc_id
        ]
        for cid in to_delete:
            del self.doc_chunks[cid]
            # Remove chunk from inverted index
            for term, postings in list(self.inverted_index.items()):
                postings.pop(cid, None)
                if not postings:
                    del self.inverted_index[term]

    def delete_document_chunks(self, doc_id: str) -> None:
        """Deletes all chunks associated with doc_id from BM25 index."""
        with self._lock:
            self._sync_delete_chunks_by_doc_id(doc_id)
            self._recalculate_stats()
            self._save_to_disk()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Executes Okapi BM25 keyword search for a query string."""
        with self._lock:
            if not self.doc_chunks or not query.strip():
                return []

            query_tokens = self.tokenize(query)
            if not query_tokens:
                return []

            scores: Dict[str, float] = {}
            N = self.total_docs
            avgdl = self.avg_doc_len if self.avg_doc_len > 0 else 1.0

            for token in query_tokens:
                if token not in self.inverted_index:
                    continue

                postings = self.inverted_index[token]
                n_q = len(postings)
                # IDF formula
                idf = math.log((N - n_q + 0.5) / (n_q + 0.5) + 1.0)

                for chunk_id, tf in postings.items():
                    doc_len = self.doc_chunks[chunk_id]["doc_len"]
                    numerator = tf * (self.k1 + 1.0)
                    denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / avgdl))
                    scores[chunk_id] = scores.get(chunk_id, 0.0) + (idf * (numerator / denominator))

            if not scores:
                return []

            # Sort by score descending
            ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

            results = []
            for chunk_id, score in ranked:
                cdata = self.doc_chunks[chunk_id]
                meta = cdata["metadata"]
                results.append({
                    "text": cdata["text"],
                    "filename": meta.get("filename", ""),
                    "chunk_index": meta.get("chunk_index", 0),
                    "doc_id": meta.get("doc_id", ""),
                    "bm25_score": round(score, 4),
                    "retrieval_source": "bm25",
                })

            return results


# Global BM25 index instance
bm25_index = BM25Index()
