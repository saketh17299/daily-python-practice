import os
import uuid
from flask import Flask, jsonify, request, send_from_directory

from database import initialize_database
from file_service import FileService

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

file_service = FileService()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def is_allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "File Upload API is running",
        "endpoints": [
            "POST /upload",
            "GET /files",
            "GET /files?type=pdf",
            "GET /files/<id>/download",
            "GET /files/<id>/preview",
            "DELETE /files/<id>"
        ],
        "allowed_file_types": list(ALLOWED_EXTENSIONS),
        "max_file_size_mb": 5
    })


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not is_allowed_file(file.filename):
        return jsonify({
            "error": "File type not allowed.",
            "allowed_types": list(ALLOWED_EXTENSIONS)
        }), 400

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return jsonify({"error": "File size exceeds 5 MB limit."}), 400

    unique_name = str(uuid.uuid4())
    stored_name = unique_name + "_" + file.filename

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], stored_name)
    file.save(file_path)

    saved_file = file_service.save_file_metadata(
        filename=file.filename,
        stored_name=stored_name,
        file_size=file_size
    )

    return jsonify(saved_file), 201


@app.route("/files", methods=["GET"])
def get_files():
    file_type = request.args.get("type")

    if file_type:
        file_type = file_type.strip().lower()
        if file_type not in ALLOWED_EXTENSIONS:
            return jsonify({
                "error": "Invalid file type filter.",
                "allowed_types": list(ALLOWED_EXTENSIONS)
            }), 400

    files = file_service.get_all_files(file_type=file_type)
    return jsonify(files), 200


@app.route("/files/<int:file_id>/download", methods=["GET"])
def download_file(file_id):
    file = file_service.get_file_by_id(file_id)

    if not file:
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(
        directory=app.config["UPLOAD_FOLDER"],
        path=file["stored_name"],
        as_attachment=True
    )


@app.route("/files/<int:file_id>/preview", methods=["GET"])
def preview_file(file_id):
    file = file_service.get_file_by_id(file_id)

    if not file:
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(
        directory=app.config["UPLOAD_FOLDER"],
        path=file["stored_name"],
        as_attachment=False
    )


@app.route("/files/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    file = file_service.get_file_by_id(file_id)

    if not file:
        return jsonify({"error": "File not found"}), 404

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file["stored_name"])

    if os.path.exists(file_path):
        os.remove(file_path)

    deleted = file_service.delete_file_metadata(file_id)

    if not deleted:
        return jsonify({"error": "Could not delete file metadata"}), 500

    return jsonify({"message": "File deleted successfully"}), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)