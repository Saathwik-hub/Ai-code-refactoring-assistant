import re
import uuid
from typing import List
from backend.analyzer.base_analyzer import BaseAnalyzer
from backend.models.analysis_model import StaticIssue

class CSSAnalyzer(BaseAnalyzer):
    def analyze(self, code: str, filename: str) -> List[StaticIssue]:
        issues = []
        lines = code.splitlines()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # !important override overuse
            if "!important" in stripped:
                issues.append(StaticIssue(
                    id=f"css_{uuid.uuid4().hex[:6]}",
                    rule_id="STYLELINT-no-important",
                    category="code_smell",
                    severity="Low",
                    message="Use of `!important` rule overrides CSS specificity cascade.",
                    line=idx,
                    column=stripped.find("!important"),
                    recommendation="Refactor selector specificity instead of forcing `!important`."
                ))

            # Zero unit violation (e.g. 0px instead of 0)
            if re.search(r'\b0(px|em|rem|pt|vh|vw)\b', stripped):
                issues.append(StaticIssue(
                    id=f"css_{uuid.uuid4().hex[:6]}",
                    rule_id="STYLELINT-zero-no-unit",
                    category="coding_standard",
                    severity="Info",
                    message="Zero values do not require unit specifiers (e.g., use `0` instead of `0px`).",
                    line=idx,
                    column=1,
                    recommendation="Remove unit suffix from 0 values."
                ))

        return issues
