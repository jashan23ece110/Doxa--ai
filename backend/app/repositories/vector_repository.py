"""
Vector Repository for ChromaDB Document Storage and Non-Blocking Retrieval.

Implements IVectorRepository interface and uses EmbeddingProviderFactory strategy.
"""

import asyncio
import hashlib
import time
from typing import List, Dict, Any, Optional
import chromadb
from app.core.config import settings
from app.core.factories.embedding_factory import EmbeddingProviderFactory
from app.core.interfaces.embedding_provider import IEmbeddingProvider
from app.core.interfaces.vector_repository import IVectorRepository
from app.core.logging import logger


class VectorRepository(IVectorRepository):
    """Encapsulates ChromaDB collection access, non-blocking embeddings, and document listing cache."""

    def __init__(self, embedding_provider_name: str = "sentence_transformers"):
        self._chroma_client: Optional[chromadb.ClientAPI] = None
        self._collection = None
        self._embedding_provider_name = embedding_provider_name
        self._embedding_provider: Optional[IEmbeddingProvider] = None
        self._doc_list_cache: Optional[List[Dict[str, Any]]] = None
        self._doc_list_cache_time: float = 0.0
        self._cache_ttl_seconds: float = 10.0

    def get_collection(self):
        """Returns or initializes the persistent ChromaDB collection."""
        if self._collection is None:
            persist_dir = settings.CHROMA_PERSIST_DIR
            logger.info(f"Initializing ChromaDB PersistentClient at {persist_dir}")
            self._chroma_client = chromadb.PersistentClient(path=persist_dir)
            self._collection = self._chroma_client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def get_embedding_provider(self) -> IEmbeddingProvider:
        """Lazy-obtains the configured IEmbeddingProvider strategy instance."""
        if self._embedding_provider is None:
            self._embedding_provider = EmbeddingProviderFactory.get_provider(self._embedding_provider_name)
        return self._embedding_provider

    # Backward compatibility alias
    def get_embedding_model(self):
        return self.get_embedding_provider()

    def invalidate_cache(self) -> None:
        """Invalidates the document list cache."""
        self._doc_list_cache = None
        self._doc_list_cache_time = 0.0

    @staticmethod
    def generate_doc_id(filename: str) -> str:
        """Generates a deterministic 12-char MD5 document ID from filename."""
        return hashlib.md5(filename.encode("utf-8")).hexdigest()[:12]

    def _sync_delete_chunks(self, doc_id: str) -> None:
        """Synchronously deletes all chunks belonging to doc_id from ChromaDB."""
        collection = self.get_collection()
        existing = collection.get(where={"doc_id": doc_id}, include=["metadatas"])
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
        self.invalidate_cache()

    async def delete_chunks_by_doc_id(self, doc_id: str) -> None:
        """Deletes all chunks belonging to doc_id off the main event loop thread."""
        await asyncio.to_thread(self._sync_delete_chunks, doc_id)

    def _sync_add_chunks(self, doc_id: str, filename: str, chunks: List[str], metadatas: List[Dict[str, Any]]) -> None:
        """Synchronously embeds and inserts text chunks into ChromaDB."""
        collection = self.get_collection()
        provider = self.get_embedding_provider()

        self._sync_delete_chunks(doc_id)

        start_time = time.time()
        embeddings = provider.encode(chunks)
        embed_time = (time.time() - start_time) * 1000
        logger.debug(f"Encoded {len(chunks)} chunks in {embed_time:.2f}ms")

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        self.invalidate_cache()

    async def add_chunks(self, doc_id: str, filename: str, chunks: List[str], metadatas: List[Dict[str, Any]]) -> None:
        """Embeds and inserts text chunks into ChromaDB off the main event loop thread."""
        await asyncio.to_thread(self._sync_add_chunks, doc_id, filename, chunks, metadatas)

    def _sync_list_all_documents(self) -> List[Dict[str, Any]]:
        """Synchronously returns unique documents stored in ChromaDB with metadata & chunk counts."""
        now = time.time()
        if self._doc_list_cache is not None and (now - self._doc_list_cache_time) < self._cache_ttl_seconds:
            return self._doc_list_cache

        collection = self.get_collection()
        all_data = collection.get(include=["metadatas"])

        if not all_data["metadatas"]:
            self._doc_list_cache = []
            self._doc_list_cache_time = now
            return []

        docs: Dict[str, Dict[str, Any]] = {}
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

        result = list(docs.values())
        self._doc_list_cache = result
        self._doc_list_cache_time = now
        return result

    async def list_all_documents(self) -> List[Dict[str, Any]]:
        """Returns unique documents stored in ChromaDB off the main event loop thread."""
        return await asyncio.to_thread(self._sync_list_all_documents)

    def _sync_query_similar(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Synchronously performs cosine-similarity search against document chunks."""
        collection = self.get_collection()
        if collection.count() == 0:
            return []

        provider = self.get_embedding_provider()
        query_embedding = provider.encode([query])

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=min(n_results, collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        contexts: List[Dict[str, Any]] = []
        if results["documents"] and results["documents"][0]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
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

    async def query_similar(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Performs cosine-similarity search against document chunks off the main event loop thread."""
        return await asyncio.to_thread(self._sync_query_similar, query, n_results)


vector_repository = VectorRepository()
