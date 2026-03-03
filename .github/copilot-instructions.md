# Habit Tracker MVP

Full-stack web application to help users build and maintain positive habits with quick daily tracking and immediate visual progress feedback.

## Tech Stack

- **Backend**: Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Uvicorn, Alembic
- **Frontend**: React 18+, Vite 5+, Tailwind CSS 3+, TanStack Query
- **Testing**: pytest, httpx, pytest-asyncio, Vitest, React Testing Library, Playwright (optional)
- **Other**: SQLite, structlog, Ruff, Black, ESLint, Prettier

## Project Structure

```
habit-tracker-code/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── habits/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   └── service.py
│   │   └── stats/
│   │       └── service.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── features/
│   │   │   ├── habits/
│   │   │   └── dashboard/
│   │   ├── components/
│   │   │   └── ui/
│   │   ├── lib/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .github/
│   ├── instructions/
│   └── skills/
├── .vscode/
│   └── mcp.json
└── PRD.md
```

## Commands

```bash
# Install dependencies
cd backend && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
cd frontend && npm install

# Run development server
cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000
cd frontend && npm run dev

# Run tests
cd backend && .venv\Scripts\activate && pytest
cd frontend && npm run test

# Build for production
cd frontend && npm run build
cd backend && .venv\Scripts\activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Reference Documentation

| Document | When to Read |
|----------|--------------|
| `PRD.md` | Product requirements, MVP scope, and API behavior |
| `.github/instructions/fastapi-best-practices.instructions.md` | Backend architecture, routing, validation, and FastAPI patterns |
| `.github/instructions/react-frontend-best-practices.instructions.md` | Frontend feature structure, state management, and UI patterns |
| `.github/instructions/sqlite-best-practices.instructions.md` | SQLite schema design, constraints, indexing, and query guidance |
| `.github/instructions/testing-and-logging.instructions.md` | Testing pyramid, integration tests, and structured logging setup |
| `.github/instructions/deployment-best-practices.instructions.md` | Local/prod deployment flow for FastAPI + React |

## Code Conventions

### Backend
- Use domain-based modules: `habits`, `stats`, shared config/database.
- Keep route handlers thin; put business logic in service layer.
- Validate all request/response bodies with Pydantic schemas.
- Use explicit imports and clear function names (no wildcard imports).
- Prefer typed function signatures and return models.

### Frontend
- Use feature-based structure under `src/features/`.
- Keep components focused and reusable; place shared UI in `components/ui`.
- Use TanStack Query for server state and caching.
- Keep forms simple and optimized for fast daily interaction.
- Follow Tailwind utility-first styling; avoid ad-hoc inline styles unless necessary.

### API Design
- Base route prefix: `/api/v1`.
- Use RESTful resources (`/habits`, `/stats`, nested completion routes).
- Use appropriate status codes: `200`, `201`, `204`, `400`, `404`, `422`.
- Return consistent JSON error payloads using FastAPI conventions.
- Ensure completion writes are idempotent via upsert behavior.

## Logging

- Use `structlog` for structured logs.
- Bind request-level context (e.g., request id, method, path) in middleware.
- Use readable console logs in development and JSON logs in production.
- Log exceptions with stack traces in backend service/route boundaries.

## Database

- Use SQLite for MVP persistence.
- Core entities: `habits`, `habit_target_days` (or encoded schedule), `completions`.
- Enforce uniqueness for completion records by `(habit_id, completed_date)`.
- Enable foreign keys and use cascade delete for habit completions.
- Store dates in ISO format (`YYYY-MM-DD`) and datetimes in ISO UTC.

## Testing Strategy

### Testing Pyramid
- **Unit tests**: Habit and stats service logic (streaks, rates, schedule handling).
- **Integration tests**: FastAPI endpoint behavior with test database.
- **E2E tests**: Optional critical flow (create habit -> mark completion -> verify dashboard).

### Test Organization
```
backend/tests/
├── unit/
├── integration/
└── e2e/

frontend/src/
├── features/**/__tests__/
└── components/**/__tests__/
```
