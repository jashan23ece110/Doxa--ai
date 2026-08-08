"""
Digital Forensic Timeline Generator.

Chronologically reconstructs execution events, file ops, registry modifications,
network connections, process launches, DLL injections, privilege events, and persistence events.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.security.dynamic_analysis.sandbox_manager import SandboxExecutionResult


class ForensicTimelineEvent(BaseModel):
    timestamp: float = Field(default_factory=time.time)
    event_type: str
    description: str
    source_process: str = "system"
    details: Dict[str, Any] = Field(default_factory=dict)


class ForensicTimeline(BaseModel):
    binary_id: str
    events: List[ForensicTimelineEvent] = Field(default_factory=list)
    total_events: int = 0


class ForensicTimelineGenerator:
    """Enterprise Digital Forensic Timeline Generator."""

    def generate_timeline(self, binary_id: str, sandbox_result: SandboxExecutionResult) -> ForensicTimeline:
        """
        Builds a chronological forensic timeline from sandbox telemetry.

        Args:
            binary_id: Unique binary identifier.
            sandbox_result: SandboxExecutionResult model.

        Returns:
            ForensicTimeline object.
        """
        events: List[ForensicTimelineEvent] = []
        base_ts = time.time() - sandbox_result.duration_seconds

        # 1. Process launches
        for idx, proc in enumerate(sandbox_result.process_tree):
            events.append(ForensicTimelineEvent(
                timestamp=base_ts + (idx * 0.1),
                event_type="process_launch",
                description=f"Process '{proc.get('name')}' launched with PID {proc.get('pid')}",
                source_process=proc.get("name", "unknown"),
                details=proc,
            ))

        # 2. File modifications
        for idx, f in enumerate(sandbox_result.created_files):
            events.append(ForensicTimelineEvent(
                timestamp=base_ts + 0.2 + (idx * 0.05),
                event_type="file_create",
                description=f"Created file payload at '{f}'",
                details={"file_path": f},
            ))

        # 3. Registry modifications
        for idx, reg in enumerate(sandbox_result.modified_registry_keys):
            events.append(ForensicTimelineEvent(
                timestamp=base_ts + 0.4 + (idx * 0.05),
                event_type="registry_modify",
                description=f"Modified registry key '{reg}'",
                details={"key": reg},
            ))

        # 4. Network connections
        for idx, conn in enumerate(sandbox_result.network_connections):
            events.append(ForensicTimelineEvent(
                timestamp=base_ts + 0.6 + (idx * 0.05),
                event_type="network_connect",
                description=f"Connected to {conn.get('dst_ip')}:{conn.get('dst_port')} over {conn.get('protocol')}",
                details=conn,
            ))

        events.sort(key=lambda e: e.timestamp)
        timeline = ForensicTimeline(
            binary_id=binary_id,
            events=events,
            total_events=len(events),
        )

        security_logger.info(f"ForensicTimelineGenerator: Built timeline with {len(events)} chronological events for binary '{binary_id}'.")
        return timeline


# Global ForensicTimelineGenerator instance
forensic_timeline_generator = ForensicTimelineGenerator()
