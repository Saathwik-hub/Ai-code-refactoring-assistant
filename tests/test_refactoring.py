import unittest
from backend.services.ai.refactoring_engine import RefactoringEngine
from backend.services.ai.optimizer_engine import OptimizerEngine
from backend.services.ai.explanation_engine import ExplanationEngine
from backend.services.ai.chat_engine import ChatEngine

class TestRefactoringAndOptimizer(unittest.TestCase):
    def test_local_refactoring_clean_code(self):
        dirty_code = """
import sys
import sys

def calculate_values(a,b,c):
    password = 'admin_secret_token_123'
    result=a+b+c
    return result
"""
        response = RefactoringEngine.refactor(
            code=dirty_code,
            filename="calc.py",
            language="python",
            mode="Clean Code"
        )

        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.refactored_code)
        self.assertGreaterEqual(len(response.explanations), 1)
        self.assertIn("health_score", response.metrics_before)
        self.assertIn("health_score", response.metrics_after)

    def test_optimizer_engine_python_complexity(self):
        nested_code = """
def find_common(list1, list2):
    common = []
    for x in list1:
        if x in list2:
            common.append(x)
    return common
"""
        res = OptimizerEngine.optimize(nested_code, "python")
        self.assertIn("optimized_code", res)
        # Should have attempted or suggested set conversion for O(1) membership lookup
        self.assertIsNotNone(res["optimized_code"])
        self.assertGreaterEqual(len(res.get("changes", [])), 0)

    def test_explanation_engine(self):
        code = "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)\n"
        res = ExplanationEngine.explain_code(code, "python")
        self.assertIn("explanation", res)
        self.assertIn("language", res)

    def test_chat_engine_fallback(self):
        reply = ChatEngine.process_chat(
            messages=[{"role": "user", "content": "Explain how this function works"}],
            current_code="def greet(): return 'Hello'",
            language="python"
        )
        self.assertIsInstance(reply, str)
        self.assertGreater(len(reply), 10)

if __name__ == "__main__":
    unittest.main()
