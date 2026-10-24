from typing import List, Dict, Any
from fastapi import APIRouter
from backend.models.ai_model import (
    RefactorRequest,
    RefactorResponse,
    ExplainRequest,
    OptimizeRequest,
    ChatRequest
)
from backend.controllers.ai_controller import AIController

router = APIRouter(prefix="/api", tags=["AI Refactoring Engine"])

@router.post("/refactor", response_model=RefactorResponse)
def refactor_code(req: RefactorRequest):
    return AIController.refactor_code(req)

@router.post("/explain")
def explain_code(req: ExplainRequest):
    return AIController.explain_code(req)

@router.post("/optimize")
def optimize_code(req: OptimizeRequest):
    return AIController.optimize_code(req)

@router.post("/chat")
def chat(req: ChatRequest):
    return AIController.process_chat(req)

@router.get("/ai/history")
def list_history():
    return AIController.list_history()

@router.get("/ai/history/{session_id}")
def get_history_session(session_id: str):
    return AIController.get_history_session(session_id)
