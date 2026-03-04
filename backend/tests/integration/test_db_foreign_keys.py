from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.habits.models import Completion


def test_completion_requires_existing_habit(db_session) -> None:
    db_session.add(
        Completion(
            habit_id=999,
            completed_date=date(2026, 3, 4),
            status="done",
        )
    )

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
