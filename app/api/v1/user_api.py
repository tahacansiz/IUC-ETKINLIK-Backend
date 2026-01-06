from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.user_query_service import UserQueryService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users")

@router.get("/me")
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await UserQueryService.get_user_by_id(
        db=db,
        user_id=current_user.id
    )


@router.get("/me/events/created")
async def my_created_events(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await UserQueryService.list_events_created_by_user(
        db=db,
        user_id=current_user.id
    )


@router.get("/me/events/joined")
async def my_joined_events(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await UserQueryService.list_events_joined_by_user(
        db=db,
        user_id=current_user.id
    )
