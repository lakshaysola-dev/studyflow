import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BlockTag

DEFAULT_BLOCK_TAGS: list[dict[str, str]] = [
    {"name": "Deep Work", "color": "#8b5cf6", "icon": "brain"},
    {"name": "Productivity", "color": "#22c55e", "icon": "zap"},
    {"name": "Lectures", "color": "#3b82f6", "icon": "graduation-cap"},
    {"name": "Relaxation", "color": "#f59e0b", "icon": "coffee"},
    {"name": "Exercise", "color": "#ef4444", "icon": "dumbbell"},
    {"name": "Sleep", "color": "#64748b", "icon": "moon"},
]


async def create_default_block_tags(db: AsyncSession, user_id: uuid.UUID) -> list[BlockTag]:
    tags = [BlockTag(user_id=user_id, **tag) for tag in DEFAULT_BLOCK_TAGS]
    db.add_all(tags)
    await db.flush()
    return tags
