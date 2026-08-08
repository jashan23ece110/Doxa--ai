"""
Enterprise Awareness Campaign Manager.

Manages awareness campaign lifecycles, scheduling, departmental targeting,
user groups, templates, versioning, progress tracking, and campaign analytics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AwarenessCampaign(BaseModel):
    campaign_id: str = Field(default_factory=lambda: f"camp_{uuid.uuid4().hex[:8]}")
    name: str
    target_department: str = "All"
    status: str = "active"  # draft, scheduled, active, completed, archived
    version: str = "1.0.0"
    participants_count: int = 0
    completion_rate_percent: float = 0.0
    start_time: float = Field(default_factory=time.time)
    end_time: float = Field(default_factory=lambda: time.time() + 2592000.0)  # 30 days default


class CampaignManager:
    """Enterprise Security Awareness Campaign Manager."""

    def __init__(self):
        self._campaigns: Dict[str, AwarenessCampaign] = {}

    def create_campaign(self, name: str, target_department: str = "All") -> AwarenessCampaign:
        """Creates and registers a new security awareness campaign."""
        camp = AwarenessCampaign(name=name, target_department=target_department)
        self._campaigns[camp.campaign_id] = camp
        security_logger.info(f"CampaignManager: Created campaign '{name}' ({camp.campaign_id}) for department '{target_department}'.")
        return camp

    def update_progress(self, campaign_id: str, completion_rate: float) -> Optional[AwarenessCampaign]:
        """Updates campaign completion progress percentage."""
        camp = self._campaigns.get(campaign_id)
        if camp:
            camp.completion_rate_percent = min(100.0, max(0.0, completion_rate))
            if camp.completion_rate_percent >= 100.0:
                camp.status = "completed"
            security_logger.info(f"CampaignManager: Updated campaign '{campaign_id}' progress to {camp.completion_rate_percent}%.")
        return camp

    def get_campaign(self, campaign_id: str) -> Optional[AwarenessCampaign]:
        """Retrieves campaign details."""
        return self._campaigns.get(campaign_id)


# Global CampaignManager instance
campaign_manager = CampaignManager()
