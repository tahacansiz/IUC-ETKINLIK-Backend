from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from fastapi import HTTPException, status
from app.models.event import Event
from app.models.event_participant import EventParticipant

class EventParticipationService:

    @staticmethod
    async def join_event(
        db: AsyncSession,
        event_id: str,
        user_id: str
    ):
        # Event var mı?
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        # Daha önce katılmış mı?
        result = await db.execute(
            select(EventParticipant).where(
                EventParticipant.event_id == event_id,
                EventParticipant.user_id == user_id
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already joined"
            )

        participation = EventParticipant(
            event_id=event_id,
            user_id=user_id
        )
        db.add(participation)
        await db.commit()

    @staticmethod
    async def leave_event(
        db: AsyncSession,
        event_id: str,
        user_id: str
    ):
        result = await db.execute(
            select(EventParticipant).where(
                EventParticipant.event_id == event_id,
                EventParticipant.user_id == user_id
            )
        )
        participation = result.scalar_one_or_none()

        if not participation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not joined"
            )

        await db.delete(participation)
        await db.commit()

    # @staticmethod
    # async def list_participants(
    #     db: AsyncSession,
    #     event_id: str
    # ):
    #     result = await db.execute(
    #         select(EventParticipant).where(
    #             EventParticipant.event_id == event_id
    #         )
    #     )
    #     return result.scalars().all()
