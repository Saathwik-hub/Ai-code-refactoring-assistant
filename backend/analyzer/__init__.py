from backend.analyzer.python_analyzer import PythonAnalyzer
from backend.analyzer.js_analyzer import JSAnalyzer
from backend.analyzer.java_analyzer import JavaAnalyzer
from backend.analyzer.cpp_analyzer import CPPAnalyzer
from backend.analyzer.html_analyzer import HTMLAnalyzer
from backend.analyzer.css_analyzer import CSSAnalyzer

def get_analyzer_for_language(language: str):
    lang = language.lower()
    if lang in ["python", "py"]:
        return PythonAnalyzer()
    elif lang in ["javascript", "js", "typescript", "ts"]:
        return JSAnalyzer()
    elif lang == "java":
        return JavaAnalyzer()
    elif lang in ["cpp", "c", "c++"]:
        return CPPAnalyzer()
    elif lang == "html":
        return HTMLAnalyzer()
    elif lang == "css":
        return CSSAnalyzer()
    else:
        return PythonAnalyzer()
