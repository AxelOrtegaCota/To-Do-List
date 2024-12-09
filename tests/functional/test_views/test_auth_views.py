import pytest
import uuid
from flask import url_for
from app.models.user import User
from app.extensions import db


def test_register_view(test_client):
    """Prueba que la vista de registro se renderiza correctamente."""
    response = test_client.get(url_for("auth.register"))
    assert response.status_code == 200
    assert b"Register" in response.data  # Valida contenido en la página


def test_register_user(test_client, init_database):
    """Prueba que un usuario se registre correctamente."""
    response = test_client.post(
        url_for("auth.register"),
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True
    )
    assert response.status_code == 200
    user = User.query.filter_by(username="testuser").first()
    assert user is not None


def test_login_view(test_client):
    """Prueba que la vista de inicio de sesión se renderiza correctamente."""
    response = test_client.get(url_for("auth.login"))
    assert response.status_code == 200
    assert 'Login'.encode('utf-8') in response.data


def test_login_user(test_client, init_database):
    """Prueba que un usuario pueda iniciar sesión con credenciales válidas."""
    unique_username = f"user_{uuid.uuid4().hex[:8]}"  # Genera un nombre único
    user = User(username=unique_username, password="password123")
    db.session.add(user)
    db.session.commit()

    response = test_client.post(
        url_for("auth.login"),
        data={"username": unique_username, "password": "password123"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert f"Welcome, {unique_username}".encode() in response.data


def test_login_invalid_user(test_client):
    """Prueba que un usuario no pueda iniciar sesión con credenciales inválidas."""
    response = test_client.post(
        url_for("auth.login"),
        data={"username": "invaliduser", "password": "wrongpassword"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Credenciales inválidas'.encode('utf-8') in response.data


def test_logout(test_client, init_database):
    """Prueba que un usuario pueda cerrar sesión correctamente."""
    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    user = User(username=unique_username, password="password123")
    db.session.add(user)
    db.session.commit()

    with test_client.session_transaction() as sess:
        sess["user_id"] = user.id

    response = test_client.get(url_for("auth.logout"), follow_redirects=True)
    assert response.status_code == 200
    assert 'Login'.encode('utf-8') in response.data