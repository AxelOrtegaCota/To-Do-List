from flask import Blueprint, render_template, request, redirect, url_for
from app.models.task import Task
from app.extensions import db

# Crear el blueprint
tasks_bp = Blueprint("tasks", __name__)

# Ruta para obtener y mostrar todas las tareas (GET) y crear nuevas (POST)
@tasks_bp.route("/", methods=["GET", "POST"])
def todo_list():
    if request.method == "POST":
        # Crear una nueva tarea desde el formulario
        content = request.form.get("task_content")
        priority = request.form.get("task_priority", "Medium")

        if content:
            new_task = Task(content=content, priority=priority)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for("tasks.todo_list"))

    # Obtener todas las tareas
    tasks = Task.query.all()
    return render_template("base.html", tasks=tasks)

# Ruta para actualizar una tarea
@tasks_bp.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect(url_for("tasks.todo_list"))  # Verifica que la tarea existe

    # Actualizar contenido y prioridad
    task.content = request.form.get("new_content", task.content)
    task.priority = request.form.get("new_priority", task.priority)
    db.session.commit()

    return redirect(url_for("tasks.todo_list"))

# Ruta para eliminar una tarea
@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect(url_for("tasks.todo_list"))  # Verifica que la tarea existe

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks.todo_list"))
