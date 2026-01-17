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
        """Join an event - matches frontend joinEvent()"""
        # Event var mı?
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etkinlik bulunamadı"
            )

        # Check if event is full
        if event.current_participants >= event.max_participants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Etkinlik dolu"
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
                detail="Zaten katıldınız"
            )

        participation = EventParticipant(
            event_id=event_id,
            user_id=user_id
        )
        db.add(participation)
        
        # Increment participant count
        event.current_participants += 1
        
        await db.commit()
        return {"success": True, "message": "Etkinliğe katıldınız"}

    @staticmethod
    async def leave_event(
        db: AsyncSession,
        event_id: str,
        user_id: str
    ):
        """Leave an event - matches frontend leaveEvent()"""
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etkinlik bulunamadı"
            )

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
                detail="Bu etkinliğe katılmamışsınız"
            )

        await db.delete(participation)
        
        # Decrement participant count
        if event.current_participants > 0:
            event.current_participants -= 1
        
        await db.commit()
        return {"success": True, "message": "Etkinlikten ayrıldınız"}
