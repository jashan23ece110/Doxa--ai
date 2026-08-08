"""
Agent Metrics Tracker for Enterprise Multi-Agent Collaboration Framework.

Tracks active agents, latency profiles, collaboration time, debate rounds,
voting accuracy, retries, synthesis latency, and agent success rates.
"""

import threading
import time
from typing import Dict, Any, List


class AgentMetricsTracker:
    """Thread-safe metrics tracker for multi-agent execution."""

    def __init__(self):
        self._lock = threading.Lock()
        self.total_collaborations: int = 0
        self.successful_collaborations: int = 0
        self.failed_collaborations: int = 0
        self.total_debate_rounds: int = 0
        self.total_votes_conducted: int = 0
        self.agent_execution_counts: Dict[str, int] = {}
        self.agent_latencies_ms: Dict[str, List[float]] = {}

    def record_agent_execution(self, agent_name: str, latency_ms: float, success: bool = True) -> None:
        """Records an execution metric for an individual agent."""
        with self._lock:
            self.agent_execution_counts[agent_name] = self.agent_execution_counts.get(agent_name, 0) + 1
            if agent_name not in self.agent_latencies_ms:
                self.agent_latencies_ms[agent_name] = []
            self.agent_latencies_ms[agent_name].append(latency_ms)
            if len(self.agent_latencies_ms[agent_name]) > 500:
                self.agent_latencies_ms[agent_name] = self.agent_latencies_ms[agent_name][-500:]

    def record_collaboration(
        self,
        success: bool = True,
        debate_rounds: int = 0,
        votes_conducted: int = 0,
    ) -> None:
        """Records a completed multi-agent collaboration workflow."""
        with self._lock:
            self.total_collaborations += 1
            if success:
                self.successful_collaborations += 1
            else:
                self.failed_collaborations += 1
            self.total_debate_rounds += debate_rounds
            self.total_votes_conducted += votes_conducted

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary statistics across multi-agent executions."""
        with self._lock:
            success_rate = (
                round(self.successful_collaborations / self.total_collaborations, 4)
                if self.total_collaborations > 0
                else 1.0
            )

            avg_agent_latencies = {
                agent: round(sum(latencies) / len(latencies), 2)
                for agent, latencies in self.agent_latencies_ms.items()
                if latencies
            }

            return {
                "total_collaborations": self.total_collaborations,
                "successful_collaborations": self.successful_collaborations,
                "failed_collaborations": self.failed_collaborations,
                "success_rate": success_rate,
                "total_debate_rounds": self.total_debate_rounds,
                "total_votes_conducted": self.total_votes_conducted,
                "agent_execution_counts": dict(self.agent_execution_counts),
                "avg_agent_latencies_ms": avg_agent_latencies,
            }


# Global AgentMetricsTracker instance
agent_metrics_tracker = AgentMetricsTracker()
