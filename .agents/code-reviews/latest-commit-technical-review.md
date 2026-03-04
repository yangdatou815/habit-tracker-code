# Technical Code Review: latest commit

**Stats:**

- Files Modified: 0
- Files Added: 0
- Files Deleted: 0
- New lines: 0
- Deleted lines: 0

severity: medium
file: backend/app/stats/service.py
line: 7
issue: Inverted date ranges are silently normalized to `days=0`.
detail: `overview()` computes `days = (to_date - from_date).days + 1` and then clamps with `max(days, 0)`. For invalid input where `from_date > to_date`, this returns a seemingly valid payload instead of rejecting the caller error, which can hide bugs and produce misleading analytics.
suggestion: Validate input range (`from_date <= to_date`) in service and/or endpoint layer; raise `ValueError` or return `HTTP 422` from API handlers.

severity: medium
file: backend/tests/conftest.py
line: 18
issue: SQLite foreign key enforcement is disabled in test database setup.
detail: The fixture test engine (`sqlite:///:memory:` with `StaticPool`) does not enable `PRAGMA foreign_keys=ON`, so relational integrity/cascade bugs may pass in tests while failing in production-like behavior.
suggestion: Add an engine connect hook or explicit pragma execution in the fixture to enable foreign keys before creating tables.

severity: low
file: README.md
line: 1
issue: README content still describes the workshop template instead of the actual Habit Tracker repository.
detail: The repository now includes a concrete backend/frontend scaffold, but the top-level README remains template-first (`# Workshop Template`, workshop framing). This reduces onboarding clarity and diverges from the project’s documented intent.
suggestion: Replace template framing with project-specific overview, architecture, setup, test, and validation commands aligned with current repository structure.

## Verification Performed

- `git status`
- `git diff HEAD`
- `git diff --stat HEAD`
- `git ls-files --others --exclude-standard`
- `git show --name-only --pretty="format:" HEAD`
- `cd backend && .venv\Scripts\python -c "from datetime import date; from app.stats.service import overview; print(overview(date(2026,3,7), date(2026,3,1)))"`
- `cd backend && .venv\Scripts\python -c "from sqlalchemy import create_engine, text; from sqlalchemy.pool import StaticPool; engine=create_engine('sqlite:///:memory:', connect_args={'check_same_thread':False}, poolclass=StaticPool); conn=engine.connect(); print(conn.execute(text('PRAGMA foreign_keys')).scalar()); conn.close()"`
