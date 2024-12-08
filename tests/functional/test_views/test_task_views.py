import pytest
import uuid
from flask import url_for
from app.models.user import User
from app.models.task import Task
from app.extensions import db


@pytest.fixture
def authenticated_client(test_client):
    """Crea un cliente autenticado con un usuario único."""
    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    user = User(username=unique_username, password="password123")
    db.session.add(user)
    db.session.commit()

    with test_client.session_transaction() as sess:
        sess["user_id"] = user.id

    return test_client, user


def test_task_view(authenticated_client):
    """Prueba que la vista de tareas se renderice correctamente."""
    client, user = authenticated_client
    response = client.get(url_for("tasks.todo_list"))
    assert response.status_code == 200
    assert b"To-Do List" in response.data


def test_create_task(authenticated_client):
    """Prueba que un usuario pueda crear una tarea desde la vista."""
    client, user = authenticated_client
    response = client.post(
        url_for("tasks.todo_list"),
        data={"task_content": "New Task", "task_priority": "High"},
        follow_redirects=True
    )
    assert response.status_code == 200
    task = Task.query.filter_by(content="New Task", user_id=user.id).first()
    assert task is not None
    assert task.priority == "High"


def test_edit_task(authenticated_client, init_database):
    """Prueba que un usuario pueda editar una tarea desde la vista."""
    client, user = authenticated_client
    task = Task(content="Old Task", priority="Medium", user_id=user.id)
    db.session.add(task)
    db.session.commit()

    response = client.post(
        url_for("tasks.edit_task", task_id=task.id),
        data={"new_content": "Updated Task", "new_priority": "High"},
        follow_redirects=True
    )
    assert response.status_code == 200
    updated_task = db.session.get(Task, task.id)
    assert updated_task.content == "Updated Task"
    assert updated_task.priority == "High"


def test_delete_task(authenticated_client, init_database):
    """Prueba que un usuario pueda eliminar una tarea desde la vista."""
    client, user = authenticated_client
    task = Task(content="Task to Delete", priority="Low", user_id=user.id)
    db.session.add(task)
    db.session.commit()

    response = client.post(
        url_for("tasks.delete_task", task_id=task.id),
        follow_redirects=True
    )
    assert response.status_code == 200
    deleted_task = db.session.get(Task, task.id)
    assert deleted_task is None
