from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Lead, Company, Event
from app.schemas import LeadCreate, LeadUpdate, LeadResponse


router = APIRouter(
    prefix="/leads",
    tags=["Leads"],
)


@router.post(
    "/",
    response_model=LeadResponse,
)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
):
    company = (
        db.query(Company)
        .filter(Company.id == lead.company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    event = (
        db.query(Event)
        .filter(Event.id == lead.event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    new_lead = Lead(
        **lead.model_dump()
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead


@router.get(
    "/",
    response_model=list[LeadResponse],
)
def get_leads(
    search: str | None = Query(
        default=None
    ),
    follow_up_status: str | None = Query(
        default=None
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Lead)

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            Lead.name.ilike(search_pattern)
            | Lead.email.ilike(search_pattern)
        )

    if follow_up_status:
        query = query.filter(
            Lead.follow_up_status
            == follow_up_status
        )

    return (
        query
        .order_by(Lead.created_at.desc())
        .all()
    )


@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
):
    lead = (
        db.query(Lead)
        .filter(Lead.id == lead_id)
        .first()
    )

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found",
        )

    return lead


@router.put(
    "/{lead_id}",
    response_model=LeadResponse,
)
def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    db: Session = Depends(get_db),
):
    lead = (
        db.query(Lead)
        .filter(Lead.id == lead_id)
        .first()
    )

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found",
        )

    update_data = lead_data.model_dump(
        exclude_unset=True
    )

    if "company_id" in update_data:
        company = (
            db.query(Company)
            .filter(
                Company.id
                == update_data["company_id"]
            )
            .first()
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

    if "event_id" in update_data:
        event = (
            db.query(Event)
            .filter(
                Event.id
                == update_data["event_id"]
            )
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found",
            )

    for key, value in update_data.items():
        setattr(lead, key, value)

    db.commit()
    db.refresh(lead)

    return lead


@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
):
    lead = (
        db.query(Lead)
        .filter(Lead.id == lead_id)
        .first()
    )

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found",
        )

    db.delete(lead)
    db.commit()

    return {
        "message": "Lead deleted successfully"
    }