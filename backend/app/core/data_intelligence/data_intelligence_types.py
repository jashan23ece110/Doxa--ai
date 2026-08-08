"""
Enterprise Data Intelligence Types & Data Models.

Defines Pydantic models for Data Sources, Data Connectors, Records, Batches, Streams,
Pipelines, Catalogs, Quality Metrics, Lineage, Classifications, Fusion Results, and Reports.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class DataClassificationLevel(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class DataSourceType(str, Enum):
    DATABASE = "database"
    FILE = "file"
    API = "api"
    STREAM = "stream"
    MESSAGE_QUEUE = "message_queue"
    CLOUD_STORAGE = "cloud_storage"


class DataSource(BaseModel):
    source_id: str = Field(default_factory=lambda: f"src_{uuid.uuid4().hex[:8]}")
    name: str
    source_type: DataSourceType
    connection_uri: str
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: float = Field(default_factory=time.time)


class DataConnector(BaseModel):
    connector_id: str = Field(default_factory=lambda: f"conn_{uuid.uuid4().hex[:8]}")
    name: str
    connector_type: DataSourceType
    version: str = "1.0.0"
    is_registered: bool = True
    capabilities: List[str] = Field(default_factory=list)


class DataRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:8]}")
    source_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    classification: DataClassificationLevel = DataClassificationLevel.INTERNAL
    ingested_at: float = Field(default_factory=time.time)


class DataBatch(BaseModel):
    batch_id: str = Field(default_factory=lambda: f"batch_{uuid.uuid4().hex[:8]}")
    source_id: str
    records: List[DataRecord] = Field(default_factory=list)
    batch_size: int = 0
    created_at: float = Field(default_factory=time.time)


class DataStream(BaseModel):
    stream_id: str = Field(default_factory=lambda: f"strm_{uuid.uuid4().hex[:8]}")
    name: str
    active_subscribers_count: int = 0
    throughput_records_per_sec: float = 0.0


class DataPipeline(BaseModel):
    pipeline_id: str = Field(default_factory=lambda: f"pipe_{uuid.uuid4().hex[:8]}")
    name: str
    stages: List[str] = Field(default_factory=lambda: [
        "Ingestion", "Validation", "Normalization", "Classification",
        "Fusion", "KnowledgeGraph", "Memory", "Analytics", "Evaluation"
    ])
    status: str = "IDLE"  # IDLE, RUNNING, COMPLETED, FAILED
    last_run_at: Optional[float] = None


class DataSchema(BaseModel):
    schema_id: str = Field(default_factory=lambda: f"sch_{uuid.uuid4().hex[:8]}")
    name: str
    fields: Dict[str, str] = Field(default_factory=dict)  # field_name -> data_type


class DataCatalog(BaseModel):
    catalog_id: str = Field(default_factory=lambda: f"cat_{uuid.uuid4().hex[:8]}")
    dataset_name: str
    schemas: List[DataSchema] = Field(default_factory=list)
    record_count: int = 0


class DataQualityMetrics(BaseModel):
    validity_percent: float = 99.5
    completeness_percent: float = 98.8
    uniqueness_percent: float = 100.0
    consistency_score: float = 0.99


class DataLineage(BaseModel):
    lineage_id: str = Field(default_factory=lambda: f"lin_{uuid.uuid4().hex[:8]}")
    source_ids: List[str] = Field(default_factory=list)
    transformation_steps: List[str] = Field(default_factory=list)
    destination_id: str


class DataClassification(BaseModel):
    target_id: str
    classification_level: DataClassificationLevel = DataClassificationLevel.INTERNAL
    contains_pii: bool = False
    confidence_score: float = 0.98


class DataFusionResult(BaseModel):
    fusion_id: str = Field(default_factory=lambda: f"fused_{uuid.uuid4().hex[:8]}")
    source_record_ids: List[str] = Field(default_factory=list)
    unified_payload: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = 0.96
    fused_at: float = Field(default_factory=time.time)


class DistributedTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"dtask_{uuid.uuid4().hex[:8]}")
    name: str
    assigned_worker_id: str = "worker_01"
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED


class AnalyticsJob(BaseModel):
    job_id: str = Field(default_factory=lambda: f"ajob_{uuid.uuid4().hex[:8]}")
    query: str
    target_dataset: str
    execution_time_ms: float = 0.0
    results_count: int = 0


class IntelligenceDataset(BaseModel):
    dataset_id: str = Field(default_factory=lambda: f"ds_{uuid.uuid4().hex[:8]}")
    name: str
    records_count: int = 0
    size_bytes: int = 0
    classification: DataClassificationLevel = DataClassificationLevel.INTERNAL
    created_at: float = Field(default_factory=time.time)


class DataIntelligenceReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"direp_{uuid.uuid4().hex[:8]}")
    title: str
    summary_findings: List[str] = Field(default_factory=list)
    quality_metrics: DataQualityMetrics = Field(default_factory=DataQualityMetrics)
    generated_at: float = Field(default_factory=time.time)


class PlatformMetrics(BaseModel):
    active_pipelines_count: int = 0
    ingestion_throughput_mb_s: float = 0.0
    average_processing_latency_ms: float = 0.0
    connector_health_percent: float = 100.0


class DataDashboardState(BaseModel):
    active_datasets_count: int = 0
    total_records_ingested: int = 0
    active_pipelines_count: int = 0
    quality_score_avg: float = 99.2
    updated_at: float = Field(default_factory=time.time)
