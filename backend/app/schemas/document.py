"""
Pydantic Schemas for RAG Document Endpoints.
"""

from typing import List
from pydantic import BaseModel, Field


class DocumentItem(BaseModel):
    doc_id: str = Field(..., description="Deterministic 12-char document identifier")
    filename: str = Field(..., description="Original filename")
    upload_date: str = Field(default="", description="ISO timestamp of upload")
    chunks_count: int = Field(..., description="Number of text chunks created")


class DocumentUploadResponse(BaseModel):
    doc_id: str
    filename: str
    chunks_count: int


class DocumentListResponse(BaseModel):
    documents: List[DocumentItem]


class DocumentDeleteResponse(BaseModel):
    doc_id: str
    deleted: bool
