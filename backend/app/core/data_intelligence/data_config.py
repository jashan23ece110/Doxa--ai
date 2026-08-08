"""
Enterprise Data Intelligence Configuration.

Defines configurable settings for data ingestion timeouts, pipeline processing limits,
cache TTLs, worker counts, and retention policies.
"""

from pydantic import BaseModel, Field


class DataIntelligenceConfig(BaseModel):
    ingestion_timeout_seconds: float = 30.0
    pipeline_timeout_seconds: float = 300.0
    cache_ttl_seconds: float = 600.0
    max_analytics_workers: int = 16
    dataset_retention_days: int = 90
    connector_directory: str = "app/core/data_intelligence/connectors"
    analytics_retention_days: int = 30
    report_retention_days: int = 365
    enable_auto_classification: bool = True
    enable_data_fusion: bool = True


# Global DataIntelligenceConfig instance
data_config = DataIntelligenceConfig()
