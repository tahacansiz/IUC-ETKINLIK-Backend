import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Integer, Boolean
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.models.association_tables import event_categories

class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    event_date = Column(DateTime, nullable=False)  # maps to dateTime in frontend
    location = Column(String(255))
    image_url = Column(String(255))  # maps to imageUrl in frontend
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)  # single category for frontend compatibility
    status = Column(Enum("upcoming", "ongoing", "completed", "cancelled"), default="upcoming")
    creator_id = Column(String(36), ForeignKey("users.id"), nullable=False)  # maps to organizerId
    organizer_name = Column(String(100), nullable=True)  # frontend needs this
    max_participants = Column(Integer, default=100)
    current_participants = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    poster_url = Column(String(255), nullable=True)
    
    # Relationships
    categories = relationship(
        "Category",
        secondary=event_categories,
        back_populates="events"
    )
    creator = relationship("User", back_populates="created_events")
    participants = relationship("EventParticipant", back_populates="event")
