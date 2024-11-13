# tests/integration/test_api/test_auth_api.py
import pytest

def test_login(test_client, init_db):
    response = test_client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200  # OK
    assert b'Welcome testuser' in response.data

def test_failed_login(test_client, init_db):
    response = test_client.post('/auth/login', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401  # Unauthorized
