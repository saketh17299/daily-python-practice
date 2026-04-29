from datetime import datetime
from flask import Flask, jsonify, request

from database import initialize_database
from expense_service import ExpenseService

app = Flask(__name__)
expense_service = ExpenseService()

VALID_CATEGORIES = {"food", "travel", "shopping", "bills", "health", "other"}


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_expense_payload(data):
    required_fields = ["title", "amount", "category", "expense_date"]

    for field in required_fields:
        if field not in data:
            return f"Missing field: {field}"

    title = str(data["title"]).strip()
    category = str(data["category"]).strip().lower()

    if not title:
        return "Title cannot be empty."

    try:
        amount = float(data["amount"])
        if amount <= 0:
            return "Amount must be positive."
    except:
        return "Invalid amount."

    if category not in VALID_CATEGORIES:
        return f"Invalid category. Use {VALID_CATEGORIES}"

    if not is_valid_date(data["expense_date"]):
        return "Invalid date format (YYYY-MM-DD)."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Expense Tracker API",
        "endpoints": [
            "GET /expenses",
            "GET /expenses?category=food",
            "GET /expenses?start_date=2026-04-01&end_date=2026-04-30",
            "POST /expenses",
            "PUT /expenses/<id>",
            "DELETE /expenses/<id>"
        ],
        "next_improvements": [
            "monthly summary",
            "category totals",
            "budget tracking",
            "charts API"
        ]
    })


@app.route("/expenses", methods=["GET"])
def get_expenses():
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if category:
        category = category.lower()
        if category not in VALID_CATEGORIES:
            return jsonify({"error": "Invalid category"}), 400

    expenses = expense_service.get_all_expenses(category, start_date, end_date)
    return jsonify(expenses), 200


@app.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json()

    error = validate_expense_payload(data)
    if error:
        return jsonify({"error": error}), 400

    expense = expense_service.create_expense(
        data["title"],
        float(data["amount"]),
        data["category"].lower(),
        data["expense_date"],
        data.get("notes", "")
    )

    return jsonify(expense), 201


@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json()

    error = validate_expense_payload(data)
    if error:
        return jsonify({"error": error}), 400

    expense = expense_service.update_expense(
        expense_id,
        data["title"],
        float(data["amount"]),
        data["category"].lower(),
        data["expense_date"],
        data.get("notes", "")
    )

    if not expense:
        return jsonify({"error": "Not found"}), 404

    return jsonify(expense), 200


@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    deleted = expense_service.delete_expense(expense_id)

    if not deleted:
        return jsonify({"error": "Not found"}), 404

    return jsonify({"message": "Deleted successfully"}), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)