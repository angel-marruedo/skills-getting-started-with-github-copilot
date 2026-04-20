"""
Tests for GET / (root) endpoint
Follows AAA (Arrange-Act-Assert) pattern
"""
import pytest


def test_root_redirects_to_index_html(client):
    """
    Test that GET / redirects to /static/index.html.
    
    AAA Pattern:
    - Arrange: Prepare TestClient
    - Act: Call GET / with follow_redirects=True
    - Assert: Verify redirect occurs (status 200 after following redirect)
    """
    # Arrange
    # (No setup needed, just use the client)
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
    # The response will be the served static file (index.html)
    assert "text/html" in response.headers.get("content-type", "")


def test_root_redirect_location(client):
    """
    Test that GET / returns redirect response with correct location header.
    
    AAA Pattern:
    - Arrange: Prepare TestClient without following redirects
    - Act: Call GET / and check the redirect response
    - Assert: Verify 307 redirect status and correct location header
    """
    # Arrange
    # (No setup needed, just use the client)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"
