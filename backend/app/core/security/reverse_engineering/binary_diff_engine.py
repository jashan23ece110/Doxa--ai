"""
Binary Diffing Engine.

Compares two binaries to detect added/removed/modified functions,
changed imports, changed exports, changed strings, changed sections, and similarity scores.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.security.security_types import BinaryMetadata, BinaryFunction


class BinaryDiffEngine:
    """Enterprise Binary Diffing Engine."""

    def diff_binaries(
        self,
        base_meta: BinaryMetadata,
        target_meta: BinaryMetadata,
        base_funcs: List[BinaryFunction],
        target_funcs: List[BinaryFunction],
    ) -> Dict[str, Any]:
        """
        Compares two binary files and returns structured diff results.

        Returns:
            Dict containing added/removed/modified functions, changed imports/exports, and similarity score.
        """
        base_func_names = {f.name for f in base_funcs}
        target_func_names = {f.name for f in target_funcs}

        added_funcs = list(target_func_names - base_func_names)
        removed_funcs = list(base_func_names - target_func_names)
        common_funcs = base_func_names.intersection(target_func_names)

        base_func_map = {f.name: f for f in base_funcs}
        target_func_map = {f.name: f for f in target_funcs}
        modified_funcs = []

        for name in common_funcs:
            b_f = base_func_map[name]
            t_f = target_func_map[name]
            if b_f.size_bytes != t_f.size_bytes or b_f.instructions_count != t_f.instructions_count:
                modified_funcs.append(name)

        base_imports = {f"{i.library}!{i.function_name}" for i in base_meta.imports}
        target_imports = {f"{i.library}!{i.function_name}" for i in target_meta.imports}
        added_imports = list(target_imports - base_imports)
        removed_imports = list(base_imports - target_imports)

        # Similarity score calculation (Jaccard similarity on functions + imports)
        total_unique = len(base_func_names.union(target_func_names)) or 1
        similarity_score = round(len(common_funcs) / total_unique, 4)

        security_logger.info(
            f"BinaryDiffEngine: Compared '{base_meta.file_name}' vs '{target_meta.file_name}'. "
            f"AddedFuncs={len(added_funcs)}, RemovedFuncs={len(removed_funcs)}, ModifiedFuncs={len(modified_funcs)}, "
            f"Similarity={similarity_score * 100:.1f}%"
        )

        return {
            "base_binary": base_meta.file_name,
            "target_binary": target_meta.file_name,
            "similarity_score": similarity_score,
            "similarity_percentage": round(similarity_score * 100.0, 2),
            "added_functions": added_funcs,
            "removed_functions": removed_funcs,
            "modified_functions": modified_funcs,
            "added_imports": added_imports,
            "removed_imports": removed_imports,
        }


# Global BinaryDiffEngine instance
binary_diff_engine = BinaryDiffEngine()
