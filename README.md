# Habit Tracker — 每日多项目打卡系统

全栈 Web 应用，用于快速每日多项目打卡（修炼/锻炼），道教暗色主题 UI。

## Tech Stack

- Backend: Python 3.9+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, SQLite, structlog
- Frontend: React 18, Vite 5, Tailwind CSS 4, TanStack Query, react-router-dom
- Testing: pytest, pytest-cov, httpx, Vitest
- UI: 道教暗色主题（太极图、祥云纹、金色/翡翠配色）

## Project Structure

```text
habit-tracker-code/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── habits/          # V1 习惯追踪
│   │   ├── projects/        # V2 打卡项目 + 打卡记录
│   │   └── stats/
│   ├── alembic/
│   ├── tests/
│   │   ├── integration/     # API 集成测试 + SCT 测试
│   │   └── unit/
│   ├── seed_projects.py     # 种子数据（11个默认项目）
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── features/projects/  # API 客户端
│   │   ├── pages/              # TodayPage, ProjectsPage
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
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python seed_projects.py          # 初始化11个默认项目
uvicorn app.main:app --host 0.0.0.0 --port 8001
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
ruff check .
black --check .
pytest tests/ -q                                         # 全部测试
pytest tests/ -m smoke -q                                # 冒烟测试
pytest tests/ -q --cov=app --cov-report=term-missing --cov-fail-under=90  # 覆盖率门禁
```

### Frontend

```bash
cd frontend
npm run build
npm run test -- --run
```

## DoD (Definition of Done) 质量门禁

提交前必须通过：

1. **覆盖率 >= 90%**: `pytest tests/ -q --cov=app --cov-fail-under=90`
2. **SCT 映射**: 每个 US 至少 1 正常 + 3 异常测试（see `tests/integration/test_projects_sct.py`）
3. **冒烟测试**: `pytest tests/ -m smoke -q`
4. **前端构建**: `npm run build`

详见 [PRD.md §10](PRD.md) 完整 DoD 定义。

## V2 打卡项目

默认 11 个打卡项目（分 4 类）：

| 类别 | 项目 |
|---|---|
| 静功 | 打坐两小时 |
| 柔韧 | 拉筋、风摆荷叶、迈毛 |
| 动功 | 金刚功、蹲墙功、瑜伽、摇一摇 |
| 养生 | 仙人揉腹、拍八虚、道具按摩 |

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

### V2 打卡 API

- `GET /api/v1/projects` — 列出所有项目
- `POST /api/v1/projects` — 创建新项目
- `PATCH /api/v1/projects/{id}` — 编辑项目
- `DELETE /api/v1/projects/{id}` — 删除项目
- `PUT /api/v1/checkins/{project_id}/{date}` — 打卡/取消
- `GET /api/v1/checkins/today` — 今日所有项目状态
- `GET /api/v1/checkins/date/{date}` — 某日所有项目状态
- `GET /api/v1/checkins/history?from_date=&to_date=` — 日期范围汇总

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
