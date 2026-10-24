import ast
import re
from backend.models.analysis_model import ComplexityMetrics

def calculate_complexity(code: str, language: str) -> ComplexityMetrics:
    lines = code.splitlines()
    fn_count = 0
    class_count = 0
    max_nesting = 0
    decision_points = 1  # Base complexity

    curr_nesting = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("//"):
            continue

        # Count nesting by indentation or braces
        leading_spaces = len(line) - len(line.lstrip())
        nesting_level = leading_spaces // 4
        if nesting_level > max_nesting:
            max_nesting = nesting_level

        # Decision keywords adding to Cyclomatic Complexity
        if re.search(r'\b(if|elif|else if|for|while|case|catch|except|&&|\|\||and|or)\b', stripped):
            decision_points += 1

        # Functions and Classes count
        if re.search(r'\b(def\s+\w+|function\s+\w*|void\s+\w+|int\s+\w+|public\s+[\w<>]+\s+\w+)\s*\(', stripped):
            fn_count += 1
        if re.search(r'\b(class|interface|struct)\s+\w+', stripped):
            class_count += 1

    fn_count = max(fn_count, 1)
    avg_fn_len = len(lines) / fn_count

    return ComplexityMetrics(
        cyclomatic_complexity=decision_points,
        nesting_depth=max(max_nesting, 1),
        function_count=fn_count,
        class_count=class_count,
        average_function_length=round(avg_fn_len, 1)
    )
