import math

def calculate(expression: str) -> str:
    """
    Safely evaluates a basic mathematical expression.
    Supports basic operators (+, -, *, /, **, %) and functions (sin, cos, tan, sqrt, log, abs, pi, e).
    """
    cleaned = expression.strip()
    
    # Whitelist of allowed words (math constants/functions)
    allowed_words = {"sin", "cos", "tan", "sqrt", "pi", "e", "log", "pow", "abs"}
    
    # Extract all words/names to verify they are in the whitelist
    words = set(re_word.group() for re_word in re_find_words(cleaned))
    
    # Check if any word is not in the whitelist
    for w in words:
        if w.lower() not in allowed_words:
            return f"Error: Unsafe expression containing unauthorized name '{w}'. Only basic math functions are allowed."
    
    # Ensure no double underscores or forbidden characters
    if "__" in cleaned or ";" in cleaned:
        return "Error: Invalid expression format."

    # Verify only math operators and characters are present
    # We strip whitelist words first to verify the remaining chars
    verify_str = cleaned
    for w in allowed_words:
        verify_str = verify_str.replace(w, "")
    
    if not all(c.isdigit() or c in " \t+-*/.()%" for c in verify_str):
        return "Error: Invalid characters in expression. Only digits, basic operators, and math functions are allowed."

    try:
        # Define safe execution context
        safe_globals = {
            "__builtins__": None,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e,
            "log": math.log,
            "pow": pow,
            "abs": abs
        }
        
        # Evaluate in a restricted sandbox
        result = eval(cleaned, safe_globals, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def re_find_words(text):
    import re
    return re.finditer(r'[a-zA-Z_]+', text)
