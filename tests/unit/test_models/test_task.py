from app.models.task import Task

def test_task_creation(init_database):
    """Prueba para la creación de tareas."""
    task = Task(content="Test Task", priority="Medium")
    assert task.content == "Test Task"
    assert task.priority == "Medium"
