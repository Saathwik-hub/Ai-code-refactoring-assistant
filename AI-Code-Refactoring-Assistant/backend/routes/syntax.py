from fastapi import APIRouter
from pydantic import BaseModel
from backend.models.file_model import (
    SyntaxValidationResult,
    LanguageDetectRequest,
    LanguageDetectResult
)
from backend.controllers.syntax_controller import SyntaxController

router = APIRouter(prefix="/api/syntax", tags=["Syntax & Language"])

class ValidateCodePayload(BaseModel):
    code: str
    language: str

@router.post("/validate", response_model=SyntaxValidationResult)
def validate_code(payload: ValidateCodePayload):
    return SyntaxController.validate_code(payload.code, payload.language)

@router.post("/detect", response_model=LanguageDetectResult)
def detect_language(req: LanguageDetectRequest):
    return SyntaxController.detect_language(req)
