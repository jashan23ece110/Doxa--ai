"""
Structured Logging and Security Audit Logging Module.

Provides root application logger and dedicated security audit logger with formatting
that redacts sensitive keys and secrets.
"""

import sys
import logging
import re
from app.core.config import settings


class SecretRedactingFormatter(logging.Formatter):
    """Custom log formatter redacting API keys, Bearer tokens, and secrets."""

    SECRET_PATTERNS = [
        re.compile(r'(api_key|token|secret|authorization|password)["\']?\s*[:=]\s*["\']?([^"\'\s&]+)', re.IGNORECASE),
        re.compile(r'(Bearer\s+)[A-Za-z0-9\-\._~\+\/]+=*', re.IGNORECASE),
    ]

    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)
        for pattern in self.SECRET_PATTERNS:
            formatted = pattern.sub(r'\1: [REDACTED]', formatted)
        return formatted


def setup_logging():
    """Configures root logger and security audit logger."""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    formatter = SecretRedactingFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger("doxa")
    root_logger.setLevel(log_level)
    if not root_logger.handlers:
        root_logger.addHandler(handler)

    security_logger = logging.getLogger("doxa.security")
    security_logger.setLevel(logging.INFO)
    if not security_logger.handlers:
        security_logger.addHandler(handler)

    return root_logger, security_logger


logger, security_logger = setup_logging()
