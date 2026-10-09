# StudyFlow

AI-powered time management and productivity web app for college students: day planner,
time-block system, Pomodoro focus engine, goals → milestones → tasks, calendar with break planner,
university portal (MUJ SLCM) sync, email sync, message-to-task webhooks and an LLM/voice engine.

## Stack

| Layer    | Tech                                                                 |
| -------- | -------------------------------------------------------------------- |
| Frontend | Next.js 14 (App Router, TypeScript), Tailwind CSS, TanStack Query    |
| Backend  | Python 3.10+, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2  |
| Database | PostgreSQL 16 (docker-compose)                                       |
| AI       | Provider-abstracted LLM client (Gemini default, OpenAI swappable)    |
| Scraping | Playwright (Python) — Phase 5                                        |

## Repository layout

```
backend/      FastAPI app (app/), Alembic migrations (alembic/), tests
frontend/     Next.js app (src/app, src/components, src/hooks, src/lib)
docker-compose.yml   Postgres for local development
.env.example         All environment variables (copy to .env)
```

## Local development

Prerequisites: Docker, Python 3.10+, Node 20+, [pnpm](https://pnpm.io), [uv](https://docs.astral.sh/uv/) (or pip).

```bash
cp .env.example .env            # edit SECRET_KEY etc. as needed
docker compose up -d            # Postgres on localhost:5432

# Backend
cd backend
uv venv .venv && uv pip install -e ".[dev]"      # or: python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/alembic upgrade head
.venv/bin/python -m app.db.seed                  # optional demo data (demo@studyflow.app / password123)
.venv/bin/uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
cp .env.example .env.local
pnpm install
pnpm dev                                         # http://localhost:3000
```

API docs: http://localhost:8000/docs

### Useful commands

```bash
# Backend
cd backend
.venv/bin/ruff check . && .venv/bin/ruff format .
.venv/bin/pytest
.venv/bin/alembic revision --autogenerate -m "describe change"

# Frontend
cd frontend
pnpm lint && pnpm exec tsc --noEmit
```

## Roadmap

1. **Phase 1** – architecture, DB schema, auth, dashboard shell ✅
2. **Phase 2** – CRUD for tasks, goals, calendar & block system
3. **Phase 3** – Pomodoro timer, focus mode, stats analytics
4. **Phase 4** – AI parsing engine, voice-to-event (Web Speech API), AI suggestions
5. **Phase 5** – Email OAuth sync, MUJ SLCM scraper, Telegram/Discord webhooks
