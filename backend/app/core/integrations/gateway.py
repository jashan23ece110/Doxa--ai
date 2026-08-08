"""
Integration Gateway for Universal Integration Platform.

Unified protocol abstraction layer providing a single clean interface regardless of backend
protocol (REST, GraphQL, WebSocket, gRPC, DB, MCP).
"""

from typing import Dict, Any, Optional
from app.core.integrations.connector_executor import connector_executor
from app.core.integrations.connector_registry import connector_registry
from app.core.integrations.integration_models import IntegrationResult


class IntegrationGateway:
    """Unified abstraction gateway normalizing all external integration calls."""

    async def invoke_connector(
        self,
        connector_id: str,
        action: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> IntegrationResult:
        """
        Invokes an external connector via the unified IntegrationGateway.
        """
        config = connector_registry.get_config(connector_id)
        if not config:
            return IntegrationResult(
                connector_id=connector_id,
                status="error",
                output=None,
                error_message=f"Connector '{connector_id}' not found in registry.",
            )

        if not config.enabled:
            return IntegrationResult(
                connector_id=connector_id,
                status="error",
                output=None,
                error_message=f"Connector '{config.name}' is currently disabled.",
            )

        return await connector_executor.execute_request(config, action, params=params, headers=headers)


# Global IntegrationGateway instance
integration_gateway = IntegrationGateway()
