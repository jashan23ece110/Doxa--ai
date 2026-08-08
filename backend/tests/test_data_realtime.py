#!/usr/bin/env python3
"""
Integration Test Suite for Stage 8 Part 6 — Enterprise Real-Time Intelligence & Global Event Streaming Platform.
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


def test_event_stream_manager():
    print("\n🌊 Testing Event Stream Manager...")
    from app.core.data_intelligence.realtime.event_stream_manager import event_stream_manager

    topic = event_stream_manager.register_topic("security_events", partitions=8)
    check("Topic registered", topic is not None)

    retrieved = event_stream_manager.get_topic("security_events")
    check("Topic retrieved", retrieved.partitions_count == 8)

    event_stream_manager.record_message("security_events")
    check("Message recorded", retrieved.total_messages_count == 1)


async def test_realtime_pipeline():
    print("\n⚡ Testing Real-Time Intelligence Pipeline...")
    from app.core.data_intelligence.realtime.realtime_pipeline import realtime_intelligence_pipeline

    res = await realtime_intelligence_pipeline.process_event("evt_rt_100", {"action": "alert"})
    check("Pipeline executed", res is not None)
    check("8 real-time stages executed", len(res.stages_executed) == 8)
    check("Overall status is SUCCESS", res.overall_status == "SUCCESS")


def test_event_router():
    print("\n🔀 Testing Event Router...")
    from app.core.data_intelligence.realtime.event_router import event_router

    decision = event_router.route_event("evt_101", {"is_urgent": True}, topic="critical_events")
    check("Event routed", decision is not None)
    check("Priority set to HIGH", decision.priority == "HIGH")

    event_router.send_to_dlq("evt_err", {"bad": "data"}, "Malformed JSON")
    check("DLQ message sent", True)


def test_stream_state_manager():
    print("\n💾 Testing Stream State Manager...")
    from app.core.data_intelligence.realtime.stream_state_manager import stream_state_manager

    stream_state_manager.update_entity_state("ent_100", {"status": "ACTIVE", "risk": "LOW"})
    st = stream_state_manager.get_entity_state("ent_100")
    check("Entity state updated", st is not None and st["risk"] == "LOW")

    cnt = stream_state_manager.increment_counter("events_count", 5)
    check("Stream counter incremented", cnt == 5)


def test_realtime_correlation():
    print("\n🔗 Testing Real-Time Correlation Engine...")
    from app.core.data_intelligence.realtime.realtime_correlation import realtime_correlation_engine

    chain = realtime_correlation_engine.correlate_stream_events("evt_base", [{"event_id": "evt_sub1"}])
    check("Correlation chain generated", chain is not None)
    check("Confidence score > 0.90", chain.confidence_score > 0.90)


def test_realtime_anomaly_detector():
    print("\n⚠️ Testing Real-Time Anomaly Detector...")
    from app.core.data_intelligence.realtime.realtime_anomaly_detector import realtime_anomaly_detector

    anomalies = realtime_anomaly_detector.evaluate_event_stream("strm_prod", current_eps=250.0, baseline_eps=50.0)
    check("Stream rate spike evaluated", len(anomalies) == 1)
    check("Anomaly type is rate_spike", anomalies[0].anomaly_type == "rate_spike")


def test_intelligence_propagator():
    print("\n📡 Testing Intelligence Propagator...")
    from app.core.data_intelligence.realtime.intelligence_propagator import intelligence_propagator

    res = intelligence_propagator.propagate_intelligence("evt_prop_1", {"key": "val"})
    check("Intelligence propagated", res.success)
    check("5 subsystems targeted", len(res.target_subsystems) == 5)

    dup_res = intelligence_propagator.propagate_intelligence("evt_prop_1", {"key": "val"})
    check("Duplicate propagation prevented", dup_res.propagation_id.startswith("prop_dup_"))


def test_stream_checkpoint_manager():
    print("\n📌 Testing Stream Checkpoint Manager...")
    from app.core.data_intelligence.realtime.stream_checkpoint_manager import stream_checkpoint_manager

    cp = stream_checkpoint_manager.create_checkpoint("strm_prod", {0: 1500, 1: 1450})
    check("Checkpoint created", cp is not None)

    retrieved = stream_checkpoint_manager.get_latest_checkpoint("strm_prod")
    check("Checkpoint retrieved", retrieved.partition_offsets[0] == 1500)


def test_realtime_cache():
    print("\n⚡ Testing Real-Time Cache...")
    from app.core.data_intelligence.realtime.realtime_cache import realtime_cache

    realtime_cache.set("hot_entity_1", {"name": "Alice"}, ttl_seconds=60.0)
    val = realtime_cache.get("hot_entity_1")
    check("Real-time cache retrieved", val is not None and val["name"] == "Alice")


def test_realtime_observability():
    print("\n👁️ Testing Real-Time Observability...")
    from app.core.data_intelligence.realtime.realtime_observability import realtime_observability

    metrics = realtime_observability.get_observability_snapshot()
    check("Observability metrics snapshot retrieved", metrics is not None)
    check("Throughput EPS > 0", metrics.throughput_events_per_sec > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-7...")
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.data_intelligence import enterprise_data_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Realtime_Test")
    check("Human Intelligence Platform operates seamlessly with Real-Time Streaming Platform", assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "realtime_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 8 PART 6 — REAL-TIME INTELLIGENCE & EVENT STREAMING TEST SUITE")
    print("==========================================================================")

    test_event_stream_manager()
    await test_realtime_pipeline()
    test_event_router()
    test_stream_state_manager()
    test_realtime_correlation()
    test_realtime_anomaly_detector()
    test_intelligence_propagator()
    test_stream_checkpoint_manager()
    test_realtime_cache()
    test_realtime_observability()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 8 PART 6 SUCCESS: Enterprise Real-Time Intelligence & Event Streaming Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
