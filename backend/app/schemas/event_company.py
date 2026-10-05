from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventCompanyCreate(BaseModel):
    event_id: int
    company_id: int


class EventCompanyResponse(EventCompanyCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)