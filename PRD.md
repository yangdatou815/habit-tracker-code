# Product Requirements Document (PRD)
## Habit Tracker MVP

## 1. Executive Summary
Habit Tracker is a full-stack web application that helps people build and maintain positive habits through fast daily logging and immediate visual progress feedback. The product prioritizes low friction: users can create a habit in seconds, mark completion quickly, and understand performance instantly without navigating complex workflows.

The core value proposition is **simplicity + visual accountability**. Users should be able to answer three daily questions at a glance: "What habits do I have?", "Did I complete them today?", and "How am I doing over time?".

The MVP goal is to deliver a reliable single-user web app with habit CRUD, daily completion tracking, and meaningful metrics (current streak, longest streak, 7-day view, completion rate).

## 2. Mission
### Mission Statement
Enable anyone to build consistency in positive behaviors by making habit tracking effortless and progress highly visible.

### Core Principles
- Simple interactions over feature complexity.
- Fast daily check-in (target: under 30 seconds for all habits).
- Visual feedback that motivates action.
- Data integrity and predictable behavior.
- Production-ready foundations even in MVP scope.

## 3. Target Users
### Primary Personas
1. **Daily Improver**
   - Wants to build 2–6 personal habits (e.g., reading, exercise, water intake).
   - Uses app once or twice daily.
2. **Busy Professional**
   - Needs quick logging with minimal cognitive load.
   - Values concise dashboard metrics.
3. **Beginner Tracker**
   - Limited technical comfort.
   - Prefers straightforward UI with clear actions.

### Technical Comfort Level
- Broad audience from low to moderate technical comfort.
- Mobile/desktop web familiarity assumed.
- No setup or advanced configuration expected for end users.

### User Needs and Pain Points
- Need a fast way to log daily completion.
- Need clear progress signals to stay motivated.
- Need simple habit setup (name + schedule).
- Pain point with existing tools: feature overload and slow workflows.

## 4. MVP Scope
### In Scope
#### Core Functionality
- ✅ Create, edit, archive, and delete habits.
- ✅ Configure habit schedule as daily with selected weekdays.
- ✅ Mark habit as done/not done for a specific date (default today).
- ✅ View dashboard with all active habits and today’s status.
- ✅ Show current streak and longest streak per habit.
- ✅ Show overall completion rate for selected timeframe (default 7 days).
- ✅ Show compact 7-day completion heatmap/status grid per habit.

#### Technical
- ✅ Single-user mode (no authentication).
- ✅ FastAPI REST API with Pydantic validation.
- ✅ SQLite persistence with relational schema and constraints.
- ✅ React + Vite + Tailwind frontend.
- ✅ Basic automated testing (unit + API integration + core UI behavior).

#### Integration
- ✅ Frontend-to-backend integration via `/api` endpoints.
- ✅ CORS/proxy setup for local development.

#### Deployment
- ✅ Local development environment scripts/instructions.
- ✅ Production build-ready frontend artifact and backend run config.

### Out of Scope
#### Core Functionality
- ❌ Social sharing, community challenges, or leaderboards.
- ❌ Push notifications/reminder engine.
- ❌ Advanced analytics dashboards beyond MVP metrics.
- ❌ Data export (CSV/PDF).

#### Technical
- ❌ Multi-user accounts and login/signup.
- ❌ Multi-tenant architecture.
- ❌ Native mobile applications.

#### Integration
- ❌ Third-party calendar/wearable integrations.
- ❌ OAuth providers.

#### Deployment
- ❌ Full cloud IaC automation in MVP.
- ❌ Horizontal scaling strategy for high-concurrency workloads.

## 5. User Stories
1. As a user, I want to create a habit with a name and selected weekdays, so that I can track routines relevant to my week.
   - Example: "Exercise" on Mon/Wed/Fri.
2. As a user, I want to quickly mark today’s habit completion, so that daily logging takes only a few seconds.
   - Example: Tap a checkbox/toggle on the dashboard.
3. As a user, I want to edit or archive habits, so that my tracker reflects current goals.
   - Example: Archive "Read 30 min" temporarily during travel.
4. As a user, I want to see my current streak, so that I stay motivated to continue.
   - Example: "Exercise: 5-day streak".
5. As a user, I want to see my longest streak, so that I can compare current consistency to my best performance.
   - Example: "Longest streak: 12 days".
6. As a user, I want a 7-day completion visualization, so that I can quickly spot missed days.
   - Example: Heatmap cells showing done/not done per day.
7. As a user, I want to view my completion rate, so that I can quantify consistency over time.
   - Example: "82% completed this week".
8. As a developer, I want validated API contracts and tests, so that behavior is predictable and regressions are caught early.

## 6. Core Architecture & Patterns
### High-Level Architecture
- Frontend SPA (React + Vite) consumes FastAPI REST API.
- Backend handles domain logic for habits, schedules, completions, and statistics.
- SQLite stores habits and completion records.

### Proposed Directory Structure
```text
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
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── features/habits/
│   │   ├── features/dashboard/
│   │   ├── components/ui/
│   │   ├── lib/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
└── PRD.md
```

### Key Patterns and Principles
- Domain-based backend modules with clear separation (router/schema/service/model).
- Feature-based frontend organization.
- Strict input validation with Pydantic.
- Service-layer business logic for streak and rate calculations.
- Repository/DB abstraction kept minimal for MVP simplicity.

## 7. Tools/Features
### Feature 1: Habit Management
- Create habit with name, optional description, active status, selected weekdays.
- Edit existing habit fields.
- Archive/unarchive habit.
- Delete habit and related completion history (confirm action in UI).

### Feature 2: Daily Tracking
- Log completion per habit/date as done/not done.
- Default action targets current local date.
- Prevent duplicate completion entries for same habit/date.

### Feature 3: Progress Dashboard
- Habit cards with today status and quick toggle.
- Current streak and longest streak displayed per habit.
- 7-day completion heatmap per habit.
- Overall completion rate across active habits.

### Feature 4: Reliability
- Validation errors displayed clearly in UI.
- Backend returns structured error payloads.
- Logging for key API operations and exceptions.

## 8. Technology Stack
### Backend
- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic v2
- SQLAlchemy 2.x (or SQLModel equivalent)
- Alembic (recommended for migrations)

### Frontend
- Node.js 20+
- React 18+
- Vite 5+
- Tailwind CSS 3+
- React Router (if route split is needed)
- TanStack Query (recommended for server state)

### Testing
- Backend: `pytest`, `httpx`, `pytest-asyncio`
- Frontend: `vitest`, `@testing-library/react`
- Optional E2E: `playwright`

### Optional/Support
- `structlog` for structured logging
- `ruff` + `black` for Python quality
- `eslint` + `prettier` for frontend quality

### Third-Party Integrations
- None required for MVP.

## 9. Security & Configuration
### Authentication/Authorization
- MVP uses single-user mode with no login.
- Security boundary is environment/deployment level rather than user-level access control.

### Configuration Management
- Backend `.env` (e.g., `DATABASE_URL`, `DEBUG`, `CORS_ORIGINS`, `LOG_LEVEL`).
- Frontend `.env` (e.g., `VITE_API_URL`).
- Separate dev and production configuration values.

### Security Scope
#### In Scope
- Input validation and schema constraints.
- SQL injection prevention through ORM parameterization.
- CORS configured for known origins.
- Safe error messages (no stack trace leakage in prod).

#### Out of Scope (MVP)
- User authentication/authorization.
- RBAC or multi-tenant data isolation.
- Advanced threat protection and WAF policy.

### Deployment Considerations
- Run backend behind reverse proxy in production.
- HTTPS termination at proxy/load balancer.
- Environment-based logging output (human-readable dev, JSON prod).

## 10. API Specification
### Base
- Base path: `/api/v1`
- Content type: `application/json`

### Endpoints
#### Habits
- `GET /api/v1/habits`
  - Returns active/archived habits (filter optional).
- `POST /api/v1/habits`
  - Creates a habit.
- `GET /api/v1/habits/{habit_id}`
  - Returns habit details + computed metrics.
- `PATCH /api/v1/habits/{habit_id}`
  - Partial update.
- `DELETE /api/v1/habits/{habit_id}`
  - Deletes habit and dependent completion rows.

#### Completions
- `PUT /api/v1/habits/{habit_id}/completions/{date}`
  - Upserts done/not done status for a date.
- `GET /api/v1/habits/{habit_id}/completions?from=YYYY-MM-DD&to=YYYY-MM-DD`
  - Returns completion records in date range.

#### Stats
- `GET /api/v1/stats/overview?from=YYYY-MM-DD&to=YYYY-MM-DD`
  - Returns completion rate and summary counts.

### Example Payloads
#### Create Habit Request
```json
{
  "name": "Exercise",
  "description": "30 min movement",
  "target_days": ["mon", "wed", "fri"],
  "is_active": true
}
```

#### Create Habit Response
```json
{
  "id": 1,
  "name": "Exercise",
  "description": "30 min movement",
  "target_days": ["mon", "wed", "fri"],
  "is_active": true,
  "created_at": "2026-03-03T10:00:00Z",
  "current_streak": 0,
  "longest_streak": 0,
  "completion_rate": 0.0
}
```

#### Upsert Completion Request
```json
{
  "status": "done"
}
```

#### Error Response
```json
{
  "detail": "Habit not found"
}
```

## 11. Success Criteria
### MVP Success Definition
Users can consistently track habits daily and understand their progress in under one minute of app interaction.

### Functional Requirements
- ✅ User can create/edit/archive/delete habits.
- ✅ User can mark completion done/not done for today and chosen date.
- ✅ Dashboard shows current streak, longest streak, 7-day heatmap, completion rate.
- ✅ API returns validated responses and proper HTTP status codes.
- ✅ Data persists across app restarts.

### Quality Indicators
- API p95 latency < 300ms for core endpoints on local/prototype env.
- No P1 defects in habit CRUD or completion logging.
- Core tests pass in CI (backend + frontend).

### UX Goals
- Add a new habit in <= 20 seconds.
- Log all daily habits in <= 30 seconds.
- Understand weekly performance at first glance on dashboard.

## 12. Implementation Phases
### Phase 1: Foundation (Week 1)
**Goal:** Establish project structure and baseline stack.

**Deliverables**
- ✅ Backend FastAPI app scaffold.
- ✅ Frontend Vite + React + Tailwind scaffold.
- ✅ SQLite setup and initial schema/migration.
- ✅ Dev environment configuration (`.env`, proxy, scripts).

**Validation Criteria**
- Backend and frontend run locally.
- Health endpoint and sample UI render successfully.

### Phase 2: Habit & Completion Core (Week 2)
**Goal:** Deliver core CRUD and daily tracking.

**Deliverables**
- ✅ Habit CRUD endpoints and UI forms.
- ✅ Completion upsert endpoint and dashboard toggles.
- ✅ Data validation and core error handling.

**Validation Criteria**
- End-to-end manual flow works for create → track → update.
- Integration tests cover core API paths.

### Phase 3: Metrics & Visualization (Week 3)
**Goal:** Add meaningful progress feedback.

**Deliverables**
- ✅ Current and longest streak calculations.
- ✅ Completion rate calculation and API.
- ✅ 7-day completion heatmap/status grid.

**Validation Criteria**
- Metric calculations verified with deterministic test cases.
- Dashboard shows consistent values with backend responses.

### Phase 4: Hardening & MVP Release (Week 4)
**Goal:** Improve reliability and release readiness.

**Deliverables**
- ✅ Unit/integration/UI test coverage for critical paths.
- ✅ Structured logging and improved error responses.
- ✅ Build and deployment documentation.

**Validation Criteria**
- CI checks pass.
- Production build succeeds.
- Release checklist completed.

## 13. Future Considerations
- Multi-user authentication and profiles.
- Reminders via email/push notifications.
- Monthly/quarterly trend analytics.
- Habit templates and onboarding wizard.
- Export and backup (CSV/JSON).
- Third-party integrations (calendar, wearables).

## 14. Risks & Mitigations
1. **Risk:** Streak logic edge cases (timezones, missed scheduled days).
   - **Mitigation:** Define strict date and schedule rules; add dedicated unit tests.
2. **Risk:** Scope creep from analytics/features.
   - **Mitigation:** Enforce MVP boundaries and backlog out-of-scope items.
3. **Risk:** Data inconsistency from duplicate completion writes.
   - **Mitigation:** Unique DB constraint on `(habit_id, date)` + upsert semantics.
4. **Risk:** Low daily engagement despite tracking availability.
   - **Mitigation:** Optimize dashboard speed/clarity and first-load guidance.
5. **Risk:** SQLite concurrency limitations if usage grows.
   - **Mitigation:** Keep repository abstraction ready for PostgreSQL migration.

## 15. Appendix
### Related Documents
- `.github/copilot-instructions.md`
- `.github/instructions/fastapi-best-practices.instructions.md`
- `.github/instructions/react-frontend-best-practices.instructions.md`
- `.github/instructions/sqlite-best-practices.instructions.md`
- `.github/instructions/testing-and-logging.instructions.md`
- `.github/instructions/deployment-best-practices.instructions.md`

### Key Dependency Notes
- FastAPI + React architecture selected for speed of iteration and clear API/UI separation.
- SQLite selected for MVP simplicity and low operational overhead.

### Repository Baseline
Current repository is a workshop template and will be expanded with `backend/` and `frontend/` app directories during implementation.
