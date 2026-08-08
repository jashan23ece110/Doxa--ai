"""
Data Intelligence Domain Events.

Defines domain event types and async publication handlers for data ingestion,
pipeline execution, classification, and data fusion.
"""

import time
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class DataEventType(str, Enum):
    DATA_INGESTED = "data_ingested"
    PIPELINE_STARTED = "pipeline_started"
    PIPELINE_COMPLETED = "pipeline_completed"
    DATA_CLASSIFIED = "data_classified"
    DATA_FUSED = "data_fused"
    DATA_VALIDATED = "data_validated"
    DATASET_REGISTERED = "dataset_registered"
    REPORT_GENERATED = "report_generated"


class DataEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"devt_{int(time.time() * 1000)}")
    event_type: DataEventType
    source_id: str
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


async def publish_data_event(event_type: DataEventType, source_id: str, data: Optional[Dict[str, Any]] = None) -> DataEvent:
    """
    Publishes a data intelligence domain event.

    Args:
        event_type: DataEventType enum value.
        source_id: Source identifier.
        data: Optional payload dictionary.

    Returns:
        DataEvent object.
    """
    evt = DataEvent(
        event_type=event_type,
        source_id=source_id,
        data=data or {},
    )
    security_logger.debug(f"DataEvents: Published data event '{evt.event_type.value}' for source '{source_id}'.")
    return evt
