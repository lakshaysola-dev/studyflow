import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class BlockTag(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Categories used by the Block System: Productivity, Lectures, Relaxation, Deep Work..."""

    __tablename__ = "block_tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_block_tags_user_name"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    color: Mapped[str] = mapped_column(String(16), nullable=False, default="#8b5cf6")
    icon: Mapped[str] = mapped_column(String(40), nullable=False, default="circle")

    blocks: Mapped[list["TimeBlock"]] = relationship(back_populates="tag")


class TimeBlock(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "time_blocks"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    tag_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("block_tags.id", ondelete="SET NULL"), nullable=True
    )
    task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_recurring: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    rrule: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_paused: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    tag: Mapped[BlockTag | None] = relationship(back_populates="blocks")
