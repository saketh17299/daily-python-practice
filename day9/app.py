from flask import Flask, jsonify, request

from database import initialize_database
from student_service import StudentService

app = Flask(__name__)
student_service = StudentService()


def is_valid_marks(value):
    try:
        marks = float(value)
        return 0 <= marks <= 100
    except (ValueError, TypeError):
        return False


def validate_student_payload(data):
    required_fields = ["name", "math_marks", "science_marks", "english_marks"]

    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"

    name = str(data["name"]).strip()

    if not name:
        return "Name cannot be empty."

    if not is_valid_marks(data["math_marks"]):
        return "Math marks must be a number between 0 and 100."

    if not is_valid_marks(data["science_marks"]):
        return "Science marks must be a number between 0 and 100."

    if not is_valid_marks(data["english_marks"]):
        return "English marks must be a number between 0 and 100."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Student Grades API is running",
        "endpoints": [
            "GET /students",
            "GET /students?result=Pass",
            "GET /students?result=Fail",
            "GET /students/<id>",
            "POST /students",
            "PUT /students/<id>",
            "DELETE /students/<id>"
        ],
        "next_improvements": [
            "topper endpoint",
            "search by student name",
            "pagination",
            "subject-wise analytics"
        ]
    })


@app.route("/students", methods=["GET"])
def get_students():
    result_filter = request.args.get("result")
    students = student_service.get_all_students()

    if result_filter:
        result_filter = result_filter.strip().capitalize()
        if result_filter not in {"Pass", "Fail"}:
            return jsonify({"error": "Result filter must be Pass or Fail."}), 400
        students = [student for student in students if student["result"] == result_filter]

    return jsonify(students), 200


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = student_service.get_student_by_id(student_id)

    if not student:
        return jsonify({"error": "Student not found."}), 404

    return jsonify(student), 200


@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_student_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    new_student = student_service.create_student(
        name=str(data["name"]).strip(),
        math_marks=float(data["math_marks"]),
        science_marks=float(data["science_marks"]),
        english_marks=float(data["english_marks"])
    )

    return jsonify(new_student), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_student_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    updated_student = student_service.update_student(
        student_id=student_id,
        name=str(data["name"]).strip(),
        math_marks=float(data["math_marks"]),
        science_marks=float(data["science_marks"]),
        english_marks=float(data["english_marks"])
    )

    if not updated_student:
        return jsonify({"error": "Student not found."}), 404

    return jsonify(updated_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    deleted = student_service.delete_student(student_id)

    if not deleted:
        return jsonify({"error": "Student not found."}), 404

    return jsonify({"message": "Student deleted successfully."}), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)