from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base
from app.models.association_tables import event_categories

class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    icon_name = Column(String(50), nullable=True)  # Maps to iconName in frontend
    color_hex = Column(String(10), nullable=True)  # Maps to colorHex in frontend

    events = relationship(
        "Event",
        secondary=event_categories,
        back_populates="categories"
    )