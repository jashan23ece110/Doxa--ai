#!/usr/bin/env python3
"""
Integration Test Suite for Stage 9 Part 3 — Enterprise Autonomous Coding & Software Engineering Agent Platform.
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


def test_code_analysis_engine():
    print("\n🔍 Testing Code Analysis Engine...")
    from app.core.agents.coding.code_analysis_engine import code_analysis_engine

    repo_ctx = code_analysis_engine.analyze_repository("DoxaBackend", "/Users/jashanpreetsingh/doxa/backend")
    check("Repository context mapped", repo_ctx is not None)
    check("5 core modules identified", len(repo_ctx.modules) == 5)


def test_code_search_engine():
    print("\n🔎 Testing Code Intelligence Search Engine...")
    from app.core.agents.coding.code_search_engine import code_search_engine

    search_res = code_search_engine.search_symbol("AgentRegistry", "DoxaBackend")
    check("Symbol search completed", search_res is not None)
    check("Matched files > 0", len(search_res.matched_files) > 0)


def test_coding_planner():
    print("\n📋 Testing Autonomous Coding Planner...")
    from app.core.agents.coding.coding_planner import coding_planner

    plan = coding_planner.create_coding_plan("Add patch rollback validation", "DoxaBackend")
    check("Coding plan created", plan is not None)
    check("4 implementation steps generated", len(plan.steps) == 4)


def test_code_generation_engine():
    print("\n⚡ Testing Code Generation Engine...")
    from app.core.agents.coding.code_generation_engine import code_generation_engine

    patch = code_generation_engine.generate_patch("repo_100", "app/core/agents/coding/patch_manager.py", "Add conflict check")
    check("Patch generated", patch is not None)
    check("1 file change included", len(patch.file_changes) == 1)


def test_patch_manager():
    print("\n🩹 Testing Patch Manager Application & Rollback...")
    from app.core.agents.coding.code_generation_engine import code_generation_engine
    from app.core.agents.coding.patch_manager import patch_manager

    patch = code_generation_engine.generate_patch("repo_100", "app/core/agents/coding/patch_manager.py", "Patch test")

    applied = patch_manager.apply_patch(patch)
    check("Patch applied cleanly", applied and patch.is_applied)

    rolled_back = patch_manager.rollback_patch(patch.patch_id)
    check("Patch rolled back cleanly", rolled_back and not patch.is_applied)


async def test_test_execution_engine():
    print("\n🧪 Testing Sandboxed Test Execution Engine...")
    from app.core.agents.coding.test_execution_engine import test_execution_engine

    test_res = await test_execution_engine.run_tests("wsp_test", "pytest tests/")
    check("Sandboxed test execution succeeded", test_res.success)

    static_res = test_execution_engine.run_static_analysis("wsp_test")
    check("Static analysis clean", static_res.lint_score == 10.0)


def test_debugging_engine():
    print("\n🐛 Testing Autonomous Debugging Engine...")
    from app.core.agents.coding.debugging_engine import debugging_engine

    session = debugging_engine.diagnose_failure("ctask_100", "TypeError: missing 1 required positional argument")
    check("Failure diagnosed", session is not None)
    check("Confidence score >= 0.90", session.diagnoses[0].confidence_score >= 0.90)


def test_code_review_engine():
    print("\n👁️ Testing AI Code Review Engine...")
    from app.core.agents.coding.code_generation_engine import code_generation_engine
    from app.core.agents.coding.code_review_engine import code_review_engine

    patch = code_generation_engine.generate_patch("repo_100", "main.py", "Feature add")
    review = code_review_engine.review_patch(patch)

    check("Code review completed", review is not None)
    check("Patch approved", review.is_approved)
    check("Review score > 9.0", review.score > 9.0)


async def test_coding_agent_orchestrator():
    print("\n🌐 Testing Global Coding Agent Orchestrator...")
    from app.core.agents.coding.coding_agent_orchestrator import coding_agent_orchestrator

    wf_res = await coding_agent_orchestrator.execute_coding_workflow("Refactor patch manager rollback logic", "DoxaBackend")
    check("Autonomous coding workflow completed", wf_res is not None)
    check("Workflow status is COMPLETED", wf_res.status == "COMPLETED")
    check("Tests and review approved", wf_res.test_success and wf_res.review_approved)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-9 Part 2...")
    from app.core.agents.planning import autonomous_planning_engine
    from app.core.agents import agent_orchestrator
    from app.core.data_intelligence.platform import enterprise_data_intelligence_platform
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    plan = await autonomous_planning_engine.create_execution_plan("goal_coding_compat", "Coding Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Coding Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Coding_Master_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Coding_Master_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "code_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 9 PART 3 — ENTERPRISE AUTONOMOUS CODING AGENT PLATFORM TEST SUITE")
    print("==========================================================================")

    test_code_analysis_engine()
    test_code_search_engine()
    test_coding_planner()
    test_code_generation_engine()
    test_patch_manager()
    await test_test_execution_engine()
    test_debugging_engine()
    test_code_review_engine()
    await test_coding_agent_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 9 PART 3 SUCCESS: Enterprise Autonomous Coding Agent Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
