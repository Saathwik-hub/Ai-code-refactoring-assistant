from fastapi import APIRouter
from backend.models.user import UserRegister, UserLogin, TokenResponse
from backend.controllers.auth_controller import AuthController

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister):
    return AuthController.register(data)

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin):
    return AuthController.login(data)
