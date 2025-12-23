"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.services.database import DatabaseService


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock database for testing"""
    # Use in-memory SQLite for tests
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine


@pytest.fixture
def sample_query_request():
    """Sample query request"""
    return {
        "question": "Show all cafes"
    }


@pytest.fixture
def sample_query_response():
    """Sample query response"""
    return {
        "sql": "SELECT id, name, ST_AsGeoJSON(geom) as geojson FROM cafes",
        "results": [
            {
                "id": 1,
                "name": "Test Cafe",
                "geojson": {
                    "type": "Point",
                    "coordinates": [34.7818, 32.0853]
                }
            }
        ],
        "execution_time": 0.5,
        "result_count": 1,
        "timestamp": "2024-01-01T00:00:00"
    }


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI response"""
    class MockChoice:
        def __init__(self):
            self.message = type('Message', (), {
                'content': 'SELECT id, name, ST_AsGeoJSON(geom) as geojson FROM cafes'
            })()

    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice()]

    return MockResponse()
