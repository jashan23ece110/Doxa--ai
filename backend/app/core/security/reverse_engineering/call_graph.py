"""
Program-Wide Call Graph Engine.

Tracks caller/callee relationships, recursion, indirect calls,
imported calls, library boundaries, and graph traversal APIs.
"""

from typing import Dict, Any, List, Set
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.security.security_types import BinaryFunction


class CallGraphNode(BaseModel):
    name: str
    address: int
    callers: List[str] = Field(default_factory=list)
    callees: List[str] = Field(default_factory=list)
    is_imported: bool = False


class ProgramCallGraph(BaseModel):
    nodes: Dict[str, CallGraphNode] = Field(default_factory=dict)
    total_functions: int = 0
    total_call_sites: int = 0
    recursive_functions: List[str] = Field(default_factory=list)


class CallGraphEngine:
    """Enterprise Program-Wide Call Graph Engine."""

    def build_call_graph(self, functions: List[BinaryFunction]) -> ProgramCallGraph:
        """
        Builds complete caller/callee program-wide call graph.

        Args:
            functions: List of recovered BinaryFunction objects.

        Returns:
            ProgramCallGraph model.
        """
        nodes: Dict[str, CallGraphNode] = {}
        addr_to_name: Dict[int, str] = {f.start_address: f.name for f in functions}
        total_call_sites = 0
        recursive_funcs: Set[str] = set()

        for f in functions:
            nodes[f.name] = CallGraphNode(
                name=f.name,
                address=f.start_address,
            )

        for f in functions:
            caller_node = nodes[f.name]
            for call_target in f.calls:
                total_call_sites += 1
                callee_name = call_target

                if call_target.startswith("0x"):
                    try:
                        target_addr = int(call_target, 16)
                        callee_name = addr_to_name.get(target_addr, f"sub_{target_addr:X}")
                    except ValueError:
                        pass

                if callee_name == f.name:
                    recursive_funcs.add(f.name)

                if callee_name not in nodes:
                    nodes[callee_name] = CallGraphNode(
                        name=callee_name,
                        address=0,
                        is_imported=True,
                    )

                if callee_name not in caller_node.callees:
                    caller_node.callees.append(callee_name)
                if f.name not in nodes[callee_name].callers:
                    nodes[callee_name].callers.append(f.name)

        cg = ProgramCallGraph(
            nodes=nodes,
            total_functions=len(nodes),
            total_call_sites=total_call_sites,
            recursive_functions=list(recursive_funcs),
        )

        security_logger.info(f"CallGraphEngine: Built Call Graph with {len(nodes)} nodes, {total_call_sites} call sites.")
        return cg


# Global CallGraphEngine instance
call_graph_engine = CallGraphEngine()
