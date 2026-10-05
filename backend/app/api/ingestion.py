from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event, Company, EventCompany, Signal
from app.schemas import IngestEventRequest, IngestEventResponse
from app.services.signal_extractor import extract_signals


router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"],
)


@router.post(
    "/event",
    response_model=IngestEventResponse,
)
def ingest_event(
    event_data: IngestEventRequest,
    db: Session = Depends(get_db),
):
    # Check company
    company = (
        db.query(Company)
        .filter(Company.id == event_data.company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    # Create event
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        event_type=event_data.event_type,
        source=event_data.source,
        location=event_data.location,
        start_time=event_data.start_time,
        end_time=event_data.end_time,
        url=event_data.url,
        organizer=event_data.organizer,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    # Connect event to company
    event_company = EventCompany(
        event_id=new_event.id,
        company_id=company.id,
    )

    db.add(event_company)

    # Extract signals automatically
    extracted_signals = extract_signals(
        title=new_event.title,
        description=new_event.description,
    )

    created_signals = []

    for extracted in extracted_signals:
        signal = Signal(
            event_id=new_event.id,
            signal_type=extracted["signal_type"],
            signal_value=extracted["signal_value"],
            confidence=extracted["confidence"],
        )

        db.add(signal)
        created_signals.append(extracted)

    db.commit()

    return {
        "event_id": new_event.id,
        "company_id": company.id,
        "signals_created": len(created_signals),
        "signals": created_signals,
    }