"""
Enterprise Data Intelligence Manager.

Central orchestrator for data ingestion scheduling, connector lifecycles, async pipeline execution,
analytics job coordination, module registration, event dispatching, health monitoring, and metrics collection.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.data_intelligence.data_intelligence_types import DataSource, DataSourceType, DataBatch, DataRecord, IntelligenceDataset
from app.core.data_intelligence.connector_registry import connector_registry
from app.core.data_intelligence.distributed_pipeline import distributed_data_pipeline, DistributedDataPipelineResult
from app.core.data_intelligence.platform_metrics import data_platform_metrics
from app.core.data_intelligence.data_events import publish_data_event, DataEventType


class EnterpriseDataIntelligenceManager:
    """Master Orchestrator for Enterprise Data Intelligence Subsystem."""

    def __init__(self):
        self._sources: Dict[str, DataSource] = {}
        self._datasets: Dict[str, IntelligenceDataset] = {}

    def register_data_source(self, name: str, source_type: DataSourceType, connection_uri: str) -> DataSource:
        """Registers a new data source in the platform."""
        source = DataSource(name=name, source_type=source_type, connection_uri=connection_uri)
        self._sources[source.source_id] = source
        security_logger.info(f"EnterpriseDataIntelligenceManager: Registered data source '{name}' ({source.source_id}).")
        return source

    async def ingest_and_process_batch(self, source_id: str, raw_records: List[Dict[str, Any]]) -> DistributedDataPipelineResult:
        """
        Ingests a batch of records and executes the distributed data processing pipeline.

        Args:
            source_id: Source ID.
            raw_records: Raw data payload dicts.

        Returns:
            DistributedDataPipelineResult model.
        """
        await publish_data_event(DataEventType.DATA_INGESTED, source_id, {"records_count": len(raw_records)})
        data_platform_metrics.record_ingestion(len(raw_records))

        pipeline_result = await distributed_data_pipeline.execute_pipeline(source_id, raw_records)
        return pipeline_result


# Global EnterpriseDataIntelligenceManager instance
enterprise_data_intelligence_manager = EnterpriseDataIntelligenceManager()
