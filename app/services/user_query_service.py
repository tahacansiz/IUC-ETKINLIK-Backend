from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.models.event import Event
from app.models.event_participant import EventParticipant

class UserQueryService:

    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: str
    ) -> User:

        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
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

