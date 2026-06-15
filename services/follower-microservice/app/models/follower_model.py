from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Index
from app.database import Base


class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(Integer, nullable=False, primary_key=True)
    followed_id = Column(Integer, nullable=False, primary_key=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    __table_args__ = (
        Index("ix_follows_follower_id", "follower_id"),
        Index("ix_follows_followed_id", "followed_id"),
    )