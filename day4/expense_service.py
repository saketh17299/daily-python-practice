from database import get_connection


class ExpenseService:
    def get_all_expenses(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, category, amount, expense_date
            FROM expenses
            ORDER BY expense_date ASC, id ASC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_expense_by_id(self, expense_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, category, amount, expense_date
            FROM expenses
            WHERE id = ?
        """, (expense_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def create_expense(self, title, category, amount, expense_date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (title, category, amount, expense_date)
            VALUES (?, ?, ?, ?)
        """, (title, category, amount, expense_date))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return self.get_expense_by_id(new_id)

    def update_expense(self, expense_id, title, category, amount, expense_date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET title = ?, category = ?, amount = ?, expense_date = ?
            WHERE id = ?
        """, (title, category, amount, expense_date, expense_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_expense_by_id(expense_id)

    def delete_expense(self, expense_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()

        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0