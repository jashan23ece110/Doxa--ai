"""
Enterprise Reverse Engineering & Binary Intelligence Framework Package Initialization.
"""

from app.core.security.reverse_engineering.disassembly_engine import (
    disassembly_engine,
    DisassemblyEngine,
    BaseDisassembler,
    X86X64Disassembler,
    ARMDisassembler,
    GenericDisassembler,
)
from app.core.security.reverse_engineering.function_recovery import (
    function_recovery_engine,
    FunctionRecoveryEngine,
)
from app.core.security.reverse_engineering.control_flow_graph import (
    cfg_engine,
    CFGEngine,
    BasicBlock,
    ControlFlowGraphModel,
)
from app.core.security.reverse_engineering.call_graph import (
    call_graph_engine,
    CallGraphEngine,
    CallGraphNode,
    ProgramCallGraph,
)
from app.core.security.reverse_engineering.symbol_resolver import (
    symbol_resolver,
    SymbolResolver,
)
from app.core.security.reverse_engineering.instruction_classifier import (
    instruction_classifier,
    InstructionClassifier,
)
from app.core.security.reverse_engineering.binary_workspace import (
    binary_workspace,
    BinaryWorkspace,
    REProject,
    AnalystNote,
)
from app.core.security.reverse_engineering.graph_repository import (
    graph_repository,
    GraphRepository,
)
from app.core.security.reverse_engineering.binary_diff_engine import (
    binary_diff_engine,
    BinaryDiffEngine,
)
from app.core.security.reverse_engineering.reverse_report_builder import (
    reverse_report_builder,
    ReverseReportBuilder,
)

__all__ = [
    "disassembly_engine",
    "DisassemblyEngine",
    "BaseDisassembler",
    "X86X64Disassembler",
    "ARMDisassembler",
    "GenericDisassembler",
    "function_recovery_engine",
    "FunctionRecoveryEngine",
    "cfg_engine",
    "CFGEngine",
    "BasicBlock",
    "ControlFlowGraphModel",
    "call_graph_engine",
    "CallGraphEngine",
    "CallGraphNode",
    "ProgramCallGraph",
    "symbol_resolver",
    "SymbolResolver",
    "instruction_classifier",
    "InstructionClassifier",
    "binary_workspace",
    "BinaryWorkspace",
    "REProject",
    "AnalystNote",
    "graph_repository",
    "GraphRepository",
    "binary_diff_engine",
    "BinaryDiffEngine",
    "reverse_report_builder",
    "ReverseReportBuilder",
]
