import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agent import run_agent_loop, get_trace

async def test_python_sandbox():
    print("\n=== Testing Python Sandbox Tool Calling ===")
    run_id = "test_python_run"
    goal = "Write a python script to sort a list of numbers [34, 12, 89, 5] and execute it to print the result."
    try:
        await run_agent_loop(run_id, goal, language="english", mode="agentic")
        trace = get_trace(run_id)
        print("Status:", trace.get("status"))
        print("Steps taken:")
        for step in trace.get("steps", []):
            print(f"- {step.get('step')} ({step.get('tool_used')}): {step.get('output')[:250]}")
        print("\nFinal Result:\n", trace.get("final_result"))
    except Exception as e:
        print(f"FAILED: Python sandbox test failed with error: {e}")

async def test_calendar():
    print("\n=== Testing Calendar Tool Calling ===")
    run_id = "test_calendar_run"
    goal = "What are my upcoming meetings? Create a meeting named 'Doxa Dinner' for 2026-07-25T19:30:00."
    try:
        await run_agent_loop(run_id, goal, language="english", mode="agentic")
        trace = get_trace(run_id)
        print("Status:", trace.get("status"))
        print("Steps taken:")
        for step in trace.get("steps", []):
            print(f"- {step.get('step')} ({step.get('tool_used')}): {step.get('output')[:250]}")
        print("\nFinal Result:\n", trace.get("final_result"))
    except Exception as e:
        print(f"FAILED: Calendar test failed with error: {e}")

async def test_timer():
    print("\n=== Testing Timer Tool Calling ===")
    run_id = "test_timer_run"
    goal = "Set a timer for 10 seconds named 'Doxa Alert test'."
    try:
        await run_agent_loop(run_id, goal, language="english", mode="agentic")
        trace = get_trace(run_id)
        print("Status:", trace.get("status"))
        print("Steps taken:")
        for step in trace.get("steps", []):
            print(f"- {step.get('step')} ({step.get('tool_used')}): {step.get('output')[:250]}")
        print("\nFinal Result:\n", trace.get("final_result"))
    except Exception as e:
        print(f"FAILED: Timer test failed with error: {e}")

async def main():
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set.")
        sys.exit(1)
    await test_python_sandbox()
    await test_calendar()
    await test_timer()

if __name__ == "__main__":
    asyncio.run(main())
