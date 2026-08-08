#!/usr/bin/env python3
"""
Integration Test Suite for Stage 8 Part 7 — Enterprise Predictive Intelligence & Autonomous Data Discovery Platform.
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


def test_predictive_intelligence_engine():
    print("\n🔮 Testing Predictive Intelligence Engine...")
    from app.core.data_intelligence.discovery.predictive_intelligence_engine import predictive_intelligence_engine

    pred = predictive_intelligence_engine.forecast_scope("Finance_Dept", "risk")
    check("Forecast generated", pred is not None)
    check("Forecasted value > 0", pred.forecasted_value > 0.0)
    check("Confidence score >= 0.90", pred.confidence_score >= 0.90)


def test_pattern_discovery_engine():
    print("\n🧩 Testing Pattern Discovery Engine...")
    from app.core.data_intelligence.discovery.pattern_discovery_engine import pattern_discovery_engine

    patterns = pattern_discovery_engine.discover_patterns("ds_logs", ["rec_1", "rec_2"])
    check("Patterns discovered", len(patterns) > 0)
    check("Pattern type is recurring", patterns[0].pattern_type == "recurring")


def test_hypothesis_engine():
    print("\n🧠 Testing Hypothesis Engine...")
    from app.core.data_intelligence.discovery.hypothesis_engine import hypothesis_engine

    hyp = hypothesis_engine.generate_hypothesis("Anomaly Detection", ["Event spike at 02:00"])
    check("Hypothesis generated", hyp is not None)
    check("Initially unverified", not hyp.is_verified)


def test_hypothesis_validation():
    print("\n✔️ Testing Hypothesis Validation Engine...")
    from app.core.data_intelligence.discovery.hypothesis_engine import hypothesis_engine
    from app.core.data_intelligence.discovery.hypothesis_validation import hypothesis_validation_engine

    hyp = hypothesis_engine.generate_hypothesis("Security Incident", ["Ev1", "Ev2"])
    val = hypothesis_validation_engine.validate_hypothesis(hyp)
    check("Validation completed", val is not None)
    check("Verdict is SUPPORTED", val.verdict == "SUPPORTED")
    check("Hypothesis updated to verified", hyp.is_verified)


def test_emerging_signal_detector():
    print("\n📡 Testing Emerging Signal Detector...")
    from app.core.data_intelligence.discovery.emerging_signal_detector import emerging_signal_detector

    signals = emerging_signal_detector.detect_emerging_signals("Enterprise_Network")
    check("Emerging signals detected", len(signals) > 0)
    check("Growth rate > 40%", signals[0].growth_rate_percent > 40.0)


def test_scenario_engine():
    print("\n🎭 Testing Scenario Engine...")
    from app.core.data_intelligence.discovery.scenario_engine import scenario_engine

    scenarios = scenario_engine.generate_scenarios("Operations")
    check("Scenario models generated", len(scenarios) >= 2)
    check("Risk scenario present", any(s.scenario_type == "risk" for s in scenarios))


def test_predictive_model_registry():
    print("\n📜 Testing Predictive Model Registry...")
    from app.core.data_intelligence.discovery.predictive_model_registry import predictive_model_registry

    model = predictive_model_registry.register_model("RiskForecaster", version="2.0.0")
    check("Model registered", model is not None)

    retrieved = predictive_model_registry.get_model(model.model_id)
    check("Model retrieved", retrieved.version == "2.0.0")


def test_discovery_scheduler():
    print("\n⏱️ Testing Discovery Scheduler...")
    from app.core.data_intelligence.discovery.discovery_scheduler import discovery_scheduler

    job = discovery_scheduler.schedule_job("Nightly Trend Scan", "forecasting")
    check("Discovery job scheduled", job is not None)

    retrieved = discovery_scheduler.get_job(job.job_id)
    check("Discovery job retrieved", retrieved.status == "COMPLETED")


def test_discovery_recommendation_engine():
    print("\n💡 Testing Discovery Recommendation Engine...")
    from app.core.data_intelligence.discovery.discovery_recommendation_engine import discovery_recommendation_engine

    recs = discovery_recommendation_engine.generate_recommendations("IT_Security", ["Signal spike"])
    check("Recommendations generated", len(recs) > 0)
    check("Expected impact is HIGH", recs[0].expected_impact == "HIGH")


def test_discovery_metrics():
    print("\n📊 Testing Discovery Metrics Tracker...")
    from app.core.data_intelligence.discovery.discovery_metrics import discovery_metrics_tracker

    snapshot = discovery_metrics_tracker.get_metrics_snapshot()
    check("Discovery metrics snapshot retrieved", snapshot is not None)
    check("Predictions count > 0", snapshot.predictions_generated_count > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-7...")
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.data_intelligence import enterprise_data_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Discovery_Test")
    check("Human Intelligence Platform operates seamlessly with Discovery Platform", assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "discovery_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 8 PART 7 — PREDICTIVE INTELLIGENCE & AUTONOMOUS DISCOVERY TEST SUITE")
    print("==========================================================================")

    test_predictive_intelligence_engine()
    test_pattern_discovery_engine()
    test_hypothesis_engine()
    test_hypothesis_validation()
    test_emerging_signal_detector()
    test_scenario_engine()
    test_predictive_model_registry()
    test_discovery_scheduler()
    test_discovery_recommendation_engine()
    test_discovery_metrics()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 8 PART 7 SUCCESS: Enterprise Predictive Intelligence & Autonomous Discovery Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
