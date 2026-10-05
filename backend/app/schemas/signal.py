from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SignalBase(BaseModel):
    signal_type: str
    signal_value: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class SignalCreate(SignalBase):
    event_id: int


class SignalResponse(SignalBase):
    id: int
    event_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)