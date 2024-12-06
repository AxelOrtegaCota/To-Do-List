import pytest
from app import create_app
from app.extensions import db

@pytest.fixture(scope='module')
def test_app():
    """Fixture para configurar la aplicación Flask en modo de prueba."""
    app = create_app('config.TestingConfig')  # Usa TestingConfig explícitamente
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def test_client(test_app):
    """Fixture para crear un cliente de prueba."""
    return test_app.test_client()

@pytest.fixture(scope='function')
def init_database(test_app):
    """Fixture para inicializar la base de datos para pruebas."""
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
