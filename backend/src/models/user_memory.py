"""
User Memory model for personalization and learning history tracking.
Stores individual user's learning patterns, strengths, weaknesses, and preferences.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from src.models.base import Base


class UserMemory(Base):
    """
    User Memory model for storing personalization data and learning history.
    Tracks user's learning patterns, strengths, weaknesses, and preferences over time.
    """

    __tablename__ = "user_memory"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True  # One memory record per user
    )

    # Learning patterns
    learning_pace: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )  # fast, moderate, slow
    preferred_difficulty: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )  # current preferred difficulty level

    # Strengths and weaknesses stored as JSON arrays of topics
    identified_strengths: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )  # {"topics": ["arrays", "recursion"], "updated_at": "2025-01-01"}
    identified_weaknesses: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )  # {"topics": ["dynamic_programming", "graphs"], "updated_at": "2025-01-01"}

    # Topic mastery tracking
    topic_mastery: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )  # {"arrays": 0.85, "linked_lists": 0.65, "trees": 0.40}

    # Interest areas
    interest_areas: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )  # {"web_development": 0.9, "data_science": 0.6}

    # Performance metrics
    average_completion_time_minutes: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    average_hints_per_exercise: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    average_grade: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )  # 0-100 scale

    # Exercise history summary
    total_exercises_attempted: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    total_exercises_completed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    total_exercises_skipped: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    # Career progression tracking
    career_goal_progress: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )  # {"goal": "Backend Developer", "progress": 0.35, "milestones": [...]}

    # Tutor interaction patterns
    common_questions: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )  # ["How do I optimize this?", "What's the time complexity?"]

    # Additional metadata for personalization
    personalization_metadata: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )  # Flexible field for additional personalization data

    # Last analysis timestamp
    last_analyzed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
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
        """String representation of UserMemory."""
        return f"<UserMemory(id={self.id}, user_id={self.user_id}, avg_grade={self.average_grade})>"
