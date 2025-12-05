"""
Pytest configuration and shared fixtures for backend tests.
Provides database setup/teardown and test client.
"""
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from src.models.base import Base
from src.app import create_app


# Test database URL - separate from development database
TEST_DATABASE_URL = "postgresql+asyncpg://annhoward@localhost:5432/codementor_test"


@pytest.fixture(scope="session")
def event_loop():
    """
    Create event loop for async tests.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """
    Create test database engine for the entire test session.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables after all tests complete
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session for each test.
    Automatically rolls back changes after each test.
    """
    # Create session factory
    async_session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_factory() as session:
        # Begin a transaction
        async with session.begin():
            yield session
            # Transaction is automatically rolled back after test


@pytest.fixture
async def app():
    """
    Create test application instance.
    """
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
async def client(app):
    """
    Create test client for making API requests.
    """
    async with app.test_client() as test_client:
        yield test_client
