"""
Startup Configuration and Storage Permissions Validator.

Verifies environment settings, validates filesystem write permissions for storage directories,
and logs diagnostic warnings at application startup.
"""

import os
from pathlib import Path
from app.core.config import settings
from app.core.logging import logger


class ConfigValidator:
    """Validates application configuration and directory write permissions at startup."""

    @staticmethod
    def validate_startup_configuration() -> None:
        """Executes all startup configuration and permission checks. Fails fast if unwritable."""
        logger.info(f"Validating startup configuration for environment profile: '{settings.ENVIRONMENT.upper()}'")

        # 1. Validate Vector Store Directory
        chroma_dir = Path(settings.CHROMA_PERSIST_DIR)
        try:
            chroma_dir.mkdir(parents=True, exist_ok=True)
            test_file = chroma_dir / ".write_test"
            test_file.touch()
            test_file.unlink()
            logger.info(f"Storage directory writable: {chroma_dir}")
        except Exception as e:
            logger.critical(f"FATAL: Vector storage directory '{chroma_dir}' is not writable: {e}")
            raise RuntimeError(f"Storage permission failure for '{chroma_dir}': {e}")

        # 2. Check LLM Provider Configuration
        if not settings.TOKENROUTER_API_KEY:
            logger.warning(
                "TOKENROUTER_API_KEY environment variable is not set. "
                "LLM completion calls will fail unless an API key is provided."
            )
        else:
            logger.info("TokenRouter LLM provider credentials configured.")

        # 3. Check Web Search Configuration
        if not settings.TAVILY_API_KEY:
            logger.warning("TAVILY_API_KEY is not set. Web search tool fallback active.")
        else:
            logger.info("Tavily web search API credentials configured.")

        # 4. Check OAuth Credentials
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            logger.info("Google OAuth credentials not configured. Calendar integration mock mode active.")

        logger.info("Startup configuration validation successful.")
