import uuid
from sqlalchemy import Column, ForeignKey, DateTime, UniqueConstraint, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base

class EventParticipant(Base):
    __tablename__ = "event_participants"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    event_id = Column(
        String(36),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    joined_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    event = relationship("Event", back_populates="participants")
    user = relationship("User", back_populates="event_participations")

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "user_id",
            name="uq_event_user"
        ),
    )
