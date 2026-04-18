from flask import Flask, jsonify, request

from database import initialize_database
from note_service import NoteService

app = Flask(__name__)
note_service = NoteService()


def validate_note_payload(data):
    required_fields = ["title", "content", "tags"]

    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"

    title = str(data["title"]).strip()
    content = str(data["content"]).strip()
    tags = str(data["tags"]).strip()

    if not title:
        return "Title cannot be empty."

    if not content:
        return "Content cannot be empty."

    if not tags:
        return "Tags cannot be empty."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Notes API is running",
        "endpoints": [
            "GET /notes",
            "GET /notes/archived",
            "GET /notes/<id>",
            "POST /notes",
            "PUT /notes/<id>",
            "PATCH /notes/<id>/archive",
            "DELETE /notes/<id>",
            "GET /notes/search?q=keyword",
            "GET /notes/tag/<tag>"
        ],
        "next_improvements": [
            "favorite notes",
            "pagination",
            "authentication",
            "restore archived notes"
        ]
    })


@app.route("/notes", methods=["GET"])
def get_notes():
    notes = note_service.get_all_notes()
    return jsonify(notes), 200


@app.route("/notes/archived", methods=["GET"])
def get_archived_notes():
    notes = note_service.get_archived_notes()
    return jsonify(notes), 200


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = note_service.get_note_by_id(note_id)

    if not note:
        return jsonify({"error": "Note not found."}), 404

    return jsonify(note), 200


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_note_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    new_note = note_service.create_note(
        title=data["title"].strip(),
        content=data["content"].strip(),
        tags=data["tags"].strip()
    )

    return jsonify(new_note), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_note_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    updated_note = note_service.update_note(
        note_id=note_id,
        title=data["title"].strip(),
        content=data["content"].strip(),
        tags=data["tags"].strip()
    )

    if not updated_note:
        return jsonify({"error": "Active note not found."}), 404

    return jsonify(updated_note), 200


@app.route("/notes/<int:note_id>/archive", methods=["PATCH"])
def archive_note(note_id):
    archived_note = note_service.archive_note(note_id)

    if not archived_note:
        return jsonify({"error": "Active note not found or already archived."}), 404

    return jsonify({
        "message": "Note archived successfully.",
        "note": archived_note
    }), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    deleted = note_service.delete_note(note_id)

    if not deleted:
        return jsonify({"error": "Note not found."}), 404

    return jsonify({"message": "Note deleted successfully."}), 200


@app.route("/notes/search", methods=["GET"])
def search_notes():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Search query parameter 'q' is required."}), 400

    results = note_service.search_notes(query)
    return jsonify(results), 200


@app.route("/notes/tag/<string:tag>", methods=["GET"])
def get_notes_by_tag(tag):
    cleaned_tag = tag.strip()

    if not cleaned_tag:
        return jsonify({"error": "Tag cannot be empty."}), 400

    notes = note_service.get_notes_by_tag(cleaned_tag)
    return jsonify(notes), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)