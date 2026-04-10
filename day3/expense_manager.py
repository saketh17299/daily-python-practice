from database import get_connection


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