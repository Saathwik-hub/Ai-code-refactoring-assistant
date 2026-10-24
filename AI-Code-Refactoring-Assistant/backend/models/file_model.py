from pydantic import BaseModel, Field
from typing import List, Optional

class FileMetadata(BaseModel):
    id: str
    filename: str
    original_name: str
    extension: str
    language: str
    size_bytes: int
    uploaded_at: str
    content: Optional[str] = None

class CreateFileRequest(BaseModel):
    filename: str
    language: str
    content: str

class RenameFileRequest(BaseModel):
    new_filename: str

class SyntaxDiagnostic(BaseModel):
    line: Optional[int] = None
    column: Optional[int] = None
    message: str
    severity: str  # "error", "warning", "info"

class SyntaxValidationResult(BaseModel):
    is_valid: bool
    language: str
    diagnostics: List[SyntaxDiagnostic]
    error_count: int
    warning_count: int
    summary: str

class LanguageDetectRequest(BaseModel):
    filename: Optional[str] = None
    code: str

class LanguageDetectResult(BaseModel):
    detected_language: str
    confidence: float
