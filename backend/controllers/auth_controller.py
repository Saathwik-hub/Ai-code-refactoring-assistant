import uuid
from datetime import datetime
from typing import Dict
from fastapi import HTTPException, status
from backend.models.user import UserRegister, UserLogin, UserResponse, TokenResponse

# In-memory storage for MVP auth users
USERS_DB: Dict[str, dict] = {
    "demo@developer.com": {
        "id": "usr_demo_001",
        "username": "demodev",
        "email": "demo@developer.com",
        "password": "password123",
        "created_at": datetime.now().isoformat()
    }
}

class AuthController:
    @staticmethod
    def register(data: UserRegister) -> TokenResponse:
        # Check if email or username exists
        for user in USERS_DB.values():
            if user["email"].lower() == data.email.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is already registered"
                )
            if user["username"].lower() == data.username.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username is already taken"
                )

        user_id = f"usr_{uuid.uuid4().hex[:8]}"
        created_at = datetime.now().isoformat()
        
        user_record = {
            "id": user_id,
            "username": data.username,
            "email": data.email,
            "password": data.password,
            "created_at": created_at
        }
        USERS_DB[data.email.lower()] = user_record
        USERS_DB[data.username.lower()] = user_record

        user_resp = UserResponse(
            id=user_id,
            username=data.username,
            email=data.email,
            created_at=created_at
        )

        return TokenResponse(
            access_token=f"mock_token_{user_id}",
            user=user_resp
        )

    @staticmethod
    def login(data: UserLogin) -> TokenResponse:
        key = data.username_or_email.lower()
        user_record = USERS_DB.get(key)
        
        if not user_record or user_record["password"] != data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username/email or password"
            )

        user_resp = UserResponse(
            id=user_record["id"],
            username=user_record["username"],
            email=user_record["email"],
            created_at=user_record["created_at"]
        )

        return TokenResponse(
            access_token=f"mock_token_{user_record['id']}",
            user=user_resp
        )
