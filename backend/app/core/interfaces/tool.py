"""
Abstract Tool Interface and Model Context Protocol (MCP) Export Schema.

Defines the contract for self-registering agent tools and future MCP server compatibility.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ITool(ABC):
    """Abstract interface for modular, self-registering agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier name of the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what the tool does."""
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON Schema parameter specification for tool arguments."""
        pass

    @property
    def category(self) -> str:
        """Category domain of the tool (utility, search, integration, execution)."""
        return "utility"

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Executes the tool with provided arguments."""
        pass

    def to_openai_schema(self) -> Dict[str, Any]:
        """Exports tool definition in OpenAI function calling schema format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def to_mcp_schema(self) -> Dict[str, Any]:
        """Exports tool definition in Model Context Protocol (MCP) format."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.parameters,
        }
