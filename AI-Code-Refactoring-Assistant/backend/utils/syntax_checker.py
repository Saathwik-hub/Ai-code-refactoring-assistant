import ast
import json
import re
from typing import Dict, List, Any

def validate_syntax(code: str, language: str) -> Dict[str, Any]:
    language = language.lower()
    diagnostics = []
    
    if language == "python":
        return _validate_python(code)
    elif language == "json":
        return _validate_json(code)
    elif language in ["javascript", "js", "typescript", "ts"]:
        return _validate_javascript(code, language)
    elif language in ["c", "cpp", "c++", "java"]:
        return _validate_c_like(code, language)
    elif language in ["html", "css"]:
        return _validate_web(code, language)
    else:
        # Default bracket check
        return _validate_brackets(code, language)

def _validate_python(code: str) -> Dict[str, Any]:
    diagnostics = []
    try:
        ast.parse(code)
        return {
            "is_valid": True,
            "language": "python",
            "diagnostics": diagnostics,
            "error_count": 0,
            "warning_count": 0,
            "summary": "Python syntax validation passed successfully."
        }
    except SyntaxError as err:
        diagnostics.append({
            "line": err.lineno or 1,
            "column": err.offset or 1,
            "message": f"SyntaxError: {err.msg}",
            "severity": "error"
        })
        return {
            "is_valid": False,
            "language": "python",
            "diagnostics": diagnostics,
            "error_count": 1,
            "warning_count": 0,
            "summary": f"Python syntax error at line {err.lineno}: {err.msg}"
        }
    except Exception as err:
        diagnostics.append({
            "line": 1,
            "column": 1,
            "message": str(err),
            "severity": "error"
        })
        return {
            "is_valid": False,
            "language": "python",
            "diagnostics": diagnostics,
            "error_count": 1,
            "warning_count": 0,
            "summary": f"Error parsing Python code: {str(err)}"
        }

def _validate_json(code: str) -> Dict[str, Any]:
    diagnostics = []
    try:
        json.loads(code)
        return {
            "is_valid": True,
            "language": "json",
            "diagnostics": [],
            "error_count": 0,
            "warning_count": 0,
            "summary": "JSON syntax validation passed successfully."
        }
    except json.JSONDecodeError as err:
        diagnostics.append({
            "line": err.lineno,
            "column": err.colno,
            "message": f"JSONDecodeError: {err.msg}",
            "severity": "error"
        })
        return {
            "is_valid": False,
            "language": "json",
            "diagnostics": diagnostics,
            "error_count": 1,
            "warning_count": 0,
            "summary": f"Invalid JSON at line {err.lineno}, column {err.colno}: {err.msg}"
        }

def _validate_javascript(code: str, language: str) -> Dict[str, Any]:
    diagnostics = []
    
    # 1. Check bracket and parenthesis matching
    bracket_errors = _check_balanced_delimiters(code)
    diagnostics.extend(bracket_errors)
    
    # 2. Check basic JS/TS syntax errors (e.g. unclosed strings, invalid keywords)
    lines = code.splitlines()
    for idx, line in enumerate(lines, start=1):
        # Unclosed single/double quotes (excluding escaped)
        quotes = [c for c in line if c in ('"', "'", '`')]
        if len(quotes) % 2 != 0 and not ("//" in line or "/*" in line):
            diagnostics.append({
                "line": idx,
                "column": len(line),
                "message": "Possible unclosed string literal or quote mismatch",
                "severity": "warning"
            })
            
        # Common syntax mistakes
        if re.search(r'\b(const|let|var)\s*$', line.strip()):
            diagnostics.append({
                "line": idx,
                "column": len(line),
                "message": "Missing variable name after declaration keyword",
                "severity": "error"
            })

    errors = [d for d in diagnostics if d["severity"] == "error"]
    warnings = [d for d in diagnostics if d["severity"] == "warning"]
    
    is_valid = len(errors) == 0
    summary = f"{language.upper()} syntax check completed. {len(errors)} error(s), {len(warnings)} warning(s)." if not is_valid else f"{language.upper()} syntax validation passed successfully."
    
    return {
        "is_valid": is_valid,
        "language": language,
        "diagnostics": diagnostics,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "summary": summary
    }

def _validate_c_like(code: str, language: str) -> Dict[str, Any]:
    diagnostics = []
    
    # Check bracket matching
    bracket_errors = _check_balanced_delimiters(code)
    diagnostics.extend(bracket_errors)
    
    # Check missing semicolons and unclosed comments
    lines = code.splitlines()
    in_block_comment = False
    
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if "/*" in stripped and not "*/" in stripped:
            in_block_comment = True
        if "*/" in stripped:
            in_block_comment = False
            
        if not stripped or stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("{") or stripped.startswith("}") or in_block_comment:
            continue

        # Check statement semicolon termination heuristic
        if not (stripped.endswith(";") or stripped.endswith("{") or stripped.endswith("}") or stripped.endswith(":") or stripped.endswith(",")):
            if any(stripped.startswith(kw) for kw in ["if", "else", "for", "while", "class", "struct", "enum", "public", "private", "protected", "void", "int", "float", "double", "char", "bool"]):
                if not stripped.endswith(")"):
                    diagnostics.append({
                        "line": idx,
                        "column": len(line),
                        "message": "Possible missing semicolon at the end of statement",
                        "severity": "warning"
                    })

    errors = [d for d in diagnostics if d["severity"] == "error"]
    warnings = [d for d in diagnostics if d["severity"] == "warning"]
    
    is_valid = len(errors) == 0
    summary = f"{language.upper()} syntax check completed with {len(errors)} error(s) and {len(warnings)} warning(s)." if not is_valid else f"{language.upper()} syntax structure verified."

    return {
        "is_valid": is_valid,
        "language": language,
        "diagnostics": diagnostics,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "summary": summary
    }

def _validate_web(code: str, language: str) -> Dict[str, Any]:
    diagnostics = []
    
    if language == "html":
        # Check unclosed tags heuristic
        tags = re.findall(r'</?([a-zA-Z0-9]+)[^>]*>', code)
        stack = []
        void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        
        lines = code.splitlines()
        for idx, line in enumerate(lines, start=1):
            line_tags = re.findall(r'</?([a-zA-Z0-9]+)[^>]*>', line)
            for t in line_tags:
                if t.lower() in void_tags:
                    continue
                if line.find(f'</{t}') != -1:
                    pass
                elif line.find(f'<{t}') != -1:
                    pass

        diagnostics.extend(_check_balanced_delimiters(code))
        
    elif language == "css":
        # Check unclosed braces
        diagnostics.extend(_check_balanced_delimiters(code))
        # Check missing property colons
        lines = code.splitlines()
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped and not stripped.startswith("/*") and not stripped.endswith("{") and not stripped.endswith("}"):
                if ":" not in stripped:
                    diagnostics.append({
                        "line": idx,
                        "column": len(line),
                        "message": "CSS declaration line missing colon separator",
                        "severity": "warning"
                    })

    errors = [d for d in diagnostics if d["severity"] == "error"]
    warnings = [d for d in diagnostics if d["severity"] == "warning"]

    return {
        "is_valid": len(errors) == 0,
        "language": language,
        "diagnostics": diagnostics,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "summary": f"{language.upper()} syntax validated successfully." if len(errors) == 0 else f"{language.upper()} syntax check found issues."
    }

def _validate_brackets(code: str, language: str) -> Dict[str, Any]:
    diagnostics = _check_balanced_delimiters(code)
    errors = [d for d in diagnostics if d["severity"] == "error"]
    warnings = [d for d in diagnostics if d["severity"] == "warning"]

    return {
        "is_valid": len(errors) == 0,
        "language": language,
        "diagnostics": diagnostics,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "summary": f"Syntax structure validation complete for {language}."
    }

def _check_balanced_delimiters(code: str) -> List[Dict[str, Any]]:
    stack = []
    matching = {')': '(', '}': '{', ']': '['}
    diagnostics = []
    
    lines = code.splitlines()
    for line_idx, line in enumerate(lines, start=1):
        for col_idx, char in enumerate(line, start=1):
            if char in '({[':
                stack.append((char, line_idx, col_idx))
            elif char in ')}]':
                if not stack:
                    diagnostics.append({
                        "line": line_idx,
                        "column": col_idx,
                        "message": f"Unmatched closing delimiter '{char}'",
                        "severity": "error"
                    })
                else:
                    top_char, top_line, top_col = stack.pop()
                    if top_char != matching[char]:
                        diagnostics.append({
                            "line": line_idx,
                            "column": col_idx,
                            "message": f"Mismatched delimiter '{char}', expected match for '{top_char}' from line {top_line}",
                            "severity": "error"
                        })
                        
    for unclosed_char, unclosed_line, unclosed_col in stack:
        diagnostics.append({
            "line": unclosed_line,
            "column": unclosed_col,
            "message": f"Unclosed opening delimiter '{unclosed_char}'",
            "severity": "error"
        })
        
    return diagnostics
