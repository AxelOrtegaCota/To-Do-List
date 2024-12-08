import pytest
import uuid
from app.models.task import Task
from app.models.user import User
from app.extensions import db


@pytest.fixture
def authenticated_client(test_client):
    """Crea un cliente autenticado con un usuario de prueba único."""
    username = f"user_{uuid.uuid4().hex[:8]}"  # Genera un nombre único
    user = User(username=username, password="password123")
    db.session.add(user)
    db.session.commit()

    # Establece user_id en la sesión
    with test_client.session_transaction() as session:
        session["user_id"] = user.id

    return test_client, user


def test_get_tasks_api_empty(authenticated_client):
    """Prueba obtener todas las tareas vía API cuando no hay tareas."""
    client, _ = authenticated_client
    response = client.get('/api/tasks/')
    assert response.status_code == 200
    assert response.get_json() == []  # La lista debe estar vacía


def test_get_tasks_api_with_data(authenticated_client, init_database):
    """Prueba obtener todas las tareas vía API con datos existentes."""
    client, user = authenticated_client

    # Crear tareas en la base de datos
    task1 = Task(content="API Task 1", priority="High", user_id=user.id)
    task2 = Task(content="API Task 2", priority="Low", user_id=user.id)
    db.session.add_all([task1, task2])
    db.session.commit()

    response = client.get('/api/tasks/')
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 2  # Verifica que se devuelven las 2 tareas
    assert tasks[0]['content'] == "API Task 1"
    assert tasks[1]['priority'] == "Low"


def test_create_task_api(authenticated_client):
    """Prueba crear una tarea vía API con datos válidos."""
    client, user = authenticated_client
    response = client.post(
        '/api/tasks/',
        json={'content': 'New API Task', 'priority': 'Medium'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Task created'
    assert data['task']['content'] == 'New API Task'
    assert data['task']['priority'] == 'Medium'
    assert data['task']['id'] is not None


def test_update_task_api(authenticated_client, init_database):
    """Prueba actualizar una tarea existente vía API."""
    client, user = authenticated_client

    # Crear tarea de prueba
    task = Task(content="Old API Task", priority="Medium", user_id=user.id)
    db.session.add(task)
    db.session.commit()

    response = client.put(
        f'/api/tasks/{task.id}',
        json={'content': 'Updated API Task', 'priority': 'High'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Task updated'
    assert data['task']['content'] == 'Updated API Task'
    assert data['task']['priority'] == 'High'


def test_delete_task_api(authenticated_client, init_database):
    """Prueba eliminar una tarea existente vía API."""
    client, user = authenticated_client

    task = Task(content="Task to Delete API", priority="Low", user_id=user.id)
    db.session.add(task)
    db.session.commit()

    response = client.delete(f'/api/tasks/{task.id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Task deleted'
