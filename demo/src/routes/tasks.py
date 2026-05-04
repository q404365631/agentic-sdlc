"""Task CRUD routes."""

from flask import Blueprint, request, jsonify
from models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("", methods=["GET"])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([{
        "id": t.id, "title": t.title, "status": t.status,
        "due_date": t.due_date.isoformat() if t.due_date else None,
        "assignee_id": t.assignee_id, "creator_id": t.creator_id
    } for t in tasks])


@tasks_bp.route("", methods=["POST"])
def create_task():
    data = request.get_json()
    task = Task(
        title=data["title"],
        description=data.get("description"),
        status=data.get("status", "Todo"),
        creator_id=data["creator_id"],
        assignee_id=data.get("assignee_id"),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "message": "Task created"}), 201


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    task.assignee_id = data.get("assignee_id", task.assignee_id)
    db.session.commit()
    return jsonify({"message": "Task updated"})


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = "Deleted"
    db.session.commit()
    return jsonify({"message": "Task deleted"})
