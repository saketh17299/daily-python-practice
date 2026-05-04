from datetime import datetime
from flask import Flask, jsonify, request

from database import initialize_database
from application_service import ApplicationService

app = Flask(__name__)
application_service = ApplicationService()

VALID_STATUSES = {
    "applied",
    "interview",
    "offer",
    "rejected",
    "withdrawn"
}


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_application_payload(data):
    if not data:
        return "Request body must be valid JSON."

    required_fields = ["company", "role", "status", "applied_date"]

    for field in required_fields:
        if field not in data:
            return f"Missing field: {field}"

    company = str(data["company"]).strip()
    role = str(data["role"]).strip()
    status = str(data["status"]).strip().lower()
    applied_date = str(data["applied_date"]).strip()

    if not company:
        return "Company cannot be empty."

    if not role:
        return "Role cannot be empty."

    if status not in VALID_STATUSES:
        return "Invalid status."

    if not is_valid_date(applied_date):
        return "Applied date must be in YYYY-MM-DD format."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Job Application Tracker API is running",
        "endpoints": [
            "GET /applications",
            "GET /applications?status=applied",
            "GET /applications/analytics",
            "GET /applications/<id>",
            "POST /applications",
            "PUT /applications/<id>",
            "DELETE /applications/<id>"
        ],
        "valid_statuses": list(VALID_STATUSES),
        "next_improvements": [
            "interview date tracking",
            "follow-up reminders",
            "export applications to CSV",
            "search by company or role"
        ]
    })


@app.route("/applications", methods=["GET"])
def get_applications():
    status = request.args.get("status")

    if status:
        status = status.strip().lower()
        if status not in VALID_STATUSES:
            return jsonify({"error": "Invalid status"}), 400

    applications = application_service.get_all_applications(status)
    return jsonify(applications), 200


@app.route("/applications/analytics", methods=["GET"])
def get_analytics():
    analytics = application_service.get_analytics()
    return jsonify(analytics), 200


@app.route("/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):
    application = application_service.get_application_by_id(application_id)

    if not application:
        return jsonify({"error": "Application not found."}), 404

    return jsonify(application), 200


@app.route("/applications", methods=["POST"])
def create_application():
    data = request.get_json()

    error = validate_application_payload(data)
    if error:
        return jsonify({"error": error}), 400

    application = application_service.create_application(
        company=str(data["company"]).strip(),
        role=str(data["role"]).strip(),
        status=str(data["status"]).strip().lower(),
        applied_date=str(data["applied_date"]).strip(),
        notes=data.get("notes", "")
    )

    return jsonify(application), 201


@app.route("/applications/<int:application_id>", methods=["PUT"])
def update_application(application_id):
    data = request.get_json()

    error = validate_application_payload(data)
    if error:
        return jsonify({"error": error}), 400

    application = application_service.update_application(
        application_id=application_id,
        company=str(data["company"]).strip(),
        role=str(data["role"]).strip(),
        status=str(data["status"]).strip().lower(),
        applied_date=str(data["applied_date"]).strip(),
        notes=data.get("notes", "")
    )

    if not application:
        return jsonify({"error": "Application not found."}), 404

    return jsonify(application), 200


@app.route("/applications/<int:application_id>", methods=["DELETE"])
def delete_application(application_id):
    deleted = application_service.delete_application(application_id)

    if not deleted:
        return jsonify({"error": "Application not found."}), 404

    return jsonify({"message": "Application deleted successfully."}), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)