"""
Modular Tool Registry and Model Context Protocol (MCP) Provider.

Manages self-registering tool instances, generates function calling schemas,
dispatches execution, and exports MCP tool definitions.
"""

from typing import Dict, List, Any, Optional
from app.core.interfaces.tool import ITool
from app.core.logging import logger


class SimpleToolAdapter(ITool):
    """Adapter class wrapping function-based tools into the ITool interface."""

    def __init__(self, name: str, description: str, parameters: Dict[str, Any], handler_func, category: str = "utility"):
        self._name = name
        self._description = description
        self._parameters = parameters
        self._handler_func = handler_func
        self._category = category

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def parameters(self) -> Dict[str, Any]:
        return self._parameters

    @property
    def category(self) -> str:
        return self._category

    async def execute(self, **kwargs) -> str:
        res = self._handler_func(**kwargs)
        if hasattr(res, "__await__"):
            return await res
        return str(res)


class ToolRegistry:
    """Central registry managing tool self-registration, dispatch, and MCP exports."""

    def __init__(self):
        self._tools: Dict[str, ITool] = {}

    def register(self, tool: ITool) -> None:
        """Registers an ITool instance."""
        self._tools[tool.name] = tool
        logger.debug(f"Registered tool '{tool.name}' (Category: {tool.category})")

    def register_func(self, name: str, description: str, parameters: Dict[str, Any], handler_func, category: str = "utility") -> None:
        """Registers a function as an ITool adapter."""
        adapter = SimpleToolAdapter(name, description, parameters, handler_func, category)
        self.register(adapter)

    def get_tool(self, name: str) -> Optional[ITool]:
        """Retrieves registered tool by name."""
        return self._tools.get(name)

    def get_tools_def(self) -> List[Dict[str, Any]]:
        """Exports all registered tools as an OpenAI-compatible function definitions array."""
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def get_mcp_schemas(self) -> List[Dict[str, Any]]:
        """Exports all registered tools in Model Context Protocol (MCP) schema format."""
        return [tool.to_mcp_schema() for tool in self._tools.values()]

    async def execute_tool(self, name: str, args: Dict[str, Any]) -> str:
        """Dispatches execution to registered tool by name."""
        tool = self.get_tool(name)
        if not tool:
            logger.error(f"Tool execution failed: '{name}' is not registered.")
            return f"Unknown tool: {name}"
        try:
            return await tool.execute(**args)
        except Exception as e:
            logger.error(f"Error executing tool '{name}': {e}")
            return f"Error executing tool: {e}"


# Global tool registry instance
tool_registry = ToolRegistry()
