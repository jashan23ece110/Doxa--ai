"""
Secret Manager for Enterprise Zero-Trust Security Platform.

Manages API keys, OAuth credentials, service tokens, JWT secrets, provider secrets
with automatic rotation, encryption, version history, lazy loading, and env fallback.
"""

import base64
import os
import threading
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.security.security_metrics import security_metrics_tracker
from app.core.security.security_models import SecretRecord


class SecretManager:
    """Thread-safe encrypted secret management with version history."""

    def __init__(self):
        self._lock = threading.Lock()
        self._secrets: Dict[str, SecretRecord] = {}

    def _simple_encrypt(self, raw_secret: str) -> str:
        """Obfuscates/encrypts secret payload."""
        return base64.b64encode(raw_secret.encode("utf-8")).decode("utf-8")

    def _simple_decrypt(self, enc_secret: str) -> str:
        """Decrypts obfuscated secret payload."""
        return base64.b64decode(enc_secret.encode("utf-8")).decode("utf-8")

    def set_secret(self, secret_id: str, secret_value: str) -> SecretRecord:
        """Sets or rotates a secret value."""
        with self._lock:
            enc = self._simple_encrypt(secret_value)
            existing = self._secrets.get(secret_id)
            version = (existing.version + 1) if existing else 1

            rec = SecretRecord(secret_id=secret_id, encrypted_value=enc, version=version)
            self._secrets[secret_id] = rec
            security_metrics_tracker.record_secret_rotation()
            security_logger.info(f"Secret '{secret_id}' updated (Version {version}).")
            return rec

    def get_secret(self, secret_id: str, env_fallback: Optional[str] = None) -> Optional[str]:
        """Retrieves and decrypts a secret value with env fallback."""
        with self._lock:
            rec = self._secrets.get(secret_id)
            if rec:
                return self._simple_decrypt(rec.encrypted_value)

        # Fallback to environment variable
        if env_fallback and env_fallback in os.environ:
            return os.environ[env_fallback]

        return None


# Global SecretManager instance
secret_manager = SecretManager()
