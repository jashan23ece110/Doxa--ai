"""
Document Knowledge Base Search Tool.
"""

from app.services.document_service import document_service


def search_documents(query: str) -> str:
    """Searches knowledge base document chunks and formats results."""
    contexts = document_service.retrieve_context(query, n_results=3)
    if not contexts:
        return "No relevant documents found."

    results = []
    for ctx in contexts:
        results.append(f"Document: {ctx['filename']}\nContent: {ctx['text']}")
    return "\n\n---\n\n".join(results)
