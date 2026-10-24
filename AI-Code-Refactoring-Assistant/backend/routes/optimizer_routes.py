from typing import Optional
from fastapi import APIRouter, Query
from backend.models.optimizer_model import OptimizeCodeRequest, OptimizeCodeResponse
from backend.controllers.optimizer_controller import OptimizerController

router = APIRouter(prefix="/api/optimizer", tags=["Code Optimizer"])


@router.get("/ollama-status")
def get_ollama_status(url: Optional[str] = Query(None)):
    return OptimizerController.get_ollama_status(url)


@router.post("/run", response_model=OptimizeCodeResponse)
def run_optimizer(req: OptimizeCodeRequest):
    return OptimizerController.optimize_code(req)

