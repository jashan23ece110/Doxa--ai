"""
Abstract Vector Repository Interface.

Defines the contract for vector database integrations (ChromaDB, Qdrant, Milvus, Pinecone, pgvector).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IVectorRepository(ABC):
    """Abstract interface for vector database storage and retrieval."""

    @abstractmethod
    async def add_chunks(
        self,
        doc_id: str,
        filename: str,
        chunks: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        """Stores document text chunks and metadatas into the vector database."""
        pass

    @abstractmethod
    async def delete_chunks_by_doc_id(self, doc_id: str) -> None:
        """Deletes all chunks associated with doc_id from the vector database."""
        pass

    @abstractmethod
    async def list_all_documents(self) -> List[Dict[str, Any]]:
        """Returns unique documents stored in the vector database with statistics."""
        pass

    @abstractmethod
    async def query_similar(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Performs vector similarity search against stored document chunks."""
        pass
