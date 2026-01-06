from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str | None = None
    event_date: datetime
    location: str | None = None