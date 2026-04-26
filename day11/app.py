from datetime import datetime
from flask import Flask, jsonify, request

from database import initialize_database
from journal_service import JournalService

app = Flask(__name__)
journal_service = JournalService()

VALID_MOODS = {"happy", "neutral", "sad", "tired", "focused", "stressed"}


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_productivity_score(score):
    try:
        value = int(score)
        return 1 <= value <= 10
    except (ValueError, TypeError):
        return False


def validate_entry_payload(data):
    required_fields = [
        "entry_date",
        "weather",
        "mood",
        "productivity_score",
        "notes"
    ]

    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"

    entry_date = str(data["entry_date"]).strip()
    weather = str(data["weather"]).strip()
    mood = str(data["mood"]).strip().lower()
    notes = str(data["notes"]).strip()

    if not is_valid_date(entry_date):
        return "Entry date must be in YYYY-MM-DD format."

    if not weather:
        return "Weather cannot be empty."

    if mood not in VALID_MOODS:
        return "Mood must be one of: happy, neutral, sad, tired, focused, stressed."

    if not is_valid_productivity_score(data["productivity_score"]):
        return "Productivity score must be an integer between 1 and 10."

    if not notes:
        return "Notes cannot be empty."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Weather Journal API is running",
        "endpoints": [
            "GET /entries",
            "GET /entries/<id>",
            "POST /entries",
            "PUT /entries/<id>",
            "DELETE /entries/<id>"
        ],
        "next_improvements": [
            "filter by mood",
            "weekly productivity summary",
            "average productivity score",
            "date range filter"
        ]
    })


@app.route("/entries", methods=["GET"])
def get_entries():
    entries = journal_service.get_all_entries()
    return jsonify(entries), 200


@app.route("/entries/<int:entry_id>", methods=["GET"])
def get_entry(entry_id):
    entry = journal_service.get_entry_by_id(entry_id)

    if not entry:
        return jsonify({"error": "Journal entry not found."}), 404

    return jsonify(entry), 200


@app.route("/entries", methods=["POST"])
def create_entry():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_entry_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    new_entry = journal_service.create_entry(
        entry_date=str(data["entry_date"]).strip(),
        weather=str(data["weather"]).strip(),
        mood=str(data["mood"]).strip().lower(),
        productivity_score=int(data["productivity_score"]),
        notes=str(data["notes"]).strip()
    )

    return jsonify(new_entry), 201


@app.route("/entries/<int:entry_id>", methods=["PUT"])
def update_entry(entry_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_entry_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    updated_entry = journal_service.update_entry(
        entry_id=entry_id,
        entry_date=str(data["entry_date"]).strip(),
        weather=str(data["weather"]).strip(),
        mood=str(data["mood"]).strip().lower(),
        productivity_score=int(data["productivity_score"]),
        notes=str(data["notes"]).strip()
    )

    if not updated_entry:
        return jsonify({"error": "Journal entry not found."}), 404

    return jsonify(updated_entry), 200


@app.route("/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    deleted = journal_service.delete_entry(entry_id)

    if not deleted:
        return jsonify({"error": "Journal entry not found."}), 404

    return jsonify({"message": "Journal entry deleted successfully."}), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)