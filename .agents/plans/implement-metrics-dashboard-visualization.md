# Feature: Metrics & Dashboard Visualization (PRD Phase 3)

The following plan should be complete, but its important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils types and models. Import from the right files etc.

## Feature Description

Deliver PRD Phase 3 — meaningful progress feedback via a stats overview API endpoint, a 7-day completion heatmap grid per habit, and a dashboard summary header showing today's completion count and overall weekly completion rate. This completes the core "visual accountability" promise of the product.

## User Story

As a habit tracker user
I want to see a 7-day visual grid on each habit card, a dashboard summary of today's progress, and an overall completion rate
So that I can quickly spot missed days, stay motivated by streaks, and understand my weekly consistency at a glance

## Problem Statement

The backend computes per-habit streaks and rates but:
1. The `stats/service.py` overview function is a stub — no API route exposes it.
2. The dashboard has no summary header (e.g. "4/6 done today, 82% this week").
3. HabitCard displays streak/rate as plain text — no 7-day visual heatmap exists.

Users cannot answer "How am I doing over time?" without these visualizations.

## Solution Statement

1. **Backend**: Wire up `GET /api/v1/stats/overview` returning aggregate completion data across all active habits for a date range. Enhance the stats service to query real data.
2. **Frontend — WeeklyHeatmap component**: A compact 7-day grid (Mon–Sun or rolling last-7-days) per habit card, showing done/missed/not-scheduled status via colored cells.
3. **Frontend — DashboardSummary component**: A header card showing today's habit count, completed count, and overall 7-day completion rate sourced from the stats endpoint.
4. **Tests**: Unit tests for stats service logic, integration test for the stats endpoint, and frontend component tests for the new components.

## Feature Metadata

**Feature Type**: New Capability
**Estimated Complexity**: Medium
**Primary Systems Affected**: `backend/app/stats/`, `backend/app/habits/router.py` (or new stats router), `frontend/src/features/dashboard/`, `frontend/src/features/habits/components/`
**Dependencies**: No new external libraries required — uses existing SQLAlchemy, FastAPI, React, TanStack Query, Tailwind CSS

---

## CONTEXT REFERENCES

### Relevant Codebase Files — IMPORTANT: YOU MUST READ THESE FILES BEFORE IMPLEMENTING!

**Backend:**
- `backend/app/stats/service.py` (lines 1-16) — Why: Current stub to replace with real implementation
- `backend/app/stats/__init__.py` — Why: Empty init, may need exports
- `backend/app/habits/router.py` (lines 1-110) — Why: Existing router pattern to mirror for stats router
- `backend/app/habits/service.py` (lines 1-65) — Why: `_compute_streaks`, `_completion_rate`, `_habit_query_with_relationships` patterns to reuse/reference
- `backend/app/habits/service.py` (lines 201-228) — Why: `list_completions_range` query pattern
- `backend/app/habits/models.py` (lines 1-62) — Why: Habit, HabitTargetDay, Completion ORM models
- `backend/app/habits/schemas.py` (lines 1-131) — Why: Pydantic schema patterns (ConfigDict, Field, validators)
- `backend/app/habits/dependencies.py` (lines 1-15) — Why: `get_habit_or_404` dependency pattern
- `backend/app/main.py` (lines 1-44) — Why: Router registration pattern (`app.include_router`)
- `backend/app/database.py` (lines 1-43) — Why: `get_db` dependency, Base, engine, session setup
- `backend/app/config.py` (lines 1-38) — Why: Settings pattern
- `backend/app/middleware.py` (lines 1-38) — Why: structlog logging pattern
- `backend/tests/conftest.py` (lines 1-53) — Why: Test fixtures (db_session, client)
- `backend/tests/integration/test_habits_api.py` (lines 1-70) — Why: Integration test pattern
- `backend/tests/integration/test_completions_api.py` (lines 1-40) — Why: Helper `_create_habit` pattern and completion assertions
- `backend/tests/unit/test_habits_service.py` (lines 1-118) — Why: Unit test pattern with db_session fixture
- `backend/pytest.ini` — Why: pytest configuration

**Frontend:**
- `frontend/src/features/dashboard/components/DashboardPage.jsx` (lines 1-22) — Why: Current dashboard layout to extend
- `frontend/src/features/dashboard/index.js` (lines 1-1) — Why: Barrel exports to update
- `frontend/src/features/habits/components/HabitCard.jsx` (lines 1-85) — Why: Card where heatmap will be inserted
- `frontend/src/features/habits/components/CompletionToggle.jsx` (lines 1-42) — Why: `formatLocalDate` utility, completion query pattern
- `frontend/src/features/habits/hooks/useHabits.js` (lines 1-110) — Why: TanStack Query hooks pattern to mirror for stats
- `frontend/src/features/habits/api/habits.js` (lines 1-56) — Why: API function pattern (`request()` usage)
- `frontend/src/features/habits/index.js` (lines 1-16) — Why: Barrel exports pattern
- `frontend/src/lib/api.js` (lines 1-35) — Why: `request()` fetch wrapper, `API_BASE_URL`
- `frontend/src/components/ui/Card.jsx` (lines 1-3) — Why: Shared Card component
- `frontend/src/features/dashboard/__tests__/DashboardPage.test.jsx` (lines 1-20) — Why: Dashboard test pattern (mocking habits feature)
- `frontend/src/features/habits/__tests__/CompletionToggle.test.jsx` (lines 1-70) — Why: Component test pattern with mocked hooks
- `frontend/src/features/habits/test-utils/renderWithQueryClient.js` — Why: Test utility pattern
- `frontend/vitest.config.js` (lines 1-10) — Why: Vitest config (jsdom, setup file)
- `frontend/src/test/setup.js` — Why: Global test setup (`@testing-library/jest-dom/vitest`)

**Documentation:**
- `PRD.md` (lines 57-63, 341-360) — Why: Phase 3 deliverables and success criteria
- `PRD.md` (lines 220-230) — Why: Stats API endpoint specification
- `.github/copilot-instructions.md` — Why: Project conventions and code standards

### New Files to Create

**Backend:**
- `backend/app/stats/router.py` — Stats API router with `GET /stats/overview` endpoint
- `backend/app/stats/schemas.py` — Pydantic response schemas for stats
- `backend/tests/integration/test_stats_api.py` — Integration tests for stats endpoint
- `backend/tests/unit/test_stats_service.py` — Unit tests for stats service logic

**Frontend:**
- `frontend/src/features/dashboard/components/DashboardSummary.jsx` — Summary header component
- `frontend/src/features/dashboard/__tests__/DashboardSummary.test.jsx` — Tests for summary component
- `frontend/src/features/dashboard/api/stats.js` — Stats API functions
- `frontend/src/features/dashboard/hooks/useStats.js` — TanStack Query hook for stats
- `frontend/src/features/habits/components/WeeklyHeatmap.jsx` — 7-day completion grid component
- `frontend/src/features/habits/__tests__/WeeklyHeatmap.test.jsx` — Tests for heatmap component

### Patterns to Follow

**Naming Conventions:**
- Backend: snake_case for functions/variables, PascalCase for classes/models/schemas
- Frontend: PascalCase for components, camelCase for hooks/functions/variables
- Files: snake_case backend, PascalCase frontend components, camelCase hooks/api

**Router Registration Pattern** (from `backend/app/main.py` line 39):
```python
app.include_router(habits_router, prefix="/api/v1")
# New: register stats router the same way
app.include_router(stats_router, prefix="/api/v1")
```

**Router Definition Pattern** (from `backend/app/habits/router.py` lines 1-10):
```python
router = APIRouter(prefix="/stats", tags=["stats"])
```

**Schema Pattern** (from `backend/app/habits/schemas.py`):
```python
class StatsOverviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # fields...
```

**Service Pattern** (from `backend/app/habits/service.py`):
- Accept `db: Session` as first arg
- Return Pydantic schema instances
- Keep route handlers thin

**TanStack Query Hook Pattern** (from `frontend/src/features/habits/hooks/useHabits.js`):
```javascript
export const statsQueryKeys = {
  all: ["stats"],
  overview: (from, to) => ["stats", "overview", from, to],
};
export function useStatsOverviewQuery({ from, to } = {}) {
  return useQuery({
    queryKey: statsQueryKeys.overview(from, to),
    queryFn: () => fetchStatsOverview({ from, to }),
  });
}
```

**API Function Pattern** (from `frontend/src/features/habits/api/habits.js`):
```javascript
import { request } from "../../../lib/api";
export function fetchStatsOverview({ from, to }) {
  return request(withSearchParams("/v1/stats/overview", { from, to }));
}
```

**Frontend Test Pattern** (from `CompletionToggle.test.jsx`):
- Mock hooks with `vi.mock`
- Use `render`, `screen` from `@testing-library/react`
- Use `vi.fn()` for mutation mocks

**Integration Test Pattern** (from `test_completions_api.py`):
- Use `client` fixture from conftest
- Helper function to create prerequisite data
- Assert status codes and JSON payloads

**Error Handling:**
- Backend: Raise `HTTPException` for 404/422. Use `ValueError` in service, catch in router.
- Frontend: TanStack Query `isError`/`isLoading` states in components.

**Logging Pattern** (from `backend/app/middleware.py`):
```python
import structlog
logger = structlog.get_logger()
logger.info("stats.overview.computed", habits_count=5, rate=85.0)
```

---

## IMPLEMENTATION PLAN

### Phase 1: Backend — Stats Schemas & Service

Build the data layer: Pydantic response schemas and a real stats service that queries completions across all active habits for a date range.

**Tasks:**
- Create stats Pydantic schemas (overview response)
- Rewrite `stats/service.py` with real DB query logic
- Compute: total active habits, completed today count, overall completion rate for a range

### Phase 2: Backend — Stats Router & Registration

Expose the stats service via `GET /api/v1/stats/overview` and register it in the app.

**Tasks:**
- Create stats router with overview endpoint
- Register router in `main.py`
- Add structlog logging for stat computation

### Phase 3: Backend — Tests

Unit test the stats service logic and integration test the API endpoint.

**Tasks:**
- Unit tests for stats service (empty DB, partial completions, full completions, date ranges)
- Integration tests for stats API endpoint (happy path, date filtering, edge cases)

### Phase 4: Frontend — Stats API & Hooks

Create the data-fetching layer for the stats endpoint.

**Tasks:**
- Create stats API functions
- Create TanStack Query hook for stats overview
- Wire into dashboard barrel exports

### Phase 5: Frontend — DashboardSummary Component

Build the summary header showing today's progress and weekly rate.

**Tasks:**
- Create DashboardSummary component
- Integrate into DashboardPage above the habit list
- Add tests

### Phase 6: Frontend — WeeklyHeatmap Component

Build the 7-day visual completion grid per habit.

**Tasks:**
- Create WeeklyHeatmap component
- Integrate into HabitCard
- Add tests

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

---

### Task 1: CREATE `backend/app/stats/schemas.py`

- **IMPLEMENT**: Pydantic schemas for stats overview response:
  ```python
  class StatsOverviewResponse(BaseModel):
      from_date: date
      to_date: date
      total_habits: int          # count of active habits
      completed_today: int       # habits with status="done" for today
      total_today: int           # active habits scheduled for today (or all active if no schedule)
      completion_rate: float     # overall % of done completions vs expected across the range
  ```
- **PATTERN**: Mirror schema style from `backend/app/habits/schemas.py` lines 95-103 (HabitResponse with ConfigDict)
- **IMPORTS**: `from __future__ import annotations`, `from datetime import date`, `from pydantic import BaseModel`
- **GOTCHA**: Use `float` for completion_rate (0.0-100.0 like existing `_completion_rate` in habits service). Do NOT use ConfigDict/from_attributes here since this is not ORM-mapped — it's a computed response.
- **VALIDATE**: `cd backend && .venv\Scripts\python -c "from app.stats.schemas import StatsOverviewResponse; print('OK')"`

---

### Task 2: UPDATE `backend/app/stats/service.py`

- **IMPLEMENT**: Replace the stub `overview()` with a real function:
  ```python
  def compute_stats_overview(db: Session, *, from_date: date, to_date: date) -> StatsOverviewResponse
  ```
  Logic:
  1. Query all active habits (with `selectinload` for target_days and completions).
  2. Compute `completed_today`: count of active habits that have a completion with `status="done"` for `datetime.now(UTC).date()`.
  3. Compute `total_today`: count of active habits whose target_days include today's weekday abbreviation (mon/tue/etc.), or all active habits if they have no target_days (daily default).
  4. Compute `completion_rate` across the range: for each active habit, count "expected" days (days within range that match target_days, or all days if no target_days), count "done" completions in that range. Rate = `(total_done / total_expected) * 100` rounded to 2 decimals. Return 0.0 if total_expected is 0.
- **PATTERN**: Follow query style from `backend/app/habits/service.py` lines 98-107 (`_habit_query_with_relationships`, `selectinload`)
- **IMPORTS**: `from __future__ import annotations`, `from datetime import UTC, date, datetime, timedelta`, `from sqlalchemy.orm import Session, selectinload`, `from app.habits.models import Completion, Habit, HabitTargetDay`, `from app.stats.schemas import StatsOverviewResponse`
- **GOTCHA**: The weekday abbreviations in the DB are 3-char lowercase: `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`. Python's `date.strftime("%a").lower()[:3]` gives the same format. Use the constant mapping from `schemas.py` if needed, or just do inline mapping.
- **GOTCHA**: Don't count archived habits (`is_active=False`). Only consider active habits.
- **GOTCHA**: Import `structlog` and log the computation: `logger.info("stats.overview.computed", total_habits=..., rate=...)`
- **VALIDATE**: `cd backend && .venv\Scripts\pytest tests/unit/test_stats_service.py -v` (after Task 5)

---

### Task 3: CREATE `backend/app/stats/router.py`

- **IMPLEMENT**: Stats router with one endpoint:
  ```python
  router = APIRouter(prefix="/stats", tags=["stats"])

  @router.get("/overview", response_model=StatsOverviewResponse)
  def get_stats_overview(
      from_date: date | None = Query(default=None, alias="from"),
      to_date: date | None = Query(default=None, alias="to"),
      db: Session = Depends(get_db),
  ) -> StatsOverviewResponse:
  ```
  - Default `from_date` to 7 days ago, `to_date` to today if not provided.
  - Validate `from_date <= to_date` or return 422.
  - Call `compute_stats_overview(db, from_date=..., to_date=...)`.
- **PATTERN**: Mirror `backend/app/habits/router.py` lines 1-10 (imports, router definition) and lines 95-110 (completions endpoint with date query params using `alias`)
- **IMPORTS**: `from __future__ import annotations`, `from datetime import UTC, date, datetime, timedelta`, `from fastapi import APIRouter, Depends, HTTPException, Query`, `from sqlalchemy.orm import Session`, `from app.database import get_db`, `from app.stats.schemas import StatsOverviewResponse`, `from app.stats.service import compute_stats_overview`
- **GOTCHA**: Use `alias="from"` and `alias="to"` for query params to match the PRD API spec (`?from=YYYY-MM-DD&to=YYYY-MM-DD`) — identical pattern to completions endpoint in habits router.
- **VALIDATE**: `cd backend && .venv\Scripts\python -c "from app.stats.router import router; print(router.routes)"`

---

### Task 4: UPDATE `backend/app/main.py`

- **IMPLEMENT**: Import and register the stats router:
  ```python
  from app.stats.router import router as stats_router
  # After existing habits router include:
  app.include_router(stats_router, prefix="/api/v1")
  ```
- **PATTERN**: Mirror the existing `app.include_router(habits_router, prefix="/api/v1")` on line 39
- **GOTCHA**: Import must be added alongside the existing `from app.habits.router import router as habits_router` to keep consistent naming.
- **VALIDATE**: `cd backend && .venv\Scripts\uvicorn app.main:app --port 8000 &; Start-Sleep 3; Invoke-RestMethod http://localhost:8000/api/v1/stats/overview; Stop-Process -Name uvicorn -ErrorAction SilentlyContinue` — OR simpler: `cd backend && .venv\Scripts\python -c "from app.main import app; routes = [r.path for r in app.routes]; assert '/api/v1/stats/overview' in routes, routes; print('OK')"`

---

### Task 5: CREATE `backend/tests/unit/test_stats_service.py`

- **IMPLEMENT**: Unit tests for `compute_stats_overview`:
  1. `test_overview_empty_database` — no habits, expect total_habits=0, completed_today=0, total_today=0, rate=0.0
  2. `test_overview_with_habits_no_completions` — 2 active habits, no completions, rate=0.0
  3. `test_overview_with_completions` — create habits with target_days, add completions, verify completed_today and rate calculations
  4. `test_overview_excludes_archived_habits` — archived habit not counted in totals
  5. `test_overview_date_range_filtering` — completions outside range not counted
- **PATTERN**: Mirror `backend/tests/unit/test_habits_service.py` — use `db_session` fixture, import service functions, create habits via `create_habit()`
- **IMPORTS**: `from datetime import date, timedelta`, `from app.habits.schemas import HabitCreate`, `from app.habits.service import create_habit, upsert_completion`, `from app.stats.service import compute_stats_overview`
- **GOTCHA**: Use deterministic dates rather than `datetime.now()` for predictable assertions. For `completed_today` testing, you may need to mock `datetime.now(UTC).date()` or use today's date in test setup.
- **VALIDATE**: `cd backend && .venv\Scripts\pytest tests/unit/test_stats_service.py -v`

---

### Task 6: CREATE `backend/tests/integration/test_stats_api.py`

- **IMPLEMENT**: Integration tests for `GET /api/v1/stats/overview`:
  1. `test_stats_overview_empty` — no data, returns 200 with zeros
  2. `test_stats_overview_with_data` — create habits + completions, verify response shape and values
  3. `test_stats_overview_custom_date_range` — pass `from` and `to` query params
  4. `test_stats_overview_rejects_reversed_dates` — `from` > `to` returns 422
  5. `test_stats_overview_defaults_to_7_day_range` — omit params, verify default range in response
- **PATTERN**: Mirror `backend/tests/integration/test_completions_api.py` — use `client` fixture, helper to create habit, assert status codes and JSON
- **IMPORTS**: Standard test imports only; fixtures come from conftest
- **GOTCHA**: Use the `_create_habit` helper pattern (local function that POSTs to create a habit and returns its ID).
- **VALIDATE**: `cd backend && .venv\Scripts\pytest tests/integration/test_stats_api.py -v`

---

### Task 7: CREATE `frontend/src/features/dashboard/api/stats.js`

- **IMPLEMENT**: Stats API functions:
  ```javascript
  import { request } from "../../../lib/api";

  function withSearchParams(path, params) { /* same helper as in habits.js */ }

  export function fetchStatsOverview({ from, to } = {}) {
    return request(withSearchParams("/v1/stats/overview", { from, to }));
  }
  ```
- **PATTERN**: Mirror `frontend/src/features/habits/api/habits.js` lines 1-15 (imports, `withSearchParams` helper, `request()` calls)
- **GOTCHA**: Duplicate `withSearchParams` locally or extract to a shared utility. For minimal scope, duplicate it (matching the existing pattern in habits.js).
- **VALIDATE**: `cd frontend && npx vitest run --reporter verbose 2>&1 | Select-String -Pattern "FAIL" -NotMatch | Select-Object -First 3` (no failures)

---

### Task 8: CREATE `frontend/src/features/dashboard/hooks/useStats.js`

- **IMPLEMENT**: TanStack Query hook for stats:
  ```javascript
  import { useQuery } from "@tanstack/react-query";
  import { fetchStatsOverview } from "../api/stats";

  export const statsQueryKeys = {
    all: ["stats"],
    overview: (from, to) => ["stats", "overview", from ?? "default", to ?? "default"],
  };

  export function useStatsOverviewQuery({ from, to } = {}) {
    return useQuery({
      queryKey: statsQueryKeys.overview(from, to),
      queryFn: () => fetchStatsOverview({ from, to }),
    });
  }
  ```
- **PATTERN**: Mirror `frontend/src/features/habits/hooks/useHabits.js` lines 1-30 (query key structure, useQuery pattern)
- **VALIDATE**: `cd frontend && node -e "import('./src/features/dashboard/hooks/useStats.js').then(() => console.log('OK')).catch(e => console.log(e.message))"` — OR rely on build check in later validation.

---

### Task 9: UPDATE `frontend/src/features/dashboard/index.js`

- **IMPLEMENT**: Add barrel exports for new modules:
  ```javascript
  export { DashboardPage } from "./components/DashboardPage";
  export { DashboardSummary } from "./components/DashboardSummary";
  export { useStatsOverviewQuery, statsQueryKeys } from "./hooks/useStats";
  ```
- **PATTERN**: Mirror `frontend/src/features/habits/index.js` barrel export style
- **VALIDATE**: `cd frontend && npm run build` (no errors)

---

### Task 10: CREATE `frontend/src/features/dashboard/components/DashboardSummary.jsx`

- **IMPLEMENT**: Summary header component:
  ```jsx
  import { Card } from "../../../components/ui/Card";
  import { useStatsOverviewQuery } from "../hooks/useStats";

  export function DashboardSummary() {
    const statsQuery = useStatsOverviewQuery();
    const stats = statsQuery.data;

    if (statsQuery.isLoading) {
      return <Card><p className="text-sm text-slate-600">Loading stats...</p></Card>;
    }

    if (statsQuery.isError || !stats) {
      return null; // Silently hide on error — non-critical
    }

    return (
      <Card className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-600">Today</p>
          <p className="text-2xl font-bold text-slate-900">
            {stats.completed_today}<span className="text-base font-normal text-slate-500">/{stats.total_today}</span>
          </p>
        </div>
        <div>
          <p className="text-sm font-medium text-slate-600">7-day rate</p>
          <p className="text-2xl font-bold text-emerald-600">{stats.completion_rate}%</p>
        </div>
        <div>
          <p className="text-sm font-medium text-slate-600">Active habits</p>
          <p className="text-2xl font-bold text-slate-900">{stats.total_habits}</p>
        </div>
      </Card>
    );
  }
  ```
- **PATTERN**: Component style from `DashboardPage.jsx` (import Card, Tailwind utilities). Stats display layout matches PRD 7-day summary requirement.
- **GOTCHA**: Return `null` on error so the dashboard is still usable even if stats fail. This is a non-blocking enhancement.
- **VALIDATE**: `cd frontend && npx vitest run src/features/dashboard/__tests__/DashboardSummary.test.jsx --reporter verbose` (after Task 12)

---

### Task 11: UPDATE `frontend/src/features/dashboard/components/DashboardPage.jsx`

- **IMPLEMENT**: Add DashboardSummary component above the habit list:
  ```jsx
  import { DashboardSummary } from "./DashboardSummary";
  // ...existing imports...

  // In the return JSX, insert between the <h1> and the HabitForm Card:
  <DashboardSummary />
  ```
  Final layout order: `<h1>` → `<DashboardSummary />` → `<Card>Add habit</Card>` → `<HabitList />`
- **PATTERN**: Existing layout pattern in `DashboardPage.jsx` lines 12-21
- **GOTCHA**: Keep `className="mb-4"` on DashboardSummary's Card wrapper or add `mb-4` to the summary component's container for consistent spacing.
- **VALIDATE**: `cd frontend && npx vitest run src/features/dashboard/__tests__/DashboardPage.test.jsx --reporter verbose`

---

### Task 12: CREATE `frontend/src/features/dashboard/__tests__/DashboardSummary.test.jsx`

- **IMPLEMENT**: Tests for DashboardSummary:
  1. `renders loading state` — mock query as loading, expect "Loading stats..." text
  2. `renders stats data` — mock query with data object, expect today count, rate, total habits
  3. `renders nothing on error` — mock query as error, expect no content rendered
- **PATTERN**: Mirror `frontend/src/features/dashboard/__tests__/DashboardPage.test.jsx` (vi.mock, render, screen) and `CompletionToggle.test.jsx` (mocking hooks)
- **IMPORTS**: Mock `../hooks/useStats` with `vi.mock`. Use `render, screen` from `@testing-library/react`.
- **VALIDATE**: `cd frontend && npx vitest run src/features/dashboard/__tests__/DashboardSummary.test.jsx --reporter verbose`

---

### Task 13: CREATE `frontend/src/features/habits/components/WeeklyHeatmap.jsx`

- **IMPLEMENT**: A 7-day completion grid component:
  ```jsx
  import { useCompletionsQuery } from "../hooks/useHabits";
  import { formatLocalDate } from "./CompletionToggle";

  function getLast7Days() {
    const days = [];
    const today = new Date();
    for (let i = 6; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      days.push(d);
    }
    return days;
  }

  function getDayAbbrev(dateObj) {
    return dateObj.toLocaleDateString("en-US", { weekday: "short" }).slice(0, 2);
  }

  export function WeeklyHeatmap({ habitId, targetDays = [] }) {
    const days = getLast7Days();
    const fromDate = formatLocalDate(days[0]);
    const toDate = formatLocalDate(days[6]);
    const completionsQuery = useCompletionsQuery(habitId, { from: fromDate, to: toDate });

    const completionMap = {};
    (completionsQuery.data?.completions || []).forEach((c) => {
      completionMap[c.completed_date] = c.status;
    });

    // Map of 3-char day names for checking if day is scheduled
    const dayNameMap = { Mon: "mon", Tue: "tue", Wed: "wed", Thu: "thu", Fri: "fri", Sat: "sat", Sun: "sun" };

    return (
      <div className="flex gap-1">
        {days.map((dayDate) => {
          const dateStr = formatLocalDate(dayDate);
          const status = completionMap[dateStr];
          const dayAbbrev = dayDate.toLocaleDateString("en-US", { weekday: "short" });
          const isScheduled = targetDays.length === 0 || targetDays.includes(dayNameMap[dayAbbrev]);

          let bgColor = "bg-slate-100"; // not scheduled or no data
          if (isScheduled) {
            if (status === "done") bgColor = "bg-emerald-500";
            else if (status === "not_done") bgColor = "bg-red-300";
            else bgColor = "bg-slate-200"; // scheduled but not yet tracked
          }

          return (
            <div key={dateStr} className="flex flex-col items-center gap-0.5" title={dateStr}>
              <span className="text-[10px] text-slate-500">{getDayAbbrev(dayDate)}</span>
              <div className={`h-5 w-5 rounded-sm ${bgColor}`} />
            </div>
          );
        })}
      </div>
    );
  }
  ```
- **PATTERN**: Uses `useCompletionsQuery` from `frontend/src/features/habits/hooks/useHabits.js` and `formatLocalDate` from `CompletionToggle.jsx` (already exported)
- **GOTCHA**: The `targetDays` array uses 3-char lowercase (`mon`, `tue`, etc.) matching the API format. JavaScript's `toLocaleDateString("en-US", { weekday: "short" })` returns `Mon`, `Tue`, etc. — map to lowercase.
- **GOTCHA**: Import `formatLocalDate` from `"./CompletionToggle"` (it's already exported as a named export).
- **VALIDATE**: `cd frontend && npx vitest run src/features/habits/__tests__/WeeklyHeatmap.test.jsx --reporter verbose` (after Task 15)

---

### Task 14: UPDATE `frontend/src/features/habits/components/HabitCard.jsx`

- **IMPLEMENT**: Add WeeklyHeatmap to each habit card. Insert it between the habit metadata and the action buttons:
  ```jsx
  import { WeeklyHeatmap } from "./WeeklyHeatmap";
  // ... in the return JSX, after the metadata div and before the buttons div:
  <WeeklyHeatmap habitId={habit.id} targetDays={habit.target_days} />
  ```
- **PATTERN**: Existing HabitCard layout at `frontend/src/features/habits/components/HabitCard.jsx` lines 46-65
- **GOTCHA**: Only show heatmap in non-editing mode (it's already inside the `if (!isEditing)` branch).
- **VALIDATE**: `cd frontend && npx vitest run --reporter verbose`

---

### Task 15: CREATE `frontend/src/features/habits/__tests__/WeeklyHeatmap.test.jsx`

- **IMPLEMENT**: Tests for WeeklyHeatmap:
  1. `renders 7 day columns` — mock completions query, expect 7 day cells rendered
  2. `marks done days with green` — provide completions data with "done" status, verify emerald background class
  3. `shows not-scheduled days as neutral` — provide targetDays that exclude some days, verify slate-100 class
  4. `handles loading state gracefully` — mock query as loading, expect cells still rendered with default colors
- **PATTERN**: Mirror `CompletionToggle.test.jsx` — mock `../hooks/useHabits` with `vi.mock`, render with props
- **GOTCHA**: Mock both `useCompletionsQuery` and any other hook imports used. Also mock `formatLocalDate` or let it run naturally since it's a pure function.
- **VALIDATE**: `cd frontend && npx vitest run src/features/habits/__tests__/WeeklyHeatmap.test.jsx --reporter verbose`

---

### Task 16: UPDATE `frontend/src/features/habits/index.js`

- **IMPLEMENT**: Add `WeeklyHeatmap` to barrel exports:
  ```javascript
  export { WeeklyHeatmap } from "./components/WeeklyHeatmap";
  ```
- **PATTERN**: Existing barrel export pattern in the same file
- **VALIDATE**: `cd frontend && npm run build`

---

### Task 17: UPDATE `frontend/src/features/dashboard/__tests__/DashboardPage.test.jsx`

- **IMPLEMENT**: Update the mock to include DashboardSummary. Since DashboardSummary is imported from within the dashboard feature (not from habits), mock the `./DashboardSummary` import or the `../hooks/useStats` hook.
  Simplest: add a mock for DashboardSummary:
  ```javascript
  vi.mock("./DashboardSummary", () => ({
    DashboardSummary: () => <div>Dashboard summary</div>,
  }));
  ```
  Or mock at the module path `../components/DashboardSummary`. Verify the existing test still passes and optionally add an assertion for the summary text.
- **PATTERN**: Existing mock pattern in the same test file (mocking `../../habits`)
- **VALIDATE**: `cd frontend && npx vitest run src/features/dashboard/__tests__/DashboardPage.test.jsx --reporter verbose`

---

## TESTING STRATEGY

### Unit Tests

**Backend (`tests/unit/test_stats_service.py`):**
- Test `compute_stats_overview` with db_session fixture
- Cover: empty DB, active-only filtering, today-count logic, date range boundaries, rate calculation accuracy
- Use deterministic dates and explicit completion inserts

### Integration Tests

**Backend (`tests/integration/test_stats_api.py`):**
- Test `GET /api/v1/stats/overview` via TestClient
- Cover: default date range, custom date range, reversed dates (422), response shape
- Use helper function to seed habits/completions

**Frontend (component tests):**
- DashboardSummary: mock useStatsOverviewQuery, test loading/data/error states
- WeeklyHeatmap: mock useCompletionsQuery, test 7-day rendering, color states

### Edge Cases

- **No habits exist**: Stats endpoint returns zeros, dashboard summary shows 0/0
- **All habits archived**: total_habits=0, completed_today=0
- **Habit with no target_days**: Treated as "daily" (every day is scheduled)
- **Completions outside requested range**: Not counted in rate
- **Reversed date range**: 422 validation error
- **Future dates**: Don't count as "expected" days for rate calculation (only count up to today or to_date, whichever is earlier)

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and 100% feature correctness.

### Level 1: Syntax & Style

```bash
cd backend && .venv\Scripts\ruff check .
cd backend && .venv\Scripts\black --check .
```

### Level 2: Unit Tests

```bash
cd backend && .venv\Scripts\pytest tests/unit/ -v
```

### Level 3: Integration Tests

```bash
cd backend && .venv\Scripts\pytest tests/integration/ -v
```

### Level 4: Full Backend Test Suite

```bash
cd backend && .venv\Scripts\pytest -v
```

### Level 5: Frontend Build & Tests

```bash
cd frontend && npm run build
cd frontend && npx vitest run --reporter verbose
```

### Level 6: Manual Validation

1. Start backend: `cd backend && .venv\Scripts\uvicorn app.main:app --reload --port 8000`
2. Test stats endpoint with no data:
   ```
   curl http://localhost:8000/api/v1/stats/overview
   ```
   Expected: `{"from_date":"2026-02-26","to_date":"2026-03-05","total_habits":0,"completed_today":0,"total_today":0,"completion_rate":0.0}`
3. Create a habit and add completions, then re-check stats endpoint.
4. Start frontend: `cd frontend && npm run dev`
5. Verify dashboard shows summary header with today's stats and 7-day rate.
6. Verify each habit card shows a 7-day heatmap with colored cells.
7. Mark a habit done/undone and verify heatmap and summary update.

---

## ACCEPTANCE CRITERIA

- [ ] `GET /api/v1/stats/overview` returns correct aggregate stats for all active habits
- [ ] Default date range is last 7 days when no query params provided
- [ ] `completed_today` accurately reflects today's done completions
- [ ] `completion_rate` calculation accounts for target_days schedule
- [ ] Dashboard shows summary header (today count, 7-day rate, active habits)
- [ ] Each habit card displays a 7-day visual heatmap with color-coded cells
- [ ] Heatmap distinguishes: done (green), missed (red/light), not-scheduled (neutral), no data (light)
- [ ] All backend tests pass (unit + integration) with zero errors
- [ ] All frontend tests pass with zero errors
- [ ] Frontend builds without errors (`npm run build`)
- [ ] Backend linting passes (`ruff check .` and `black --check .`)
- [ ] No regressions in existing habit CRUD or completion workflows
- [ ] Stats endpoint returns 422 for reversed date ranges
- [ ] Archived habits are excluded from all stats calculations

---

## COMPLETION CHECKLIST

- [ ] All 17 tasks completed in order
- [ ] Each task validation passed immediately
- [ ] All validation commands executed successfully
- [ ] Full backend test suite passes (unit + integration)
- [ ] Full frontend test suite passes
- [ ] No linting or formatting errors
- [ ] Manual testing confirms feature works end-to-end
- [ ] Acceptance criteria all met
- [ ] Code reviewed for quality and maintainability

---

## NOTES

### Design Decisions

1. **Stats as separate domain module**: The stats router/service/schemas live in `backend/app/stats/` as a distinct bounded context, not shoehorned into the habits module. This follows the existing directory structure and PRD API spec.

2. **Rolling 7-day heatmap (not fixed Mon–Sun)**: The WeeklyHeatmap shows the last 7 calendar days rather than a fixed Mon–Sun week. This gives more useful "recent activity" context and avoids empty cells at the start of a week.

3. **DashboardSummary gracefully degrades**: On API error, the summary returns `null` rather than showing an error state. The habit list and creation form remain fully functional even if stats fail.

4. **Completion rate considers target_days schedule**: If a habit targets Mon/Wed/Fri, only those days count as "expected" within the date range. Habits with no target_days are treated as daily (every day is expected). This produces meaningful rates rather than penalizing weekend-only habits.

5. **No new dependencies**: Everything is built with existing libraries — no new NPM or pip packages needed.

### Risks

- **Today's date sensitivity in tests**: Stats rely on `datetime.now(UTC).date()` for `completed_today`. Unit tests should either inject today's date or create completions for the actual current date. Consider making `today` a parameter with a default.
- **Heatmap N+1 queries**: Each HabitCard's WeeklyHeatmap fires a separate completions query. This is acceptable for MVP (typically 2-6 habits) but could be optimized later by batch-fetching all completions in a single dashboard query.
- **Timezone edge case**: `formatLocalDate()` uses the browser's local timezone. A user checking in at 11:55 PM might see different results than the UTC-based backend. This is a known PRD risk (Risk #1) and is acceptable for MVP.
