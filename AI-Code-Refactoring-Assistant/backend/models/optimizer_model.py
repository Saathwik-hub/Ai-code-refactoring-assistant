from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class OptimizeCodeRequest(BaseModel):
    code: str
    language: str = "python"
    model: Optional[str] = None
    ollama_url: Optional[str] = None


class OptimizationChange(BaseModel):
    title: str
    before: str
    after: str
    description: str


class OptimizeCodeResponse(BaseModel):
    id: str
    original_code: str
    optimized_code: str
    frontend_code: Optional[str] = None
    backend_code: Optional[str] = None
    separation_note: Optional[str] = None
    speedup_estimate: Optional[str] = None
    language: str
    changes: List[OptimizationChange]
    complexity_before: str
    complexity_after: str
    lines_before: int
    lines_after: int
    summary: str
    model_used: Optional[str] = "Rule-based Optimizer"
    created_at: str


