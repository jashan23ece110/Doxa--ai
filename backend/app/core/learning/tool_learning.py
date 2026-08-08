"""
Tool Learning Engine for Enterprise Continuous Learning Layer.

Tracks tool success rate, failure rate, execution latency, usefulness, and retries.
Generates recommendations for tool ordering, priority, timeouts, and disable suggestions.
"""

import threading
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.learning.learning_metrics import learning_metrics_tracker
from app.core.logging import logger


class ToolExecutionStats(BaseModel):
    """Execution metrics for an individual tool."""

    tool_name: str
    invocations: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_latency_ms: float = 0.0

    @property
    def success_rate(self) -> float:
        return round(self.success_count / self.invocations, 2) if self.invocations > 0 else 1.0

    @property
    def avg_latency_ms(self) -> float:
        return round(self.total_latency_ms / self.invocations, 2) if self.invocations > 0 else 0.0


class ToolLearningEngine:
    """Tracks tool execution statistics and generates optimization recommendations."""

    def __init__(self):
        self._lock = threading.Lock()
        self._stats: Dict[str, ToolExecutionStats] = {}

    def record_tool_execution(
        self,
        tool_name: str,
        success: bool = True,
        latency_ms: float = 0.0,
    ) -> None:
        """Records a tool execution event."""
        with self._lock:
            if tool_name not in self._stats:
                self._stats[tool_name] = ToolExecutionStats(tool_name=tool_name)

            stat = self._stats[tool_name]
            stat.invocations += 1
            if success:
                stat.success_count += 1
            else:
                stat.failure_count += 1
            stat.total_latency_ms += latency_ms

    def generate_tool_recommendations(self) -> List[Dict[str, Any]]:
        """Generates recommendations for tool ordering, timeouts, or disable suggestions."""
        recs = []
        with self._lock:
            for tool_name, stat in self._stats.items():
                if stat.invocations >= 5 and stat.success_rate < 0.50:
                    recs.append({
                        "tool_name": tool_name,
                        "type": "disable_suggestion",
                        "reason": f"Tool '{tool_name}' has low success rate ({stat.success_rate * 100}% over {stat.invocations} runs).",
                    })

                if stat.avg_latency_ms > 3000.0:
                    recs.append({
                        "tool_name": tool_name,
                        "type": "timeout_recommendation",
                        "recommended_timeout_s": 5.0,
                        "reason": f"Tool '{tool_name}' has high average latency ({stat.avg_latency_ms}ms).",
                    })

        for r in recs:
            learning_metrics_tracker.record_recommendation(category="tool")
            logger.info(f"Tool Learning Recommendation: {r['tool_name']} ({r['reason']})")

        return recs


# Global ToolLearningEngine instance
tool_learning_engine = ToolLearningEngine()
