from datetime import datetime
from database import initialize_database
from expense_manager import ExpenseManager


def print_menu():
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Total Spent")
    print("4. View Spending by Category")
    print("5. Filter Expenses by Category")
    print("6. Delete Expense")
    print("7. Update Expense")
    print("8. Export Expenses to CSV")
    print("9. Exit")


def print_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\nID | Title | Category | Amount | Date")
    print("-" * 60)
    for expense in expenses:
        expense_id, title, category, amount, expense_date = expense
        print(f"{expense_id} | {title} | {category} | ${amount:.2f} | {expense_date}")


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_expense_input():
    title = input("Enter expense title: ").strip()
    category = input("Enter category: ").strip()
    amount_input = input("Enter amount: ").strip()
    expense_date = input("Enter date (YYYY-MM-DD): ").strip()

    if not title or not category or not expense_date:
        print("All fields are required and cannot be empty.")
        return None

    try:
        amount = float(amount_input)
        if amount <= 0:
            print("Amount must be greater than 0.")
            return None
    except ValueError:
        print("Invalid amount.")
        return None

    if not is_valid_date(expense_date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return None

    return title, category, amount, expense_date


def main():
    initialize_database()
    manager = ExpenseManager()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            expense_data = get_expense_input()
            if expense_data is None:
                continue

            title, category, amount, expense_date = expense_data
            manager.add_expense(title, category, amount, expense_date)
            print("Expense added successfully.")

        elif choice == "2":
            expenses = manager.view_expenses()
            print_expenses(expenses)

        elif choice == "3":
            total = manager.get_total_spent()
            print(f"\nTotal spent: ${total:.2f}")

        elif choice == "4":
            summary = manager.get_category_summary()
            if not summary:
                print("No expense data found.")
            else:
                print("\nCategory | Total Spent")
                print("-" * 40)
                for category, total in summary:
                    print(f"{category} | ${total:.2f}")

        elif choice == "5":
            category = input("Enter category to filter: ").strip()
            expenses = manager.filter_by_category(category)
            print_expenses(expenses)

        elif choice == "6":
            expense_id_input = input("Enter Expense ID to delete: ").strip()

            try:
                expense_id = int(expense_id_input)
            except ValueError:
                print("Invalid ID.")
                continue

            deleted = manager.delete_expense(expense_id)

            if deleted:
                print("Expense deleted successfully.")
            else:
                print("Expense not found.")

        elif choice == "7":
            expense_id_input = input("Enter Expense ID to update: ").strip()

            try:
                expense_id = int(expense_id_input)
            except ValueError:
                print("Invalid ID.")
                continue

            expense_data = get_expense_input()
            if expense_data is None:
                continue

            title, category, amount, expense_date = expense_data
            updated = manager.update_expense(
                expense_id, title, category, amount, expense_date
            )

            if updated:
                print("Expense updated successfully.")
            else:
                print("Expense not found.")

        elif choice == "8":
            file_name = manager.export_to_csv()
            print(f"Expenses exported successfully to {file_name}")

        elif choice == "9":
            print("Exiting Expense Tracker.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()