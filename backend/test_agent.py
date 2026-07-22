import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agent import run_agent_loop, get_trace

async def test_search():
    print("\n=== Testing Web Search Tool Calling ===")
    run_id = "test_search_run"
    goal = "what is the latest news today"
    try:
        await run_agent_loop(run_id, goal, language="english", mode="agentic")
        trace = get_trace(run_id)
        print("Status:", trace.get("status"))
        print("Steps taken:")
        for step in trace.get("steps", []):
            print(f"- {step.get('step')} ({step.get('tool_used')}): {step.get('output')[:150]}")
        print("\nFinal Result:\n", trace.get("final_result"))
        print("Self-check check_content:\n", trace.get("self_check"))
    except Exception as e:
        print(f"FAILED: Search test failed with error: {e}")

async def test_calculator():
    print("\n=== Testing Calculator Tool Calling ===")
    run_id = "test_calc_run"
    goal = "what is 4529 * 93"
    try:
        await run_agent_loop(run_id, goal, language="english", mode="agentic")
        trace = get_trace(run_id)
        print("Status:", trace.get("status"))
        print("Steps taken:")
        for step in trace.get("steps", []):
            print(f"- {step.get('step')} ({step.get('tool_used')}): {step.get('output')[:150]}")
        print("\nFinal Result:\n", trace.get("final_result"))
        print("Self-check check_content:\n", trace.get("self_check"))
    except Exception as e:
        print(f"FAILED: Calculator test failed with error: {e}")

async def main():
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set.")
        sys.exit(1)
    await test_search()
    await test_calculator()

if __name__ == "__main__":
    asyncio.run(main())
