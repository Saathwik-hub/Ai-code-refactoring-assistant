from fastapi import HTTPException
from typing import Dict, Any, Optional
from backend.models.optimizer_model import OptimizeCodeRequest
from backend.services.ai.optimizer_engine import OptimizerEngine
from backend.services.ai.ollama_service import OllamaService


class OptimizerController:
    @staticmethod
    def get_ollama_status(url: Optional[str] = None) -> Dict[str, Any]:
        is_avail = OllamaService.is_ollama_available(url)
        models = OllamaService.get_installed_models(url) if is_avail else []
        best_model = OllamaService.get_best_model(None, url) if is_avail else None
        return {
            "available": is_avail,
            "models": models,
            "best_model": best_model,
            "endpoint": OllamaService._resolve_base_url(url)
        }

    @staticmethod
    def optimize_code(req: OptimizeCodeRequest) -> Dict[str, Any]:
        if not req.code or not req.code.strip():
            raise HTTPException(status_code=400, detail="Code body cannot be empty.")

        result = OptimizerEngine.optimize(
            code=req.code,
            language=req.language,
            model=req.model,
            ollama_url=req.ollama_url
        )
        return result

