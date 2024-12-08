import pytest
from app.forms.forms import LoginForm, RegisterForm


def test_login_form_valid(test_app):
    """Prueba con datos válidos para LoginForm."""
    with test_app.test_request_context():  # Contexto de solicitud
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'securepassword'
        })
        assert form.validate()  # Debe pasar la validación


def test_login_form_invalid_username(test_app):
    """Prueba LoginForm con nombre de usuario vacío."""
    with test_app.test_request_context():  # Contexto de solicitud
        form = LoginForm(data={
            'username': '',
            'password': 'securepassword'
        })
        assert not form.validate()
        assert 'username' in form.errors  # Debe tener un error en el campo username


def test_login_form_invalid_password(test_app):
    """Prueba LoginForm con contraseña vacía."""
    with test_app.test_request_context():  # Contexto de solicitud
        form = LoginForm(data={
            'username': 'testuser',
            'password': ''
        })
        assert not form.validate()
        assert 'password' in form.errors  # Debe tener un error en el campo password


def test_register_form_valid(test_app):
    """Prueba con datos válidos para RegisterForm."""
    with test_app.test_request_context():  # Contexto de solicitud
        form = RegisterForm(data={
            'username': 'testuser',
            'password': 'securepassword',
            'confirm_password': 'securepassword'
        })
        assert form.validate()  # Debe pasar la validación


def test_register_form_invalid_password_mismatch(test_app):
    """Prueba RegisterForm con contraseñas que no coinciden."""
    with test_app.test_request_context():  # Contexto de solicitud
        form = RegisterForm(data={
            'username': 'testuser',
            'password': 'securepassword',
            'confirm_password': 'wrongpassword'
        })
        assert not form.validate()
        assert 'confirm_password' in form.errors  # Debe tener un error en el campo confirm_password


def test_register_form_invalid_short_password(test_app):
    """Prueba RegisterForm con una contraseña demasiado corta."""
    with test_app.test_request_context():  # Contexto de solicitud
        form = RegisterForm(data={
            'username': 'testuser',
            'password': '123',
            'confirm_password': '123'
        })
        assert not form.validate()
        assert 'password' in form.errors  # Debe tener un error en el campo password
