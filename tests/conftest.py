import pytest
from app import create_app
from app.extensions import db


@pytest.fixture(scope='module')
def test_app():
    """Crea una instancia de la aplicación Flask en modo de prueba."""
    app = create_app('config.TestingConfig')  # Configuración de pruebas
    with app.app_context():
        db.create_all()  # Crea las tablas antes de las pruebas
        yield app
        db.session.remove()  # Limpia la sesión de la base de datos
        db.drop_all()  # Elimina las tablas después de las pruebas


@pytest.fixture(scope='function')
def test_client(test_app):
    """Crea un cliente de prueba con contexto de aplicación."""
    with test_app.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def init_database(test_app):
    """Inicializa la base de datos para cada prueba con un contexto de aplicación."""
    with test_app.app_context():  # Asegura que las pruebas usen un contexto de aplicación
        try:
            yield db
        finally:
            db.session.rollback()  # Revierte cualquier cambio
            db.session.remove()  # Limpia la sesión

