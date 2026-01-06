import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.models.association_tables import event_categories

class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(255))
    image_url = Column(String(255))
    status = Column(Enum("pending", "approved", "rejected"), default="pending")
    creator_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    categories = relationship(
        "Category",
        secondary=event_categories,
        back_populates="events"
    )
    poster_url = Column(String(255), nullable=True)
