from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class StaticIssue(BaseModel):
    id: str
    rule_id: str
    category: str  # "security", "code_smell", "coding_standard", "bug_risk"
    severity: str  # "Critical", "High", "Medium", "Low", "Info"
    message: str
    line: int
    column: Optional[int] = 1
    recommendation: str

class DuplicateSnippet(BaseModel):
    original_line: int
    duplicate_line: int
    similarity_percentage: float
    snippet_preview: str

class QualityScores(BaseModel):
    readability: float
    maintainability: float
    security: float
    complexity: float
    overall_health: float
    grade: str  # "A+", "A", "B", "C", "D", "F"

class ComplexityMetrics(BaseModel):
    cyclomatic_complexity: int
    nesting_depth: int
    function_count: int
    class_count: int
    average_function_length: float

class AnalysisReport(BaseModel):
    id: str
    filename: str
    language: str
    health_score: int
    grade: str
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    scores: QualityScores
    complexity: ComplexityMetrics
    issues: List[StaticIssue]
    duplicates: List[DuplicateSnippet]
    recommendations: List[str]
    created_at: str

class AnalyzeRequest(BaseModel):
    code: str
    filename: Optional[str] = "snippet.txt"
    language: Optional[str] = "python"
