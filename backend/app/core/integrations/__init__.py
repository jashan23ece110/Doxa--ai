"""Integrations package initialization."""
from app.core.integrations.integration_models import (
    ConnectorType,
    MCPTool,
    MCPResource,
    MCPPrompt,
    ConnectorHealth,
    ConnectorConfig,
    ConnectorMetadata,
    IntegrationResult,
)
from app.core.integrations.connector_registry import connector_registry, ConnectorRegistry
from app.core.integrations.connector_metrics import connector_metrics_tracker, ConnectorMetricsTracker
from app.core.integrations.auth_manager import auth_manager, AuthManager
from app.core.integrations.mcp_engine import mcp_engine, MCPEngine
from app.core.integrations.sandbox import connector_sandbox, ConnectorSandbox
from app.core.integrations.connector_executor import connector_executor, ConnectorExecutor
from app.core.integrations.gateway import integration_gateway, IntegrationGateway
from app.core.integrations.event_bridge import event_bridge, EventBridge
from app.core.integrations.integration_scheduler import integration_scheduler, IntegrationScheduler
from app.core.integrations.integration_repository import integration_repository, JSONIntegrationRepository
from app.core.integrations.integration_manager import integration_manager, IntegrationManager

__all__ = [
    "ConnectorType",
    "MCPTool",
    "MCPResource",
    "MCPPrompt",
    "ConnectorHealth",
    "ConnectorConfig",
    "ConnectorMetadata",
    "IntegrationResult",
    "connector_registry",
    "ConnectorRegistry",
    "connector_metrics_tracker",
    "ConnectorMetricsTracker",
    "auth_manager",
    "AuthManager",
    "mcp_engine",
    "MCPEngine",
    "connector_sandbox",
    "ConnectorSandbox",
    "connector_executor",
    "ConnectorExecutor",
    "integration_gateway",
    "IntegrationGateway",
    "event_bridge",
    "EventBridge",
    "integration_scheduler",
    "IntegrationScheduler",
    "integration_repository",
    "JSONIntegrationRepository",
    "integration_manager",
    "IntegrationManager",
]
