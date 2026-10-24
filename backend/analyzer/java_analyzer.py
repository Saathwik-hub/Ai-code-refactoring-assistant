import re
import uuid
from typing import List
from backend.analyzer.base_analyzer import BaseAnalyzer
from backend.models.analysis_model import StaticIssue

class JavaAnalyzer(BaseAnalyzer):
    def analyze(self, code: str, filename: str) -> List[StaticIssue]:
        issues = []
        lines = code.splitlines()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Google Java Style & PMD / Checkstyle rules
            if re.search(r'\bpublic\s+static\s+\w+\s+[a-z_0-9]+\s*\(', stripped) and not ("main" in stripped or "get" in stripped or "set" in stripped):
                issues.append(StaticIssue(
                    id=f"java_{uuid.uuid4().hex[:6]}",
                    rule_id="CHECKSTYLE-Naming",
                    category="coding_standard",
                    severity="Low",
                    message="Method name should follow camelCase naming convention.",
                    line=idx,
                    column=1,
                    recommendation="Rename method using lowerCamelCase format."
                ))

            # System.out.println in production
            if "System.out.print" in stripped:
                issues.append(StaticIssue(
                    id=f"java_{uuid.uuid4().hex[:6]}",
                    rule_id="PMD-SystemPrintln",
                    category="code_smell",
                    severity="Info",
                    message="Use of `System.out.println` instead of a standard logger framework.",
                    line=idx,
                    column=stripped.find("System.out"),
                    recommendation="Use SLF4J / Log4j logger framework (e.g., `logger.info()`)."
                ))

            # Generic Exception catching
            if re.search(r'catch\s*\(\s*Exception\b', stripped):
                issues.append(StaticIssue(
                    id=f"java_{uuid.uuid4().hex[:6]}",
                    rule_id="PMD-AvoidCatchingGenericException",
                    category="code_smell",
                    severity="Medium",
                    message="Catching generic `Exception` suppresses specific errors.",
                    line=idx,
                    column=1,
                    recommendation="Catch specific checked/unchecked exception subclasses."
                ))

            # Hardcoded Password
            if re.search(r'(password|secret)\s*=\s*[\'"][^\'"]+[\'"]', stripped, re.IGNORECASE):
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-JAVA-001",
                    category="security",
                    severity="Critical",
                    message="Hardcoded credentials in Java source file.",
                    line=idx,
                    column=1,
                    recommendation="Inject secrets using system properties or vault configuration."
                ))

        return issues
