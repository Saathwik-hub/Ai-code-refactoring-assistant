from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RefactorRequest(BaseModel):
    code: str
    filename: Optional[str] = "main.py"
    language: str
    mode: Optional[str] = "Clean Code"  # "Clean Code", "Performance", "Security", "Readability", "SOLID Principles", "Beginner Friendly", "Senior Engineer Style"
    analysis_report_id: Optional[str] = None
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = 2048

class ExplanationItem(BaseModel):
    title: str
    original_snippet: str
    refactored_snippet: str
    rationale: str
    principle_used: str  # e.g., "DRY", "KISS", "Single Responsibility", "Guard Clause"
    trade_off: Optional[str] = "None"

class RefactorResponse(BaseModel):
    id: str
    filename: str
    language: str
    mode: str
    model_used: str
    original_code: str
    refactored_code: str
    explanations: List[ExplanationItem]
    metrics_before: Dict[str, Any]
    metrics_after: Dict[str, Any]
    summary: str
    created_at: str

class ExplainRequest(BaseModel):
    code: str
    language: str
    line_number: Optional[int] = None

class OptimizeRequest(BaseModel):
    code: str
    language: str

class ChatMessage(BaseModel):
    role: str  # "user", "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    current_code: Optional[str] = ""
    language: Optional[str] = "python"
