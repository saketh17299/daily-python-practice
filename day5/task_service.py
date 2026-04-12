from datetime import datetime
from database import get_connection


class TaskService:
    def get_all_tasks(self, status=None, priority=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, title, description, status, priority, due_date
            FROM tasks
            WHERE 1=1
        """
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        if priority:
            query += " AND priority = ?"
            params.append(priority)

        query += " ORDER BY due_date ASC, id ASC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_task_by_id(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, description, status, priority, due_date
            FROM tasks
            WHERE id = ?
        """, (task_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def create_task(self, title, description, status, priority, due_date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, description, status, priority, due_date)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, status, priority, due_date))

        conn.commit()
        task_id = cursor.lastrowid
        conn.close()

        return self.get_task_by_id(task_id)

    def update_task(self, task_id, title, description, status, priority, due_date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET title = ?, description = ?, status = ?, priority = ?, due_date = ?
            WHERE id = ?
        """, (title, description, status, priority, due_date, task_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_task_by_id(task_id)

    def update_task_status(self, task_id, status):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """, (status, task_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_task_by_id(task_id)

    def delete_task(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0

    def get_summary(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM tasks
            GROUP BY status
            ORDER BY count DESC, status ASC
        """)
        status_summary = cursor.fetchall()

        cursor.execute("""
            SELECT priority, COUNT(*) as count
            FROM tasks
            GROUP BY priority
            ORDER BY count DESC, priority ASC
        """)
        priority_summary = cursor.fetchall()

        conn.close()

        return {
            "status_summary": [dict(row) for row in status_summary],
            "priority_summary": [dict(row) for row in priority_summary]
        }

    def get_overdue_tasks(self):
        conn = get_connection()
        cursor = conn.cursor()

        today = datetime.today().strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT id, title, description, status, priority, due_date
            FROM tasks
            WHERE due_date < ? AND status != 'completed'
            ORDER BY due_date ASC, id ASC
        """, (today,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]