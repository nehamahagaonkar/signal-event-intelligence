from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    title: str
    description: str | None = None
    event_type: str | None = None
    source: str | None = None
    location: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    url: str | None = None
    organizer: str | None = None


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)