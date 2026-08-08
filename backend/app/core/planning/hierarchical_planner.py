"""
Hierarchical Planner for Enterprise Planning & Reasoning Engine.

Generates multi-level plans (Mission -> Objectives -> Tasks -> Subtasks -> Actions)
with priorities, dependencies, estimated durations, and tool requirements.
"""

from typing import List, Dict, Any
from app.core.planning.planning_models import (
    Goal,
    Objective,
    Task,
    SubTask,
    Action,
    Dependency,
    Plan,
    TaskStatus,
)


class HierarchicalPlanner:
    """Generates multi-level hierarchical plan trees."""

    @staticmethod
    def generate_hierarchical_plan(goal: Goal) -> Plan:
        """Constructs a multi-level hierarchical plan tree from a Goal graph."""
        objectives: List[Objective] = []
        dependencies: List[Dependency] = []

        if goal.complexity == "simple":
            # Single Objective, 1 Task
            t1 = Task(
                name="Direct Goal Execution",
                description=f"Execute query: {goal.description}",
                priority=1,
                required_tools=goal.required_tools,
                subtasks=[
                    SubTask(
                        name="Process Input & Respond",
                        actions=[Action(name="Generate Direct Answer")],
                    )
                ],
            )
            obj1 = Objective(title="Process Simple Query", tasks=[t1])
            objectives.append(obj1)

        elif goal.complexity in ("complex", "coding"):
            # 2 Objectives: Architecture & Code Execution
            t1 = Task(
                name="Architecture & Schema Design",
                description="Design modular component architecture and interfaces.",
                priority=1,
                subtasks=[SubTask(name="Draft Spec", actions=[Action(name="Create Component Model")])],
            )
            t2 = Task(
                name="Implementation & Code Generation",
                description="Implement source code following specifications.",
                priority=2,
                dependencies=[t1.task_id],
                required_tools=goal.required_tools,
                subtasks=[SubTask(name="Write Code", actions=[Action(name="Execute Code Syntax Validation")])],
            )
            t3 = Task(
                name="Verification & Refinement",
                description="Audit generated code and verify edge cases.",
                priority=3,
                dependencies=[t2.task_id],
                subtasks=[SubTask(name="Run Tests", actions=[Action(name="Perform Code Audit")])],
            )

            dependencies.append(Dependency(source_task_id=t1.task_id, target_task_id=t2.task_id))
            dependencies.append(Dependency(source_task_id=t2.task_id, target_task_id=t3.task_id))

            obj1 = Objective(title="Design & Architecture", tasks=[t1])
            obj2 = Objective(title="Implementation & Verification", tasks=[t2, t3])
            objectives.append(obj1)
            objectives.append(obj2)

        else: # Research / Default
            # Multi-level Research Objectives
            t1 = Task(
                name="Information Retrieval & Search",
                description="Gather relevant documents and search context.",
                priority=1,
                required_tools=["web_search", "document_search"],
                subtasks=[SubTask(name="Execute Hybrid Search", actions=[Action(name="Query Chroma & Web")])],
            )
            t2 = Task(
                name="Evidence Analysis & Synthesis",
                description="Analyze facts and synthesize cohesive answer.",
                priority=2,
                dependencies=[t1.task_id],
                subtasks=[SubTask(name="Reason & Verify", actions=[Action(name="Construct Final Output")])],
            )

            dependencies.append(Dependency(source_task_id=t1.task_id, target_task_id=t2.task_id))

            obj1 = Objective(title="Context Gathering", tasks=[t1])
            obj2 = Objective(title="Synthesis & Verification", tasks=[t2])
            objectives.append(obj1)
            objectives.append(obj2)

        return Plan(goal=goal, objectives=objectives, dependencies=dependencies)


# Global HierarchicalPlanner instance
hierarchical_planner = HierarchicalPlanner()
