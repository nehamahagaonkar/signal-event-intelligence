from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event, Signal
from app.schemas import SignalCreate, SignalResponse

from app.services.scoring import (
    calculate_company_score,
    calculate_signal_score,
    calculate_recency_weight,
    calculate_diversity_bonus,
)
router = APIRouter(
    prefix="/signals",
    tags=["Signals"],
)


@router.post("/", response_model=SignalResponse)
def create_signal(
    signal: SignalCreate,
    db: Session = Depends(get_db),
):
    event = db.query(Event).filter(Event.id == signal.event_id).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    new_signal = Signal(**signal.model_dump())

    db.add(new_signal)
    db.commit()
    db.refresh(new_signal)

    return new_signal


@router.get("/", response_model=list[SignalResponse])
def get_signals(
    db: Session = Depends(get_db),
):
    return db.query(Signal).order_by(Signal.created_at.desc()).all()


@router.get("/event/{event_id}", response_model=list[SignalResponse])
def get_event_signals(
    event_id: int,
    db: Session = Depends(get_db),
):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return (
        db.query(Signal)
        .filter(Signal.event_id == event_id)
        .order_by(Signal.created_at.desc())
        .all()
    )