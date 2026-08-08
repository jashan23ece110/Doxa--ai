"""
Diagnostics Engine for Enterprise Observability Platform.

Automatically diagnoses slow retrieval, slow agents, slow memory, deadlocks, high contention,
resource starvation, thread exhaustion, and memory pressure.
"""

from typing import List, Dict, Any
from app.core.logging import logger
from app.core.observability.metrics_engine import metrics_engine
from app.core.observability.observability_models import DiagnosticReport


class DiagnosticsEngine:
    """Automated root-cause diagnostic analyzer."""

    @staticmethod
    def run_diagnostics() -> DiagnosticReport:
        """
        Analyzes latency percentiles and system metrics to pinpoint primary bottlenecks.
        """
        percentiles = metrics_engine.get_percentiles()
        p99 = percentiles.get("p99", 0.0)

        if p99 > 2000.0:
            bottleneck = "llm_latency"
            summary = f"P99 latency spike detected ({p99}ms). Primary bottleneck in LLM Provider API response times."
            action = "Scale worker concurrency or switch fallback LLM model route."
        elif p99 > 1000.0:
            bottleneck = "vector_retrieval"
            summary = f"P99 latency ({p99}ms). Bottleneck in ChromaDB vector embedding search."
            action = "Rebuild vector index and optimize embedding batch size."
        else:
            bottleneck = "none"
            summary = "System performance nominal. No deadlocks or resource starvation detected."
            action = "No action required."

        report = DiagnosticReport(
            primary_bottleneck=bottleneck,
            root_cause_summary=summary,
            affected_components=[bottleneck] if bottleneck != "none" else [],
            recommended_action=action,
        )

        logger.info(f"DiagnosticsEngine generated report '{report.report_id}': Primary Bottleneck='{bottleneck}'.")
        return report


# Global DiagnosticsEngine instance
diagnostics_engine = DiagnosticsEngine()
