"""
Pytest configuration and fixtures for FastAPI tests
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient with a fresh app instance.
    Resets activities data before each test to ensure isolation.
    """
    # Store original activities
    original_activities = {
        key: {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy(),
        }
        for key, value in activities.items()
    }
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Reset activities to original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_activity():
    """
    Provide a sample activity for testing.
    """
    return {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
    }


@pytest.fixture
def sample_email():
    """
    Provide a sample email for testing.
    """
    return "test@mergington.edu"
