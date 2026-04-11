from datetime import datetime
from flask import Flask, jsonify, request # type: ignore

from database import initialize_database # type: ignore
from expense_service import ExpenseService # type: ignore

app = Flask(__name__)
expense_service = ExpenseService()


def validate_expense_payload(data):
    required_fields = ["title", "category", "amount", "expense_date"]

    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"

    title = str(data["title"]).strip()
    category = str(data["category"]).strip()
    expense_date = str(data["expense_date"]).strip()

    if not title:
        return "Title cannot be empty."

    if not category:
        return "Category cannot be empty."

    try:
        amount = float(data["amount"])
        if amount <= 0:
            return "Amount must be greater than 0."
    except (ValueError, TypeError):
        return "Amount must be a valid number."

    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        return "Expense date must use YYYY-MM-DD format."

    return None


@app.route("/")
def home():
    return jsonify({
        "message": "Expense Tracker API is running",
        "endpoints": [
            "GET /expenses",
            "GET /expenses/<id>",
            "POST /expenses",
            "PUT /expenses/<id>",
            "DELETE /expenses/<id>"
        ]
    })


@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = expense_service.get_all_expenses()
    return jsonify(expenses), 200


@app.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = expense_service.get_expense_by_id(expense_id)

    if not expense:
        return jsonify({"error": "Expense not found."}), 404

    return jsonify(expense), 200


@app.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_expense_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    new_expense = expense_service.create_expense(
        title=data["title"].strip(),
        category=data["category"].strip(),
        amount=float(data["amount"]),
        expense_date=data["expense_date"].strip()
    )

    return jsonify(new_expense), 201


@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    validation_error = validate_expense_payload(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    updated_expense = expense_service.update_expense(
        expense_id=expense_id,
        title=data["title"].strip(),
        category=data["category"].strip(),
        amount=float(data["amount"]),
        expense_date=data["expense_date"].strip()
    )

    if not updated_expense:
        return jsonify({"error": "Expense not found."}), 404

    return jsonify(updated_expense), 200


@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    deleted = expense_service.delete_expense(expense_id)

    if not deleted:
        return jsonify({"error": "Expense not found."}), 404

    return jsonify({"message": "Expense deleted successfully."}), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)