import sys
import io
import math
import multiprocessing
import traceback
from typing import Dict, Any

def _run_in_sandbox(code_str: str, queue: multiprocessing.Queue):
    """
    Worker function meant to run inside a separate, isolated process.
    Redirects stdout/stderr and executes restricted code, sending results back via Queue.
    """
    # Redirect output streams
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = buffer_out = io.StringIO()
    sys.stderr = buffer_err = io.StringIO()

    try:
        # Whitelisted safe builtins
        safe_builtins = {
            "abs": abs,
            "all": all,
            "any": any,
            "bin": bin,
            "bool": bool,
            "chr": chr,
            "dict": dict,
            "divmod": divmod,
            "enumerate": enumerate,
            "float": float,
            "format": format,
            "hash": hash,
            "hex": hex,
            "id": id,
            "int": int,
            "isinstance": isinstance,
            "issubclass": issubclass,
            "len": len,
            "list": list,
            "map": map,
            "max": max,
            "min": min,
            "next": next,
            "oct": oct,
            "ord": ord,
            "pow": pow,
            "print": print,
            "range": range,
            "repr": repr,
            "reversed": reversed,
            "round": round,
            "set": set,
            "slice": slice,
            "sorted": sorted,
            "str": str,
            "sum": sum,
            "tuple": tuple,
            "type": type,
            "zip": zip,
        }

        # Safe math functions mapping
        safe_math = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "radians": math.radians,
            "degrees": math.degrees
        }

        # restricted environment dictionary
        sandbox_globals = {
            "__builtins__": safe_builtins,
            "math": math,
            **safe_math
        }

        # Execute
        exec(code_str, sandbox_globals, {})
        
        stdout_val = buffer_out.getvalue()
        stderr_val = buffer_err.getvalue()
        
        queue.put({
            "success": True,
            "stdout": stdout_val,
            "stderr": stderr_val
        })
    except Exception as e:
        queue.put({
            "success": False,
            "error": "".join(traceback.format_exception_only(type(e), e)).strip()
        })
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def execute_python_code(code: str) -> str:
    """
    Executes a snippet of Python code in a restricted sandbox process.
    Times out and terminates execution if it runs for more than 4 seconds.
    """
    if not code.strip():
        return "Error: Empty script provided."

    # Process communication queue
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_run_in_sandbox, args=(code, queue))
    
    try:
        process.start()
        # Wait up to 4 seconds
        process.join(timeout=4.0)
        
        if process.is_alive():
            # Terminate running process on timeout
            process.terminate()
            process.join()
            return "Execution Timeout Error: Code took too long to execute (> 4.0 seconds) and was terminated."
            
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
        if process.is_alive():
            process.terminate()
            process.join()
        return f"Sandbox execution manager error: {str(e)}"
