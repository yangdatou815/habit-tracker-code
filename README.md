# Habit Tracker MVP

Habit Tracker is a full-stack web application focused on quick daily habit logging with immediate progress visibility.

## Tech Stack

- Backend: Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, SQLite, structlog
- Frontend: React 18+, Vite 5+, Tailwind CSS, TanStack Query
- Testing: pytest, httpx, pytest-asyncio, Vitest, React Testing Library

## Project Structure

```text
habit-tracker-code/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── habits/
│   │   └── stats/
│   ├── alembic/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── features/
│   │   ├── components/ui/
│   │   └── lib/
│   ├── package.json
│   └── vite.config.js
├── .github/
│   ├── instructions/
│   └── skills/
└── PRD.md
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Validation Commands

### Backend

```bash
cd backend
.venv\Scripts\ruff check .
.venv\Scripts\black --check .
.venv\Scripts\pytest -q tests
```

### Frontend

```bash
cd frontend
npm run build
npm run test -- --run
```

## Phase 2 Capabilities

Implemented core Habit & Completion workflows:

- Habit CRUD APIs and dashboard form/actions
- Completion upsert (`done` / `not_done`) from dashboard toggle
- Query-based refresh through TanStack Query invalidation
- Backend integration tests for core API paths

### Core API Endpoints

- `GET /api/v1/habits`
- `POST /api/v1/habits`
- `GET /api/v1/habits/{habit_id}`
- `PATCH /api/v1/habits/{habit_id}`
- `DELETE /api/v1/habits/{habit_id}`
- `PUT /api/v1/habits/{habit_id}/completions/{date}`
- `GET /api/v1/habits/{habit_id}/completions?from=YYYY-MM-DD&to=YYYY-MM-DD`

## Workflow Commands

- `/core-piv-loop-prime` — Load project context
- `/core-piv-loop-plan-feature` — Create implementation plan
- `/core-piv-loop-execute` — Execute the implementation plan
- `/validation-code-review` — Review changed files for technical issues
- `/validation-code-review-fix` — Fix issues found in review
- `/validation-validate` — Run validation sequence

## Reference Docs

- [PRD.md](PRD.md)
- [.github/copilot-instructions.md](.github/copilot-instructions.md)
- [.github/instructions/fastapi-best-practices.instructions.md](.github/instructions/fastapi-best-practices.instructions.md)
- [.github/instructions/react-frontend-best-practices.instructions.md](.github/instructions/react-frontend-best-practices.instructions.md)
- [.github/instructions/sqlite-best-practices.instructions.md](.github/instructions/sqlite-best-practices.instructions.md)
- [.github/instructions/testing-and-logging.instructions.md](.github/instructions/testing-and-logging.instructions.md)
- [.github/instructions/deployment-best-practices.instructions.md](.github/instructions/deployment-best-practices.instructions.md)
