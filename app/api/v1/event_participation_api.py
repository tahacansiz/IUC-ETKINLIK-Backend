from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.event_participation_service import EventParticipationService
from app.services.event_query_service import EventQueryService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/events")


@router.post("/{event_id}/join")
async def join_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await EventParticipationService.join_event(
        db=db,
        event_id=event_id,
        user_id=current_user.id
    )
    return {"detail": "Joined event"}


@router.post("/{event_id}/leave")
async def leave_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await EventParticipationService.leave_event(
        db=db,
        event_id=event_id,
        user_id=current_user.id
    )
    return {"detail": "Left event"}


@router.get("/{event_id}/participants")
async def list_participants(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventQueryService.list_participants(
        db=db,
        event_id=event_id,
        requester_id=current_user.id
    )
