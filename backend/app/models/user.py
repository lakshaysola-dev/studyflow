from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="Asia/Kolkata")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # Pomodoro defaults (minutes)
    focus_minutes: Mapped[int] = mapped_column(nullable=False, default=25)
    short_break_minutes: Mapped[int] = mapped_column(nullable=False, default=5)
    long_break_minutes: Mapped[int] = mapped_column(nullable=False, default=15)
    daily_focus_goal_minutes: Mapped[int] = mapped_column(nullable=False, default=240)
