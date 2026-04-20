"""
Tests for GET /activities endpoint
Follows AAA (Arrange-Act-Assert) pattern
"""
import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all available activities.
    
    AAA Pattern:
    - Arrange: Use the TestClient fixture
    - Act: Call GET /activities endpoint
    - Assert: Verify response contains all 9 activities
    """
    # Arrange
    expected_activity_count = 9
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count
    assert all(isinstance(name, str) for name in activities.keys())


def test_get_activities_response_schema(client):
    """
    Test that each activity in GET /activities response has required fields.
    
    AAA Pattern:
    - Arrange: Define expected fields
    - Act: Call GET /activities endpoint
    - Assert: Verify all activities have required fields with correct types
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        assert all(isinstance(email, str) for email in activity_data["participants"])


def test_get_activities_contains_chess_club(client):
    """
    Test that Chess Club activity exists with correct data.
    
    AAA Pattern:
    - Arrange: Define expected Chess Club data
    - Act: Call GET /activities endpoint
    - Assert: Verify Chess Club exists and has expected structure
    """
    # Arrange
    expected_name = "Chess Club"
    expected_initial_participant_count = 2
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert expected_name in activities
    chess_club = activities[expected_name]
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) == expected_initial_participant_count
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
