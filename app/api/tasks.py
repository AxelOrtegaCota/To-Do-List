from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from app.models.task import Task
from app.extensions import db

# Crear los blueprints
tasks_bp = Blueprint("tasks", __name__)  # Para las rutas normales
tasks_api_bp = Blueprint("tasks_api", __name__, url_prefix='/api/tasks')  # Para las rutas API

# Rutas normales
@tasks_bp.route("/", methods=["GET", "POST"])
def todo_list():
    # Verifica si el usuario está autenticado
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        content = request.form.get("task_content")
        priority = request.form.get("task_priority", "Medium")

        if content:
            new_task = Task(content=content, priority=priority, user_id=user_id)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for("tasks.todo_list"))

    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template("base.html", tasks=tasks)

@tasks_bp.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    # Verifica si el usuario está autenticado
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return redirect(url_for("tasks.todo_list"))

    task.content = request.form.get("new_content", task.content)
    task.priority = request.form.get("new_priority", task.priority)
    db.session.commit()
    return redirect(url_for("tasks.todo_list"))

@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    # Verifica si el usuario está autenticado
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return redirect(url_for("tasks.todo_list"))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks.todo_list"))

# Rutas API
@tasks_api_bp.route("/", methods=["GET"])
def get_tasks():
    # Verifica si el usuario está autenticado
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    tasks = Task.query.filter_by(user_id=user_id).all()
    tasks_list = [{"id": t.id, "content": t.content, "priority": t.priority, "completed": t.completed} for t in tasks]
    return jsonify(tasks_list), 200

@tasks_api_bp.route("/", methods=["POST"])
def create_task():
    # Verifica si el usuario está autenticado
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    data = request.get_json()
    content = data.get("content")
    priority = data.get("priority", "Medium")

    if not content:
        return jsonify({"error": "Task content is required"}), 400

    new_task = Task(content=content, priority=priority, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created", "task": {"id": new_task.id, "content": new_task.content, "priority": new_task.priority}}), 201

@tasks_api_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    # Verifica si el usuario está autenticado
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.content = data.get("content", task.content)
    task.priority = data.get("priority", task.priority)
    db.session.commit()

    return jsonify({"message": "Task updated", "task": {"id": task.id, "content": task.content, "priority": task.priority}}), 200

@tasks_api_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    # Verifica si el usuario está autenticado
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
