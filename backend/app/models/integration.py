import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

PROVIDERS = ("slcm", "gmail", "outlook", "telegram", "discord")


class IntegrationCredential(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Encrypted third-party credentials / OAuth tokens. Payload is Fernet-encrypted JSON."""

    __tablename__ = "integration_credentials"
    __table_args__ = (UniqueConstraint("user_id", "provider", name="uq_integration_user_provider"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    encrypted_payload: Mapped[str] = mapped_column(Text, nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)


class ScrapeCache(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Postgres-backed cache for scraped portal data (stands in for Redis)."""

    __tablename__ = "scrape_cache"
    __table_args__ = (UniqueConstraint("user_id", "cache_key", name="uq_scrape_cache_user_key"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    cache_key: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
