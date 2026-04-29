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

    def get_monthly_summary(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                SUBSTR(expense_date, 1, 7) as month,
                COUNT(*) as expense_count,
                COALESCE(SUM(amount), 0) as total_spending
            FROM expenses
            GROUP BY month
            ORDER BY month DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append({
                "month": row["month"],
                "expense_count": row["expense_count"],
                "total_spending": round(row["total_spending"], 2)
            })

        return result

    def set_budget(self, category, month, budget_amount):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO budgets (category, month, budget_amount)
            VALUES (?, ?, ?)
            ON CONFLICT(category, month)
            DO UPDATE SET budget_amount = excluded.budget_amount
        """, (category, month, budget_amount))

        conn.commit()
        conn.close()

        return self.get_budget(category, month)

    def get_budget(self, category, month):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, category, month, budget_amount
            FROM budgets
            WHERE category = ? AND month = ?
        """, (category, month))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_all_budgets(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, category, month, budget_amount
            FROM budgets
            ORDER BY month DESC, category ASC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_budget_status(self, month):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                b.category,
                b.month,
                b.budget_amount,
                COALESCE(SUM(e.amount), 0) as actual_spending
            FROM budgets b
            LEFT JOIN expenses e
                ON b.category = e.category
                AND SUBSTR(e.expense_date, 1, 7) = b.month
            WHERE b.month = ?
            GROUP BY b.category, b.month, b.budget_amount
            ORDER BY b.category ASC
        """, (month,))

        rows = cursor.fetchall()
        conn.close()

        result = []

        for row in rows:
            actual_spending = round(row["actual_spending"], 2)
            budget_amount = round(row["budget_amount"], 2)
            remaining = round(budget_amount - actual_spending, 2)

            result.append({
                "category": row["category"],
                "month": row["month"],
                "budget_amount": budget_amount,
                "actual_spending": actual_spending,
                "remaining": remaining,
                "is_overspent": actual_spending > budget_amount
            })

        return result