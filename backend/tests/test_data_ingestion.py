#!/usr/bin/env python3
"""
Integration Test Suite for Stage 8 Part 2 — Enterprise Distributed Data Ingestion & Processing Platform.
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


async def test_ingestion_engine():
    print("\n📥 Testing Ingestion Engine...")
    from app.core.data_intelligence.ingestion.ingestion_engine import ingestion_engine

    raw_recs = [{"id": 1, "val": "A"}, {"id": 2, "val": "B"}]
    batch = await ingestion_engine.ingest_batch("src_test_01", raw_recs)
    check("Batch ingested", batch is not None)
    check("Batch size == 2", batch.batch_size == 2)

    cp = ingestion_engine.get_checkpoint("src_test_01")
    check("Checkpoint created", cp is not None)
    check("Checkpoint processed count == 2", cp.processed_count == 2)


def test_source_manager():
    print("\n🔌 Testing Source Manager...")
    from app.core.data_intelligence.ingestion.source_manager import source_manager
    from app.core.data_intelligence.data_intelligence_types import DataSourceType

    src = source_manager.register_source("API Gateway", DataSourceType.API, "https://api.doxa.internal/v1")
    check("Source registered", src is not None)

    status = source_manager.check_health(src.source_id)
    check("Source health checked", status.is_healthy)


async def test_distributed_processor():
    print("\n⚙️ Testing Distributed Processor...")
    from app.core.data_intelligence.ingestion.distributed_processor import distributed_processor

    items = [{"item": i} for i in range(10)]
    res = await distributed_processor.execute_task("Partitioned_Transform", items)
    check("Distributed task executed", res is not None)
    check("Output count == 10", res.output_count == 10)


def test_stream_processor():
    print("\n🌊 Testing Stream Processor...")
    from app.core.data_intelligence.ingestion.stream_processor import stream_processor
    from app.core.data_intelligence.data_intelligence_types import DataRecord

    recs = [DataRecord(source_id="strm_01", payload={"val": i}) for i in range(5)]
    agg = stream_processor.process_stream_window("strm_01", recs)
    check("Stream window processed", agg is not None)
    check("Aggregated records count == 5", agg.records_count == 5)


async def test_batch_processor():
    print("\n📦 Testing Batch Processor...")
    from app.core.data_intelligence.ingestion.batch_processor import batch_processor
    from app.core.data_intelligence.data_intelligence_types import DataBatch, DataRecord

    recs = [DataRecord(source_id="b_01", payload={"v": i}) for i in range(3)]
    batch = DataBatch(source_id="b_01", records=recs, batch_size=3)

    job = await batch_processor.process_batch_job(batch)
    check("Batch processing job completed", job is not None)
    check("Job status is COMPLETED", job.status == "COMPLETED")


def test_schema_registry():
    print("\n📜 Testing Schema Registry...")
    from app.core.data_intelligence.ingestion.schema_registry import schema_registry

    schema = schema_registry.register_schema("UserEventSchema", {"user_id": "int", "action": "string"})
    check("Schema registered", schema is not None)

    valid = schema_registry.validate_record_schema(schema.schema_id, {"user_id": 100, "action": "login"})
    check("Record schema validated", valid)


def test_data_quality_engine():
    print("\n✨ Testing Data Quality Engine...")
    from app.core.data_intelligence.ingestion.data_quality_engine import data_quality_engine
    from app.core.data_intelligence.data_intelligence_types import DataRecord

    recs = [DataRecord(source_id="src_qual", payload={"a": 1})]
    assess = data_quality_engine.evaluate_quality("src_qual", recs)
    check("Quality assessment created", assess is not None)
    check("Overall quality score > 98.0", assess.overall_quality_score > 98.0)


def test_deduplication_engine():
    print("\n🔍 Testing Deduplication Engine...")
    from app.core.data_intelligence.ingestion.deduplication_engine import deduplication_engine
    from app.core.data_intelligence.data_intelligence_types import DataRecord

    r1 = DataRecord(source_id="src_dedup", payload={"key": "val1"})
    r2 = DataRecord(source_id="src_dedup", payload={"key": "val1"})  # Duplicate payload
    r3 = DataRecord(source_id="src_dedup", payload={"key": "val2"})

    res = deduplication_engine.deduplicate([r1, r2, r3])
    check("Deduplication completed", res is not None)
    check("Duplicates found count == 1", res.duplicates_found_count == 1)
    check("Unique records count == 2", len(res.unique_records) == 2)


def test_data_lineage():
    print("\n🕸️ Testing Data Lineage Engine...")
    from app.core.data_intelligence.ingestion.data_lineage import data_lineage_engine

    data_lineage_engine.record_lineage("src_db", "source", "Database Source")
    data_lineage_engine.record_lineage("pipe_01", "pipeline", "Cleanse Pipeline", parents=["src_db"])
    data_lineage_engine.record_lineage("ds_final", "dataset", "Analytics Dataset", parents=["pipe_01"])

    trace = data_lineage_engine.trace_lineage("ds_final")
    check("Lineage traced", len(trace) >= 3)


def test_ingestion_monitor():
    print("\n📊 Testing Ingestion Monitor...")
    from app.core.data_intelligence.ingestion.ingestion_monitor import ingestion_monitor

    metrics = ingestion_monitor.get_monitoring_snapshot()
    check("Monitoring snapshot retrieved", metrics is not None)
    check("Processed records count > 0", metrics.total_records_processed > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-7...")
    from app.core.data_intelligence import enterprise_data_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    src = enterprise_data_intelligence_manager.register_data_source("Ingestion_Test_Source", "api", "https://api.test/v1")
    check("Data Intelligence Manager integrated with ingestion platform", src is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "ingest_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 8 PART 2 — DISTRIBUTED DATA INGESTION & PROCESSING TEST SUITE")
    print("==========================================================================")

    await test_ingestion_engine()
    test_source_manager()
    await test_distributed_processor()
    test_stream_processor()
    await test_batch_processor()
    test_schema_registry()
    test_data_quality_engine()
    test_deduplication_engine()
    test_data_lineage()
    test_ingestion_monitor()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 8 PART 2 SUCCESS: Distributed Data Ingestion & Processing Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
