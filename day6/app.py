import secrets
from datetime import datetime
from flask import Flask, jsonify, request

from auth import require_auth
from database import initialize_database
from task_service import TaskService
from user_service import UserService

app = Flask(__name__)
task_service = TaskService()
user_service = UserService()

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


def validate_user_payload(data):
    required_fields = ["username", "password"]

    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"

    username = str(data["username"]).strip()
    password = str(data["password"]).strip()

    if not username:
        return "Username cannot be empty."

    if not password:
        return "Password cannot be empty."

    if len(username) < 3:
        return "Username must be at least 3 characters long."

    if len(password) < 4:
        return "Password must be at least 4 characters long."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Task Manager API with Basic Authentication is running",
        "public_endpoints": [
            "POST /register",
            "POST /login"
        ],
        "protected_endpoints": [
            "POST /logout",
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


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_user_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    existing_user = user_service.get_user_by_username(data["username"].strip())
    if existing_user:
        return jsonify({"error": "Username already exists."}), 409

    user = user_service.create_user(
        username=data["username"].strip(),
        password=data["password"].strip()
    )

    if not user:
        return jsonify({"error": "Unable to create user."}), 500

    return jsonify({
        "message": "User registered successfully.",
        "user": {
            "id": user["id"],
            "username": user["username"]
        }
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_user_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    user = user_service.get_user_by_username(data["username"].strip())
    if not user or user["password"] != data["password"].strip():
        return jsonify({"error": "Invalid username or password."}), 401

    token = secrets.token_hex(16)
    user_service.update_user_token(user["id"], token)

    return jsonify({
        "message": "Login successful.",
        "token": token
    }), 200


@app.route("/logout", methods=["POST"])
@require_auth
def logout():
    current_user = request.current_user

    user_service.clear_user_token(current_user["id"])

    return jsonify({
        "message": "Logout successful. Token invalidated."
    }), 200


@app.route("/tasks", methods=["GET"])
@require_auth
def get_tasks():
    current_user = request.current_user
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

    tasks = task_service.get_all_tasks(
        user_id=current_user["id"],
        status=status,
        priority=priority
    )
    return jsonify(tasks), 200


@app.route("/tasks/summary", methods=["GET"])
@require_auth
def get_summary():
    current_user = request.current_user
    summary = task_service.get_summary(current_user["id"])
    return jsonify(summary), 200


@app.route("/tasks/overdue", methods=["GET"])
@require_auth
def get_overdue_tasks():
    current_user = request.current_user
    tasks = task_service.get_overdue_tasks(current_user["id"])
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
@require_auth
def get_task(task_id):
    current_user = request.current_user
    task = task_service.get_task_by_id(task_id, current_user["id"])

    if not task:
        return jsonify({"error": "Task not found."}), 404

    return jsonify(task), 200


@app.route("/tasks", methods=["POST"])
@require_auth
def create_task():
    current_user = request.current_user
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
        due_date=data["due_date"].strip(),
        user_id=current_user["id"]
    )

    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
@require_auth
def update_task(task_id):
    current_user = request.current_user
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
        due_date=data["due_date"].strip(),
        user_id=current_user["id"]
    )

    if not updated_task:
        return jsonify({"error": "Task not found."}), 404

    return jsonify(updated_task), 200


@app.route("/tasks/<int:task_id>/status", methods=["PATCH"])
@require_auth
def update_task_status(task_id):
    current_user = request.current_user
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_status_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    updated_task = task_service.update_task_status(
        task_id=task_id,
        status=data["status"].strip().lower(),
        user_id=current_user["id"]
    )

    if not updated_task:
        return jsonify({"error": "Task not found."}), 404

    return jsonify(updated_task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@require_auth
def delete_task(task_id):
    current_user = request.current_user
    deleted = task_service.delete_task(task_id, current_user["id"])

    if not deleted:
        return jsonify({"error": "Task not found."}), 404

    return jsonify({"message": "Task deleted successfully."}), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)