"""
Security Configuration for Enterprise Cybersecurity & Reverse Engineering Platform.
"""

import os
from typing import Optional


class SecurityResearchConfig:
    """Security Research Configuration settings."""

    # Maximum file size for binary analysis upload (default: 100MB)
    MAX_BINARY_SIZE_BYTES: int = 100 * 1024 * 1024

    # Timeout for sandbox execution (seconds)
    SANDBOX_TIMEOUT_SECONDS: float = 60.0

    # Timeout for static/dynamic analysis pipeline (seconds)
    ANALYSIS_TIMEOUT_SECONDS: float = 120.0

    # Upload rate limit (uploads per minute per tenant)
    UPLOAD_LIMIT_PER_MINUTE: int = 30

    # Cache TTL for analysis results and IOC lookups (seconds)
    CACHE_TTL_SECONDS: float = 3600.0

    # Number of async security research workers
    WORKER_COUNT: int = 4

    # Retention period for generated threat reports (days)
    REPORT_RETENTION_DAYS: int = 90

    # Retention period for forensic artifacts (days)
    FORENSIC_RETENTION_DAYS: int = 180

    # In-memory IOC cache size limit
    IOC_CACHE_MAX_ENTRIES: int = 50000

    # Plugin directory path for custom analyzers and RE tools
    PLUGIN_DIRECTORY: str = os.getenv("SECURITY_PLUGIN_DIR", "./security_plugins")


security_config = SecurityResearchConfig()
