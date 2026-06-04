from sqlalchemy import Column,ForeignKey,UniqueConstraint,DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from datetime import datetime
from sqlalchemy.orm import relationship


from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True)

    email = Column(String, unique=True)

    password = Column(String)

    followers=relationship("Follower",foreign_keys="Follower.followed_id", back_populates="followed",cascade="all,delete-orphan")
    following=relationship("Follower",foreign_keys="Follower.follower_id", back_populates="follower_user",cascade="all,delete-orphan")


class Follower(Base):
    __tablename__ = "followers"

    id          = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅
    followed_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅
    created_at  = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="uq_follow_pair"),
    )

    follower_user = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed      = relationship("User", foreign_keys=[followed_id], back_populates="followers")
