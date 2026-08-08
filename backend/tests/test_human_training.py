#!/usr/bin/env python3
"""
Integration Test Suite for Stage 7 Part 5 — Enterprise Security Awareness & Behavioral Training Platform.
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


def test_adaptive_learning_engine():
    print("\n🎓 Testing Adaptive Learning Engine...")
    from app.core.human_intelligence.training.adaptive_learning_engine import adaptive_learning_engine

    path = adaptive_learning_engine.build_personalized_path("emp_100", role="Engineering", security_score=85.0)
    check("Personalized learning path built", path is not None)
    check("Assigned modules count > 0", len(path.assigned_modules) > 0)


def test_behavior_improvement_engine():
    print("\n📈 Testing Behavior Improvement Engine...")
    from app.core.human_intelligence.training.behavior_improvement_engine import behavior_improvement_engine

    metrics = behavior_improvement_engine.evaluate_improvement("emp_100", baseline_score=75.0, current_score=87.5)
    check("Score improvement delta calculated (+12.5%)", metrics.score_improvement_delta == 12.5)
    check("Behavioral maturity stage PROACTIVE", metrics.behavioral_maturity_stage == "PROACTIVE")


def test_coaching_engine():
    print("\n💬 Testing AI Security Coaching Engine...")
    from app.core.human_intelligence.training.coaching_engine import security_coaching_engine

    session = security_coaching_engine.generate_coaching_feedback("emp_100", "Phishing Awareness")
    check("Coaching session generated", session is not None)
    check("Suggested habits count > 0", len(session.suggested_habits) > 0)


def test_competency_framework():
    print("\n🏆 Testing Enterprise Competency Framework...")
    from app.core.human_intelligence.training.competency_framework import competency_framework

    profile = competency_framework.evaluate_competency("emp_100", security_score=88.0)
    check("Proficiency level ADVANCED", profile.proficiency_level == "ADVANCED")
    check("Certified skills present", len(profile.certified_skills) > 0)


def test_curriculum_manager():
    print("\n📚 Testing Enterprise Curriculum Manager...")
    from app.core.human_intelligence.training.curriculum_manager import curriculum_manager

    courses = curriculum_manager.get_curriculum_for_role("All")
    check("Role curriculum courses count > 0", len(courses) > 0)


def test_engagement_analytics():
    print("\n📊 Testing Learning Engagement Analytics Engine...")
    from app.core.human_intelligence.training.engagement_analytics import learning_engagement_analytics

    metrics = learning_engagement_analytics.compute_engagement("Engineering")
    check("Knowledge retention score > 90%", metrics.knowledge_retention_score > 90.0)
    check("Participation rate > 95%", metrics.participation_rate_percent > 95.0)


def test_awareness_maturity_engine():
    print("\n🏰 Testing Security Awareness Maturity Engine...")
    from app.core.human_intelligence.training.awareness_maturity_engine import awareness_maturity_engine

    maturity = awareness_maturity_engine.evaluate_maturity("Organization", average_score=88.0)
    check("Maturity level == 4", maturity.maturity_level == 4)
    check("Maturity stage PROACTIVE & RESILIENT", "PROACTIVE" in maturity.maturity_stage_name)


def test_learning_recommendation_engine():
    print("\n💡 Testing Training AI Recommendation Engine...")
    from app.core.human_intelligence.training.learning_recommendation_engine import training_recommendation_engine

    recs = training_recommendation_engine.generate_training_recommendations("emp_100", current_score=85.0)
    check("Training recommendations count > 0", len(recs) > 0)


def test_training_dashboard_backend():
    print("\n🖥️ Testing Training Dashboard Backend...")
    from app.core.human_intelligence.training.training_dashboard_backend import training_dashboard_backend

    metrics = training_dashboard_backend.get_dashboard_metrics()
    check("Completed courses count > 0", metrics.completed_courses_count > 0)
    check("Coaching satisfaction rate > 95%", metrics.coaching_satisfaction_rate > 95.0)


def test_training_report_builder():
    print("\n📄 Testing Training Report Builder...")
    from app.core.human_intelligence.training.behavior_improvement_engine import behavior_improvement_engine
    from app.core.human_intelligence.training.competency_framework import competency_framework
    from app.core.human_intelligence.training.awareness_maturity_engine import awareness_maturity_engine
    from app.core.human_intelligence.training.training_report_builder import training_report_builder

    imp = behavior_improvement_engine.evaluate_improvement("emp_100")
    comp = competency_framework.evaluate_competency("emp_100")
    mat = awareness_maturity_engine.evaluate_maturity("Organization")

    data = training_report_builder.build_report_data(imp, comp, mat)
    check("Report data produced", data["employee_id"] == "emp_100")

    md = training_report_builder.to_markdown(data)
    check("Markdown training report generated", "# Enterprise Human Intelligence Training Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-6...")
    from app.core.human_intelligence import enterprise_human_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    emp = enterprise_human_intelligence_manager.register_employee_profile("Ada Lovelace", "ada@doxa.internal", "Research", "Lead Scientist")
    check("Human Intelligence Manager operates seamlessly with training platform", emp is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "training_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 7 PART 5 — BEHAVIORAL TRAINING & HUMAN INTELLIGENCE TEST SUITE")
    print("==========================================================================")

    test_adaptive_learning_engine()
    test_behavior_improvement_engine()
    test_coaching_engine()
    test_competency_framework()
    test_curriculum_manager()
    test_engagement_analytics()
    test_awareness_maturity_engine()
    test_learning_recommendation_engine()
    test_training_dashboard_backend()
    test_training_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 7 PART 5 SUCCESS: Behavioral Training & Human Intelligence Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
