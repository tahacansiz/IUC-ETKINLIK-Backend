from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class EventStatus(str, Enum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"


class EventCreate(BaseModel):
    """Schema for creating a new event - matches frontend event creation"""
    title: str
    description: str | None = None
    dateTime: datetime = Field(alias="event_date")  # frontend sends dateTime
    location: str | None = None
    categoryId: str | None = Field(default=None, alias="category_id")  # frontend sends categoryId
    imageUrl: str | None = Field(default=None, alias="image_url")
    maxParticipants: int = Field(default=100, alias="max_participants")
    
    class Config:
        populate_by_name = True


class EventUpdate(BaseModel):
    """Schema for updating an event"""
    title: str | None = None
    description: str | None = None
    dateTime: datetime | None = Field(default=None, alias="event_date")
    location: str | None = None
    categoryId: str | None = Field(default=None, alias="category_id")
    imageUrl: str | None = Field(default=None, alias="image_url")
    maxParticipants: int | None = Field(default=None, alias="max_participants")
    status: EventStatus | None = None
    isFeatured: bool | None = Field(default=None, alias="is_featured")
    
    class Config:
        populate_by_name = True


class EventOut(BaseModel):
    """Schema for event response - matches frontend EventModel"""
    id: str
    title: str
    description: str | None = None
    dateTime: datetime = Field(serialization_alias="dateTime")
    location: str | None = None
    imageUrl: str | None = Field(default=None, serialization_alias="imageUrl")
    categoryId: str | None = Field(default=None, serialization_alias="categoryId")
    organizerId: str = Field(serialization_alias="organizerId")
    organizerName: str | None = Field(default=None, serialization_alias="organizerName")
    maxParticipants: int = Field(default=100, serialization_alias="maxParticipants")
    currentParticipants: int = Field(default=0, serialization_alias="currentParticipants")
    status: str = "upcoming"
    isFeatured: bool = Field(default=False, serialization_alias="isFeatured")
    createdAt: datetime = Field(serialization_alias="createdAt")

    class Config:
        from_attributes = True
        populate_by_name = True
    
    @classmethod
    def from_orm_model(cls, event) -> "EventOut":
        """Convert SQLAlchemy model to Pydantic schema with proper field mapping"""
        return cls(
            id=event.id,
            title=event.title,
            description=event.description,
            dateTime=event.event_date,
            location=event.location,
            imageUrl=event.image_url,
            categoryId=event.category_id,
            organizerId=event.creator_id,
            organizerName=event.organizer_name,
            maxParticipants=event.max_participants,
            currentParticipants=event.current_participants,
            status=event.status or "upcoming",
            isFeatured=event.is_featured or False,
            createdAt=event.created_at
        )