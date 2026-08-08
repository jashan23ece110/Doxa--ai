"""
Agent Facade Module for Backward Compatibility.
Delegates calls to app.services.agent_service and app.services.llm_service.
"""

from app.services.agent_service import (
    agent_service,
    classify_sentiment,
)
from app.services.llm_service import llm_service
from app.repositories.trace_repository import trace_repository

# Facade Functions & Aliases
run_agent_loop = agent_service.run_agent_loop
save_trace = trace_repository.save_trace
get_trace = trace_repository.get_trace
global_traces = trace_repository._global_traces

call_tokenrouter = llm_service.call_tokenrouter
call_gemini = llm_service.call_tokenrouter
call_llama = llm_service.call_tokenrouter

from app.tools.document_search import search_documents
from app.tools.base import TOOLS_DEF
