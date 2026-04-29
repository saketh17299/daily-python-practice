from database import get_connection


class ExpenseService:
    def get_all_expenses(self, category=None, start_date=None, end_date=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, title, amount, category, expense_date, notes
            FROM expenses
            WHERE 1=1
        """
        params = []

        if category:
            query += " AND category = ?"
            params.append(category)

        if start_date:
            query += " AND expense_date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND expense_date <= ?"
            params.append(end_date)

        query += " ORDER BY expense_date DESC, id DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_expense_by_id(self, expense_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, amount, category, expense_date, notes
            FROM expenses
            WHERE id = ?
        """, (expense_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def create_expense(self, title, amount, category, expense_date, notes):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (title, amount, category, expense_date, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (title, amount, category, expense_date, notes))

        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()

        return self.get_expense_by_id(expense_id)

    def update_expense(self, expense_id, title, amount, category, expense_date, notes):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET title = ?, amount = ?, category = ?, expense_date = ?, notes = ?
            WHERE id = ?
        """, (title, amount, category, expense_date, notes, expense_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_expense_by_id(expense_id)

    def delete_expense(self, expense_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ?
        """, (expense_id,))

        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0

    def get_analytics(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) as expense_count,
                   COALESCE(SUM(amount), 0) as total_spending
            FROM expenses
        """)
        summary = dict(cursor.fetchone())

        cursor.execute("""
            SELECT category,
                   COALESCE(SUM(amount), 0) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """)
        category_totals = [dict(row) for row in cursor.fetchall()]

        highest_category = category_totals[0] if category_totals else None

        conn.close()

        return {
            "expense_count": summary["expense_count"],
            "total_spending": round(summary["total_spending"], 2),
            "highest_spending_category": highest_category,
            "category_totals": category_totals
        }