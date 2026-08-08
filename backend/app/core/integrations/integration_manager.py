"""
Integration Manager Orchestrator for Universal Integration Platform & MCP Engine.

Central manager for connector registration, discovery, health monitoring, enable/disable,
authentication, and execution. Integrates seamlessly with existing Tool Registry.
"""

from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.integrations.connector_registry import connector_registry
from app.core.integrations.gateway import integration_gateway
from app.core.integrations.integration_models import (
    ConnectorConfig,
    ConnectorMetadata,
    ConnectorType,
    IntegrationResult,
)
from app.core.integrations.integration_repository import integration_repository
from app.core.integrations.mcp_engine import mcp_engine


class IntegrationManager:
    """Central lifecycle orchestrator for Universal Integration & MCP Platform."""

    def __init__(self):
        self._register_default_connectors()

    def _register_default_connectors(self) -> None:
        """Registers built-in default integration connectors (REST & MCP)."""
        c1 = ConnectorConfig(
            name="GitHub API Connector",
            connector_type=ConnectorType.REST,
            base_url="https://api.github.com",
            auth_type="bearer",
            auth_credentials={"token": "mock_github_token"},
        )
        c2 = ConnectorConfig(
            name="Enterprise SQL Database Connector",
            connector_type=ConnectorType.DATABASE,
            base_url="postgresql://localhost:5432/doxa",
            auth_type="basic",
        )
        c3 = ConnectorConfig(
            name="Model Context Protocol Server",
            connector_type=ConnectorType.MCP,
            base_url="mcp://localhost:8080",
            auth_type="api_key",
        )

        for c in (c1, c2, c3):
            connector_registry.register_connector(c)
            integration_repository.save_connector(c)

    async def discover_and_register_mcp_server(
        self,
        name: str,
        base_url: str,
        auth_type: str = "api_key",
        auth_credentials: Optional[Dict[str, Any]] = None,
    ) -> ConnectorConfig:
        """
        Registers an MCP server, negotiates capabilities via MCPEngine,
        and saves configuration to repository.
        """
        config = ConnectorConfig(
            name=name,
            connector_type=ConnectorType.MCP,
            base_url=base_url,
            auth_type=auth_type,
            auth_credentials=auth_credentials or {},
        )

        metadata = await mcp_engine.discover_mcp_capabilities(config)
        connector_registry.register_connector(config, metadata=metadata)
        integration_repository.save_connector(config)

        logger.info(f"Successfully discovered and registered MCP server '{name}' at '{base_url}'.")
        return config

    async def execute_integration(
        self,
        connector_id: str,
        action: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> IntegrationResult:
        """
        Delegates execution to IntegrationGateway.
        """
        return await integration_gateway.invoke_connector(
            connector_id,
            action,
            params=params,
            headers=headers,
        )

    def list_connectors(self) -> List[ConnectorConfig]:
        """Lists all registered connectors."""
        return connector_registry.list_connectors()


# Global IntegrationManager instance
integration_manager = IntegrationManager()
