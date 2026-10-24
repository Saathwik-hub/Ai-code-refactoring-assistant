from typing import List, Dict, Any
from fastapi import HTTPException
from backend.models.ai_model import (
    RefactorRequest,
    RefactorResponse,
    ExplainRequest,
    OptimizeRequest,
    ChatRequest
)
from backend.services.ai.refactoring_engine import RefactoringEngine
from backend.services.ai.explanation_engine import ExplanationEngine
from backend.services.ai.chat_engine import ChatEngine
from backend.database import save_refactoring_session, get_refactoring_history, get_refactoring_session, get_analysis_report

class AIController:
    @staticmethod
    def refactor_code(req: RefactorRequest) -> RefactorResponse:
        if not req.code or not req.code.strip():
            raise HTTPException(status_code=400, detail="Code body cannot be empty.")

        analysis_report = None
        if req.analysis_report_id:
            analysis_report = get_analysis_report(req.analysis_report_id)

        res = RefactoringEngine.refactor(
            code=req.code,
            filename=req.filename or "main.py",
            language=req.language,
            mode=req.mode or "Clean Code",
            analysis_report=analysis_report
        )

        # Save to SQLite refactoring history
        save_refactoring_session(res.dict())
        return res

    @staticmethod
    def explain_code(req: ExplainRequest) -> Dict[str, Any]:
        return ExplanationEngine.explain_code(req.code, req.language, req.line_number)

    @staticmethod
    def optimize_code(req: OptimizeRequest) -> Dict[str, Any]:
        res = RefactoringEngine.refactor(req.code, "snippet.txt", req.language, mode="Performance")
        return {
            "original_code": res.original_code,
            "optimized_code": res.refactored_code,
            "explanations": res.explanations
        }

    @staticmethod
    def process_chat(req: ChatRequest) -> Dict[str, Any]:
        msg_dicts = [m.dict() for m in req.messages]
        reply = ChatEngine.process_chat(msg_dicts, req.current_code or "", req.language or "python")
        return {"reply": reply}

    @staticmethod
    def list_history() -> List[Dict[str, Any]]:
        return get_refactoring_history()

    @staticmethod
    def get_history_session(session_id: str) -> RefactorResponse:
        raw = get_refactoring_session(session_id)
        if not raw:
            raise HTTPException(status_code=404, detail="Refactoring session not found.")
        return RefactorResponse(**raw)
