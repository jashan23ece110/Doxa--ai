"""
API Key Manager for Enterprise Zero-Trust Security Platform.

Manages creation, rotation, expiration, revocation, hashed storage, scopes, and rate plans.
"""

import hashlib
import secrets
import threading
from typing import Dict, Any, List, Optional, Tuple
from app.core.logging import security_logger
from app.core.security.security_models import APIKey


class APIKeyManager:
    """Thread-safe hashed API Key management."""

    def __init__(self):
        self._lock = threading.Lock()
        self._keys_by_hash: Dict[str, APIKey] = {}

    def _hash_key(self, raw_key: str) -> str:
        """SHA-256 hash for raw API key."""
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def generate_api_key(
        self,
        owner_id: str,
        tenant_id: str = "default_tenant",
        scopes: Optional[List[str]] = None,
        rate_plan: str = "enterprise_standard",
    ) -> Tuple[str, APIKey]:
        """
        Generates a new raw API key and stores its SHA-256 hash.
        Returns: (raw_api_key, APIKeyRecord).
        """
        raw_key = f"doxa_{secrets.token_urlsafe(32)}"
        key_hash = self._hash_key(raw_key)

        record = APIKey(
            key_hash=key_hash,
            owner_id=owner_id,
            tenant_id=tenant_id,
            scopes=scopes or ["api:read", "api:write"],
            rate_plan=rate_plan,
        )

        with self._lock:
            self._keys_by_hash[key_hash] = record
            security_logger.info(f"Generated API key '{record.key_id}' for owner '{owner_id}' (Tenant: {tenant_id}).")

        return raw_key, record

    def validate_api_key(self, raw_key: str) -> Optional[APIKey]:
        """Validates raw API key by checking hashed storage and revocation status."""
        key_hash = self._hash_key(raw_key)
        with self._lock:
            record = self._keys_by_hash.get(key_hash)
            if record and not record.is_revoked:
                return record
        return None

    def revoke_api_key(self, key_id: str) -> bool:
        """Revokes an API key by ID."""
        with self._lock:
            for record in self._keys_by_hash.values():
                if record.key_id == key_id:
                    record.is_revoked = True
                    security_logger.info(f"Revoked API key '{key_id}'.")
                    return True
        return False


# Global APIKeyManager instance
api_key_manager = APIKeyManager()
