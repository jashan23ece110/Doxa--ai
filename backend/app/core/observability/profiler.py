"""
Performance Profiler for Enterprise Observability Platform.

Profiles CPU hotspots, slow functions, blocking operations, and long-running tasks.
"""

import time
import threading
from typing import Dict, Any, List


class PerformanceProfiler:
    """Profiles execution functions and identifies latency hotspots."""

    def __init__(self):
        self._lock = threading.Lock()
        self._function_timings: Dict[str, List[float]] = {}

    def record_function_execution(self, func_name: str, duration_ms: float) -> None:
        """Records function execution timing."""
        with self._lock:
            if func_name not in self._function_timings:
                self._function_timings[func_name] = []
            self._function_timings[func_name].append(duration_ms)
            if len(self._function_timings[func_name]) > 1000:
                self._function_timings[func_name] = self._function_timings[func_name][-1000:]

    def get_slowest_functions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Returns top N slowest functions by average duration."""
        with self._lock:
            summary = []
            for func, timings in self._function_timings.items():
                if timings:
                    avg_dur = round(sum(timings) / len(timings), 2)
                    summary.append({"function": func, "avg_duration_ms": avg_dur, "calls": len(timings)})

            summary.sort(key=lambda item: item["avg_duration_ms"], reverse=True)
            return summary[:limit]


# Global PerformanceProfiler instance
profiler = PerformanceProfiler()
