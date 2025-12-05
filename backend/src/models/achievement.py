"""
Achievement models for tracking user accomplishments and badges.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
import enum
from src.models.base import Base


class AchievementCategory(str, enum.Enum):
    """Achievement category enumeration."""
    STREAK = "streak"  # Consecutive day achievements
    EXERCISE = "exercise"  # Exercise completion milestones
    GITHUB = "github"  # GitHub review achievements
    COMMUNITY = "community"  # Community participation
    MENTORSHIP = "mentorship"  # Mentoring achievements
    SKILL = "skill"  # Skill mastery achievements
    SPECIAL = "special"  # Special event achievements


class Achievement(Base):
    """
    Achievement model defining available badges and milestones.
    """

    __tablename__ = "achievements"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Achievement identification
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )  # URL-friendly identifier

    # Achievement details
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[AchievementCategory] = mapped_column(
        SQLEnum(AchievementCategory, name="achievement_category_enum"),
        nullable=False,
        index=True
    )

    # Requirements and metadata
    requirement_value: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # e.g., 7 for 7-day streak, 100 for 100 exercises
    requirement_description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )  # Human-readable requirement

    # Visual representation
    icon_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    badge_color: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )  # e.g., "gold", "silver", "bronze", or hex color

    # Achievement properties
    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )  # Hidden until earned
    is_repeatable: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )  # Can be earned multiple times
    points: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )  # Point value for gamification

    # Display order
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )  # For sorting achievements

    # Active status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation of Achievement."""
        return f"<Achievement(id={self.id}, name='{self.name}', category='{self.category}')>"


class UserAchievement(Base):
    """
    User Achievement model tracking which achievements users have earned.
    """

    __tablename__ = "user_achievements"

    # Composite primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    achievement_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("achievements.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Achievement progress
    progress_current: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Current progress toward achievement
    progress_target: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Target value to earn achievement

    # Completion tracking
    earned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    earned_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Notification tracking
    notification_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # For repeatable achievements
    times_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Ensure user can't have duplicate achievements (unless repeatable)
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "achievement_id",
            name="uq_user_achievement"
        ),
    )

    def __repr__(self) -> str:
        """String representation of UserAchievement."""
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id}, earned={self.earned})>"
