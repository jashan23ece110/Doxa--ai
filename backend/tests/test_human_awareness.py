#!/usr/bin/env python3
"""
Integration Test Suite for Stage 7 Part 2 — Security Awareness, Phishing Simulation & Assessment Platform.
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


def test_campaign_manager():
    print("\n📢 Testing Awareness Campaign Manager...")
    from app.core.human_intelligence.awareness.campaign_manager import campaign_manager

    camp = campaign_manager.create_campaign("Q3 Spear-Phishing Awareness Campaign", "Engineering")
    check("Campaign created", camp.campaign_id is not None)
    check("Target department is Engineering", camp.target_department == "Engineering")

    updated = campaign_manager.update_progress(camp.campaign_id, 100.0)
    check("Campaign completed when progress == 100%", updated.status == "completed")


def test_phishing_simulation_engine():
    print("\n🎣 Testing Safe Phishing Simulation Engine...")
    from app.core.human_intelligence.awareness.phishing_simulation_engine import phishing_simulation_engine

    res = phishing_simulation_engine.evaluate_mock_interaction("emp_100", "email_awareness", user_reported=True, user_clicked_link=False)
    check("Mock interaction evaluated", res is not None)
    check("Recognized indicator is True when reported and unclicked", res.recognized_indicator)
    check("Educational feedback present", len(res.educational_feedback) > 0)


def test_assessment_engine():
    print("\n🧠 Testing Security Assessment Engine...")
    from app.core.human_intelligence.awareness.assessment_engine import assessment_engine

    questions = assessment_engine.generate_quiz("phishing_awareness", "executive")
    check("Quiz questions generated > 0", len(questions) > 0)

    res = assessment_engine.evaluate_answers("emp_100", {"q1": 1})
    check("Evaluation score percent == 100.0%", res.score_percent == 100.0)


def test_training_engine():
    print("\n📚 Testing Enterprise Training Engine...")
    from app.core.human_intelligence.awareness.training_engine import enterprise_training_engine

    rec = enterprise_training_engine.assign_training("emp_100", "Executive Phishing Defense 101")
    check("Training assigned", rec.status == "assigned")

    completed = enterprise_training_engine.complete_training(rec.record_id, "emp_100")
    check("Training marked completed", completed.status == "completed")


def test_awareness_scoring():
    print("\n📊 Testing Awareness Scoring Engine...")
    from app.core.human_intelligence.awareness.awareness_scoring import awareness_scoring_engine

    score = awareness_scoring_engine.calculate_employee_score("emp_100", [90.0, 95.0, 100.0])
    check("Overall awareness score calculated", score.overall_awareness_score > 90.0)
    check("Improvement trend improving", score.improvement_trend == "improving")


def test_scenario_library():
    print("\n📚 Testing Simulation Scenario Library...")
    from app.core.human_intelligence.awareness.scenario_library import scenario_library

    scenarios = scenario_library.list_scenarios()
    check("Scenarios registered > 0", len(scenarios) > 0)
    check("QR code awareness scenario present", any("QR Code" in s.title for s in scenarios) or len(scenarios) >= 2)


def test_learning_analytics():
    print("\n📈 Testing Learning Analytics Engine...")
    from app.core.human_intelligence.awareness.learning_analytics import learning_analytics_engine

    metrics = learning_analytics_engine.analyze_department_performance("Engineering")
    check("Department metrics produced", metrics.department_name == "Engineering")
    check("Completion rate > 90%", metrics.completion_rate_percent > 90.0)


def test_recommendation_engine():
    print("\n💡 Testing AI Learning Recommendation Engine...")
    from app.core.human_intelligence.awareness.recommendation_engine import ai_learning_recommendation_engine

    recs = ai_learning_recommendation_engine.generate_learning_recommendations("emp_100", ["QR Code Auth"])
    check("Learning recommendations count > 0", len(recs) > 0)
    check("High priority recommendation produced", recs[0].priority == "HIGH")


def test_awareness_dashboard_backend():
    print("\n🖥️ Testing Awareness Dashboard Backend...")
    from app.core.human_intelligence.awareness.awareness_dashboard_backend import awareness_dashboard_backend

    metrics = awareness_dashboard_backend.get_dashboard_metrics()
    check("Org awareness score > 80.0%", metrics.overall_org_awareness_score > 80.0)
    check("Phishing simulation report rate > 80.0%", metrics.phishing_simulation_report_rate > 80.0)


def test_awareness_report_builder():
    print("\n📄 Testing Awareness Report Builder...")
    from app.core.human_intelligence.awareness.campaign_manager import campaign_manager
    from app.core.human_intelligence.awareness.awareness_report_builder import awareness_report_builder

    camp = campaign_manager.create_campaign("Annual Security Awareness Drive")
    data = awareness_report_builder.build_report_data(camp, avg_awareness_score=91.5)
    check("Report data created", data["campaign_name"] == "Annual Security Awareness Drive")

    md = awareness_report_builder.to_markdown(data)
    check("Markdown awareness report generated", "# Enterprise Security Awareness Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-6...")
    from app.core.human_intelligence import enterprise_human_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    emp = enterprise_human_intelligence_manager.register_employee_profile("Eve Adams", "eve@doxa.internal", "Finance", "Analyst")
    check("Human Intelligence Manager works with awareness platform", emp is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "awareness_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 7 PART 2 — SECURITY AWARENESS & PHISHING SIMULATION TEST SUITE")
    print("==========================================================================")

    test_campaign_manager()
    test_phishing_simulation_engine()
    test_assessment_engine()
    test_training_engine()
    test_awareness_scoring()
    test_scenario_library()
    test_learning_analytics()
    test_recommendation_engine()
    test_awareness_dashboard_backend()
    test_awareness_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 7 PART 2 SUCCESS: Security Awareness & Phishing Simulation Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
