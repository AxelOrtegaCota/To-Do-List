from flask import Blueprint, request, jsonify
from app.models.task import Task
from app.extensions import db

# Crear el blueprint
tasks = Blueprint("tasks", __name__)

# Ruta para obtener todas las tareas
@tasks.route("/", methods=["GET"])
def get_tasks():
    all_tasks = Task.query.all()
    tasks_list = [{"id": t.id, "content": t.content, "priority": t.priority} for t in all_tasks]
    return jsonify(tasks_list), 200

# Ruta para crear una nueva tarea
@tasks.route("/", methods=["POST"])
def create_task():
    data = request.get_json()
    content = data.get("content")
    priority = data.get("priority", "Medium")

    if not content:
        return jsonify({"error": "Task content is required"}), 400

    new_task = Task(content=content, priority=priority)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created", "task": {"id": new_task.id, "content": new_task.content, "priority": new_task.priority}}), 201

# Ruta para actualizar una tarea
@tasks.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.content = data.get("content", task.content)
    task.priority = data.get("priority", task.priority)
    db.session.commit()

    return jsonify({"message": "Task updated", "task": {"id": task.id, "content": task.content, "priority": task.priority}}), 200

# Ruta para eliminar una tarea
@tasks.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
