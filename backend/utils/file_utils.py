import os
import re

EXTENSION_MAP = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".ts": "typescript",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".json": "json"
}

ALLOWED_EXTENSIONS = list(EXTENSION_MAP.keys())
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

def get_language_from_filename(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    return EXTENSION_MAP.get(ext, "plaintext")

def is_allowed_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in EXTENSION_MAP

def detect_language_from_content(code: str, filename: str = None) -> tuple[str, float]:
    """Detects language based on filename extension or code syntax signatures."""
    if filename:
        ext_lang = get_language_from_filename(filename)
        if ext_lang != "plaintext":
            return ext_lang, 0.95

    code_strip = code.strip()
    if not code_strip:
        return "plaintext", 0.1

    # Python check
    if re.search(r'\b(def\s+\w+|class\s+\w+|import\s+\w+|from\s+\w+\s+import|if\s+__name__\s*==\s*[\'"]__main__[\'"])\b', code_strip):
        return "python", 0.90

    # HTML check
    if re.search(r'<!DOCTYPE\s+html|<html|<head|<body|<div|<script|<style', code_strip, re.IGNORECASE):
        return "html", 0.95

    # JSON check
    if (code_strip.startswith("{") and code_strip.endswith("}")) or (code_strip.startswith("[") and code_strip.endswith("]")):
        try:
            import json
            json.loads(code_strip)
            return "json", 0.95
        except Exception:
            pass

    # Java check
    if re.search(r'\b(public\s+class|public\s+static\s+void\s+main|System\.out\.println|import\s+java\.)\b', code_strip):
        return "java", 0.92

    # C++ check
    if re.search(r'#include\s*<iostream>|std::cout|std::vector|using\s+namespace\s+std;', code_strip):
        return "cpp", 0.93

    # C check
    if re.search(r'#include\s*<stdio\.h>|printf\(|int\s+main\s*\(\s*int\s+argc', code_strip):
        return "c", 0.90

    # TypeScript check
    if re.search(r'\b(interface\s+\w+|type\s+\w+\s*=|\:\s*(string|number|boolean|any|void)|implements\s+\w+)\b', code_strip):
        return "typescript", 0.90

    # JavaScript check
    if re.search(r'\b(const\s+\w+|let\s+\w+|var\s+\w+|function\s*\w*|console\.log|document\.getElementById|export\s+default)\b', code_strip):
        return "javascript", 0.88

    # CSS check
    if re.search(r'[\{\}\;\:]', code_strip) and re.search(r'(\.[a-zA-Z0-9_\-]+|\#[a-zA-Z0-9_\-]+|[a-zA-Z0-9_\-]+)\s*\{', code_strip):
        return "css", 0.85

    return "plaintext", 0.50
