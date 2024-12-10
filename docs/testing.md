# Project Struture

- app/: Main application logic.
- tests/: Contains all test cases.
- docs/: Documentation for the project.

## Running Tests
1. Ensure all dependencies are installed.
2. Run the tests using:
   ```bash
   pytest


## Coverage Report
1. Generate a coverage report:
    pytest --cov=app

2. View the coverage report:
    pytest --cov=app --cov-report=html


## Example Tests


## Unit Test Example
def test_user_creation(init_database):
    """Prueba para la creación de usuarios."""
    user = User(username="testuser")
    user.password = "plaintextpassword"
    assert user.username == "testuser"
    assert user._password != "plaintextpassword"


## Integration Test Example
def test_task_creation(init_database):
    """Prueba la creación de una tarea y su asociación con un usuario."""
    user = User.query.filter_by(username="test_user").first()
    task = Task(content="Test Task", user_id=user.id, priority="Medium")
    db.session.add(task)
    db.session.commit()
    task_in_db = Task.query.filter_by(content="Test Task").first()
    assert task_in_db is not None
    assert task_in_db.user_id == user.id
    assert task_in_db.priority == "Medium"


## Functional Test Example
def test_register_view(test_client):
    """Prueba que la vista de registro se renderiza correctamente."""
    response = test_client.get(url_for("auth.register"))
    assert response.status_code == 200
    assert b"Register" in response.data


## GitHub Actions Workflow


### Explanation of the Workflow
1. **Trigger on Push:**
   - The workflow is triggered on every `push` to the `main` branch.

2. **Set up Python:**
   - Specifies the Python version (`3.10`) to be used in the CI environment.

3. **Install Dependencies:**
   - Installs the project's dependencies as specified in `requirements.txt`.

4. **Run Tests:**
   - Executes `pytest` with coverage to ensure all tests pass and generate a code coverage report.


