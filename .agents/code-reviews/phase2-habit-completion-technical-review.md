# Technical Code Review — Phase 2 Habit & Completion Core

## Scope and Context
- Reviewed standards in `.github/copilot-instructions.md` and `README.md`.
- `/core` and `/docs` directories are not present in this repository; review baseline was derived from existing backend/frontend domain modules and `.github/instructions/*` guidance.
- Executed required inventory commands:
  - `git status`
  - `git diff HEAD`
  - `git diff --stat HEAD`
  - `git ls-files --others --exclude-standard`
- Read each changed and new file in full.

## Stats
- Files Modified: 8
- Files Added: 15
- Files Deleted: 0
- New lines: 1584
- Deleted lines: 13

## Findings

severity: medium
file: frontend/src/features/habits/components/CompletionToggle.jsx
line: 5
issue: Completion date is derived from UTC instead of user local date.
detail: `new Date().toISOString().slice(0, 10)` uses UTC day boundaries, so users in positive/negative offsets near midnight can submit completion for the wrong calendar day. Verified with `node -e "const d = new Date('2026-03-05T00:30:00+08:00'); console.log(d.toISOString().slice(0,10));"` returning `2026-03-04`.
suggestion: Build local date string from local date parts (e.g., `const d = new Date(); const local = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}``) or use a timezone-safe date utility.

severity: medium
file: backend/app/habits/service.py
line: 97
issue: Habit listing path introduces N+1 ORM query behavior.
detail: `list_habits()` loads `Habit` rows, then `_build_habit_response()` accesses `habit.target_days` and `habit.completions` per habit, which are lazy relationships. Verified relationship loading strategy is `select` (`completions_lazy= select`, `target_days_lazy= select`), causing extra queries as habit count grows.
suggestion: Eager-load relationships in `list_habits()` and detail queries (e.g., SQLAlchemy `selectinload(Habit.target_days)` and `selectinload(Habit.completions)`) before serialization.

## Verification Notes
- No direct SQL injection, secret exposure, or obvious auth bypass issues found in reviewed scope.
- Existing tests pass for implemented flows, but current tests do not cover timezone boundary behavior or query-count regression for list operations.
