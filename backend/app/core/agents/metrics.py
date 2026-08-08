"""
Agent Metrics Tracker for Enterprise Multi-Agent Operating System.

Tracks active, idle, and failed agents, restarts, handoffs, collaborations,
workspace objects, messages sent/received, and consensus latency.
"""

import threading
from typing import Dict, Any, List


class AgentMetricsTracker:
    """Thread-safe metrics tracker for multi-agent OS operations."""

    def __init__(self):
        self._lock = threading.Lock()
        self.active_agents_count: int = 0
        self.idle_agents_count: int = 0
        self.failed_agents_count: int = 0
        self.agent_restarts_count: int = 0
        self.handoff_count: int = 0
        self.collaboration_count: int = 0
        self.workspace_objects_count: int = 0
        self.messages_sent_count: int = 0
        self.messages_received_count: int = 0
        self.consensus_latencies_ms: List[float] = []

    def record_agent_status(self, active: int = 0, idle: int = 0, failed: int = 0) -> None:
        """Updates active, idle, and failed agent counts."""
        with self._lock:
            self.active_agents_count = active
            self.idle_agents_count = idle
            self.failed_agents_count = failed

    def record_restart(self) -> None:
        """Records an agent restart event."""
        with self._lock:
            self.agent_restarts_count += 1
            self.failed_agents_count = max(self.failed_agents_count - 1, 0)

    def record_handoff(self) -> None:
        """Records an inter-agent task handoff."""
        with self._lock:
            self.handoff_count += 1

    def record_collaboration(self) -> None:
        """Records a multi-agent collaboration execution."""
        with self._lock:
            self.collaboration_count += 1

    def record_message(self) -> None:
        """Records inter-agent message passing."""
        with self._lock:
            self.messages_sent_count += 1
            self.messages_received_count += 1

    def record_consensus_latency(self, latency_ms: float) -> None:
        """Records conflict consensus resolution latency."""
        with self._lock:
            self.consensus_latencies_ms.append(latency_ms)
            if len(self.consensus_latencies_ms) > 1000:
                self.consensus_latencies_ms = self.consensus_latencies_ms[-1000:]

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary statistics across multi-agent OS operations."""
        with self._lock:
            avg_consensus_lat = (
                round(sum(self.consensus_latencies_ms) / len(self.consensus_latencies_ms), 2)
                if self.consensus_latencies_ms
                else 0.0
            )

            return {
                "active_agents": self.active_agents_count,
                "idle_agents": self.idle_agents_count,
                "failed_agents": self.failed_agents_count,
                "agent_restarts": self.agent_restarts_count,
                "handoff_count": self.handoff_count,
                "collaboration_count": self.collaboration_count,
                "workspace_objects": self.workspace_objects_count,
                "messages_sent": self.messages_sent_count,
                "messages_received": self.messages_received_count,
                "consensus_latency_ms": avg_consensus_lat,
            }


# Global AgentMetricsTracker instance
agent_metrics_tracker = AgentMetricsTracker()
