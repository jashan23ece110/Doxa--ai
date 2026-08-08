"""
Document Service for Knowledge Base RAG Operations with Hybrid Retrieval, Memory, & Context Engineering.

Handles file upload validation, magic byte verification, prompt injection defense,
word-level chunking, synchronized ChromaDB & BM25 index updating, hybrid retrieval, memory context, and context engine prompt optimization.
"""

import asyncio
import io
import os
from datetime import datetime, timezone
from typing import List, Dict, Any
from app.core.config import settings
from app.core.context.context_engine import context_engine
from app.core.events import event_dispatcher, EventType
from app.core.exceptions import BadRequestError
from app.core.logging import logger
from app.core.memory.memory_manager import memory_manager
from app.core.retrieval.bm25 import bm25_index
from app.core.retrieval.hybrid import hybrid_retriever
from app.core.security import DocumentSanitizer, PromptSanitizer
from app.repositories.vector_repository import vector_repository


class DocumentService:
    """Service handling RAG document ingestion, security validation, and hybrid context retrieval."""

    @staticmethod
    def extract_text_from_file(filename: str, content_bytes: bytes) -> str:
        """Extracts text content from uploaded file bytes (.txt or .pdf). Lazy-loads PyPDF2."""
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".txt":
            return content_bytes.decode("utf-8", errors="replace")

        if ext == ".pdf":
            try:
                import PyPDF2
            except ImportError:
                raise BadRequestError("PDF processing library PyPDF2 is not installed.")

            try:
                reader = PyPDF2.PdfReader(io.BytesIO(content_bytes))
                pages_text = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                return "\n".join(pages_text)
            except Exception as e:
                raise BadRequestError(f"Failed to parse PDF document content: {e}")

        raise BadRequestError(f"Unsupported file type: {ext}. Only .txt and .pdf are supported.")

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = settings.RAG_DEFAULT_CHUNK_SIZE,
        overlap: int = settings.RAG_DEFAULT_OVERLAP,
    ) -> List[str]:
        """Splits text into overlapping word-based chunks using memory-efficient generators."""
        words = text.split()
        if not words:
            return []

        chunks: List[str] = []
        start = 0
        total_words = len(words)
        step = chunk_size - overlap

        while start < total_words:
            end = start + chunk_size
            chunks.append(" ".join(words[start:end]))
            start += step

        return chunks

    async def add_document(self, filename: str, content_bytes: bytes) -> Dict[str, Any]:
        """Ingests a document securely: validates size/magic-bytes/text, updates ChromaDB & BM25 synchronously."""
        # 1. Security Check: Validate Upload Size & Magic Bytes
        clean_filename, ext = DocumentSanitizer.validate_file_upload(filename, content_bytes)

        # 2. Resource Check: Enforce Maximum Stored Documents
        existing_docs = await vector_repository.list_all_documents()
        if len(existing_docs) >= settings.MAX_DOCUMENT_COUNT:
            doc_id_candidate = vector_repository.generate_doc_id(clean_filename)
            is_replacement = any(d["doc_id"] == doc_id_candidate for d in existing_docs)
            if not is_replacement:
                raise BadRequestError(f"Document storage capacity limit reached ({settings.MAX_DOCUMENT_COUNT} documents max). Please delete unused documents.")

        logger.info(f"Ingesting document '{clean_filename}' ({len(content_bytes)} bytes)")
        doc_id = vector_repository.generate_doc_id(clean_filename)

        # 3. Extraction & Security Inspection
        text = self.extract_text_from_file(clean_filename, content_bytes)
        DocumentSanitizer.inspect_extracted_text(text)

        chunks = self.chunk_text(text)
        if not chunks:
            raise BadRequestError("No readable text could be extracted from the file.")

        upload_date = datetime.now(timezone.utc).isoformat()
        metadatas = [
            {
                "doc_id": doc_id,
                "filename": clean_filename,
                "chunk_index": i,
                "upload_date": upload_date,
            }
            for i in range(len(chunks))
        ]

        # 4. Synchronized Index Ingestion (ChromaDB + BM25)
        await vector_repository.add_chunks(doc_id, clean_filename, chunks, metadatas)
        await asyncio.to_thread(bm25_index.add_document_chunks, doc_id, chunks, metadatas)

        logger.info(f"Successfully indexed document '{clean_filename}' into ChromaDB & BM25 with doc_id={doc_id}, chunks={len(chunks)}")

        # 5. Decoupled Domain Event Publishing
        await event_dispatcher.publish(
            EventType.DOCUMENT_INGESTED,
            {"doc_id": doc_id, "filename": clean_filename, "chunks_count": len(chunks)},
        )

        return {
            "doc_id": doc_id,
            "filename": clean_filename,
            "chunks_count": len(chunks),
        }

    @staticmethod
    async def list_documents() -> List[Dict[str, Any]]:
        """Returns all documents stored in the knowledge base asynchronously."""
        return await vector_repository.list_all_documents()

    @staticmethod
    async def delete_document(doc_id: str) -> Dict[str, Any]:
        """Deletes a document and its chunks from ChromaDB and BM25 index synchronously."""
        if not doc_id or not doc_id.isalnum():
            raise BadRequestError("Invalid document ID specified.")
        logger.info(f"Deleting document doc_id={doc_id}")

        # Synchronized Deletion (ChromaDB + BM25)
        await vector_repository.delete_chunks_by_doc_id(doc_id)
        await asyncio.to_thread(bm25_index.delete_document_chunks, doc_id)

        # Decoupled Domain Event Publishing
        await event_dispatcher.publish(
            EventType.DOCUMENT_DELETED,
            {"doc_id": doc_id},
        )

        return {"doc_id": doc_id, "deleted": True}

    @staticmethod
    async def retrieve_context(query: str, n_results: int = settings.RAG_DEFAULT_TOP_K) -> List[Dict[str, Any]]:
        """Retrieves relevant context chunks using Hybrid (Dense + BM25 + RRF + Cross-Encoder) retrieval."""
        if not query or not query.strip():
            return []
        cleaned_query = PromptSanitizer.sanitize_user_input(query)
        return await hybrid_retriever.retrieve_context(cleaned_query, n_results=n_results)

    @staticmethod
    def build_rag_prompt(user_prompt: str, contexts: List[Dict[str, Any]], memory_context: str = "") -> str:
        """Constructs an enterprise token-budgeted, deduplicated, structured RAG prompt via ContextEngine."""
        return context_engine.build_optimal_prompt(
            user_prompt=user_prompt,
            contexts=contexts,
            memory_context=memory_context,
        )


document_service = DocumentService()
