import unittest
from backend.utils.syntax_checker import validate_syntax
from backend.utils.file_utils import detect_language_from_content, get_language_from_filename

class TestSyntaxValidation(unittest.TestCase):
    def test_valid_python_syntax(self):
        code = "def add(a, b):\n    return a + b\n"
        result = validate_syntax(code, "python")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["error_count"], 0)

    def test_invalid_python_syntax(self):
        code = "def broken_func(\n    return 42\n"
        result = validate_syntax(code, "python")
        self.assertFalse(result["is_valid"])
        self.assertGreater(result["error_count"], 0)
        self.assertGreater(len(result["diagnostics"]), 0)
        self.assertIn("line", result["diagnostics"][0])

    def test_valid_json_syntax(self):
        code = '{"name": "refactor-assistant", "version": "1.0.0"}'
        result = validate_syntax(code, "json")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["error_count"], 0)

    def test_invalid_json_syntax(self):
        code = '{"name": "missing_quote, 123}'
        result = validate_syntax(code, "json")
        self.assertFalse(result["is_valid"])
        self.assertGreater(result["error_count"], 0)

    def test_javascript_bracket_balance(self):
        valid_js = "function test() { if (true) { return 1; } }"
        res = validate_syntax(valid_js, "javascript")
        self.assertTrue(res["is_valid"])

        invalid_js = "function test() { if (true) { return 1; }"
        res_err = validate_syntax(invalid_js, "javascript")
        self.assertFalse(res_err["is_valid"])

class TestLanguageDetection(unittest.TestCase):
    def test_extension_detection(self):
        self.assertEqual(get_language_from_filename("script.py"), "python")
        self.assertEqual(get_language_from_filename("index.js"), "javascript")
        self.assertEqual(get_language_from_filename("Main.java"), "java")
        self.assertEqual(get_language_from_filename("app.cpp"), "cpp")
        self.assertEqual(get_language_from_filename("page.html"), "html")
        self.assertEqual(get_language_from_filename("styles.css"), "css")
        self.assertEqual(get_language_from_filename("config.json"), "json")

    def test_content_heuristic_detection(self):
        py_code = "def process_data(items):\n    return [x * 2 for x in items]"
        lang, conf = detect_language_from_content(py_code, None)
        self.assertEqual(lang, "python")

        html_code = "<!DOCTYPE html><html><body><h1>Title</h1></body></html>"
        lang, conf = detect_language_from_content(html_code, None)
        self.assertEqual(lang, "html")

if __name__ == "__main__":
    unittest.main()
