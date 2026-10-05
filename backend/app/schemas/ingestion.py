from datetime import datetime

from pydantic import BaseModel


class IngestEventRequest(BaseModel):
    company_id: int

    title: str
    description: str | None = None
    event_type: str | None = None
    source: str | None = None
    location: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    url: str | None = None
    organizer: str | None = None


class IngestEventResponse(BaseModel):
    event_id: int
    company_id: int
    signals_created: int
    signals: list[dict]