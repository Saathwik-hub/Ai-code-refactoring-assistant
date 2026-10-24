from fastapi import APIRouter, Response
import json
from backend.models.analysis_model import AnalyzeRequest, AnalysisReport
from backend.controllers.analysis_controller import AnalysisController

router = APIRouter(prefix="/api/analysis", tags=["Static Code Analysis"])

@router.post("/run", response_model=AnalysisReport)
def run_analysis(req: AnalyzeRequest):
    return AnalysisController.run_analysis(req)

@router.get("/report/{report_id}", response_model=AnalysisReport)
def get_report(report_id: str):
    return AnalysisController.get_report(report_id)

@router.get("/download/{report_id}")
def download_report(report_id: str, format: str = "json"):
    report = AnalysisController.get_report(report_id)
    if format.lower() == "txt":
        content = f"""==================================================
AI CODE REFACTORING ASSISTANT - ANALYSIS REPORT
==================================================
Report ID: {report.id}
File Name: {report.filename}
Language:  {report.language.upper()}
Date:      {report.created_at}

HEALTH SCORE: {report.health_score}% (Grade {report.grade})
TOTAL ISSUES: {report.total_issues} (Critical: {report.critical_count}, High: {report.high_count}, Medium: {report.medium_count})

SCORES BREAKDOWN:
- Readability:      {report.scores.readability}%
- Maintainability:  {report.scores.maintainability}%
- Security:         {report.scores.security}%
- Complexity Score: {report.scores.complexity}%

COMPLEXITY METRICS:
- Cyclomatic Complexity: {report.complexity.cyclomatic_complexity}
- Nesting Depth:         {report.complexity.nesting_depth}
- Function Count:        {report.complexity.function_count}

DETECTED ISSUES:
"""
        for idx, i in enumerate(report.issues, start=1):
            content += f"\n[{idx}] [{i.severity.upper()}] Line {i.line}: {i.message}\n    Recommendation: {i.recommendation}\n"

        return Response(content=content, media_type="text/plain", headers={"Content-Disposition": f"attachment; filename=report_{report_id}.txt"})
    else:
        return Response(content=json.dumps(report.dict(), indent=2), media_type="application/json", headers={"Content-Disposition": f"attachment; filename=report_{report_id}.json"})
