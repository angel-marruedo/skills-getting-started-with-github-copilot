"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint
Follows AAA (Arrange-Act-Assert) pattern
"""
import pytest


def test_remove_participant_success(client):
    """
    Test successful removal of a participant from an activity.
    
    AAA Pattern:
    - Arrange: Get activity with existing participant
    - Act: Call DELETE endpoint to remove participant
    - Assert: Verify response success and participant is removed
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]


def test_remove_participant_updates_list(client):
    """
    Test that removing a participant actually removes them from the activity.
    
    AAA Pattern:
    - Arrange: Get initial participant count
    - Act: Remove a participant
    - Assert: Participant count decreased and email is not in list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Get initial state
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[activity_name]["participants"])
    assert email in activities_before[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_after = client.get("/activities").json()
    final_count = len(activities_after[activity_name]["participants"])
    assert final_count == initial_count - 1
    assert email not in activities_after[activity_name]["participants"]


def test_remove_participant_activity_not_found(client):
    """
    Test that removing from nonexistent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare nonexistent activity name
    - Act: Call DELETE on nonexistent activity
    - Assert: Verify 404 error response
    """
    # Arrange
    invalid_activity = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_remove_participant_not_found(client):
    """
    Test that removing nonexistent participant returns 404.
    
    AAA Pattern:
    - Arrange: Valid activity, but email not in participants
    - Act: Call DELETE with nonexistent email
    - Assert: Verify 404 error response
    """
    # Arrange
    activity_name = "Chess Club"
    nonexistent_email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{nonexistent_email}"
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Participant not found" in result["detail"]


def test_remove_participant_response_format(client):
    """
    Test that successful removal response has correct message format.
    
    AAA Pattern:
    - Arrange: Prepare activity and participant to remove
    - Act: Remove participant
    - Assert: Verify response message format is correct
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    expected_message_template = f"Removed {email} from {activity_name}"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    result = response.json()
    
    # Assert
    assert response.status_code == 200
    assert result["message"] == expected_message_template


def test_remove_then_re_signup(client):
    """
    Test that a participant can be removed and then sign up again.
    
    AAA Pattern:
    - Arrange: Get a participant from an activity
    - Act: Remove them, then sign them up again
    - Assert: Both operations succeed, participant list updated twice
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Get initial state
    activities_initial = client.get("/activities").json()
    initial_count = len(activities_initial[activity_name]["participants"])
    
    # Act - Remove participant
    response_remove = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Assert - Removal successful
    assert response_remove.status_code == 200
    activities_after_remove = client.get("/activities").json()
    assert len(activities_after_remove[activity_name]["participants"]) == initial_count - 1
    
    # Act - Sign up again
    response_signup = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert - Re-signup successful
    assert response_signup.status_code == 200
    activities_after_signup = client.get("/activities").json()
    assert len(activities_after_signup[activity_name]["participants"]) == initial_count
    assert email in activities_after_signup[activity_name]["participants"]
