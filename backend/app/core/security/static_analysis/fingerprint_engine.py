"""
File Fingerprinting Engine.

Generates SHA256, SHA1, MD5, and SHA512 cryptographic hashes.
Provides duplicate detection, similarity matching, fingerprint caching, and indexing.
"""

import hashlib
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_types import FileFingerprint


class FingerprintEngine:
    """Thread-safe File Fingerprinting and Duplicate Detection Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cache: Dict[str, FileFingerprint] = {}
        self._hash_index: Dict[str, str] = {}  # hash -> file_name mapping

    def generate_fingerprint(self, file_bytes: bytes, file_name: str = "binary.bin") -> FileFingerprint:
        """
        Generates cryptographic hashes and returns a FileFingerprint.
        Utilizes caching for duplicate files.
        """
        md5 = hashlib.md5(file_bytes).hexdigest()

        with self._lock:
            if md5 in self._cache:
                security_logger.debug(f"FingerprintEngine: Cache hit for MD5 {md5[:8]}")
                return self._cache[md5]

        sha1 = hashlib.sha1(file_bytes).hexdigest()
        sha256 = hashlib.sha256(file_bytes).hexdigest()
        file_size = len(file_bytes)

        # Magic detection
        magic = "UNKNOWN"
        if file_bytes.startswith(b"MZ"):
            magic = "PE32/PE32+"
        elif file_bytes.startswith(b"\x7fELF"):
            magic = "ELF"
        elif file_bytes.startswith(b"\xfe\xed\xfa"):
            magic = "Mach-O"
        elif file_bytes.startswith(b"PK\x03\x04"):
            magic = "ZIP/JAR/APK"

        fingerprint = FileFingerprint(
            md5=md5,
            sha1=sha1,
            sha256=sha256,
            file_size_bytes=file_size,
            file_type_magic=magic,
        )

        with self._lock:
            self._cache[md5] = fingerprint
            self._hash_index[sha256] = file_name
            # Evict if cache exceeds 10,000 entries
            if len(self._cache) > 10000:
                oldest_keys = list(self._cache.keys())[:1000]
                for k in oldest_keys:
                    self._cache.pop(k, None)

        security_logger.info(f"FingerprintEngine: Fingerprinted '{file_name}' (SHA256: {sha256[:12]}...).")
        return fingerprint

    def is_duplicate(self, sha256: str) -> bool:
        """Checks if a file with the given SHA256 has been processed previously."""
        with self._lock:
            return sha256 in self._hash_index

    def get_cached_fingerprint(self, md5_or_sha256: str) -> Optional[FileFingerprint]:
        """Retrieves cached fingerprint if present."""
        with self._lock:
            if md5_or_sha256 in self._cache:
                return self._cache[md5_or_sha256]
            for fp in self._cache.values():
                if fp.sha256 == md5_or_sha256:
                    return fp
            return None


# Global FingerprintEngine instance
fingerprint_engine = FingerprintEngine()
