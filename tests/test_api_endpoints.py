import unittest
from backend.controllers.syntax_controller import SyntaxController
from backend.controllers.analysis_controller import AnalysisController
from backend.controllers.auth_controller import AuthController
from backend.controllers.file_controller import FileController
from backend.controllers.optimizer_controller import OptimizerController
from backend.controllers.ai_controller import AIController
from backend.models.file_model import LanguageDetectRequest
from backend.models.analysis_model import AnalyzeRequest
from backend.models.user import UserRegister, UserLogin
from backend.models.optimizer_model import OptimizeCodeRequest
from backend.models.ai_model import RefactorRequest, ChatRequest, ChatMessage

class TestApiControllers(unittest.TestCase):
    def test_syntax_controller(self):
        valid_res = SyntaxController.validate_code("def add(x, y): return x + y", "python")
        self.assertTrue(valid_res.is_valid)

        detect_req = LanguageDetectRequest(code="console.log('hello')", filename="app.js")
        detect_res = SyntaxController.detect_language(detect_req)
        self.assertEqual(detect_res.detected_language, "javascript")

    def test_analysis_controller(self):
        req = AnalyzeRequest(
            code="def hello():\n    print('Hello world')\n",
            filename="hello.py",
            language="python"
        )
        report = AnalysisController.run_analysis(req)
        self.assertIsNotNone(report.id)
        self.assertEqual(report.language, "python")
        self.assertGreaterEqual(report.health_score, 0)
        self.assertIn("grade", report.model_dump() if hasattr(report, "model_dump") else report.dict())

    def test_auth_controller(self):
        # Unique email and username
        test_email = "architect_test@repo.org"
        test_user = "architect_dev"
        reg_payload = UserRegister(
            username=test_user,
            email=test_email,
            password="SecurePassword123!"
        )
        reg_resp = AuthController.register(reg_payload)
        self.assertIsNotNone(reg_resp.access_token)
        self.assertEqual(reg_resp.user.email, test_email)

        login_payload = UserLogin(
            username_or_email=test_email,
            password="SecurePassword123!"
        )
        login_resp = AuthController.login(login_payload)
        self.assertIsNotNone(login_resp.access_token)

    def test_file_controller(self):
        files = FileController.list_files()
        self.assertIsInstance(files, list)

    def test_optimizer_controller(self):
        status = OptimizerController.get_ollama_status()
        self.assertIn("available", status)
        self.assertIn("endpoint", status)

        opt_req = OptimizeCodeRequest(
            code="def find_dup(arr):\n    return [x for x in arr if arr.count(x) > 1]\n",
            language="python"
        )
        opt_res = OptimizerController.optimize_code(opt_req)
        self.assertIn("optimized_code", opt_res)

    def test_ai_controller_refactor_and_chat(self):
        ref_req = RefactorRequest(
            code="def process():\n    a = 10\n    return a\n",
            filename="proc.py",
            language="python",
            mode="Clean Code"
        )
        ref_res = AIController.refactor_code(ref_req)
        self.assertIsNotNone(ref_res.refactored_code)

        chat_req = ChatRequest(
            messages=[ChatMessage(role="user", content="How do I refactor code?")],
            current_code="def run(): pass",
            language="python"
        )
        chat_res = AIController.process_chat(chat_req)
        self.assertIn("reply", chat_res)

if __name__ == "__main__":
    unittest.main()
