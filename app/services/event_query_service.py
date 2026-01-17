from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.event import Event
from app.models.event_participant import EventParticipant
from sqlalchemy import select, and_, or_
from app.models.category import Category
from app.models.association_tables import event_categories


class EventQueryService:

    @staticmethod
    async def list_events(
        db: AsyncSession,
        page: int = 1,
        limit: int = 20,
        category_id: str = None,
        search_query: str = None,
        start_date: datetime = None,
        end_date: datetime = None
    ):
        """List events with pagination and filters - matches frontend getEvents()"""
        stmt = select(Event)
        
        # Category filter
        if category_id:
            stmt = stmt.where(Event.category_id == category_id)
        
        # Search filter
        if search_query:
            stmt = stmt.where(
                or_(
                    Event.title.ilike(f"%{search_query}%"),
                    Event.description.ilike(f"%{search_query}%"),
                    Event.location.ilike(f"%{search_query}%")
                )
            )
        
        # Date range filter
        if start_date:
            stmt = stmt.where(Event.event_date >= start_date)
        if end_date:
            stmt = stmt.where(Event.event_date <= end_date)
        
        # Order by date
        stmt = stmt.order_by(Event.event_date.asc())
        
        # Pagination
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()


    @staticmethod
    async def get_event_by_id(
        db: AsyncSession,
        event_id: str
    ) -> Event:
        """Get event by ID - matches frontend getEventById()"""
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etkinlik bulunamadı"
            )
        return event

    @staticmethod
    async def get_featured_events(db: AsyncSession):
        """Get featured events - matches frontend getFeaturedEvents()"""
        result = await db.execute(
            select(Event).where(Event.is_featured == True).order_by(Event.event_date.asc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_upcoming_events(db: AsyncSession, limit: int = 5):
        """Get upcoming events - matches frontend getUpcomingEvents()"""
        now = datetime.utcnow()
        result = await db.execute(
            select(Event)
            .where(Event.event_date >= now)
            .order_by(Event.event_date.asc())
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def list_events_created_by_user(
        db: AsyncSession,
        user_id: str
    ):
        """Get events created by a user"""
        result = await db.execute(
            select(Event).where(Event.creator_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def list_events_joined_by_user(
        db: AsyncSession,
        user_id: str
    ):
        """Get events a user has joined"""
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
        """Get event participants (only event creator can view)"""
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        if requester_id != event.creator_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to view participants"
            )

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
        """Search events with filters"""
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
            stmt = stmt.where(Event.event_date >= start_date)

        if end_date:
            stmt = stmt.where(Event.event_date <= end_date)

        result = await db.execute(stmt.distinct())
        return result.scalars().all()