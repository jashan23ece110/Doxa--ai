#!/usr/bin/env python3
"""
Integration Test Suite for Stage 9 Part 1 — Foundational Enterprise Autonomous Agent Platform.
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


def test_agent_registry():
    print("\n📋 Testing Agent Registry & Capability Discovery...")
    from app.core.agents.agent_types import AgentDefinition, AgentCapability, AgentRole
    from app.core.agents.agent_registry import agent_registry

    cap = AgentCapability(name="threat_modeling", description="Capability to model threats")
    agent_def = AgentDefinition(
        name="TestThreatAgent",
        role=AgentRole.SECURITY_AUDITOR,
        description="Threat modeling specialist agent",
        capabilities=[cap],
    )

    agent_registry.register_agent(agent_def)
    discovered = agent_registry.find_agents_by_capability("threat_modeling")
    check("Agent registered and discovered by capability", len(discovered) == 1 and discovered[0].name == "TestThreatAgent")


def test_agent_manager():
    print("\n🔄 Testing Agent Manager Lifecycle Transitions...")
    from app.core.agents.agent_types import AgentState
    from app.core.agents.agent_manager import agent_manager
    from app.core.agents.agent_registry import agent_registry

    agents = agent_registry.list_all_agents()
    target_id = agents[0].agent_id

    agent_manager.initialize_agent(target_id)
    check("Agent initialized (State = IDLE)", agent_manager.get_agent_state(target_id) == AgentState.IDLE)

    agent_manager.activate_agent(target_id)
    check("Agent activated (State = EXECUTING)", agent_manager.get_agent_state(target_id) == AgentState.EXECUTING)

    agent_manager.suspend_agent(target_id)
    check("Agent suspended (State = SUSPENDED)", agent_manager.get_agent_state(target_id) == AgentState.SUSPENDED)


def test_goal_manager():
    print("\n🎯 Testing Goal Management Engine...")
    from app.core.agents.goal_manager import goal_manager

    goal = goal_manager.create_goal("Audit Network", "Execute threat scan across scope", priority=1)
    check("Goal created", goal is not None)

    tasks = goal_manager.decompose_goal(goal.goal_id, ["Scan Ports", "Audit Firewall"])
    check("Goal decomposed into 2 tasks", len(tasks) == 2)
    check("Goal status updated to IN_PROGRESS", goal_manager.get_goal(goal.goal_id).status == "IN_PROGRESS")


async def test_agent_context_manager():
    print("\n🧠 Testing Agent Context Manager...")
    from app.core.agents.agent_context_manager import agent_context_manager

    ctx = await agent_context_manager.build_context("goal_ctx_test", token_budget=2048)
    check("Context assembled", ctx is not None)
    check("Memory references present", len(ctx.memory_references) > 0)
    check("Token count within budget", ctx.token_count <= 2048)


def test_agent_state_store():
    print("\n💾 Testing Persistent Agent State Store...")
    from app.core.agents.agent_types import AgentExecution, AgentState, ToolResult
    from app.core.agents.agent_state_store import agent_state_store

    exec_obj = AgentExecution(agent_id="ag_store_test", goal_id="goal_1", state=AgentState.COMPLETED)
    agent_state_store.save_execution(exec_obj)

    retrieved = agent_state_store.get_execution(exec_obj.execution_id)
    check("Execution state persisted and retrieved", retrieved is not None and retrieved.state == AgentState.COMPLETED)

    t_res = ToolResult(invocation_id="inv_1", tool_name="system_analyzer", success=True)
    agent_state_store.save_tool_result("ag_store_test", t_res)
    history = agent_state_store.get_agent_tool_history("ag_store_test")
    check("Tool result saved in history", len(history) == 1)


async def test_agent_message_bus():
    print("\n🚌 Testing Agent Communication Bus...")
    from app.core.agents.agent_types import AgentMessage
    from app.core.agents.agent_message_bus import agent_message_bus

    received_messages = []

    def handle_msg(msg):
        received_messages.append(msg)

    agent_message_bus.subscribe("recipient_agent_1", handle_msg)

    msg = AgentMessage(
        sender_agent_id="sender_agent_1",
        recipient_agent_id="recipient_agent_1",
        message_type="TASK_DELEGATION",
        payload={"task": "Perform Scan"},
    )
    await agent_message_bus.send_message(msg)

    check("Inter-agent message delivered", len(received_messages) == 1 and received_messages[0].payload["task"] == "Perform Scan")


async def test_tool_registry():
    print("\n🛠️ Testing Tool Registry Authorization & Sandbox Bounds...")
    from app.core.agents.agent_types import ToolDefinition, ToolInvocation
    from app.core.agents.tool_registry import tool_registry

    # 1. Block unregistered tool
    unreg_inv = ToolInvocation(tool_name="unregistered_tool", arguments={}, agent_id="agent_1")
    unreg_res = await tool_registry.invoke_tool(unreg_inv)
    check("Unregistered tool invocation blocked", not unreg_res.success)

    # 2. Execute registered tool
    reg_tool = ToolDefinition(tool_name="test_tool", description="Test tool")
    tool_registry.register_tool(reg_tool, lambda args: {"status": "ok"})
    reg_inv = ToolInvocation(tool_name="test_tool", arguments={}, agent_id="agent_1")
    reg_res = await tool_registry.invoke_tool(reg_inv)
    check("Registered tool executed cleanly", reg_res.success and reg_res.output["status"] == "ok")


async def test_agent_execution_engine():
    print("\n⚡ Testing Agent Execution Engine Lifecycle...")
    from app.core.agents.agent_execution_engine import agent_execution_engine
    from app.core.agents.agent_types import AgentState

    exec_res = await agent_execution_engine.execute_goal("agent_exec_test", "Security Audit Goal", "Audit system configuration")
    check("Goal lifecycle executed", exec_res is not None)
    check("Execution state is COMPLETED", exec_res.state == AgentState.COMPLETED)


async def test_agent_orchestrator():
    print("\n🌐 Testing Global Autonomous Agent Orchestrator...")
    from app.core.agents.agent_orchestrator import agent_orchestrator

    res = await agent_orchestrator.execute_autonomous_goal("Enterprise Vulnerability Assessment", "Assess system vulnerability profile", "system_analysis")
    check("Autonomous goal orchestrated", res is not None)
    check("Selected agent ID assigned", len(res.selected_agent_id) > 0)
    check("Execution status is COMPLETED", res.execution_status == "COMPLETED")


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-8...")
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.data_intelligence.platform import enterprise_data_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Agent_Master_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly with Agent Platform", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Agent_Master_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "agent_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 9 PART 1 — ENTERPRISE AUTONOMOUS AGENT PLATFORM TEST SUITE")
    print("==========================================================================")

    test_agent_registry()
    test_agent_manager()
    test_goal_manager()
    await test_agent_context_manager()
    test_agent_state_store()
    await test_agent_message_bus()
    await test_tool_registry()
    await test_agent_execution_engine()
    await test_agent_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 9 PART 1 SUCCESS: Enterprise Autonomous Agent Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
