"""
Execution Optimizer for Doxa AI Operating System.

Detects and eliminates duplicate work by memoizing and reusing previous computations for:
Repeated Retrieval, Repeated Embeddings, Repeated Planning, Repeated Reasoning,
Repeated Tool Executions, Duplicate Workflows, and Duplicate Memory Writes.
"""

import hashlib
import json
import threading
import time
from typing import Dict, Any, Optional, Tuple
from app.core.logging import logger
from app.core.config import settings
from app.core.intelligence.intelligence_types import OptimizationCacheEntry


class ExecutionOptimizer:
    """Enterprise Execution Optimizer for eliminating redundant computations."""

    def __init__(self, default_ttl_seconds: float = 300.0):
        self.default_ttl = default_ttl_seconds
        self._cache: Dict[str, OptimizationCacheEntry] = {}
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def generate_cache_key(self, computation_type: str, input_payload: Any) -> str:
        """
        Generates a deterministic MD5 cache key from computation type and payload.
        """
        try:
            if isinstance(input_payload, dict) or isinstance(input_payload, list):
                serialized = json.dumps(input_payload, sort_keys=True, default=str)
            else:
                serialized = str(input_payload)
        except Exception:
            serialized = str(input_payload)

        raw_str = f"{computation_type}:{serialized}"
        return hashlib.md5(raw_str.encode("utf-8")).hexdigest()

    def get_cached_result(self, computation_type: str, input_payload: Any) -> Optional[Any]:
        """
        Retrieves a valid non-expired cached result if present.

        Args:
            computation_type: 'retrieval', 'embedding', 'planning', 'reasoning', 'tool', 'workflow', 'memory_write'.
            input_payload: Payload or parameters of the computation.

        Returns:
            Cached result object, or None if miss/expired.
        """
        if not settings.EXECUTION_OPTIMIZER_ENABLED:
            return None

        key = self.generate_cache_key(computation_type, input_payload)
        now = time.time()

        with self._lock:
            entry = self._cache.get(key)
            if entry:
                # Check expiration
                if (now - entry.cached_at) <= entry.ttl_seconds:
                    entry.hit_count += 1
                    self._hits += 1
                    logger.debug(f"ExecutionOptimizer HIT ({computation_type}): key={key[:8]}, hits={entry.hit_count}")
                    return entry.result
                else:
                    # Expired entry
                    self._cache.pop(key, None)

            self._misses += 1
            return None

    def store_result(
        self,
        computation_type: str,
        input_payload: Any,
        result: Any,
        ttl_seconds: Optional[float] = None,
    ) -> str:
        """
        Stores a computation result in the optimizer cache.

        Args:
            computation_type: Type of computation being cached.
            input_payload: Arguments/inputs used for computation.
            result: Computed result to cache.
            ttl_seconds: Optional custom TTL override.

        Returns:
            The generated cache key.
        """
        if not settings.EXECUTION_OPTIMIZER_ENABLED:
            return ""

        key = self.generate_cache_key(computation_type, input_payload)
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl

        entry = OptimizationCacheEntry(
            cache_key=key,
            computation_type=computation_type,
            result=result,
            hit_count=0,
            cached_at=time.time(),
            ttl_seconds=ttl,
        )

        with self._lock:
            self._cache[key] = entry
            # Prune cache if oversized
            if len(self._cache) > 2000:
                self._evict_oldest()

        logger.debug(f"ExecutionOptimizer STORED ({computation_type}): key={key[:8]}, ttl={ttl}s")
        return key

    def invalidate_type(self, computation_type: str):
        """Invalidates all cache entries for a specific computation type."""
        with self._lock:
            keys_to_remove = [k for k, v in self._cache.items() if v.computation_type == computation_type]
            for k in keys_to_remove:
                self._cache.pop(k, None)
            logger.info(f"ExecutionOptimizer: Invalidated {len(keys_to_remove)} entries for type '{computation_type}'.")

    def get_metrics(self) -> Dict[str, Any]:
        """Returns cache efficiency metrics."""
        with self._lock:
            total = self._hits + self._misses
            hit_rate = round(self._hits / max(total, 1), 4)
            return {
                "cache_size": len(self._cache),
                "total_hits": self._hits,
                "total_misses": self._misses,
                "hit_rate": hit_rate,
            }

    def _evict_oldest(self):
        """Evicts expired or least hit cache entries."""
        now = time.time()
        expired = [k for k, v in self._cache.items() if (now - v.cached_at) > v.ttl_seconds]
        if expired:
            for k in expired:
                self._cache.pop(k, None)
        else:
            # Sort by hit count + age and remove lowest 200
            sorted_entries = sorted(self._cache.items(), key=lambda x: (x[1].hit_count, x[1].cached_at))
            for k, _ in sorted_entries[:200]:
                self._cache.pop(k, None)


# Global ExecutionOptimizer instance
execution_optimizer = ExecutionOptimizer()
