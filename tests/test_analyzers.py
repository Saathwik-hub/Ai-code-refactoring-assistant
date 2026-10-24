import unittest
from backend.analyzer import get_analyzer_for_language
from backend.analyzer.python_analyzer import PythonAnalyzer
from backend.metrics.complexity import calculate_complexity
from backend.metrics.maintainability import compute_quality_scores

class TestStaticAnalyzers(unittest.TestCase):
    def test_analyzer_factory(self):
        self.assertIsInstance(get_analyzer_for_language("python"), PythonAnalyzer)
        self.assertIsNotNone(get_analyzer_for_language("javascript"))
        self.assertIsNotNone(get_analyzer_for_language("java"))
        self.assertIsNotNone(get_analyzer_for_language("cpp"))
        self.assertIsNotNone(get_analyzer_for_language("html"))
        self.assertIsNotNone(get_analyzer_for_language("css"))

    def test_python_security_issues_detected(self):
        insecure_code = """
import os
password = "super_secret_password_123"
eval("2 + 2")
try:
    x = 10 / 0
except:
    pass
"""
        analyzer = PythonAnalyzer()
        issues = analyzer.analyze(insecure_code, "security_test.py")
        
        rule_ids = [i.rule_id for i in issues]
        # Should detect hardcoded secret (SEC-001)
        self.assertIn("SEC-001", rule_ids)
        # Should detect eval (SEC-002)
        self.assertIn("SEC-002", rule_ids)
        # Should detect bare except (SMELL-001)
        self.assertIn("SMELL-001", rule_ids)

    def test_complexity_metrics(self):
        code = """
def complex_decision(a, b, c):
    if a > 0:
        if b > 0:
            return 1
        elif c > 0:
            return 2
    else:
        for i in range(10):
            if i == b:
                return 3
    return 0
"""
        metrics = calculate_complexity(code, "python")
        self.assertGreater(metrics.cyclomatic_complexity, 1)
        self.assertGreaterEqual(metrics.nesting_depth, 2)
        self.assertEqual(metrics.function_count, 1)

    def test_quality_score_computation(self):
        analyzer = PythonAnalyzer()
        issues = analyzer.analyze("def add(x, y):\n    return x + y\n", "clean.py")
        comp = calculate_complexity("def add(x, y):\n    return x + y\n", "python")
        scores = compute_quality_scores(issues, comp)

        self.assertGreaterEqual(scores.overall_health, 80)
        self.assertIn(scores.grade, ["A+", "A", "B", "C", "D", "F"])

if __name__ == "__main__":
    unittest.main()
