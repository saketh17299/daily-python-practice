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


def is_valid_month(month_text):
    try:
        datetime.strptime(month_text, "%Y-%m")
        return True
    except ValueError:
        return False


def validate_expense_payload(data):
    if not data:
        return "Request body must be valid JSON."

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
    except (ValueError, TypeError):
        return "Invalid amount."

    if category not in VALID_CATEGORIES:
        return "Invalid category."

    if not is_valid_date(data["expense_date"]):
        return "Invalid date format. Use YYYY-MM-DD."

    return None


def validate_budget_payload(data):
    if not data:
        return "Request body must be valid JSON."

    required_fields = ["category", "month", "budget_amount"]

    for field in required_fields:
        if field not in data:
            return f"Missing field: {field}"

    category = str(data["category"]).strip().lower()
    month = str(data["month"]).strip()

    if category not in VALID_CATEGORIES:
        return "Invalid category."

    if not is_valid_month(month):
        return "Month must be in YYYY-MM format."

    try:
        budget_amount = float(data["budget_amount"])
        if budget_amount <= 0:
            return "Budget amount must be positive."
    except (ValueError, TypeError):
        return "Invalid budget amount."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Expense Tracker API",
        "endpoints": [
            "GET /expenses",
            "GET /expenses?category=food",
            "GET /expenses?start_date=2026-04-01&end_date=2026-04-30",
            "GET /expenses/analytics",
            "GET /expenses/monthly-summary",
            "POST /expenses",
            "PUT /expenses/<id>",
            "DELETE /expenses/<id>",
            "POST /budgets",
            "GET /budgets",
            "GET /budgets/status?month=2026-04"
        ]
    })


@app.route("/expenses", methods=["GET"])
def get_expenses():
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if category:
        category = category.strip().lower()
        if category not in VALID_CATEGORIES:
            return jsonify({"error": "Invalid category"}), 400

    if start_date and not is_valid_date(start_date):
        return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD."}), 400

    if end_date and not is_valid_date(end_date):
        return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD."}), 400

    expenses = expense_service.get_all_expenses(category, start_date, end_date)
    return jsonify(expenses), 200


@app.route("/expenses/analytics", methods=["GET"])
def get_expense_analytics():
    analytics = expense_service.get_analytics()
    return jsonify(analytics), 200


@app.route("/expenses/monthly-summary", methods=["GET"])
def get_monthly_summary():
    summary = expense_service.get_monthly_summary()
    return jsonify(summary), 200


@app.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json()

    error = validate_expense_payload(data)
    if error:
        return jsonify({"error": error}), 400

    expense = expense_service.create_expense(
        title=str(data["title"]).strip(),
        amount=float(data["amount"]),
        category=str(data["category"]).strip().lower(),
        expense_date=str(data["expense_date"]).strip(),
        notes=data.get("notes", "")
    )

    return jsonify(expense), 201


@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json()

    error = validate_expense_payload(data)
    if error:
        return jsonify({"error": error}), 400

    expense = expense_service.update_expense(
        expense_id=expense_id,
        title=str(data["title"]).strip(),
        amount=float(data["amount"]),
        category=str(data["category"]).strip().lower(),
        expense_date=str(data["expense_date"]).strip(),
        notes=data.get("notes", "")
    )

    if not expense:
        return jsonify({"error": "Expense not found."}), 404

    return jsonify(expense), 200


@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    deleted = expense_service.delete_expense(expense_id)

    if not deleted:
        return jsonify({"error": "Expense not found."}), 404

    return jsonify({"message": "Deleted successfully"}), 200


@app.route("/budgets", methods=["POST"])
def set_budget():
    data = request.get_json()

    error = validate_budget_payload(data)
    if error:
        return jsonify({"error": error}), 400

    budget = expense_service.set_budget(
        category=str(data["category"]).strip().lower(),
        month=str(data["month"]).strip(),
        budget_amount=float(data["budget_amount"])
    )

    return jsonify(budget), 201


@app.route("/budgets", methods=["GET"])
def get_budgets():
    budgets = expense_service.get_all_budgets()
    return jsonify(budgets), 200


@app.route("/budgets/status", methods=["GET"])
def get_budget_status():
    month = request.args.get("month")

    if not month:
        return jsonify({"error": "month query parameter is required."}), 400

    month = month.strip()

    if not is_valid_month(month):
        return jsonify({"error": "Month must be in YYYY-MM format."}), 400

    status = expense_service.get_budget_status(month)
    return jsonify(status), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)