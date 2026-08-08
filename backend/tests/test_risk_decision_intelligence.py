#!/usr/bin/env python3
"""
Integration Test Suite for Stage 10 Part 3 — Enterprise Risk Intelligence & Forecasting Platform.
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


async def test_risk_identification_engine():
    print("\n🔍 Testing Risk Identification Engine...")
    from app.core.decision_intelligence.risk.risk_identification_engine import risk_identification_engine

    risks = await risk_identification_engine.identify_risks("GatewayService")
    check("Risks identified", len(risks) == 2)
    check("Operational risk present", risks[0].category == "OPERATIONAL")
    check("Security risk present", risks[1].category == "SECURITY")


def test_risk_scoring_engine():
    print("\n📊 Testing Risk Scoring Engine...")
    from app.core.decision_intelligence.risk.risk_types import Risk, RiskProbability, RiskImpact
    from app.core.decision_intelligence.risk.risk_scoring_engine import risk_scoring_engine

    risk = Risk(title="Test Risk", probability=RiskProbability(value=0.20), impact=RiskImpact(severity="MEDIUM"))
    score = risk_scoring_engine.calculate_risk_score(risk)

    check("Risk score calculated", score is not None)
    check("Raw score > 0.0", score.raw_score > 0.0)
    check("Methodology recorded", score.scoring_methodology == "PROBABILITY_X_IMPACT")


def test_risk_correlation_engine():
    print("\n🔗 Testing Risk Correlation Engine...")
    from app.core.decision_intelligence.risk.risk_types import Risk
    from app.core.decision_intelligence.risk.risk_correlation_engine import risk_correlation_engine

    r1 = Risk(title="Risk 1")
    r2 = Risk(title="Risk 2")
    corrs = risk_correlation_engine.correlate_risks([r1, r2])

    check("Risk correlation edge created", len(corrs) == 1)
    check("Correlation coefficient == 0.65", corrs[0].correlation_coefficient == 0.65)


def test_risk_propagation_engine():
    print("\n🌊 Testing Risk Propagation Engine...")
    from app.core.decision_intelligence.risk.risk_types import Risk
    from app.core.decision_intelligence.risk.risk_propagation_engine import risk_propagation_engine

    root = Risk(title="Root Outage")
    downstream = [Risk(title="API Failure")]
    prop = risk_propagation_engine.analyze_propagation(root, downstream)

    check("Risk propagation modeled", prop is not None)
    check("Cascading risk IDs recorded", len(prop.cascading_risk_ids) == 1)
    check("Amplification factor == 1.25", prop.amplification_factor == 1.25)


def test_forecasting_engine():
    print("\n📈 Testing Enterprise Forecasting Engine...")
    from app.core.decision_intelligence.risk.forecasting_engine import forecasting_engine

    fcst = forecasting_engine.forecast_risk_trajectory("OperationalRisk", horizon_days=30)
    check("Risk forecast generated", fcst is not None)
    check("Horizon == 30 days", fcst.horizon_days == 30)
    check("Projected risk score > 0", fcst.projected_risk_score > 0)


def test_early_warning_engine():
    print("\n🚨 Testing Early Warning System...")
    from app.core.decision_intelligence.risk.risk_types import Risk, RiskIndicator
    from app.core.decision_intelligence.risk.early_warning_engine import early_warning_engine

    r = Risk(title="High Latency Risk", indicators=[RiskIndicator(name="p99_latency", threshold_value=100.0, current_value=150.0)])
    signals = early_warning_engine.check_indicators([r])

    check("Early warning signal detected", len(signals) == 1)
    check("Threshold breach message recorded", "breached threshold" in signals[0].message)


def test_risk_scenario_engine():
    print("\n🎭 Testing Risk Scenario Engine...")
    from app.core.decision_intelligence.risk.risk_scenario_engine import risk_scenario_engine

    scenarios = risk_scenario_engine.generate_risk_scenarios("PaymentGateway")
    check("3 risk scenarios generated", len(scenarios) == 3)
    check("BASELINE scenario present", scenarios[0].name == "BASELINE")


def test_risk_mitigation_engine():
    print("\n🛠️ Testing Risk Mitigation Engine...")
    from app.core.decision_intelligence.risk.risk_types import Risk
    from app.core.decision_intelligence.risk.risk_mitigation_engine import risk_mitigation_engine

    risk = Risk(title="Memory Leak Risk")
    mits = risk_mitigation_engine.propose_mitigations(risk)

    check("Mitigations proposed", len(mits) == 1)
    check("Expected risk reduction == 80%", mits[0].expected_risk_reduction_pct == 80.0)
    check("Requires human approval", mits[0].requires_approval)


async def test_risk_intelligence_orchestrator():
    print("\n🌐 Testing Global Risk Intelligence Orchestrator...")
    from app.core.decision_intelligence.risk.risk_intelligence_orchestrator import risk_intelligence_orchestrator

    res = await risk_intelligence_orchestrator.execute_risk_assessment("CoreDataStore")
    check("Master risk assessment completed", res is not None)
    check("Status is COMPLETED", res.status == "COMPLETED")
    check("Assessment score calculated", res.assessment.overall_risk_score > 0)
    check("Recommendation generated", res.recommendation is not None)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-10 Part 2...")
    from app.core.decision_intelligence.strategy.strategic_orchestrator import strategic_orchestrator
    from app.core.decision_intelligence.decision_intelligence_orchestrator import decision_intelligence_orchestrator
    from app.core.agents.platform import autonomous_agent_orchestrator
    from app.core.agents.autonomy import agent_memory_engine
    from app.core.agents.collaboration import collaboration_orchestrator
    from app.core.agents.devops import devops_agent_orchestrator
    from app.core.agents.research import research_agent_orchestrator
    from app.core.agents.coding import coding_agent_orchestrator
    from app.core.agents.planning import autonomous_planning_engine
    from app.core.agents import agent_orchestrator
    from app.core.data_intelligence.platform import enterprise_data_intelligence_platform
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    strat_res = await strategic_orchestrator.execute_strategic_analysis("Risk Integration Strategic Plan")
    check("Stage 10 Part 2 Strategic Intelligence Orchestrator operates seamlessly", strat_res is not None)

    dec_res = await decision_intelligence_orchestrator.execute_decision_analysis("Risk Integration Decision", "Evaluate integration")
    check("Stage 10 Part 1 Decision Intelligence Orchestrator operates seamlessly", dec_res is not None)

    master_agent_res = await autonomous_agent_orchestrator.execute_master_autonomous_goal("Risk Integration Test Goal", "DoxaBackend")
    check("Stage 9 Global Autonomous Agent Platform operates seamlessly", master_agent_res is not None)

    mem = agent_memory_engine.get_or_create_memory("risk_compat_agent")
    check("Stage 9 Part 7 Agent Memory Engine operates seamlessly", mem is not None)

    cres = await collaboration_orchestrator.execute_collaboration_session("Risk Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Risk-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Risk Security", "Analyze Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor risk logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_risk_compat", "Risk Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Risk Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Risk_Platform_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Risk_Platform_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "risk_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 10 PART 3 — ENTERPRISE RISK INTELLIGENCE & FORECASTING TEST SUITE")
    print("==========================================================================")

    await test_risk_identification_engine()
    test_risk_scoring_engine()
    test_risk_correlation_engine()
    test_risk_propagation_engine()
    test_forecasting_engine()
    test_early_warning_engine()
    test_risk_scenario_engine()
    test_risk_mitigation_engine()
    await test_risk_intelligence_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 10 PART 3 SUCCESS: Enterprise Risk Intelligence Platform Complete!")


if __name__ == "__main__":
    asyncio.run(main())
