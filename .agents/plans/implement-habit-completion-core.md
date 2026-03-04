# Feature: Implement Habit & Completion Core

The following plan should be complete, but its important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils types and models. Import from the right files etc.

## Feature Description

Implement Phase 2 of the MVP: complete habit CRUD, completion upsert/query APIs, and dashboard interactions so users can create habits, edit/archive/delete them, and mark daily completion from the main dashboard.

This plan assumes the feature argument was omitted and defaults to the next documented milestone in the PRD: **Phase 2: Habit & Completion Core**.

## User Story

As a habit-tracking user
I want to create/update/archive/delete habits and mark daily completions
So that I can track my routines quickly and keep my dashboard up to date each day.

## Problem Statement

The repository currently has a foundation scaffold with health checks, basic model skeletons, and placeholder UI. Core habit management and completion workflows are not implemented yet, so the MVP’s primary user value is unavailable.

## Solution Statement

Add end-to-end Habit & Completion core flows:
- Backend: implement REST endpoints for habits and completions under `/api/v1`, with validated payloads, proper status codes, and idempotent completion writes.
- Frontend: replace placeholder components with real list/form/toggle interactions powered by TanStack Query.
- Testing: add unit + integration API tests and frontend component tests for create/update/complete flows.

## Feature Metadata

**Feature Type**: New Capability
**Estimated Complexity**: High
**Primary Systems Affected**: `backend/app/habits/*`, backend tests, frontend habits/dashboard features, shared API utilities
**Dependencies**: FastAPI, Pydantic v2, SQLAlchemy 2.x (SQLite dialect upsert), TanStack Query, React Testing Library, Vitest

---

## CONTEXT REFERENCES

### Relevant Codebase Files IMPORTANT: YOU MUST READ THESE FILES BEFORE IMPLEMENTING!

- `PRD.md` (lines 232, 237-251, 333, 337-338, 342) - API base path, exact Phase 2 endpoint contract, and delivery/validation goals.
- `.github/copilot-instructions.md` (lines 87, 94, 100-105, 122+) - architecture and API conventions (including idempotent upsert requirement).
- `backend/app/main.py` (lines 28, 36, 39) - middleware/router mounting pattern and API namespace.
- `backend/app/database.py` (lines 17-24, 38-43) - engine/session setup and dependency injection pattern.
- `backend/app/habits/models.py` (lines 11, 30, 42, 45-46, 52) - current entities and DB constraints.
- `backend/app/habits/schemas.py` (lines 8, 13-19, 21-27) - response schema style and `from_attributes` usage.
- `backend/app/habits/router.py` (lines 11, 14-15) - current APIRouter conventions.
- `backend/app/habits/service.py` (line 8) - service-layer placement pattern.
- `backend/alembic/versions/20260304_0001_initial_schema.py` (lines 18-71) - existing migration baseline and uniqueness rules.
- `backend/tests/conftest.py` (lines 17-33, 43-54) - test DB/session and dependency override fixtures.
- `backend/tests/integration/test_health_endpoint.py` (lines 4-8) - API integration test style.
- `backend/tests/integration/test_db_foreign_keys.py` (lines 11-23) - integrity behavior test style.
- `frontend/src/lib/api.js` (lines 1-4, 20-24) - fetch wrapper and base URL pattern.
- `frontend/src/main.jsx` (lines 7-12, 18-20) - QueryClient defaults and provider setup.
- `frontend/src/features/dashboard/components/DashboardPage.jsx` (lines 4, 9, 11) - current dashboard composition point.
- `frontend/src/features/habits/components/HabitListPlaceholder.jsx` (lines 3, 7) - placeholder location to replace with real list.
- `frontend/package.json` (lines 6-9) - available scripts and current validation limits.
- `frontend/vite.config.js` (lines 8-10) - `/api` proxy contract for local dev.

### New Files to Create

#### Backend
- `backend/app/habits/dependencies.py` - reusable habit lookup dependency (`404` handling).
- `backend/tests/integration/test_habits_api.py` - CRUD endpoint integration tests.
- `backend/tests/integration/test_completions_api.py` - completion upsert/list integration tests.
- `backend/tests/unit/test_habits_service.py` - service-level behavior tests (validation/transform helpers).
- `backend/alembic/versions/<timestamp>_habit_phase2_constraints.py` - optional DB hardening migration (if adding new constraints/indexes).

#### Frontend
- `frontend/src/features/habits/api/habits.js` - habits/completions API functions.
- `frontend/src/features/habits/hooks/useHabits.js` - queries + mutations with invalidation.
- `frontend/src/features/habits/components/HabitForm.jsx` - create/edit form.
- `frontend/src/features/habits/components/HabitCard.jsx` - card with completion toggle and quick actions.
- `frontend/src/features/habits/components/HabitList.jsx` - list state wrapper.
- `frontend/src/features/habits/components/CompletionToggle.jsx` - done/not-done per day interaction.
- `frontend/src/features/habits/__tests__/HabitForm.test.jsx` - form interaction tests.
- `frontend/src/features/habits/__tests__/HabitList.test.jsx` - list fetch/render tests.
- `frontend/src/features/habits/__tests__/CompletionToggle.test.jsx` - completion mutation behavior tests.
- `frontend/src/features/habits/test-utils/renderWithQueryClient.js` - shared test provider helper.

### Relevant Documentation YOU SHOULD READ THESE BEFORE IMPLEMENTING!

- [FastAPI Path Params](https://fastapi.tiangolo.com/tutorial/path-params/)
  - Specific section: typed path parameter validation.
  - Why: robust `{habit_id}` and `{date}` parameter handling.
- [FastAPI Query Params](https://fastapi.tiangolo.com/tutorial/query-params/)
  - Specific section: optional filtering params.
  - Why: `/completions?from=&to=` date-range support.
- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
  - Specific section: Pydantic request model parsing.
  - Why: create/update payload validation.
- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
  - Specific section: session lifecycle and ORM usage.
  - Why: consistent DB interaction in services.
- [SQLAlchemy SQLite Upsert](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#insert-on-conflict-upsert)
  - Specific section: `INSERT ... ON CONFLICT DO UPDATE`.
  - Why: idempotent completion writes by `(habit_id, completed_date)`.
- [SQLAlchemy Select Query Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html)
  - Specific section: modern `select()` patterns.
  - Why: scalable read/query style for list/detail endpoints.
- [TanStack Query Mutations](https://tanstack.com/query/latest/docs/framework/react/guides/mutations)
  - Specific section: `useMutation` lifecycle and state.
  - Why: create/update/complete action flows.
- [TanStack Query Invalidations](https://tanstack.com/query/latest/docs/framework/react/guides/invalidations-from-mutations)
  - Specific section: `onSuccess` invalidation.
  - Why: keep dashboard/habit list data in sync.

### Patterns to Follow

**Naming Conventions:**
- Backend: snake_case modules under domain folders (`backend/app/habits/*`) and typed function signatures.
- Frontend: PascalCase components + feature-local API/hooks under `src/features/habits`.

**Error Handling:**
- Use FastAPI status semantics (`200`, `201`, `204`, `404`, `422`) and explicit `HTTPException` for missing resources.
- Prefer dependency-based resource loading for repeated `{habit_id}` checks.

**Logging Pattern:**
- Keep request-level logging in middleware only; add targeted service-level logs only where needed.
- Do not bypass configured `structlog` context pattern from `backend/app/logging_config.py`.

**Other Relevant Patterns (from current code):**

```python
# DB session injection pattern
@router.get("", response_model=list[HabitResponse])
def get_habits(db: Session = Depends(get_db)) -> list[Habit]:
    return list_habits(db)
```

```javascript
// Frontend API utility pattern
const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";
async function request(path, options = {}) { ... }
```

```python
# Test dependency override pattern
app.dependency_overrides[get_db] = override_get_db
with TestClient(app) as test_client:
    yield test_client
app.dependency_overrides.clear()
```

---

## IMPLEMENTATION PLAN

### Phase 1: Foundation

Define contracts and shared helpers required by all CRUD/completion flows.

**Tasks:**
- Expand Pydantic schemas for create/update/detail and completion upsert/list.
- Add helper dependency for validated habit retrieval.
- Add API utility functions and query key strategy on frontend.

### Phase 2: Core Implementation

Implement backend endpoints and frontend components for full habit/completion core.

**Tasks:**
- Implement backend Habit CRUD routes + service functions.
- Implement completion upsert/list routes + service functions.
- Replace placeholder UI with form/list/card/toggle components.
- Wire TanStack Query mutations + invalidations.

### Phase 3: Integration

Connect backend and frontend flows to achieve create → track → update loop.

**Tasks:**
- Ensure dashboard renders server-backed habits and updates after actions.
- Ensure completion toggle writes idempotently and reflects current state.
- Preserve existing health route and middleware behavior.

### Phase 4: Testing & Validation

Add targeted tests for regressions and edge cases.

**Tasks:**
- Add backend integration tests for all new endpoints.
- Add frontend component tests for form submission and toggle behavior.
- Run full lint/test/build/coverage command set supported by project scripts.

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

### UPDATE `backend/app/habits/schemas.py`
- **IMPLEMENT**: Add `HabitCreate`, `HabitUpdate`, `HabitDetailResponse`, `CompletionUpsertRequest`, `CompletionListResponse`, and day/status validators.
- **PATTERN**: `backend/app/habits/schemas.py` lines 8-27 (`BaseModel` + `ConfigDict(from_attributes=True)`).
- **IMPORTS**: `Field`, `field_validator`, `date`, `datetime`, optional enums/literals.
- **GOTCHA**: Keep update schema optional fields-only and reject blank habit names.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q tests/unit/test_habits_service.py`

### CREATE `backend/app/habits/dependencies.py`
- **IMPLEMENT**: Add `get_habit_or_404(habit_id, db)` dependency returning model or raising `HTTPException(404)`.
- **PATTERN**: `backend/app/database.py` lines 38-43 for dependency style.
- **IMPORTS**: `Depends`, `HTTPException`, `Session`, `get_db`, `Habit`.
- **GOTCHA**: Keep DB access centralized and avoid duplicate lookup logic in each route.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q tests/integration/test_habits_api.py -k not completions`

### UPDATE `backend/app/habits/service.py`
- **IMPLEMENT**: Add `create_habit`, `get_habit`, `update_habit`, `delete_habit`, `upsert_completion`, `list_completions_range` service functions.
- **PATTERN**: existing `list_habits` function and model relationships in `backend/app/habits/models.py`.
- **IMPORTS**: SQLAlchemy session + sqlite dialect `insert` for upsert (or equivalent conflict-safe flow).
- **GOTCHA**: Ensure upsert idempotency on `(habit_id, completed_date)` and transaction-safe commits.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q tests/unit/test_habits_service.py`

### UPDATE `backend/app/habits/router.py`
- **IMPLEMENT**: Add endpoints for:
  - `POST /habits`
  - `GET /habits/{habit_id}`
  - `PATCH /habits/{habit_id}`
  - `DELETE /habits/{habit_id}` (204)
  - `PUT /habits/{habit_id}/completions/{date}`
  - `GET /habits/{habit_id}/completions`
- **PATTERN**: existing APIRouter pattern at lines 11-15.
- **IMPORTS**: new schemas, service funcs, habit dependency.
- **GOTCHA**: parse completion date as ISO `YYYY-MM-DD`; return `422` on invalid format.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q tests/integration/test_habits_api.py tests/integration/test_completions_api.py`

### UPDATE `backend/app/habits/models.py` (optional hardening)
- **IMPLEMENT**: If needed, add DB-level status/day constraints and indexes for range queries.
- **PATTERN**: existing uniqueness + FK constraints at lines 45-52.
- **IMPORTS**: SQLAlchemy `CheckConstraint` and indexes if introduced.
- **GOTCHA**: Keep migration compatibility with existing revision chain.
- **VALIDATE**: `cd backend && .venv\Scripts\alembic upgrade head`

### CREATE `backend/alembic/versions/<timestamp>_habit_phase2_constraints.py` (if model changed)
- **IMPLEMENT**: Migration for any new constraints/indexes only.
- **PATTERN**: `backend/alembic/versions/20260304_0001_initial_schema.py` structure.
- **IMPORTS**: `alembic.op`, `sqlalchemy as sa`.
- **GOTCHA**: Include both upgrade and downgrade operations; preserve data.
- **VALIDATE**: `cd backend && .venv\Scripts\alembic upgrade head`

### CREATE `backend/tests/integration/test_habits_api.py`
- **IMPLEMENT**: Test create/list/get/patch/delete behavior and status codes.
- **PATTERN**: `backend/tests/integration/test_health_endpoint.py` style + fixture usage.
- **IMPORTS**: pytest + client fixture.
- **GOTCHA**: Assert response payload shape matches schema contract.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q tests/integration/test_habits_api.py`

### CREATE `backend/tests/integration/test_completions_api.py`
- **IMPLEMENT**: Test upsert idempotency, date-range listing, and invalid date/body cases.
- **PATTERN**: integrity test style in `backend/tests/integration/test_db_foreign_keys.py`.
- **IMPORTS**: pytest + client fixture.
- **GOTCHA**: Verify second PUT on same date updates/overwrites instead of duplicating rows.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q tests/integration/test_completions_api.py`

### CREATE `backend/tests/unit/test_habits_service.py`
- **IMPLEMENT**: Service-level tests for update semantics, archive toggles, date-range validation.
- **PATTERN**: `backend/tests/unit/test_health_or_stats_smoke.py` structure.
- **IMPORTS**: pytest + db/session fixtures/helpers.
- **GOTCHA**: Keep deterministic dates and avoid timezone-coupled assertions.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest -q tests/unit/test_habits_service.py`

### CREATE `frontend/src/features/habits/api/habits.js`
- **IMPLEMENT**: Add API functions for habits CRUD and completion calls using shared `request` helper.
- **PATTERN**: `frontend/src/lib/api.js` lines 1-24.
- **IMPORTS**: `request` helper only.
- **GOTCHA**: Match backend path format exactly (`/v1/habits/...`).
- **VALIDATE**: `cd frontend && npm run test -- --run src/features/habits/__tests__/HabitList.test.jsx`

### CREATE `frontend/src/features/habits/hooks/useHabits.js`
- **IMPLEMENT**: Add `useQuery` for list/detail and `useMutation` hooks for create/update/delete/complete with invalidation.
- **PATTERN**: Query provider setup in `frontend/src/main.jsx` lines 7-20 and TanStack docs mutation invalidation pattern.
- **IMPORTS**: `useQuery`, `useMutation`, `useQueryClient`.
- **GOTCHA**: Use stable query keys, avoid broad invalidation where targeted keys suffice.
- **VALIDATE**: `cd frontend && npm run test -- --run src/features/habits/__tests__/CompletionToggle.test.jsx`

### CREATE `frontend/src/features/habits/components/HabitForm.jsx`
- **IMPLEMENT**: Add create/edit form with name/description/target days + inline validation errors.
- **PATTERN**: Existing UI composition style (`Card`/`Button` components).
- **IMPORTS**: feature hooks + shared UI components.
- **GOTCHA**: Preserve low-friction UX (minimal fields, clear submit states).
- **VALIDATE**: `cd frontend && npm run test -- --run src/features/habits/__tests__/HabitForm.test.jsx`

### CREATE `frontend/src/features/habits/components/HabitCard.jsx`
- **IMPLEMENT**: Show habit info + quick completion toggle + edit/archive/delete actions.
- **PATTERN**: structure used in `DashboardPage.jsx` and `HabitListPlaceholder.jsx`.
- **IMPORTS**: `CompletionToggle`, `Button`, mutation hooks.
- **GOTCHA**: Keep completion action idempotent per selected date.
- **VALIDATE**: `cd frontend && npm run test -- --run src/features/habits/__tests__/HabitList.test.jsx`

### CREATE `frontend/src/features/habits/components/CompletionToggle.jsx`
- **IMPLEMENT**: Toggle done/not-done for a habit/date via completion upsert mutation.
- **PATTERN**: API path semantics from PRD and hooks invalidation pattern.
- **IMPORTS**: `useMutation` hook wrapper.
- **GOTCHA**: Guard against double-submit while mutation pending.
- **VALIDATE**: `cd frontend && npm run test -- --run src/features/habits/__tests__/CompletionToggle.test.jsx`

### CREATE `frontend/src/features/habits/components/HabitList.jsx`
- **IMPLEMENT**: Fetch and render habits; manage loading/empty/error states.
- **PATTERN**: placeholder replacement point in `DashboardPage.jsx` line 11.
- **IMPORTS**: query hook + `HabitCard`.
- **GOTCHA**: avoid re-render loops by memoizing derived filters if needed.
- **VALIDATE**: `cd frontend && npm run test -- --run src/features/habits/__tests__/HabitList.test.jsx`

### UPDATE `frontend/src/features/habits/index.js`
- **IMPLEMENT**: Export new hooks/components/API surface for feature module.
- **PATTERN**: existing single-line export style.
- **IMPORTS**: feature-local modules only.
- **GOTCHA**: keep export names stable and explicit.
- **VALIDATE**: `cd frontend && npm run build`

### UPDATE `frontend/src/features/dashboard/components/DashboardPage.jsx`
- **IMPLEMENT**: Replace placeholder with real habits list + create form composition.
- **PATTERN**: current dashboard container and layout classes.
- **IMPORTS**: new habits components from feature index.
- **GOTCHA**: maintain simple MVP UX; avoid introducing extra pages/modals.
- **VALIDATE**: `cd frontend && npm run test -- --run src/features/dashboard/__tests__/DashboardPage.test.jsx`

### CREATE frontend tests for new components/hooks
- **IMPLEMENT**: Add tests listed above + provider-aware test utility.
- **PATTERN**: existing RTL patterns in dashboard/habits tests.
- **IMPORTS**: RTL + Vitest + QueryClient provider helper.
- **GOTCHA**: run Vitest in non-watch mode (`--run`) for automation.
- **VALIDATE**: `cd frontend && npm run test -- --run`

### UPDATE README and/or PRD progress markers (if desired)
- **IMPLEMENT**: Document Phase 2 run/test flows and endpoint availability.
- **PATTERN**: project README command section.
- **IMPORTS**: N/A.
- **GOTCHA**: keep docs aligned with actual scripts and implemented routes.
- **VALIDATE**: `git diff -- README.md PRD.md`

---

## TESTING STRATEGY

### Unit Tests
- Backend service functions for create/update/delete and date-range validation.
- Frontend component logic for form validation and toggle disabled states.

### Integration Tests
- Backend API tests for full habit lifecycle and completion upsert/list behavior.
- Frontend query/mutation integration using mocked API responses + QueryClient provider.

### Edge Cases
- Blank/whitespace habit names rejected (`422`).
- Invalid completion date format/path rejected (`422`).
- Repeated completion PUT on same `(habit_id, date)` remains single-row idempotent.
- Deleting habit cascades completion rows.
- Completion list query handles empty ranges and reversed dates.
- Archived habits handling on list and completion operations (explicitly defined behavior).

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and 100% feature correctness.

### Level 1: Syntax & Style
- `cd backend && .venv\Scripts\ruff check .`
- `cd backend && .venv\Scripts\black --check .`
- `cd frontend && npm run build`

### Level 2: Unit Tests
- `cd backend && .venv\Scripts\pytest -q tests/unit`
- `cd frontend && npm run test -- --run src/features/habits/__tests__/HabitForm.test.jsx src/features/habits/__tests__/CompletionToggle.test.jsx`

### Level 3: Integration Tests
- `cd backend && .venv\Scripts\pytest -q tests/integration/test_habits_api.py tests/integration/test_completions_api.py`
- `cd backend && .venv\Scripts\pytest -q tests/integration/test_db_foreign_keys.py`

### Level 4: Manual Validation
- Start backend: `cd backend && .venv\Scripts\uvicorn app.main:app --reload --port 8000`
- Start frontend: `cd frontend && npm run dev -- --host 127.0.0.1 --port 5173`
- Create habit from UI.
- Toggle completion for today.
- Refresh page and confirm state persists.
- Edit habit and verify dashboard updates.
- Delete habit and verify related completions no longer appear.

### Level 5: Additional Validation (Optional)
- Run `cd backend && .venv\Scripts\python -m mypy app/` once endpoint/schema signatures stabilize.
- Use Playwright MCP for smoke E2E if available.

---

## ACCEPTANCE CRITERIA

- [ ] All Phase 2 endpoints from PRD are implemented with correct status codes and validation behavior.
- [ ] Completion upsert is idempotent by `(habit_id, completed_date)`.
- [ ] Frontend dashboard supports create → track → update habit flow.
- [ ] Integration tests verify core CRUD and completion workflow.
- [ ] Unit tests cover service-level edge cases.
- [ ] Existing health endpoint and baseline tests remain green.
- [ ] Documentation reflects newly available feature flows.

---

## COMPLETION CHECKLIST

- [ ] All tasks completed in order.
- [ ] Each task validation passed immediately.
- [ ] All validation commands executed successfully.
- [ ] Full test suite passes (unit + integration).
- [ ] No linting/type-check regressions in touched areas.
- [ ] Manual create/complete/update/delete workflow verified.
- [ ] Acceptance criteria met.
- [ ] Implementation ready for Phase 3 (metrics & visualization).

---

## NOTES

- Scope is intentionally aligned to PRD Phase 2 only; streak/overview metric logic remains a Phase 3 concern.
- API contract decisions to settle early:
  - Archive behavior (`is_active=false`) vs physical delete semantics in UI.
  - Completion `status` domain (`done`/`not_done` vs `done`/`skipped`) must be consistently defined in schema + UI.
- Validation infrastructure caveat: frontend currently lacks `lint/typecheck/test:coverage` scripts; keep plan commands executable with existing scripts unless this feature explicitly adds those scripts.
- Prefer minimal new dependencies; existing stack already supports required behaviors.

**Confidence Score**: 8.8/10 for one-pass execution success.
