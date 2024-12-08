import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.task import Task


@pytest.fixture(scope="module")
def test_client():
    """
    Configuración de una aplicación Flask para pruebas con base de datos temporal.
    """
    app = create_app("config.TestingConfig")  # Usa la configuración de prueba
    testing_client = app.test_client()

    # Pushea el contexto de la aplicación
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    # Elimina el contexto después de las pruebas
    ctx.pop()


@pytest.fixture(scope="module")
def init_database(test_client):
    """
    Configuración y limpieza de la base de datos para pruebas.
    """
    # Asegura el contexto de la aplicación
    with test_client.application.app_context():
        db.create_all()

        # Crear datos iniciales
        user = User(username="test_user")
        user.password = "password123"
        db.session.add(user)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()


def test_user_creation(init_database):
    """
    Prueba la creación de un usuario en la base de datos.
    """
    user = User.query.filter_by(username="test_user").first()
    assert user is not None
    assert user.username == "test_user"


def test_task_creation(init_database):
    """
    Prueba la creación de una tarea y su asociación con un usuario.
    """
    user = User.query.filter_by(username="test_user").first()
    task = Task(content="Test Task", user_id=user.id, priority="Medium")
    db.session.add(task)
    db.session.commit()

    task_in_db = Task.query.filter_by(content="Test Task").first()
    assert task_in_db is not None
    assert task_in_db.user_id == user.id
    assert task_in_db.priority == "Medium"


def test_cascade_delete(init_database):
    """
    Prueba que al eliminar un usuario, sus tareas asociadas también se eliminen.
    """
    user = User.query.filter_by(username="test_user").first()
    db.session.delete(user)
    db.session.commit()

    user_in_db = User.query.filter_by(username="test_user").first()
    tasks_in_db = Task.query.filter_by(user_id=user.id).all()

    assert user_in_db is None
    assert len(tasks_in_db) == 0
