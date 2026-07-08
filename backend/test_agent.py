import asyncio
from agent import run_agent_loop, global_traces

async def test():
    goal = "Research our remote work policy and draft a welcome message for new remote employees"
    await run_agent_loop("test_run_1", goal)
    import pprint
    pprint.pprint(global_traces["test_run_1"])

if __name__ == "__main__":
    asyncio.run(test())
