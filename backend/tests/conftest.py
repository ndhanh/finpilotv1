"""
Pytest configuration and fixtures for FinPilot backend testing.

Provides database fixtures, client fixtures, and test data for comprehensive testing.
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from src.config import settings
from src.database import Base, get_db
from src.main import app

# Test database URL - use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = async_sessionmaker(test_engine, expire_on_commit=False)

    async with async_session as session:
        yield session
        # Rollback any changes after test
        await session.rollback()


@pytest.fixture
def test_app(test_session: AsyncSession) -> FastAPI:
    """Create test FastAPI application with test database."""

    async def override_get_db():
        yield test_session

    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db

    return app


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    """Create test client for API testing."""
    return TestClient(test_app)


# Calculation testing fixtures
@pytest.fixture
def sample_projection_inputs():
    """Sample projection calculation inputs for testing."""
    return {
        "target_amount": 500_000_000,  # 500M VND
        "timeline_years": 5,
        "monthly_contribution": 5_000_000,  # 5M VND/month
        "current_savings": 50_000_000,  # 50M VND
        "current_debt": 20_000_000,  # 20M VND
        "expected_return_rate": 0.07,  # 7%
        "inflation_rate": 0.04,  # 4%
        "debt_interest_rate": 0.12,  # 12%
    }


@pytest.fixture
def sample_house_purchase_goal():
    """Sample house purchase goal data."""
    return {
        "name": "Dream Home Purchase",
        "description": "Buying a house in Hanoi",
        "goal_type": "house_purchase",
        "target_amount": 2_000_000_000,  # 2B VND
        "target_date": "2030-12-31",
        "current_savings": 200_000_000,  # 200M VND
        "assumptions": {
            "down_payment_percentage": 0.20,
            "closing_costs_percentage": 0.04,
            "property_location": "hanoi",
        },
    }


@pytest.fixture
def sample_emergency_fund_goal():
    """Sample emergency fund goal data."""
    return {
        "name": "Emergency Fund",
        "description": "6 months of expenses",
        "goal_type": "emergency_fund",
        "target_amount": 60_000_000,  # 60M VND (10M/month * 6)
        "target_date": "2025-06-30",
        "current_savings": 10_000_000,  # 10M VND
        "assumptions": {"monthly_expenses": 10_000_000, "months_coverage": 6},
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
    }


@pytest.fixture
def sample_recommendation_context():
    """Sample context for recommendation engine testing."""
    return {
        "target_amount": 1_000_000_000,  # 1B VND
        "timeline_months": 60,  # 5 years
        "monthly_contribution": 10_000_000,  # 10M VND/month
        "current_savings": 100_000_000,  # 100M VND
        "current_debt": 50_000_000,  # 50M VND
        "is_achievable": True,
        "shortfall_amount": 0,
        "estimated_monthly_income": 30_000_000,  # 30M VND
    }


# Async test utilities
@pytest.fixture
async def async_client(test_app: FastAPI) -> AsyncGenerator[TestClient, None]:
    """Create async test client for API testing."""
    from httpx import AsyncClient

    async with AsyncClient(app=test_app, base_url="http://testserver") as client:
        yield client


# Database cleanup fixture
@pytest.fixture(autouse=True)
async def clean_db(test_session: AsyncSession):
    """Clean database between tests."""
    # This runs before each test
    yield
    # Clean up after each test
    for table in reversed(Base.metadata.sorted_tables):
        await test_session.execute(table.delete())
    await test_session.commit()


# Test data factories
def create_test_user_data(
    email: str = "test@example.com", full_name: str = "Test User"
):
    """Factory for creating test user data."""
    return {"email": email, "full_name": full_name, "password": "testpassword123"}


def create_test_goal_data(
    name: str = "Test Goal",
    goal_type: str = "house_purchase",
    target_amount: int = 500_000_000,
    target_date: str = "2030-12-31",
    current_savings: int = 50_000_000,
):
    """Factory for creating test goal data."""
    return {
        "name": name,
        "description": f"Test {goal_type} goal",
        "goal_type": goal_type,
        "target_amount": target_amount,
        "target_date": target_date,
        "current_savings": current_savings,
        "assumptions": {},
    }


def create_test_projection_data(
    target_amount: int = 500_000_000,
    timeline_years: int = 5,
    monthly_contribution: int = 5_000_000,
    current_savings: int = 50_000_000,
):
    """Factory for creating test projection data."""
    return {
        "target_amount": target_amount,
        "timeline_years": timeline_years,
        "monthly_contribution": monthly_contribution,
        "current_savings": current_savings,
        "current_debt": 0,
        "expected_return_rate": 0.07,
        "inflation_rate": 0.04,
        "debt_interest_rate": 0.12,
    }
