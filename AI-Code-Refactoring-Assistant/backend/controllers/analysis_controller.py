import uuid
from datetime import datetime
from typing import Dict, Any, List
from fastapi import HTTPException
from backend.models.analysis_model import AnalyzeRequest, AnalysisReport
from backend.analyzer import get_analyzer_for_language
from backend.metrics.complexity import calculate_complexity
from backend.metrics.maintainability import compute_quality_scores
from backend.metrics.duplication import detect_duplicates
from backend.database import save_analysis_report, get_analysis_report

class AnalysisController:
    @staticmethod
    def run_analysis(req: AnalyzeRequest) -> AnalysisReport:
        if not req.code or not req.code.strip():
            raise HTTPException(status_code=400, detail="Code body cannot be empty.")

        report_id = f"report_{uuid.uuid4().hex[:8]}"
        language = req.language.lower() if req.language else "python"

        # 1. Run Static Analyzer
        analyzer = get_analyzer_for_language(language)
        issues = analyzer.analyze(req.code, req.filename or "snippet.txt")

        # 2. Run Metrics Computation
        complexity = calculate_complexity(req.code, language)
        scores = compute_quality_scores(issues, complexity)
        duplicates = detect_duplicates(req.code)

        # 3. Categorize Issue Counts
        crit = sum(1 for i in issues if i.severity == "Critical")
        high = sum(1 for i in issues if i.severity == "High")
        med = sum(1 for i in issues if i.severity == "Medium")
        low = sum(1 for i in issues if i.severity == "Low")
        info = sum(1 for i in issues if i.severity == "Info")

        # 4. Recommendations List
        recs = [i.recommendation for i in issues[:5]]
        if not recs:
            recs.append("Code structure is clean and adheres to quality standards.")

        report = AnalysisReport(
            id=report_id,
            filename=req.filename or "snippet.txt",
            language=language,
            health_score=int(scores.overall_health),
            grade=scores.grade,
            total_issues=len(issues),
            critical_count=crit,
            high_count=high,
            medium_count=med,
            low_count=low,
            info_count=info,
            scores=scores,
            complexity=complexity,
            issues=issues,
            duplicates=duplicates,
            recommendations=recs,
            created_at=datetime.now().isoformat()
        )

        # Store report in SQLite DB
        save_analysis_report(report.dict())
        return report

    @staticmethod
    def get_report(report_id: str) -> AnalysisReport:
        raw = get_analysis_report(report_id)
        if not raw:
            raise HTTPException(status_code=404, detail="Analysis report not found.")
        return AnalysisReport(**raw)
