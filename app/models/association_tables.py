from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

event_categories = Table(
    "event_categories",
    Base.metadata,
    Column(
        "event_id",
        UUID(as_uuid=True),
        ForeignKey("events.id"),
        primary_key=True
    ),
    Column(
        "category_id",
        UUID(as_uuid=True),
        ForeignKey("categories.id"),
        primary_key=True
    )
)