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

---

## V2: 每日多项目打卡系统

### V2.1 概述
改造为 **每日多项目打卡** 平台，用户每天对多个固定练习项目进行打卡记录。核心关注两个视图：
1. **今日打卡流水**：清晰展示今天每个项目的打卡状态（已完成/未完成），一键打卡。
2. **历史打卡日历**：查看过去任一天所有项目的打卡情况。

### V2.2 默认打卡项目
| # | 项目名 | 类别 |
|---|---|---|
| 1 | 打坐两小时 | 静功 |
| 2 | 拉筋 | 柔韧 |
| 3 | 风摆荷叶 | 动功 |
| 4 | 迈毛 | 动功 |
| 5 | 仙人揉腹 | 养生 |
| 6 | 拍八虚 | 养生 |
| 7 | 金刚功 | 动功 |
| 8 | 蹲墙功 | 动功 |
| 9 | 瑜伽 | 柔韧 |
| 10 | 摇一摇 | 动功 |
| 11 | 道具按摩 | 养生 |

### V2.3 数据模型

#### `projects` 表
| Column | Type | Notes |
|---|---|---|
| id | int PK | Auto-increment |
| name | str(100) | NOT NULL |
| category | str(50) | "静功", "柔韧", "动功", "养生" |
| sort_order | int | Display order |
| is_active | bool | Default true |
| created_at | datetime | Server default |

#### `checkins` 表
| Column | Type | Notes |
|---|---|---|
| id | int PK | |
| project_id | FK → projects | CASCADE |
| checkin_date | date | |
| status | str(20) | "done" or "not_done" |
| created_at | datetime | |

Unique constraint: `(project_id, checkin_date)`.

### V2.4 API 端点

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/v1/projects` | 列出所有项目 |
| `POST` | `/api/v1/projects` | 创建新项目 |
| `PATCH` | `/api/v1/projects/{id}` | 编辑项目 |
| `DELETE` | `/api/v1/projects/{id}` | 删除项目 |
| `PUT` | `/api/v1/checkins/{project_id}/{date}` | 打卡/取消打卡 |
| `GET` | `/api/v1/checkins/today` | 今日所有项目打卡状态 |
| `GET` | `/api/v1/checkins/date/{date}` | 某一天所有项目打卡状态 |
| `GET` | `/api/v1/checkins/history?from=&to=` | 日期范围内每天打卡汇总 |
| `GET` | `/api/v1/stats/overview` | 总体统计（连续天数、完成率等） |

### V2.5 前端页面

| Route | 页面 | 说明 |
|---|---|---|
| `/` | 今日打卡 | 显示所有项目，一键打卡/取消，实时流水状更新 |
| `/history` | 历史视图 | 日历选择器 + 选定日期的打卡详情 |
| `/projects` | 项目管理 | 增删改查项目列表 |

### V2.6 用户故事

1. 作为用户，我打开首页就能看到今天所有11个项目的打卡状态。
2. 作为用户，我点击一下就能完成某个项目的打卡，页面即时反馈。
3. 作为用户，我能看到今天已完成 X/11 的进度。
4. 作为用户，我能切换到历史视图，选择任一天查看那天的打卡情况。
5. 作为用户，我能在日历上看到每天的完成比例（颜色深浅）。
6. 作为用户，我能添加、编辑或删除打卡项目。

### V2.7 UI 设计
- **今日视图**：项目列表，每行显示项目名 + 类别标签 + 打卡按钮（✅/⬜）。已完成项目有绿色背景。顶部显示进度条 "X/11 已完成"。
- **历史视图**：左侧日历（月视图），每天格子颜色深浅表示完成比例。右侧显示选中日期的打卡列表。
- **移动优先**，简洁无干扰。
- 中文界面。

### V2.8 实施计划
1. **Phase 1**: 数据库迁移（habits→projects, completions→checkins），seed 默认11个项目
2. **Phase 2**: 后端 API（项目 CRUD + 打卡 + 历史查询）
3. **Phase 3**: 前端今日打卡页 + 历史视图页 + 项目管理页
4. **Phase 4**: 测试、优化、部署

---

## 10. Definition of Done (DoD)

所有变更在提交前必须通过以下质量门禁：

### 10.1 覆盖率门禁

变更涉及的后端模块测试覆盖率 >= 90%.

```bash
cd backend
pytest tests/ -q --cov=app --cov-report=term-missing --cov-fail-under=90
```

### 10.2 SCT 门禁（系统组件测试映射）

V2.6 中的每个用户故事（US），必须对应：
- 至少 **1 个** 正常路径（happy-path）测试用例
- 至少 **3 个** 异常路径（validation / error / empty-state / boundary）测试用例

| US | 正常用例 | 异常用例 |
|---|---|---|
| US1 今日打卡状态 | GET /checkins/today 返回所有项目 | 无项目时返回空、无效日期格式、数据库异常 |
| US2 一键打卡 | PUT /checkins/{id}/{date} 切换状态 | 不存在的项目ID、无效日期、重复打卡覆盖 |
| US3 进度显示 | 返回正确 done_count/total | 全部完成、全部未完成、部分完成 |
| US4 历史查看 | GET /checkins/date/{date} 正确返回 | 未来日期、无数据日期、无效格式 |
| US5 日历完成比例 | GET /checkins/history 返回正确汇总 | from > to、无数据范围、超大范围 |
| US6 项目管理 | POST/PATCH/DELETE 正常 CRUD | 名称过长、不存在的ID更新/删除、重复名称 |

### 10.3 冒烟测试门禁

关键冒烟测试套件必须通过：

```bash
pytest tests/ -m smoke -q
```

冒烟测试覆盖：
- 健康检查端点
- 项目列表 API
- 今日打卡 API
- 打卡切换 API

### 10.4 提交前检查清单

- [ ] 覆盖率门禁通过 (>= 90%)
- [ ] SCT 门禁通过（每个变更的 US 有 >= 1 正常 + >= 3 异常用例）
- [ ] 冒烟测试通过
- [ ] 前端构建无报错 (`npm run build`)
- [ ] README.md 与实际代码同步
