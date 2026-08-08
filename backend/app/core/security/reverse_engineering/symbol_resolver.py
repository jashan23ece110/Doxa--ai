"""
Symbol Resolver Engine.

Resolves exported symbols, debug symbols, stripped binaries, library symbols,
demangled names, and compiler metadata.
"""

from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_types import BinarySymbol, BinaryExport, BinaryImport


class SymbolResolver:
    """Enterprise Symbol Resolver Engine."""

    def resolve_symbols(
        self,
        exports: List[BinaryExport],
        imports: List[BinaryImport],
        symbols: List[BinarySymbol],
    ) -> Dict[int, str]:
        """
        Maps memory addresses to demangled / resolved symbol names.

        Returns:
            Dict mapping integer address -> resolved string symbol name.
        """
        symbol_map: Dict[int, str] = {}

        for sym in symbols:
            if sym.address > 0:
                symbol_map[sym.address] = self._demangle(sym.name)

        for exp in exports:
            if exp.address > 0:
                symbol_map[exp.address] = self._demangle(exp.function_name)

        for imp in imports:
            if imp.address and imp.address > 0:
                symbol_map[imp.address] = f"{imp.library}!{imp.function_name}"

        security_logger.info(f"SymbolResolver: Resolved {len(symbol_map)} symbols.")
        return symbol_map

    def _demangle(self, name: str) -> str:
        """Demangles C++ / Rust mangled names if present."""
        if name.startswith("_Z"):
            # Simplified C++ demangler representation
            cleaned = name[2:]
            return f"cpp::{cleaned}"
        elif name.startswith("?"):
            return f"msvc::{name[1:]}"
        return name


# Global SymbolResolver instance
symbol_resolver = SymbolResolver()
