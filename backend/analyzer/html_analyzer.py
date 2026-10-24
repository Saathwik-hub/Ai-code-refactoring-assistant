import re
import uuid
from typing import List
from backend.analyzer.base_analyzer import BaseAnalyzer
from backend.models.analysis_model import StaticIssue

class HTMLAnalyzer(BaseAnalyzer):
    def analyze(self, code: str, filename: str) -> List[StaticIssue]:
        issues = []
        lines = code.splitlines()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Inline Style attribute
            if re.search(r'\bstyle\s*=\s*[\'"][^\'"]+[\'"]', stripped, re.IGNORECASE):
                issues.append(StaticIssue(
                    id=f"html_{uuid.uuid4().hex[:6]}",
                    rule_id="HTMLHINT-no-inline-style",
                    category="code_smell",
                    severity="Info",
                    message="Use of inline `style` attribute reduces CSS maintainability.",
                    line=idx,
                    column=stripped.lower().find("style="),
                    recommendation="Move inline CSS declarations to an external or embedded stylesheet."
                ))

            # Missing alt tag on img
            if "<img" in stripped.lower() and "alt=" not in stripped.lower():
                issues.append(StaticIssue(
                    id=f"html_{uuid.uuid4().hex[:6]}",
                    rule_id="HTMLHINT-img-alt-required",
                    category="coding_standard",
                    severity="Low",
                    message="`<img>` element is missing an `alt` accessibility attribute.",
                    line=idx,
                    column=stripped.lower().find("<img"),
                    recommendation="Add descriptive `alt='...'` text for web accessibility."
                ))

            # Deprecated tags like <font>, <center>, <marquee>
            if re.search(r'<(font|center|marquee|blink)\b', stripped, re.IGNORECASE):
                issues.append(StaticIssue(
                    id=f"html_{uuid.uuid4().hex[:6]}",
                    rule_id="HTMLHINT-deprecated-tag",
                    category="coding_standard",
                    severity="Medium",
                    message="Use of deprecated HTML tag.",
                    line=idx,
                    column=1,
                    recommendation="Replace deprecated tags with semantic HTML5 elements and CSS."
                ))

        return issues
