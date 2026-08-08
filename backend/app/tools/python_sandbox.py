"""
Python Code Subprocess Execution Sandbox Tool.

Runs Python snippets safely in isolated subprocesses without blocking the event loop.
Validates input parameter limits and enforces strict timeouts.
"""

import sys
import io
import math
import asyncio
import multiprocessing
import traceback
from app.core.config import settings
from app.core.logging import logger
from app.core.security import ToolValidator


def _run_in_sandbox(code_str: str, queue: multiprocessing.Queue):
    """Worker function executing code inside an isolated subprocess."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = buffer_out = io.StringIO()
    sys.stderr = buffer_err = io.StringIO()

    try:
        safe_builtins = {
            "abs": abs, "all": all, "any": any, "bin": bin, "bool": bool,
            "chr": chr, "dict": dict, "divmod": divmod, "enumerate": enumerate,
            "float": float, "format": format, "hash": hash, "hex": hex, "id": id,
            "int": int, "isinstance": isinstance, "issubclass": issubclass,
            "len": len, "list": list, "map": map, "max": max, "min": min,
            "next": next, "oct": oct, "ord": ord, "pow": pow, "print": print,
            "range": range, "repr": repr, "reversed": reversed, "round": round,
            "set": set, "slice": slice, "sorted": sorted, "str": str,
            "sum": sum, "tuple": tuple, "type": type, "zip": zip,
        }

        safe_math = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "pi": math.pi, "e": math.e,
            "radians": math.radians, "degrees": math.degrees,
        }

        sandbox_globals = {
            "__builtins__": safe_builtins,
            "math": math,
            **safe_math,
        }

        exec(code_str, sandbox_globals, {})

        stdout_val = buffer_out.getvalue()
        stderr_val = buffer_err.getvalue()

        queue.put({
            "success": True,
            "stdout": stdout_val,
            "stderr": stderr_val,
        })
    except Exception as e:
        queue.put({
            "success": False,
            "error": "".join(traceback.format_exception_only(type(e), e)).strip(),
        })
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def _sync_execute_python_code(code: str) -> str:
    """Synchronous core sandbox process join."""
    try:
        clean_code = ToolValidator.validate_python_code(code)
    except Exception as err:
        return f"Execution Validation Error: {str(err)}"

    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_run_in_sandbox, args=(clean_code, queue))

    timeout = settings.SANDBOX_TIMEOUT_SECONDS

    try:
        process.start()
        process.join(timeout=timeout)

        if process.is_alive():
            process.terminate()
            process.join()
            logger.warning(f"Python sandbox process timed out (> {timeout}s)")
            return f"Execution Timeout Error: Code took too long to execute (> {timeout} seconds) and was terminated."

        if not queue.empty():
            res = queue.get()
            if res.get("success"):
                stdout = res.get("stdout", "").strip()
                stderr = res.get("stderr", "").strip()
                output = []
                if stdout:
                    output.append(f"Standard Output:\n{stdout}")
                if stderr:
                    output.append(f"Standard Error:\n{stderr}")

                if not output:
                    return "Execution completed successfully with no output returned."
                return "\n\n".join(output)
            else:
                return f"Execution failed:\n{res.get('error')}"
        else:
            return "Execution failed: Sandbox process closed prematurely with no response."

    except Exception as e:
        logger.error(f"Sandbox manager error: {e}")
        if process.is_alive():
            process.terminate()
            process.join()
        return f"Sandbox execution manager error: {str(e)}"


def execute_python_code(code: str) -> str:
    """Executes Python code in an isolated subprocess (sync fallback)."""
    return _sync_execute_python_code(code)


async def execute_python_code_async(code: str) -> str:
    """Executes Python code off the main asyncio event loop thread."""
    return await asyncio.to_thread(_sync_execute_python_code, code)
