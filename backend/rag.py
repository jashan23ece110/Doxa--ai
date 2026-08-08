"""
RAG Facade Module for Backward Compatibility.
Delegates calls to app.services.document_service and app.repositories.vector_repository.
"""

from app.services.document_service import document_service
from app.repositories.vector_repository import vector_repository

get_chroma_collection = vector_repository.get_collection
get_embedding_model = vector_repository.get_embedding_model
generate_doc_id = vector_repository.generate_doc_id

extract_text_from_file = document_service.extract_text_from_file
chunk_text = document_service.chunk_text
add_document = document_service.add_document
list_documents = document_service.list_documents
delete_document = document_service.delete_document
retrieve_context = document_service.retrieve_context
build_rag_prompt = document_service.build_rag_prompt
