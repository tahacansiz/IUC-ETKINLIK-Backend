from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.services.user_query_service import UserQueryService
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserOut
from app.schemas.event import EventOut

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserOut)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user profile - matches frontend getCurrentUser()"""
    user = await UserQueryService.get_user_by_id(
        db=db,
        user_id=current_user.id
    )
    # Get joined event IDs
    joined_events = await UserQueryService.list_events_joined_by_user(db, current_user.id)
    joined_event_ids = [e.id for e in joined_events]
    
    return UserOut.from_orm_model(user, joined_event_ids)


@router.get("/me/events/created", response_model=List[EventOut])
async def my_created_events(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get events created by current user"""
    events = await UserQueryService.list_events_created_by_user(
        db=db,
        user_id=current_user.id
    )
    return [EventOut.from_orm_model(e) for e in events]


@router.get("/me/events/joined", response_model=List[EventOut])
async def my_joined_events(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get events joined by current user"""
    events = await UserQueryService.list_events_joined_by_user(
        db=db,
        user_id=current_user.id
    )
    return [EventOut.from_orm_model(e) for e in events]


# Alias for profile endpoint (frontend may use /users/profile)
@router.get("/profile", response_model=UserOut)
async def get_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Alias for /me - Get current user profile"""
    user = await UserQueryService.get_user_by_id(
        db=db,
        user_id=current_user.id
    )
    joined_events = await UserQueryService.list_events_joined_by_user(db, current_user.id)
    joined_event_ids = [e.id for e in joined_events]
    
    return UserOut.from_orm_model(user, joined_event_ids)
