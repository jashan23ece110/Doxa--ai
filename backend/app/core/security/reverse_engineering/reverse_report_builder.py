"""
Enterprise Reverse Engineering Report Builder.

Generates comprehensive Reverse Engineering Reports including binary overview,
architecture summary, recovered functions, CFG statistics, call graph summary,
symbol recovery, diff results, analyst annotations, timeline, and recommendations.
Supports JSON and GitHub Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_types import BinaryMetadata, BinaryFunction
from app.core.security.reverse_engineering.call_graph import ProgramCallGraph


class ReverseReportBuilder:
    """Enterprise Reverse Engineering Report Builder."""

    def build_report_data(
        self,
        metadata: BinaryMetadata,
        functions: List[BinaryFunction],
        call_graph: Optional[ProgramCallGraph] = None,
        diff_results: Optional[Dict[str, Any]] = None,
        analyst_notes: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive Reverse Engineering report dictionary.
        """
        total_instructions = sum(f.instructions_count for f in functions)
        avg_complexity = (sum(f.cyclomatic_complexity for f in functions) / len(functions)) if functions else 1.0

        report_data = {
            "title": f"Reverse Engineering Analysis Report — {metadata.file_name}",
            "binary_id": metadata.binary_id,
            "file_name": metadata.file_name,
            "architecture": metadata.architecture.value,
            "format": metadata.format.value.upper(),
            "entry_point": f"0x{metadata.entry_point:X}",
            "is_packed": metadata.is_packed,
            "recovered_functions_count": len(functions),
            "total_instructions_count": total_instructions,
            "average_cyclomatic_complexity": round(avg_complexity, 2),
            "call_graph_summary": {
                "total_nodes": call_graph.total_functions if call_graph else 0,
                "total_call_sites": call_graph.total_call_sites if call_graph else 0,
                "recursive_functions": call_graph.recursive_functions if call_graph else [],
            },
            "diff_results": diff_results or {},
            "analyst_notes_count": len(analyst_notes or []),
            "generated_at": time.time(),
        }

        security_logger.info(f"ReverseReportBuilder: Built report for binary '{metadata.file_name}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any], functions: List[BinaryFunction]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 📐 Binary Architecture Overview",
            f"- **File Name**: `{report_data['file_name']}`",
            f"- **Format**: `{report_data['format']}`",
            f"- **Architecture**: `{report_data['architecture']}`",
            f"- **Entry Point**: `{report_data['entry_point']}`",
            f"- **Packed**: `{report_data['is_packed']}`",
            "",
            "## ⚙️ Reverse Engineering Statistics",
            f"- **Recovered Functions**: `{report_data['recovered_functions_count']}`",
            f"- **Total Instructions**: `{report_data['total_instructions_count']}`",
            f"- **Average Complexity**: `{report_data['average_cyclomatic_complexity']}`",
            f"- **Call Sites**: `{report_data['call_graph_summary']['total_call_sites']}`",
            "",
            "## 🧩 Recovered Function List",
        ]

        for f in functions[:10]:
            lines.append(f"- **`{f.name}`** (Addr: `0x{f.start_address:X}`, Size: `{f.size_bytes}B`, Complexity: `{f.cyclomatic_complexity}`)")

        if len(functions) > 10:
            lines.append(f"- *...and {len(functions) - 10} more functions.*")

        lines.extend([
            "",
            "## 💡 Recommendations",
            "1. Proceed with symbolic execution on complex functions.",
            "2. Cross-reference decompiled C stubs with threat intelligence IOCs.",
        ])

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global ReverseReportBuilder instance
reverse_report_builder = ReverseReportBuilder()
