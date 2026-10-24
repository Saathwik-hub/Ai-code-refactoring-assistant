import re
import uuid
from typing import List
from backend.analyzer.base_analyzer import BaseAnalyzer
from backend.models.analysis_model import StaticIssue

class JSAnalyzer(BaseAnalyzer):
    def analyze(self, code: str, filename: str) -> List[StaticIssue]:
        issues = []
        lines = code.splitlines()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # 1. Security Analysis (OWASP JS rules)
            if re.search(r'(password|secret|api_key|token)\s*[:=]\s*[\'"][^\'"]+[\'"]', stripped, re.IGNORECASE):
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-JS-001",
                    category="security",
                    severity="Critical",
                    message="Hardcoded sensitive credentials/API key in client-side JavaScript.",
                    line=idx,
                    column=1,
                    recommendation="Never store secrets in client-side code. Use server-side environment variables."
                ))

            # XSS Risk with innerHTML
            if ".innerHTML" in stripped:
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-JS-002",
                    category="security",
                    severity="High",
                    message="Direct assignment to `innerHTML` exposes DOM-based Cross-Site Scripting (XSS).",
                    line=idx,
                    column=stripped.find(".innerHTML"),
                    recommendation="Use `textContent` or `innerText` or sanitize dynamic markup using DOMPurify."
                ))

            # Dangerous eval() or document.write()
            if re.search(r'\b(eval|document\.write)\s*\(', stripped):
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-JS-003",
                    category="security",
                    severity="High",
                    message="Use of unsafe `eval()` or `document.write()`.",
                    line=idx,
                    column=1,
                    recommendation="Remove dynamic code evaluation or document stream modification."
                ))

            # 2. ESLint & Quality Rules
            # Deprecated 'var' keyword
            if re.search(r'\bvar\s+\w+', stripped):
                issues.append(StaticIssue(
                    id=f"eslint_{uuid.uuid4().hex[:6]}",
                    rule_id="ESLINT-no-var",
                    category="coding_standard",
                    severity="Medium",
                    message="Use of `var` scope keyword. Modern JS prefers block-scoped `const` or `let`.",
                    line=idx,
                    column=stripped.find("var"),
                    recommendation="Replace `var` with `const` for immutable variables or `let` for mutable bindings."
                ))

            # Loose Equality ==
            if re.search(r'[^=!<>]==[^=]', stripped) and not ("//" in stripped or "/*" in stripped):
                issues.append(StaticIssue(
                    id=f"eslint_{uuid.uuid4().hex[:6]}",
                    rule_id="ESLINT-eqeqeq",
                    category="code_smell",
                    severity="Low",
                    message="Use of loose equality operator `==`. Potential implicit type coercion bugs.",
                    line=idx,
                    column=stripped.find("=="),
                    recommendation="Use strict equality `===` instead of `==`."
                ))

            # Console log leftover
            if "console.log(" in stripped:
                issues.append(StaticIssue(
                    id=f"eslint_{uuid.uuid4().hex[:6]}",
                    rule_id="ESLINT-no-console",
                    category="code_smell",
                    severity="Info",
                    message="Leftover `console.log()` statement.",
                    line=idx,
                    column=stripped.find("console.log"),
                    recommendation="Remove console debugging statements before deploying to production."
                ))

        return issues
