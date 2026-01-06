from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.event import Event
from app.models.event_participant import EventParticipant
from sqlalchemy import select, and_, or_
from app.models.event import Event
from app.models.category import Category
from app.models.association_tables import event_categories
class EventQueryService:

    @staticmethod
    async def list_events(db: AsyncSession):
        result = await db.execute(
            select(Event)
        )
        return result.scalars().all()


    @staticmethod
    async def get_event_by_id(
        db: AsyncSession,
        event_id: str
    ) -> Event:

        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return event

    @staticmethod
    async def list_events_created_by_user(
        db: AsyncSession,
        user_id: str
    ):
        result = await db.execute(
            select(Event).where(Event.creator_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def list_events_joined_by_user(
        db: AsyncSession,
        user_id: str
    ):
        result = await db.execute(
            select(Event)
            .join(EventParticipant)
            .where(EventParticipant.user_id == user_id)
        )
        return result.scalars().all()
    
    @staticmethod
    async def list_participants(
        db: AsyncSession,
        event_id: str,
        requester_id: str
    ):
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        if requester_id == event.creator_id:
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to view participants"
            )

        # Katılımcıları getir
        result = await db.execute(
            select(EventParticipant).where(
                EventParticipant.event_id == event_id
            )
        )
        return result.scalars().all()
    @staticmethod
    async def search_events(
        db,
        query: str | None = None,
        category_ids: list[str] | None = None,
        start_date=None,
        end_date=None
    ):
        stmt = select(Event)

        if query:
            stmt = stmt.where(
                or_(
                    Event.title.ilike(f"%{query}%"),
                    Event.description.ilike(f"%{query}%")
                )
            )

        if category_ids:
            stmt = stmt.join(event_categories).where(
                event_categories.c.category_id.in_(category_ids)
            )

        if start_date:
            stmt = stmt.where(Event.start_time >= start_date)

        if end_date:
            stmt = stmt.where(Event.start_time <= end_date)

        result = await db.execute(stmt.distinct())
        return result.scalars().all()