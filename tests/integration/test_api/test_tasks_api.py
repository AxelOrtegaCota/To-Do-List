# tests/integration/test_api/test_tasks_api.py
import pytest
from app.models import Task

def test_create_task(test_client, auth, init_db):
    response = test_client.post('/tasks/create', data={
        'title': 'Test Task',
        'description': 'A test task description'
    })
    assert response.status_code == 201  # Created
    assert b'Test Task' in response.data

def test_get_task(test_client, auth, init_db):
    task = Task.query.first()
    response = test_client.get(f'/tasks/{task.id}')
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_update_task(test_client, auth, init_db):
    task = Task.query.first()
    response = test_client.post(f'/tasks/{task.id}/edit', data={
        'title': 'Updated Task',
        'description': 'Updated description'
    })
    assert response.status_code == 200
    assert b'Updated Task' in response.data

def test_delete_task(test_client, auth, init_db):
    task = Task.query.first()
    response = test_client.delete(f'/tasks/{task.id}')
    assert response.status_code == 200
    assert Task.query.get(task.id) is None
