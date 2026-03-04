# Feature: Scaffold Habit Tracker Foundation

The following plan should be complete, but its important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils types and models. Import from the right files etc.

## Feature Description

Create the Phase 1 foundation for the Habit Tracker MVP by scaffolding the backend (FastAPI + SQLite + SQLAlchemy + Alembic + testing/logging baseline) and frontend (React + Vite + Tailwind + TanStack Query + testing baseline), with working local dev commands and minimal smoke endpoints/views.

This plan is intentionally scoped to **foundation only** (no full habit CRUD/business logic yet) so the next execution step can implement core features on top of stable project structure.

## User Story

As a developer building the Habit Tracker MVP
I want a production-ready baseline scaffold for backend and frontend
So that feature implementation can proceed quickly with consistent architecture, testing, and deployment conventions.

## Problem Statement

The repository currently contains PRD/instructions and workflow assets, but no backend/frontend runtime code. Without an agreed scaffold and conventions baked into files, feature work risks inconsistency, rework, and integration drift.

## Solution Statement

Implement a standards-aligned scaffold that mirrors documented architecture and conventions:
- Backend domain structure (`habits`, `stats`) with app bootstrap, config, DB session wiring, router registration, health endpoint, and initial migration baseline.
- Frontend feature structure with Vite app bootstrap, API client, QueryClient provider, simple dashboard shell, and Tailwind setup.
- Baseline tests, lint/format config stubs, and runnable local scripts.

## Feature Metadata

**Feature Type**: New Capability (Foundation Scaffold)
**Estimated Complexity**: Medium
**Primary Systems Affected**: Backend app bootstrap, frontend app bootstrap, project-level dev workflow
**Dependencies**: FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, Uvicorn, structlog, pytest stack, React 18+, Vite 5+, Tailwind CSS, TanStack Query, Vitest/RTL

---

## CONTEXT REFERENCES

### Relevant Codebase Files IMPORTANT: YOU MUST READ THESE FILES BEFORE IMPLEMENTING!

- `PRD.md` (lines 114-147) - Proposed directory structure to mirror exactly.
- `PRD.md` (line 232) - API base path requirement (`/api/v1`).
- `PRD.md` (lines 320-331) - Phase 1 Foundation deliverables and validation criteria.
- `PRD.md` (line 403) - Explicit note that backend/frontend directories are not yet present.
- `.github/copilot-instructions.md` (lines 5-10) - Target stack versions and required libraries.
- `.github/copilot-instructions.md` (lines 12-50) - Canonical project structure to scaffold.
- `.github/copilot-instructions.md` (lines 53-70) - Canonical run/test/build commands.
- `.github/copilot-instructions.md` (lines 84-105) - Backend/frontend/API conventions and status codes.
- `.github/copilot-instructions.md` (lines 107-121) - Logging and DB constraints expectations.
- `.github/copilot-instructions.md` (lines 122-136) - Testing strategy and expected directory layout.
- `README.md` (lines 11-22) - PIV loop workflow and handoff expectations.
- `.github/instructions/fastapi-best-practices.instructions.md` (lines 28-79, 80-169, 170-268, 634-741, 742-785) - FastAPI structure/routing/validation/testing/CORS patterns.
- `.github/instructions/react-frontend-best-practices.instructions.md` (lines 32-73, 309-420, 587-694, 890-1007, 1063-1168) - React feature structure, TanStack Query usage, styling, routing, and testing.
- `.github/instructions/sqlite-best-practices.instructions.md` (lines 62-141, 271-365, 416-537, 538-617) - SQLite schema/indexing/SQLAlchemy/integrity/transaction patterns.
- `.github/instructions/testing-and-logging.instructions.md` (lines 55-129, 130-219, 321-349, 350-518, 519-629, 754-820) - structlog configuration + test pyramid patterns.
- `.github/instructions/deployment-best-practices.instructions.md` (lines 29-91, 92-148, 149-220, 221-304) - local dev topology and deployment expectations.

### New Files to Create

#### Backend scaffold
- `backend/requirements.txt`
- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/database.py`
- `backend/app/logging_config.py`
- `backend/app/middleware.py`
- `backend/app/habits/router.py`
- `backend/app/habits/schemas.py`
- `backend/app/habits/models.py`
- `backend/app/habits/service.py`
- `backend/app/stats/service.py`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/versions/<timestamp>_initial_schema.py`
- `backend/tests/conftest.py`
- `backend/tests/unit/test_health_or_stats_smoke.py`
- `backend/tests/integration/test_health_endpoint.py`

#### Frontend scaffold
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/index.html`
- `frontend/src/main.jsx`
- `frontend/src/App.jsx`
- `frontend/src/index.css`
- `frontend/src/lib/api.js`
- `frontend/src/features/habits/index.js`
- `frontend/src/features/dashboard/index.js`
- `frontend/src/components/ui/Button.jsx`
- `frontend/src/components/ui/Card.jsx`
- `frontend/src/features/dashboard/components/DashboardPage.jsx`
- `frontend/src/features/habits/components/HabitListPlaceholder.jsx`
- `frontend/src/features/habits/__tests__/HabitListPlaceholder.test.jsx`
- `frontend/src/features/dashboard/__tests__/DashboardPage.test.jsx`
- `frontend/vitest.config.js`
- `frontend/src/test/setup.js`

#### Shared/dev config
- `.env.example`
- `backend/.env.example`
- `frontend/.env.example`
- `.gitignore` updates (if needed for `.venv`, `node_modules`, build outputs)

### Relevant Documentation YOU SHOULD READ THESE BEFORE IMPLEMENTING!

- [FastAPI Tutorial - First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
  - Specific section: app creation and path operations.
  - Why: baseline app bootstrap.
- [FastAPI - Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
  - Specific section: `APIRouter` modularization.
  - Why: domain-based backend structure.
- [FastAPI - SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
  - Specific section: session dependency and model lifecycle.
  - Why: DB integration pattern.
- [Pydantic v2 Models](https://docs.pydantic.dev/latest/concepts/models/)
  - Specific section: `BaseModel`, validation, `ConfigDict(from_attributes=True)`.
  - Why: request/response schema design.
- [SQLAlchemy 2.0 ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
  - Specific section: declarative model + session usage.
  - Why: ORM baseline aligned with 2.x APIs.
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
  - Specific section: environment setup and revision workflow.
  - Why: migration baseline.
- [TanStack Query React Installation](https://tanstack.com/query/latest/docs/framework/react/installation)
  - Specific section: `QueryClient` and provider setup.
  - Why: server-state baseline in frontend.
- [Vite Guide](https://vite.dev/guide/)
  - Specific section: scripts/dev/build conventions.
  - Why: frontend runtime/build defaults.
- [Tailwind + Vite Installation](https://tailwindcss.com/docs/installation/using-vite)
  - Specific section: plugin/config/import flow.
  - Why: styling baseline.
- [pytest Getting Started](https://docs.pytest.org/en/stable/getting-started.html)
  - Specific section: discovery and fixtures.
  - Why: backend test setup.
- [Vitest Guide](https://vitest.dev/guide/)
  - Specific section: config and jsdom tests.
  - Why: frontend unit test setup.
- [structlog Getting Started](https://www.structlog.org/en/stable/getting-started.html)
  - Specific section: processor pipeline and context binding.
  - Why: structured logging baseline.

### Patterns to Follow

**Naming Conventions:**
- Backend modules use snake_case files and domain folders (`habits`, `stats`) per `.github/copilot-instructions.md`.
- Frontend components use PascalCase; hooks/utilities camelCase per `.github/instructions/react-frontend-best-practices.instructions.md`.

**Error Handling:**
- FastAPI default JSON error payloads and explicit status codes (`200/201/204/400/404/422`) from `.github/copilot-instructions.md`.
- Keep route handlers thin and push domain logic to service layer.

**Logging Pattern:**
- Configure `structlog` once, bind request context in middleware, switch console vs JSON by environment.
- Mirror the config + middleware flow described in `.github/instructions/testing-and-logging.instructions.md`.

**Other Relevant Patterns (from repository docs):**

```text
# Backend-first + frontend second local run flow
cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000
cd frontend && npm run dev
```

```text
# API namespace requirement
Base path: /api/v1
```

```text
# Feature structure expectation
frontend/src/features/habits/
frontend/src/features/dashboard/
frontend/src/components/ui/
```

---

## IMPLEMENTATION PLAN

### Phase 1: Foundation

Establish executable project skeletons and configuration before any domain logic.

**Tasks:**
- Create backend/frontend directory structures exactly as documented.
- Add package manifests and dependency lists.
- Add base environment templates and ignore rules.

### Phase 2: Core Implementation

Implement minimal runnable app foundations.

**Tasks:**
- Backend app bootstrap with `/api/v1/health` endpoint.
- DB engine/session wiring + SQLite PRAGMAs + model base.
- Frontend app bootstrap with QueryClient provider and placeholder dashboard view.
- Add Vite proxy to backend API.

### Phase 3: Integration

Connect modules and ensure runtime paths operate correctly.

**Tasks:**
- Register routers and middleware in FastAPI app.
- Ensure frontend API client points to `/api` (dev proxy) and `VITE_API_URL` override.
- Add initial migration script and table baseline placeholders.

### Phase 4: Testing & Validation

Lock in reliability with smoke tests and command-level validation.

**Tasks:**
- Add backend unit/integration smoke tests.
- Add frontend render tests for placeholder components.
- Run lint/test/build smoke commands and fix setup issues.

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

### CREATE backend/requirements.txt
- **IMPLEMENT**: Add pinned/compatible dependencies for FastAPI, SQLAlchemy, Alembic, Pydantic v2, Uvicorn, structlog, pytest stack.
- **PATTERN**: `.github/copilot-instructions.md` lines 5-10 and 53-70.
- **IMPORTS**: N/A (dependency manifest).
- **GOTCHA**: Keep dependencies minimal for scaffold; avoid adding app-level extras prematurely.
- **VALIDATE**: `cd backend && python -m venv .venv && .venv\Scripts\python -m pip install -r requirements.txt`

### CREATE backend/app/config.py
- **IMPLEMENT**: Central settings object for DB URL, debug, CORS origins, log mode.
- **PATTERN**: FastAPI config section in `.github/instructions/fastapi-best-practices.instructions.md` lines 786+.
- **IMPORTS**: `pydantic-settings` (if used) or Pydantic BaseModel/env parsing.
- **GOTCHA**: Keep defaults local-dev safe; do not hardcode secrets.
- **VALIDATE**: `cd backend && .venv\Scripts\python -c "from app.config import settings; print(settings.DATABASE_URL)"`

### CREATE backend/app/database.py
- **IMPLEMENT**: SQLAlchemy 2.x engine/session/base + SQLite foreign key enablement.
- **PATTERN**: `.github/copilot-instructions.md` lines 114-121 and SQLite guide lines 62-141, 538-617.
- **IMPORTS**: `sqlalchemy`, `sqlalchemy.orm`, `contextlib` if needed.
- **GOTCHA**: Ensure `PRAGMA foreign_keys = ON` per connection for SQLite.
- **VALIDATE**: `cd backend && .venv\Scripts\python -c "from app.database import engine; print(engine.url)"`

### CREATE backend/app/logging_config.py + backend/app/middleware.py
- **IMPLEMENT**: `structlog` setup and request-context middleware skeleton.
- **PATTERN**: testing/logging guide lines 55-219.
- **IMPORTS**: `structlog`, `logging`, `uuid`, `time`, FastAPI/Starlette middleware base.
- **GOTCHA**: Clear/bind context per request to avoid context leakage.
- **VALIDATE**: `cd backend && .venv\Scripts\python -c "from app.logging_config import configure_logging; configure_logging(); print('ok')"`

### CREATE backend/app/habits/{models.py,schemas.py,service.py,router.py}
- **IMPLEMENT**: Minimal domain placeholders (non-CRUD full logic) with typed schemas and empty service functions; router with at least one stub/list endpoint under `/habits`.
- **PATTERN**: `.github/copilot-instructions.md` lines 84-105 and FastAPI guide lines 80-268.
- **IMPORTS**: `fastapi.APIRouter`, Pydantic models, service module.
- **GOTCHA**: Keep router thin; no heavy logic in endpoint functions.
- **VALIDATE**: `cd backend && .venv\Scripts\python -m compileall app`

### CREATE backend/app/stats/service.py
- **IMPLEMENT**: Stub overview calculation function signatures and TODO-safe return placeholder for scaffold.
- **PATTERN**: PRD API `/api/v1/stats/overview` and service-layer principle.
- **IMPORTS**: typing/date utilities only.
- **GOTCHA**: Keep signature aligned with future PRD endpoint params (`from`, `to`).
- **VALIDATE**: `cd backend && .venv\Scripts\python -m compileall app`

### CREATE backend/app/main.py
- **IMPLEMENT**: FastAPI app factory/bootstrap, CORS, logging middleware, include habit router with `/api/v1` prefix, health endpoint.
- **PATTERN**: `.github/copilot-instructions.md` lines 100-105 and deployment guide lines 29-91.
- **IMPORTS**: `FastAPI`, `CORSMiddleware`, router modules.
- **GOTCHA**: Register API routers before adding any static-serving behavior (if added later).
- **VALIDATE**: `cd backend && .venv\Scripts\python -c "from app.main import app; print(len(app.routes))"`

### CREATE backend/alembic config and initial revision
- **IMPLEMENT**: Alembic bootstrap and first migration creating baseline tables (`habits`, `completions`, optional `habit_target_days`).
- **PATTERN**: SQLite constraints from `.github/copilot-instructions.md` lines 114-121 and PRD duplicate-prevention rule.
- **IMPORTS**: Alembic op, SQLAlchemy types.
- **GOTCHA**: Include unique constraint on `(habit_id, completed_date)` and FK cascade on completions.
- **VALIDATE**: `cd backend && .venv\Scripts\alembic upgrade head`

### CREATE backend/tests/conftest.py
- **IMPLEMENT**: test DB fixture (SQLite in-memory/static pool) and FastAPI dependency override.
- **PATTERN**: testing/logging guide lines 411-518.
- **IMPORTS**: `pytest`, `fastapi.testclient`, SQLAlchemy sessionmaker.
- **GOTCHA**: ensure override cleanup (`app.dependency_overrides.clear()`).
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q backend/tests --maxfail=1`

### CREATE backend/tests/unit and integration smoke tests
- **IMPLEMENT**: one unit test for service placeholder behavior and one integration test for `/api/v1/health`.
- **PATTERN**: test organization from `.github/copilot-instructions.md` lines 122-136.
- **IMPORTS**: pytest/assertions.
- **GOTCHA**: Keep tests deterministic and isolated.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q backend/tests/unit backend/tests/integration`

### CREATE frontend/package.json + vite.config.js + index.html
- **IMPLEMENT**: Vite React scripts (`dev/build/test`), dependencies, and API proxy `/api -> http://localhost:8000`.
- **PATTERN**: deployment guide lines 29-91 and React best practices lines 309+.
- **IMPORTS**: Vite React plugin, optionally Tailwind Vite plugin.
- **GOTCHA**: Ensure Node version compatibility (Vite docs indicate modern Node 20+).
- **VALIDATE**: `cd frontend && npm install && npm run build`

### CREATE frontend/src bootstrap files
- **IMPLEMENT**: `main.jsx` with `QueryClientProvider`, `App.jsx` shell, `index.css` with Tailwind import, `lib/api.js` base client.
- **PATTERN**: React guide lines 309-420 and Tailwind+Vite install guide.
- **IMPORTS**: `@tanstack/react-query`, `react`, `react-dom`.
- **GOTCHA**: Keep API URL configurable via `VITE_API_URL` fallback to `/api`.
- **VALIDATE**: `cd frontend && npm run dev -- --host 127.0.0.1 --port 5173`

### CREATE frontend feature/ui placeholders
- **IMPLEMENT**: `features/dashboard`, `features/habits`, and shared `components/ui` placeholders to prove structure.
- **PATTERN**: React feature-based structure lines 32-73.
- **IMPORTS**: component-local only.
- **GOTCHA**: Do not implement full product UX yet; keep placeholders minimal.
- **VALIDATE**: `cd frontend && npm run build`

### CREATE frontend test setup
- **IMPLEMENT**: Vitest + RTL config and two render tests for dashboard/habit placeholder components.
- **PATTERN**: React testing section lines 1063-1168.
- **IMPORTS**: `vitest`, `@testing-library/react`, `@testing-library/jest-dom`.
- **GOTCHA**: Use `jsdom` environment; include setup file.
- **VALIDATE**: `cd frontend && npm run test -- --run`

### UPDATE root and env templates
- **IMPLEMENT**: Add root/backend/frontend `.env.example` files and update `.gitignore` if gaps exist.
- **PATTERN**: deployment guide environment configuration section.
- **IMPORTS**: N/A.
- **GOTCHA**: Keep sample values safe and explicit (no secrets).
- **VALIDATE**: `git status --short`

### ADD end-to-end scaffold verification script docs (optional)
- **IMPLEMENT**: Add concise README section for running backend + frontend together.
- **PATTERN**: `.github/copilot-instructions.md` command section lines 53-70.
- **IMPORTS**: N/A.
- **GOTCHA**: Keep docs aligned with actual script names.
- **VALIDATE**: `python -c "print('docs-check')" && cd frontend && npm run build && cd ..\backend && .venv\Scripts\pytest -q`

---

## TESTING STRATEGY

Test only scaffold behavior in this phase; deeper feature tests belong to subsequent plans.

### Unit Tests
- Backend: service placeholder test(s), config loading, helper/date sanity as available.
- Frontend: simple render tests for dashboard shell and habit placeholder components.

### Integration Tests
- Backend: `/api/v1/health` returns `200` and expected payload.
- Optional lightweight API test for stub habits endpoint shape.

### Edge Cases
- Missing/invalid env variable defaults still allow local startup.
- SQLite startup with foreign keys enabled.
- CORS allows configured frontend origin only.
- API base prefix strictly `/api/v1`.
- Frontend API client respects `VITE_API_URL` override.

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and feature correctness.

### Level 1: Syntax & Style
- `cd backend && .venv\Scripts\python -m compileall app`
- `cd backend && .venv\Scripts\ruff check .` (if configured)
- `cd backend && .venv\Scripts\black --check .` (if configured)
- `cd frontend && npm run build`
- `cd frontend && npm run lint` (if configured)

### Level 2: Unit Tests
- `cd backend && .venv\Scripts\pytest -q backend/tests/unit`
- `cd frontend && npm run test -- --run --reporter=basic`

### Level 3: Integration Tests
- `cd backend && .venv\Scripts\pytest -q backend/tests/integration`

### Level 4: Manual Validation
- Start backend: `cd backend && .venv\Scripts\uvicorn app.main:app --reload --port 8000`
- Start frontend: `cd frontend && npm run dev`
- Check health: `curl http://localhost:8000/api/v1/health`
- Open UI and confirm placeholder dashboard renders without console errors.

### Level 5: Additional Validation (Optional)
- Use Playwright MCP (configured in `vscode/mcp.json`) to sanity-check initial page render.

---

## ACCEPTANCE CRITERIA

- [ ] Backend and frontend directory scaffolds exist and match documented structure.
- [ ] Backend starts successfully and exposes `/api/v1/health`.
- [ ] Frontend starts and renders dashboard placeholder with Tailwind styles loaded.
- [ ] SQLite + migration baseline applies without errors.
- [ ] Backend and frontend smoke tests pass.
- [ ] API prefix and status-code conventions are reflected in scaffold endpoints.
- [ ] Logging middleware is wired with request-context binding.
- [ ] Local run/build commands in docs execute successfully.

---

## COMPLETION CHECKLIST

- [ ] All tasks completed in order.
- [ ] Each task validation passed immediately.
- [ ] Validation commands executed successfully.
- [ ] Unit + integration tests pass.
- [ ] No linting/type errors in scaffold scope.
- [ ] Manual run confirms backend/frontend integration.
- [ ] Acceptance criteria met.
- [ ] Implementation is ready for Phase 2 (habit/completion core).

---

## NOTES

- Scope guard: this plan intentionally avoids implementing full habit CRUD and metrics logic; it only creates a stable base for those features.
- Because the repo currently has no runtime code, all “patterns to mirror” come from PRD + instruction documents rather than existing implementation files.
- FastAPI and SQLAlchemy official pages may have extractor issues in automated fetch tooling; links are still included as authoritative references.
- Suggested order is backend-first scaffold, then frontend scaffold, then tests/docs, to minimize cross-system debugging.

**Confidence Score**: 8.5/10 for one-pass execution success.
