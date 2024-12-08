import pytest
from app.models.task import Task
from app.extensions import db


def test_get_tasks_api_empty(test_client):
    """Prueba obtener todas las tareas vía API cuando no hay tareas."""
    response = test_client.get('/api/tasks/')
    assert response.status_code == 200
    assert response.get_json() == []  # La lista debe estar vacía


from app.models.task import Task


def test_get_tasks_api_with_data(test_client, init_database):
    """Prueba obtener todas las tareas vía API con datos existentes."""
    # Crear tareas en la base de datos
    task1 = Task(content="API Task 1", priority="High")
    task2 = Task(content="API Task 2", priority="Low")
    init_database.session.add_all([task1, task2])
    init_database.session.commit()

    response = test_client.get('/api/tasks/')
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 2  # Verifica que se devuelven las 2 tareas
    assert tasks[0]['content'] == "API Task 1"
    assert tasks[1]['priority'] == "Low"


def test_update_task_api(test_client, init_database):
    """Prueba actualizar una tarea existente vía API."""
    task = Task(content="Old API Task", priority="Medium")
    init_database.session.add(task)
    init_database.session.commit()

    response = test_client.put(
        f'/api/tasks/{task.id}',
        json={'content': 'Updated API Task', 'priority': 'High'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Task updated'
    assert data['task']['content'] == 'Updated API Task'
    assert data['task']['priority'] == 'High'


def test_delete_task_api(test_client, init_database):
    """Prueba eliminar una tarea existente vía API."""
    task = Task(content="Task to Delete API", priority="Low")
    init_database.session.add(task)
    init_database.session.commit()

    response = test_client.delete(f'/api/tasks/{task.id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Task deleted'


def test_create_task_api(test_client):
    """Prueba crear una tarea vía API con datos válidos."""
    response = test_client.post(
        '/api/tasks/',
        json={'content': 'New API Task', 'priority': 'Medium'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Task created'
    assert data['task']['content'] == 'New API Task'
    assert data['task']['priority'] == 'Medium'


def test_create_task_api_missing_content(test_client):
    """Prueba crear una tarea vía API sin contenido (debe devolver error)."""
    response = test_client.post('/api/tasks/', json={'priority': 'High'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Task content is required'


def test_update_task_api(test_client, init_database):
    """Prueba actualizar una tarea existente vía API."""
    # Crear tarea de prueba
    task = Task(content="Old API Task", priority="Medium")
    init_database.session.add(task)
    init_database.session.commit()

    response = test_client.put(
        f'/api/tasks/{task.id}',
        json={'content': 'Updated API Task', 'priority': 'High'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Task updated'
    assert data['task']['content'] == 'Updated API Task'
    assert data['task']['priority'] == 'High'


def test_update_task_api_not_found(test_client):
    """Prueba actualizar una tarea inexistente vía API."""
    response = test_client.put('/api/tasks/9999', json={'content': 'Nonexistent Task'})
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Task not found'


def test_delete_task_api(test_client, init_database):
    """Prueba eliminar una tarea existente vía API."""
    task = Task(content="Task to Delete API", priority="Low")
    init_database.session.add(task)
    init_database.session.commit()

    response = test_client.delete(f'/api/tasks/{task.id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Task deleted'


def test_delete_task_api_not_found(test_client):
    """Prueba eliminar una tarea inexistente vía API."""
    response = test_client.delete('/api/tasks/9999')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Task not found'
