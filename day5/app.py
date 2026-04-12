from datetime import datetime
from flask import Flask, jsonify, request # type: ignore

from database import initialize_database
from task_service import TaskService

app = Flask(__name__)
task_service = TaskService()

VALID_STATUSES = {"pending", "in_progress", "completed"}
VALID_PRIORITIES = {"low", "medium", "high"}


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_task_payload(data):
    required_fields = ["title", "description", "status", "priority", "due_date"]

    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"

    title = str(data["title"]).strip()
    description = str(data["description"]).strip()
    status = str(data["status"]).strip().lower()
    priority = str(data["priority"]).strip().lower()
    due_date = str(data["due_date"]).strip()

    if not title:
        return "Title cannot be empty."

    if not description:
        return "Description cannot be empty."

    if status not in VALID_STATUSES:
        return "Status must be one of: pending, in_progress, completed."

    if priority not in VALID_PRIORITIES:
        return "Priority must be one of: low, medium, high."

    if not validate_date(due_date):
        return "Due date must be in YYYY-MM-DD format."

    return None


def validate_status_payload(data):
    if "status" not in data:
        return "Missing required field: status"

    status = str(data["status"]).strip().lower()

    if status not in VALID_STATUSES:
        return "Status must be one of: pending, in_progress, completed."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Task Manager API is running",
        "endpoints": [
            "GET /tasks",
            "GET /tasks/<id>",
            "POST /tasks",
            "PUT /tasks/<id>",
            "PATCH /tasks/<id>/status",
            "DELETE /tasks/<id>",
            "GET /tasks?status=pending",
            "GET /tasks?priority=high",
            "GET /tasks/summary",
            "GET /tasks/overdue"
        ]
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    priority = request.args.get("priority")

    if status:
        status = status.strip().lower()
        if status not in VALID_STATUSES:
            return jsonify({"error": "Invalid status filter."}), 400

    if priority:
        priority = priority.strip().lower()
        if priority not in VALID_PRIORITIES:
            return jsonify({"error": "Invalid priority filter."}), 400

    tasks = task_service.get_all_tasks(status=status, priority=priority)
    return jsonify(tasks), 200


@app.route("/tasks/summary", methods=["GET"])
def get_summary():
    summary = task_service.get_summary()
    return jsonify(summary), 200


@app.route("/tasks/overdue", methods=["GET"])
def get_overdue_tasks():
    tasks = task_service.get_overdue_tasks()
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_service.get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found."}), 404

    return jsonify(task), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_task_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    new_task = task_service.create_task(
        title=data["title"].strip(),
        description=data["description"].strip(),
        status=data["status"].strip().lower(),
        priority=data["priority"].strip().lower(),
        due_date=data["due_date"].strip()
    )

    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_task_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    updated_task = task_service.update_task(
        task_id=task_id,
        title=data["title"].strip(),
        description=data["description"].strip(),
        status=data["status"].strip().lower(),
        priority=data["priority"].strip().lower(),
        due_date=data["due_date"].strip()
    )

    if not updated_task:
        return jsonify({"error": "Task not found."}), 404

    return jsonify(updated_task), 200


@app.route("/tasks/<int:task_id>/status", methods=["PATCH"])
def update_task_status(task_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_status_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    updated_task = task_service.update_task_status(
        task_id=task_id,
        status=data["status"].strip().lower()
    )

    if not updated_task:
        return jsonify({"error": "Task not found."}), 404

    return jsonify(updated_task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = task_service.delete_task(task_id)

    if not deleted:
        return jsonify({"error": "Task not found."}), 404

    return jsonify({"message": "Task deleted successfully."}), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)