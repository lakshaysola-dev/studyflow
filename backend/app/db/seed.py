"""Seed a demo user with sample blocks and tasks for local development.

Usage: python -m app.db.seed [--email EMAIL] [--password PASSWORD]
"""

import argparse
import asyncio
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models import BlockTag, Task, TimeBlock, User
from app.services.defaults import create_default_block_tags

DEMO_BLOCKS = [
    ("Morning review", "Productivity", 8, 0, 8, 45),
    ("Data Structures lecture", "Lectures", 9, 0, 10, 30),
    ("Operating Systems lecture", "Lectures", 11, 0, 12, 30),
    ("Lunch & walk", "Relaxation", 12, 30, 13, 30),
    ("DSA problem set", "Deep Work", 14, 0, 16, 0),
    ("Gym", "Exercise", 17, 0, 18, 0),
    ("Math revision", "Deep Work", 19, 30, 21, 0),
]

DEMO_TASKS = [
    ("Submit OS assignment 2", True, True, 18, 0),
    ("Read chapter 5 of DSA textbook", False, True, 21, 0),
    ("Reply to project group on Discord", True, False, 15, 0),
    ("Reorganise notes folder", False, False, 22, 0),
]


async def seed(email: str, password: str) -> None:
    async with AsyncSessionLocal() as db:
        user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
        if user is None:
            user = User(
                email=email,
                hashed_password=hash_password(password),
                full_name="Demo Student",
            )
            db.add(user)
            await db.flush()
            await create_default_block_tags(db, user.id)

        tags = {
            t.name: t
            for t in (await db.execute(select(BlockTag).where(BlockTag.user_id == user.id)))
            .scalars()
            .all()
        }
        tz = ZoneInfo(user.timezone)
        today = datetime.now(tz).date()

        def at(h: int, m: int) -> datetime:
            return datetime.combine(today, time(h, m), tzinfo=tz)

        for title, tag_name, sh, sm, eh, em in DEMO_BLOCKS:
            db.add(
                TimeBlock(
                    user_id=user.id,
                    tag_id=tags[tag_name].id if tag_name in tags else None,
                    title=title,
                    start_at=at(sh, sm),
                    end_at=at(eh, em),
                )
            )
        for title, urgent, important, h, m in DEMO_TASKS:
            db.add(
                Task(
                    user_id=user.id,
                    title=title,
                    is_urgent=urgent,
                    is_important=important,
                    due_at=at(h, m),
                )
            )
        db.add(
            Task(
                user_id=user.id,
                title="Morning stretch",
                status="done",
                completed_at=datetime.now(tz) - timedelta(hours=1),
                due_at=at(7, 30),
            )
        )
        await db.commit()
    print(f"Seeded demo data for {email}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", default="demo@studyflow.app")
    parser.add_argument("--password", default="password123")
    args = parser.parse_args()
    asyncio.run(seed(args.email, args.password))


if __name__ == "__main__":
    main()
