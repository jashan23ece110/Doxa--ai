"""
Document Management API Router with Dependency Injection.
"""

from fastapi import APIRouter, UploadFile, File, Depends
from app.schemas.document import DocumentUploadResponse, DocumentListResponse, DocumentDeleteResponse
from app.services.document_service import DocumentService
from app.api.deps import get_document_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    doc_service: DocumentService = Depends(get_document_service),
):
    """Upload a document (.txt or .pdf) to the RAG knowledge base."""
    content_bytes = await file.read()
    result = await doc_service.add_document(file.filename, content_bytes)
    return result


@router.get("", response_model=DocumentListResponse)
async def get_documents(
    doc_service: DocumentService = Depends(get_document_service),
):
    """List all documents in the RAG knowledge base."""
    docs = await doc_service.list_documents()
    return {"documents": docs}


@router.delete("/{doc_id}", response_model=DocumentDeleteResponse)
async def remove_document(
    doc_id: str,
    doc_service: DocumentService = Depends(get_document_service),
):
    """Delete a document and all its chunks from the knowledge base."""
    result = await doc_service.delete_document(doc_id)
    return result
