# Code Review: Phase 3 — Metrics & Dashboard Visualization

**Commit:** `4d7466095fc15883f0b075a26558b5b5b9361d97`
**Date:** 2026-03-05

## Stats

- Files Modified: 8
- Files Added: 11
- Files Deleted: 0
- New lines: +1421
- Deleted lines: -25

## Issues

```
severity: medium
file: backend/app/stats/service.py
line: 33-37
issue: Eager-loading ALL completions into memory — unbounded query
detail: `selectinload(Habit.completions)` fetches every completion row for every active habit into Python memory. For an MVP this is acceptable, but as data grows (hundreds of habits × thousands of completion rows), this will become a memory and performance bottleneck. The completions could be filtered at the DB level to only load rows within the date range (and today).
suggestion: Replace the eager-load of completions with a filtered subquery or a separate targeted query that only fetches completions within `[from_date, to_date]` plus today's date. Example: use `contains_eager` with a pre-filtered join, or run a separate aggregation query.
```

```
severity: medium
file: backend/app/stats/service.py
line: 55-59
issue: completed_today and total_today are computed regardless of date range
detail: The `completed_today` and `total_today` fields are always relative to the actual current date, even when the caller passes a historical date range like `?from=2025-01-01&to=2025-01-31`. This is arguably correct behavior (the dashboard always wants "today"), but the coupling is implicit — the response mixes range-scoped data (completion_rate) with today-scoped data (completed_today, total_today) without documentation clarifying this.
suggestion: Add a docstring to `compute_stats_overview` clarifying that `completed_today` and `total_today` are always anchored to the current date regardless of the from/to range. Alternatively, consider including a `today` field in the response so the client knows what "today" means on the server.
```

```
severity: low
file: frontend/src/features/dashboard/api/stats.js
line: 3-14
issue: Duplicated withSearchParams helper across two feature modules
detail: The `withSearchParams` function is copied verbatim from `frontend/src/features/habits/api/habits.js`. This is a DRY violation — two identical 12-line functions exist in the codebase.
suggestion: Extract `withSearchParams` into `frontend/src/lib/api.js` (alongside `request`) and import it from both `habits/api/habits.js` and `dashboard/api/stats.js`. This was noted as an acceptable tradeoff in the plan but should be cleaned up.
```

```
severity: low
file: frontend/src/features/habits/components/WeeklyHeatmap.jsx
line: 19
issue: toLocaleDateString("en-US") depends on locale availability in the JS runtime
detail: `getDayAbbrev` and the weekday lookup both use `toLocaleDateString("en-US", { weekday: "short" })` which returns locale-dependent strings like "Mon", "Tue", etc. If a JS runtime doesn't have the "en-US" locale data (unusual but possible in minimal server-side rendering contexts), the mapping through `DAY_NAME_MAP` could fail silently, producing `undefined` and causing `targetDays.includes(undefined)` to always be false — making all days appear as "not scheduled".
suggestion: This is very unlikely to be an issue in browser environments but worth noting. A safer alternative would be to compute the day abbreviation from the weekday index, similar to the backend's `WEEKDAY_ABBREV` tuple approach: `const WEEKDAY_ABBREV = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]; const abbrev = WEEKDAY_ABBREV[dayDate.getDay()];`
```

```
severity: low
file: frontend/src/features/habits/components/WeeklyHeatmap.jsx
line: 7-14
issue: getLast7Days() is called on every render without memoization
detail: `getLast7Days()` creates 7 new Date objects on every render of every HabitCard. Given that the date won't change during a session and this component is rendered once per habit, the performance impact is negligible, but it's wasteful in principle.
suggestion: No immediate action needed given the MVP scale. If habit count grows large, consider memoizing with `useMemo` or extracting to a module-level constant.
```

```
severity: low
file: backend/tests/unit/test_health_or_stats_smoke.py
line: 1-16
issue: Lost test coverage for invalid date range at service layer
detail: The old `test_overview_raises_for_invalid_date_range` test was removed entirely when the file was updated. The date range validation moved to the router layer (which returns 422) and is tested in `test_stats_api.py::test_stats_overview_rejects_reversed_dates`, so coverage exists — but there's no longer a unit test verifying that the service handles or rejects reversed dates if called directly.
suggestion: This is acceptable since the router enforces the constraint before the service is called. No action needed, but document that date validation is a router responsibility.
```

## Summary

The implementation is solid overall. The code follows existing codebase patterns closely, the router/service/schema separation is clean, and test coverage is comprehensive (12 backend tests, 7 frontend tests). The main technical concern is the unbounded eager-loading of completions in the stats service, which won't be an issue at MVP scale but should be addressed as the app grows. No security issues, no logic errors in the core computation, and the frontend components handle loading/error states correctly.

**Verdict:** Code review passed with minor issues. No critical or high-severity bugs detected.
