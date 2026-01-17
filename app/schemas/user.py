from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    full_name: str = Field(alias="fullName")
    email: EmailStr
    password: str
    
    class Config:
        populate_by_name = True


class UserOut(BaseModel):
    """Schema for user response - matches frontend UserModel"""
    id: str
    fullName: str = Field(serialization_alias="fullName")
    email: str
    role: str
    avatarUrl: str | None = Field(default=None, serialization_alias="avatarUrl")
    createdAt: datetime = Field(serialization_alias="createdAt")
    joinedEventIds: List[str] = Field(default_factory=list, serialization_alias="joinedEventIds")

    class Config:
        from_attributes = True
        populate_by_name = True
    
    @classmethod
    def from_orm_model(cls, user, joined_event_ids: List[str] = None) -> "UserOut":
        """Convert SQLAlchemy model to Pydantic schema with proper field mapping"""
        return cls(
            id=user.id,
            fullName=user.full_name,
            email=user.email,
            role=user.role or "student",
            avatarUrl=user.avatar_url,
            createdAt=user.created_at,
            joinedEventIds=joined_event_ids or []
        )
    
    @classmethod
    def model_validate(cls, user) -> "UserOut":
        """Validate and convert a User model to UserOut"""
        return cls(
            id=user.id,
            fullName=user.full_name,
            email=user.email,
            role=user.role or "student",
            avatarUrl=getattr(user, 'avatar_url', None),
            createdAt=getattr(user, 'created_at', datetime.utcnow()),
            joinedEventIds=[]
        )