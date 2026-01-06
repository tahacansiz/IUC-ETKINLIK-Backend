from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.event import EventCreate
from app.services.event_service import EventService
from app.services.event_query_service import EventQueryService
from app.api.deps import get_current_user
from app.models.user import User
from fastapi import UploadFile, File


router = APIRouter()

@router.post("/")
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.create_event(
        db=db,
        event_in=event_in,
        creator_id=current_user.id
    )

@router.get("/")
async def list_events(
    db: AsyncSession = Depends(get_db)
):
    return await EventQueryService.list_events(db)

@router.get("/{event_id}")
async def get_event(
    event_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await EventQueryService.get_event_by_id(db, event_id)

@router.delete("/{event_id}")
async def delete_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await EventService.delete_event(
        db=db,
        event_id=event_id,
        requester_id=current_user.id
    )
    return {"detail": "Event deleted"}

@router.put("/{event_id}")
async def update_event(
    event_id: str,
    event_in: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.update_event(
        db=db,
        event_id=event_id,
        requester_id=current_user.id,
        event_in=event_in
    )

@router.put("/{event_id}/categories")
async def update_event_categories(
    event_id: str,
    category_ids: list[str],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.assign_categories(
        db=db,
        event_id=event_id,
        category_ids=category_ids,
        requester_id=current_user.id
    )

@router.get("/search")
async def search_events(
    q: Optional[str] = None,
    categories: Optional[List[str]] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    return await EventQueryService.search_events(
        db=db,
        query=q,
        category_ids=categories,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/upcoming")
async def upcoming_events(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    return await EventQueryService.upcoming_events(db, limit)

@router.post("/{event_id}/poster")
async def upload_event_poster(
    event_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.upload_event_poster(
        db=db,
        event_id=event_id,
        requester_id=current_user.id,
        file=file
    )
