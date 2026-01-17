from sqlalchemy import Table, Column, ForeignKey, String
from app.models.base import Base

event_categories = Table(
    "event_categories",
    Base.metadata,
    Column(
        "event_id",
        String(36),
        ForeignKey("events.id"),
        primary_key=True
    ),
    Column(
        "category_id",
        String(36),
        ForeignKey("categories.id"),
        primary_key=True
    )
)