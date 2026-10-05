# Signal Intelligence — Event Lead Manager

> A full-stack AI-powered event lead management platform that turns event conversations and business signals into structured, actionable follow-up workflows.

[![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)](https://www.postgresql.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-4285F4?logo=google)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

**Live application:** https://signal-event-intelligence.vercel.app
**API documentation:** https://signal-event-intelligence.onrender.com/docs

---

## Overview

Signal Intelligence is a lightweight CRM-style application designed for managing leads captured through events and networking interactions.

The platform combines a clean responsive interface with a FastAPI backend, PostgreSQL persistence, rule-based signal extraction, opportunity scoring, and a server-side Gemini integration for AI-assisted lead workflows.

The core workflow is simple:

**Capture → Organize → Understand → Follow Up**

A user can create and manage leads, associate them with companies and events, search and filter their pipeline, summarize interaction notes with AI, and generate personalized follow-up messages.

---

## Key Features

### Lead Management
- Create new event leads
- Edit existing leads
- Delete leads
- Search by name or email
- Filter by follow-up status
- Track `pending`, `contacted`, `followed_up`, and `converted` stages
- Associate every lead with a company and event

### AI-Assisted Workflows
- Generate concise interaction summaries
- Draft personalized follow-up messages
- Copy generated follow-up messages directly from the interface
- AI requests are handled server-side so API credentials are never exposed to the browser

### Event Intelligence Backend
- Event ingestion endpoint
- Rule-based signal extraction for funding, hiring, expansion, product launches, and partnerships
- Confidence-weighted signal scoring
- Recency weighting
- Signal diversity bonus
- Company opportunity scoring

### Production Architecture
- Next.js frontend deployed on Vercel
- FastAPI backend deployed on Render
- Managed PostgreSQL database on Neon
- Gemini API used for production AI generation

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL 16 |
| Database Hosting | Neon |
| Backend Hosting | Render |
| Frontend Hosting | Vercel |
| AI | Google Gemini 2.5 Flash |
| Local Development | Docker, PostgreSQL, Ollama (legacy/local option) |
| API Docs | FastAPI / Swagger UI |
| Version Control | Git + GitHub |

---

## Architecture

```text
                           ┌─────────────────────────┐
                           │        GitHub            │
                           │      Source Code        │
                           └────────────┬────────────┘
                                        │
                       ┌────────────────┴────────────────┐
                       │                                 │
                       ▼                                 ▼
             ┌──────────────────┐             ┌──────────────────┐
             │      Vercel      │             │      Render      │
             │  Next.js Frontend│────────────►│ FastAPI Backend  │
             └──────────────────┘             └────────┬─────────┘
                                                       │
                                      ┌────────────────┼────────────────┐
                                      │                │                │
                                      ▼                ▼                ▼
                              ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
                              │     Neon     │  │    Gemini    │  │   Scoring    │
                              │ PostgreSQL   │  │    API       │  │   Service    │
                              └──────────────┘  └──────────────┘  └──────────────┘
```

### Request Flow

1. The browser loads the Next.js application from Vercel.
2. The frontend calls the FastAPI REST API hosted on Render.
3. FastAPI reads and writes application data in Neon PostgreSQL.
4. AI endpoints send lead notes to Gemini 2.5 Flash and return the generated result.
5. The frontend renders the response without exposing the Gemini API key.

---

## Project Structure

```text
signal-event-intelligence/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── ai.py
│   │   │   ├── companies.py
│   │   │   ├── event_companies.py
│   │   │   ├── events.py
│   │   │   ├── ingestion.py
│   │   │   ├── leads.py
│   │   │   ├── scoring.py
│   │   │   └── signals.py
│   │   │
│   │   ├── models/
│   │   │   ├── company.py
│   │   │   ├── event.py
│   │   │   ├── event_company.py
│   │   │   ├── lead.py
│   │   │   └── signal.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── company.py
│   │   │   ├── event.py
│   │   │   ├── event_company.py
│   │   │   ├── ingestion.py
│   │   │   ├── lead.py
│   │   │   └── signal.py
│   │   │
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── scoring.py
│   │   │   └── signal_extractor.py
│   │   │
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env                  # local only — never commit
│
├── frontend/
│   ├── app/
│   │   └── page.tsx
│   ├── package.json
│   └── package-lock.json
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Data Model

The backend is organized around five primary entities:

```text
Company
   │
   ├───────────────┐
   │               │
   ▼               ▼
Event          EventCompany
   │
   ├───────────────┐
   │               │
   ▼               ▼
Signal           Lead
```

### Core tables

| Table | Purpose |
|---|---|
| `companies` | Stores organizations associated with events and leads |
| `events` | Stores event and networking context |
| `event_companies` | Links events to companies |
| `signals` | Stores extracted business signals and confidence values |
| `leads` | Stores contact, notes, event, company, and follow-up status |

---

## Opportunity Scoring

The backend includes a lightweight scoring service that turns individual signals into a company-level opportunity score.

The current model uses:

- **Signal type weight** — funding, expansion, hiring, product launch, and partnership signals have different importance levels.
- **Confidence** — signal scores are scaled by extraction confidence.
- **Recency** — newer signals receive a stronger weight.
- **Signal diversity** — companies showing multiple distinct signal types receive a small bonus.

Conceptually:

```text
Signal Score = Signal Weight × Confidence × Recency Weight

Company Score = Average Weighted Signal Score + Diversity Bonus
```

The score is capped at `1.0` so it remains easy to interpret as a normalized opportunity score.

---

## Signal Extraction

The ingestion service currently uses a transparent rule-based extractor rather than a black-box classifier.

Supported signal categories include:

| Signal | Example keywords |
|---|---|
| Funding | funding, raised, Series B, investment |
| Hiring | hiring, recruiting, jobs, talent |
| Expansion | expansion, new office, new market |
| Product Launch | launch, released, new product |
| Partnership | partnership, collaboration, agreement |

Each detected signal is stored with a confidence value and a short explanation of the matched keywords.

This approach was intentionally chosen because it is:

- Fast
- Explainable
- Easy to debug
- Easy to extend with additional signal rules

A learned NLP model can be introduced later without changing the rest of the API architecture.

---

## AI Integration

The production application uses **Google Gemini 2.5 Flash** through the Google GenAI Python SDK.

### Current AI workflows

**Interaction Summary**

Takes event notes and returns a concise summary focused on:
- what was discussed
- the lead's interest
- the next meaningful step

**Follow-up Draft**

Uses the lead's name and interaction notes to create a short, personalized follow-up message without inventing information.

### Security model

The frontend never receives the Gemini API key.

```text
Browser
   ↓
POST /ai/leads/{id}/summary
   ↓
FastAPI
   ↓
GEMINI_API_KEY (server environment variable)
   ↓
Gemini API
```

---

## API Endpoints

### Health

```text
GET /health
```

### Events

```text
GET  /events/
POST /events/
GET  /events/{event_id}
```

### Companies

```text
GET  /companies/
POST /companies/
GET  /companies/{company_id}
```

### Event–Company Links

```text
GET  /event-companies/
POST /event-companies/
```

### Signals

```text
GET  /signals/
POST /signals/
GET  /signals/event/{event_id}
```

### Ingestion

```text
POST /ingest/event
```

Creates an event, associates it with a company, extracts matching signals, and stores them.

### Scoring

```text
GET /scoring/company/{company_id}
GET /scoring/companies
```

### Leads

```text
GET    /leads/
POST   /leads/
GET    /leads/{lead_id}
PUT    /leads/{lead_id}
DELETE /leads/{lead_id}
```

Search and filtering are supported through query parameters such as:

```text
GET /leads/?search=aarav
GET /leads/?follow_up_status=pending
```

### AI

```text
POST /ai/leads/{lead_id}/summary
POST /ai/leads/{lead_id}/follow-up
```

Interactive API documentation is available through FastAPI Swagger UI at:

https://signal-event-intelligence.onrender.com/docs

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop
- Git
- A Google Gemini API key for AI functionality

### 1. Clone the repository

```bash
git clone https://github.com/nehamahagaonkar/signal-event-intelligence.git
cd signal-event-intelligence
```

### 2. Start PostgreSQL with Docker

```bash
docker compose up -d
```

The local database is exposed on:

```text
localhost:5433
```

### 3. Configure the backend

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql+psycopg2://signal_user:signal_dev_password@localhost:5433/signal_db
GEMINI_API_KEY=your_gemini_api_key
```

Never commit this file.

### 4. Install backend dependencies

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 5. Run FastAPI

```powershell
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### 6. Install frontend dependencies

```powershell
cd ..\frontend
npm install
```

### 7. Configure the frontend API URL

For local development, the frontend falls back to:

```text
http://127.0.0.1:8000
```

For production, set:

```env
NEXT_PUBLIC_API_URL=https://signal-event-intelligence.onrender.com
```

### 8. Run Next.js

```powershell
npm run dev
```

Open:

```text
http://localhost:3000
```

---

## Production Deployment

The current production deployment uses three services:

### Frontend — Vercel

The `frontend/` directory is deployed as a Next.js application.

Required environment variable:

```text
NEXT_PUBLIC_API_URL=https://signal-event-intelligence.onrender.com
```

### Backend — Render

The `backend/` directory is deployed as a Python Web Service.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Required environment variables:

```text
DATABASE_URL=<Neon PostgreSQL connection string>
GEMINI_API_KEY=<Gemini API key>
```

### Database — Neon

The hosted PostgreSQL database is used only by the production backend. Local development can continue using Docker PostgreSQL.

---

## Environment Variables

| Variable | Used by | Sensitive | Description |
|---|---|---:|---|
| `DATABASE_URL` | Backend | Yes | PostgreSQL connection string |
| `GEMINI_API_KEY` | Backend | Yes | Gemini API authentication key |
| `NEXT_PUBLIC_API_URL` | Frontend | No | Public URL of the FastAPI backend |

### Security rule

Do not commit secrets to GitHub.

The repository ignores:

```text
.env
backend/.env
frontend/node_modules/
frontend/.next/
backend/.venv/
```

---

## Design Decisions

### Why FastAPI?

FastAPI provides typed request validation, automatic OpenAPI documentation, and a clean structure for separating routing, services, models, and schemas.

### Why PostgreSQL?

The application has several related entities — companies, events, signals, and leads — making a relational database a natural fit.

### Why a lightweight scoring system?

The scoring engine is intentionally transparent. A reviewer can inspect the weights, confidence, recency logic, and diversity bonus instead of relying on an opaque prediction.

### Why server-side AI?

AI credentials belong on the backend. Keeping Gemini calls inside FastAPI prevents the API key from being exposed in the browser bundle.

### Why a simple UI?

The product is designed around the core user task: quickly reviewing event leads and deciding what to do next. The interface prioritizes readability, clear status indicators, and minimal interaction overhead.

---

## Error Handling

The backend includes explicit validation and HTTP error handling for common cases such as:

- Missing companies
- Missing events
- Missing leads
- Duplicate company creation
- Duplicate event-company associations
- Leads without interaction notes for AI generation
- Missing AI configuration
- AI provider connection failures

The frontend also provides loading and failure feedback during AI generation.

---

## Testing Checklist

Before submitting or demonstrating the application, verify:

- [ ] Homepage loads successfully
- [ ] Leads are fetched from the production API
- [ ] New leads can be created
- [ ] Existing leads can be edited
- [ ] Leads can be deleted
- [ ] Search works
- [ ] Status filtering works
- [ ] AI summary generates successfully
- [ ] AI follow-up generates successfully
- [ ] Generated follow-up can be copied
- [ ] `/health` returns `{"status":"ok"}`
- [ ] Swagger `/docs` loads successfully
- [ ] Production database persists changes after refresh

---

## Future Improvements

The current implementation intentionally focuses on a small, working product. Natural next steps include:

- Authentication and role-based access
- Pagination for large lead lists
- Richer company intelligence views
- Background AI jobs for long-running generations
- More advanced NLP-based signal extraction
- CRM integrations such as HubSpot or Salesforce
- Email sending and follow-up scheduling
- Analytics for conversion rates and pipeline performance
- Automated event ingestion from external sources

---

## Project Goal

This project was built as a practical demonstration of full-stack development, API design, relational data modeling, deployment, and AI integration in a single product workflow.

The central product idea is straightforward:

> **Event interactions contain valuable signals. Structure those signals, connect them to leads, and use AI to make the next action easier.**

---

## Author

**Neha Mahagaonkar**  
MSc Data Science and AI
Mithibai College, Mumbai 

GitHub: https://github.com/nehamahagaonkar

---

## License

This project is licensed under the MIT License.
