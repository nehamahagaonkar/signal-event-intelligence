from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Company, EventCompany, Signal
from app.services.scoring import (
    calculate_company_score,
    calculate_signal_score,
    calculate_recency_weight,
    calculate_diversity_bonus,

)


router = APIRouter(
    prefix="/scoring",
    tags=["Scoring"],
)


@router.get("/company/{company_id}")
def get_company_score(
    company_id: int,
    db: Session = Depends(get_db),
):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    event_ids = (
        db.query(EventCompany.event_id)
        .filter(EventCompany.company_id == company_id)
        .all()
    )

    event_ids = [
        event_id
        for (event_id,) in event_ids
    ]

    if not event_ids:
        return {
            "company_id": company_id,
            "company_name": company.name,
            "score": 0.0,
            "signals": [],
        }

    signals = (
        db.query(Signal)
        .filter(Signal.event_id.in_(event_ids))
        .all()
    )

    score = calculate_company_score(signals)
    return {
    "company_id": company.id,
    "company_name": company.name,
    "score": score,
    "diversity_bonus": calculate_diversity_bonus(
        signals
    ),
    "signals": [
        {
            "type": signal.signal_type,
            "value": signal.signal_value,
            "confidence": signal.confidence,
            "score": round(
                calculate_signal_score(
                    signal.signal_type,
                    signal.confidence,
                )
                * calculate_recency_weight(
                    signal.created_at
                ),
                3,
            ),
            "recency_weight": calculate_recency_weight(
                signal.created_at
            ),
        }
        for signal in signals
    ],
}


@router.get("/companies")
def get_company_scores(
    db: Session = Depends(get_db),
):
    companies = (
        db.query(Company)
        .order_by(Company.name)
        .all()
    )

    results = []

    for company in companies:
        event_ids = (
            db.query(EventCompany.event_id)
            .filter(
                EventCompany.company_id == company.id
            )
            .all()
        )

        event_ids = [
            event_id
            for (event_id,) in event_ids
        ]

        signals = []

        if event_ids:
            signals = (
                db.query(Signal)
                .filter(
                    Signal.event_id.in_(event_ids)
                )
                .all()
            )

        score = calculate_company_score(signals)

        results.append(
            {
                "company_id": company.id,
                "company_name": company.name,
                "score": score,
                "signal_count": len(signals),
                "event_ids": event_ids,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results