from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.event import EventCreate, EventUpdate, EventOut
from app.services.event_service import EventService
from app.services.event_query_service import EventQueryService
from app.api.deps import get_current_user
from app.models.user import User
from fastapi import UploadFile, File


router = APIRouter()


@router.post("/", response_model=EventOut)
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new event"""
    event = await EventService.create_event(
        db=db,
        event_in=event_in,
        creator_id=current_user.id,
        organizer_name=current_user.full_name
    )
    return EventOut.from_orm_model(event)


@router.get("/", response_model=List[EventOut])
async def list_events(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    categoryId: Optional[str] = None,
    search: Optional[str] = None,
    startDate: Optional[datetime] = None,
    endDate: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all events with optional filters"""
    events = await EventQueryService.list_events(
        db=db,
        page=page,
        limit=limit,
        category_id=categoryId,
        search_query=search,
        start_date=startDate,
        end_date=endDate
    )
    return [EventOut.from_orm_model(e) for e in events]


@router.get("/featured", response_model=List[EventOut])
async def featured_events(
    db: AsyncSession = Depends(get_db)
):
    """Get featured events"""
    events = await EventQueryService.get_featured_events(db)
    return [EventOut.from_orm_model(e) for e in events]


@router.get("/upcoming", response_model=List[EventOut])
async def upcoming_events(
    limit: int = Query(5, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get upcoming events"""
    events = await EventQueryService.get_upcoming_events(db, limit)
    return [EventOut.from_orm_model(e) for e in events]


@router.get("/search", response_model=List[EventOut])
async def search_events(
    q: Optional[str] = None,
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """Search events"""
    events = await EventQueryService.search_events(
        db=db,
        query=q,
        category_ids=categories,
        start_date=start_date,
        end_date=end_date
    )
    return [EventOut.from_orm_model(e) for e in events]


@router.get("/{event_id}", response_model=EventOut)
async def get_event(
    event_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a single event by ID"""
    event = await EventQueryService.get_event_by_id(db, event_id)
    return EventOut.from_orm_model(event)


@router.delete("/{event_id}")
async def delete_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an event"""
    await EventService.delete_event(
        db=db,
        event_id=event_id,
        requester_id=current_user.id
    )
    return {"detail": "Event deleted"}


@router.put("/{event_id}", response_model=EventOut)
async def update_event(
    event_id: str,
    event_in: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an event"""
    event = await EventService.update_event(
        db=db,
        event_id=event_id,
        requester_id=current_user.id,
        event_in=event_in
    )
    return EventOut.from_orm_model(event)


@router.put("/{event_id}/categories")
async def update_event_categories(
    event_id: str,
    category_ids: list[str],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update event categories"""
    return await EventService.assign_categories(
        db=db,
        event_id=event_id,
        category_ids=category_ids,
        requester_id=current_user.id
    )


@router.post("/{event_id}/poster")
async def upload_event_poster(
    event_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload event poster image"""
    return await EventService.upload_event_poster(
        db=db,
        event_id=event_id,
        requester_id=current_user.id,
        file=file
    )
