"""
Master Tool Definitions Registry and Provider.

Registers all core tools (search_documents, summarize_text, draft_message,
brave_search, calculate, list_calendar_events, create_calendar_event,
execute_python_code, set_timer) into tool_registry and exports TOOLS_DEF.
"""

from typing import List, Dict, Any
from app.tools.registry import tool_registry

# Register Core Tools into tool_registry
tool_registry.register_func(
    name="search_documents",
    description="Search internal knowledge base documents for relevant context or answers.",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query to match against documents."}
        },
        "required": ["query"],
    },
    handler_func=None,  # Dispatched dynamically in agent_service
    category="rag",
)

tool_registry.register_func(
    name="summarize_text",
    description="Summarize long text, articles, or transcripts into key points.",
    parameters={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "The text to summarize."}
        },
        "required": ["text"],
    },
    handler_func=None,
    category="utility",
)

tool_registry.register_func(
    name="draft_message",
    description="Draft an email, message, or formal communication based on context and purpose.",
    parameters={
        "type": "object",
        "properties": {
            "context": {"type": "string", "description": "Background information for the message."},
            "purpose": {"type": "string", "description": "Goal or objective of the message."}
        },
        "required": ["context", "purpose"],
    },
    handler_func=None,
    category="utility",
)

tool_registry.register_func(
    name="brave_search",
    description="Search the live web for current information, news, code samples, or facts.",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The web search query."}
        },
        "required": ["query"],
    },
    handler_func=None,
    category="search",
)

tool_registry.register_func(
    name="calculate",
    description="Safely evaluate mathematical expressions (e.g. '24 * 15', 'sqrt(144)').",
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Math expression string to evaluate."}
        },
        "required": ["expression"],
    },
    handler_func=None,
    category="utility",
)

tool_registry.register_func(
    name="list_calendar_events",
    description="List upcoming Google Calendar events.",
    parameters={
        "type": "object",
        "properties": {},
    },
    handler_func=None,
    category="integration",
)

tool_registry.register_func(
    name="create_calendar_event",
    description="Schedule a new Google Calendar event.",
    parameters={
        "type": "object",
        "properties": {
            "summary": {"type": "string", "description": "Event title or summary."},
            "start_time": {"type": "string", "description": "Start time ISO string (e.g. '2026-08-06T10:00:00Z')."},
            "duration_minutes": {"type": "integer", "description": "Duration in minutes (default 30)."},
            "description": {"type": "string", "description": "Optional event description."}
        },
        "required": ["summary", "start_time"],
    },
    handler_func=None,
    category="integration",
)

tool_registry.register_func(
    name="execute_python_code",
    description="Execute a Python script safely inside an isolated subprocess and return standard output or error.",
    parameters={
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python code snippet to execute."}
        },
        "required": ["code"],
    },
    handler_func=None,
    category="execution",
)

tool_registry.register_func(
    name="set_timer",
    description="Schedule an in-app alarm or reminder timer that triggers a real-time notification.",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Title or label for the timer/reminder."},
            "duration_seconds": {"type": "integer", "description": "Duration in seconds until the timer fires."}
        },
        "required": ["title", "duration_seconds"],
    },
    handler_func=None,
    category="utility",
)

# Export OpenAI tool schema list derived from tool_registry
TOOLS_DEF: List[Dict[str, Any]] = tool_registry.get_tools_def()
