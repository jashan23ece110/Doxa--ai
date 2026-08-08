"""
Human Intelligence Platform Configuration.

Defines configuration options for assessment timeouts, analysis limits, cache TTLs,
worker concurrency, and retention policies.
"""

from pydantic import BaseModel, Field


class HumanIntelligenceConfig(BaseModel):
    assessment_timeout_seconds: float = 30.0
    analysis_timeout_seconds: float = 60.0
    cache_ttl_seconds: float = 600.0
    worker_count: int = 8
    profile_retention_days: int = 365
    training_retention_days: int = 730
    analytics_retention_days: int = 365
    plugin_directory: str = "app/plugins/human_intelligence"
    report_retention_days: int = 180


# Global HumanIntelligenceConfig instance
human_config = HumanIntelligenceConfig()
