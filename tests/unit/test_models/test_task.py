# tests/unit/test_models/test_task.py
import pytest
from app.models import Task

def test_task_creation(init_db):
    task = Task.query.first()
    assert task.title == 'Test Task'
    assert task.description == 'A test task description'
