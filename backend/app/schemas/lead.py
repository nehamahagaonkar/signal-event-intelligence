from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class LeadBase(BaseModel):
    name: str
    company_id: int
    email: EmailStr
    event_id: int
    notes: str | None = None
    follow_up_status: str = "pending"


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    name: str | None = None
    company_id: int | None = None
    email: EmailStr | None = None
    event_id: int | None = None
    notes: str | None = None
    follow_up_status: str | None = None


class LeadResponse(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )