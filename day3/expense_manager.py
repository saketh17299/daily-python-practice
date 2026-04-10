from database import get_connection
import csv


class ExpenseManager:
    def add_expense(self, title, category, amount, expense_date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (title, category, amount, expense_date)
            VALUES (?, ?, ?, ?)
        """, (title, category, amount, expense_date))

        conn.commit()
        conn.close()

    def view_expenses(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, category, amount, expense_date
            FROM expenses
            ORDER BY expense_date ASC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_total_spent(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
        total = cursor.fetchone()[0]

        conn.close()
        return total

    def get_category_summary(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)
        rows = cursor.fetchall()

        conn.close()
        return rows

    def filter_by_category(self, category):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, category, amount, expense_date
            FROM expenses
            WHERE category = ?
            ORDER BY expense_date ASC
        """, (category,))
        rows = cursor.fetchall()

        conn.close()
        return rows

    def delete_expense(self, expense_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()

        rows_deleted = cursor.rowcount
        conn.close()

        return rows_deleted

    def update_expense(self, expense_id, title, category, amount, expense_date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET title = ?, category = ?, amount = ?, expense_date = ?
            WHERE id = ?
        """, (title, category, amount, expense_date, expense_id))

        conn.commit()
        rows_updated = cursor.rowcount
        conn.close()

        return rows_updated

    def export_to_csv(self, output_file="expenses_export.csv"):
        expenses = self.view_expenses()

        with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["ID", "Title", "Category", "Amount", "Date"])
            writer.writerows(expenses)

        return output_file