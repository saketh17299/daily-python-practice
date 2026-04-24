import os
import uuid
from flask import Flask, jsonify, request, send_from_directory

from database import initialize_database
from file_service import FileService

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

file_service = FileService()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "File Upload API is running",
        "endpoints": [
            "POST /upload",
            "GET /files",
            "GET /files/<id>/download"
        ],
        "next_improvements": [
            "delete file",
            "file type validation",
            "authentication",
            "cloud storage integration"
        ]
    })


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    unique_name = str(uuid.uuid4())
    stored_name = unique_name + "_" + file.filename

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], stored_name)
    file.save(file_path)

    file_size = os.path.getsize(file_path)

    saved_file = file_service.save_file_metadata(
        filename=file.filename,
        stored_name=stored_name,
        file_size=file_size
    )

    return jsonify(saved_file), 201


@app.route("/files", methods=["GET"])
def get_files():
    files = file_service.get_all_files()
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


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)