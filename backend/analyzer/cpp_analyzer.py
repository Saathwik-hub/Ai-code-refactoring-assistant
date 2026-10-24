import re
import uuid
from typing import List
from backend.analyzer.base_analyzer import BaseAnalyzer
from backend.models.analysis_model import StaticIssue

class CPPAnalyzer(BaseAnalyzer):
    def analyze(self, code: str, filename: str) -> List[StaticIssue]:
        issues = []
        lines = code.splitlines()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Raw pointer new without smart pointer
            if re.search(r'\b\w+\s*\*+\s*\w+\s*=\s*new\s+', stripped):
                issues.append(StaticIssue(
                    id=f"cpp_{uuid.uuid4().hex[:6]}",
                    rule_id="CPPCHECK-RawPointerNew",
                    category="code_smell",
                    severity="Medium",
                    message="Use of raw pointer memory allocation (`new`). Memory leak risk.",
                    line=idx,
                    column=1,
                    recommendation="Use smart pointers (`std::unique_ptr` or `std::shared_ptr`) or `std::make_unique`."
                ))

            # Dangerous functions like strcpy, gets, sprintf
            if re.search(r'\b(gets|strcpy|sprintf|strcat)\s*\(', stripped):
                issues.append(StaticIssue(
                    id=f"sec_{uuid.uuid4().hex[:6]}",
                    rule_id="SEC-CPP-001",
                    category="security",
                    severity="High",
                    message="Use of buffer overflow vulnerable C function.",
                    line=idx,
                    column=1,
                    recommendation="Replace with safe bounded alternatives like `strncpy`, `snprintf`, or `std::string`."
                ))

            # Using namespace std in header or global scope
            if "using namespace std;" in stripped:
                issues.append(StaticIssue(
                    id=f"cpp_{uuid.uuid4().hex[:6]}",
                    rule_id="CPPCHECK-NamespaceStd",
                    category="coding_standard",
                    severity="Info",
                    message="`using namespace std;` pollutes global scope and leads to symbol collisions.",
                    line=idx,
                    column=1,
                    recommendation="Explicitly scope types with `std::` (e.g. `std::cout`, `std::vector`)."
                ))

        return issues
