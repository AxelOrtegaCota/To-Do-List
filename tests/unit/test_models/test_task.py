import pytest
from app.models.task import Task
from app.extensions import db

def test_task_creation(init_database):
    """Prueba crear una tarea válida."""
    task = Task(content="Test Task", priority="High", completed=True)
    db.session.add(task)
    db.session.commit()

    assert task.id is not None
    assert task.content == "Test Task"
    assert task.priority == "High"
    assert task.completed is True

def test_task_default_values(init_database):
    """Prueba los valores predeterminados de prioridad y completado."""
    task = Task(content="Test Task")
    db.session.add(task)
    db.session.commit()

    assert task.priority == "Medium"  # Valor por defecto
    assert task.completed is False    # Valor por defecto

def test_task_missing_content(init_database):
    """Prueba que no se pueda crear una tarea sin contenido."""
    with pytest.raises(Exception):  # SQLAlchemy lanza una excepción
        task = Task(priority="Low")
        db.session.add(task)
        db.session.commit()

def test_task_repr(init_database):
    """Prueba la representación (__repr__) del modelo Task."""
    task = Task(content="Test Task", priority="High", completed=True)
    db.session.add(task)
    db.session.commit()

    assert repr(task) == "<Task Test Task (Priority: High, Completed: True)>"
