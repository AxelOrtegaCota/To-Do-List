import pytest
from flask import url_for
from app.models.user import User

def test_register_user(test_client, init_database):
    """Prueba para registrar un nuevo usuario."""
    response = test_client.post(
        '/auth/register',  # Ruta absoluta
        json={
            'username': 'testuser',
            'password': 'securepassword'
        }
    )
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Usuario testuser registrado exitosamente'

def test_register_existing_user(test_client, init_database):
    """Prueba para registrar un usuario existente."""
    # Crea un usuario directamente en la base de datos
    user = User(username='testuser')
    user.password = 'securepassword'
    init_database.session.add(user)
    init_database.session.commit()

    response = test_client.post(
        '/auth/register',  # Ruta absoluta
        json={
            'username': 'testuser',
            'password': 'securepassword'
        }
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == 'El usuario ya existe'

def test_login_user(test_client, init_database):
    """Prueba para iniciar sesión con un usuario existente."""
    # Crea un usuario directamente en la base de datos
    user = User(username='testuser')
    user.password = 'securepassword'
    init_database.session.add(user)
    init_database.session.commit()

    response = test_client.post(
        '/auth/login',  # Ruta absoluta
        json={
            'username': 'testuser',
            'password': 'securepassword'
        }
    )
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Bienvenido testuser'

def test_login_invalid_credentials(test_client, init_database):
    """Prueba para iniciar sesión con credenciales inválidas."""
    response = test_client.post(
        '/auth/login',  # Ruta absoluta
        json={
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }
    )
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Usuario o contraseña incorrectos'

def test_logout_user(test_client):
    """Prueba para cerrar sesión."""
    # Simula que el usuario está autenticado
    with test_client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'testuser'

    response = test_client.post('/auth/logout')  # Ruta absoluta
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Sesión cerrada correctamente'
