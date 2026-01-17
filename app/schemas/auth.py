from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserOut


class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Schema for register request - matches frontend register call"""
    full_name: str = Field(alias="fullName")
    email: EmailStr
    password: str
    role: str = "student"  # default to student
    
    class Config:
        populate_by_name = True


class TokenResponse(BaseModel):
    """Schema for token response"""
    token: str
    refresh_token: str | None = Field(default=None, alias="refreshToken")
    
    class Config:
        populate_by_name = True


class AuthResponse(BaseModel):
    """Schema for auth response - matches frontend AuthResult"""
    user: UserOut
    token: str