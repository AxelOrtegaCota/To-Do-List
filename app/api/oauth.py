from flask import Blueprint, redirect, url_for, session, jsonify, request
from app.extensions import oauth

oauth_bp = Blueprint('oauth', __name__)

@oauth_bp.route('/login')
def login():
    """Route for Google login."""
    session['oauth_state'] = 'test_state'  # Mock state for testing
    return oauth.google.authorize_redirect(url_for('oauth.callback', _external=True))

@oauth_bp.route('/callback')
def callback():
    """Handles the OAuth callback."""
    # Check if state is present and matches
    expected_state = session.pop('oauth_state', None)
    request_state = request.args.get('state')

    if not expected_state or expected_state != request_state:
        return jsonify({'error': 'Invalid or missing state'}), 400

    # Check if the token is present
    token = request.args.get('code')
    if not token:
        return jsonify({'error': 'Invalid or missing token'}), 400

    # Simulate a successful login
    return redirect(url_for('tasks.todo_list'))
