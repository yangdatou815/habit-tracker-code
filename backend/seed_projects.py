"""Seed the 11 default projects for V2 daily check-in."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the backend directory is on sys.path so app.* imports resolve.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal, engine, Base
from app.projects.models import Project

DEFAULTS = [
    {"name": "打坐两小时", "category": "静功", "sort_order": 1},
    {"name": "拉筋",       "category": "柔韧", "sort_order": 2},
    {"name": "风摆荷叶",   "category": "动功", "sort_order": 3},
    {"name": "迈毛",       "category": "动功", "sort_order": 4},
    {"name": "仙人揉腹",   "category": "养生", "sort_order": 5},
    {"name": "拍八虚",     "category": "养生", "sort_order": 6},
    {"name": "金刚功",     "category": "动功", "sort_order": 7},
    {"name": "蹲墙功",     "category": "动功", "sort_order": 8},
    {"name": "瑜伽",       "category": "柔韧", "sort_order": 9},
    {"name": "摇一摇",     "category": "动功", "sort_order": 10},
    {"name": "道具按摩",   "category": "养生", "sort_order": 11},
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Project).count()
        if existing > 0:
            print(f"Already {existing} project(s) in DB – skipping seed.")
            return
        for item in DEFAULTS:
            db.add(Project(**item))
        db.commit()
        print(f"Seeded {len(DEFAULTS)} projects.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
