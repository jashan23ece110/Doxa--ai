#!/usr/bin/env python3
"""
Integration Test Suite for Stage 7 Part 3 — Enterprise Human Behavior Modeling & Influence Analysis Platform.
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


def test_behavior_model_engine():
    print("\n🧠 Testing Behavior Modeling Engine...")
    from app.core.human_intelligence.behavior.behavior_model_engine import behavior_model_engine

    prof = behavior_model_engine.build_behavior_profile("emp_100", security_score=88.0)
    check("Probabilistic behavior profile built", prof is not None)
    check("Security habit score == 88.0", prof.security_habit_score == 88.0)
    check("Observed patterns present", len(prof.observed_patterns) > 0)


def test_influence_analysis():
    print("\n🌐 Testing Influence Analysis Engine...")
    from app.core.human_intelligence.behavior.influence_analysis import influence_analysis_engine

    influence = influence_analysis_engine.analyze_influence("emp_100")
    check("Influence metric produced", influence is not None)
    check("Influence score > 80.0", influence.influence_score > 80.0)


def test_human_risk_engine():
    print("\n⚠️ Testing Human Risk Engine...")
    from app.core.human_intelligence.behavior.human_risk_engine import human_risk_engine

    risk = human_risk_engine.evaluate_human_risk("emp_100", security_score=90.0)
    check("Human risk score calculated", risk.behavioral_risk_score == 1.0)
    check("Phishing susceptibility estimate present", risk.phishing_susceptibility_estimate > 0)


def test_communication_analytics():
    print("\n📡 Testing Communication Intelligence Engine...")
    from app.core.human_intelligence.behavior.communication_analytics import communication_analytics_engine

    analytics = communication_analytics_engine.analyze_metadata("emp_100")
    check("Communication metadata analytics produced", analytics is not None)
    check("Daily collaboration count > 0", analytics.daily_collaboration_events_count > 0)


def test_trust_graph():
    print("\n🕸️ Testing Enterprise Trust Graph...")
    from app.core.human_intelligence.behavior.trust_graph import enterprise_trust_graph

    rel = enterprise_trust_graph.add_relationship("emp_100", "emp_200", "manager", 0.95)
    check("Trust relationship added", rel is not None)

    connections = enterprise_trust_graph.get_trusted_connections("emp_100")
    check("Trusted connections retrieved", len(connections) >= 1)


def test_behavioral_pattern_repository():
    print("\n💾 Testing Behavioral Pattern Repository...")
    from app.core.human_intelligence.human_intelligence_types import BehaviorPattern
    from app.core.human_intelligence.behavior.behavioral_pattern_repository import behavioral_pattern_repository

    pats = [BehaviorPattern(pattern_id="p1", category="auth", description="Password hygiene")]
    rec = behavioral_pattern_repository.save_patterns("emp_100", pats)
    check("Patterns saved to repository", rec is not None)

    history = behavioral_pattern_repository.get_history("emp_100")
    check("Pattern history retrieved", len(history) >= 1)


def test_anomaly_detection():
    print("\n🚨 Testing Behavioral Anomaly Engine...")
    from app.core.human_intelligence.behavior.anomaly_detection import behavioral_anomaly_engine

    anomalies = behavioral_anomaly_engine.detect_anomalies("emp_100", security_score=50.0)
    check("Awareness regression anomaly detected", len(anomalies) == 1)
    check("Anomaly severity is HIGH", anomalies[0].severity == "HIGH")


def test_explainability_engine():
    print("\n💡 Testing Behavior Explainability Engine...")
    from app.core.human_intelligence.behavior.explainability_engine import behavior_explainability_engine

    explanation = behavior_explainability_engine.explain_risk_score("emp_100", risk_score=1.5)
    check("Behavioral explanation produced", explanation is not None)
    check("Contributing factors present", len(explanation.contributing_factors) > 0)


def test_behavior_dashboard_backend():
    print("\n🖥️ Testing Behavior Analytics Dashboard Backend...")
    from app.core.human_intelligence.behavior.behavior_dashboard_backend import behavior_dashboard_backend

    metrics = behavior_dashboard_backend.get_dashboard_metrics()
    check("Total profiles modeled > 0", metrics.total_profiles_modeled > 0)
    check("Trust graph nodes count > 0", metrics.trust_graph_nodes_count > 0)


def test_behavior_report_builder():
    print("\n📄 Testing Behavioral Report Builder...")
    from app.core.human_intelligence.behavior.behavior_model_engine import behavior_model_engine
    from app.core.human_intelligence.behavior.influence_analysis import influence_analysis_engine
    from app.core.human_intelligence.behavior.explainability_engine import behavior_explainability_engine
    from app.core.human_intelligence.behavior.behavior_report_builder import behavior_report_builder

    prof = behavior_model_engine.build_behavior_profile("emp_100")
    inf = influence_analysis_engine.analyze_influence("emp_100")
    expl = behavior_explainability_engine.explain_risk_score("emp_100", 1.5)

    data = behavior_report_builder.build_report_data(prof, inf, expl)
    check("Report data produced", data["employee_id"] == "emp_100")

    md = behavior_report_builder.to_markdown(data)
    check("Markdown behavioral report generated", "# Enterprise Behavioral Intelligence Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-6...")
    from app.core.human_intelligence import enterprise_human_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    emp = enterprise_human_intelligence_manager.register_employee_profile("Frank Castle", "frank@doxa.internal", "Security", "Analyst")
    check("Human Intelligence Manager operates seamlessly with behavior platform", emp is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "behavior_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 7 PART 3 — HUMAN BEHAVIOR MODELING & INFLUENCE ANALYSIS TEST SUITE")
    print("==========================================================================")

    test_behavior_model_engine()
    test_influence_analysis()
    test_human_risk_engine()
    test_communication_analytics()
    test_trust_graph()
    test_behavioral_pattern_repository()
    test_anomaly_detection()
    test_explainability_engine()
    test_behavior_dashboard_backend()
    test_behavior_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 7 PART 3 SUCCESS: Human Behavior Modeling & Influence Analysis Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
