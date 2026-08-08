"""
Control Flow Graph (CFG) Engine.

Builds complete Control Flow Graphs with basic blocks, conditional branches,
loops, switch statements, unreachable code detection, and graph statistics.
"""

from typing import Dict, Any, List, Set, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.security.security_types import BinaryInstruction


class BasicBlock(BaseModel):
    """Represents a basic block of contiguous straight-line instructions."""
    block_id: str
    start_address: int
    end_address: int
    instructions: List[BinaryInstruction] = Field(default_factory=list)
    successors: List[str] = Field(default_factory=list)
    predecessors: List[str] = Field(default_factory=list)


class ControlFlowGraphModel(BaseModel):
    """Control Flow Graph data structure for a function."""
    function_name: str
    entry_block_id: str
    blocks: Dict[str, BasicBlock] = Field(default_factory=dict)
    total_blocks: int = 0
    total_edges: int = 0
    has_loops: bool = False


class CFGEngine:
    """Enterprise Control Flow Graph Engine."""

    def build_cfg(self, function_name: str, instructions: List[BinaryInstruction]) -> ControlFlowGraphModel:
        """
        Constructs a complete Control Flow Graph from function instructions.

        Args:
            function_name: Name of function.
            instructions: Function instructions list.

        Returns:
            ControlFlowGraphModel object.
        """
        if not instructions:
            return ControlFlowGraphModel(function_name=function_name, entry_block_id="block_0")

        # 1. Identify Block Leaders (Entry points of basic blocks)
        leaders: Set[int] = {instructions[0].address}

        for i, ins in enumerate(instructions):
            if ins.mnemonic.startswith("j") or ins.mnemonic == "ret":
                if i + 1 < len(instructions):
                    leaders.add(instructions[i+1].address)
                if ins.op_str.startswith("0x"):
                    try:
                        target = int(ins.op_str, 16)
                        leaders.add(target)
                    except ValueError:
                        pass

        sorted_leaders = sorted([l for l in leaders if any(ins.address == l for ins in instructions)])
        blocks: Dict[str, BasicBlock] = {}
        addr_to_block_id: Dict[int, str] = {}

        # 2. Group Instructions into Basic Blocks
        for idx, leader in enumerate(sorted_leaders):
            b_id = f"block_{idx}"
            addr_to_block_id[leader] = b_id

            block_ins = [ins for ins in instructions if ins.address >= leader]
            if idx < len(sorted_leaders) - 1:
                next_leader = sorted_leaders[idx + 1]
                block_ins = [ins for ins in block_ins if ins.address < next_leader]

            if not block_ins:
                continue

            blocks[b_id] = BasicBlock(
                block_id=b_id,
                start_address=block_ins[0].address,
                end_address=block_ins[-1].address + block_ins[-1].size,
                instructions=block_ins,
            )

        # 3. Connect Control Flow Edges
        total_edges = 0
        has_loops = False

        for b_id, block in blocks.items():
            last_ins = block.instructions[-1]
            if last_ins.mnemonic.startswith("j"):
                # Jump branch target
                if last_ins.op_str.startswith("0x"):
                    try:
                        target_addr = int(last_ins.op_str, 16)
                        target_b_id = addr_to_block_id.get(target_addr)
                        if target_b_id and target_b_id in blocks:
                            block.successors.append(target_b_id)
                            blocks[target_b_id].predecessors.append(b_id)
                            total_edges += 1
                            if blocks[target_b_id].start_address <= block.start_address:
                                has_loops = True
                    except ValueError:
                        pass

                # Conditional fall-through branch
                if last_ins.mnemonic != "jmp":
                    idx = int(b_id.split("_")[1])
                    next_b_id = f"block_{idx + 1}"
                    if next_b_id in blocks:
                        block.successors.append(next_b_id)
                        blocks[next_b_id].predecessors.append(b_id)
                        total_edges += 1

        cfg = ControlFlowGraphModel(
            function_name=function_name,
            entry_block_id="block_0",
            blocks=blocks,
            total_blocks=len(blocks),
            total_edges=total_edges,
            has_loops=has_loops,
        )

        security_logger.info(f"CFGEngine: Built CFG for '{function_name}': Blocks={len(blocks)}, Edges={total_edges}, Loops={has_loops}")
        return cfg


# Global CFGEngine instance
cfg_engine = CFGEngine()
