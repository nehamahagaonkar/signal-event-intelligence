from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event, Company, EventCompany
from app.schemas import EventCompanyCreate, EventCompanyResponse


router = APIRouter(
    prefix="/event-companies",
    tags=["Event Companies"],
)


@router.post("/", response_model=EventCompanyResponse)
def create_event_company(
    relationship: EventCompanyCreate,
    db: Session = Depends(get_db),
):
    event = (
        db.query(Event)
        .filter(Event.id == relationship.event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    company = (
        db.query(Company)
        .filter(Company.id == relationship.company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    existing = (
        db.query(EventCompany)
        .filter(
            EventCompany.event_id == relationship.event_id,
            EventCompany.company_id == relationship.company_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Event is already linked to this company",
        )

    new_relationship = EventCompany(
        event_id=relationship.event_id,
        company_id=relationship.company_id,
    )

    db.add(new_relationship)
    db.commit()
    db.refresh(new_relationship)

    return new_relationship


@router.get("/", response_model=list[EventCompanyResponse])
def get_event_companies(
    db: Session = Depends(get_db),
):
    return db.query(EventCompany).all()