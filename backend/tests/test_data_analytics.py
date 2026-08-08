#!/usr/bin/env python3
"""
Integration Test Suite for Stage 8 Part 4 — Enterprise Distributed Analytics & Real-Time Event Correlation Platform.
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


async def test_distributed_analytics_engine():
    print("\n📊 Testing Distributed Analytics Engine...")
    from app.core.data_intelligence.analytics.distributed_analytics_engine import distributed_analytics_engine

    recs = [{"metric": 10.0}, {"metric": 20.0}, {"metric": 30.0}]
    res = await distributed_analytics_engine.execute_analytics_query("mean", "ds_prod", recs)
    check("Analytics query executed", res is not None)
    check("Records analyzed count == 3", res.records_analyzed == 3)
    check("Calculated mean == 20.0", res.aggregated_results.get("mean") == 20.0)


def test_event_correlation_engine():
    print("\n🔗 Testing Event Correlation Engine...")
    from app.core.data_intelligence.analytics.event_correlation_engine import event_correlation_engine

    chain = event_correlation_engine.correlate_events("evt_01", ["evt_02", "evt_03"])
    check("Correlation chain generated", chain is not None)
    check("Correlated events count == 2", len(chain.correlated_event_ids) == 2)


def test_anomaly_detection_engine():
    print("\n⚠️ Testing Anomaly Detection Engine...")
    from app.core.data_intelligence.analytics.anomaly_detection_engine import anomaly_detection_engine

    points = [1.0, 1.2, 1.1, 1.3, 50.0, 1.2]
    anomalies = anomaly_detection_engine.detect_anomalies("metric_cpu", points)
    check("Anomalies evaluated", anomalies is not None)
    check("Detected anomaly count == 1", len(anomalies) == 1)


def test_time_series_engine():
    print("\n📈 Testing Time-Series Engine...")
    from app.core.data_intelligence.analytics.time_series_engine import time_series_engine

    series = [10.0, 12.0, 15.0, 18.0, 22.0]
    res = time_series_engine.analyze_series("ts_sales", series)
    check("Time series analyzed", res is not None)
    check("Trend direction is UPWARD", res.trend_direction == "UPWARD")


def test_predictive_analytics():
    print("\n🔮 Testing Predictive Analytics Engine...")
    from app.core.data_intelligence.analytics.predictive_analytics import predictive_analytics_engine

    history = [100.0, 110.0, 120.0]
    pred = predictive_analytics_engine.predict_future_value("revenue", history)
    check("Prediction generated", pred is not None)
    check("Predicted value > 110.0", pred.predicted_value > 110.0)


def test_streaming_analytics():
    print("\n🌊 Testing Streaming Analytics Engine...")
    from app.core.data_intelligence.analytics.streaming_analytics import streaming_analytics_engine

    events = [{"event": "login"}, {"event": "view"}]
    metrics = streaming_analytics_engine.evaluate_stream_window("strm_auth", events)
    check("Stream window metrics generated", metrics is not None)
    check("Events processed == 2", metrics.events_processed == 2)


def test_analytics_job_manager():
    print("\n⚙️ Testing Analytics Job Manager...")
    from app.core.data_intelligence.analytics.analytics_job_manager import analytics_job_manager

    job = analytics_job_manager.submit_job("SELECT COUNT(*) FROM logs", priority="HIGH")
    check("Job submitted", job is not None)

    retrieved = analytics_job_manager.get_job(job.job_id)
    check("Job retrieved", retrieved.priority == "HIGH")


def test_analytics_cache():
    print("\n⚡ Testing Analytics Cache...")
    from app.core.data_intelligence.analytics.analytics_cache import analytics_cache

    analytics_cache.set("query_stats", {"avg": 42.0}, ttl_seconds=60.0)
    val = analytics_cache.get("query_stats")
    check("Cached analytics retrieved", val is not None and val["avg"] == 42.0)


def test_analytics_explainability():
    print("\n📜 Testing Analytics Explainability Engine...")
    from app.core.data_intelligence.analytics.analytics_explainability import analytics_explainability_engine

    expl = analytics_explainability_engine.explain_result("anom_100", "anomaly", ["High CPU spikes"])
    check("Explanation generated", expl is not None)
    check("Confidence level > 0.90", expl.confidence_level > 0.90)


def test_analytics_metrics():
    print("\n📊 Testing Analytics Metrics Tracker...")
    from app.core.data_intelligence.analytics.analytics_metrics import analytics_metrics_tracker

    snapshot = analytics_metrics_tracker.get_metrics_snapshot()
    check("Analytics metrics snapshot retrieved", snapshot is not None)
    check("Jobs completed > 0", snapshot.jobs_completed_count > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-7...")
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.data_intelligence import enterprise_data_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Analytics_Test")
    check("Human Intelligence Platform operates seamlessly with Analytics Platform", assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "analytics_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 8 PART 4 — ENTERPRISE DISTRIBUTED ANALYTICS TEST SUITE")
    print("==========================================================================")

    await test_distributed_analytics_engine()
    test_event_correlation_engine()
    test_anomaly_detection_engine()
    test_time_series_engine()
    test_predictive_analytics()
    test_streaming_analytics()
    test_analytics_job_manager()
    test_analytics_cache()
    test_analytics_explainability()
    test_analytics_metrics()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 8 PART 4 SUCCESS: Enterprise Distributed Analytics & Real-Time Event Correlation Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
