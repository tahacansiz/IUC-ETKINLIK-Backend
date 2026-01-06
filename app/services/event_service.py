from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.event import Event
from app.schemas.event import EventCreate
from app.models.category import Category
from app.services.media_service import MediaService

class EventService:

    @staticmethod
    async def create_event(
        db: AsyncSession,
        event_in: EventCreate,
        creator_id: str
    ) -> Event:

        event = Event(
            title=event_in.title,
            description=event_in.description,
            event_date=event_in.event_date,
            location=event_in.location,
            creator_id=creator_id
        )

        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event
    
    @staticmethod
    async def list_events(db: AsyncSession) -> list[Event]:
        result = await db.execute(select(Event))
        events = result.scalars().all()
        return events
    

    @staticmethod
    async def get_event_by_id(db: AsyncSession, event_id: str) -> Event:
        result = await db.execute(
            select(Event).where(Event.id == event_id)
        )
        event = result.scalar_one_or_none()

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return event
        
    @staticmethod
    async def delete_event(
        db,
        event_id: str,
        requester_id: str
    ):
        result = await db.execute(
            select(Event).where(Event.id == event_id)
        )
        event = result.scalar_one_or_none()

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        # ❗ SAHİPLİK KONTROLÜ
        if event.creator_id != requester_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this event"
            )

        await db.delete(event)
        await db.commit()

    @staticmethod
    async def update_event(
        db,
        event_id: str,
        requester_id: str,
        event_in
    ):
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.creator_id != requester_id:
            raise HTTPException(status_code=403, detail="Not allowed")

        for field, value in event_in.model_dump(exclude_unset=True).items():
            setattr(event, field, value)

        await db.commit()
        await db.refresh(event)
        return event
    from app.models.category import Category

    @staticmethod
    async def assign_categories(
        db: AsyncSession,
        event_id: str,
        category_ids: list[str],
        requester_id: str
    ):
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(404, "Event not found")

        if event.creator_id != requester_id:
            raise HTTPException(403, "Not allowed")

        categories = (
            await db.execute(
                select(Category).where(Category.id.in_(category_ids))
            )
        ).scalars().all()

        event.categories = categories
        await db.commit()
        await db.refresh(event)
        return event
    
    @staticmethod
    async def upcoming_events(db, limit: int = 10):
        stmt = (
            select(Event)
            .where(Event.start_time >= datetime.utcnow())
            .order_by(Event.start_time.asc())
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()
    
    @staticmethod
    async def upload_event_poster(
        db,
        event_id: str,
        requester_id: str,
        file
    ):
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(404, "Event not found")

        if event.creator_id != requester_id:
            raise HTTPException(403, "Not allowed")

        poster_url = await MediaService.save_event_poster(file, event_id)

        event.poster_url = poster_url
        await db.commit()
        await db.refresh(event)
        return event