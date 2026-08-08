"""
Enterprise Event Stream Manager.

Manages event stream lifecycles, topics, partition assignments, consumer groups,
producer registrations, offset tracking, and real-time stream health.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class StreamTopic(BaseModel):
    topic_name: str
    partitions_count: int = 4
    consumer_groups: List[str] = Field(default_factory=list)
    total_messages_count: int = 0
    created_at: float = Field(default_factory=time.time)


class EventStreamManager:
    """Thread-safe Enterprise Event Stream Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._topics: Dict[str, StreamTopic] = {}

    def register_topic(self, topic_name: str, partitions: int = 4) -> StreamTopic:
        """Registers a new event stream topic."""
        topic = StreamTopic(topic_name=topic_name, partitions_count=partitions)
        with self._lock:
            self._topics[topic_name] = topic
            security_logger.info(f"EventStreamManager: Registered stream topic '{topic_name}' ({partitions} partitions).")
        return topic

    def get_topic(self, topic_name: str) -> Optional[StreamTopic]:
        """Retrieves topic details by name."""
        with self._lock:
            return self._topics.get(topic_name)

    def record_message(self, topic_name: str):
        """Increments message counter for topic."""
        with self._lock:
            topic = self._topics.get(topic_name)
            if topic:
                topic.total_messages_count += 1


# Global EventStreamManager instance
event_stream_manager = EventStreamManager()
