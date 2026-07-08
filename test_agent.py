import asyncio
import os
import sys

# Add backend dir to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from dotenv import load_dotenv
load_dotenv("backend/.env")

from backend.agent import run_agent_loop, global_traces

async def main():
    print("Testing agent loop...")
    run_id = "test-run-123"
    goal = "Research our remote work policy and draft a welcome message for new remote employees"
    
    task = asyncio.create_task(run_agent_loop(run_id, goal))
    
    while True:
        trace = global_traces.get(run_id)
        if trace:
            status = trace.get("status")
            print(f"Status: {status}")
            if status in ["completed", "failed"]:
                print("Final Trace:")
                import json
                print(json.dumps(trace, indent=2))
                break
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
