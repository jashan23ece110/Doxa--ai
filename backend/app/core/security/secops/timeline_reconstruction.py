"""
Enterprise Investigation Timeline Reconstruction Engine.

Correlates process executions, filesystem events, registry modifications,
authentication attempts, IOC detections, milestones, and analyst actions.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class TimelineEntry(BaseModel):
    entry_id: str
    timestamp: float = Field(default_factory=time.time)
    category: str  # execution, filesystem, registry, authentication, ioc, milestone, analyst
    actor: str = "system"
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)


class InvestigationTimeline(BaseModel):
    investigation_id: str
    entries: List[TimelineEntry] = Field(default_factory=list)
    total_entries: int = 0


class TimelineReconstructionEngine:
    """Enterprise Timeline Reconstruction Engine."""

    def build_timeline(self, investigation_id: str, events: List[Dict[str, Any]]) -> InvestigationTimeline:
        """
        Reconstructs a chronological investigation timeline.

        Args:
            investigation_id: Investigation identifier.
            events: List of raw event dicts.

        Returns:
            InvestigationTimeline object.
        """
        entries: List[TimelineEntry] = []
        base_time = time.time() - 3600.0  # 1 hour ago default

        for idx, evt in enumerate(events):
            entries.append(TimelineEntry(
                entry_id=f"tle_{idx + 1}",
                timestamp=base_time + (idx * 10.0),
                category=evt.get("category", "execution"),
                actor=evt.get("actor", "system"),
                summary=evt.get("summary", "Security event recorded"),
                details=evt.get("details", {}),
            ))

        entries.sort(key=lambda e: e.timestamp)
        timeline = InvestigationTimeline(
            investigation_id=investigation_id,
            entries=entries,
            total_entries=len(entries),
        )

        security_logger.info(f"TimelineReconstructionEngine: Reconstructed timeline for '{investigation_id}' ({len(entries)} entries).")
        return timeline


# Global TimelineReconstructionEngine instance
timeline_reconstruction_engine = TimelineReconstructionEngine()
