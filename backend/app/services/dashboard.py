from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import AttendanceRecord, FocusSession, Task, TimeBlock, User
from app.schemas.dashboard import (
    BlockSummary,
    DashboardStats,
    DashboardSummary,
    TagMinutes,
    TaskSummary,
)

LOW_ATTENDANCE_THRESHOLD = 75.0


def _greeting(now: datetime, name: str) -> str:
    hour = now.hour
    if hour < 12:
        word = "Good morning"
    elif hour < 17:
        word = "Good afternoon"
    else:
        word = "Good evening"
    return f"{word}, {name}" if name else word


async def build_dashboard_summary(db: AsyncSession, user: User) -> DashboardSummary:
    try:
        tz = ZoneInfo(user.timezone)
    except Exception:
        tz = ZoneInfo("UTC")
    now = datetime.now(tz)
    day_start = datetime.combine(now.date(), time.min, tzinfo=tz)
    day_end = day_start + timedelta(days=1)

    blocks_result = await db.execute(
        select(TimeBlock)
        .options(selectinload(TimeBlock.tag))
        .where(
            TimeBlock.user_id == user.id,
            TimeBlock.start_at < day_end,
            TimeBlock.end_at > day_start,
            TimeBlock.is_paused.is_(False),
        )
        .order_by(TimeBlock.start_at)
    )
    blocks = list(blocks_result.scalars())

    minutes_by_tag: dict[str, TagMinutes] = {}
    for block in blocks:
        start = max(block.start_at, day_start)
        end = min(block.end_at, day_end)
        minutes = int((end - start).total_seconds() // 60)
        name = block.tag.name if block.tag else "Untagged"
        color = block.tag.color if block.tag else "#64748b"
        entry = minutes_by_tag.setdefault(name, TagMinutes(tag_name=name, color=color, minutes=0))
        entry.minutes += minutes

    tasks_result = await db.execute(
        select(Task)
        .where(
            Task.user_id == user.id,
            Task.status.notin_(("done", "cancelled")),
            Task.due_at >= day_start,
            Task.due_at < day_end,
        )
        .order_by(Task.is_urgent.desc(), Task.is_important.desc(), Task.due_at)
    )
    tasks_today = list(tasks_result.scalars())

    completed_today = await db.scalar(
        select(func.count(Task.id)).where(
            Task.user_id == user.id,
            Task.status == "done",
            Task.completed_at >= day_start,
            Task.completed_at < day_end,
        )
    )

    focus_seconds = await db.scalar(
        select(func.coalesce(func.sum(FocusSession.actual_seconds), 0)).where(
            FocusSession.user_id == user.id,
            FocusSession.kind.in_(("pomodoro", "custom")),
            FocusSession.started_at >= day_start,
            FocusSession.started_at < day_end,
        )
    )

    attendance_rows = (
        await db.execute(
            select(AttendanceRecord.attended, AttendanceRecord.total).where(
                AttendanceRecord.user_id == user.id
            )
        )
    ).all()
    attended_sum = sum(row.attended for row in attendance_rows)
    total_sum = sum(row.total for row in attendance_rows)
    attendance_pct = round(attended_sum / total_sum * 100, 1) if total_sum else None
    low_courses = sum(
        1
        for row in attendance_rows
        if row.total and (row.attended / row.total * 100) < LOW_ATTENDANCE_THRESHOLD
    )

    return DashboardSummary(
        date=now.date().isoformat(),
        greeting=_greeting(now, user.full_name.split(" ")[0] if user.full_name else ""),
        stats=DashboardStats(
            focus_minutes_today=int((focus_seconds or 0) // 60),
            focus_goal_minutes=user.daily_focus_goal_minutes,
            tasks_due_today=len(tasks_today),
            tasks_completed_today=int(completed_today or 0),
            attendance_percentage=attendance_pct,
            low_attendance_courses=low_courses,
            minutes_by_tag_today=sorted(
                minutes_by_tag.values(), key=lambda t: t.minutes, reverse=True
            ),
        ),
        blocks_today=[
            BlockSummary(
                id=b.id,
                title=b.title,
                start_at=b.start_at,
                end_at=b.end_at,
                tag_name=b.tag.name if b.tag else None,
                tag_color=b.tag.color if b.tag else None,
            )
            for b in blocks
        ],
        tasks_today=[
            TaskSummary(
                id=t.id,
                title=t.title,
                status=t.status,
                is_urgent=t.is_urgent,
                is_important=t.is_important,
                due_at=t.due_at,
            )
            for t in tasks_today
        ],
    )
