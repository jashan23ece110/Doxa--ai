"""
Human Intelligence Domain Events.

Defines domain event types and async publication methods for human security intelligence.
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import time
from app.core.logging import security_logger


class HumanEventType(str, Enum):
    PROFILE_CREATED = "profile_created"
    PROFILE_UPDATED = "profile_updated"
    BEHAVIOR_ANALYZED = "behavior_analyzed"
    RISK_SCORE_UPDATED = "risk_score_updated"
    TRAINING_COMPLETED = "training_completed"
    ASSESSMENT_FINISHED = "assessment_finished"
    INSIDER_RISK_DETECTED = "insider_risk_detected"
    REPORT_GENERATED = "report_generated"


class HumanEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"hevt_{int(time.time() * 1000)}")
    event_type: HumanEventType
    actor_id: str = "system"
    target_id: str
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


async def publish_human_event(event_type: HumanEventType, target_id: str, data: Optional[Dict[str, Any]] = None, actor_id: str = "system") -> HumanEvent:
    """
    Publishes a human intelligence domain event.

    Args:
        event_type: Enum event type.
        target_id: Employee or Department ID.
        data: Additional payload dictionary.
        actor_id: Triggering entity string.

    Returns:
        HumanEvent object.
    """
    evt = HumanEvent(
        event_type=event_type,
        actor_id=actor_id,
        target_id=target_id,
        data=data or {},
    )
    security_logger.debug(f"HumanEvents: Published event '{evt.event_type.value}' for target '{target_id}'.")
    return evt
