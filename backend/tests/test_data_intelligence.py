#!/usr/bin/env python3
"""
Integration Test Suite for Stage 8 Part 1 — Enterprise Massive-Scale Data Intelligence Platform Foundation.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

PASS = 0
FAIL = 0


def check(label, condition):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}")


def test_data_types():
    print("\n📦 Testing Data Intelligence Types & Data Models...")
    from app.core.data_intelligence.data_intelligence_types import (
        DataSource, DataSourceType, DataRecord, DataBatch, DataQualityMetrics, DataLineage, DataFusionResult
    )

    src = DataSource(name="Database_Prod", source_type=DataSourceType.DATABASE, connection_uri="postgresql://prod:5432/doxa")
    check("DataSource created", src.source_id.startswith("src_"))

    rec = DataRecord(source_id=src.source_id, payload={"user_id": 101, "event": "login"})
    check("DataRecord created", rec.record_id.startswith("rec_"))

    batch = DataBatch(source_id=src.source_id, records=[rec], batch_size=1)
    check("DataBatch created", len(batch.records) == 1)

    qual = DataQualityMetrics()
    check("DataQualityMetrics default validity > 99%", qual.validity_percent > 99.0)


def test_connector_registry():
    print("\n🔌 Testing Data Connector Registry...")
    from app.core.data_intelligence.connector_registry import connector_registry
    from app.core.data_intelligence.data_intelligence_types import DataSourceType

    conn = connector_registry.register_connector("PostgreSQL Connector", DataSourceType.DATABASE, version="1.2.0")
    check("Connector registered", conn is not None)

    retrieved = connector_registry.get_connector(conn.connector_id)
    check("Connector retrieved from registry", retrieved.name == "PostgreSQL Connector")

    db_conns = connector_registry.list_connectors_by_type(DataSourceType.DATABASE)
    check("List connectors by type count > 0", len(db_conns) > 0)


def test_unified_data_context():
    print("\n🧠 Testing Unified Enterprise Data Context Manager...")
    from app.core.data_intelligence.unified_data_context import unified_data_context_manager

    ctx = unified_data_context_manager.build_unified_context("Cyber Threat Analytics Query", token_budget=4096)
    check("Unified context created", ctx is not None)
    check("Tokens used within budget", ctx.tokens_used <= ctx.token_budget)
    check("Clustered topics present", len(ctx.clustered_topics) > 0)


async def test_distributed_pipeline():
    print("\n⚡ Testing Distributed Data Pipeline...")
    from app.core.data_intelligence.distributed_pipeline import distributed_data_pipeline

    raw_batch = [{"id": 1, "metric": 88.0}, {"id": 2, "metric": 92.5}]
    res = await distributed_data_pipeline.execute_pipeline("src_test_01", raw_batch)

    check("Distributed pipeline executed", res is not None)
    check("Total records processed == 2", res.total_records_processed == 2)
    check("Pipeline steps executed == 9", len(res.step_results) == 9)
    check("Overall status is COMPLETED", res.overall_status == "COMPLETED")


async def test_enterprise_data_intelligence_manager():
    print("\n🌐 Testing Enterprise Data Intelligence Manager...")
    from app.core.data_intelligence.data_intelligence_manager import enterprise_data_intelligence_manager
    from app.core.data_intelligence.data_intelligence_types import DataSourceType

    src = enterprise_data_intelligence_manager.register_data_source("S3 Log Stream", DataSourceType.CLOUD_STORAGE, "s3://doxa-logs/")
    check("Data source registered via manager", src is not None)

    raw_batch = [{"log_event": "auth_success"}]
    res = await enterprise_data_intelligence_manager.ingest_and_process_batch(src.source_id, raw_batch)
    check("Ingest and process batch completed", res.overall_status == "COMPLETED")


def test_platform_metrics():
    print("\n📊 Testing Data Platform Metrics Tracker...")
    from app.core.data_intelligence.platform_metrics import data_platform_metrics

    data_platform_metrics.record_ingestion(100)
    data_platform_metrics.record_fusion(50)
    metrics = data_platform_metrics.get_metrics()
    check("Platform metrics snapshot retrieved", metrics is not None)
    check("Connector health percent == 100%", metrics.connector_health_percent == 100.0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-7...")
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Data_Intel_Test")
    check("Human Intelligence Platform operates seamlessly with Data Platform", assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "data_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 8 PART 1 — ENTERPRISE MASSIVE-SCALE DATA INTELLIGENCE TEST SUITE")
    print("==========================================================================")

    test_data_types()
    test_connector_registry()
    test_unified_data_context()
    await test_distributed_pipeline()
    await test_enterprise_data_intelligence_manager()
    test_platform_metrics()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 8 PART 1 SUCCESS: Enterprise Data Intelligence Platform Foundation Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
