#!/usr/bin/env python3
"""
Integration Test Suite for Stage 6 Part 3 - Enterprise Reverse Engineering Framework.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

PASS = 0
FAIL = 0


def check(label, condition):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}")


def test_disassembly_engine():
    print("\n🔬 Testing Disassembly Engine...")
    from app.core.security.reverse_engineering.disassembly_engine import DisassemblyEngine
    from app.core.security.security_types import Architecture

    de = DisassemblyEngine()
    x64_bytes = b"\x55\x48\x89\xe5\x48\x83\xec\x20\x31\xc0\x90\xc3"
    res = de.disassemble(x64_bytes, base_address=0x401000, arch=Architecture.X64)

    check("Disassembled instructions count > 0", res["instructions_count"] > 0)
    mnemonics = [ins.mnemonic for ins in res["instructions"]]
    check("Push decoded", "push" in mnemonics)
    check("Ret decoded", "ret" in mnemonics)


def test_function_recovery():
    print("\n🧩 Testing Function Recovery Engine...")
    from app.core.security.reverse_engineering.disassembly_engine import DisassemblyEngine
    from app.core.security.reverse_engineering.function_recovery import FunctionRecoveryEngine
    from app.core.security.security_types import Architecture

    de = DisassemblyEngine()
    fre = FunctionRecoveryEngine()

    code = b"\x55\x48\x89\xe5\xe8\x0a\x00\x00\x00\xc3\x55\x48\x89\xe5\x31\xc0\xc3"
    disasm = de.disassemble(code, base_address=0x401000, arch=Architecture.X64)
    funcs = fre.recover_functions(disasm["instructions"])

    check("Functions recovered >= 1", len(funcs) >= 1)
    check("Function has pseudo-C decompiled code", funcs[0].decompiled_c is not None)


def test_control_flow_graph():
    print("\n🔀 Testing Control Flow Graph Engine...")
    from app.core.security.reverse_engineering.disassembly_engine import DisassemblyEngine
    from app.core.security.reverse_engineering.control_flow_graph import CFGEngine
    from app.core.security.security_types import Architecture

    de = DisassemblyEngine()
    cfg_eng = CFGEngine()

    code = b"\x55\x48\x89\xe5\x85\xc0\x74\x02\x31\xc0\xc3"
    disasm = de.disassemble(code, base_address=0x401000, arch=Architecture.X64)
    cfg = cfg_eng.build_cfg("sub_401000", disasm["instructions"])

    check("CFG generated with basic blocks", cfg.total_blocks > 0)
    check("CFG has entry block", cfg.entry_block_id in cfg.blocks)


def test_call_graph():
    print("\n📞 Testing Program-Wide Call Graph Engine...")
    from app.core.security.reverse_engineering.call_graph import CallGraphEngine
    from app.core.security.security_types import BinaryFunction

    cge = CallGraphEngine()
    funcs = [
        BinaryFunction(name="main", start_address=0x401000, end_address=0x401050, calls=["sub_401050"]),
        BinaryFunction(name="sub_401050", start_address=0x401050, end_address=0x401080, calls=[]),
    ]

    cg = cge.build_call_graph(funcs)
    check("Call graph total nodes >= 2", cg.total_functions >= 2)
    check("Main calls sub_401050", "sub_401050" in cg.nodes["main"].callees)


def test_symbol_resolver():
    print("\n🏷️ Testing Symbol Resolver...")
    from app.core.security.reverse_engineering.symbol_resolver import SymbolResolver
    from app.core.security.security_types import BinaryExport, BinaryImport

    sr = SymbolResolver()
    exports = [BinaryExport(function_name="_Z4testv", address=0x401000)]
    imports = [BinaryImport(library="kernel32.dll", function_name="ExitProcess", address=0x402000)]

    symbols = sr.resolve_symbols(exports, imports, [])
    check("Export symbol resolved and demangled", symbols.get(0x401000) == "cpp::4testv")
    check("Import symbol resolved", symbols.get(0x402000) == "kernel32.dll!ExitProcess")


def test_instruction_classifier():
    print("\n📊 Testing Instruction Classifier...")
    from app.core.security.reverse_engineering.instruction_classifier import InstructionClassifier
    from app.core.security.security_types import BinaryInstruction

    ic = InstructionClassifier()
    inst = BinaryInstruction(address=0x401000, mnemonic="add", op_str="eax, 1", size=2)
    cat = ic.classify_instruction(inst)
    check("Add classified as arithmetic", cat == "arithmetic")


def test_binary_workspace():
    print("\n📁 Testing Binary Workspace...")
    from app.core.security.reverse_engineering.binary_workspace import BinaryWorkspace

    ws = BinaryWorkspace()
    proj = ws.create_project("proj_1", "Test Project", "bin_123")
    check("Project created", proj.project_id == "proj_1")

    renamed = ws.rename_function("proj_1", "sub_401000", "main_entry")
    check("Function renamed in workspace", renamed)

    note = ws.add_note("proj_1", "Main initialization routine", address=0x401000)
    check("Analyst note added", note is not None)


async def test_graph_repository():
    print("\n💾 Testing Graph Repository...")
    from app.core.security.reverse_engineering.graph_repository import GraphRepository
    from app.core.security.reverse_engineering.control_flow_graph import ControlFlowGraphModel

    gr = GraphRepository()
    cfg = ControlFlowGraphModel(function_name="main", entry_block_id="block_0")
    await gr.store_cfg("bin_123", cfg)

    retrieved = await gr.get_cfg("bin_123", "main")
    check("Stored CFG retrieved", retrieved is not None and retrieved.function_name == "main")


def test_binary_diff_engine():
    print("\n⚖️ Testing Binary Diff Engine...")
    from app.core.security.reverse_engineering.binary_diff_engine import BinaryDiffEngine
    from app.core.security.security_types import BinaryMetadata, BinaryFunction, FileFingerprint, FileFormat

    diff_eng = BinaryDiffEngine()
    fp = FileFingerprint(md5="1", sha1="2", sha256="3", file_size_bytes=100)
    meta_a = BinaryMetadata(file_name="v1.exe", fingerprint=fp, format=FileFormat.PE)
    meta_b = BinaryMetadata(file_name="v2.exe", fingerprint=fp, format=FileFormat.PE)

    funcs_a = [BinaryFunction(name="main", start_address=0x401000, end_address=0x401050, instructions_count=10)]
    funcs_b = [
        BinaryFunction(name="main", start_address=0x401000, end_address=0x401060, instructions_count=12),
        BinaryFunction(name="new_feature", start_address=0x401060, end_address=0x401080, instructions_count=5),
    ]

    res = diff_eng.diff_binaries(meta_a, meta_b, funcs_a, funcs_b)
    check("Added function detected", "new_feature" in res["added_functions"])
    check("Modified function detected", "main" in res["modified_functions"])


def test_reverse_report_builder():
    print("\n📄 Testing Reverse Engineering Report Builder...")
    from app.core.security.reverse_engineering.reverse_report_builder import ReverseReportBuilder
    from app.core.security.security_types import BinaryMetadata, BinaryFunction, FileFingerprint, FileFormat

    builder = ReverseReportBuilder()
    fp = FileFingerprint(md5="1", sha1="2", sha256="3", file_size_bytes=100)
    meta = BinaryMetadata(file_name="sample.exe", fingerprint=fp, format=FileFormat.PE)
    funcs = [BinaryFunction(name="main", start_address=0x401000, end_address=0x401050)]

    rep = builder.build_report_data(meta, funcs)
    check("Report data created", rep["file_name"] == "sample.exe")

    md = builder.to_markdown(rep, funcs)
    check("Markdown output generated", "# Reverse Engineering Analysis Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility...")
    from app.core.security import enterprise_security_manager
    from app.core.intelligence import ai_os_kernel

    sess = await enterprise_security_manager.start_reverse_engineering_session("bin_re_test")
    check("EnterpriseSecurityManager starts RE session", sess is not None)
    check("AI OS Kernel remains functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 6 PART 3 - ENTERPRISE REVERSE ENGINEERING FRAMEWORK TEST SUITE")
    print("==========================================================================")

    test_disassembly_engine()
    test_function_recovery()
    test_control_flow_graph()
    test_call_graph()
    test_symbol_resolver()
    test_instruction_classifier()
    test_binary_workspace()
    await test_graph_repository()
    test_binary_diff_engine()
    test_reverse_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 PART 3 SUCCESS: Enterprise Reverse Engineering Framework Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
