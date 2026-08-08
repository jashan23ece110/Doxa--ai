"""
Enterprise Optimization & Resource Allocation Types & Data Schemas.

Comprehensive Pydantic models for OptimizationRequest, OptimizationObjective, OptimizationVariable,
DecisionVariable, Constraint, ConstraintSet, OptimizationModel, OptimizationSolution, FeasibleSolution,
ObjectiveValue, Resource, ResourceAllocation, AllocationPlan, OptimizationScenario, OptimizationTradeoff,
OptimizationExplanation, and OptimizationMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class OptimizationObjective(BaseModel):
    objective_id: str = Field(default_factory=lambda: f"oobj_{uuid.uuid4().hex[:8]}")
    name: str
    direction: str = "MAXIMIZE"  # MAXIMIZE, MINIMIZE
    weight: float = 1.0
    target_metric: str = "NET_BENEFIT"


class OptimizationVariable(BaseModel):
    variable_id: str = Field(default_factory=lambda: f"ovbr_{uuid.uuid4().hex[:8]}")
    name: str
    variable_type: str = "CONTINUOUS"  # CONTINUOUS, INTEGER, BINARY
    lower_bound: float = 0.0
    upper_bound: float = 1000.0
    current_value: float = 0.0


class DecisionVariable(BaseModel):
    var_id: str = Field(default_factory=lambda: f"dvar_{uuid.uuid4().hex[:8]}")
    name: str
    assigned_value: float = 100.0


class Constraint(BaseModel):
    constraint_id: str = Field(default_factory=lambda: f"cnst_{uuid.uuid4().hex[:8]}")
    name: str
    is_hard: bool = True
    expression: str = "x <= 500"
    max_limit: float = 500.0


class ConstraintSet(BaseModel):
    set_id: str = Field(default_factory=lambda: f"cset_{uuid.uuid4().hex[:8]}")
    constraints: List[Constraint] = Field(default_factory=list)


class Resource(BaseModel):
    resource_id: str = Field(default_factory=lambda: f"res_{uuid.uuid4().hex[:8]}")
    name: str  # COMPUTE, BUDGET, WORKFORCE, INFRASTRUCTURE
    total_capacity: float = 1000.0
    allocated_quantity: float = 0.0
    unit: str = "UNITS"


class ResourceAllocation(BaseModel):
    allocation_id: str = Field(default_factory=lambda: f"raloc_{uuid.uuid4().hex[:8]}")
    resource_id: str
    resource_name: str
    allocated_amount: float = 250.0
    target_entity: str = "ComputeService"


class AllocationPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"aplan_{uuid.uuid4().hex[:8]}")
    allocations: List[ResourceAllocation] = Field(default_factory=list)
    total_cost: float = 25000.0
    efficiency_score: float = 0.95


class ObjectiveValue(BaseModel):
    objective_name: str
    value: float = 95.0
    is_optimal: bool = True


class FeasibleSolution(BaseModel):
    solution_id: str = Field(default_factory=lambda: f"fsol_{uuid.uuid4().hex[:8]}")
    variables: List[DecisionVariable] = Field(default_factory=list)
    objective_values: List[ObjectiveValue] = Field(default_factory=list)
    feasibility_score: float = 1.0  # 1.0 = Fully Feasible


class OptimizationSolution(BaseModel):
    solution_id: str = Field(default_factory=lambda: f"osol_{uuid.uuid4().hex[:8]}")
    best_solution: FeasibleSolution
    allocation_plan: AllocationPlan
    solver_status: str = "OPTIMAL"  # OPTIMAL, FEASIBLE, INFEASIBLE, TIMEOUT
    solve_time_ms: float = 0.50
    solved_at: float = Field(default_factory=time.time)


class OptimizationModel(BaseModel):
    model_id: str = Field(default_factory=lambda: f"omod_{uuid.uuid4().hex[:8]}")
    name: str
    paradigm: str = "MIXED_INTEGER_PROGRAMMING"  # LINEAR, INTEGER, MIXED_INTEGER, HEURISTIC
    objectives: List[OptimizationObjective] = Field(default_factory=list)
    constraints: List[Constraint] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class OptimizationScenario(BaseModel):
    scenario_id: str = Field(default_factory=lambda: f"oscen_{uuid.uuid4().hex[:8]}")
    name: str  # BASELINE, RESOURCE_SHORTAGE, DEMAND_SPIKE
    delta_capacity_pct: float = 0.0
    projected_objective_value: float = 95.0


class OptimizationTradeoff(BaseModel):
    tradeoff_id: str = Field(default_factory=lambda: f"otrade_{uuid.uuid4().hex[:8]}")
    objective_a: str
    objective_b: str
    pareto_frontier_points: List[Dict[str, float]] = Field(default_factory=list)


class OptimizationExplanation(BaseModel):
    explanation_id: str = Field(default_factory=lambda: f"oexpl_{uuid.uuid4().hex[:8]}")
    binding_constraints: List[str] = Field(default_factory=list)
    rationale: str = "Solution achieves maximum ROI bounded by $500k budget limit constraint."


class OptimizationRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"oreq_{uuid.uuid4().hex[:8]}")
    title: str
    objectives: List[OptimizationObjective] = Field(default_factory=list)
    resources: List[Resource] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class OptimizationMetrics(BaseModel):
    optimizations_executed_count: int = 0
    resources_managed_count: int = 0
    average_solve_time_ms: float = 0.50
    optimal_solutions_pct: float = 100.0
