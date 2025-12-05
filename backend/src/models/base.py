"""
Database base configuration and session management.
Provides SQLAlchemy declarative base and database connection setup.
"""
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from src.config import settings
from src.logging_config import get_logger

logger = get_logger(__name__)

# SQLAlchemy declarative base
Base = declarative_base()

# Global database engine and session factory
_engine: Optional[AsyncEngine] = None
_async_session_factory: Optional[async_sessionmaker] = None


def get_database_url() -> str:
    """
    Get database URL with async driver.

    Returns:
        Database URL string with asyncpg driver
    """
    # Replace postgresql:// with postgresql+asyncpg:// for async support
    url = settings.database_url
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


async def init_db() -> None:
    """Initialize database connection and create engine."""
    global _engine, _async_session_factory

    if _engine is not None:
        logger.warning("Database already initialized")
        return

    database_url = get_database_url()

    logger.info("Initializing database connection")

    # Create async engine
    _engine = create_async_engine(
        database_url,
        echo=settings.debug,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_pre_ping=True,  # Verify connections before using
    )

    # Create session factory
    _async_session_factory = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    logger.info(
        "Database initialized",
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
    )


async def close_db() -> None:
    """Close database connection and dispose engine."""
    global _engine, _async_session_factory

    if _engine is None:
        logger.warning("Database not initialized")
        return

    logger.info("Closing database connection")

    await _engine.dispose()
    _engine = None
    _async_session_factory = None

    logger.info("Database connection closed")


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session as async context manager.

    Yields:
        AsyncSession for database operations

    Example:
        async with get_db_session() as session:
            result = await session.execute(query)
    """
    if _async_session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with _async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables. For development only."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    logger.info("Creating database tables")

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created")


async def drop_tables() -> None:
    """Drop all database tables. For development/testing only."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    logger.warning("Dropping all database tables")

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    logger.info("Database tables dropped")
