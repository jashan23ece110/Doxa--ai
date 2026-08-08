"""
Safe Mathematical Calculator Tool with Parameter Sanitization.
"""

import ast
import operator
from typing import Dict, Any
from app.core.logging import logger
from app.core.security import ToolValidator


class MathEvaluator(ast.NodeVisitor):
    """AST node visitor evaluating safe arithmetic expressions."""

    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def visit_BinOp(self, node: ast.BinOp) -> float:
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in self.ALLOWED_OPERATORS:
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise ValueError("Division by zero")
            if op_type == ast.Pow and right > 1000:
                raise ValueError("Exponent too large")
            return self.ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type.__name__}")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> float:
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in self.ALLOWED_OPERATORS:
            return self.ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    def visit_Constant(self, node: ast.Constant) -> float:
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    def generic_visit(self, node: ast.AST) -> float:
        raise ValueError(f"Unsupported AST node: {type(node).__name__}")


def calculate(expression: str) -> str:
    """Safely evaluates a mathematical expression string."""
    try:
        clean_expr = ToolValidator.validate_calculator_expression(expression)
        logger.info(f"Evaluating math expression: '{clean_expr}'")
        parsed = ast.parse(clean_expr, mode="eval")
        evaluator = MathEvaluator()
        result = evaluator.visit(parsed.body)
        return str(result)
    except Exception as e:
        logger.error(f"Calculator evaluation error for expression '{expression}': {e}")
        return f"Calculation Error: {str(e)}"
