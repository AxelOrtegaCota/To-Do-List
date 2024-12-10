import pytest
import uuid
from app.models.user import User
from app import create_app
from app.extensions import db, oauth



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

@pytest.fixture
def authenticated_client(test_client):
    """Crea un cliente autenticado con un usuario único."""
    username = f"user_{uuid.uuid4().hex[:8]}"  # Genera un nombre único
    email = f"{username}@example.com"
    user = User(username=username, email=email, password="password123")
    db.session.add(user)
    db.session.commit()

    with test_client.session_transaction() as sess:
        sess["user_id"] = user.id

    return test_client, user


@pytest.fixture(scope="module", autouse=True)
def setup_oauth():
    """Configura el cliente OAuth para los tests."""
    oauth.register(
        name="google",
        client_id="test_client_id",
        client_secret="test_client_secret",
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        client_kwargs={"scope": "openid email profile"},
    )

