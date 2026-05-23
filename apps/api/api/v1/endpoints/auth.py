from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from core.security import hash_password, verify_password, create_access_token, create_refresh_token

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    """Register a new user."""
    # TODO: Implement user creation logic
    # For now, just return dummy tokens
    access_token = create_access_token({"sub": request.email})
    refresh_token = create_refresh_token({"sub": request.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login user."""
    # TODO: Implement login logic
    # For now, just return dummy tokens
    access_token = create_access_token({"sub": request.email})
    refresh_token = create_refresh_token({"sub": request.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Refresh access token."""
    # TODO: Implement refresh logic
    access_token = create_access_token({"sub": "user@example.com"})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/logout")
async def logout():
    """Logout user."""
    return {"message": "Logged out successfully"}
