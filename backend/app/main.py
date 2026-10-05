from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models import (
    Event,
    Signal,
    Company,
    EventCompany,
    Lead,
)

from app.api.events import router as events_router
from app.api.signals import router as signals_router
from app.api.companies import router as companies_router
from app.api.event_companies import router as event_companies_router
from app.api.scoring import router as scoring_router
from app.api.ingestion import router as ingestion_router
from app.api.leads import router as leads_router
from app.api.ai import router as ai_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Signal API",
    description="Event Lead Intelligence API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://signal-event-intelligence-q3rk2i0nq-neham1.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router)
app.include_router(signals_router)
app.include_router(companies_router)
app.include_router(event_companies_router)
app.include_router(scoring_router)
app.include_router(ingestion_router)
app.include_router(leads_router)
app.include_router(ai_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
