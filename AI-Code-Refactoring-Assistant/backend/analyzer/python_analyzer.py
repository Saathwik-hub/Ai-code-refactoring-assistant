import ast
import re
import uuid
from typing import List
from backend.analyzer.base_analyzer import BaseAnalyzer
from backend.models.analysis_model import StaticIssue

class PythonAnalyzer(BaseAnalyzer):
    def analyze(self, code: str, filename: str) -> List[StaticIssue]:
        issues = []
        lines = code.splitlines()

        # 1. Security Analysis (Bandit / OWASP rules)
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Hardcoded Secret / Password
            if re.search(r'(password|secret|api_key|private_key|token)\s*=\s*[\'"][^\'"]+[\'"]', stripped, re.IGNORECASE):
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-001",
                    category="security",
                    severity="Critical",
                    message="Hardcoded sensitive credentials/secret detected.",
                    line=idx,
                    column=1,
                    recommendation="Store API keys and passwords in environment variables or a secure key vault."
                ))

            # Dangerous eval() or exec()
            if re.search(r'\b(eval|exec)\s*\(', stripped):
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-002",
                    category="security",
                    severity="High",
                    message="Use of unsafe `eval()` or `exec()` function.",
                    line=idx,
                    column=stripped.find("eval") if "eval" in stripped else 1,
                    recommendation="Avoid dynamic code execution. Use ast.literal_eval() or safe parser functions."
                ))

            # Subprocess shell=True
            if "shell=True" in stripped and ("subprocess" in stripped or "popen" in stripped.lower()):
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-003",
                    category="security",
                    severity="High",
                    message="Subprocess call with `shell=True` poses shell injection risks.",
                    line=idx,
                    column=1,
                    recommendation="Set `shell=False` and pass arguments as a list of strings."
                ))

            # Insecure Randomness
            if re.search(r'\brandom\.(random|randint|choice)\b', stripped) and ("token" in stripped.lower() or "password" in stripped.lower() or "secret" in stripped.lower()):
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-004",
                    category="security",
                    severity="Medium",
                    message="Standard `random` module is not cryptographically secure for secret tokens.",
                    line=idx,
                    column=1,
                    recommendation="Use Python's `secrets` module for generating security sensitive tokens."
                ))

            # Unsafe Pickle
            if "pickle.loads" in stripped or "pickle.load" in stripped:
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-005",
                    category="security",
                    severity="High",
                    message="`pickle` deserialization is vulnerable to arbitrary code execution.",
                    line=idx,
                    column=1,
                    recommendation="Use safer serialization formats like JSON, Protocol Buffers, or msgpack."
                ))

            # PEP8 Line Length > 100
            if len(line) > 100:
                issues.append(StaticIssue(
                    id=f"pep8_{uuid.uuid4().hex[:6]}",
                    rule_id="PEP8-001",
                    category="coding_standard",
                    severity="Info",
                    message=f"Line length ({len(line)} chars) exceeds PEP8 recommended limit (79-100 chars).",
                    line=idx,
                    column=100,
                    recommendation="Break long lines across multiple lines or use parentheses."
                ))

            # Bare Except
            if re.match(r'^\s*except\s*:\s*$', stripped):
                issues.append(StaticIssue(
                    id=f"smell_{uuid.uuid4().hex[:6]}",
                    rule_id="SMELL-001",
                    category="code_smell",
                    severity="Medium",
                    message="Bare `except:` clause catches system exceptions like KeyboardInterrupt.",
                    line=idx,
                    column=1,
                    recommendation="Catch specific exceptions (e.g., `except ValueError:` or `except Exception:`)."
                ))

        # 2. AST-based Code Quality & Smells
        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                # Poor Variable Naming (single letter variables except i, j, k, _, x, y)
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    if len(node.id) == 1 and node.id not in ['i', 'j', 'k', '_', 'x', 'y', 'e', 'f']:
                        issues.append(StaticIssue(
                            id=f"smell_{uuid.uuid4().hex[:6]}",
                            rule_id="SMELL-002",
                            category="code_smell",
                            severity="Low",
                            message=f"Single-letter variable name '{node.id}' reduces code readability.",
                            line=getattr(node, 'lineno', 1),
                            column=getattr(node, 'col_offset', 1),
                            recommendation="Rename variable to a descriptive noun or identifier."
                        ))

                # Function checks
                if isinstance(node, ast.FunctionDef):
                    fn_lines = (node.end_lineno or node.lineno) - node.lineno
                    if fn_lines > 25:
                        issues.append(StaticIssue(
                            id=f"smell_{uuid.uuid4().hex[:6]}",
                            rule_id="SMELL-003",
                            category="code_smell",
                            severity="Medium",
                            message=f"Long function '{node.name}' ({fn_lines} lines). Single Responsibility Principle violation.",
                            line=node.lineno,
                            column=node.col_offset,
                            recommendation="Extract sub-tasks into modular helper functions."
                        ))

                    if not ast.get_docstring(node) and not node.name.startswith("_"):
                        issues.append(StaticIssue(
                            id=f"doc_{uuid.uuid4().hex[:6]}",
                            rule_id="PEP8-002",
                            category="coding_standard",
                            severity="Info",
                            message=f"Public function '{node.name}' is missing docstring documentation.",
                            line=node.lineno,
                            column=node.col_offset,
                            recommendation="Add docstring explaining purpose, parameters, and return values."
                        ))

        except Exception:
            pass

        return issues
