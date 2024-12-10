import pytest
from app.models.task import Task
from app.models.user import User
from app.extensions import db
import uuid


@pytest.fixture
def create_user(init_database):
    """Crea un usuario único para asociar tareas."""
    username = f"user_{uuid.uuid4().hex[:8]}"  # Genera un nombre único
    user = User(username=username, password="password123")
    db.session.add(user)
    db.session.commit()
    return user


def test_task_creation(init_database, create_user):
    """Prueba crear una tarea válida."""
    user = create_user
    task = Task(content="Test Task", priority="High", completed=True, user_id=user.id)
    db.session.add(task)
    db.session.commit()

    assert task.id is not None
    assert task.content == "Test Task"
    assert task.priority == "High"
    assert task.completed is True


def test_task_default_values(init_database, create_user):
    """Prueba los valores predeterminados de prioridad y completado."""
    user = create_user
    task = Task(content="Test Task", user_id=user.id)
    db.session.add(task)
    db.session.commit()

    assert task.priority == "Medium"  # Valor por defecto
    assert task.completed is False    # Valor por defecto


def test_task_missing_content(init_database, create_user):
    """Prueba que no se pueda crear una tarea sin contenido."""
    user = create_user
    with pytest.raises(Exception):  # SQLAlchemy lanza una excepción
        task = Task(priority="Low", user_id=user.id)
        db.session.add(task)
        db.session.commit()


def test_task_repr(init_database, create_user):
    """Prueba la representación (__repr__) del modelo Task."""
    user = create_user
    task = Task(content="Test Task", priority="High", completed=True, user_id=user.id)
    db.session.add(task)
    db.session.commit()

    assert repr(task) == "<Task Test Task (Priority: High, Completed: True)>"
