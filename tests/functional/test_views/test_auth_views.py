'''# tests/functional/test_views/test_auth_views.py
import pytest

def test_login_form_validation(test_client):
    response = test_client.post('/auth/login', data={})
    assert b'This field is required.' in response.data
'''