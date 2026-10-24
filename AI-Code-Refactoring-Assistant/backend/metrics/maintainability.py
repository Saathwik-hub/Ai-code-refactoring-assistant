from typing import List
from backend.models.analysis_model import StaticIssue, QualityScores, ComplexityMetrics

def compute_quality_scores(issues: List[StaticIssue], complexity: ComplexityMetrics) -> QualityScores:
    # Initial 100% scores
    readability = 95.0
    maintainability = 92.0
    security = 100.0
    comp_score = 90.0

    # Penalize based on issue severity
    for issue in issues:
        sev = issue.severity
        cat = issue.category

        if cat == "security":
            if sev == "Critical": security -= 25.0
            elif sev == "High": security -= 15.0
            elif sev == "Medium": security -= 10.0
        elif cat == "code_smell":
            readability -= 4.0
            maintainability -= 5.0
        elif cat == "coding_standard":
            readability -= 3.0
            maintainability -= 2.0

    # Penalize based on complexity
    if complexity.cyclomatic_complexity > 10:
        comp_score -= (complexity.cyclomatic_complexity - 10) * 3
    if complexity.nesting_depth > 4:
        comp_score -= (complexity.nesting_depth - 4) * 5

    # Clamp scores between 10% and 100%
    readability = max(min(readability, 100.0), 15.0)
    maintainability = max(min(maintainability, 100.0), 15.0)
    security = max(min(security, 100.0), 10.0)
    comp_score = max(min(comp_score, 100.0), 15.0)

    overall = round((readability * 0.25) + (maintainability * 0.35) + (security * 0.25) + (comp_score * 0.15), 1)

    if overall >= 90: grade = "A+"
    elif overall >= 80: grade = "A"
    elif overall >= 70: grade = "B"
    elif overall >= 60: grade = "C"
    elif overall >= 50: grade = "D"
    else: grade = "F"

    return QualityScores(
        readability=round(readability, 1),
        maintainability=round(maintainability, 1),
        security=round(security, 1),
        complexity=round(comp_score, 1),
        overall_health=overall,
        grade=grade
    )
