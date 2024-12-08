import pytest
from flask import url_for
from app.models.user import User
from app.extensions import db


def test_register_user(test_client, init_database):
    """Prueba para registrar un nuevo usuario."""
    response = test_client.post(
        url_for('auth.register'),
        json={
            'username': 'testuser',
            'password': 'securepassword'
        }
    )
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Usuario testuser registrado exitosamente'

def test_login_invalid_credentials(test_client):
    """Prueba para iniciar sesión con credenciales inválidas."""
    response = test_client.post(
        url_for('auth.login'),
        json={
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }
    )
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Usuario o contraseña incorrectos'


def test_logout_user(test_client):
    """Prueba para cerrar sesión."""
    with test_client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'testuser'

    response = test_client.post(url_for('auth.logout'))
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Sesión cerrada correctamente'
