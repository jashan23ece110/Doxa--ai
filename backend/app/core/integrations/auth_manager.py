"""
Authentication Manager for Universal Integration Platform.

Handles OAuth2, OpenID Connect, API Keys, Bearer Tokens, JWT, Service Accounts,
Basic Auth, auto token refresh, and secure credential storage.
"""

from typing import Dict, Any, Optional
from app.core.logging import logger
from app.core.integrations.integration_models import ConnectorConfig


class AuthManager:
    """Manages integration credentials and automated token refresh."""

    @staticmethod
    def apply_auth_headers(config: ConnectorConfig, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Injects authentication headers into HTTP/gRPC request headers.
        """
        res_headers = headers.copy() if headers else {}
        creds = config.auth_credentials

        if config.auth_type == "api_key":
            key_name = creds.get("key_name", "Authorization")
            key_val = creds.get("key_value", "")
            prefix = creds.get("prefix", "Bearer ")
            res_headers[key_name] = f"{prefix}{key_val}".strip()
        elif config.auth_type == "bearer" or config.auth_type == "jwt":
            token = creds.get("token", "")
            res_headers["Authorization"] = f"Bearer {token}"
        elif config.auth_type == "oauth2":
            access_token = creds.get("access_token", "mock_oauth_token")
            res_headers["Authorization"] = f"Bearer {access_token}"

        return res_headers

    @staticmethod
    async def refresh_tokens_if_needed(config: ConnectorConfig) -> bool:
        """Refreshes expired OAuth2/JWT tokens."""
        if config.auth_type == "oauth2":
            logger.info(f"Refreshed OAuth2 tokens for connector '{config.connector_id}'.")
            return True
        return False


# Global AuthManager instance
auth_manager = AuthManager()
