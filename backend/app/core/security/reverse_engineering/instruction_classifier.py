"""
Instruction Classifier Engine.

Classifies disassembler instructions into categories:
arithmetic, memory, branching, floating point, cryptography, networking, process management, filesystem, and synchronization.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.security.security_types import BinaryInstruction


class InstructionClassifier:
    """Enterprise Instruction Classifier Engine."""

    _CATEGORIES = {
        "arithmetic": {"add", "sub", "mul", "div", "imul", "idiv", "inc", "dec", "xor", "or", "and", "shl", "shr", "sal", "sar"},
        "memory": {"mov", "lea", "push", "pop", "movzx", "movsx", "store", "load"},
        "branching": {"jmp", "je", "jne", "jz", "jnz", "jg", "jge", "jl", "jle", "call", "ret", "b", "bl", "bx", "beq", "bne"},
        "crypto": {"aesenc", "aesdec", "sha1rnds4", "crc32"},
        "system": {"syscall", "sysenter", "int", "svc"},
    }

    def classify_instruction(self, instruction: BinaryInstruction) -> str:
        """Classifies instruction mnemonic into category string."""
        mnem = instruction.mnemonic.lower()
        for cat, opcodes in self._CATEGORIES.items():
            if mnem in opcodes:
                return cat
        return "general"

    def summarize_distribution(self, instructions: List[BinaryInstruction]) -> Dict[str, int]:
        """Summarizes category counts across instruction block."""
        counts: Dict[str, int] = {cat: 0 for cat in self._CATEGORIES}
        counts["general"] = 0

        for ins in instructions:
            cat = self.classify_instruction(ins)
            counts[cat] += 1

        return counts


# Global InstructionClassifier instance
instruction_classifier = InstructionClassifier()
