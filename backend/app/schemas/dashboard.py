import uuid
from datetime import datetime

from pydantic import BaseModel


class BlockSummary(BaseModel):
    id: uuid.UUID
    title: str
    start_at: datetime
    end_at: datetime
    tag_name: str | None
    tag_color: str | None


class TaskSummary(BaseModel):
    id: uuid.UUID
    title: str
    status: str
    is_urgent: bool
    is_important: bool
    due_at: datetime | None


class TagMinutes(BaseModel):
    tag_name: str
    color: str
    minutes: int


class DashboardStats(BaseModel):
    focus_minutes_today: int
    focus_goal_minutes: int
    tasks_due_today: int
    tasks_completed_today: int
    attendance_percentage: float | None
    low_attendance_courses: int
    minutes_by_tag_today: list[TagMinutes]


class DashboardSummary(BaseModel):
    date: str
    greeting: str
    stats: DashboardStats
    blocks_today: list[BlockSummary]
    tasks_today: list[TaskSummary]
