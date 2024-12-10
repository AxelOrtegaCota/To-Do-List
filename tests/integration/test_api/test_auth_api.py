import pytest
from flask import url_for


def test_register_user(test_client):
    """Test that a user can register successfully."""
    response = test_client.post(
        url_for('auth.register'),
        json={  # Cambia a JSON para probar la API REST
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "User testuser successfully registered"


def test_login_invalid_credentials(test_client):
    """Prueba que la API devuelva 401 para credenciales inválidas."""
    response = test_client.post(
        '/auth/login',
        json={'username': 'invaliduser', 'password': 'wrongpassword'}
    )
    assert response.status_code == 401  # Código de estado esperado
    assert response.get_json() == {'error': 'Invalid credentials'}  # Valida el mensaje


def test_login_missing_credentials(test_client):
    """Prueba que la API devuelva 400 cuando faltan credenciales."""
    response = test_client.post(
        '/auth/login',
        json={'username': ''}
    )
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Username and password are required'}


def test_logout_user(test_client):
    """Prueba para cerrar sesión."""
    with test_client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'testuser'

    response = test_client.post(url_for('auth.logout'))
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Successfully logged out'
