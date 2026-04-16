---
applyTo: "backend/tests/**"
---

# Testing Instructions

## 测试分层

- **Unit tests** (`tests/unit/`): 纯服务逻辑，mock 外部依赖，快速执行
- **Integration tests** (`tests/integration/`): httpx TestClient + 内存 SQLite，验证 API 合约
- **SCT tests** (`tests/integration/test_*_sct.py`): 系统组件测试，覆盖每个 US 的正常 + 异常路径
- **Smoke tests** (`@pytest.mark.smoke`): 关键路径冒烟，CI 快速验证

## DoD 质量门禁

所有提交必须通过：

1. **覆盖率 >= 90%**
   ```bash
   pytest tests/ -q --cov=app --cov-report=term-missing --cov-fail-under=90
   ```

2. **SCT 映射**（每个 US >= 1 正常 + >= 3 异常用例）
   - 正常路径在 `test_projects_api.py`
   - 异常路径在 `test_projects_sct.py`

3. **冒烟测试通过**
   ```bash
   pytest tests/ -m smoke -q
   ```

## Marker 使用

```python
import pytest

@pytest.mark.smoke
def test_critical_path(client):
    ...
```

注册在 `pytest.ini`:
```ini
markers =
    smoke: critical path smoke tests
```

## Fixture 约定

- `db_session`: 函数作用域，内存 SQLite，每个测试独立数据库
- `client`: httpx TestClient，注入 db_session
- `_seed_projects`: 创建测试用项目种子数据（以 `_` 前缀表示无返回值 fixture）

## SCT 用户故事映射

| US | 测试文件 | 正常路径 | 异常路径 |
|---|---|---|---|
| US1 今日状态 | test_projects_api + _sct | test_today_checkins | no_projects, all_inactive, idempotent |
| US2 一键打卡 | test_projects_api + _sct | test_toggle_checkin | nonexistent, invalid_date, invalid_status, overwrite |
| US3 进度 | test_projects_api + _sct | test_today_with_done | all_done, all_undone, partial |
| US4 历史查看 | test_projects_api + _sct | test_date_checkins | no_data, invalid_format, future |
| US5 日历汇总 | test_projects_api + _sct | test_history | no_data_range, from_after_to, missing_params |
| US6 项目管理 | test_projects_api + _sct | create/update/delete | empty_name, missing_name, update/delete_nonexistent |
