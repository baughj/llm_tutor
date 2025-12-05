"""
Conversation model for chat history with LLM tutor.
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
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
import enum
from src.models.base import Base


class MessageRole(str, enum.Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Conversation(Base):
    """Conversation model for organizing chat sessions."""

    __tablename__ = "conversations"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Conversation metadata
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    context_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # exercise, general, code_review

    # Related entity (if applicable)
    exercise_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("exercises.id", ondelete="SET NULL"),
        nullable=True
    )

    # Message count for quick reference
    message_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

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
        """String representation of Conversation."""
        return f"<Conversation(id={self.id}, user_id={self.user_id}, messages={self.message_count})>"


class Message(Base):
    """Message model for individual chat messages."""

    __tablename__ = "messages"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign key
    conversation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Message details
    role: Mapped[MessageRole] = mapped_column(
        SQLEnum(MessageRole, name="message_role_enum"),
        nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Metadata
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    message_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    def __repr__(self) -> str:
        """String representation of Message."""
        return f"<Message(id={self.id}, role='{self.role}', conversation_id={self.conversation_id})>"
