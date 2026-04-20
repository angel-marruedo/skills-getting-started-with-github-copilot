"""
Tests for POST /activities/{activity_name}/signup endpoint
Follows AAA (Arrange-Act-Assert) pattern
"""
import pytest


def test_signup_success(client, sample_email):
    """
    Test successful signup for a new participant.
    
    AAA Pattern:
    - Arrange: Prepare activity name and new email
    - Act: Call POST signup endpoint
    - Assert: Verify response success and participant is added
    """
    # Arrange
    activity_name = "Programming Class"
    new_email = sample_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert new_email in result["message"]
    assert activity_name in result["message"]


def test_signup_adds_participant_to_activity(client, sample_email):
    """
    Test that signup actually adds the participant to the activity's participant list.
    
    AAA Pattern:
    - Arrange: Get initial participant count
    - Act: Sign up a new participant
    - Assert: Verify participant count increased and email is in list
    """
    # Arrange
    activity_name = "Programming Class"
    new_email = sample_email
    
    # Get initial state
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify participant was added
    activities_after = client.get("/activities").json()
    final_count = len(activities_after[activity_name]["participants"])
    assert final_count == initial_count + 1
    assert new_email in activities_after[activity_name]["participants"]


def test_signup_activity_not_found(client, sample_email):
    """
    Test signup fails with 404 when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: Prepare non-existent activity name
    - Act: Call POST signup with invalid activity
    - Assert: Verify 404 error response
    """
    # Arrange
    invalid_activity = "Nonexistent Activity"
    email = sample_email
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "Activity not found"


def test_signup_duplicate_participant_rejected(client, sample_email):
    """
    Test signup fails with 400 when participant already registered.
    
    AAA Pattern:
    - Arrange: Choose activity with existing participant
    - Act: Try to sign up the same participant twice
    - Assert: Verify 400 error on second signup attempt
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]


def test_signup_new_participant_then_duplicate(client, sample_email):
    """
    Test that attempting duplicate signup after first signup fails.
    
    AAA Pattern:
    - Arrange: Prepare email that's not yet registered
    - Act: Sign up participant, then try to sign up again
    - Assert: First succeeds, second fails with 400
    """
    # Arrange
    activity_name = "Programming Class"
    new_email = sample_email
    
    # Act - First signup
    response_first = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert - First signup succeeds
    assert response_first.status_code == 200
    
    # Act - Duplicate signup attempt
    response_second = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert - Second signup fails
    assert response_second.status_code == 400
    result = response_second.json()
    assert "already signed up" in result["detail"]


def test_signup_response_format(client, sample_email):
    """
    Test that successful signup response has correct message format.
    
    AAA Pattern:
    - Arrange: Prepare activity and email
    - Act: Sign up participant
    - Assert: Verify response message format is correct
    """
    # Arrange
    activity_name = "Gym Class"
    new_email = sample_email
    expected_message_template = f"Signed up {new_email} for {activity_name}"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    result = response.json()
    
    # Assert
    assert response.status_code == 200
    assert result["message"] == expected_message_template
