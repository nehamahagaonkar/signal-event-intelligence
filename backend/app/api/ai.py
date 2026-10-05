from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Lead
from app.services.ai_service import (
    summarize_notes,
    draft_follow_up,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/leads/{lead_id}/summary")
def generate_lead_summary(
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

    if not lead.notes or not lead.notes.strip():
        raise HTTPException(
            status_code=400,
            detail="Lead has no interaction notes",
        )

    try:
        summary = summarize_notes(lead.notes)

        return {
            "lead_id": lead.id,
            "summary": summary,
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )


@router.post("/leads/{lead_id}/follow-up")
def generate_lead_follow_up(
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

    if not lead.notes or not lead.notes.strip():
        raise HTTPException(
            status_code=400,
            detail="Lead has no interaction notes",
        )

    try:
        message = draft_follow_up(
            name=lead.name,
            notes=lead.notes,
        )

        return {
            "lead_id": lead.id,
            "follow_up": message,
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )