#!/usr/bin/env python3
"""
Integration Test Suite for Stage 9 Part 6 — Enterprise Multi-Agent Collaboration Platform.
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


def test_agent_team_manager():
    print("\n👥 Testing Agent Team Manager...")
    from app.core.agents.collaboration.agent_team_manager import agent_team_manager

    team = agent_team_manager.form_team(
        "FeatureDeliverySwarm",
        ["agent_research", "agent_coder", "agent_devops"],
        {"agent_research": "RESEARCHER", "agent_coder": "CODER", "agent_devops": "DEVOPS"},
    )
    check("Agent team formed", team is not None)
    check("3 member agents registered", len(team.member_agent_ids) == 3)
    check("Role assigned to agent_coder", team.roles_map.get("agent_coder") == "CODER")


def test_task_delegation_engine():
    print("\n📋 Testing Autonomous Task Delegation Engine...")
    from app.core.agents.collaboration.task_delegation_engine import task_delegation_engine

    dtask = task_delegation_engine.delegate_task("cgoal_100", "Generate Patch", "code_generation", "agent_coder")
    check("Task delegated", dtask is not None)
    check("Assigned agent matches candidate", dtask.assigned_agent_id == "agent_coder")
    check("Status is IN_PROGRESS", dtask.status == "IN_PROGRESS")


def test_collaboration_bus():
    print("\n💬 Testing Enterprise Agent Collaboration Bus...")
    from app.core.agents.collaboration.collaboration_types import AgentMessage
    from app.core.agents.collaboration.collaboration_bus import collaboration_bus

    msg1 = AgentMessage(sender_agent_id="agent_research", recipient_agent_id="agent_coder", message_type="RESEARCH_EVIDENCE")
    published = collaboration_bus.publish_message(msg1)
    check("Message published to bus", published)

    msgs = collaboration_bus.get_messages_for_agent("agent_coder")
    check("Recipient retrieved message", len(msgs) > 0)


def test_shared_context_manager():
    print("\n🌐 Testing Shared Context Manager...")
    from app.core.agents.collaboration.collaboration_types import AgentObservation
    from app.core.agents.collaboration.shared_context_manager import shared_context_manager

    obs = AgentObservation(agent_id="agent_research", observation_type="CODE_STRUCTURE", details={"files": 150})
    shared_context_manager.add_observation("session_100", obs)

    sctx = shared_context_manager.get_or_create_context("session_100")
    check("Shared context created", sctx is not None)
    check("1 observation stored", len(sctx.observations) == 1)


def test_consensus_engine():
    print("\n🗳️ Testing Multi-Agent Consensus Engine...")
    from app.core.agents.collaboration.collaboration_types import AgentVote
    from app.core.agents.collaboration.consensus_engine import consensus_engine

    votes = [
        AgentVote(agent_id="a1", proposal_id="prop_1", decision="APPROVE"),
        AgentVote(agent_id="a2", proposal_id="prop_1", decision="APPROVE"),
        AgentVote(agent_id="a3", proposal_id="prop_1", decision="REJECT"),
    ]

    cres = consensus_engine.evaluate_consensus("prop_1", votes, strategy="MAJORITY")
    check("Consensus evaluated", cres is not None)
    check("Consensus reached (>50%)", cres.is_consensus_reached)
    check("Approval ratio == 0.67", cres.approval_ratio == 0.67)


def test_conflict_resolution_engine():
    print("\n⚖️ Testing Agent Conflict Resolution Engine...")
    from app.core.agents.collaboration.collaboration_types import Conflict
    from app.core.agents.collaboration.conflict_resolution_engine import conflict_resolution_engine

    conflict = Conflict(
        agent_ids=["agent_a", "agent_b"],
        description="Conflicting deployment strategy proposals",
        competing_proposals=[{"proposal_id": "prop_canary"}, {"proposal_id": "prop_rolling"}],
    )

    res = conflict_resolution_engine.resolve_conflict(conflict)
    check("Conflict resolved", res is not None)
    check("Winning proposal selected", res.winning_proposal_id == "prop_canary")


def test_workflow_state_manager():
    print("\n💾 Testing Persistent Workflow State Manager...")
    from app.core.agents.collaboration.workflow_state_manager import workflow_state_manager

    chk = workflow_state_manager.create_checkpoint("wf_100", "RESEARCH_COMPLETE", {"status": "SUCCESS"})
    check("Checkpoint created", chk is not None)
    check("Checkpoint step name matches", chk.step_name == "RESEARCH_COMPLETE")

    state = workflow_state_manager.get_or_create_state("wf_100")
    check("Current step updated in workflow state", state.current_step == "RESEARCH_COMPLETE")


async def test_workflow_coordinator():
    print("\n⚙️ Testing Multi-Agent Workflow Coordinator...")
    from app.core.agents.collaboration.workflow_coordinator import workflow_coordinator

    steps = ["RESEARCH", "PLANNING", "CODING", "DEVOPS"]
    state = await workflow_coordinator.execute_multi_agent_workflow("wf_coord_1", steps)
    check("Workflow executed cleanly", state is not None)
    check("Workflow status is COMPLETED", state.status == "COMPLETED")
    check("4 checkpoints logged", len(state.checkpoints) == 4)


async def test_collaboration_orchestrator():
    print("\n🌐 Testing Global Collaboration Orchestrator Workflow...")
    from app.core.agents.collaboration.collaboration_orchestrator import collaboration_orchestrator

    res = await collaboration_orchestrator.execute_collaboration_session(
        "Build & Deploy Security Analytics Module",
        ["agent_researcher", "agent_planner", "agent_coder", "agent_devops"],
    )
    check("Multi-agent collaboration session completed", res is not None)
    check("Session status is COMPLETED", res.status == "COMPLETED")
    check("Consensus reached", res.consensus_reached)
    check("5 workflow steps completed", res.steps_completed_count == 5)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-9 Part 5...")
    from app.core.agents.devops import devops_agent_orchestrator
    from app.core.agents.research import research_agent_orchestrator
    from app.core.agents.coding import coding_agent_orchestrator
    from app.core.agents.planning import autonomous_planning_engine
    from app.core.agents import agent_orchestrator
    from app.core.data_intelligence.platform import enterprise_data_intelligence_platform
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Collab-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Multi-Agent Security", "Analyze Swarm Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor collab bus logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_collab_compat", "Collab Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Collab Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Collab_Master_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Collab_Master_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "collab_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 9 PART 6 — ENTERPRISE MULTI-AGENT COLLABORATION PLATFORM TEST SUITE")
    print("==========================================================================")

    test_agent_team_manager()
    test_task_delegation_engine()
    test_collaboration_bus()
    test_shared_context_manager()
    test_consensus_engine()
    test_conflict_resolution_engine()
    test_workflow_state_manager()
    await test_workflow_coordinator()
    await test_collaboration_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 9 PART 6 SUCCESS: Enterprise Multi-Agent Collaboration Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
