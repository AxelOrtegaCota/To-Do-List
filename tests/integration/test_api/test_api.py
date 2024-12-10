from flask import url_for

def test_google_login_redirect(test_client):
    """Test that the login route redirects correctly to Google."""
    response = test_client.get(url_for("oauth.login"), follow_redirects=False)
    assert response.status_code == 302
    assert "accounts.google.com" in response.headers["Location"]


def test_google_callback_no_token(test_client):
    """Test that the callback handles the absence of a token correctly."""
    with test_client.session_transaction() as session:
        session["oauth_state"] = "test_state"  # Mocking session state

    response = test_client.get(
        url_for("oauth.callback"),
        query_string={"state": "test_state"},  # No token (`code`) provided
        follow_redirects=True
    )

    # Check for 400 status and specific error message
    assert response.status_code == 400
    assert b'{"error":"Invalid or missing token"}' in response.data
