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
    """Prueba que la API devuelva 401 para credenciales inválidas."""
    response = test_client.post(
        '/auth/login',
        json={'username': 'invaliduser', 'password': 'wrongpassword'}
    )
    assert response.status_code == 401  # Código de estado esperado
    assert response.get_json() == {'error': 'Credenciales inválidas'}  # Valida el mensaje

def test_login_missing_credentials(test_client):
    """Prueba que la API devuelva 400 cuando faltan credenciales."""
    response = test_client.post(
        '/auth/login',
        json={'username': ''}
    )
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Se requiere usuario y contraseña'}


def test_logout_user(test_client):
    """Prueba para cerrar sesión."""
    with test_client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'testuser'

    response = test_client.post(url_for('auth.logout'))
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Sesión cerrada correctamente'
