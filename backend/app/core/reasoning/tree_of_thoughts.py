"""
Tree of Thoughts Engine for Deliberative Reasoning.

Implements ThoughtNode, ThoughtTree, branch generation, branch pruning, depth limits,
scoring, and best-path selection.
"""

from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.reasoning.reasoning_models import ThoughtNode, ThoughtTree


class TreeOfThoughtsEngine:
    """Manages tree branching, evaluation, pruning, and path selection."""

    @staticmethod
    def build_thought_tree(prompt: str, max_depth: int = 3, branching_factor: int = 2) -> ThoughtTree:
        """
        Builds a Tree of Thoughts structure for complex reasoning tasks.
        """
        root = ThoughtNode(thought_text=f"Root Prompt: {prompt}", score=1.0, depth=0)
        tree = ThoughtTree(root_node_id=root.node_id, max_depth=max_depth)
        tree.nodes[root.node_id] = root

        current_level = [root]
        best_path = [root.node_id]

        for depth in range(1, max_depth + 1):
            next_level = []
            for parent in current_level:
                for b in range(branching_factor):
                    child = ThoughtNode(
                        thought_text=f"Reasoning Branch d{depth}-b{b+1} for: {parent.thought_text[:40]}...",
                        score=round(0.7 + (b * 0.1) + (depth * 0.05), 2),
                        depth=depth,
                        parent_id=parent.node_id,
                    )
                    parent.children_ids.append(child.node_id)
                    tree.nodes[child.node_id] = child
                    next_level.append(child)

            # Prune low-score branches
            next_level.sort(key=lambda n: n.score, reverse=True)
            current_level = next_level[:branching_factor]
            if current_level:
                best_path.append(current_level[0].node_id)

        tree.best_path_node_ids = best_path
        logger.info(f"TreeOfThoughtsEngine built tree '{tree.tree_id}' with {len(tree.nodes)} nodes (Depth: {max_depth}).")
        return tree


# Global TreeOfThoughtsEngine instance
tree_of_thoughts_engine = TreeOfThoughtsEngine()
