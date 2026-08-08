"""
Integration Models for Universal Integration Platform & MCP Engine.

Defines Pydantic data models for ConnectorConfig, ConnectorMetadata, ConnectorHealth,
MCPTool, MCPResource, MCPPrompt, IntegrationResult, and ConnectorType.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ConnectorType(str, Enum):
    """Supported connector protocol types."""

    REST = "rest"
    GRAPHQL = "graphql"
    WEBSOCKET = "websocket"
    GRPC = "grpc"
    MCP = "mcp"
    DATABASE = "database"
    CLOUD_STORAGE = "cloud_storage"
    MESSAGE_QUEUE = "message_queue"
    WEBHOOK = "webhook"
    FILESYSTEM = "filesystem"
    CUSTOM = "custom"


class MCPTool(BaseModel):
    """Model Context Protocol tool schema definition."""

    name: str
    description: str
    input_schema: Dict[str, Any] = Field(default_factory=dict)


class MCPResource(BaseModel):
    """Model Context Protocol resource definition."""

    uri: str
    name: str
    mime_type: Optional[str] = "text/plain"
    description: Optional[str] = None


class MCPPrompt(BaseModel):
    """Model Context Protocol prompt template definition."""

    name: str
    description: Optional[str] = None
    arguments: List[Dict[str, Any]] = Field(default_factory=list)


class ConnectorHealth(BaseModel):
    """Connector health check status."""

    is_healthy: bool = True
    latency_ms: float = 0.0
    error_count: int = 0
    last_check_time: float = Field(default_factory=time.time)


class ConnectorConfig(BaseModel):
    """Configuration for registered integration connector."""

    connector_id: str = Field(default_factory=lambda: f"conn_{uuid.uuid4().hex[:8]}")
    name: str
    connector_type: ConnectorType
    base_url: Optional[str] = None
    auth_type: str = "none"  # oauth2, api_key, bearer, jwt, basic, none
    auth_credentials: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True
    version: str = "1.0.0"
    created_at: float = Field(default_factory=time.time)


class ConnectorMetadata(BaseModel):
    """Metadata describing capabilities of a connector."""

    connector_id: str
    name: str
    connector_type: ConnectorType
    supported_actions: List[str] = Field(default_factory=list)
    mcp_tools: List[MCPTool] = Field(default_factory=list)
    mcp_resources: List[MCPResource] = Field(default_factory=list)
    mcp_prompts: List[MCPPrompt] = Field(default_factory=list)
    health: ConnectorHealth = Field(default_factory=ConnectorHealth)


class IntegrationResult(BaseModel):
    """Unified result model across all integration executions."""

    connector_id: str
    status: str = "success"  # success, error, rate_limited, timeout
    output: Any
    latency_ms: float = 0.0
    error_message: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)
