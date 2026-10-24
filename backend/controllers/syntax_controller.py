from backend.models.file_model import (
    SyntaxValidationResult,
    LanguageDetectRequest,
    LanguageDetectResult
)
from backend.utils.syntax_checker import validate_syntax
from backend.utils.file_utils import detect_language_from_content

class SyntaxController:
    @staticmethod
    def validate_code(code: str, language: str) -> SyntaxValidationResult:
        raw_res = validate_syntax(code, language)
        return SyntaxValidationResult(**raw_res)

    @staticmethod
    def detect_language(req: LanguageDetectRequest) -> LanguageDetectResult:
        lang, conf = detect_language_from_content(req.code, req.filename)
        return LanguageDetectResult(detected_language=lang, confidence=conf)
